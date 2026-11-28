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

    # ---- Learn (handbooks) ----
    pg, errs = page(b)
    check(pg.locator("#v-learn.on").count() == 1, "learn: Learn is the default view")
    check(pg.locator("#lrail .lmod").count() == 12, "learn: 12 modules in the rail")
    pg.click('#lrail [data-lmod="M7"]'); pg.wait_for_timeout(200)
    check("Graphs" in pg.inner_text("#lhead"), "learn: picking a module shows its handbook")
    check(pg.locator("#ltabs [role=tab]").count() == 6, "learn: one tab per lecture (M7 has 6)")
    pg.click('#ltabs [data-ltab="L24"]'); pg.wait_for_timeout(200)
    check(pg.locator('#ltabs [aria-selected=true]').inner_text().startswith("L24"), "learn: lecture tab switches")
    first = pg.locator("#lpanel .lblk").first
    first.locator("> summary").click(); pg.wait_for_timeout(150)
    check(first.evaluate("e => e.open"), "learn: section accordion opens")
    blk = pg.locator('#lpanel .lblk:has(.codeswap)').first
    if not blk.evaluate("e => e.open"): blk.locator("> summary").click()
    vis = lambda: blk.locator(".codeswap pre:visible").get_attribute("data-lang")
    check(vis() == "cpp", "learn: C++ code shown by default")
    blk.locator('[data-clang="java"]').first.click(); pg.wait_for_timeout(150)
    check(vis() == "java" and pg.get_attribute("#l-java", "aria-pressed") == "true", "learn: code toggle switches to Java everywhere")
    first.locator("[data-read]").click(); pg.wait_for_timeout(200)
    saved = json.loads(pg.evaluate("localStorage.getItem('dsa-course-v1')"))
    check(len(saved["learn"]["read"]) == 1, "learn: mark-as-read is saved")
    check("1/" in pg.locator('#ltabs [aria-selected=true]').inner_text(), "learn: tab shows sections read")
    pg.click('#ltabs [data-ltab="L23"]'); pg.wait_for_timeout(150)
    q = pg.locator("#lpanel .lblk.k-quiz").first; q.locator("> summary").click()
    q.locator(".qans").first.fill("When all edges cost the same"); q.locator('[data-v="got"]').first.click(); pg.wait_for_timeout(500)
    saved = json.loads(pg.evaluate("localStorage.getItem('dsa-course-v1')"))
    check(list(saved["learn"]["quiz"].values()) == ["got"] and saved["learn"]["ans"], "learn: quiz answer and self-rating saved")
    pr = pg.locator("#lpanel .lblk.k-practice").first; pr.locator("> summary").click()
    pr.locator(".chk").first.click(); pg.wait_for_timeout(200)
    saved = json.loads(pg.evaluate("localStorage.getItem('dsa-course-v1')"))
    check(any(v == "Solved" for v in saved["st"].values()), "learn: practice rows tick problems in the shared bank")
    pg.click('#lrail [data-lmod="M0"]'); pg.click('#ltabs [data-ltab="start-here"]'); pg.wait_for_timeout(150)
    pg.locator("#lpanel .lblk").first.locator("> summary").click()
    pg.locator("#lpanel [data-chk]").first.check(); pg.wait_for_timeout(200)
    saved = json.loads(pg.evaluate("localStorage.getItem('dsa-course-v1')"))
    check(len(saved["learn"]["chk"]) == 1, "learn: setup checklist ticks are saved")
    pg.fill("#lsq", "dijkstra"); pg.wait_for_timeout(200)
    check(pg.locator("#lsres .lsr").count() > 0, "learn: handbook search finds Dijkstra")
    pg.locator("#lsres .lsr").first.click(); pg.wait_for_timeout(400)
    check(pg.locator("#lpanel .lblk[open]").count() >= 1 and "M7" in pg.locator("#lrail .lmod.on").inner_text(), "learn: search result opens the section")
    pg.goto(URL + "#lectures"); pg.wait_for_timeout(300)
    pg.click('.tile[data-lec="30"]'); pg.wait_for_timeout(300)
    pg.locator('#lec-30 [data-notes]').click(); pg.wait_for_timeout(300)
    check(pg.locator("#v-learn.on").count() == 1 and "L30" in pg.locator('#ltabs [aria-selected=true]').inner_text(), "learn: lecture plan links to its notes")
    check(pg.locator("#lmode:visible").count() == 0, "learn: teacher-guide switch hidden for non-staff")
    pg.screenshot(path=str(SHOTS / "learn-desktop.png"), full_page=False)
    check(not errs, f"learn: no script errors {errs}")
    pg, errs = page(b, width=390)
    pg.locator("#lpanel .lblk").first.locator("> summary").click(); pg.wait_for_timeout(200)
    check(pg.evaluate("document.documentElement.scrollWidth") <= 390, "learn phone: no sideways scroll")
    pg.select_option("#lsel", "M8"); pg.wait_for_timeout(200)
    check("Dynamic" in pg.inner_text("#lhead"), "learn phone: module dropdown works")
    pg.screenshot(path=str(SHOTS / "learn-phone.png"), full_page=False)
    check(not errs, f"learn phone: no script errors {errs}")
    # staff with a teacher guide in the db
    tseed = dict(SEED); TJ = json.loads((ROOT / "portal/teacher.json").read_text())
    tseed["teacher/M0"] = TJ["M0"]
    import gzip, base64
    tseed["teacher/M2"] = {"z": base64.b64encode(gzip.compress(json.dumps(TJ["M2"]).encode())).decode()}
    pg, errs = page(b, mock={"uid": "staff1", "staff": True, "names": NAMES, "seed": tseed})
    pg.wait_for_timeout(800)
    check(pg.locator("#lmode:visible").count() == 1, "learn staff: teacher-guide switch visible")
    pg.click("#lm-t"); pg.wait_for_timeout(500)
    check("Teacher guide" in pg.inner_text("#lhead") and pg.locator("#ltabs [role=tab]").count() >= 2, "learn staff: teacher guide loads from the database")
    pg.click('#ltabs [data-ltab="L1"]'); pg.wait_for_timeout(150)
    pg.locator("#lpanel .lblk.k-quiz > summary").first.click(); pg.locator("#lpanel .qa summary").first.click(); pg.wait_for_timeout(150)
    check(pg.locator("#lpanel .qa[open] div").first.inner_text().strip() != "", "learn staff: model answers can be revealed")
    pg.click('#lrail [data-lmod="M2"]'); pg.wait_for_timeout(600)
    check("Run sheet" in pg.inner_text("#lpanel") or pg.locator("#ltabs [role=tab]").count() >= 2, "learn staff: compressed teacher guide decodes")
    pg.click('#lrail [data-lmod="M1"]'); pg.wait_for_timeout(500)
    check("No teacher guide" in pg.inner_text("#lpanel"), "learn staff: missing guide shows a message")
    check(not errs, f"learn staff: no script errors {errs}")
    html_all = (ROOT / "dist/index.html").read_text() + (ROOT / "dist/site/index.html").read_text()
    check("Run sheet (180 min)" not in html_all and "Recap quiz (answers)" not in html_all, "build: teacher guides are not shipped in either page")
    b.close()

print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
