"""Build the portal from portal/template.html + portal/app.js + portal/learn.js + portal/data.json + portal/learn.json.

Run portal/build_learn.py first when the handbooks in course/content change.

Usage:  python portal/build_portal.py

Writes two builds:
  dist/index.html        published as the Claude artifact (shared progress, staff views)
  dist/site/index.html   public copy for code.<domain> (progress stays in each browser)
  dist/site/pilot/index.html  redirect from code.<domain>/pilot to the Claude artifact
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTIFACT_URL = "https://claude.ai/artifact/Fmt9FH4NKNvmDHeoWQwiJT"

tpl = (ROOT / "portal/template.html").read_text(encoding="utf-8")
learn = (ROOT / "portal/learn.json").read_text(encoding="utf-8").replace("</", "<\\/")
learn_js = (ROOT / "portal/learn.js").read_text(encoding="utf-8").replace("__LEARN__", learn)
app = (ROOT / "portal/app.js").read_text(encoding="utf-8").replace("__LEARNJS__", learn_js)
data = (ROOT / "portal/data.json").read_text(encoding="utf-8").replace("</", "<\\/")
page = tpl.replace("__APP__", app).replace("__DATA__", data)

banner = ('<p class="pub">Enrolled in the course? Use the <a href="/pilot/">shared portal</a> '
          'so your teachers can see your progress (needs a claude.ai account).</p>')
outs = {
    ROOT / "dist/index.html": page.replace("<!--PUBLIC_BANNER-->", ""),
    ROOT / "dist/site/index.html": page.replace("<!--PUBLIC_BANNER-->", banner),
    ROOT / "dist/site/pilot/index.html": f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>DSA Placement Course: shared portal</title>
<meta http-equiv="refresh" content="0; url={ARTIFACT_URL}">
<link rel="canonical" href="{ARTIFACT_URL}">
<style>body{{font:17px/1.5 system-ui,sans-serif;margin:0;display:grid;place-items:center;min-height:100vh;background:#0a2540;color:#fff;padding:16px}}a{{color:#8fd3ff}}</style>
</head><body><p>Opening the shared course portal&hellip; If nothing happens, <a href="{ARTIFACT_URL}">open it here</a>.</p>
<script>location.replace({ARTIFACT_URL!r});</script></body></html>
""",
}
for path, html in outs.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} ({len(html.encode()) // 1024} KB)")
