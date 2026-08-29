"""OCR для настоящих картинок (не перепечатанного вручную текста).

`ingest/reader.py` умел только «текст со скриншота» — .txt-файл, куда
кто-то уже перепечатал содержимое фото. Реальный .png/.jpg с телефона
раньше тихо (потом — с предупреждением) пропускался: распознавания не
было вообще.

pillow и pytesseract — опциональные зависимости, ровно как ключ модели
для `extract/llm.py`: комната принципиально работает без pip install
(README: naive-путь «работает всегда и бесплатно»), поэтому если их нет
— не падаем, а откатываемся на честный пропуск с объяснением.

Установка (нужна один раз, не для остального конвейера):
    brew install tesseract          # сам движок распознавания
    pip3 install pillow pytesseract
"""

from __future__ import annotations

from pathlib import Path

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp", ".gif"}

try:
    import pytesseract
    from PIL import Image

    AVAILABLE = True
except ImportError:
    AVAILABLE = False


def is_image(f: Path) -> bool:
    return f.suffix.lower() in IMAGE_SUFFIXES


# rus+eng лучше всего для комнаты (примеры двуязычные), но языковой пакет
# rus часто не поставлен вместе с tesseract из коробки — тогда откатываемся
# на eng, а не теряем OCR целиком из-за отсутствующего пакета.
_LANGS = ("rus+eng", "eng", None)


def extract_text(f: Path) -> str | None:
    """Распознать текст на картинке. None — OCR недоступен, файл битый
    или движок ничего не нашёл (пустое фото, не текст)."""
    if not AVAILABLE:
        return None
    try:
        with Image.open(f) as img:
            img.load()
            for lang in _LANGS:
                try:
                    text = pytesseract.image_to_string(img, lang=lang) if lang else pytesseract.image_to_string(img)
                    break
                except pytesseract.TesseractError:
                    continue
            else:
                return None
    except Exception:
        # битый файл, неподдержанный формат, tesseract не поставлен и т.п. —
        # это тот же «не смог прочитать», что и для остальных источников
        return None
    text = text.strip()
    return text or None
