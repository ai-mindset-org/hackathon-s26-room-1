"""Прогон приёмочных примеров и счёт «прошло N из M».

Сверка здесь ГРУБАЯ и осознанно: пункт считается покрытым, если в реестре есть
запись, где встречаются и дата пункта, и хотя бы одно его ключевое слово.
Сверка по смыслу через LLM-судью — фаза 2 (D-12). До неё счёт занижен, и это
нормально: он честно показывает, где мы на самом деле.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "examples"

ITEM = re.compile(r"^\s*\d+\.\s+(.*)$")
DATE = re.compile(r"\b\d{1,2}\.\d{2}\b")
# Пункт-количество: «записей про «Витрину» ровно одна». Грепом непроверяем
# в принципе — считаем строки реестра, а не ищем подстроку.
COUNT = re.compile(r"«([^»]+)»[^«»]*?ровно\s+(одна|один|одно|два|две|\d+)",
                   re.IGNORECASE)
NUMWORD = {"одна": 1, "один": 1, "одно": 1, "два": 2, "две": 2}
ENTRY = re.compile(r"^\s*-\s+\[[ x]\]")
STEM = 5  # «Витрину» и «Витрина» — одна запись, а не две
STOP = {
    "источник", "письмо", "школы", "чат", "транскрипт", "спикер", "или",
    "допустимо", "назначен", "событие", "действий", "подготовке", "нет",
    "регулярное", "ближайшее", "число", "напоминание", "тоже", "снято",
}


def expected_items(path: Path) -> list[str]:
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ITEM.match(line)
        if m:
            items.append(m.group(1).strip())
    if items:
        return items
    # пример 02 записан списком через дефис
    return [
        ln.strip("- ").strip()
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip().startswith("- ")
    ]


def keywords(item: str) -> list[str]:
    words = re.findall(r"[А-Яа-яЁёA-Za-z]{4,}", item)
    return [w.lower() for w in words if w.lower() not in STOP][:6]


def count_check(item: str, registry_text: str) -> bool | None:
    """-> True/False для пункта-количества, None если пункт не про количество."""
    m = COUNT.search(item)
    if not m:
        return None
    stem = m.group(1).lower().strip("«»\"' ")[:STEM]
    want = NUMWORD.get(m.group(2).lower(), 0) or int(
        m.group(2) if m.group(2).isdigit() else 0)
    got = sum(
        1 for ln in registry_text.splitlines()
        if ENTRY.match(ln) and stem in ln.lower()
    )
    return got == want


def covered(item: str, registry_text: str) -> bool:
    counted = count_check(item, registry_text)
    if counted is not None:
        return counted
    low = registry_text.lower()
    dates = DATE.findall(item)
    kws = keywords(item)
    has_kw = any(k in low for k in kws) if kws else False
    if dates:
        return has_kw and any(d in registry_text for d in dates)
    return has_kw


def run_one(example: Path, today: str, llm: bool = False,
            use_judge: bool = False) -> tuple[int, int, list[str]]:
    expected = example / "expected.md"
    inputs = example / "input"
    if not expected.exists() or not inputs.exists():
        return 0, 0, []

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "реестр.md"
        proc = subprocess.run(
            [sys.executable, str(REPO / "cli.py"), "run",
             "--input", str(inputs),
             "--today", today,
             "--registry", str(Path(tmp) / "registry.json"),
             "--out", str(out)] + (["--llm"] if llm else []),
            cwd=REPO, capture_output=True, text=True,
        )
        if proc.returncode != 0:
            return 0, 0, [f"прогон упал: {proc.stderr.strip()[:200]}"]
        text = out.read_text(encoding="utf-8") if out.exists() else ""

    items = expected_items(expected)

    if use_judge:
        from runner.judge import judge
        verdicts = judge(items, text)
        if verdicts:  # пусто = судья не сработал, откатываемся на grep
            missed = []
            for it, (ok, why) in zip(items, verdicts):
                # количество — арифметика, а не смысл: судью тут не спрашиваем
                counted = count_check(it, text)
                if counted is not None:
                    ok, why = counted, "" if counted else "число записей не сошлось"
                if not ok:
                    missed.append(f"{it}" + (f"  — {why}" if why else ""))
            return len(items) - len(missed), len(items), missed
        print("    (судья не ответил — грубая сверка)")

    missed = [it for it in items if not covered(it, text)]
    return len(items) - len(missed), len(items), missed


def run_all(today: str = "2026-08-28", llm: bool = False,
            use_judge: bool = False) -> int:
    from runner.judge import available as judge_available

    if use_judge and not judge_available():
        print("нет ключа — сверка грубая, счёт занижен\n")
        use_judge = False
    print("сверка: " + ("по смыслу, LLM-судья" if use_judge
                        else "грубая, по подстроке") + "\n")
    total_ok = total = 0
    for example in sorted(EXAMPLES.iterdir()):
        if not example.is_dir():
            continue
        ok, n, missed = run_one(example, today, llm, use_judge)
        total_ok += ok
        total += n
        print(f"{example.name}: прошло {ok} из {n}")
        for m in missed:
            if "  — " in m:
                item, why = m.split("  — ", 1)
                print(f"    ✗ {item[:80]}")
                print(f"      причина: {why}")
            else:
                print(f"    ✗ {m[:100]}")
    print(f"\nИТОГО: {total_ok} из {total}")
    return 0
