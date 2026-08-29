"""Разрешение сроков: сырой текст -> Deadline (интент), а не просто дата.

Контракт модуля:

    resolve(commitments, today) -> list[Commitment]

Опорная дата — ПАРАМЕТР, не now(). Если у обязательства есть `said_on`
(дата сообщения) — считаем от неё: «до пятницы», сказанное 27.08, означает
пятницу после 27.08, а не после дня прогона.

Почему структура, а не дата:

  * «до» и «к» — разные границы. «К понедельнику» включительно, «до пятницы»
    строго значит раньше пятницы. Обе трактовки сохраняем, одну выбираем.
  * «31.08» и «до конца месяца» дают одну дату, но это сроки разной точности.
    Сортировать их как равные — врать человеку.
  * Хранить только результат нельзя: при следующем прогоне «до пятницы» уже
    не пересчитать, интент потерян.

Неразрешимый срок НЕ выбрасывает запись: она живёт с пометкой в uncertainty.
"""

from __future__ import annotations

import calendar
import datetime as dt
import re

from core.model import (
    BEFORE, BY, DAY, EXACT, FUZZY, PERIOD, Commitment, Deadline,
)

MONTHS = {
    "январ": 1, "феврал": 2, "март": 3, "апрел": 4, "ма": 5, "июн": 6,
    "июл": 7, "август": 8, "сентябр": 9, "октябр": 10, "ноябр": 11, "декабр": 12,
}

WEEKDAYS = {
    "понедельник": 0, "вторник": 1, "сред": 2, "четверг": 3,
    "пятниц": 4, "суббот": 5, "воскресень": 6,
}

WEEKDAY_NAME = {
    0: "понедельник", 1: "вторник", 2: "среда", 3: "четверг",
    4: "пятница", 5: "суббота", 6: "воскресенье",
}

ORDINALS = {
    "первого": 1, "второго": 2, "третьего": 3, "четвёртого": 4, "четвертого": 4,
    "пятого": 5, "шестого": 6, "седьмого": 7, "восьмого": 8, "девятого": 9,
    "десятого": 10, "одиннадцатого": 11, "двенадцатого": 12,
    "тринадцатого": 13, "четырнадцатого": 14, "пятнадцатого": 15,
    "двадцатого": 20, "двадцать пятого": 25, "тридцатого": 30,
}

NUM_DATE = re.compile(r"\b(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?\b")
LEAD = re.compile(r"за\s+(\d+)\s+(?:день|дня|дней)\s+до\s+(.+)", re.IGNORECASE)
DAY_MONTH = re.compile(r"\b(\d{1,2})\s+([А-Яа-яЁё]+)")
DAY_OF_MONTH = re.compile(r"\b(\d{1,2})\s+числа")


def read_boundary(raw: str) -> str:
    """«до» — строго раньше. «к», «на» — включительно.

    В деловой речи «до пятницы» почти всегда значит «включая пятницу», поэтому
    строгое прочтение мы записываем в alternatives, а не выбираем по умолчанию.
    Спор решает заказчик, а не мы молча.
    """
    low = raw.lower().lstrip()
    if low.startswith("до "):
        return BEFORE
    return BY


def _next_day_of_month(ref: dt.date, day: int) -> dt.date:
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


