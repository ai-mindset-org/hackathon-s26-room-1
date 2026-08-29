"""Узлы графа обязательств.

Контракт для всей комнаты. Поля, которые фаза 1 ещё не заполняет, всё равно
присутствуют: добавить их позже — значит сломать чужие модули.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional


# Виды обязательства
TASK = "task"
EVENT = "event"
RECURRING = "recurring"

# Статусы
OPEN = "open"
DONE = "done"
CANCELLED = "cancelled"

# Корзины
MINE = "mine"
WORK = "work"
UNKNOWN = "unknown"


@dataclass
class Source:
    """Входящий файл."""

    id: str
    kind: str  # email | chat | transcript | screenshot_text | text
    name: str


@dataclass
class Chunk:
    """Фрагмент источника с точной цитатой, по которой человек может проверить."""

    id: str
    text: str
    quote: str
    source_id: Optional[str] = None


@dataclass
class Person:
    id: str
    name: str
    aliases: list[str] = field(default_factory=list)


@dataclass
class Event:
    """Событие в календаре. Не задача: делать с ним нечего, только присутствовать."""

    id: str
    title: str
    date: Optional[str] = None  # ГГГГ-ММ-ДД


@dataclass
class Topic:
    id: str
    name: str


@dataclass
class Commitment:
    """Обязательство.

    `id` выдаётся один раз и никогда не меняется — на него ссылаются решения
    человека. `key` — человекочитаемый слаг для сопоставления при повторном
    прогоне; он может смениться, id — нет.

    Связи с источником, персоной, событием и родителем живут в рёбрах графа,
    а не в полях.
    """

    id: str
    key: str
    what: str
    owner: Optional[str] = None
    due: Optional[str] = None  # ГГГГ-ММ-ДД, заполняет dates/
    due_raw: Optional[str] = None  # как было сказано в тексте
    said_on: Optional[str] = None  # дата сообщения — опора для «до пятницы»
    kind: str = TASK
    status: str = OPEN
    basket: str = UNKNOWN  # заполняет фаза 4
    uncertainty: list[str] = field(default_factory=list)


NODE_TYPES = {
    "source": Source,
    "chunk": Chunk,
    "person": Person,
    "event": Event,
    "topic": Topic,
    "commitment": Commitment,
}


def to_dict(node) -> dict:
    return asdict(node)
