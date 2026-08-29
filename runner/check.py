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


def covered(item: str, registry_text: str) -> bool:
    low = registry_text.lower()
    dates = DATE.findall(item)
    kws = keywords(item)
    has_kw = any(k in low for k in kws) if kws else False
    if dates:
        return has_kw and any(d in registry_text for d in dates)
    return has_kw


def run_one(example: Path, today: str, llm: bool = False) -> tuple[int, int, list[str]]:
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
    missed = [it for it in items if not covered(it, text)]
    return len(items) - len(missed), len(items), missed


def run_all(today: str = "2026-08-28", llm: bool = False) -> int:
    total_ok = total = 0
    for example in sorted(EXAMPLES.iterdir()):
        if not example.is_dir():
            continue
        ok, n, missed = run_one(example, today, llm)
        total_ok += ok
        total += n
        print(f"{example.name}: прошло {ok} из {n}")
        for m in missed:
            print(f"    ✗ {m[:100]}")
    print(f"\nИТОГО: {total_ok} из {total}")
    return 0
