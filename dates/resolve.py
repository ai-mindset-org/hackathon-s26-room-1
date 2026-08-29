"""Разрешение сроков: due_raw -> due (ГГГГ-ММ-ДД).

Контракт модуля:

    resolve(commitments, today) -> list[Commitment]

Опорная дата — ПАРАМЕТР, не now(). Если у обязательства есть `said_on`
(дата сообщения, из которого оно извлечено) — считаем от неё: «до пятницы»,
сказанное 27.08, означает пятницу после 27.08, а не после дня прогона.

Неразрешимый срок НЕ выбрасывает запись: она остаётся живой с пометкой
в `uncertainty`. Пропустить страшнее, чем показать лишнее.
"""

from __future__ import annotations

import calendar
import datetime as dt
import re

from core.model import Commitment

MONTHS = {
    "январ": 1, "феврал": 2, "март": 3, "апрел": 4, "ма": 5, "июн": 6,
    "июл": 7, "август": 8, "сентябр": 9, "октябр": 10, "ноябр": 11, "декабр": 12,
}

WEEKDAYS = {
    "понедельник": 0, "вторник": 1, "сред": 2, "четверг": 3,
    "пятниц": 4, "суббот": 5, "воскресень": 6,
}

ORDINALS = {
    "первого": 1, "второго": 2, "третьего": 3, "четвёртого": 4, "четвертого": 4,
    "пятого": 5, "шестого": 6, "седьмого": 7, "восьмого": 8, "девятого": 9,
    "десятого": 10, "одиннадцатого": 11, "двенадцатого": 12,
    "тринадцатого": 13, "четырнадцатого": 14, "пятнадцатого": 15,
    "двадцатого": 20, "двадцать пятого": 25, "тридцатого": 30,
}

NUM_DATE = re.compile(r"\b(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?\b")
DAY_MONTH = re.compile(r"\b(\d{1,2})\s+([А-Яа-яЁё]+)")
DAY_OF_MONTH = re.compile(r"\b(\d{1,2})\s+числа")


def _next_day_of_month(ref: dt.date, day: int) -> dt.date:
    """Ближайшее число месяца строго после опорной даты."""
    if day > ref.day:
        last = calendar.monthrange(ref.year, ref.month)[1]
        return dt.date(ref.year, ref.month, min(day, last))
    year, month = (ref.year + 1, 1) if ref.month == 12 else (ref.year, ref.month + 1)
    last = calendar.monthrange(year, month)[1]
    return dt.date(year, month, min(day, last))


def _next_weekday(ref: dt.date, weekday: int) -> dt.date:
    delta = (weekday - ref.weekday()) % 7
    return ref + dt.timedelta(days=delta or 7)


def _month_from_word(word: str) -> int | None:
    low = word.lower()
    for stem, num in MONTHS.items():
        if low.startswith(stem):
            return num
    return None


def resolve_one(raw: str | None, ref: dt.date) -> tuple[str | None, str | None]:
    """-> (ГГГГ-ММ-ДД или None, причина неуверенности или None)"""
    if not raw:
        return None, "срок не назван"

    low = raw.lower().strip()

    # 05.09 / 14.09.2026
    m = NUM_DATE.search(low)
    if m:
        day, month = int(m.group(1)), int(m.group(2))
        year = int(m.group(3)) if m.group(3) else ref.year
        if not m.group(3) and month < ref.month:
            year += 1
        try:
            return dt.date(year, month, day).isoformat(), None
        except ValueError:
            return None, f"не разобрал дату «{raw}»"

    # завтра / сегодня
    if "завтра" in low:
        return (ref + dt.timedelta(days=1)).isoformat(), None
    if "сегодня" in low:
        return ref.isoformat(), None

    # до конца месяца
    if "конца месяца" in low:
        last = calendar.monthrange(ref.year, ref.month)[1]
        return dt.date(ref.year, ref.month, last).isoformat(), None

    # до 3 числа каждого месяца / до 10 числа
    m = DAY_OF_MONTH.search(low)
    if m:
        return _next_day_of_month(ref, int(m.group(1))).isoformat(), None

    # 5 сентября / 12 сентября
    m = DAY_MONTH.search(low)
    if m:
        month = _month_from_word(m.group(2))
        if month:
            day = int(m.group(1))
            year = ref.year + 1 if month < ref.month else ref.year
            try:
                return dt.date(year, month, day).isoformat(), None
            except ValueError:
                return None, f"не разобрал дату «{raw}»"

    # до пятницы / к понедельнику
    for stem, wd in WEEKDAYS.items():
        if stem in low:
            return _next_weekday(ref, wd).isoformat(), None

    # до десятого / до двадцать пятого
    for word, day in sorted(ORDINALS.items(), key=lambda kv: -len(kv[0])):
        if word in low:
            return _next_day_of_month(ref, day).isoformat(), None

    return None, f"не разобрал срок «{raw}»"


def resolve(commitments: list[Commitment], today: str) -> list[Commitment]:
    run_ref = dt.date.fromisoformat(today)

    for c in commitments:
        if c.due:
            continue
        # относительное считаем от даты сообщения, если она известна
        ref = run_ref
        if getattr(c, "said_on", None):
            try:
                ref = dt.date.fromisoformat(c.said_on)
            except (ValueError, TypeError):
                ref = run_ref

        due, why = resolve_one(c.due_raw, ref)
        c.due = due
        if why and why not in c.uncertainty:
            c.uncertainty.append(why)

    return commitments
