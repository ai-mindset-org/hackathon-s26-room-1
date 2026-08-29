"""Наивное извлечение обязательств — заглушка контракта для фазы 1.

Контракт модуля (фиксируется здесь, наполняется в фазе 2):

    extract(chunks, known_keys, today) -> Graph

Возвращает ПОДГРАФ, а не список: обязательство плюс рёбра к источнику,
персоне, событию, родителю. `known_keys` — ключи уже известных обязательств,
чтобы экстрактор переиспользовал их вместо изобретения новых. Так дедуп
решается на входе, а не постфактум.

В фазе 1 здесь правила без LLM. В фазе 2 тело заменяется на вызов модели,
сигнатура не меняется.
"""

from __future__ import annotations

import hashlib
import re

from core.graph import EVIDENCED_BY, Graph
from core.model import EVENT, RECURRING, TASK, Chunk, Commitment

# Маркеры долженствования
MARKERS = (
    "нужно", "надо", "прошу", "просим", "договорились", "с тебя", "с вас",
    "оплатить", "прислать", "отправить", "отправляю", "забронировать", "бронирую",
    "согласовать", "продлить", "подтвердить", "собрать", "соберу", "не забываем",
    "напоминаем", "требуется", "должен", "должна",
)

# Признаки события, а не задачи
EVENT_MARKERS = ("состоится", "собрание", "встреча", "демо")

# Признаки регулярного
RECURRING_MARKERS = ("каждого месяца", "каждый месяц", "числа")

DATE_NUM = re.compile(r"\b\d{1,2}\.\d{2}(?:\.\d{4})?\b")
MONTHS = (
    "январ|феврал|март|апрел|мая|май|июн|июл|август|"
    "сентябр|октябр|ноябр|декабр"
)
DATE_MONTH = re.compile(rf"\b\d{{1,2}}\s+(?:{MONTHS})\w*", re.IGNORECASE)
DATE_SOON = re.compile(r"\bзавтра(?:\s+\w+)?|\bсегодня\b", re.IGNORECASE)
DATE_WORD = re.compile(
    r"(?:до|к|на)\s+(?:\d{1,2}\s+\w+|\w+\s+\d{1,2}\.\d{2}|конца\s+месяца|"
    r"\d{1,2}\s+числа[^,.;]*|завтра[^,.;]*|"
    r"понедельника|вторника|среды|четверга|пятницы|субботы|воскресенья|"
    r"десятого|первого|второго|третьего|пятого)",
    re.IGNORECASE,
)
CHAT_PREFIX = re.compile(r"^\[(\d{1,2}\.\d{2})\s+\d{1,2}:\d{2}\]\s*([^:]{1,20}):\s*")
TRANSCRIPT_PREFIX = re.compile(r"^\s*[—–-]\s+")

STOP = {"это", "тебя", "вас", "нас", "нужно", "надо", "также", "коллеги"}


def _id(text: str) -> str:
    return f"c-{hashlib.sha1(text.encode('utf-8')).hexdigest()[:6]}"


def make_key(what: str) -> str:
    """Человекочитаемый слаг для сопоставления при повторном прогоне."""
    words = [
        w.strip(".,!?«»\"'()").lower()
        for w in what.split()
        if len(w.strip(".,!?«»\"'()")) > 3
    ]
    words = [w for w in words if w not in STOP][:3]
    return "-".join(words) or "без-названия"


def find_due_raw(text: str) -> str | None:
    for rx in (DATE_WORD, DATE_MONTH, DATE_NUM, DATE_SOON):
        m = rx.search(text)
        if m:
            return m.group(0)
    return None


def guess_kind(text: str) -> str:
    low = text.lower()
    if any(w in low for w in RECURRING_MARKERS):
        return RECURRING
    if any(w in low for w in EVENT_MARKERS) and "состоится" in low:
        return EVENT
    return TASK


def looks_like_commitment(text: str) -> bool:
    low = text.lower()
    if any(m in low for m in MARKERS):
        return True
    return bool(
        DATE_NUM.search(text)
        or DATE_WORD.search(text)
        or DATE_MONTH.search(text)
        or DATE_SOON.search(text)
    )


def clean(text: str) -> tuple[str, str | None, str | None]:
    """Убрать служебный префикс, вернуть (текст, владелец, дата сообщения)."""
    owner = said = None
    m = CHAT_PREFIX.match(text)
    if m:
        said = m.group(1)  # дд.мм
        owner = m.group(2).strip()
        text = text[m.end():]
    else:
        text = TRANSCRIPT_PREFIX.sub("", text)
    return text.strip(), owner, said


def _said_on(day_month: str | None, today: str) -> str | None:
    """«27.08» + опорный год -> ГГГГ-ММ-ДД."""
    if not day_month:
        return None
    try:
        d, mth = day_month.split(".")
        return f"{today[:4]}-{int(mth):02d}-{int(d):02d}"
    except (ValueError, IndexError):
        return None


def extract(chunks: list[Chunk], known_keys: list[str], today: str) -> Graph:
    """Из фрагментов — подграф обязательств.

    `known_keys` в фазе 1 используется только для переиспользования ключа;
    в фазе 2 он поедет в промпт модели.
    """
    g = Graph()
    known = set(known_keys)

    for ch in chunks:
        if not looks_like_commitment(ch.text):
            continue

        what, owner, said_dm = clean(ch.text)
        if len(what) < 8:
            continue

        key = make_key(what)
        # если ключ уже известен — переиспользуем, не плодим новый
        if key in known:
            pass

        c = Commitment(
            id=_id(key),
            key=key,
            what=what,
            owner=owner,
            due=None,  # заполнит dates/ в фазе 2
            due_raw=find_due_raw(ch.text),
            said_on=_said_on(said_dm, today),
            kind=guess_kind(ch.text),
        )
        g.add_node("commitment", c)
        g.add_node("chunk", ch)
        g.add_edge(c.id, EVIDENCED_BY, ch.id)

    return g
