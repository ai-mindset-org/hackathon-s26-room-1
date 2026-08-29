"""Решения человека — отдельный файл, который инструмент читает и НИКОГДА
не перезаписывает.

Итог = извлечённое + наложенные решения. Правка не может потеряться,
потому что теряться негде: она живёт вне реестра, и любой прогон
накладывает её заново поверх свежего извлечения.

Формат — JSONL или массив JSON:

    {"id": "c-7f3a", "action": "close",   "why": "сделал вчера"}
    {"id": "c-91bd", "action": "set_due", "value": "2026-09-05"}
    {"id": "c-2e40", "action": "not_mine"}
"""

from __future__ import annotations

import json
from pathlib import Path

from core.graph import DERIVED_FROM
from core.model import CANCELLED, DONE, OPEN

DEFAULT_DECISIONS = Path.home() / ".commitments" / "decisions.json"

ACTIONS = ("close", "cancel", "reopen", "not_mine", "set_due", "set_owner")


def load(path: Path | str | None = None) -> list[dict]:
    p = Path(path) if path else DEFAULT_DECISIONS
    if not p.exists():
        return []
    raw = p.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    try:  # массив целиком
        data = json.loads(raw)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        pass
    out = []  # построчный JSONL, комментарии и мусор пропускаем
    for line in raw.splitlines():
        line = line.strip().rstrip(",")
        if not line or line.startswith(("//", "#")):
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def apply(graph, path: Path | str | None = None) -> int:
    """Наложить решения на граф. -> сколько применено."""
    applied = 0
    for d in load(path):
        cid, action = d.get("id"), d.get("action")
        if not cid or action not in ACTIONS:
            continue
        c = graph.get("commitment", cid)
        if c is None:  # решение про запись, которой в этом прогоне нет —
            continue   # не ошибка: файл живёт дольше любого реестра
        if action == "close":
            c.status = DONE
        elif action in ("cancel", "not_mine"):
            c.status = CANCELLED
            for child_id in graph.descendants(c.id, DERIVED_FROM):
                child = graph.get("commitment", child_id)
                if child is not None:
                    child.status = CANCELLED
        elif action == "reopen":
            c.status = OPEN
        elif action == "set_due" and d.get("value"):
            c.due = d["value"]
            c.uncertainty = [u for u in c.uncertainty if "срок" not in u]
        elif action == "set_owner" and d.get("value"):
            c.owner = d["value"]
        applied += 1
    return applied
