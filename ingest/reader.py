"""Чтение разнородного входа и нарезка на фрагменты с точными цитатами.

Контракт модуля: read_folder(path) -> (sources, chunks).
Каждый Chunk несёт `quote` — исходную строку, по которой человек может проверить.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from core.model import Chunk, Source

EMAIL = "email"
CHAT = "chat"
TRANSCRIPT = "transcript"
SCREENSHOT_TEXT = "screenshot_text"
PLAIN = "text"

CHAT_LINE = re.compile(r"^\[\d{1,2}\.\d{2}\s+\d{1,2}:\d{2}\]\s*")
TRANSCRIPT_LINE = re.compile(r"^\s*[—–-]\s+")


def _id(prefix: str, text: str) -> str:
    return f"{prefix}-{hashlib.sha1(text.encode('utf-8')).hexdigest()[:6]}"


def detect_kind(text: str) -> str:
    """Вид источника — по содержимому, а не по расширению."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return PLAIN
    if lines[0].startswith("От:"):
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
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
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
