"""Headless UI-проверка веб-интерфейса (Playwright, Chromium).

Запуск из корня репозитория:  python oleg_web/tests/test_ui_headless.py [порт]
Порт также можно задать через OLEG_WEB_TEST_PORT; по умолчанию берётся свободный.
Сервер поднимается сам, реестр пишется во временный файл (репозиторий не меняется).
"""
import json, os, socket, subprocess, sys, tempfile, time, urllib.request, shutil
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "oleg_web" / "sample"


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


FAKE_SRC = '''import argparse, json, shutil, sys
from pathlib import Path
SAMPLE = Path(sys.argv[0]).resolve().parent / "sample"
ap = argparse.ArgumentParser(); ap.add_argument("run", nargs="?"); ap.add_argument("--input"); ap.add_argument("--registry")
a = ap.parse_args()
scen = Path(a.input).resolve().parent.name
src = SAMPLE / ("registry-after-02.json" if scen.startswith("02") else "registry.json")
data = json.loads(src.read_text("utf-8"))
data["fake_fixture"] = scen
Path(a.registry).write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
print(json.dumps({"created": 8, "updated": 1, "closed": 1, "total_open": 7, "run_id": "fakeeng"}))
'''

COPY_SRC = '''import argparse, shutil, sys
from pathlib import Path
SAMPLE = Path(sys.argv[0]).resolve().parent / "sample"
ap = argparse.ArgumentParser(); ap.add_argument("run", nargs="?"); ap.add_argument("--input"); ap.add_argument("--registry")
a = ap.parse_args()
scen = Path(a.input).resolve().parent.name
src = SAMPLE / ("registry-after-02.json" if scen.startswith("02") else "registry.json")
shutil.copy(src, a.registry)
print('{"created": 8, "updated": 1, "closed": 1, "total_open": 7, "run_id": "copyeng"}')
'''

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)
    print(("  OK  " if cond else "  FAIL") + " " + msg)


def rows(page):
    return page.evaluate("""() => [...document.querySelectorAll('tr.ob')].map(tr => {
        const td = tr.querySelectorAll('td');
        const v = el => el ? (el.querySelector('input,select') ? el.querySelector('input,select').value : el.textContent.trim()) : null;
        return {what: td[1].textContent.trim(), owner: v(td[2]), due: v(td[3]), status: v(td[5]),
                src: td[6].querySelector('.src').textContent.trim(), quote: td[6].querySelector('.quote').textContent.trim(), closed: tr.classList.contains('closed')};
    })""")


def run(page, ex_substr, engcmd, fresh, wait_s=30):
    page.select_option("#ex", label=page.evaluate(f"""() => [...document.querySelectorAll('#ex option')].map(o=>o.textContent).find(t=>t.includes('{ex_substr}'))"""))
    page.fill("#engcmd", engcmd)
    page.click(f"#fresh button:has-text('{'новый' if fresh else 'поверх'}')")
    page.click("#run")
    t0 = time.time()
    while time.time() - t0 < wait_s:
        if not page.is_disabled("#run") and (page.text_content("#status") or "").strip() and "выполняется" not in page.text_content("#status"):
            break
        if page.is_visible("#err") and not page.is_disabled("#run"):
            break
        time.sleep(0.3)
    return {"status": page.text_content("#status"), "err": page.text_content("#err") if page.is_visible("#err") else "",
            "log": page.text_content("#log")[-400:], "rows": rows(page)}


