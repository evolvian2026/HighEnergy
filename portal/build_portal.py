"""Build dist/index.html from portal/template.html + portal/app.js + portal/data.json.

Usage:  python portal/build_portal.py
Regenerate data first with:  python course/export_portal_data.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
tpl = (ROOT / "portal/template.html").read_text(encoding="utf-8")
app = (ROOT / "portal/app.js").read_text(encoding="utf-8")
data = (ROOT / "portal/data.json").read_text(encoding="utf-8").replace("</", "<\\/")
out = ROOT / "dist/index.html"
out.write_text(tpl.replace("__APP__", app).replace("__DATA__", data), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
