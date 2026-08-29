"""Unit-тесты oleg_pipeline без вызовов LLM: судья, цепочка примеров, изоляция ошибок движка.

Запуск: python -m unittest oleg_pipeline.test_pipeline -v
"""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest

from oleg_pipeline import cli


def _make_scenario(examples: Path, name: str, expected: str) -> None:
    root = examples / name
    (root / "input").mkdir(parents=True)
    (root / "input" / "source.txt").write_text(f"источник {name}\n", encoding="utf-8")
    (root / "expected.md").write_text(expected, encoding="utf-8")


class JudgeParsingTests(unittest.TestCase):
    def test_valid_pass_verdict(self) -> None:
        verdict = cli._parse_json_object(
            json.dumps({"pass": True, "reason": "всё совпало", "facts": [{"fact": "срок 2026-09-01", "ok": True}]})
        )
        self.assertIs(verdict["pass"], True)
        self.assertEqual(verdict["reason"], "всё совпало")

    def test_pass_true_with_failed_fact_is_fail(self) -> None:
        raw = json.dumps(
            {
                "pass": True,
                "reason": "судья ошибся",
                "facts": [{"fact": "исполнитель Иванов", "ok": True}, {"fact": "сумма 500 руб.", "ok": False}],
            },
            ensure_ascii=False,
        )
        verdict = cli._parse_json_object(raw)
        self.assertIs(verdict["pass"], False)
        self.assertIn("сумма 500 руб.", verdict["reason"])

    def test_invalid_json_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            cli._parse_json_object("это не json")
        with self.assertRaises(ValueError):
            cli._parse_json_object('{"pass": true, "reason": "x"}')  # нет facts

    def test_invalid_json_goes_through_retry_path(self) -> None:
        calls: list[str] = []

        def broken_codex(prompt: str, result_file: Path) -> dict[str, object]:
            calls.append("codex")
            return cli._parse_json_object("garbage ```")

        def broken_claude(prompt: str, result_file: Path) -> dict[str, object]:
            calls.append("claude")
            return cli._parse_json_object("{not json")

        with tempfile.TemporaryDirectory() as tmp:
            examples = Path(tmp) / "examples"
            _make_scenario(examples, "01-base", "# Ожидание\n")
            scenario = cli.discover_scenarios(examples)[0]
            original = (cli._run_codex_judge, cli._run_claude_judge)
            cli._run_codex_judge, cli._run_claude_judge = broken_codex, broken_claude
            try:
                with self.assertRaises(RuntimeError) as ctx:
                    cli.judge(scenario, "# реестр\n", "codex", Path(tmp))
            finally:
                cli._run_codex_judge, cli._run_claude_judge = original
        self.assertEqual(calls, ["codex", "codex", "claude", "claude"])
        message = str(ctx.exception)
        for expected in ("codex попытка 1", "codex попытка 2", "claude попытка 2"):
            self.assertIn(expected, message)


class ChainRuleTests(unittest.TestCase):
    def test_chain_marker_resolves_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            examples = Path(tmp) / "examples"
            _make_scenario(examples, "01-base", "# Базовый реестр\n")
            _make_scenario(examples, "02-chain", "# Продолжение\n\nПроверка идёт ПОВЕРХ реестра из примера 01.\n")
            scenarios = cli.discover_scenarios(examples)
            by_name = {s.name: s for s in scenarios}
            self.assertIsNone(by_name["01-base"].parent_token)
            self.assertIsNone(cli._find_parent(by_name["01-base"], scenarios))
            self.assertEqual(by_name["02-chain"].parent_token, "01")
            parent = cli._find_parent(by_name["02-chain"], scenarios)
            self.assertIsNotNone(parent)
            self.assertEqual(parent.name, "01-base")


class EngineIsolationTests(unittest.TestCase):
    def test_failing_engine_yields_fail_row_and_run_continues(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            examples = base / "examples"
            _make_scenario(examples, "01-bad", "# Сценарий с падением\n")
            _make_scenario(examples, "02-good", "# Обычный сценарий\n")
            engine = base / "engine.py"
            engine.write_text(
                textwrap.dedent(
                    """
                    import json, pathlib, sys
                    inp, reg = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
                    if "bad" in inp.parent.name:
                        sys.stderr.write("engine boom: synthetic failure\\n")
                        sys.exit(3)
                    reg.write_text(json.dumps({"items": []}), encoding="utf-8")
                    reg.with_suffix(".md").write_text("# registry\\n", encoding="utf-8")
                    """
                ),
                encoding="utf-8",
            )
            template = f"{cli._shell_quote(sys.executable)} {cli._shell_quote(engine)} {{input}} {{registry}}"
            out = base / "out"
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = cli.main(
                    ["run", "--examples", str(examples), "--engine", template, "--judge", "none", "--out", str(out), "--jobs", "1"]
                )
            self.assertEqual(code, 1)
            report = (out / "report.md").read_text(encoding="utf-8")
            self.assertIn("| `01-bad` | ENGINE FAIL |", report)
            self.assertIn("движок завершился с кодом 3", report)
            self.assertIn("engine boom: synthetic failure", report)
            self.assertIn("| `02-good` | ENGINE OK |", report)
            self.assertTrue((out / "02-good" / "registry.md").is_file())
            self.assertIn("ENGINE OK 02-good", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
