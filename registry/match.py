"""Сопоставление обязательств — три ступени, от дешёвой к дорогой.

1. ключ            — точное совпадение, бесплатно
2. текст и владелец — пересечение основ слов плюс общая дата, бесплатно
3. LLM-судья       — только на спорной полосе, единицы вызовов

Третья ступень подключается через параметр `judge`: если он не передан,
модуль работает полностью детерминированно, и его тесты ничего не стоят.
"""

from __future__ import annotations

import re

from core.model import Commitment

from .signals import strip_noise

DATE = re.compile(r"\b\d{1,2}\.\d{2}(?:\.\d{4})?\b")
WORD = re.compile(r"[А-Яа-яЁёA-Za-z@][А-Яа-яЁёA-Za-z@\d]{3,}")

# Шум переписки: встречается везде и сопоставлению только мешает.
STOP = {
    "колле", "приве", "спаси", "пожал", "нужно", "нужен", "нужна", "надо",
    "также", "это", "тебя", "вас", "нас", "ваша", "вашем", "запро",
    "прошу", "просим", "забыв", "напом", "котор", "будет", "может",
}

# Грубая нормализация вместо стеммера: «Витрина» и «Витрине» должны
# совпасть, а тащить pymorphy в хакатон — лишняя зависимость.
STEM = 5

# Полоса, на которой стоит спросить судью, если он есть.
SURE = 0.60
MAYBE = 0.34


def tokens(text: str) -> tuple[set[str], set[str]]:
    """-> (основы значимых слов, даты)"""
    low = strip_noise(text)
    dates = set(DATE.findall(text))
    words = set()
    for w in WORD.findall(low):
        stem = w.lower().strip("@")[:STEM]
        if stem and stem not in STOP:
            words.add(stem)
    return words, dates


def score(a: str, b: str) -> tuple[float, int, bool]:
    """-> (похожесть, сколько основ общих, есть ли общая дата)

    Считаем containment, а не Жаккара: короткое уточнение «цифры по
    отгрузкам закрыто» должно совпасть с длинной исходной формулировкой,
    хотя по Жаккару они далеки.
    """
    wa, da = tokens(a)
    wb, db = tokens(b)
    if not wa or not wb:
        return 0.0, 0, False
    shared = wa & wb
    same_date = bool(da & db)
    return len(shared) / min(len(wa), len(wb)), len(shared), same_date


def looks_same(a: str, b: str) -> tuple[bool, float]:
    """Вторая ступень: решение без модели."""
    s, n, same_date = score(a, b)
    if same_date and n >= 1:
        return True, max(s, SURE)
    if n >= 2 and s >= 0.55:
        return True, s
    return False, s


def find(
    base,
    c: Commitment,
    *,
    exclude: set[str] | None = None,
    judge=None,
) -> Commitment | None:
    """Найти в реестре то же обязательство. Ничего не меняет."""
    exclude = exclude or set()

    # ступень 1 — ключ
    same_key = base.find_commitment_by_key(c.key)
    if same_key is not None and same_key.id not in exclude:
        return same_key

    # ступень 2 — текст
    doubtful: list[tuple[float, Commitment]] = []
    for other in base.commitments():
        if other.id in exclude or other.id == c.id:
            continue
        ok, s = looks_same(c.what, other.what)
        if ok:
            return other
        if MAYBE <= s < 0.55:
            doubtful.append((s, other))

    # ступень 3 — судья, только по спорным парам
    if judge and doubtful:
        doubtful.sort(key=lambda p: -p[0])
        for _, other in doubtful[:3]:
            if judge(c.what, other.what):
                return other
    return None
