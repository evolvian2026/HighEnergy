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

## Shared-progress pilot (Option A)

When the portal is opened from its Claude artifact link by signed-in users, it switches to shared mode:

* **Students** (Contributor access) sync their own progress and profile to the artifact's database and see their scores.
* **Teachers and the TPO** (Editor access) get **Class** and **Readiness** tabs: live class progress, lecture heatmap, hardest problems, score entry, and a ranked readiness list with CSV shortlist export.

See [`docs/roles-and-access.md`](docs/roles-and-access.md) for roles, sharing levels, the data model and limits. The access rules live in [`portal/capabilities.json`](portal/capabilities.json); declare them on the artifact before publishing a version that relies on them.

The tests run the portal against an in-memory stand-in for the database (`tests/mock_claude.js`). They cover offline, student and staff modes.

## Public site (code.<domain>)

`python portal/build_portal.py` also writes `dist/site/`. Upload its contents to the subdomain's web root (`public_html` for the subdomain on Hostinger):

* `index.html` is the public copy of the portal. Anyone can use it, and progress stays in each browser.
* `pilot/index.html` redirects `code.<domain>/pilot` to the shared Claude artifact.

`dist/code-site.zip` holds the same files, ready for a file-manager upload.
