"""python -m oleg_web [--port 8765] [--host 127.0.0.1]"""
from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m oleg_web",
                                 description="Веб-интерфейс реестра обязательств")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--features", default="",
                    help="включить/выключить надстройки: timeline,edit,run_examples или -edit / all")
    ap.add_argument("--reload", action="store_true")
    args = ap.parse_args(argv)

    if args.features:
        import os
        prev = os.environ.get("OLEG_WEB_FEATURES", "")
        os.environ["OLEG_WEB_FEATURES"] = (prev + "," + args.features).strip(",")

    import uvicorn
    from oleg_web.server import app, ensure_default_registry

    ensure_default_registry()
    print(f"Реестр обязательств: http://{args.host}:{args.port}", flush=True)
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
