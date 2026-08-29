"""FastAPI-сервер веб-интерфейса реестра обязательств.

Запуск:  python -m oleg_web [--port 8765]
Страница: http://127.0.0.1:8765
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse

# --------------------------------------------------------------------------
# FEATURES — единственное место, где включаются/выключаются надстройки.
# Каждая по умолчанию выключена, пока её собственный тест не пройдёт.
# Переопределение: env OLEG_WEB_FEATURES="timeline,edit" или ?features=timeline
# Префикс "-" выключает: ?features=-edit
# --------------------------------------------------------------------------
FEATURES: Dict[str, bool] = {
    "timeline": False,      # (2) раскрытие строки: история, supersession, диф прогона
    "edit": False,          # (3) inline-редактирование владельца/срока/статуса + Save
    "run_examples": False,  # кнопка «Прогнать примеры» (pipeline)
}

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
OUT_DIR = HERE / "out"
UPLOAD_DIR = OUT_DIR / "uploads"
DEFAULT_REGISTRY = OUT_DIR / "registry.json"
SAMPLE_REGISTRY = HERE / "sample" / "registry.json"


# --------------------------------------------------------------------------
# Поиск движка и пайплайна
# --------------------------------------------------------------------------
def _candidate_dirs(env_var: str, module: str) -> List[Path]:
    cands: List[Path] = []
    env = os.environ.get(env_var)
    if env:
        cands.append(Path(env))
    cands.append(REPO_ROOT)
    cands.append(REPO_ROOT.parent / "wt-engine")
    cands.append(REPO_ROOT.parent / "wt-pipeline")
    cands.append(REPO_ROOT.parent / "hackathon-s26-room-1")
    out: List[Path] = []
    for c in cands:
        try:
            c = c.resolve()
        except OSError:
            continue
        if c not in out:
            out.append(c)
    return out


def find_module_dir(env_var: str, module: str) -> Optional[Path]:
    """Каталог, из которого импортируется <module> (в нём лежит <module>/__main__.py)."""
    for c in _candidate_dirs(env_var, module):
        if (c / module / "__main__.py").is_file() or (c / module / "__init__.py").is_file():
            return c
    return None


def engine_dir() -> Optional[Path]:
    return find_module_dir("OLEG_ENGINE_DIR", "oleg_engine")


def pipeline_dir() -> Optional[Path]:
    return find_module_dir("OLEG_PIPELINE_DIR", "oleg_pipeline")


def child_env(extra_paths: List[Path]) -> Dict[str, str]:
    env = dict(os.environ)
    parts = [str(p) for p in extra_paths if p]
    old = env.get("PYTHONPATH")
    if old:
        parts.append(old)
    env["PYTHONPATH"] = os.pathsep.join(parts)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    return env


# --------------------------------------------------------------------------
# Примеры
# --------------------------------------------------------------------------
def examples_roots() -> List[Path]:
    roots: List[Path] = []
    for p in [
        Path(os.environ["OLEG_EXAMPLES_DIR"]) if os.environ.get("OLEG_EXAMPLES_DIR") else None,
        REPO_ROOT / "examples",
        REPO_ROOT.parent / "wt-examples-test" / "examples_test",
        REPO_ROOT / "examples_test",
    ]:
        if p is None:
            continue
        try:
            p = p.resolve()
        except OSError:
            continue
        if p.is_dir() and p not in roots:
            roots.append(p)
    return roots


def discover_examples() -> List[Dict[str, str]]:
    found: List[Dict[str, str]] = []
    for root in examples_roots():
        for child in sorted(root.iterdir()):
            if not child.is_dir():
                continue
            inp = child / "input"
            if inp.is_dir():
                found.append({
                    "name": f"{root.name}/{child.name}",
                    "path": str(inp),
                    "expected": str(child / "expected.md") if (child / "expected.md").is_file() else "",
                    "group": root.name,
                })
    return found


# --------------------------------------------------------------------------
# Реестр
# --------------------------------------------------------------------------
def read_registry(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_registry(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def ensure_default_registry() -> Path:
    """Если рабочего реестра ещё нет — положить рядом образец (пример 01)."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not DEFAULT_REGISTRY.is_file() and SAMPLE_REGISTRY.is_file():
        shutil.copyfile(SAMPLE_REGISTRY, DEFAULT_REGISTRY)
    return DEFAULT_REGISTRY


