"""Слияние нового извлечения с живым реестром.

    merge(base, new) -> Graph

Порядок операций важен: сначала сопоставляем с существующим, потом берём
ЕГО id, и только для действительно новых заводим новый. Наоборот нельзя —
переформулированная задача получит новый id, и правка человека осиротеет.
На демо это выглядит как «оно потеряло мою галочку».
"""

from __future__ import annotations

from pathlib import Path

from core.graph import DERIVED_FROM, Graph
from core.model import CANCELLED, DONE, Commitment

from . import decisions as human
from . import signals
from .match import find

CARRY = ("source", "chunk", "person", "event", "topic")


def _absorb(old: Commitment, fresh: Commitment, *, override_due: bool = False) -> None:
    """Влить свежее упоминание в существующую запись. id и key не трогаем."""
    if not old.owner and fresh.owner:
        old.owner = fresh.owner
    if not old.said_on and fresh.said_on:
        old.said_on = fresh.said_on

    newer = (fresh.said_on or "") >= (old.said_on or "")
    if fresh.due and (override_due or (newer and not old.due)):
        old.due = fresh.due
    if fresh.due_raw and (override_due or not old.due_raw):
        old.due_raw = fresh.due_raw

    if override_due:  # срок уточнён — старые сомнения о нём сняты
        old.uncertainty = [u for u in old.uncertainty if "срок" not in u]
    for u in fresh.uncertainty:
        if u not in old.uncertainty:
            old.uncertainty.append(u)


def _cancel_cascade(graph: Graph, target: Commitment) -> None:
    """Снять запись и всё, что от неё производно.

    «Подтвердить за 3 дня» существует только потому, что существует запись
    на ТО. Отменили ТО — производное обязано уйти следом, иначе человек
    получит напоминание о том, чего нет.
    """
    target.status = CANCELLED
    for child_id in graph.descendants(target.id, DERIVED_FROM):
        child = graph.get("commitment", child_id)
        if child is not None:
            child.status = CANCELLED


def merge(
    base: Graph,
    new: Graph,
    *,
    decisions_path: Path | str | None = None,
    judge=None,
) -> Graph:
    """Обновить существующее, не создать дубль. Закрыть. Отменить с каскадом."""
    # Graph.__len__ считает обязательства: пустой граф ложный, поэтому
    # проверяем именно на None, иначе потеряем уже загруженные источники.
    if base is None:
        base = Graph()

    # вспомогательные узлы переносим как есть — на них ссылаются рёбра
    for kind in CARRY:
        for nid, node in new.nodes.get(kind, {}).items():
            base.nodes[kind][nid] = node

    remap: dict[str, str] = {}
    pending: list[tuple[str, Commitment]] = []

    # ── первый проход: обычные обязательства ───────────────────────────
    for c in new.commitments():
        sig = signals.detect(c.what)
        if sig:
            pending.append((sig, c))  # сигналы — после, поверх собранного
            continue

        match = find(base, c, judge=judge)
        if match is not None:
            remap[c.id] = match.id
            _absorb(match, c)
        else:
            base.add_node("commitment", c)
            remap[c.id] = c.id

    # рёбра переносим с подменой id, иначе доказательства осиротеют
    for e in new.edges:
        base.add_edge(remap.get(e.src, e.src), e.type, remap.get(e.dst, e.dst))

    # ── второй проход: сигналы поверх уже собранного реестра ───────────
    for sig, c in pending:
        target = find(base, c, judge=judge)

        if target is None:
            # Сигнал ни к чему не привязался. Recall-first: не выбрасываем,
            # оставляем живым с пометкой — пропустить страшнее, чем показать.
            base.add_node("commitment", c)
            note = "не понял, к чему относится это обновление"
            if note not in c.uncertainty:
                c.uncertainty.append(note)
            for e in new.edges:
                if e.src == c.id:
                    base.add_edge(c.id, e.type, e.dst)
            continue

        # доказательства сигнала переезжают на цель
        for e in new.edges:
            if e.src == c.id:
                base.add_edge(target.id, e.type, e.dst)

        if sig == "cancel":
            _cancel_cascade(base, target)
        elif sig == "close":
            target.status = DONE
        elif sig == "move":
            _absorb(target, c, override_due=True)

    # ── решения человека поверх всего ──────────────────────────────────
    human.apply(base, decisions_path)
    return base
