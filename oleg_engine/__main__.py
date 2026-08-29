from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .backend import BackendError
from .engine import run_engine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m oleg_engine", description="Build and update an obligation registry from a folder of text inputs.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="ingest one input folder")
    run.add_argument("--input", required=True, type=Path)
    run.add_argument("--registry", required=True, type=Path)
    run.add_argument("--mode", choices=("auto", "parallel", "sequential"), default="auto")
    run.add_argument("--backend", choices=("codex", "claude"), default="codex")
    run.add_argument("--model")
    run.add_argument("--now", help="reference date in YYYY-MM-DD")
    run.add_argument("--json", action="store_true", help="suppress human progress text")
    run.add_argument("--prefilter", action="store_true", help="for files over 16 KiB, send only candidate chunks and one neighbour (default: off)")
    adjudication = run.add_mutually_exclusive_group()
    adjudication.add_argument("--adjudicate", dest="adjudicate", action="store_true", default=True)
    adjudication.add_argument("--no-adjudicate", dest="adjudicate", action="store_false", help="debug only; disables semantic merge")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        summary = run_engine(
            input_dir=args.input,
            registry_path=args.registry,
            mode=args.mode,
            backend=args.backend,
            model=args.model,
            now_arg=args.now,
            prefilter=args.prefilter,
            adjudicate=args.adjudicate,
        )
    except (BackendError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"engine error: {exc}", file=sys.stderr)
        return 1
    if not args.json:
        print(f"Реестр обновлён: создано {summary['created']}, обновлено {summary['updated']}, закрыто {summary['closed']}.")
    print(json.dumps(summary, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
