from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import datetime as dt
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import time
from typing import Iterable


PACKAGE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = PACKAGE_DIR / "judge_schema.json"
CHAIN_RE = re.compile(
    r"поверх\s+реестра\s+из\s+примера\s+([A-Za-zА-Яа-я]?\d{1,3})",
    re.IGNORECASE,
)
REFERENCE_RE = re.compile(
    r"(?:Опорное\s+время|Reference\s+(?:time|clock))[^\n\d]*(\d{4}-\d{2}-\d{2})",
    re.IGNORECASE,
)


@dataclasses.dataclass(frozen=True)
class Scenario:
    name: str
    root: Path
    input_dir: Path
    expected_path: Path
    expected: str
    parent_token: str | None
    now: str


@dataclasses.dataclass
class Result:
    scenario: Scenario
    passed: bool
    reason: str
    facts: list[dict[str, object]]
    registry_path: Path | None
    registry_md_path: Path | None
    engine_ok: bool
    engine_seconds: float
    judge_backend: str


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def discover_scenarios(examples_dir: Path) -> list[Scenario]:
    if not examples_dir.is_dir():
        raise ValueError(f"каталог примеров не найден: {examples_dir}")
    scenarios: list[Scenario] = []
    for root in sorted((p for p in examples_dir.iterdir() if p.is_dir()), key=lambda p: p.name.casefold()):
        expected_path = root / "expected.md"
        input_dir = root / "input"
        if not expected_path.is_file() or not input_dir.is_dir():
            continue
        expected = _read_text(expected_path)
        chain_match = CHAIN_RE.search(expected)
        reference_match = REFERENCE_RE.search(expected)
        scenarios.append(
            Scenario(
                name=root.name,
                root=root,
                input_dir=input_dir,
                expected_path=expected_path,
                expected=expected,
                parent_token=chain_match.group(1) if chain_match else None,
                now=reference_match.group(1) if reference_match else dt.date.today().isoformat(),
            )
        )
    if not scenarios:
        raise ValueError(f"в {examples_dir} нет каталогов с input/ и expected.md")
    return scenarios


def _find_parent(scenario: Scenario, all_scenarios: list[Scenario]) -> Scenario | None:
    if not scenario.parent_token:
        return None
    token = scenario.parent_token.casefold()
    exact_prefix = [s for s in all_scenarios if s.name.casefold().startswith(token + "-")]
    if len(exact_prefix) == 1:
        return exact_prefix[0]
    numeric = re.sub(r"\D", "", token).lstrip("0") or "0"
    candidates = []
    for candidate in all_scenarios:
        match = re.match(r"[A-Za-zА-Яа-я]?(\d{1,3})(?:-|$)", candidate.name)
        if match and (match.group(1).lstrip("0") or "0") == numeric:
            candidates.append(candidate)
    return candidates[0] if len(candidates) == 1 else None


def _shell_quote(value: Path | str) -> str:
    text = str(value)
    if os.name == "nt":
        return subprocess.list2cmdline([text])
    return shlex.quote(text)


def render_engine_command(template: str, scenario: Scenario, registry_path: Path) -> str:
    missing = [field for field in ("{input}", "{registry}") if field not in template]
    if missing:
        raise ValueError("в --engine отсутствуют обязательные placeholders: " + ", ".join(missing))
    return (
        template.replace("{input}", _shell_quote(scenario.input_dir))
        .replace("{registry}", _shell_quote(registry_path))
        .replace("{now}", _shell_quote(scenario.now))
    )


def _tail(text: str, limit: int = 1200) -> str:
    clean = (text or "").strip()
    return clean[-limit:] if clean else "нет диагностического вывода"


def _run_process(
    command: str | list[str],
    *,
    input_text: str | None = None,
    env: dict[str, str] | None = None,
    timeout: int = 600,
    shell: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        timeout=timeout,
        shell=shell,
        encoding="utf-8",
        errors="replace",
    )


