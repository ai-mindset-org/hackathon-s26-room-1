#!/usr/bin/env python3
"""Честный отчёт: штатный движок (core/extract/dates/registry) на правилах,
без модели, против всех 26 сценариев этого корпуса.

Зачем: корпус не подключён к `cli.py check` (та сверка жёстко завязана на
`examples/`), и ни одного отчёта о прогоне штатного движка против него не
было закоммичено — комната просто не знала своих цифр здесь. Этот скрипт
не решает, чей движок «главный» и не подменяет `cli.py check` — он просто
делает пробел видимым и воспроизводимым.

Сверка ГРУБАЯ и по количеству, не по смыслу: сравниваем число извлечённых
обязательств с `required_records` из `index.csv`. Это не замена LLM-судье
(`runner/check.py --judge`) — семантику (тот ли срок, то ли лицо, та ли
цитата) так не проверить. Здесь только: движок вообще что-то увидел или
тихо промолчал.

Прогон только на правилах (`--llm` не использован): в этом окружении не
было ANTHROPIC_API_KEY. Прогон с моделью — открытый пробел, см. итог внизу
отчёта.

Запуск:  python3 oleg_examples_quick_untrusted/report_naive.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from cli import _extract  # noqa: E402
from ingest.reader import read_folder  # noqa: E402

CORPUS = Path(__file__).resolve().parent
ANCHOR = re.compile(r"Опорное время:\s*`(\d{4}-\d{2}-\d{2})")


def _anchor_date(expected_md: Path) -> str | None:
    m = ANCHOR.search(expected_md.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def run() -> list[dict]:
    rows = []
    with (CORPUS / "index.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            scen_id = row["id"]
            scen_dir = next(CORPUS.glob(f"{scen_id}-*"), None)
            if scen_dir is None:
                rows.append({**row, "extracted": None, "note": "папка сценария не найдена"})
                continue

            today = _anchor_date(scen_dir / "expected.md")
            if today is None:
                rows.append({**row, "extracted": None, "note": "не нашёл опорное время в expected.md"})
                continue

            sources, chunks = read_folder(scen_dir / "input")
            graph = _extract(chunks, [], today, want_llm=False)
            extracted = len(graph.commitments())
            expected_zero = row["zero_obligations"].strip().lower() == "true"
            required = int(row["required_records"] or 0)

            if expected_zero:
                ok = extracted == 0
            else:
                ok = extracted >= 1  # грубо: хоть что-то увидел, не 0 на непустом ожидании

            rows.append({
                **row,
                "extracted": extracted,
                "required": required,
                "ok": ok,
            })
    return rows


def render(rows: list[dict]) -> str:
    lines = [
        "# Штатный движок (без --llm) против корпуса gagebt",
        "",
        "Сгенерировано `report_naive.py`. Грубая сверка по количеству,",
        "не по смыслу — не замена LLM-судьи. Прогон без `--llm`: в окружении,",
        "где строился отчёт, не было `ANTHROPIC_API_KEY`.",
        "",
        "| id | сценарий | язык | ожидается 0? | required | извлечено (naive) | ок? |",
        "|---|---|---|---:|---:|---:|:---:|",
    ]
    ok_count = 0
    for r in rows:
        if r.get("extracted") is None:
            lines.append(f"| {r['id']} | {r.get('title', '?')} | — | — | — | — | ⚠️ {r['note']} |")
            continue
        mark = "✅" if r["ok"] else "❌"
        if r["ok"]:
            ok_count += 1
        lines.append(
            f"| {r['id']} | {r['title']} | {r['languages']} | "
            f"{'да' if r['zero_obligations'].strip().lower() == 'true' else 'нет'} | "
            f"{r['required']} | {r['extracted']} | {mark} |"
        )

    total = len([r for r in rows if r.get("extracted") is not None])
    lines += [
        "",
        f"**Итого: {ok_count} из {total}** прошли грубую сверку по количеству "
        f"(0 там, где ожидается 0; хотя бы 1 там, где ожидается непустой результат).",
        "",
        "## Что это значит",
        "",
        "Корпус целиком на английском/смешанных языках (`languages` в "
        "`index.csv`), а `extract/naive.py` — правила целиком на русском "
        "(маркеры долженствования, названия месяцев, разбор дат). Провал "
        "здесь ожидаем и задокументирован в README-tool.md — правила "
        "заточены под стиль `examples/`, для остального нужен `--llm`.",
        "",
        "Не проверено: прогон с `--llm` против этого же корпуса — нужен "
        "`ANTHROPIC_API_KEY`, которого не было в окружении, где готовился "
        "отчёт. Следующий шаг для честной цифры — прогнать этот же скрипт "
        "с ключом и добавить колонку.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    report = render(run())
    out = CORPUS / "NAIVE-REPORT.md"
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nзаписано в {out}", file=sys.stderr)
