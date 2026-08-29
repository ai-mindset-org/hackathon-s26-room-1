#!/usr/bin/env python3
"""Адаптер: запускает штатный движок комнаты (`cli.py`) по контракту oleg_pipeline.

    python oleg_pipeline/room_engine.py --input {input} --registry {registry} [--today ГГГГ-ММ-ДД] [--room-root ПУТЬ]

`cli.py` требует `--today` и пишет реестр в `--registry` (json) и `--out` (md).
Адаптер выводит md рядом с json, как ждёт pipeline. По умолчанию `--today 2026-08-28`
(опорная дата приёмочных примеров, см. README-tool.md). `--room-root` — корень
репозитория с `cli.py`; по умолчанию корень этого репозитория.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="папка входов одного сценария")
    ap.add_argument("--registry", required=True, help="путь к registry.json (md пишется рядом)")
    ap.add_argument("--today", default="2026-08-28", help="опорная дата для cli.py (по умолчанию 2026-08-28)")
    ap.add_argument("--room-root", default=None, help="корень репозитория с cli.py")
    a = ap.parse_args()

    root = pathlib.Path(a.room_root).resolve() if a.room_root else pathlib.Path(__file__).resolve().parents[1]
    cli = root / "cli.py"
    if not cli.exists():
        print(f"room_engine: cli.py не найден в {root}; укажите --room-root", file=sys.stderr)
        return 2
    reg = pathlib.Path(a.registry).resolve()
    reg.parent.mkdir(parents=True, exist_ok=True)
    md = reg.with_suffix(".md")
    cmd = [sys.executable, str(cli), "run", "--input", str(pathlib.Path(a.input).resolve()),
           "--today", a.today, "--registry", str(reg), "--out", str(md)]
    return subprocess.run(cmd, cwd=root).returncode


if __name__ == "__main__":
    sys.exit(main())
