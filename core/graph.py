"""Граф обязательств: узлы, рёбра, обходы.

Хранится плоскими списками. Форма графовая, поэтому слой хранения можно
поменять на настоящую БД, не трогая модель.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional

from .model import NODE_TYPES, Commitment

# Типы рёбер
FROM = "FROM"  # Chunk -> Source
EVIDENCED_BY = "EVIDENCED_BY"  # Commitment -> Chunk (может быть несколько)
OWNED_BY = "OWNED_BY"  # Commitment -> Person
PREPARES = "PREPARES"  # Commitment -> Event  (бронь до 10.09 готовит демо 25.09)
DERIVED_FROM = "DERIVED_FROM"  # Commitment -> Commitment (каскад отмен)
SUPERSEDES = "SUPERSEDES"  # Commitment -> Commitment (переформулировка)
ABOUT = "ABOUT"  # Commitment -> Topic

EDGE_TYPES = (FROM, EVIDENCED_BY, OWNED_BY, PREPARES, DERIVED_FROM, SUPERSEDES, ABOUT)


@dataclass(frozen=True)
class Edge:
    src: str
    type: str
    dst: str


class Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {t: {} for t in NODE_TYPES}
        self.edges: list[Edge] = []
        self.events: list[dict] = []  # журнал прогонов, наполняет фаза 3

    # — узлы —

    def add_node(self, kind: str, node) -> str:
        if kind not in self.nodes:
            raise ValueError(f"неизвестный тип узла: {kind}")
        self.nodes[kind][node.id] = node
        return node.id

    def get(self, kind: str, node_id: str):
        return self.nodes[kind].get(node_id)

    def commitments(self) -> list[Commitment]:
        return list(self.nodes["commitment"].values())

    def find_commitment_by_key(self, key: str) -> Optional[Commitment]:
        for c in self.nodes["commitment"].values():
            if c.key == key:
                return c
        return None

    def known_keys(self) -> list[str]:
        """Список ключей для передачи экстрактору — так он переиспользует
        существующий ключ вместо изобретения нового. Дедуп на входе."""
        return [c.key for c in self.nodes["commitment"].values()]

    # — рёбра —

    def add_edge(self, src: str, type_: str, dst: str) -> None:
        if type_ not in EDGE_TYPES:
            raise ValueError(f"неизвестный тип ребра: {type_}")
        e = Edge(src, type_, dst)
        if e not in self.edges:
            self.edges.append(e)

    def neighbors(self, node_id: str, type_: str) -> list[str]:
        return [e.dst for e in self.edges if e.src == node_id and e.type == type_]

    def incoming(self, node_id: str, type_: str) -> list[str]:
        return [e.src for e in self.edges if e.dst == node_id and e.type == type_]

    def descendants(self, node_id: str, type_: str) -> list[str]:
        """Обход в глубину по входящим рёбрам — каскад отмен.

        Отмена ТО должна погасить и «подтвердить за 3 дня», которое ссылается
        на неё через DERIVED_FROM.
        """
        seen: list[str] = []
        stack = list(self.incoming(node_id, type_))
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.append(cur)
            stack.extend(self.incoming(cur, type_))
        return seen

    def __iter__(self) -> Iterator[Commitment]:
        return iter(self.commitments())

    def __len__(self) -> int:
        return len(self.nodes["commitment"])
