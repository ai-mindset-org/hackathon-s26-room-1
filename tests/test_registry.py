"""Тесты слияния. Без модели и без сети — гоняются за секунду, стоят ноль.

Запуск:  python3 -m pytest tests/ -q     или     python3 tests/test_registry.py
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.graph import DERIVED_FROM, EVIDENCED_BY, Graph
from core.model import CANCELLED, DONE, OPEN, Chunk, Commitment
from registry import merge


def C(cid, key, what, **kw):
    return Commitment(id=cid, key=key, what=what, **kw)


def G(*commitments):
    g = Graph()
    for c in commitments:
        g.add_node("commitment", c)
    return g


def active(g):
    return [c for c in g.commitments() if c.status == OPEN]


# ── дедупликация ──────────────────────────────────────────────────────

def test_повторный_прогон_не_плодит_дубли():
    a = G(C("c-1", "статус-витрина", "статус по проекту «Витрина» нужен к 31.08"))
    b = G(C("c-9", "статус-витрина", "статус по проекту «Витрина» нужен к 31.08"))
    out = merge(a, b, decisions_path="/nonexistent")
    assert len(out.commitments()) == 1, "одна и та же задача задвоилась"


def test_переформулировка_сливается_по_тексту():
    a = G(C("c-1", "статус-проекту-витрина",
            "коллеги, статус по проекту «Витрина» нужен к понедельнику 31.08"))
    b = G(C("c-9", "апдейт-статус-витрине",
            "апдейт: статус по «Витрине» переносим на среду 02.09",
            due="2026-09-02", due_raw="на среду 02.09", said_on="2026-08-28"))
    out = merge(a, b, decisions_path="/nonexistent")
    assert len(out.commitments()) == 1, "переформулировка завела вторую запись"
    assert out.commitments()[0].due == "2026-09-02", "срок не обновился"


def test_id_переживает_переформулировку():
    """Правка человека ссылается на id. Сменился id — осиротела правка."""
    a = G(C("c-СТАРЫЙ", "статус-витрина", "статус по «Витрина» к 31.08"))
    b = G(C("c-НОВЫЙ", "апдейт-витрине",
            "апдейт: статус по «Витрине» переносим на 02.09", said_on="2026-08-28"))
    out = merge(a, b, decisions_path="/nonexistent")
    assert out.commitments()[0].id == "c-СТАРЫЙ", "id сменился — правка потеряется"


# ── закрытие и отмена ─────────────────────────────────────────────────

def test_закрытие_убирает_из_активных():
    a = G(C("c-1", "цифры-отгрузкам", "@Павел с тебя цифры по отгрузкам до пятницы"))
    b = G(C("c-9", "цифры-закрыто", "цифры по отгрузкам уже отправил, закрыто",
            said_on="2026-08-28"))
    out = merge(a, b, decisions_path="/nonexistent")
    assert len(out.commitments()) == 1, "закрытие завело новую задачу"
    assert out.commitments()[0].status == DONE, "не помечено выполненным"


def test_отмена_гасит_производное_каскадом():
    """«Подтвердить за 3 дня» существует только пока существует запись на ТО."""
    parent = C("c-то", "то-автомобиля", "ТО автомобиля, запись на 21.09")
    child = C("c-подтв", "подтвердить-то", "подтвердить ТО за 3 дня")
    a = G(parent, child)
    a.add_edge(child.id, DERIVED_FROM, parent.id)

    b = G(C("c-письмо", "отмена-то",
            "Ваша запись на техническое обслуживание 21.09 отменена"))
    out = merge(a, b, decisions_path="/nonexistent")

    assert out.get("commitment", "c-то").status == CANCELLED, "родитель не снят"
    assert out.get("commitment", "c-подтв").status == CANCELLED, \
        "производное осталось: человек получит напоминание о том, чего нет"
    assert not active(out), "после отмены активных быть не должно"


def test_отмена_привязывает_доказательство():
    """Человек должен видеть, ПОЧЕМУ запись снята."""
    a = G(C("c-то", "то-автомобиля", "ТО автомобиля, запись на 21.09"))
    ch = Chunk(id="ch-1", text="письмо", quote="запись на ТО 21.09 отменена")
    b = Graph()
    sig = C("c-письмо", "отмена-то", "Ваша запись на ТО 21.09 отменена")
    b.add_node("commitment", sig)
    b.add_node("chunk", ch)
    b.add_edge(sig.id, EVIDENCED_BY, ch.id)

    out = merge(a, b, decisions_path="/nonexistent")
    assert "ch-1" in out.neighbors("c-то", EVIDENCED_BY), \
        "доказательство отмены не переехало на снятую запись"


def test_несвязанное_не_склеивается():
    a = G(C("c-1", "счёт-подрядчику", "счёт подрядчику согласовать до конца месяца"))
    b = G(C("c-9", "цифры-отгрузкам", "цифры по отгрузкам до пятницы"))
    out = merge(a, b, decisions_path="/nonexistent")
    assert len(out.commitments()) == 2, "склеились разные задачи"


def test_сигнал_без_адресата_не_теряется():
    """Recall-first: пропустить страшнее, чем показать лишнее."""
    a = G(C("c-1", "аренда-офиса", "аренда офиса до 3 числа"))
    b = G(C("c-9", "готово-непонятно", "всё готово, закрыто"))
    out = merge(a, b, decisions_path="/nonexistent")
    assert len(out.commitments()) == 2, "непривязанный сигнал выброшен молча"
    kept = out.get("commitment", "c-9")
    assert kept.uncertainty, "не помечен как сомнительный"


# ── решения человека ──────────────────────────────────────────────────

def test_правка_человека_переживает_прогон():
    with tempfile.TemporaryDirectory() as tmp:
        dec = Path(tmp) / "decisions.json"
        dec.write_text(
            json.dumps({"id": "c-1", "action": "close", "why": "сделал вчера"}),
            encoding="utf-8")

        a = G(C("c-1", "аренда-офиса", "аренда офиса до 3 числа"))
        b = G(C("c-9", "интернет", "интернет до 10 числа"))
        out = merge(a, b, decisions_path=dec)

        assert out.get("commitment", "c-1").status == DONE, \
            "решение человека затёрто прогоном"
        # и файл решений не тронут
        assert json.loads(dec.read_text(encoding="utf-8"))["id"] == "c-1"


def test_решение_set_due_поверх_извлечённого():
    with tempfile.TemporaryDirectory() as tmp:
        dec = Path(tmp) / "d.json"
        dec.write_text('{"id": "c-1", "action": "set_due", "value": "2026-09-05"}',
                       encoding="utf-8")
        a = G(C("c-1", "кружок", "оплатить кружок", due="2026-09-01"))
        out = merge(a, Graph(), decisions_path=dec)
        assert out.get("commitment", "c-1").due == "2026-09-05"


def test_решение_про_исчезнувшую_запись_не_ломает_прогон():
    with tempfile.TemporaryDirectory() as tmp:
        dec = Path(tmp) / "d.json"
        dec.write_text('{"id": "c-нет-такой", "action": "close"}', encoding="utf-8")
        out = merge(G(C("c-1", "к", "что-то")), Graph(), decisions_path=dec)
        assert len(out.commitments()) == 1


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ✓ {name}")
            except AssertionError as e:
                fails += 1
                print(f"  ✗ {name}\n      {e}")
    print(f"\n{'всё зелено' if not fails else f'провалено: {fails}'}")
    sys.exit(1 if fails else 0)