def main() -> int:
    port = pick_port()
    tmp = Path(tempfile.mkdtemp(prefix="oleg_web_ui_"))
    shutil.copytree(SAMPLE, tmp / "sample")
    REG = tmp / "registry.json"
    shutil.copy(SAMPLE / "registry.json", REG)
    (tmp / "fake_engine.py").write_text(FAKE_SRC, "utf-8")
    (tmp / "copy_engine.py").write_text(COPY_SRC, "utf-8")
    URL = f"http://127.0.0.1:{port}/?registry={quote(str(REG))}"
    print(f"порт {port}, временный реестр {REG}")
    srv = subprocess.Popen([sys.executable, "-m", "oleg_web", "--port", str(port)], cwd=str(ROOT),
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    errs = []
    try:
        up = False
        for _ in range(60):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=1)
                up = True
                break
            except Exception:
                time.sleep(0.3)
        check(up, "сервер поднялся")
        if not up:
            return 1
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            page = b.new_page()
            page.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}") if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
            page.on("requestfailed", lambda r: errs.append(f"reqfail: {r.url} {r.failure}"))
            page.goto(URL)
            page.wait_for_selector("tr.ob", timeout=10000)
            time.sleep(0.5)
            r0 = rows(page)
            print("C1 rows:", len(r0), "| count:", page.text_content("#count"), "| feat:", page.text_content("#hdr-feat"),
                  "| boot err:", page.text_content("#err") if page.is_visible("#err") else "-")
            for r in r0:
                print("   ", json.dumps(r, ensure_ascii=False)[:230])
            check(len(r0) > 0, "C1 реестр отрисован")
            check(all(r['what'] and r['due'] and r['status'] and r['src'] and r['quote'] for r in r0), "C1 поля заполнены")
            opts = page.evaluate("() => [...document.querySelectorAll('#ex option')].map(o=>o.textContent)")
            print("C1 options:", opts)
            check(len(opts) >= 2, "C1 примеры найдены")
            # C2a «фиктивный» движок
            fake = f'python "{tmp / "fake_engine.py"}" run --input {{input}} --registry {{registry}}'
            a = run(page, "01", fake, True)
            print("C2a fake01 fresh:", a["status"], "| err:", a["err"], "| rows:", len(a["rows"]))
            check(not a["err"] and len(a["rows"]) > 0, "C2a прогон «с нуля» без ошибки")
            a = run(page, "02", fake, False)
            disk_marker = json.loads(REG.read_text('utf-8')).get("fake_fixture")
            print("C2a fake02 ontop:", a["status"], "| err:", a["err"], "| rows:", len(a["rows"]), "| disk:", disk_marker)
            check(bool(disk_marker), "C2a движок записал реестр на диск")
            # C2b копирующий движок — проверка отображения слитого состояния
            ce = f'python "{tmp / "copy_engine.py"}" run --input {{input}} --registry {{registry}}'
            a = run(page, "01", ce, True)
            print("C2b copy01 fresh:", a["status"], "| rows:", len(a["rows"]))
            a = run(page, "02", ce, False)
            vit = [r for r in a["rows"] if "Витрин" in r["what"]]
            otg = [r for r in a["rows"] if "отгруз" in r["what"]]
            print("C2b copy02 ontop:", a["status"], "| rows:", len(a["rows"]), "| Витрина rows:", len(vit),
                  [(v['due'], v['status']) for v in vit], "| отгрузки:", [(o['status'], o['closed']) for o in otg],
                  "| diff:", page.text_content("#diff"))
            ids = page.evaluate("() => [...document.querySelectorAll('tr.ob .caret')].map(c=>c.dataset.id)")
            print("C2b ids dup:", len(ids) - len(set(ids)), "closed at bottom:", [r['closed'] for r in a["rows"]])
            check(len(ids) == len(set(ids)), "C2b нет дублей id")
            # C3 таймлайн
            page.click("tr.ob .caret >> nth=0")
            time.sleep(0.3)
            tl = page.query_selector_all("tr.tl")
            print("C3 timeline rows:", len(tl), "| text:", (tl[0].text_content().strip()[:300] if tl else "-"))
            check(len(tl) > 0, "C3 таймлайн раскрывается")
            page.click("tr.ob .caret >> nth=0")
            time.sleep(0.2)
            # C3 правка + сохранение
            first_id = ids[0]
            page.fill(f"input.ed[data-id='{first_id}'][data-f='owner']", "Тестовый Владелец")
            time.sleep(0.2)
            print("C3 save visible:", page.is_visible("#save"))
            page.click("#save")
            time.sleep(1.0)
            print("C3 after save status:", page.text_content("#status"), "| err:", page.text_content("#err") if page.is_visible("#err") else "-")
            disk = json.loads(REG.read_text('utf-8'))
            ob = next(o for o in disk["obligations"] if o["id"] == first_id)
            print("C3 disk owner:", ob.get("owner"), "| manual:", ob.get("manual"), "| hist last:", ob.get("history", [])[-1] if ob.get("history") else None)
            check(ob.get("owner") == "Тестовый Владелец", "C3 правка сохранена на диск")
            page.reload()
            page.wait_for_selector("tr.ob")
            time.sleep(0.5)
            rr = rows(page)
            print("C3 after reload owner of first:", [r['owner'] for r in rr][:1], "| rows:", len(rr),
                  "| правка chip:", page.evaluate("() => document.querySelectorAll('.chip.man').length"))
            # C4 ошибочные пути
            a = run(page, "01", "nonsense_engine_xyz run --input {input} --registry {registry}", False, wait_s=15)
            print("C4 nonsense:", "| err:", repr(a["err"]), "| status:", a["status"], "| log tail:", repr(a["log"][-200:]), "| rows:", len(a["rows"]))
            check(bool(a["err"]) or "ошиб" in (a["status"] or "").lower(), "C4 несуществующий движок даёт видимую ошибку")
            a = run(page, "01", "python {bogus}", False, wait_s=15)
            print("C4 bad placeholder:", "| err:", repr(a["err"])[:200])
            check(bool(a["err"]), "C4 неизвестный плейсхолдер даёт ошибку")
            # C5 элементы управления
            page.click("th[data-k='what']")
            time.sleep(0.2)
            print("C5 sort click ok, first what:", rows(page)[0]['what'][:40])
            page.click("tr.ob .src >> nth=0")
            time.sleep(0.8)
            dlg_open = page.evaluate("() => document.querySelector('#dlg').open")
            print("C5 src dialog:", dlg_open, page.text_content("#dlg-t")[:160])
            check(bool(dlg_open), "C5 диалог источника открывается")
            page.evaluate("() => dlg.close()")
            print("C5 runex visible:", page.is_visible("#runex"))
            b.close()
        hard = [e for e in errs if e.startswith("pageerror")]
        print("C5 console/page errors:", len(errs))
        for e in errs:
            print("   ", e[:200])
        check(not hard, "нет JS-исключений на странице")
    finally:
        srv.kill()
        shutil.rmtree(tmp, ignore_errors=True)
    print(("ПРОВАЛЕНО: " + "; ".join(fails)) if fails else "ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
