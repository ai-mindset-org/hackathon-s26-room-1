"""Тесты производного обязательства и пункта-количества в приёмке.

Оба места до этого держались на честном слове: каскад отмен был зелен
юнит-тестом реестра, но на приёмочном примере не проверялся вовсе, а «дублей
нет» грепом непроверяемо в принципе.

Запуск:  python3 -m pytest tests/ -q     или     python3 tests/test_derived.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.graph import DERIVED_FROM, Graph
from core.model import CANCELLED, Chunk
from dates.resolve import resolve, resolve_one
from extract.naive import _split_derived, extract
from registry import merge
from runner.check import count_check

ТО = "ТО автомобиля ...... запись на 21.09, подтвердить за 3 дня"
ОТМЕНА = "Ваша запись на техническое обслуживание 21.09 отменена по вашему запросу."


def ch(i, text):
    return Chunk(id=f"ch-{i}", text=text, quote=text, source_id="s-1")


def граф_то():
    g = extract([ch(1, ТО)], [], "2026-08-28")
    resolve(g.commitments(), "2026-08-28")
    return g


def найти(g, кусок):
    return next(c for c in g.commitments() if кусок in c.what)


# ── разделение строки на два обязательства ────────────────────────────

def test_хвост_с_напоминанием_отделяется():
    head, tail, lead = _split_derived(ТО)
    assert tail == "подтвердить за 3 дня", f"хвост не отделён: {tail}"
    assert lead == "за 3 дня", f"опережение не найдено: {lead}"
    assert "подтвердить" not in head, "хвост остался в родителе"


def test_обычная_запятая_не_режет_обязательство():
    what = "коллеги, статус по проекту «Витрина» нужен к понедельнику 31.08"
    head, tail, _ = _split_derived(what)
    assert tail is None and head == what, "запись разрезана на пустом месте"


def test_уточнение_без_глагола_не_становится_обязательством():
    head, tail, _ = _split_derived("страховка авто, продление за 5 дней")
    assert tail is None, "«продление» — существительное, не долг"


# ── производное обязательство ─────────────────────────────────────────

def test_производное_ссылается_на_родителя():
    g = граф_то()
    assert len(g.commitments()) == 2, "строка дала не два обязательства"
    child = найти(g, "подтвердить")
    parent = найти(g, "ТО автомобиля")
    assert g.neighbors(child.id, DERIVED_FROM) == [parent.id], "нет ребра на родителя"


def test_срок_производного_считается_от_даты_родителя():
    child = найти(граф_то(), "подтвердить")
    assert child.due == "2026-09-18", f"ждали 18.09, получили {child.due}"
    assert child.deadline.kind == "lead_time"


def test_опережение_без_опоры_не_выдумывает_дату():
    import datetime as dt
    d = resolve_one("за 3 дня до", dt.date(2026, 8, 28))
    assert d.date is None, "срок высосан из пальца"


# ── каскад на реальном пути, а не в пробирке ──────────────────────────

def test_отмена_гасит_производное_через_весь_конвейер():
    base = merge(Graph(), граф_то(), decisions_path="/nonexistent")

    новое = extract([ch(2, ОТМЕНА)], base.known_keys(), "2026-08-28")
    resolve(новое.commitments(), "2026-08-28")
    out = merge(base, новое, decisions_path="/nonexistent")

    parent = найти(out, "ТО автомобиля")
    child = найти(out, "подтвердить")
    assert parent.status == CANCELLED, "отмена не дошла до записи на ТО"
    assert child.status == CANCELLED, "напоминание пережило отмену родителя"


def test_отмена_не_гасит_соседей():
    g = extract([ch(1, ТО), ch(3, "Интернет ........... до 10 числа")],
                [], "2026-08-28")
    resolve(g.commitments(), "2026-08-28")
    base = merge(Graph(), g, decisions_path="/nonexistent")

    новое = extract([ch(2, ОТМЕНА)], base.known_keys(), "2026-08-28")
    resolve(новое.commitments(), "2026-08-28")
    out = merge(base, новое, decisions_path="/nonexistent")

    assert найти(out, "Интернет").status != CANCELLED, "каскад задел чужую запись"


# ── пункт-количество в приёмке ────────────────────────────────────────

ПУНКТ = "Записей про «Витрину» в реестре **ровно одна** — дубля прогон не создал"


def test_количество_считается_а_не_грепается():
    одна = "- [ ] статус по проекту «Витрина» · Марина · 02.09\n  ↳ источник: чат\n"
    две = одна + "- [ ] отчёт по проекту Витрина · Игорь · 31.08\n"
    assert count_check(ПУНКТ, одна) is True, "одна запись не засчитана"
    assert count_check(ПУНКТ, две) is False, "дубль проехал незамеченным"
    assert count_check(ПУНКТ, "- [ ] счёт подрядчику · 31.08\n") is False, \
        "пустой реестр засчитан как «ровно одна»"


def test_обычный_пункт_не_считается_количеством():
    assert count_check("«Цифры по отгрузкам» — закрыто", "что угодно") is None


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
