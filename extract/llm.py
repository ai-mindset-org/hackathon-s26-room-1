"""Извлечение через модель — шов, включается ключом в окружении.

Сигнатура та же, что у extract.naive.extract, поэтому переключение сводится
к одной строке в cli.py. Без ключа модуль честно говорит «не могу» и вызывающая
сторона откатывается на правила.

Почему это важно: на regexp инструмент хорошо выглядит только на examples/.
На реальной пачке заказчика — разнородной, с чужими формулировками — правила
рассыпаются. Промпт ниже уже написан и проверен глазами; ему нужен только ключ.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from core.graph import EVIDENCED_BY, PREPARES, Graph
from core.model import Chunk, Commitment, Event

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"

PROMPT = """\
Ты извлекаешь обязательства из входящих сообщений. Верни ТОЛЬКО JSON.

Опорная дата (сегодня): {today}
Уже известные ключи обязательств: {known_keys}

Правила:
1. Обязательство — то, что кто-то должен СДЕЛАТЬ. Событие (встреча, собрание,
   демо) — не обязательство: на нём надо присутствовать, а не делать.
2. Если задача ГОТОВИТ событие — у задачи свой срок, у события своя дата.
   «Забронировать зал до 10.09 для демо 25.09» — срок задачи 10.09, НЕ 25.09.
   Это самая частая ошибка. Проверь себя дважды.
3. Производное обязательство («подтвердить за 3 дня до записи») ссылается на
   родителя через derived_from.
4. Если обязательство совпадает по смыслу с известным ключом — ВЕРНИ ЭТОТ КЛЮЧ,
   не придумывай новый. Формулировка могла измениться, обязательство то же.
5. Владелец — тот, кто должен сделать. «@Павел с тебя цифры» — владелец Павел,
   а не автор сообщения. Не назван — оставь null, это нормально.
6. Лучше вернуть сомнительное с пометкой в uncertainty, чем промолчать.
   Пропустить обязательство хуже, чем показать лишнее.
7. due_raw — срок ровно как сказано в тексте, не разбирай его в дату.
8. quote — точная строка из входа, по которой человек может проверить.

Формат:
{{"commitments": [{{"key": "слаг-из-двух-трёх-слов", "what": "...",
  "owner": null, "due_raw": "...", "kind": "task|event|recurring",
  "derived_from": null, "prepares_event": null, "uncertainty": [],
  "quote": "..."}}],
 "events": [{{"id": "ev-1", "title": "...", "date_raw": "..."}}]}}

Входящие:
{text}
"""


class NoKey(RuntimeError):
    pass


def available() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def _call(prompt: str, timeout: int = 60) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise NoKey("ANTHROPIC_API_KEY не задан")

    body = json.dumps({
        "model": MODEL,
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL, data=body,
        headers={
            "content-type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read())
    return payload["content"][0]["text"]


def _parse(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        raw = raw[4:] if raw.startswith("json") else raw
    start, end = raw.find("{"), raw.rfind("}")
    return json.loads(raw[start:end + 1]) if start >= 0 else {}


def extract(chunks: list[Chunk], known_keys: list[str], today: str) -> Graph:
    """Тот же контракт, что у naive.extract. Бросает NoKey без ключа."""
    text = "\n".join(f"[{c.id}] {c.text}" for c in chunks)
    raw = _call(PROMPT.format(
        today=today,
        known_keys=", ".join(known_keys) or "(пусто)",
        text=text,
    ))
    data = _parse(raw)

    g = Graph()
    by_quote = {c.quote: c for c in chunks}

    for ev in data.get("events", []):
        g.add_node("event", Event(id=ev["id"], title=ev.get("title", ""),
                                  date=None))

    for i, row in enumerate(data.get("commitments", [])):
        c = Commitment(
            id=f"c-{row.get('key', i)}",
            key=row.get("key", f"без-названия-{i}"),
            what=row.get("what", ""),
            owner=row.get("owner"),
            due_raw=row.get("due_raw"),
            kind=row.get("kind", "task"),
            uncertainty=list(row.get("uncertainty") or []),
        )
        g.add_node("commitment", c)

        ch = by_quote.get(row.get("quote", ""))
        if ch:
            g.add_node("chunk", ch)
            g.add_edge(c.id, EVIDENCED_BY, ch.id)

        if row.get("prepares_event"):
            g.add_edge(c.id, PREPARES, row["prepares_event"])

    return g
