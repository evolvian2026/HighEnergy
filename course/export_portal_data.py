"""Rebuild both Excel workbooks and the portal's data.json from course/data.py.

Usage:  python course/export_portal_data.py
Writes: dist/DSA_CP_Course_Plan_CPP.xlsx, dist/DSA_CP_Course_Plan_Java.xlsx, portal/data.json
"""
import json, os, pathlib, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
tmp = pathlib.Path(tempfile.mkdtemp())
for lang, tag in (("C++", "CPP"), ("Java", "Java")):
    env = dict(os.environ, EXPORT_JSON=str(tmp / f"{tag}.json"))
    subprocess.run([sys.executable, str(ROOT / "course/build_excel.py"), lang,
                    str(ROOT / f"dist/DSA_CP_Course_Plan_{tag}.xlsx")], check=True, env=env, cwd=ROOT / "course")

c = json.loads((tmp / "CPP.json").read_text()); j = json.loads((tmp / "Java.json").read_text())
d = dict(
    lectures=[{k: v for k, v in l.items() if k != "note"} for l in c["lectures"]],
    notes={"cpp": [l["note"] for l in c["lectures"]], "java": [l["note"] for l in j["lectures"]]},
    problems=[{k: p[k] for k in ("id", "lec", "plat", "name", "typ", "diff", "idea", "url")} for p in c["problems"]],
    projects=[{k: v for k, v in p.items() if k != "stack"} for p in c["projects"]],
    stacks={"cpp": [p["stack"] for p in c["projects"]], "java": [p["stack"] for p in j["projects"]]},
    kit={"cpp": c["kit"], "java": j["kit"]}, contests=c["contests"], live=c["live"],
    placement=c["placement"], platforms=c["platforms"], weights=c["weights"],
)
(ROOT / "portal/data.json").write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("wrote portal/data.json")
print("Note: Excel formulas have no cached values until opened in Excel or recalculated with LibreOffice.")
