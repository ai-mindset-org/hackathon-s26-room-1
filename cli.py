#!/usr/bin/env python3
"""Реестр обязательств — CLI.

    python3 cli.py run   --input ПАПКА --today ГГГГ-ММ-ДД [--registry ПУТЬ] [--out ФАЙЛ]
    python3 cli.py check [--today ГГГГ-ММ-ДД]

Опорная дата `--today` обязательна и никогда не берётся из системных часов:
приёмочные примеры содержат «до пятницы», и без фиксации даты приёмка протухнет
через сутки, а на демо мы этого не заметим.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from core.graph import EVIDENCED_BY, Graph
from core.model import CANCELLED, DONE, EVENT, RECURRING
from core.store import DEFAULT_REGISTRY, load, save
from dates.resolve import resolve, sort_key
from extract import llm as extract_llm
from extract.naive import extract as extract_naive
from ingest.reader import read_folder
from registry import merge

KIND_LABEL = {EVENT: "событие", RECURRING: "регулярное"}


def render(graph: Graph) -> str:
    lines = ["# Реестр обязательств", ""]

    active = [c for c in graph.commitments() if c.status not in (DONE, CANCELLED)]
    unsure = [c for c in active if c.uncertainty]
    solid = [c for c in active if not c.uncertainty]

    if not solid:
        lines.append("_Пусто._")

    for c in sorted(solid, key=sort_key):
        lines.append(_line(graph, c))

    if unsure:
        lines += ["", "## Проверь меня", "",
                  "_Не уверен, что это обязательства._", ""]
        for c in unsure:
            lines.append(_line(graph, c))

    closed = [c for c in graph.commitments() if c.status in (DONE, CANCELLED)]
    if closed:
        lines += ["", "## Закрытые и снятые", ""]
        for c in closed:
            mark = "снято/отменено" if c.status == CANCELLED else "сделано"
            lines.append(f"- [x] {c.what} · {mark}")

    return "\n".join(lines) + "\n"


MARK = {"exact": "", "day": "", "period": " ~", "fuzzy": " ?"}


def _due_label(c) -> str:
    d = c.deadline
    if d is None or not d.date:
        return c.due_raw or "срок неясен"
    y, mth, day = d.date.split("-")
    raw = f" ({d.raw})" if d.raw else ""
    return f"{day}.{mth}{MARK.get(d.precision, '')}{raw}"


def _line(graph: Graph, c) -> str:
    owner = c.owner or "не назначен"
    due = _due_label(c)
    kind = KIND_LABEL.get(c.kind)
    tail = f" · {kind}" if kind else ""
    out = [f"- [ ] {c.what} · {owner} · {due}{tail}"]
    for chunk_id in graph.neighbors(c.id, EVIDENCED_BY):
        ch = graph.get("chunk", chunk_id)
        if not ch:
            continue
        src = graph.get("source", ch.source_id) if ch.source_id else None
        name = src.name if src else "источник"
        out.append(f"  ↳ источник: {name} — «{ch.quote}»")
    d = c.deadline
    if d and d.alternatives:
        out.append(f"  ↳ иначе: {'; '.join(d.alternatives)}")
    if d and d.note and d.date:
        out.append(f"  ↳ {d.note}")
    return "\n".join(out)


def _extract(chunks, known_keys, today, want_llm: bool):
    """Модель, если попросили и есть ключ. Иначе правила — молча и рабоче."""
    if not want_llm:
        return extract_naive(chunks, known_keys, today)
    if not extract_llm.available():
        print("ANTHROPIC_API_KEY не задан — работаю на правилах",
              file=sys.stderr)
        return extract_naive(chunks, known_keys, today)
    try:
        return extract_llm.extract(chunks, known_keys, today)
    except Exception as exc:  # модель упала — приёмка не должна падать вместе
        print(f"модель недоступна ({exc}) — откатываюсь на правила",
              file=sys.stderr)
        return extract_naive(chunks, known_keys, today)


def cmd_run(args: argparse.Namespace) -> int:
    registry_path = Path(args.registry)
    graph = load(registry_path)

    sources, chunks = read_folder(args.input)
    for s in sources:
        graph.add_node("source", s)

    new = _extract(chunks, graph.known_keys(), args.today, args.llm)
    resolve(new.commitments(), args.today)
    graph = merge(graph, new)

    save(graph, registry_path)
    text = render(graph)

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)

    print(
        f"\n[реестр: {registry_path} · обязательств: {len(graph)}]",
        file=sys.stderr,
    )
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    from runner.check import run_all

    return run_all(today=args.today, llm=args.llm)


def main() -> int:
    p = argparse.ArgumentParser(prog="cli.py", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="прогнать папку входящих в реестр")
    r.add_argument("--input", required=True, help="папка с входящими файлами")
    r.add_argument("--today", required=True, help="опорная дата ГГГГ-ММ-ДД")
    r.add_argument("--registry", default=str(DEFAULT_REGISTRY),
                   help="путь к реестру (по умолчанию вне репозитория)")
    r.add_argument("--out", help="куда положить markdown (по умолчанию stdout)")
    r.add_argument("--llm", action="store_true",
                   help="извлекать моделью (нужен ANTHROPIC_API_KEY)")
    r.set_defaults(func=cmd_run)

    c = sub.add_parser("check", help="прогнать приёмочные примеры")
    c.add_argument("--today", default="2026-08-28",
                   help="опорная дата для примеров")
    c.add_argument("--llm", action="store_true",
                   help="извлекать моделью")
    c.set_defaults(func=cmd_check)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
