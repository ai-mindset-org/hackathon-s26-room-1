"""Small contract-compatible engine used to prove the pipeline end to end."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def fixture_for(input_dir: Path) -> Path | None:
    scenario = input_dir.resolve().parent.name
    for prefix in ("01", "02", "03"):
        if scenario.startswith(prefix + "-"):
            return FIXTURES / f"{prefix}.md"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run", nargs="?")
    parser.add_argument("--input", required=True)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--now")
    parser.add_argument("--wrong-booking-deadline", action="store_true")
    parser.add_argument("--fail", action="store_true")
    args = parser.parse_args()
    if args.fail:
        print("fake engine: requested failure", file=sys.stderr)
        return 23
    fixture = fixture_for(Path(args.input))
    if fixture is None:
        print(f"fake engine: no fixture for {Path(args.input).resolve().parent.name}", file=sys.stderr)
        return 24
    registry = Path(args.registry)
    registry.parent.mkdir(parents=True, exist_ok=True)
    markdown = fixture.read_text(encoding="utf-8")
    if args.wrong_booking_deadline and fixture.name == "01.md":
        markdown = markdown.replace("**до 10.09**", "**до 25.09**")
    registry.write_text(
        json.dumps({"version": 1, "obligations": [], "fake_fixture": fixture.name}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    registry.with_suffix(".md").write_text(markdown, encoding="utf-8")
    print(json.dumps({"created": 0, "updated": 0, "closed": 0, "total_open": 0, "run_id": "fake"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
