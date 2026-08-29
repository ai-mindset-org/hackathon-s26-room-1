"""Извлечение обязательств моделью. Работает с OpenAI и с Anthropic.

Сигнатура та же, что у extract.naive.extract, поэтому переключение — один флаг.
Ключ берётся из окружения или из .env (который в .gitignore).

Почему это важно: на правилах инструмент хорошо выглядит только на examples/.
На реальной пачке заказчика — с чужими формулировками, вежливыми оборотами
и косвенными просьбами — регулярки слепые.

Границу держим ту же: модель ПОНИМАЕТ (что сказано, кто должен, то же ли это,
насколько уверена), а код РЕШАЕТ (какая это дата, что обновить, что погасить).
Даты модель не считает — она врёт в арифметике; она отдаёт `due_raw` как
сказано, а разбирает его dates/.
"""

from __future__ import annotations

import json
import os
import urllib.request

import re

from core.env import load as load_env
from core.graph import DERIVED_FROM, EVIDENCED_BY, PREPARES, Graph
from core.model import Chunk, Commitment, Event

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-5"

# дата сообщения в чат-экспорте: [27.08 14:05]
CHAT_STAMP = re.compile(r"\[(\d{1,2})\.(\d{2})\s+\d{1,2}:\d{2}\]")

PROMPT = """\
Ты извлекаешь обязательства из входящих сообщений (письма, чаты, транскрипты
созвонов, текст со скриншотов). Верни ТОЛЬКО JSON, без пояснений.

Сегодня: {today}
Уже известные ключи обязательств: {known_keys}

ПРАВИЛА

1. Обязательство — то, что кто-то должен СДЕЛАТЬ. Событие (собрание, демо,
   встреча) — не обязательство: на нём надо присутствовать, а не делать.
   НО событие всё равно верни в commitments с kind="event" — человеку нужно
   видеть его в реестре. Просто не выдумывай для него действий.

2. САМАЯ ЧАСТАЯ ОШИБКА: задача, которая ГОТОВИТ событие, имеет СВОЙ срок,
   отличный от даты события. «Бронирую зал на демо 25 сентября» + «зал бронируй
   до десятого» = одна задача «забронировать зал», срок «до десятого»,
   prepares_event указывает на демо 25.09. НЕ ставь 25.09 сроком задачи.

3. Реплики про одно и то же — ОДНО обязательство, не три. В транскрипте
   «я бронирую» / «бронируй до десятого» / «понял, забронирую» — это одна
   задача. Собери из них лучшую формулировку и все цитаты в quotes.

4. Владелец — тот, кто ДОЛЖЕН СДЕЛАТЬ, а не автор сообщения.
   «@Павел с тебя цифры» — владелец Павел. «Я отправлю договор» — владелец тот,
   кто говорит. Не понял — ставь null, это нормально.

5. Производное обязательство ссылается на родителя: «подтвердить за 3 дня»
   при записи на ТО — derived_from на ключ записи на ТО.

6. Если обязательство по смыслу совпадает с известным ключом — ВЕРНИ ЭТОТ
   КЛЮЧ. Формулировка могла измениться, обязательство то же.

7. Пропустить хуже, чем показать лишнее. Сомневаешься — верни с пометкой
   в uncertainty, а не молчи.

8. due_raw — срок РОВНО как сказано в тексте. НЕ вычисляй дату, не переводи
   «до пятницы» в число. Это сделает код.

9. quotes — точные строки из входа, по которым человек может проверить.
   Копируй дословно, включая служебные префиксы.

10. Таблица или расписание — это ТОЖЕ обязательства, по одному на строку.
    «Аренда офиса ....... до 3 числа каждого месяца» — обязательство
    «оплатить аренду офиса», due_raw «до 3 числа каждого месяца»,
    kind="recurring". Не пропускай строки только потому, что это таблица,
    а не предложение. Точки-заполнители игнорируй.

11. Отмену НЕ применяй сам: если письмо говорит «запись отменена», всё равно
    верни и запись, и факт отмены отдельными обязательствами. Что чем гасится,
    решит код по рёбрам.

ФОРМАТ
{{"commitments": [
   {{"key": "слаг-два-три-слова", "what": "что сделать",
     "owner": null, "due_raw": "до пятницы",
     "kind": "task|event|recurring", "basket": "mine|work|unknown",
     "derived_from": null, "prepares_event": null,
     "uncertainty": [], "quotes": ["точная строка"]}}],
 "events": [{{"id": "ev-1", "title": "демо", "date_raw": "25 сентября"}}]}}

ВХОДЯЩИЕ
{text}
"""


def _provider() -> str | None:
    load_env()
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    return None


def available() -> bool:
    return _provider() is not None


