"""Browser smoke tests for dist/index.html.

Runs the portal in headless Chrome in three modes:
  * offline  (no Claude runtime: progress in localStorage only)
  * student  (mocked db/user: own progress syncs, no staff tabs)
  * staff    (mocked db/user as Editor: Class + Readiness views, score entry, CSV export)

Usage:  python tests/test_portal.py   [--chrome /path/to/chrome]
"""
import json, pathlib, shutil, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "dist/index.html").as_uri()
MOCK = (ROOT / "tests/mock_claude.js").read_text()
CHROME = sys.argv[sys.argv.index("--chrome") + 1] if "--chrome" in sys.argv else (shutil.which("google-chrome") or shutil.which("chromium"))
SHOTS = ROOT / "test-results"; SHOTS.mkdir(exist_ok=True)

fails = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)

def page(b, mock=None, local=None, width=1280):
    ctx = b.new_context(viewport={"width": width, "height": 900})
    errs = []
    if local is not None:
        ctx.add_init_script(f"localStorage.setItem('dsa-course-v1', {json.dumps(json.dumps(local))});")
    if mock is not None:
        ctx.add_init_script(f"window.__MOCK = {json.dumps(mock)};\n{MOCK}")
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("dialog", lambda d: (errs.append("dialog: " + d.message), d.dismiss()))
    pg.goto(URL); pg.wait_for_timeout(600)
    return pg, errs

