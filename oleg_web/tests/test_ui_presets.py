"""Headless-проверка пресетов команды движка и скачивания реестра (Playwright, Chromium).

Запуск из корня репозитория:  python oleg_web/tests/test_ui_presets.py [порт]
Порт также можно задать через OLEG_WEB_TEST_PORT; по умолчанию берётся свободный.
"""
import os, shutil, socket, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "oleg_web" / "sample"

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)
    print(("  OK  " if cond else "  FAIL") + " " + msg)


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def pick_port() -> int:
    for v in (sys.argv[1] if len(sys.argv) > 1 else None, os.environ.get("OLEG_WEB_TEST_PORT")):
        if v and str(v).strip().isdigit():
            return int(v)
    return free_port()


def main() -> int:
    port = pick_port()
    tmp = Path(tempfile.mkdtemp(prefix="oleg_web_preset_"))
    REG = tmp / "registry.json"
    shutil.copy(SAMPLE / "registry.json", REG)
    REG.with_suffix(".md").write_text("# Реестр обязательств (тестовая копия)", "utf-8")
    base = f"http://127.0.0.1:{port}/"
    URL = f"{base}?registry={quote(str(REG))}"
    print(f"порт {port}, временный реестр {REG}")
    srv = subprocess.Popen([sys.executable, "-m", "oleg_web", "--port", str(port)], cwd=str(ROOT),
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        up = False
        for _ in range(60):
            try:
                urllib.request.urlopen(base + "api/health", timeout=1)
                up = True
                break
            except Exception:
                time.sleep(0.3)
        check(up, "сервер поднялся")
        if not up:
            return 1
        errs = []
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            page = b.new_page()
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            page.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
            page.goto(URL)
            page.wait_for_selector("tr.ob", timeout=10000)
            time.sleep(0.4)
            n = len(page.query_selector_all("tr.ob"))
            print("rows:", n)
            check(n > 0, "реестр отрисован")
            print("preset default:", page.input_value("#engpreset"), "| field empty:", page.input_value("#engcmd") == "")
            check(page.input_value("#engcmd") == "", "по умолчанию поле команды пустое")
            print("cli option:", page.evaluate("() => { const o=document.querySelector('#engpreset option[value=cli]'); return [o.disabled, o.title, o.textContent]; }"))
            page.select_option("#engpreset", "oleg")
            page.dispatch_event("#engpreset", "change")
            after = page.input_value("#engcmd")
            print("after oleg:", after)
            check("oleg_engine" in after, "пресет oleg подставляет команду")
            page.fill("#engcmd", "x")
            print("after manual edit preset:", page.input_value("#engpreset"))
            check(page.input_value("#engpreset") == "custom", "ручная правка переключает пресет в «своя»")
            page.select_option("#engpreset", "custom")
            print("custom keeps field:", page.input_value("#engcmd"))
            check(page.input_value("#engcmd") == "x", "выбор «своя» не затирает поле")
            hrefs = page.evaluate("() => [document.querySelector('#dlmd').href, document.querySelector('#dljson').href]")
            print("hrefs:", hrefs)
            for h in hrefs:
                r = page.request.get(h)
                print("GET", h.split('?')[1][:60], "->", r.status, r.headers.get("content-type"), "bytes", len(r.body()))
                check(r.status == 200 and len(r.body()) > 0, f"скачивание отдаёт файл: {h.split('?')[1][:40]}")
            r = page.request.get(base + "api/download?kind=md&path=out/nope.json")
            print("404 case ->", r.status, r.text()[:60])
            check(r.status == 404, "скачивание несуществующего файла даёт 404")
            b.close()
        print("js errors:", errs or "none")
        check(not [e for e in errs if e.startswith("pageerror")], "нет JS-исключений на странице")
    finally:
        srv.kill()
        shutil.rmtree(tmp, ignore_errors=True)
    print(("ПРОВАЛЕНО: " + "; ".join(fails)) if fails else "ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
