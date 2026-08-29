#!/usr/bin/env python3
"""Демо-сервер: страница + настоящий реестр из настоящего пайплайна.

    python demo/serve.py            # http://127.0.0.1:8000
    python demo/serve.py --port 9000

Зачем отдельный сервер. `demo/index.html` открывается двойным кликом и разбирает
текст на JS — это витрина продуктового поведения. Сервер добавляет вторую
вкладку, где та же страница показывает **вывод настоящего пайплайна**: сервер
запускает `python cli.py run ...` подпроцессом и отдаёт получившийся реестр.
Никакой второй реализации правил тут нет — если CLI сломан, вкладка честно
покажет ошибку, а не нарисует правдоподобную картинку.

Реестр демо лежит во временной папке, а не в `~/.commitments/registry.json`:
демо повторяемо и не трогает чужие данные.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DEMO_DIR = Path(__file__).resolve().parent
ROOT = DEMO_DIR.parent
EXAMPLES = ROOT / "examples"

# Опорная дата примеров зафиксирована: expected.md говорит «до пятницы 29.08».
TODAY = "2026-08-28"

STATE = {"registry": None, "before": {}, "log": []}


# ── реестр → плоский вид для страницы ────────────────────────────────────────


def _flatten(registry_path: Path) -> list[dict]:
    """Граф из registry.json → список карточек: что · владелец · срок · статус · цитата."""
    raw = json.loads(registry_path.read_text(encoding="utf-8"))
    nodes = raw.get("nodes", {})
    chunks = {c["id"]: c for c in nodes.get("chunk", [])}
    sources = {s["id"]: s for s in nodes.get("source", [])}

    quotes: dict[str, list[dict]] = {}
    prepares: dict[str, str] = {}
    derived: dict[str, str] = {}
    for e in raw.get("edges", []):
        kind = e.get("type") or e.get("kind")
        if kind == "EVIDENCED_BY":
            ch = chunks.get(e["dst"])
            if ch:
                src = sources.get(ch.get("source_id")) or {}
                quotes.setdefault(e["src"], []).append(
                    {"quote": ch.get("quote") or ch.get("text") or "",
                     "source": src.get("name") or "—",
                     "source_kind": src.get("kind") or ""}
                )
        elif kind == "PREPARES":
            prepares[e["src"]] = e["dst"]
        elif kind == "DERIVED_FROM":
            derived[e["src"]] = e["dst"]

    out = []
    for c in nodes.get("commitment", []):
        dl = c.get("deadline") or {}
        out.append({
            "id": c.get("id"),
            "key": c.get("key"),
            "what": c.get("what") or "",
            "owner": c.get("owner"),
            "due": c.get("due"),
            "due_raw": c.get("due_raw") or dl.get("raw"),
            "precision": dl.get("precision"),
            "boundary": dl.get("boundary"),
            "alternatives": dl.get("alternatives") or [],
            "note": dl.get("note"),
            "status": c.get("status"),
            "kind": c.get("kind"),
            "basket": c.get("basket"),
            "uncertainty": c.get("uncertainty") or [],
            "evidence": quotes.get(c.get("id"), []),
            "prepares": prepares.get(c.get("id")),
            "derived_from": derived.get(c.get("id")),
        })
    return out


def _snapshot(cards: list[dict]) -> dict:
    return {c["id"]: {"due": c["due"], "status": c["status"], "what": c["what"]}
            for c in cards}


def _diff(before: dict, cards: list[dict]) -> None:
    """Проставляет каждой карточке change: new | updated | same, и что поменялось."""
    for c in cards:
        old = before.get(c["id"])
        if old is None:
            c["change"] = "new" if before else "first"
            c["changed_fields"] = []
            continue
        changed = [f for f in ("due", "status") if old.get(f) != c[f]]
        c["change"] = "updated" if changed else "same"
        c["changed_fields"] = changed
        c["was"] = {f: old.get(f) for f in changed}


# ── запуск настоящего CLI ────────────────────────────────────────────────────


def _example_dir(name: str) -> Path:
    """'01' → examples/01-…/input. Ошибка внятная, а не пустой ответ."""
    matches = sorted(p for p in EXAMPLES.glob(f"{name}*") if (p / "input").is_dir())
    if not matches:
        available = ", ".join(sorted(p.name for p in EXAMPLES.iterdir() if p.is_dir()))
        raise FileNotFoundError(
            f"Нет примера «{name}» в {EXAMPLES}. Доступны: {available or '(пусто)'}"
        )
    return matches[0] / "input"


def _run_cli(input_dir: Path, registry: Path) -> dict:
    cmd = [sys.executable, str(ROOT / "cli.py"), "run",
           "--input", str(input_dir), "--today", TODAY, "--registry", str(registry)]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, timeout=120)
    dec = lambda b: b.decode("utf-8", "replace")  # noqa: E731
    return {"cmd": " ".join(f'"{c}"' if " " in c else c for c in cmd),
            "returncode": proc.returncode,
            "stdout": dec(proc.stdout), "stderr": dec(proc.stderr)}


def _registry_path() -> Path:
    if STATE["registry"] is None:
        STATE["registry"] = Path(tempfile.mkdtemp(prefix="demo-registry-")) / "registry.json"
    return STATE["registry"]


def do_run(example: str) -> dict:
    registry = _registry_path()
    before = STATE["before"]
    input_dir = _example_dir(example)
    run = _run_cli(input_dir, registry)
    if run["returncode"] != 0:
        raise RuntimeError(
            f"cli.py вернул код {run['returncode']}.\n"
            f"Команда: {run['cmd']}\n{run['stderr'] or run['stdout'] or '(пусто)'}"
        )
    if not registry.exists():
        raise RuntimeError(f"cli.py отработал, но реестр не появился: {registry}")
    cards = _flatten(registry)
    _diff(before, cards)
    STATE["before"] = _snapshot(cards)
    STATE["log"].append({"example": input_dir.parent.name, "cmd": run["cmd"],
                         "count": len(cards)})
    return {"ok": True, "example": input_dir.parent.name, "today": TODAY,
            "cmd": run["cmd"], "stdout": run["stdout"].strip(),
            "count": len(cards), "cards": cards, "log": STATE["log"]}


def do_reset() -> dict:
    reg = STATE["registry"]
    if reg is not None:
        shutil.rmtree(reg.parent, ignore_errors=True)
    STATE.update({"registry": None, "before": {}, "log": []})
    return {"ok": True, "count": 0, "cards": [], "log": []}


# ── HTTP ─────────────────────────────────────────────────────────────────────


class Handler(BaseHTTPRequestHandler):
    server_version = "commitments-demo"

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, payload: dict) -> None:
        self._send(code, json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    def _api(self, path: str, query: dict) -> None:
        try:
            if path == "/api/health":
                self._json(200, {"ok": True, "today": TODAY, "root": str(ROOT)})
            elif path == "/api/run":
                self._json(200, do_run((query.get("example") or ["01"])[0]))
            elif path == "/api/reset":
                self._json(200, do_reset())
            else:
                self._json(404, {"ok": False, "error": f"Нет такого API: {path}"})
        except Exception as exc:  # ошибка видна на странице, а не в тишине
            self._json(500, {"ok": False, "error": str(exc),
                             "trace": traceback.format_exc()[-1500:]})

    def do_GET(self) -> None:  # noqa: N802
        u = urlparse(self.path)
        if u.path.startswith("/api/"):
            return self._api(u.path, parse_qs(u.query))
        if u.path in ("/", "/index.html"):
            page = DEMO_DIR / "index.html"
            if not page.exists():
                return self._send(500, f"Нет файла {page}".encode("utf-8"),
                                  "text/plain; charset=utf-8")
            return self._send(200, page.read_bytes(), "text/html; charset=utf-8")
        self._send(404, b"404", "text/plain; charset=utf-8")

    def do_POST(self) -> None:  # noqa: N802
        u = urlparse(self.path)
        if u.path.startswith("/api/"):
            return self._api(u.path, parse_qs(u.query))
        self._send(404, b"404", "text/plain; charset=utf-8")

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("  %s\n" % (fmt % args))


def main() -> int:
    ap = argparse.ArgumentParser(description="Демо-сервер реестра обязательств")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()

    if not (ROOT / "cli.py").exists():
        print(f"Не вижу cli.py рядом с demo/ (искал в {ROOT})", file=sys.stderr)
        return 2

    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Демо: http://{args.host}:{args.port}/  (опорная дата {TODAY})")
    print("Вкладка «настоящий реестр» запускает cli.py по-настоящему. Ctrl+C — стоп.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановлен.")
    finally:
        srv.server_close()
        do_reset()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
