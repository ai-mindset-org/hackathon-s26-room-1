"""Тест: 0 обязательств на правилах не должно молчать, когда во входе явно
непонятая дата — но и не должно кричать на честном нуле.

extract/naive.py заточен под русский стиль examples/: 0 обязательств на
входе без такого сигнала — законный результат (T003-newsletter-zero-
obligations и другие «нулевые» сценарии в oleg_examples_quick_untrusted
специально это проверяют, и README корпуса прямо запрещает «осторожный»
список для них — ложная тревога так же вредна, как и потеря). Но 0 на
входе с датой вида MM/DD/YYYY, которую правила физически не парсят
(DATE_NUM ловит только «27.08») — это не «нечего сообщить», и молчать об
этом нельзя.

Без сети, без модели — гоняются за секунду.

Запуск:  python3 tests/test_cli_quiet_zero.py
"""

import io
import sys
from contextlib import redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cli import _extract
from core.model import Chunk


def ch(i, text):
    return Chunk(id=f"ch-{i}", text=text, quote=text, source_id="s-1")


def _stderr_of(chunks):
    buf = io.StringIO()
    with redirect_stderr(buf):
        graph = _extract(chunks, [], "2027-06-01", want_llm=False)
    return graph, buf.getvalue()


def test_us_дата_без_совпадений_предупреждает():
    graph, err = _stderr_of([ch(1, "Nina, please file the renewal packet by 04/05/2027.")])
    assert not graph.commitments()
    assert "--llm" in err


def test_честный_ноль_без_us_даты_не_предупреждает():
    """T003: 'deadline was 30 November 2026' — прошедшее время, не
    обязательство, и не MM/DD/YYYY. Ложной тревоги быть не должно."""
    graph, err = _stderr_of([
        ch(1, "Last year's volunteer application deadline was 30 November 2026."),
        ch(2, "This message is informational. No reply, booking, payment, or other action is requested."),
    ])
    assert not graph.commitments()
    assert err == ""


def test_найденное_обязательство_не_предупреждает():
    """Есть результат — предупреждать не о чем, даже если попутно есть US-дата."""
    graph, err = _stderr_of([ch(1, "статус по проекту «Витрина» нужен к понедельнику 31.08")])
    assert graph.commitments()
    assert err == ""


def test_пустой_вход_не_предупреждает():
    graph, err = _stderr_of([])
    assert not graph.commitments()
    assert err == ""


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
