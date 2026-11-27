# Roles, access and data (Option A pilot)

The pilot runs the portal as a Claude artifact. The artifact's built-in database stores progress, and its sign-in identifies who is viewing. No separate server is needed. Option B (a standalone web app with college SSO) is the long-term plan.

## Who can do what

Roles come from the **sharing level each person is given on the artifact's Share menu**. The page reads that level and shows the matching views.

| Role | Share level to give | What they see and can do |
|---|---|---|
| Student | **Contributor** | Course content, own progress synced to the database, own profile (roll no., batch, Codeforces/LeetCode/CodeChef handles), own scores (read-only) |
| Teacher / trainer, mentor | **Editor** | Everything a student sees, plus **Class** (every student's progress, lecture heatmap, hardest problems, student detail drawer, score entry) |
| TPO / placement cell | **Editor** | Same as teacher, plus the **Readiness** view: ranked list, filters (batch, min readiness, min % solved, has Codeforces handle), CSV shortlist export |
| Owner (course admin) | Owner | Everything; publishes new versions; manages sharing |
| Anyone else / Viewer | Viewer or link-only | Course content; progress stays in their own browser only |

Teachers and the TPO both hold Editor access, so the page shows them the same staff tabs. Editors can also publish new versions of the page, so give Editor access only to trusted staff.

## Requirements for everyone

* Each person needs a **claude.ai account** and must be **signed in**. They also need to be in the owner's claude.ai organization, or invited to the artifact by email.
* Students must be given **Contributor** access. Viewers cannot write, so their progress would stay in their own browser.
* Signed-out visitors, or anyone without write access, still get the full course. Their progress is saved in their own browser.

## Data stored

| Path | Written by | Readable by | Contents |
|---|---|---|---|
| `progress/<userId>` | that student | that student + Editors/Owner | `st` (problem ID → status), `lang`, `prof` {roll, batch, cf, lc, cc}, `solved`, `updatedAt` |
| `scores/<userId>` | Editors/Owner | that student + Editors/Owner | `contests` {c1…c6}, `projects`, `mock` (all 0-100), `updatedAt`, `by` |

The full rules are in `portal/capabilities.json`. Names come from each person's claude.ai profile and are never stored in the database.

Readiness uses the same formula as the Excel Student Tracker:
`contest avg × 30% + problem score × 20% + projects × 30% + mock × 20%`, where problem score = min(100, solved ÷ 284 × 100 ÷ 0.7).

## Usage examples

* **Student:** signs in and opens the link. Their earlier in-browser progress is uploaded automatically. They fill in My progress → My profile, then solve problems; each tick syncs.
* **Teacher:** opens Class and filters by batch. Pale tiles in the lecture heatmap show where the class is behind. They clicks a student → Details, and enters contest and project scores after each assessment.
* **TPO:** opens Readiness, sets the batch, sets "Min readiness 60" and "Has Codeforces handle", and exports the CSV shortlist for a company drive.

## Known limits of the pilot

* Solves are self-reported (no automatic verification yet; Codeforces' public API is the first candidate in Option B).
* Up to 25,000 database documents per artifact (two per student). That is plenty for a pilot of a few hundred students.
* There is no separate teacher vs TPO permission; both are Editors.
* Treat student data under your institution's data policy and India's DPDP Act, 2023. Tell students what is shared and with whom.