def describe() -> str:
    """Для честной декларации: какая модель реально в контуре."""
    p = _provider()
    if p == "openai":
        return os.environ.get("LLM_MODEL", DEFAULT_OPENAI_MODEL)
    if p == "anthropic":
        return os.environ.get("LLM_MODEL", DEFAULT_ANTHROPIC_MODEL)
    return "нет"


def _post(url: str, body: dict, headers: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), headers=headers
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _call(prompt: str, timeout: int = 90) -> str:
    provider = _provider()
    if provider is None:
        raise RuntimeError("нет ключа: ни OPENAI_API_KEY, ни ANTHROPIC_API_KEY")

    if provider == "openai":
        data = _post(
            OPENAI_URL,
            {
                "model": os.environ.get("LLM_MODEL", DEFAULT_OPENAI_MODEL),
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
                "temperature": 0,
            },
            {
                "content-type": "application/json",
                "authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            },
            timeout,
        )
        return data["choices"][0]["message"]["content"]

    data = _post(
        ANTHROPIC_URL,
        {
            "model": os.environ.get("LLM_MODEL", DEFAULT_ANTHROPIC_MODEL),
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        },
        {
            "content-type": "application/json",
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
        },
        timeout,
    )
    return data["content"][0]["text"]


def call(prompt: str, timeout: int = 90) -> str:
    """Публичная точка входа для других модулей (например, судьи в runner/)."""
    return _call(prompt, timeout)


def _parse(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        raw = raw[4:] if raw.startswith("json") else raw
    start, end = raw.find("{"), raw.rfind("}")
    return json.loads(raw[start:end + 1]) if start >= 0 else {}


def extract(chunks: list[Chunk], known_keys: list[str], today: str) -> Graph:
    """Тот же контракт, что у naive.extract."""
    text = "\n".join(c.text for c in chunks)
    raw = _call(PROMPT.format(
        today=today,
        known_keys=", ".join(known_keys) or "(пусто)",
        text=text,
    ))
    data = _parse(raw)

    g = Graph()
    by_quote = {c.quote: c for c in chunks}
    key_to_id: dict[str, str] = {}

    for ev in data.get("events", []):
        g.add_node("event", Event(id=ev.get("id", "ev"),
                                  title=ev.get("title", ""), date=None))

    rows = data.get("commitments", [])

    for i, row in enumerate(rows):
        key = row.get("key") or f"без-названия-{i}"
        cid = f"c-{key}"
        key_to_id[key] = cid

        c = Commitment(
            id=cid,
            key=key,
            what=row.get("what", ""),
            owner=row.get("owner"),
            due_raw=row.get("due_raw"),
            kind=row.get("kind") or "task",
            basket=row.get("basket") or "unknown",
            uncertainty=list(row.get("uncertainty") or []),
        )
        g.add_node("commitment", c)

        for q in row.get("quotes") or []:
            ch = by_quote.get(q) or next(
                (x for x in chunks if q and q in x.text), None
            )
            if ch:
                g.add_node("chunk", ch)
                g.add_edge(c.id, EVIDENCED_BY, ch.id)
                # относительный срок считается от даты сообщения, а не прогона:
                # «до пятницы», сказанное 27.08, — это пятница после 27.08
                if c.said_on is None:
                    stamp = CHAT_STAMP.search(ch.text)
                    if stamp:
                        c.said_on = (
                            f"{today[:4]}-{stamp.group(2)}-{int(stamp.group(1)):02d}"
                        )

        if row.get("prepares_event"):
            g.add_edge(c.id, PREPARES, row["prepares_event"])

    # события, которые модель унесла в events и не продублировала в commitments,
    # материализуем сами: человеку нужно видеть их в реестре.
    # Уговаривать промпт ненадёжно — дешевле гарантировать кодом.
    seen = {c.what.lower() for c in g.commitments()}
    for ev in data.get("events", []):
        title = (ev.get("title") or "").strip()
        if not title or any(title.lower() in s for s in seen):
            continue
        ec = Commitment(
            id=f"c-{ev.get('id', title)}",
            key=ev.get("id", title),
            what=title,
            due_raw=ev.get("date_raw"),
            kind="event",
        )
        g.add_node("commitment", ec)
        for ch in chunks:
            if title.lower() in ch.text.lower():
                g.add_node("chunk", ch)
                g.add_edge(ec.id, EVIDENCED_BY, ch.id)
                break

    # рёбра на родителей — вторым проходом, когда все id известны
    for row in rows:
        parent = row.get("derived_from")
        if parent and parent in key_to_id and row.get("key") in key_to_id:
            g.add_edge(key_to_id[row["key"]], DERIVED_FROM, key_to_id[parent])

    return g