# --------------------------------------------------------------------------
# Прогоны (фоновые процессы + опрос)
# --------------------------------------------------------------------------
class Run:
    def __init__(self, kind: str) -> None:
        self.id = uuid.uuid4().hex[:12]
        self.kind = kind
        self.lines: List[str] = []
        self.done = False
        self.exit_code: Optional[int] = None
        self.error: Optional[str] = None
        self.summary: Optional[Dict[str, Any]] = None
        self.registry_path: Optional[str] = None
        self.report_path: Optional[str] = None
        self.cmd: str = ""
        self.started = time.time()
        self.lock = threading.Lock()

    def add(self, line: str) -> None:
        with self.lock:
            self.lines.append(line.rstrip("\r\n"))

    def snapshot(self, since: int = 0) -> Dict[str, Any]:
        with self.lock:
            return {
                "id": self.id,
                "kind": self.kind,
                "cmd": self.cmd,
                "lines": self.lines[since:],
                "next": len(self.lines),
                "done": self.done,
                "exit": self.exit_code,
                "error": self.error,
                "summary": self.summary,
                "registry_path": self.registry_path,
                "report_path": self.report_path,
                "elapsed": round(time.time() - self.started, 1),
            }


RUNS: Dict[str, Run] = {}


def _readable_error(run: Run) -> str:
    """Одна понятная строка вместо стектрейса."""
    tail = [l.strip() for l in run.lines if l.strip()]
    for line in reversed(tail):
        low = line.lower()
        if "no module named" in low:
            return f"Модуль не найден: {line}"
        if line.startswith(("Error", "ERROR", "error:", "usage:", "Ошибка")):
            return line
        if ": " in line and ("Error" in line or "Exception" in line):
            return line
    if tail:
        return tail[-1]
    return f"Процесс завершился с кодом {run.exit_code}."


def _spawn(run: Run, cmd: List[str], cwd: Path, env: Dict[str, str]) -> None:
    run.cmd = " ".join(cmd)

    def worker() -> None:
        try:
            proc = subprocess.Popen(
                cmd, cwd=str(cwd), env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace", bufsize=1,
            )
        except Exception as exc:  # noqa: BLE001
            run.error = f"Не удалось запустить процесс: {exc}"
            run.exit_code = -1
            run.done = True
            return
        assert proc.stdout is not None
        for line in proc.stdout:
            run.add(line)
        proc.wait()
        run.exit_code = proc.returncode
        # Последняя JSON-строка stdout — сводка движка.
        for line in reversed(run.lines):
            s = line.strip()
            if s.startswith("{") and s.endswith("}"):
                try:
                    run.summary = json.loads(s)
                    break
                except json.JSONDecodeError:
                    continue
        if proc.returncode != 0:
            run.error = _readable_error(run)
        run.done = True

    threading.Thread(target=worker, daemon=True).start()


# --------------------------------------------------------------------------
# Приложение
# --------------------------------------------------------------------------
app = FastAPI(title="Реестр обязательств — веб")


