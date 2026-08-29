"""Тесты ingest/reader.py: разбор разных типов входящих.

До этого файла модуль не трогали ни разу с самого скелета — работал он
только за счёт того, что три официальных примера случайно все в UTF-8.
Реальный хаос так себя не ведёт: старые экспорты чатов и писем нередко в
cp1251 или utf-16, и модуль терял такие файлы молча — Source и Chunk'и
для них просто не появлялись, без единого предупреждения. Это ровно то,
против чего Core Value комнаты: «ничего из входящего хаоса не теряется».

Плюс OCR: раньше настоящая картинка (не перепечатанный вручную текст со
скриншота) вообще не читалась. pillow/pytesseract — опциональная
зависимость, поэтому конвейер вокруг OCR проверяется заглушкой всегда,
а сам движок — отдельным тестом, который тихо пропускает себя, если
библиотек нет.

Без сети, без модели — гоняются за секунду (кроме одного теста с реальным
OCR, если библиотеки стоят — там доли секунды на распознавание).

Запуск:  python3 -m pytest tests/ -q     или     python3 tests/test_reader.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ingest import ocr, reader
from ingest.reader import CHAT, EMAIL, PLAIN, SCREENSHOT_TEXT, TRANSCRIPT, detect_kind, read_folder


def _folder(**files: bytes | str) -> Path:
    d = Path(tempfile.mkdtemp())
    for name, content in files.items():
        data = content.encode("utf-8") if isinstance(content, str) else content
        (d / name).write_bytes(data)
    return d


# ── распознавание вида по содержимому ───────────────────────────────────

def test_письмо_по_заголовку_От():
    assert detect_kind("От: Гимназия №14 <info@school.example>\nТема: собрание\n\nТекст.") == EMAIL


def test_чат_по_двум_и_более_строкам_с_таймстампом():
    assert detect_kind(
        "[27.08 14:02] Марина: статус нужен к понедельнику\n"
        "[27.08 14:05] Игорь: ок, соберу"
    ) == CHAT


def test_транскрипт_по_тире():
    assert detect_kind(
        "— Договорились: отправляю договор завтра утром.\n"
        "— Да, я тогда бронирую зал."
    ) == TRANSCRIPT


def test_текст_со_скриншота_по_точкам_заполнителям():
    assert detect_kind(
        "Аренда офиса ....... до 3 числа каждого месяца\n"
        "Интернет ........... до 10 числа\n"
        "Страховка авто ..... продлить до 14.09.2026"
    ) == SCREENSHOT_TEXT


def test_неизвестный_вид_не_роняет_прогон_а_считается_текстом():
    """IN-04: одна строка без тире и без таймстампа — просто текст."""
    assert detect_kind("Купить корм коту.") == PLAIN


# ── чтение папки: происхождение и цитата ────────────────────────────────

def test_разные_виды_в_одной_папке_за_один_прогон():
    """IN-01/IN-02: письмо + чат + транскрипт вперемешку — все распознаны."""
    d = _folder(
        **{
            "письмо.txt": "От: школа\n\nСобрание 12 сентября.",
            "чат.txt": "[27.08 14:02] Марина: статус нужен к 31.08\n[27.08 14:05] Игорь: принял",
            "транскрипт.txt": "— Бронирую зал на 25.09.\n— Понял, забронирую.",
        }
    )
    sources, _ = read_folder(d)
    kinds = {s.name: s.kind for s in sources}
    assert kinds == {
        "письмо.txt": EMAIL,
        "чат.txt": CHAT,
        "транскрипт.txt": TRANSCRIPT,
    }


def test_цитата_совпадает_с_исходной_строкой():
    """IN-03: quote — та самая строка, по которой человек может проверить."""
    строка = "[27.08 14:05] Игорь: цифры по отгрузкам до пятницы"
    d = _folder(**{"чат.txt": f"[27.08 14:02] Марина: старт\n{строка}"})
    _, chunks = read_folder(d)
    assert any(c.quote == строка and c.text == строка for c in chunks)


# ── кодировки: не терять хаос молча ──────────────────────────────────────

def test_cp1251_не_теряется():
    строка = "[27.08 14:02] Марина: счёт подрядчику согласовать до конца месяца"
    d = _folder(**{"старый-экспорт.txt": строка.encode("cp1251")})
    sources, chunks = read_folder(d)
    assert len(sources) == 1, "файл в cp1251 пропал бесследно"
    assert any(c.text == строка for c in chunks)


def test_utf16_не_теряется():
    строка = "— Договорились: отправляю договор завтра.\n— Понял."
    d = _folder(**{"экспорт.txt": строка.encode("utf-16")})
    sources, _ = read_folder(d)
    assert len(sources) == 1, "файл в utf-16 пропал бесследно"


def test_действительно_бинарный_файл_не_роняет_прогон():
    """Не текст ни в одной кодировке, не картинка — пропускаем, но не падаем."""
    d = _folder(**{"вложение.bin": b"\x89ABC\r\n\x1a\n\x00\x01\x02\xff\xfe\x00\x00"})
    sources, chunks = read_folder(d)
    assert sources == []
    assert chunks == []


# ── OCR: настоящие картинки, не перепечатанный текст ─────────────────────

def test_is_image_по_расширению():
    assert ocr.is_image(Path("скрин.png"))
    assert ocr.is_image(Path("фото.JPG"))
    assert not ocr.is_image(Path("текст.txt"))
    assert not ocr.is_image(Path("письмо.eml"))


def _подмена_ocr(available, extract):
    """Заглушка вместо реального движка, без pytest-фикстур: в комнате тесты
    гоняются и голым `python3 tests/test_reader.py`, без monkeypatch."""
    было = (reader.ocr.AVAILABLE, reader.ocr.extract_text)
    reader.ocr.AVAILABLE, reader.ocr.extract_text = available, extract
    return было


def test_картинка_идёт_в_реестр_как_screenshot_text():
    """Заглушка вместо реального OCR — проверяем конвейер вокруг него, не сам движок."""
    было = _подмена_ocr(True, lambda f: "Аренда офиса до 3 числа")
    try:
        d = _folder(**{"фото.png": b"n/a: extract_text is mocked"})
        sources, chunks = read_folder(d)
    finally:
        reader.ocr.AVAILABLE, reader.ocr.extract_text = было

    assert len(sources) == 1
    assert sources[0].kind == SCREENSHOT_TEXT
    assert any("Аренда офиса" in c.text for c in chunks)


def test_картинка_без_поставленного_ocr_не_роняет_прогон():
    """pillow/pytesseract не установлены — честный пропуск, не падение."""
    было = _подмена_ocr(False, lambda f: None)
    try:
        d = _folder(**{"фото.png": b"n/a"})
        sources, chunks = read_folder(d)
    finally:
        reader.ocr.AVAILABLE, reader.ocr.extract_text = было

    assert sources == []
    assert chunks == []


def test_ocr_реальным_движком_если_он_поставлен():
    """Если pillow+pytesseract реально стоят — проверяем по-настоящему,
    а не только через заглушку. Иначе тихо пропускаем: OCR необязателен."""
    if not ocr.AVAILABLE:
        return
    from PIL import Image, ImageDraw

    d = _folder()
    img = Image.new("RGB", (500, 80), "white")
    ImageDraw.Draw(img).text((10, 20), "Aренда офиса до 3 числа", fill="black")
    img.save(d / "фото.png")

    sources, chunks = read_folder(d)
    assert len(sources) == 1
    assert sources[0].kind == SCREENSHOT_TEXT
    assert chunks, "OCR ничего не распознал на читаемой картинке"


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