SEED = {
    "progress/stuA": {"st": {"P001": "Solved", "P002": "Solved", "P003": "Upsolved", "P010": "Revisit"}, "lang": "cpp",
                      "prof": {"roll": "21CS001", "batch": "CSE-A 2027", "cf": "tourist"}, "updatedAt": "2026-11-26T10:00:00Z"},
    "progress/stuB": {"st": {"P001": "Solved"}, "lang": "java",
                      "prof": {"roll": "=HYPERLINK(\"http://x\")", "batch": "<img src=x onerror=alert(1)>"}, "updatedAt": "2026-10-01T10:00:00Z"},
    "progress/stuC": {"st": {f"P{i:03d}": "Solved" for i in range(1, 201)}, "lang": "cpp",
                      "prof": {"roll": "21CS003", "batch": "CSE-A 2027", "cf": "petr"}, "updatedAt": "2026-11-27T08:00:00Z"},
    "scores/stuC": {"contests": {"c1": 90, "c2": 80}, "projects": 85, "mock": 70},
}
NAMES = {"stuA": "Aarav Shah", "stuB": "Bhavya Rao", "stuC": "Chitra Iyer", "staff1": "Prof. Menon"}

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME) if CHROME else p.chromium.launch()

    # ---- offline ----
    pg, errs = page(b)
    check("browser" in pg.inner_text("#synct"), "offline: sync chip says saved in this browser")
    pg.click('.tile[data-lec="1"]'); pg.wait_for_timeout(200)
    pg.locator("#lec-1 .chk").first.click(); pg.wait_for_timeout(200)
    saved = json.loads(pg.evaluate("localStorage.getItem('dsa-course-v1')"))
    check(saved["st"].get("P001") == "Solved", "offline: solving saves to localStorage")
    check(pg.locator(".staffonly:visible").count() == 0, "offline: staff tabs hidden")
    check(not errs, f"offline: no script errors {errs}")

    # ---- student ----
    pg, errs = page(b, mock={"uid": "stuD", "staff": False, "names": NAMES, "seed": SEED},
                    local={"lang": "java", "st": {"P005": "Solved"}, "prof": {}})
    pg.wait_for_timeout(1200)
    store = pg.evaluate("window.__store")
    check(store.get("progress/stuD", {}).get("st", {}).get("P005") == "Solved", "student: local progress uploaded on first sign-in")
    check("Synced" in pg.inner_text("#synct"), "student: sync chip shows synced")
    pg.click('.tile[data-lec="1"]'); pg.wait_for_timeout(200)
    pg.locator("#lec-1 .chk").first.click(); pg.wait_for_timeout(1200)
    check(pg.evaluate("window.__store['progress/stuD'].st.P001") == "Solved", "student: new solve synced to db")
    pg.goto(URL + "#progress"); pg.wait_for_timeout(800)
    pg.fill("#f-roll", "21CS099"); pg.fill("#f-batch", "CSE-B 2027"); pg.fill("#f-cf", "my_handle!!"); pg.click("#pform button[type=submit]"); pg.wait_for_timeout(1200)
    prof = pg.evaluate("window.__store['progress/stuD'].prof")
    check(prof["roll"] == "21CS099" and prof["cf"] == "my_handle", "student: profile saved and handle sanitised")
    check(pg.locator(".staffonly:visible").count() == 0, "student: staff tabs hidden")
    pg.goto(URL + "#class"); pg.wait_for_timeout(800)
    check(pg.locator("#v-class.on").count() == 0, "student: #class route falls back to lectures")
    check(not errs, f"student: no script errors {errs}")

    # ---- staff ----
    pg, errs = page(b, mock={"uid": "staff1", "staff": True, "names": NAMES, "seed": SEED})
    pg.wait_for_timeout(1000)
    check(pg.locator(".staffonly:visible").count() == 2, "staff: Class and Readiness tabs visible")
    check("progress/staff1" not in pg.evaluate("window.__store"), "staff: browsing alone does not create a student record")
    pg.goto(URL + "#class"); pg.wait_for_timeout(1000)
    rows = pg.locator("#ctbody tr").count()
    check(rows == 3, f"staff: class table lists 3 students (got {rows})")
    check(pg.locator("#ctbody img").count() == 0, "staff: student-entered HTML is escaped")
    check("Chitra Iyer" in pg.inner_text("#ctbody"), "staff: names resolved from profiles")
    pg.screenshot(path=str(SHOTS / "staff-class.png"), full_page=True)
    pg.locator('[data-stu="stuA"]').click(); pg.wait_for_timeout(300)
    check(pg.locator("#drawer:visible").count() == 1, "staff: student drawer opens")
    pg.fill('#scform input[name=c1]', "75"); pg.fill("#scform input[name=projects]", "95"); pg.click("#scform button[type=submit]"); pg.wait_for_timeout(600)
    sc = pg.evaluate("window.__store['scores/stuA']")
    check(sc["contests"]["c1"] == 75 and sc["projects"] == 95, "staff: scores saved")
    pg.screenshot(path=str(SHOTS / "staff-drawer.png"))
    pg.keyboard.press("Escape")
    pg.goto(URL + "#readiness"); pg.wait_for_timeout(800)
    first = pg.locator("#rbody tr").first.inner_text()
    check("Chitra" in first, "staff: readiness ranks the strongest student first")
    pg.fill("#rmin", "60"); pg.wait_for_timeout(200)
    check(pg.locator("#rbody tr").count() == 1, "staff: min-readiness filter works")
    pg.fill("#rmin", "0"); pg.click("#rexp"); pg.wait_for_timeout(400)
    dl = pg.evaluate("window.__download")
    check(dl and dl["filename"].endswith(".csv") and "'=HYPERLINK" in dl["data"], "staff: CSV exported with formula injection neutralised")
    pg.screenshot(path=str(SHOTS / "staff-readiness.png"), full_page=True)
    check(not errs, f"staff: no script errors {errs}")

    # ---- staff on a phone ----
    pg, errs = page(b, mock={"uid": "staff1", "staff": True, "names": NAMES, "seed": SEED}, width=390)
    pg.goto(URL + "#class"); pg.wait_for_timeout(1000)
    check(pg.evaluate("document.documentElement.scrollWidth") <= 390, "phone: class view has no sideways scroll")
    pg.screenshot(path=str(SHOTS / "staff-phone.png"), full_page=True)
    b.close()

print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
