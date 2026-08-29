"""Чтение разнородного входа и нарезка на фрагменты с точными цитатами.

Контракт модуля: read_folder(path) -> (sources, chunks).
Каждый Chunk несёт `quote` — исходную строку, по которой человек может проверить.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

from core.model import Chunk, Source
from ingest import ocr

EMAIL = "email"
CHAT = "chat"
TRANSCRIPT = "transcript"
SCREENSHOT_TEXT = "screenshot_text"
PLAIN = "text"

CHAT_LINE = re.compile(r"^\[\d{1,2}\.\d{2}\s+\d{1,2}:\d{2}\]\s*")
TRANSCRIPT_LINE = re.compile(r"^\s*[—–-]\s+")

# Реальные экспорты редко приходят в UTF-8: старые чаты и письма из
# почтовых клиентов на Windows часто в cp1251. Пробуем по очереди — иначе
# файл теряется молча, а Core Value комнаты как раз «ничего из входящего
# хаоса не теряется».
_ENCODINGS = ("utf-8", "utf-8-sig", "cp1251")

# utf-16 без BOM неотличим от бинарника по нулевым байтам (они там —
# половина каждого символа), поэтому доверяем ему только с BOM в начале.
_BOM_ENCODINGS = ((b"\xff\xfe", "utf-16"), (b"\xfe\xff", "utf-16"), (b"\xef\xbb\xbf", "utf-8-sig"))


def _id(prefix: str, text: str) -> str:
    return f"{prefix}-{hashlib.sha1(text.encode('utf-8')).hexdigest()[:6]}"


def _read_text(f: Path) -> str | None:
    """Прочитать файл, перебирая кодировки. None — реально нечитаемо
    (бинарник или файловая ошибка), и вызывающий код должен это озвучить,
    а не проглотить.

    Однобайтовые кодировки вроде cp1251 расшифровывают почти любые байты
    без ошибки — иначе фото или PDF в папке тихо превратились бы в мусорный
    «текст» вместо честного пропуска. Поэтому сперва отсекаем бинарник по
    нулевому байту (тот же трюк, что у git), и только потом перебираем
    кодировки для настоящего текста. BOM проверяем отдельно и раньше —
    у utf-16 нулевые байты часть кодировки, а не признак бинарника."""
    try:
        with f.open("rb") as raw:
            head = raw.read(8000)
    except OSError:
        return None

    for bom, enc in _BOM_ENCODINGS:
        if head.startswith(bom):
            try:
                return f.read_text(encoding=enc)
            except (UnicodeDecodeError, UnicodeError, OSError):
                return None

    if b"\x00" in head:
        return None
    for enc in _ENCODINGS:
        try:
            return f.read_text(encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
        except OSError:
            return None
    return None


def detect_kind(text: str) -> str:
    """Вид источника — по содержимому, а не по расширению."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return PLAIN
    if lines[0].startswith(("От:", "From:")):
        return EMAIL
    if sum(bool(CHAT_LINE.match(ln)) for ln in lines) >= 2:
        return CHAT
    if sum(bool(TRANSCRIPT_LINE.match(ln)) for ln in lines) >= 2:
        return TRANSCRIPT
    if len(lines) >= 3 and sum("...." in ln or "…" in ln for ln in lines) >= 2:
        return SCREENSHOT_TEXT
    return PLAIN


def _email_chunks(text: str) -> list[str]:
    """Тело письма режем по предложениям: обязательство редко совпадает со строкой."""
    lines = text.splitlines()
    body_start = 0
    for i, ln in enumerate(lines):
        if not ln.strip():
            body_start = i + 1
            break
    body = " ".join(ln.strip() for ln in lines[body_start:] if ln.strip())
    parts = re.split(r"(?<=[.!?])\s+", body)
    return [p.strip() for p in parts if p.strip()]


def _line_chunks(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def chunk_text(text: str, kind: str) -> list[str]:
    if kind == EMAIL:
        return _email_chunks(text)
    # чат, транскрипт, скриншот и простой текст — по строке:
    # там строка и есть смысловая единица
    return _line_chunks(text)


def read_folder(path: str | Path) -> tuple[list[Source], list[Chunk]]:
    """Прочитать папку с входящими. Неизвестный вид не роняет прогон."""
    path = Path(path)
    sources: list[Source] = []
    chunks: list[Chunk] = []

    for f in sorted(path.iterdir()):
        if f.is_dir():
            continue

        if ocr.is_image(f):
            # настоящее фото/скриншот, а не перепечатанный текст — вид
            # известен по происхождению файла, гадать по содержимому не надо
            text = ocr.extract_text(f)
            if text is None:
                why = ("OCR не поставлен: pip3 install pillow pytesseract"
                       if not ocr.AVAILABLE else "не нашёл текста на картинке")
                print(f"ingest: {f.name} — {why}, файл пропущен", file=sys.stderr)
                continue
            kind = SCREENSHOT_TEXT
        else:
            text = _read_text(f)
            if text is None:
                # не роняем прогон, но и не молчим: человек должен знать,
                # что часть хаоса не доехала, а не решить, что её не было
                print(f"ingest: не смог прочитать {f.name} — файл пропущен", file=sys.stderr)
                continue
            kind = detect_kind(text)

        src = Source(id=_id("src", f.name), kind=kind, name=f.name)
        sources.append(src)

        for raw in chunk_text(text, kind):
            chunks.append(
                Chunk(
                    id=_id("ch", f"{f.name}{raw}"),
                    text=raw,
                    quote=raw,
                    source_id=src.id,
                )
            )

    return sources, chunks