def _parse_json_object(text: str) -> dict[str, object]:
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*", "", candidate, flags=re.IGNORECASE)
        candidate = re.sub(r"\s*```$", "", candidate)
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("ответ не содержит JSON-объект")
        value = json.loads(candidate[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("ответ судьи не является JSON-объектом")
    if set(value) != {"pass", "reason", "facts"}:
        raise ValueError("JSON судьи должен содержать только pass, reason и facts")
    if not isinstance(value["pass"], bool) or not isinstance(value["reason"], str):
        raise ValueError("поля pass/reason имеют неверный тип")
    facts = value["facts"]
    if not isinstance(facts, list) or any(
        not isinstance(item, dict)
        or set(item) != {"fact", "ok"}
        or not isinstance(item["fact"], str)
        or not isinstance(item["ok"], bool)
        for item in facts
    ):
        raise ValueError("поле facts имеет неверный формат")
    return value


def _lineage(scenario: Scenario) -> list[Scenario]:
    scenarios = discover_scenarios(scenario.root.parent)
    by_name = {item.name: item for item in scenarios}
    lineage = [scenario]
    seen = {scenario.name}
    current = scenario
    while current.parent_token:
        parent = _find_parent(current, scenarios)
        if parent is None or parent.name in seen:
            break
        lineage.insert(0, by_name[parent.name])
        seen.add(parent.name)
        current = parent
    return lineage


def _judge_prompt(scenario: Scenario, registry_md: str) -> str:
    source_parts = []
    for source_scenario in _lineage(scenario):
        for source in sorted(p for p in source_scenario.input_dir.rglob("*") if p.is_file()):
            relative = source.relative_to(source_scenario.root).as_posix()
            source_parts.append(
                f"\n--- SOURCE {source_scenario.name}/{relative} ---\n{_read_text(source)}"
            )
    sources = "".join(source_parts)
    return f"""Ты строгий смысловой судья реестра обязательств. Верни только JSON по схеме.

Проверь все факты ожидаемого результата: что, кто, срок/время, числа, тип, конечный статус, слияния и разделение похожих записей. Если expected.md содержит раздел «Не создавать», negative checks или нулевой результат, строго проверь их. Каждая цитата, которую реестр приписывает именованному источнику, должна быть точной непрерывной подстрокой этого исходного файла. Не требуй дословного совпадения формулировок самого обязательства. Не штрафуй за дополнительные поля или историю, если они не противоречат ожидаемому состоянию. При любой существенной ошибке pass=false. Reason дай кратко на русском и назови решающий ошибочный факт. В facts перечисли конкретные проверенные факты, включая ключевые отрицательные проверки; не используй общие фразы.

СЦЕНАРИЙ: {scenario.name}

--- EXPECTED.MD ---
{scenario.expected}

--- REGISTRY.MD ---
{registry_md}

--- INPUT FILES ---
{sources}
"""


def _run_codex_judge(prompt: str, result_file: Path) -> dict[str, object]:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("codex не найден в PATH")
    result_file.unlink(missing_ok=True)
    args = [
        codex,
        "exec",
        "--model",
        "gpt-5.6-sol",
        "-c",
        "model_reasoning_effort=high",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--ignore-rules",
        "--disable",
        "default_mode_request_user_input",
        "--output-schema",
        str(SCHEMA_PATH),
        "-o",
        str(result_file),
        "-",
    ]
    completed = _run_process(args, input_text=prompt, timeout=int(os.getenv("OLEG_PIPELINE_JUDGE_TIMEOUT", "600")))
    if completed.returncode != 0:
        raise RuntimeError("codex judge завершился с ошибкой: " + _tail(completed.stderr or completed.stdout))
    if not result_file.is_file():
        raise RuntimeError("codex judge не создал файл результата")
    return _parse_json_object(_read_text(result_file))


def _run_claude_judge(prompt: str) -> dict[str, object]:
    claude = shutil.which("claude")
    if not claude:
        raise RuntimeError("claude не найден в PATH")
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    env.pop("ANTHROPIC_AUTH_TOKEN", None)
    args = [
        claude,
        "-p",
        "--model",
        "opus",
        "--output-format",
        "json",
        "--mcp-config",
        '{"mcpServers":{}}',
        "--strict-mcp-config",
        prompt,
    ]
    completed = _run_process(args, env=env, timeout=int(os.getenv("OLEG_PIPELINE_JUDGE_TIMEOUT", "600")))
    if completed.returncode != 0:
        raise RuntimeError("claude judge завершился с ошибкой: " + _tail(completed.stderr or completed.stdout))
    outer = _parse_json_loose(completed.stdout)
    payload = outer.get("result", outer) if isinstance(outer, dict) else outer
    if isinstance(payload, dict):
        return _parse_json_object(json.dumps(payload, ensure_ascii=False))
    return _parse_json_object(str(payload))


def _parse_json_loose(text: str) -> object:
    candidate = text.strip()
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("ответ backend не содержит JSON")
        return json.loads(candidate[start : end + 1])


def judge(scenario: Scenario, registry_md: str, requested: str, work_dir: Path) -> tuple[dict[str, object], str]:
    prompt = _judge_prompt(scenario, registry_md)
    errors: list[str] = []
    backends = [requested] if requested == "claude" else ["codex", "claude"]
    for backend in backends:
        for attempt in range(2):
            try:
                if backend == "codex":
                    verdict = _run_codex_judge(prompt, work_dir / f"judge-codex-{attempt + 1}.json")
                else:
                    verdict = _run_claude_judge(prompt)
                return verdict, backend
            except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
                errors.append(f"{backend} попытка {attempt + 1}: {exc}")
    raise RuntimeError("; ".join(errors))


def _copy_parent_registry(parent: Result, registry_path: Path) -> None:
    if not parent.registry_path or not parent.registry_path.is_file():
        raise RuntimeError(f"родитель {parent.scenario.name} не создал registry.json")
    shutil.copy2(parent.registry_path, registry_path)
    if parent.registry_md_path and parent.registry_md_path.is_file():
        shutil.copy2(parent.registry_md_path, registry_path.with_suffix(".md"))


def run_scenario(
    scenario: Scenario,
    engine_template: str,
    out_dir: Path,
    requested_judge: str,
    parent: Result | None,
    should_judge: bool,
) -> Result:
    scenario_out = out_dir / scenario.name
    scenario_out.mkdir(parents=True, exist_ok=True)
    registry_path = scenario_out / "registry.json"
    registry_md_path = registry_path.with_suffix(".md")
    for stale in (registry_path, registry_md_path):
        stale.unlink(missing_ok=True)
    if parent:
        try:
            _copy_parent_registry(parent, registry_path)
        except RuntimeError as exc:
            return Result(scenario, False, str(exc), [], None, None, False, 0.0, "none")
    try:
        command = render_engine_command(engine_template, scenario, registry_path)
    except ValueError as exc:
        return Result(scenario, False, str(exc), [], None, None, False, 0.0, "none")
    started = time.monotonic()
    try:
        completed = _run_process(
            command,
            timeout=int(os.getenv("OLEG_PIPELINE_ENGINE_TIMEOUT", "600")),
            shell=True,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return Result(scenario, False, f"ошибка запуска движка: {exc}", [], None, None, False, time.monotonic() - started, "none")
    elapsed = time.monotonic() - started
    if completed.returncode != 0:
        return Result(
            scenario,
            False,
            f"движок завершился с кодом {completed.returncode}: {_tail(completed.stderr or completed.stdout)}",
            [],
            registry_path if registry_path.exists() else None,
            registry_md_path if registry_md_path.exists() else None,
            False,
            elapsed,
            "none",
        )
    if not registry_path.is_file() or not registry_md_path.is_file():
        missing = "registry.json" if not registry_path.is_file() else "registry.md"
        return Result(scenario, False, f"движок не создал {missing}", [], None, None, False, elapsed, "none")
    if not should_judge or requested_judge == "none":
        return Result(scenario, True, "движок выполнен; смысловая проверка отключена", [], registry_path, registry_md_path, True, elapsed, "none")
    try:
        verdict, backend = judge(scenario, _read_text(registry_md_path), requested_judge, scenario_out)
    except RuntimeError as exc:
        return Result(scenario, False, f"судья недоступен: {exc}", [], registry_path, registry_md_path, True, elapsed, "unavailable")
    return Result(
        scenario,
        bool(verdict["pass"]),
        str(verdict["reason"]),
        list(verdict["facts"]),
        registry_path,
        registry_md_path,
        True,
        elapsed,
        backend,
    )


def _escape_table(text: str) -> str:
    return " ".join(text.replace("|", "\\|").splitlines())


def write_report(results: list[Result], out_dir: Path, requested_judge: str) -> Path:
    passed = sum(result.passed for result in results)
    lines = [
        "# Отчёт приёмочного pipeline",
        "",
        f"- Судья: `{requested_judge}`",
        f"- Итог: **прошло {passed} из {len(results)}**",
        "",
        "| Сценарий | Результат | Причина |",
        "|---|---|---|",
    ]
    for result in results:
        mark = "PASS" if result.passed else "FAIL"
        lines.append(f"| `{result.scenario.name}` | {mark} | {_escape_table(result.reason)} |")
    for result in results:
        lines.extend(["", f"## {result.scenario.name}", "", f"- Вердикт: {'PASS' if result.passed else 'FAIL'}", f"- Причина: {result.reason}", f"- Судья: `{result.judge_backend}`", f"- Время движка: {result.engine_seconds:.2f} с"])
        if result.registry_path:
            lines.append(f"- Реестр: `{result.registry_path}`")
        if result.facts:
            lines.extend(["- Проверенные факты:", ""])
            for fact in result.facts:
                lines.append(f"  - {'OK' if fact['ok'] else 'FAIL'}: {fact['fact']}")
        if requested_judge == "none" and result.registry_md_path and result.registry_md_path.is_file():
            lines.extend(["", "```markdown", _read_text(result.registry_md_path).rstrip(), "```"])
    report_path = out_dir / "report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def run_pipeline(args: argparse.Namespace) -> int:
    examples_dir = Path(args.examples).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    all_scenarios = discover_scenarios(examples_dir)
    selected = [s for s in all_scenarios if not args.only or args.only.casefold() in s.name.casefold()]
    if not selected:
        raise ValueError(f"--only={args.only!r} не выбрал ни одного сценария")

    parent_by_name: dict[str, Scenario | None] = {}
    for scenario in all_scenarios:
        parent = _find_parent(scenario, all_scenarios)
        if scenario.parent_token and parent is None:
            raise ValueError(f"для {scenario.name} не найден однозначный родитель {scenario.parent_token}")
        parent_by_name[scenario.name] = parent

    needed = {scenario.name for scenario in selected}
    frontier = list(selected)
    while frontier:
        scenario = frontier.pop()
        parent = parent_by_name[scenario.name]
        if parent and parent.name not in needed:
            needed.add(parent.name)
            frontier.append(parent)

    pending = {scenario.name: scenario for scenario in all_scenarios if scenario.name in needed}
    results_by_name: dict[str, Result] = {}
    selected_names = {scenario.name for scenario in selected}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        while pending:
            ready = [
                scenario
                for scenario in pending.values()
                if parent_by_name[scenario.name] is None or parent_by_name[scenario.name].name in results_by_name
            ]
            if not ready:
                raise ValueError("обнаружен цикл зависимостей между сценариями")
            futures = {}
            for scenario in ready:
                parent_scenario = parent_by_name[scenario.name]
                parent_result = results_by_name.get(parent_scenario.name) if parent_scenario else None
                future = executor.submit(
                    run_scenario,
                    scenario,
                    args.engine,
                    out_dir,
                    args.judge,
                    parent_result,
                    scenario.name in selected_names,
                )
                futures[future] = scenario
            for future in concurrent.futures.as_completed(futures):
                scenario = futures[future]
                try:
                    results_by_name[scenario.name] = future.result()
                except Exception as exc:  # preserve one row even for an unexpected scenario failure
                    results_by_name[scenario.name] = Result(scenario, False, f"внутренняя ошибка pipeline: {exc}", [], None, None, False, 0.0, "none")
                del pending[scenario.name]

    results = [results_by_name[scenario.name] for scenario in selected]
    report = write_report(results, out_dir, args.judge)
    for result in results:
        symbol = "PASS" if result.passed else "FAIL"
        print(f"{symbol} {result.scenario.name}: {result.reason}")
        if args.judge == "none" and result.registry_md_path and result.registry_md_path.is_file():
            print(f"\n--- {result.scenario.name}/registry.md ---\n{_read_text(result.registry_md_path).rstrip()}\n")
    passed = sum(result.passed for result in results)
    denominator = len(results) if args.judge != "none" else 0
    numerator = passed if args.judge != "none" else 0
    print(f"прошло {numerator} из {denominator}")
    print(f"отчёт: {report}")
    return 0 if all(result.passed for result in results) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m oleg_pipeline", description="Приёмочный pipeline для реестров обязательств")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="запустить примеры через указанный движок")
    run.add_argument("--examples", required=True, help="каталог со сценариями input/ + expected.md")
    run.add_argument("--engine", required=True, help="команда с {input}, {registry} и необязательным {now}")
    run.add_argument("--judge", choices=("codex", "claude", "none"), default="codex", help="смысловой судья (по умолчанию: codex)")
    run.add_argument("--out", default="oleg_pipeline/out", help="каталог отчёта и реестров")
    run.add_argument("--only", help="запустить сценарии, имя которых содержит эту строку")
    run.add_argument("--jobs", type=int, default=4, help="число параллельных независимых сценариев (по умолчанию: 4)")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "run":
        if args.jobs < 1:
            parser.error("--jobs должен быть не меньше 1")
        try:
            return run_pipeline(args)
        except ValueError as exc:
            parser.error(str(exc))
    return 2