def resolve_one(raw: str | None, ref: dt.date) -> Deadline:
    if not raw:
        return Deadline(raw="", kind="none", precision=FUZZY,
                        note="срок не назван")

    low = raw.lower().strip()
    boundary = read_boundary(raw)
    anchor = ref.isoformat()

    def made(date: dt.date, kind: str, precision: str,
             alts: list[str] | None = None, note: str | None = None) -> Deadline:
        alternatives = list(alts or [])
        # строгое прочтение «до X» — на день раньше. Не выбираем, но показываем.
        if boundary == BEFORE and precision in (DAY, EXACT):
            strict = (date - dt.timedelta(days=1)).isoformat()
            alternatives.append(f"{strict} — если читать «до» строго")
        return Deadline(raw=raw, kind=kind, boundary=boundary, anchor=anchor,
                        date=date.isoformat(), precision=precision,
                        alternatives=alternatives, note=note)

    # «подтвердить за 3 дня» — срок считается от чужой даты, а не от опорной.
    # Ставим раньше NUM_DATE: иначе «за 3 дня до 21.09» вернёт само 21.09.
    m = LEAD.search(low)
    if m:
        base = resolve_one(m.group(2), ref)
        if base.date:
            shifted = dt.date.fromisoformat(base.date) - dt.timedelta(days=int(m.group(1)))
            return made(shifted, "lead_time", base.precision,
                        note=f"за {m.group(1)} дн. до {base.date}")
        return Deadline(raw=raw, kind="lead_time", boundary=boundary, anchor=anchor,
                        precision=FUZZY,
                        note=f"не от чего считать «{raw}»")

    # 05.09 / 14.09.2026 — названа дата
    m = NUM_DATE.search(low)
    if m:
        day, month = int(m.group(1)), int(m.group(2))
        year = int(m.group(3)) if m.group(3) else ref.year
        if not m.group(3) and month < ref.month:
            year += 1
        try:
            return made(dt.date(year, month, day), "hard", EXACT)
        except ValueError:
            return Deadline(raw=raw, kind="none", boundary=boundary,
                            anchor=anchor, precision=FUZZY,
                            note=f"не разобрал дату «{raw}»")

    if "завтра" in low:
        return made(ref + dt.timedelta(days=1), "relative", DAY)
    if "сегодня" in low:
        return made(ref, "relative", DAY)

    if "конца месяца" in low:
        last = calendar.monthrange(ref.year, ref.month)[1]
        return made(dt.date(ref.year, ref.month, last), "end_of_period", PERIOD,
                    note="граница периода, не названная дата")

    m = DAY_OF_MONTH.search(low)
    if m:
        d = _next_day_of_month(ref, int(m.group(1)))
        recurring = "кажд" in low
        return made(d, "day_of_month", DAY,
                    note="повторяется ежемесячно" if recurring else None)

    m = DAY_MONTH.search(low)
    if m:
        month = _month_from_word(m.group(2))
        if month:
            day = int(m.group(1))
            year = ref.year + 1 if month < ref.month else ref.year
            try:
                return made(dt.date(year, month, day), "hard", EXACT)
            except ValueError:
                pass

    for stem, wd in WEEKDAYS.items():
        if stem in low:
            d = _next_weekday(ref, wd)
            return made(d, "weekday", DAY,
                        note=f"ближайшая {WEEKDAY_NAME[wd]} после {anchor}")

    for word, day in sorted(ORDINALS.items(), key=lambda kv: -len(kv[0])):
        if word in low:
            return made(_next_day_of_month(ref, day), "day_of_month", DAY)

    return Deadline(raw=raw, kind="none", boundary=boundary, anchor=anchor,
                    precision=FUZZY, note=f"не разобрал срок «{raw}»")


def sort_key(c: Commitment) -> tuple:
    """Сортировка с учётом точности: сроки без даты — в конец, а среди
    равных дат неточные идут после точных."""
    rank = {EXACT: 0, DAY: 1, PERIOD: 2, FUZZY: 3}
    d = c.deadline
    if d is None or not d.date:
        return ("9999-99-99", 9, c.what)
    return (d.date, rank.get(d.precision, 3), c.what)


def resolve(commitments: list[Commitment], today: str) -> list[Commitment]:
    run_ref = dt.date.fromisoformat(today)

    for c in commitments:
        if c.deadline is not None:
            continue

        ref = run_ref
        if c.said_on:
            try:
                ref = dt.date.fromisoformat(c.said_on)
            except (ValueError, TypeError):
                ref = run_ref

        d = resolve_one(c.due_raw, ref)
        c.deadline = d
        c.due = d.date  # плоская проекция для тех, кому хватает даты

        if d.date is None and d.note:
            if d.note not in c.uncertainty:
                c.uncertainty.append(d.note)

    return commitments
