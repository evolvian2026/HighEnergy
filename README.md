# HighEnergy: DSA & Competitive Programming Placement Course

A 120-hour course (40 lectures × 3 hours) in Data Structures, Algorithms and competitive programming. It is built for students aiming at placements paying ₹10+ LPA, with separate C++ and Java tracks.

## What's in this repo

| Path | What it is |
|---|---|
| `course/data.py` | Single source of truth: the 40 lectures, 284 problems (CSES, LeetCode, Codeforces, AtCoder), language notes, project milestones |
| `course/build_excel.py` | Builds one interactive Excel workbook per language track (Home dashboard, Lecture Explorer, Problem Bank, Contests, Projects, Placement module, Toolkit, Student Tracker) |
| `course/export_portal_data.py` | Rebuilds both workbooks and `portal/data.json` |
| `portal/template.html` | The web portal (single page; data is injected at build time) |
| `portal/build_portal.py` | Writes `dist/index.html` from the template + data |
| `dist/` | Built outputs: `index.html` and the two `.xlsx` workbooks |
| `docs/` | Role guide and data model |
| `tests/` | Browser smoke tests for the portal |

## Rebuild everything

```bash
pip install openpyxl playwright
python course/export_portal_data.py   # Excel workbooks + portal/data.json
python portal/build_portal.py         # dist/index.html
python tests/test_portal.py           # smoke tests (needs Chrome/Chromium)
```

To change the course, edit `course/data.py` (lectures, problems) and rebuild. Problem IDs (`P001`…) are numbered in file order across the whole course. **Only append new problems after the last `add(40, …)` block, and never delete or reorder existing ones.** Otherwise every later ID shifts and students' saved progress points at the wrong problems. To retire a problem, change its type rather than deleting it.

## Where the portal runs

The portal is published as a Claude artifact. When it is opened outside Claude (as a plain file or on any static host), it still works, saving progress in the browser only.