def effective_features(request: Optional[Request]) -> Dict[str, bool]:
    feats = dict(FEATURES)

    def apply(spec: str) -> None:
        for token in spec.split(","):
            token = token.strip()
            if not token:
                continue
            off = token.startswith("-")
            name = token[1:] if off else token
            if name == "all":
                for k in feats:
                    feats[k] = not off
            elif name in feats:
                feats[name] = not off

    env = os.environ.get("OLEG_WEB_FEATURES")
    if env:
        apply(env)
    if request is not None:
        q = request.query_params.get("features")
        if q:
            apply(q)
    return feats


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    html = (HERE / "static" / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(html)


@app.get("/api/config")
def api_config(request: Request) -> JSONResponse:
    ed, pd = engine_dir(), pipeline_dir()
    ensure_default_registry()
    return JSONResponse({
        "features": effective_features(request),
        "examples": discover_examples(),
        "examples_roots": [str(p) for p in examples_roots()],
        "registry_default": str(DEFAULT_REGISTRY),
        "engine_dir": str(ed) if ed else None,
        "pipeline_dir": str(pd) if pd else None,
        "engine_available": ed is not None,
        "pipeline_available": pd is not None,
        "repo_root": str(REPO_ROOT),
        "python": sys.executable,
    })


@app.get("/api/registry")
def api_registry(path: str = "") -> JSONResponse:
    p = Path(path) if path else ensure_default_registry()
    if not p.is_absolute():
        p = (REPO_ROOT / p).resolve()
    if not p.is_file():
        return JSONResponse({"ok": False, "error": f"Реестр не найден: {p}", "path": str(p)})
    try:
        data = read_registry(p)
    except json.JSONDecodeError as exc:
        return JSONResponse({"ok": False, "error": f"Битый JSON в {p.name}: {exc}", "path": str(p)})
    return JSONResponse({"ok": True, "path": str(p), "registry": data,
                         "mtime": p.stat().st_mtime})


@app.post("/api/run")
async def api_run(request: Request) -> JSONResponse:
    body = await request.json()
    inp = (body.get("input") or "").strip()
    if not inp:
        return JSONResponse({"ok": False, "error": "Не выбрана папка со входящими."}, status_code=400)
    inp_path = Path(inp)
    if not inp_path.is_absolute():
        inp_path = (REPO_ROOT / inp_path).resolve()
    if not inp_path.is_dir():
        return JSONResponse({"ok": False, "error": f"Папка не найдена: {inp_path}"}, status_code=400)

    ed = engine_dir()
    if ed is None:
        tried = ", ".join(str(p) for p in _candidate_dirs("OLEG_ENGINE_DIR", "oleg_engine"))
        return JSONResponse({"ok": False, "error":
            f"Движок не найден: нет модуля oleg_engine. Искали в: {tried}. "
            f"Задайте OLEG_ENGINE_DIR или дождитесь сборки движка."}, status_code=503)

    reg = Path(body.get("registry") or DEFAULT_REGISTRY)
    if not reg.is_absolute():
        reg = (OUT_DIR / reg).resolve()
    reg.parent.mkdir(parents=True, exist_ok=True)
    if body.get("fresh", True):
        for suffix in (".json", ".md"):
            f = reg.with_suffix(suffix)
            if f.is_file():
                f.unlink()

    cmd = [sys.executable, "-u", "-m", "oleg_engine", "run",
           "--input", str(inp_path), "--registry", str(reg)]
    mode = body.get("mode")
    if mode and mode != "auto":
        cmd += ["--mode", mode]
    for flag, key in (("--backend", "backend"), ("--model", "model"), ("--now", "now")):
        val = (body.get(key) or "").strip()
        if val:
            cmd += [flag, val]

    run = Run("engine")
    run.registry_path = str(reg)
    RUNS[run.id] = run
    _spawn(run, cmd, ed, child_env([ed]))
    return JSONResponse({"ok": True, "run": run.id, "cmd": " ".join(cmd), "registry_path": str(reg)})


@app.post("/api/run_examples")
async def api_run_examples(request: Request) -> JSONResponse:
    if not effective_features(request).get("run_examples"):
        return JSONResponse({"ok": False, "error": "Функция «Прогнать примеры» выключена (FEATURES.run_examples)."},
                            status_code=403)
    body = await request.json()
    ex = (body.get("examples") or "").strip()
    if not ex:
        return JSONResponse({"ok": False, "error": "Не выбрана папка примеров."}, status_code=400)
    ex_path = Path(ex)
    if not ex_path.is_absolute():
        ex_path = (REPO_ROOT / ex_path).resolve()
    if not ex_path.is_dir():
        return JSONResponse({"ok": False, "error": f"Папка примеров не найдена: {ex_path}"}, status_code=400)

    pd, ed = pipeline_dir(), engine_dir()
    if pd is None:
        return JSONResponse({"ok": False, "error":
            "Пайплайн не найден: нет модуля oleg_pipeline. Задайте OLEG_PIPELINE_DIR."}, status_code=503)
    if ed is None:
        return JSONResponse({"ok": False, "error":
            "Движок не найден: нет модуля oleg_engine. Задайте OLEG_ENGINE_DIR."}, status_code=503)

    out = OUT_DIR / "pipeline"
    out.mkdir(parents=True, exist_ok=True)
    engine_tpl = f'"{sys.executable}" -u -m oleg_engine run --input {{input}} --registry {{registry}}'
    cmd = [sys.executable, "-u", "-m", "oleg_pipeline", "run",
           "--examples", str(ex_path), "--engine", engine_tpl,
           "--judge", body.get("judge") or "codex", "--out", str(out)]
    only = (body.get("only") or "").strip()
    if only:
        cmd += ["--only", only]
    jobs = body.get("jobs")
    if jobs:
        cmd += ["--jobs", str(jobs)]

    run = Run("pipeline")
    run.report_path = str(out / "report.md")
    RUNS[run.id] = run
    _spawn(run, cmd, pd, child_env([pd, ed]))
    return JSONResponse({"ok": True, "run": run.id, "cmd": " ".join(cmd), "report_path": run.report_path})


@app.get("/api/run/{run_id}")
def api_run_status(run_id: str, since: int = 0) -> JSONResponse:
    run = RUNS.get(run_id)
    if run is None:
        return JSONResponse({"ok": False, "error": "Прогон не найден."}, status_code=404)
    snap = run.snapshot(since)
    snap["ok"] = True
    return JSONResponse(snap)


@app.post("/api/save")
async def api_save(request: Request) -> JSONResponse:
    if not effective_features(request).get("edit"):
        return JSONResponse({"ok": False, "error": "Редактирование выключено (FEATURES.edit)."}, status_code=403)
    body = await request.json()
    p = Path(body.get("path") or DEFAULT_REGISTRY)
    if not p.is_absolute():
        p = (REPO_ROOT / p).resolve()
    if not p.is_file():
        return JSONResponse({"ok": False, "error": f"Реестр не найден: {p}"}, status_code=400)
    edits = body.get("edits") or []
    if not isinstance(edits, list):
        return JSONResponse({"ok": False, "error": "Поле edits должно быть списком."}, status_code=400)

    data = read_registry(p)
    by_id = {ob.get("id"): ob for ob in data.get("obligations", [])}
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_id = "web_" + uuid.uuid4().hex[:8]
    changed = 0
    unknown: List[str] = []
    for edit in edits:
        ob = by_id.get(edit.get("id"))
        if ob is None:
            unknown.append(str(edit.get("id")))
            continue
        touched = False
        for field in ("owner", "due", "status", "what", "due_text", "kind"):
            if field not in edit:
                continue
            new = edit[field]
            if isinstance(new, str):
                new = new.strip()
                if field in ("owner", "due") and new == "":
                    new = None
            old = ob.get(field)
            if new == old:
                continue
            ob[field] = new
            ob.setdefault("history", []).append({
                "run_id": run_id, "ts": ts, "change": "manual_edit",
                "field": field, "from": old, "to": new, "source_path": None,
            })
            touched = True
        if touched:
            ob["manual"] = True
            changed += 1
    write_registry(p, data)
    fresh = read_registry(p)  # перечитали файл — доказательство записи
    return JSONResponse({"ok": True, "path": str(p), "changed": changed,
                         "unknown_ids": unknown, "run_id": run_id,
                         "registry": fresh, "mtime": p.stat().st_mtime})


@app.post("/api/upload")
async def api_upload(files: List[UploadFile] = File(...)) -> JSONResponse:
    dest = UPLOAD_DIR / (datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6])
    dest.mkdir(parents=True, exist_ok=True)
    saved = []
    for f in files:
        name = Path(f.filename or "file.txt").name
        target = dest / name
        target.write_bytes(await f.read())
        saved.append(name)
    return JSONResponse({"ok": True, "path": str(dest), "files": saved})


@app.get("/api/file")
def api_file(path: str, quote: str = "") -> JSONResponse:
    p = Path(path)
    if not p.is_absolute():
        p = (REPO_ROOT / p).resolve()
    if not p.is_file():
        return JSONResponse({"ok": False, "error": f"Файл не найден: {p}"})
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return JSONResponse({"ok": False, "error": str(exc)})
    return JSONResponse({"ok": True, "path": str(p), "text": text[:20000],
                         "quote_found": (quote in text) if quote else None})


@app.get("/api/health")
def api_health() -> JSONResponse:
    return JSONResponse({"ok": True, "features": FEATURES})
