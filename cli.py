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
from extract.naive import extract
from ingest.reader import read_folder

KIND_LABEL = {EVENT: "событие", RECURRING: "регулярное"}


def merge_into(base: Graph, new: Graph) -> Graph:
    """Фаза 1: вливаем по id, без умного слияния.

    Умное слияние (обновить срок, не создать дубль, закрыть, отменить
    с каскадом) — контракт registry.merge, фаза 3.
    """
    for kind, nodes in new.nodes.items():
        for node_id, node in nodes.items():
            base.nodes[kind][node_id] = node
    for e in new.edges:
        base.add_edge(e.src, e.type, e.dst)
    return base


def render(graph: Graph) -> str:
    lines = ["# Реестр обязательств", ""]

    active = [c for c in graph.commitments() if c.status not in (DONE, CANCELLED)]
    unsure = [c for c in active if c.uncertainty]
    solid = [c for c in active if not c.uncertainty]

    if not solid:
        lines.append("_Пусто._")

    for c in solid:
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
            mark = "снято" if c.status == CANCELLED else "сделано"
            lines.append(f"- [x] {c.what} · {mark}")

    return "\n".join(lines) + "\n"


def _line(graph: Graph, c) -> str:
    owner = c.owner or "не назначен"
    due = c.due or c.due_raw or "срок неясен"
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
    return "\n".join(out)


def cmd_run(args: argparse.Namespace) -> int:
    registry_path = Path(args.registry)
    graph = load(registry_path)

    sources, chunks = read_folder(args.input)
    for s in sources:
        graph.add_node("source", s)

    new = extract(chunks, graph.known_keys(), args.today)
    graph = merge_into(graph, new)

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

    return run_all(today=args.today)


def main() -> int:
    p = argparse.ArgumentParser(prog="cli.py", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="прогнать папку входящих в реестр")
    r.add_argument("--input", required=True, help="папка с входящими файлами")
    r.add_argument("--today", required=True, help="опорная дата ГГГГ-ММ-ДД")
    r.add_argument("--registry", default=str(DEFAULT_REGISTRY),
                   help="путь к реестру (по умолчанию вне репозитория)")
    r.add_argument("--out", help="куда положить markdown (по умолчанию stdout)")
    r.set_defaults(func=cmd_run)

    c = sub.add_parser("check", help="прогнать приёмочные примеры")
    c.add_argument("--today", default="2026-08-28",
                   help="опорная дата для примеров")
    c.set_defaults(func=cmd_check)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
