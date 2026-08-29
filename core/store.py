"""Сохранение и чтение графа.

Дефолтный путь — ВНЕ репозитория. Репо публичный, а реестр это чужая почта:
одного `git add .` хватит, чтобы личная переписка уехала в открытый GitHub.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from .graph import Edge, Graph
from .model import NODE_TYPES, to_dict

DEFAULT_REGISTRY = Path(os.path.expanduser("~/.commitments/registry.json"))


def save(graph: Graph, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "nodes": {
            kind: [to_dict(n) for n in nodes.values()]
            for kind, nodes in graph.nodes.items()
        },
        "edges": [{"src": e.src, "type": e.type, "dst": e.dst} for e in graph.edges],
        "events": graph.events,
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return path


def load(path: str | Path) -> Graph:
    """Отсутствующий или пустой файл даёт пустой граф, а не исключение."""
    graph = Graph()
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        return graph

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return graph

    for kind, rows in payload.get("nodes", {}).items():
        cls = NODE_TYPES.get(kind)
        if cls is None:
            continue
        for row in rows:
            graph.nodes[kind][row["id"]] = cls(**row)

    for e in payload.get("edges", []):
        graph.edges.append(Edge(e["src"], e["type"], e["dst"]))

    graph.events = payload.get("events", [])
    return graph
