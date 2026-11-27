import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule, CellIsRule, DataBarRule, ColorScaleRule
import json, os
from data import *

LANGNAME = sys.argv[1]  # "C++" or "Java"
OUT = sys.argv[2]

F = "Arial"
HDR_FILL = PatternFill("solid", start_color="1F3864")
SUB_FILL = PatternFill("solid", start_color="D9E2F3")
INPUT_FILL = PatternFill("solid", start_color="FFFF00")
ALT = PatternFill("solid", start_color="F2F2F2")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
MOD_FILLS = {}
palette = ["DEEAF6","E2EFDA","FFF2CC","FCE4D6","EDE7F6","DDEBF7","E2F0D9","FBE5D6","F4E1F0","E7E6E6","D9F2F2","FFF0F0"]

wb = Workbook()

def header(ws, row, cols, widths=None):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font = Font(name=F, bold=True, color="FFFFFF")
        cell.fill = HDR_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = BORDER
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 32

def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(name=F, bold=True, size=14, color="1F3864")
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(name=F, italic=True, size=9, color="595959")

def body(cell, bold=False, color="000000"):
    cell.font = Font(name=F, size=10, bold=bold, color=color)
    cell.alignment = WRAP
    cell.border = BORDER

# ---------------- Problem IDs ----------------
probs = []
for i, (lec, plat, pid, name, typ, diff, idea) in enumerate(P, 1):
    probs.append(dict(id=f"P{i:03d}", lec=lec, plat=plat, pid=pid, name=name, typ=typ, diff=diff, idea=idea, url=url(plat, pid)))
# sanity: no duplicate urls
urls = [p["url"] for p in probs]
assert len(urls) == len(set(urls)), [u for u in urls if urls.count(u) > 1]
lec_topic = {l[0]: l[3] for l in L}
lec_module = {l[0]: l[1] for l in L}
mods = []
for l in L:
    if l[1] not in mods: mods.append(l[1])
for i, m in enumerate(mods):
    MOD_FILLS[m] = PatternFill("solid", start_color=palette[i % len(palette)])

NLEC = len(L)
NPROB = len(probs)

# ================= Sheet 1: Course Overview =================
ws = wb.active
ws.title = "Course Overview"
title(ws, f"DSA & Competitive Programming for ₹10+ LPA Placements: {LANGNAME} Track",
      "120 contact hours · 40 lectures × 3 hrs · Prerequisite: basic programming, arrays, recursion, sorting")
ws.column_dimensions["A"].width = 34; ws.column_dimensions["B"].width = 22; ws.column_dimensions["C"].width = 70

r = 4
ws.cell(row=r, column=1, value="Course parameters (edit yellow cells)").font = Font(name=F, bold=True, size=11, color="1F3864")
r += 1
params = [
 ("Hours per lecture", 3, "Given in course brief"),
 ("Lectures per week", 2, "Assumption: 2 lectures/week, giving a 20-week course. Change this and the Week column in Lecture Plan updates."),
 ("Course start date", None, "Optional: enter a date to plan the calendar"),
]
for lbl, val, note in params:
    body(ws.cell(row=r, column=1, value=lbl), bold=True)
    c = ws.cell(row=r, column=2, value=val); body(c, color="0000FF"); c.fill = INPUT_FILL
    body(ws.cell(row=r, column=3, value=note))
    r += 1
ws["B7"].number_format = "dd-mmm-yyyy"
# derived
r += 1
ws.cell(row=r, column=1, value="Course at a glance (calculated)").font = Font(name=F, bold=True, size=11, color="1F3864"); r += 1
derived = [
 ("Total lectures", "=COUNTA('Lecture Plan'!A5:A200)"),
 ("Total contact hours", "=SUM('Lecture Plan'!E5:E44)"),
 ("Course duration (weeks)", "=ROUNDUP(B10/B6,0)"),
 ("Total curated problems", "=COUNTA('Problem Bank'!A5:A1000)"),
 ("  In-class problems", "=COUNTIF('Problem Bank'!G5:G1000,\"In-class\")"),
 ("  Take-home problems", "=COUNTIF('Problem Bank'!G5:G1000,\"Take-home\")"),
 ("  Contest problems", "=COUNTIF('Problem Bank'!G5:G1000,\"Contest\")"),
 ("  OA / interview practice", "=COUNTIF('Problem Bank'!G5:G1000,\"OA / Interview practice\")"),
 ("Problems on Codeforces", "=COUNTIF('Problem Bank'!E5:E1000,\"Codeforces\")"),
 ("Problems on CSES", "=COUNTIF('Problem Bank'!E5:E1000,\"CSES\")"),
 ("Problems on AtCoder", "=COUNTIF('Problem Bank'!E5:E1000,\"AtCoder\")"),
 ("Problems on LeetCode", "=COUNTIF('Problem Bank'!E5:E1000,\"LeetCode\")"),
 ("Hands-on projects", "=COUNTA(Projects!A5:A10)"),
]
for lbl, f in derived:
    body(ws.cell(row=r, column=1, value=lbl), bold=not lbl.startswith("  "))
    c = ws.cell(row=r, column=2, value=f); body(c); c.number_format = "0"
    r += 1

r += 1
ws.cell(row=r, column=1, value="Assessment weights").font = Font(name=F, bold=True, size=11, color="1F3864"); r += 1
header(ws, r, ["Component", "Weight", "Details"]); r += 1
wstart = r
weights = [("Contests (5 internal + mock OA)", 0.30, "Best 5 of 6 counted; upsolving required within 48 hrs"),
           ("Problem completion", 0.20, "% of in-class + take-home problems solved (see Student Tracker)"),
           ("Projects", 0.30, "Project 0 & 1: 10%, two electives: 10%, capstone: 10%"),
           ("Mock OA & interviews", 0.20, "OA score (L37) + 2 mock interviews (L39), rubric in Placement Module")]
for comp, w, d in weights:
    body(ws.cell(row=r, column=1, value=comp))
    c = ws.cell(row=r, column=2, value=w); body(c, color="0000FF"); c.number_format = "0%"; c.fill = INPUT_FILL
    body(ws.cell(row=r, column=3, value=d)); r += 1
body(ws.cell(row=r, column=1, value="Total (must be 100%)"), bold=True)
c = ws.cell(row=r, column=2, value=f"=SUM(B{wstart}:B{r-1})"); body(c, bold=True); c.number_format = "0%"
WEIGHT_ROWS = (wstart, r - 1)
r += 2

ws.cell(row=r, column=1, value="Practice platforms").font = Font(name=F, bold=True, size=11, color="1F3864"); r += 1
header(ws, r, ["Platform", "Role in course", "Link"]); r += 1
plats = [("Codeforces", "Main CP source; Div. 3/Div. 4 & Educational rounds for live practice", "https://codeforces.com"),
         ("CSES Problem Set", "Topic-wise drills with stable links (core of the take-home sets)", "https://cses.fi/problemset/"),
         ("AtCoder (Educational DP Contest)", "The standard DP ladder, plus weekly Beginner Contests (ABC)", "https://atcoder.jp/contests/dp"),
         ("LeetCode", "Interview/OA-style problems and weekly/biweekly contests", "https://leetcode.com/problemset/"),
         ("CodeChef", "Weekly Starters contests (live rated practice); practice paths by difficulty", "https://www.codechef.com/contests"),
         ("cp-algorithms", "Reference theory for every algorithm in the course", "https://cp-algorithms.com"),
         ("USACO Guide", "Structured explanations and CSES solution walkthroughs", "https://usaco.guide"),
         ("CP Handbook (Antti Laaksonen)", "Free textbook aligned with CSES", "https://cses.fi/book/book.pdf")]
for a, b, u in plats:
    body(ws.cell(row=r, column=1, value=a), bold=True); body(ws.cell(row=r, column=2, value=b))
    c = ws.cell(row=r, column=3, value=u); body(c, color="0563C1"); c.hyperlink = u; c.font = Font(name=F, size=10, color="0563C1", underline="single")
    r += 1
r += 1
ws.cell(row=r, column=1, value="Course rules").font = Font(name=F, bold=True, size=11, color="1F3864"); r += 1
for rule in ["Upsolving: every contest problem you didn't solve must be solved within 48 hours, using the editorial if needed, and logged in the tracker.",
             "Take-home sets are due before the next lecture; solve at least 70% of each week's take-home problems.",
             "Students take at least one live rated contest per week (Codeforces, CodeChef Starters, LeetCode Weekly, or AtCoder ABC).",
             f"All code in {LANGNAME}, using the course template (Language Toolkit sheet). Keep a personal GitHub repo of solutions.",
             "Rating milestones: Codeforces 1200+ by mid-term, 1400+ (Specialist) by course end; LeetCode contest rating 1700+."]:
    c = ws.cell(row=r, column=1, value="• " + rule); c.font = Font(name=F, size=10); c.alignment = WRAP
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3); ws.row_dimensions[r].height = 28
    r += 1
ws.column_dimensions["B"].width = 50

# ================= Sheet 2: Lecture Plan =================
lp = wb.create_sheet("Lecture Plan")
title(lp, f"Lecture-wise plan: 40 lectures × 3 hours ({LANGNAME} track)",
      "Week is calculated from 'Lectures per week' on Course Overview. Problem IDs refer to the Problem Bank sheet.")
cols = ["Lecture #", "Week", "Module", "Topic", "Hours", "Subtopics covered", "Learning outcomes",
        "Session format (3 hrs)", f"{LANGNAME} focus", "In-class problems", "Take-home / contest problems",
        "# In-class", "# Take-home / other", "Project milestone"]
header(lp, 4, cols, [9, 7, 22, 32, 7, 50, 38, 40, 40, 26, 30, 10, 12, 26])
for i, (no, mod, topic, sub, out, kind) in enumerate(L):
    r = 5 + i
    ic = [p["id"] for p in probs if p["lec"] == no and p["typ"] == IC]
    oth = [p["id"] for p in probs if p["lec"] == no and p["typ"] != IC]
    vals = [no, f"=ROUNDUP(A{r}/'Course Overview'!$B$6,0)", mod, topic, "='Course Overview'!$B$5", sub, out, FORMAT[kind],
            LANG[LANGNAME][no], ", ".join(ic) or "-", ", ".join(oth) or "-",
            f"=COUNTIFS('Problem Bank'!$B$5:$B$1000,A{r},'Problem Bank'!$G$5:$G$1000,\"In-class\")",
            f"=COUNTIFS('Problem Bank'!$B$5:$B$1000,A{r})-L{r}",
            PROJECT_MILESTONE.get(no, "")]
    for j, v in enumerate(vals, 1):
        c = lp.cell(row=r, column=j, value=v); body(c, bold=(j == 4))
    for j in (1, 2, 3):
        lp.cell(row=r, column=j).fill = MOD_FILLS[mod]
    lp.row_dimensions[r].height = 75
end = 5 + NLEC - 1
r = end + 1
body(lp.cell(row=r, column=4, value="TOTAL"), bold=True)
c = lp.cell(row=r, column=5, value=f"=SUM(E5:E{end})"); body(c, bold=True)
c = lp.cell(row=r, column=12, value=f"=SUM(L5:L{end})"); body(c, bold=True)
c = lp.cell(row=r, column=13, value=f"=SUM(M5:M{end})"); body(c, bold=True)
lp.freeze_panes = "E5"
lp.auto_filter.ref = f"A4:N{end}"

# ================= Sheet 3: Problem Bank =================
pb = wb.create_sheet("Problem Bank")
title(pb, f"Curated problem bank: {NPROB} problems with direct links",
      "Status column (yellow) is for a student's personal copy: pick from the dropdown. Est. time = suggested solving budget.")
cols = ["Problem ID", "Lecture #", "Topic (lecture)", "Problem name", "Platform", "Link", "Type", "Difficulty",
        "Key idea / hint", "Est. time (min)", "Status", "Date solved", "Notes"]
header(pb, 4, cols, [10, 9, 32, 40, 12, 58, 14, 10, 42, 10, 13, 12, 25])
for i, p in enumerate(probs):
    r = 5 + i
    vals = [p["id"], p["lec"], lec_topic[p["lec"]], p["name"], p["plat"], p["url"], p["typ"], p["diff"], p["idea"], EST[p["diff"]], "Not started", None, None]
    for j, v in enumerate(vals, 1):
        c = pb.cell(row=r, column=j, value=v); body(c)
    lc = pb.cell(row=r, column=6); lc.hyperlink = p["url"]; lc.font = Font(name=F, size=10, color="0563C1", underline="single")
    pb.cell(row=r, column=11).fill = INPUT_FILL
    pb.cell(row=r, column=12).number_format = "dd-mmm-yyyy"
    dcol = {"Easy": "E2EFDA", "Medium": "FFF2CC", "Hard": "FCE4D6"}[p["diff"]]
    pb.cell(row=r, column=8).fill = PatternFill("solid", start_color=dcol)
pend = 5 + NPROB - 1
dv = DataValidation(type="list", formula1='"Not started,Attempted,Solved,Upsolved,Revisit"', allow_blank=True)
pb.add_data_validation(dv); dv.add(f"K5:K{pend}")
pb.freeze_panes = "E5"
pb.auto_filter.ref = f"A4:O{pend}"
# helper columns: Module + Explorer key
for colno, h in ((14, "Module (auto)"), (15, "Explorer key (auto)")):
    c = pb.cell(row=4, column=colno, value=h); c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = PatternFill("solid", start_color="7F7F7F")
    c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center"); c.border = BORDER
pb.column_dimensions["N"].width = 26; pb.column_dimensions["O"].width = 10
for r in range(5, pend + 1):
    c = pb.cell(row=r, column=14, value=f"=INDEX('Lecture Plan'!$C$5:$C$44,MATCH(B{r},'Lecture Plan'!$A$5:$A$44,0))"); body(c, color="7F7F7F")
    c = pb.cell(row=r, column=15, value=f"=IF(B{r}='Lecture Explorer'!$C$5,COUNTIF($B$5:B{r},'Lecture Explorer'!$C$5),\"\")"); body(c, color="7F7F7F")
# status colouring
STATUS_COL = {"Solved": "C6EFCE", "Upsolved": "BDD7EE", "Attempted": "FFEB9C", "Revisit": "F8CBAD"}
for s_, col in STATUS_COL.items():
    pb.conditional_formatting.add(f"A5:J{pend}", FormulaRule(formula=[f'$K5="{s_}"'], fill=PatternFill("solid", start_color=col, end_color=col)))
    pb.conditional_formatting.add(f"K5:K{pend}", CellIsRule(operator="equal", formula=[f'"{s_}"'], fill=PatternFill("solid", start_color=col, end_color=col), font=Font(name=F, bold=True)))
# summary at right
pb["Q4"] = "Summary"; pb["Q4"].font = Font(name=F, bold=True, color="FFFFFF"); pb["Q4"].fill = HDR_FILL
pb["R4"] = "Count"; pb["R4"].font = Font(name=F, bold=True, color="FFFFFF"); pb["R4"].fill = HDR_FILL
pb.column_dimensions["Q"].width = 26; pb.column_dimensions["R"].width = 10
summ = [("Total problems", f"=COUNTA(A5:A{pend})"), ("Easy", f'=COUNTIF(H5:H{pend},"Easy")'),
        ("Medium", f'=COUNTIF(H5:H{pend},"Medium")'), ("Hard", f'=COUNTIF(H5:H{pend},"Hard")'),
        ("Solved + Upsolved", f'=COUNTIF(K5:K{pend},"Solved")+COUNTIF(K5:K{pend},"Upsolved")'),
        ("% complete", f"=IFERROR(R9/R5,0)"),
        ("Total est. hours", f"=SUM(J5:J{pend})/60")]
for k, (a, f) in enumerate(summ):
    body(pb.cell(row=5 + k, column=17, value=a), bold=True)
    c = pb.cell(row=5 + k, column=18, value=f); body(c)
    c.number_format = "0%" if a == "% complete" else ("0.0" if "hours" in a else "0")
legend_r = 5 + len(summ) + 1
body(pb.cell(row=legend_r, column=17, value="Status colours"), bold=True)
for k, (s_, col) in enumerate(STATUS_COL.items()):
    c = pb.cell(row=legend_r + 1 + k, column=17, value=s_); body(c); c.fill = PatternFill("solid", start_color=col)

# ================= Sheet 4: Contests & Assessments =================
ca = wb.create_sheet("Contests & Assessments")
title(ca, "Contests, mock OAs & weekly live practice")
cols = ["#", "Assessment", "Held in lecture", "Format", "Syllabus", "Problem source", "Duration", "Weightage note", "Upsolve deadline"]
header(ca, 4, cols, [5, 26, 10, 34, 34, 46, 10, 30, 18])
contests = [
 ("Contest 1", 11, "Individual, ICPC-style scoring, 4 problems", "Modules 0-3", "Problem Bank 'Contest' rows for L11 (or a Codeforces mashup of the same problems)", "2 hrs", "Counts toward Contests (30%)"),
 ("Mid-term contest", 21, "Individual, 4 problems + 1 bonus", "Modules 0-6", "Problem Bank 'Contest' rows for L21 + 1 instructor-picked tree problem", "2 hrs", "Counts toward Contests (30%)"),
 ("Contest 2 (Graphs)", 27, "Individual, 4 problems", "Module 7", "Codeforces mashup of graph problems not yet assigned", "1.5 hrs", "Counts toward Contests (30%)"),
 ("Contest 3 (DP)", 33, "Individual, 4 problems", "Module 8", "AtCoder DP Contest letters not assigned in class (e.g. M, Q, R, T, U, W, X, Y, Z)", "1.5 hrs", "Counts toward Contests (30%)"),
 ("Mock OA", 37, "3 problems, partial scoring, hidden tests", "Full course", "Problem Bank 'OA / Interview practice' rows for L37, on HackerRank/HackerEarth-style platform", "1.5 hrs", "Counts toward Mock OA & interviews (20%)"),
 ("Final contest", 40, "Individual, 5 problems", "Full course", "Problem Bank 'Contest' rows for L40", "2 hrs", "Counts toward Contests (30%)"),
]
for i, (n, lec, fmt, syl, src, dur, w) in enumerate(contests):
    r = 5 + i
    for j, v in enumerate([i + 1, n, lec, fmt, syl, src, dur, w, "48 hrs after contest"], 1):
        body(ca.cell(row=r, column=j, value=v), bold=(j == 2))
    ca.row_dimensions[r].height = 42
r = 5 + len(contests) + 1
ca.cell(row=r, column=1, value="Weekly live rated contests (mandatory: at least one per week)").font = Font(name=F, bold=True, size=11, color="1F3864"); r += 1
header(ca, r, ["#", "Contest", "Platform", "Why", "Link"]); r += 1
live = [("Codeforces Div. 3 / Div. 4 / Educational rounds", "Codeforces", "Best rating ladder for 800-1600 problems", "https://codeforces.com/contests"),
        ("CodeChef Starters", "CodeChef", "Weekly rated contest, good Indian peer group", "https://www.codechef.com/contests"),
        ("LeetCode Weekly & Biweekly", "LeetCode", "Closest to OA/interview difficulty", "https://leetcode.com/contest/"),
        ("AtCoder Beginner Contest (ABC)", "AtCoder", "Clean problems, strong maths and DP", "https://atcoder.jp/contests/")]
for i, (a, b, c_, u) in enumerate(live):
    for j, v in enumerate([i + 1, a, b, c_, u], 1):
        cell = ca.cell(row=r, column=j, value=v); body(cell)
    ca.cell(row=r, column=5).hyperlink = u; ca.cell(row=r, column=5).font = Font(name=F, size=10, color="0563C1", underline="single")
    r += 1
r += 1
ca.cell(row=r, column=1, value="Rating milestones").font = Font(name=F, bold=True, size=11, color="1F3864"); r += 1
header(ca, r, ["#", "Checkpoint", "Lecture", "Codeforces target", "LeetCode target"]); r += 1
for i, row in enumerate([("Start of course", 1, "Account + 1 contest", "Account + 1 contest"),
                         ("Mid-term", 21, "1200+ (Pupil)", "150 problems solved; contest rating 1500+"),
                         ("End of DP module", 33, "1300+", "Contest rating 1600+"),
                         ("Course end", 40, "1400+ (Specialist)", "300 problems solved; contest rating 1700+")]):
    for j, v in enumerate((i + 1,) + row, 1):
        body(ca.cell(row=r, column=j, value=v))
    r += 1

# ================= Sheet 5: Projects =================
pj = wb.create_sheet("Projects")
title(pj, f"Hands-on projects ({LANGNAME} track)",
      "Project 0 & 1 are mandatory (individual). Pick TWO of the electives (2-4). Capstone (5) in teams of 2-3, demo in L40.")
stack = {"C++": {"0": "C++17, bash/Python runner script, random generators", "1": "C++17, CMake, GoogleTest, optional TCP socket server",
                 "2": "C++17, Qt or terminal UI, OpenStreetMap CSV data", "3": "C++17, ncurses/terminal or Crow web micro-framework",
                 "4": "C++17, libcurl + nlohmann/json for Codeforces API", "5": "C++17, Crow/Drogon REST API, GoogleTest"},
         "Java": {"0": "Java 17, shell/Python runner script, random generators", "1": "Java 17, Maven/Gradle, JUnit 5, optional TCP server",
                  "2": "Java 17, JavaFX or Swing, OpenStreetMap CSV data", "3": "Java 17, Spring Boot (optional) or CLI",
                  "4": "Java 17, java.net.http HttpClient + Jackson for Codeforces API", "5": "Java 17, Spring Boot REST API, JUnit 5"}}[LANGNAME]
projects = [
 ("0", "Stress Tester & Local Judge", "Mandatory (individual)", "L1-L4", "L2", "L4",
  "Random test generators, brute-force vs optimised comparison, time limits, complexity",
  "CLI tool that generates random tests, runs a brute-force and an optimised solution, diffs outputs and reports the first failing case plus run times.",
  "M1: generator + runner (L3) | M2: diff + minimal failing case + timing report (L4)",
  "Correctness 40% · Usability 20% · Code quality 20% · README/demo 20%"),
 ("1", "In-Memory Key-Value Store with LRU/LFU & TTL", "Mandatory (individual)", "L2, L5, L13, L14", "L5", "L14",
  "Hash maps, doubly linked lists, heaps (TTL expiry), design trade-offs",
  "Redis-like store with GET/SET/DEL, a pluggable LRU or LFU eviction policy, key TTL via a min-heap, and a benchmark harness comparing policies.",
  "M1: core map + LRU (L10) | M2: LFU + TTL heap (L13) | M3: benchmarks + tests (L14)",
  "Correctness & complexity 40% · Tests 20% · Design & code quality 20% · Benchmark report 20%"),
 ("2", "City Route Planner", "Elective", "L22-L25", "L14 or L22", "L22 (A) / L33 (B)",
  "BFS, Dijkstra, A*, 0-1 BFS, MST, DSU, graph modelling",
  "Load a city/metro graph and answer shortest-route, fewest-transfers (state graph) and minimum-cable-network (MST) queries. Visualise the paths.",
  "M1: graph loader + BFS/Dijkstra | M2: A* + transfers | M3: MST + visualisation + benchmark",
  "Algorithms 40% · Correctness on test maps 20% · UI/visualisation 20% · Report 20%"),
 ("3", "Rate Limiter & Job Scheduler", "Elective", "L4, L6, L13", "L14 or L22", "L22 (A) / L33 (B)",
  "Sliding window, deques, token bucket, heaps, interval scheduling",
  "Library with fixed-window, sliding-log and token-bucket rate limiters, plus a priority job scheduler with deadlines. Includes a simulator replaying request traces.",
  "M1: 3 limiter algorithms | M2: scheduler with heap | M3: simulator + comparison report",
  "Algorithms 40% · Concurrency safety 20% · Tests 20% · Report 20%"),
 ("4", "Codeforces Profile Analyser & Problem Recommender", "Elective", "L5, L13, L34", "L14 or L22", "L22 (A) / L33 (B)",
  "Hashing, sorting, heaps (top-k), prefix sums over time, binary search on rating",
  "Pulls a user's submissions from the public Codeforces API, computes tag strengths and weaknesses and rating progress, and recommends unsolved problems near the user's rating in weak tags.",
  "M1: API client + caching | M2: analytics (tags, verdicts, timeline) | M3: recommender + report",
  "Data handling 30% · Analytics correctness 30% · Recommendation quality 20% · UX/report 20%"),
 ("5", "Capstone: Mini Search Engine", "Capstone (team 2-3)", "L5, L13, L30, L35, L36", "L33", "L40",
  "Tries, inverted index, hashing, heaps (top-k ranking), edit distance (did-you-mean), segment tree / BIT for analytics",
  "Indexes a document corpus, supports prefix autocomplete (trie), ranked keyword search (TF-IDF + top-k heap), spell correction (edit distance) and a query-analytics dashboard. Exposed via REST API or CLI.",
  "M1: tokenizer + inverted index (L35) | M2: ranking + autocomplete (L36) | M3: spell-check + API + demo (L40)",
  "Algorithms & complexity 35% · Feature completeness 25% · Code quality & tests 20% · Demo & viva 20%"),
]
cols = ["Project #", "Project", "Category", "Reinforces lectures", "Kickoff", "Due", "DSA concepts applied", "Description",
        "Milestones", f"Suggested {LANGNAME} stack", "Grading rubric"]
header(pj, 4, cols, [9, 30, 16, 16, 10, 14, 36, 55, 42, 34, 34])
for i, p in enumerate(projects):
    r = 5 + i
    vals = list(p[:8]) + [p[8], stack[p[0]], p[9]]
    for j, v in enumerate(vals, 1):
        body(pj.cell(row=r, column=j, value=v), bold=(j == 2))
    pj.row_dimensions[r].height = 110
r = 5 + len(projects) + 1
pj.cell(row=r, column=1, value="Resume tip: projects 1, 2, 4 and 5 make the strongest resume lines. Ask students to report measurable results (e.g. 'O(1) LRU, 1M ops/s').").font = Font(name=F, italic=True, size=10)

# ================= Sheet 6: Placement Module =================
pm = wb.create_sheet("Placement Module")
title(pm, "Placement readiness module (L37-L40 + ongoing)")
cols = ["Area", "Item", "What students do", "When", "Deliverable / check"]
header(pm, 4, cols, [22, 30, 60, 14, 34])
items = [
 ("Online assessments", "OA strategy", "Read all problems first; bank easy points; write brute force for partial credit; test edge cases (n=1, max values, duplicates, negatives)", "L37", "Mock OA score"),
 ("Online assessments", "Common OA patterns", "Arrays/strings + hashing, greedy + sorting, BFS/DSU on grids, 1D/2D DP, binary search on answer: map each to the Problem Bank", "L37", "Pattern cheat-sheet"),
 ("Low-level design", "OOP & SOLID", "Encapsulation, inheritance vs composition, interfaces; SOLID with small examples", "L38", "Class-diagram exercise"),
 ("Low-level design", "Design patterns", "Strategy (eviction policy), Observer (notifications), Factory, Singleton; tied to Projects 1 and 3", "L38", "Refactor one project using a pattern"),
 ("Low-level design", "Classic LLD problems", "Parking lot, LRU cache, rate limiter, elevator, BookMyShow-style seat booking: entities, APIs, concurrency notes", "L38", "One LLD write-up per student"),
 ("Interviews", "Think-aloud framework", "Clarify → examples → brute force → optimise → code → dry run → complexity → edge cases", "L39", "Used in every mock"),
 ("Interviews", "Mock interviews", "2 × 45-min peer/instructor mocks: one DSA, one DSA + LLD", "L39", "Mock interview rubric (below)"),
 ("Interviews", "Behavioural (STAR)", "Prepare 5 STAR stories: conflict, failure, leadership, deadline, project deep-dive", "L39", "STAR story sheet"),
 ("CS fundamentals", "OOP, DBMS, OS, CN", "Revision checklist: normalisation, indexing, transactions/ACID; processes vs threads, deadlock, paging; TCP/UDP, HTTP, DNS", "Self-study, wk 15-20", "Quiz in L39"),
 ("Profile building", "Resume", "One page; 2-3 projects with measurable impact; coding profiles with ratings; no fluff", "L39", "Instructor-reviewed resume"),
 ("Profile building", "GitHub & coding profiles", "Pinned project repos with READMEs; solutions repo; Codeforces/LeetCode/CodeChef handles linked", "Ongoing", "Profiles in Student Tracker"),
 ("Profile building", "Revision plan", "Last 2 weeks before drives: revisit 'Revisit'-status problems, one mock OA every 3 days", "After L40", "Personal plan"),
]
for i, row in enumerate(items):
    r = 5 + i
    for j, v in enumerate(row, 1):
        body(pm.cell(row=r, column=j, value=v), bold=(j == 1))
    pm.row_dimensions[r].height = 40
r = 5 + len(items) + 1
pm.cell(row=r, column=1, value="Mock interview rubric (score 1-5 each)").font = Font(name=F, bold=True, size=11, color="1F3864"); r += 1
header(pm, r, ["Criterion", "Weight", "1 = needs work", "3 = acceptable", "5 = hire signal"]); r += 1
rstart = r
for crit, w, a, b, c in [("Problem understanding", 0.15, "Jumps into code", "Asks some clarifying questions", "Clarifies constraints & edge cases upfront"),
                         ("Approach & optimisation", 0.30, "Brute force only", "Reaches optimal with hints", "Reaches optimal independently, compares options"),
                         ("Coding", 0.25, "Buggy, messy", "Works with minor bugs", "Clean, modular, bug-free"),
                         ("Testing & complexity", 0.15, "No dry run", "Dry runs happy path", "Tests edge cases, states exact complexity"),
                         ("Communication", 0.15, "Silent", "Explains when asked", "Thinks aloud clearly throughout")]:
    body(pm.cell(row=r, column=1, value=crit), bold=True)
    cc = pm.cell(row=r, column=2, value=w); body(cc, color="0000FF"); cc.number_format = "0%"
    for j, v in enumerate([a, b, c], 3): body(pm.cell(row=r, column=j, value=v))
    r += 1
body(pm.cell(row=r, column=1, value="Total"), bold=True)
cc = pm.cell(row=r, column=2, value=f"=SUM(B{rstart}:B{r-1})"); body(cc, bold=True); cc.number_format = "0%"

# ================= Sheet 7: Language Toolkit =================
lt = wb.create_sheet(f"{LANGNAME} Toolkit")
title(lt, f"{LANGNAME} competitive-programming toolkit", "Containers, idioms and pitfalls used throughout the course")
header(lt, 4, ["Need", f"{LANGNAME} tool / idiom", "Complexity", "Pitfall / tip"], [28, 52, 16, 60])
if LANGNAME == "C++":
    kit = [("Fast I/O", "ios::sync_with_stdio(false); cin.tie(nullptr);", "-", "Don't mix printf/scanf with cin/cout after this; use '\\n', not endl"),
           ("64-bit integers", "long long; 1LL * a * b", "-", "int overflow is the #1 cause of WA; sums beyond 2.1e9 need long long"),
           ("Dynamic array", "vector<T>, reserve(), emplace_back", "O(1) amortised push", "Pass by reference (const vector<int>&) to avoid copies"),
           ("Hash map / set", "unordered_map / unordered_set + custom splitmix64 hash", "O(1) avg", "Anti-hash tests on Codeforces can cause TLE; use a custom hash"),
           ("Ordered map / set", "map, set, multiset; lower_bound(), prev(), next()", "O(log n)", "multiset::erase(value) removes ALL copies; use erase(find(x))"),
           ("Priority queue", "priority_queue<T> (max); priority_queue<T, vector<T>, greater<T>> (min)", "O(log n)", "No decrease-key: push duplicates and skip stale entries"),
           ("Deque / stack / queue", "deque<T>, stack<T>, queue<T>", "O(1)", "Use vector as a stack when you need iteration"),
           ("Sorting", "sort(v.begin(), v.end(), [](auto&a, auto&b){ return ...; })", "O(n log n)", "Comparator must be a strict weak ordering (use <, never <=)"),
           ("Binary search", "lower_bound / upper_bound / partition_point", "O(log n)", "On a set/map use s.lower_bound(x), not std::lower_bound (that is O(n))"),
           ("Bits", "__builtin_popcountll, __builtin_ctzll, __lg, bitset<N>", "O(1) / O(N/64)", "1<<40 overflows int; write 1LL<<40"),
           ("Permutations", "next_permutation", "O(n) per step", "Sort first to enumerate all permutations"),
           ("Policy-based DS", "__gnu_pbds ordered_set (order_of_key, find_by_order)", "O(log n)", "GCC only; handy for k-th element / rank queries"),
           ("Deep recursion", "Iterative DFS or increase stack (judge-dependent)", "-", "Recursion depth 1e5+ on a line tree can overflow the stack"),
           ("Template", "#include <bits/stdc++.h>, using ll = long long; solve() per test case", "-", "Reset global arrays between test cases")]
else:
    kit = [("Fast I/O", "BufferedReader + StringTokenizer (or custom DataInputStream reader); PrintWriter with flush at end", "-", "Scanner and System.out.println are too slow for 1e5+ lines"),
           ("64-bit integers", "long; (long) a * b", "-", "int overflow silently wraps; cast before multiplying"),
           ("Dynamic array", "ArrayList<Integer>, or int[] when the size is known", "O(1) amortised add", "Boxing is slow; prefer primitive arrays in hot loops"),
           ("Hash map / set", "HashMap / HashSet; map.merge(k, 1, Integer::sum)", "O(1) avg", "Anti-hash tests: randomise keys (e.g. XOR with a random salt) or use TreeMap"),
           ("Ordered map / set", "TreeMap / TreeSet; floorKey, ceilingKey, higherKey", "O(log n)", "Multiset = TreeMap<Integer,Integer> of counts"),
           ("Priority queue", "PriorityQueue<T> (min); new PriorityQueue<>(Comparator.reverseOrder()) (max)", "O(log n)", "remove(Object) is O(n); use lazy deletion"),
           ("Deque / stack / queue", "ArrayDeque<T> for stack and queue", "O(1)", "Avoid legacy Stack and LinkedList (slower)"),
           ("Sorting", "Arrays.sort(arr, (a,b) -> Integer.compare(a[0], b[0])); Collections.sort", "O(n log n)", "Arrays.sort(int[]) is quicksort and can be hacked to O(n^2): shuffle first or sort Integer[]/long via list"),
           ("Binary search", "Hand-written lowerBound(); TreeSet.ceiling()", "O(log n)", "Arrays.binarySearch returns an arbitrary index with duplicates"),
           ("Bits", "Long.bitCount, Long.numberOfTrailingZeros, BitSet", "O(1) / O(N/64)", "Use >>> for unsigned shift; 1L<<40 for longs"),
           ("Strings", "StringBuilder; char[] s = str.toCharArray()", "O(n)", "String += in a loop is O(n^2)"),
           ("Deep recursion", "new Thread(null, () -> solve(), \"main\", 1<<27).start();", "-", "Default stack overflows at depth ~1e4-1e5"),
           ("Equality", "a.equals(b) for Integer/Long objects", "-", "Using == on Integer outside -128..127 compares references, not values"),
           ("Template", "Main class with FastReader, PrintWriter out, solve() per test case", "-", "Always out.flush()/close() at the end")]
for i, row in enumerate(kit):
    r = 5 + i
    for j, v in enumerate(row, 1):
        body(lt.cell(row=r, column=j, value=v), bold=(j == 1))
    lt.row_dimensions[r].height = 32

# ================= Sheet 8: Student Tracker =================
st = wb.create_sheet("Student Tracker")
title(st, "Student progress tracker (template)",
      "Edit yellow cells only. Row 5 is an example. Scores are 0-100; Final score uses weights from Course Overview.")
cols = ["Student name", "Roll no.", "Codeforces handle", "LeetCode handle", "CodeChef handle", "CF rating (start)", "CF rating (current)",
        "Rating gain", "Problems solved (of bank)", "% of bank solved", "Avg contest score", "Project score", "Mock OA + interview score",
        "Problem score", "Final weighted score", "Grade"]
header(st, 4, cols, [20, 10, 16, 16, 16, 10, 10, 9, 11, 10, 10, 10, 12, 10, 12, 8])
ex = ["Example Student", "21CS001", "example_cf", "example_lc", "example_cc", 950, 1240, None, 120, None, 68, 82, 74]
for r in range(5, 46):
    for j in range(1, 17):
        c = st.cell(row=r, column=j); body(c)
        if j <= 7 or j in (9, 11, 12, 13):
            c.fill = INPUT_FILL
            c.font = Font(name=F, size=10, color="0000FF")
    if r == 5:
        for j, v in enumerate(ex, 1):
            if v is not None: st.cell(row=r, column=j, value=v)
    st.cell(row=r, column=8, value=f'=IF(OR(F{r}="",G{r}=""),"",G{r}-F{r})')
    st.cell(row=r, column=10, value=f'=IF(I{r}="","",I{r}/{NPROB})'); st.cell(row=r, column=10).number_format = "0%"
    st.cell(row=r, column=14, value=f'=IF(I{r}="","",MIN(100,I{r}/{NPROB}*100/0.7))'); st.cell(row=r, column=14).number_format = "0"
    wa, wb_ = WEIGHT_ROWS
    st.cell(row=r, column=15, value=(f'=IF(A{r}="","",IFERROR(K{r}*\'Course Overview\'!$B${wa}+N{r}*\'Course Overview\'!$B${wa+1}'
                                     f'+L{r}*\'Course Overview\'!$B${wa+2}+M{r}*\'Course Overview\'!$B${wa+3},""))'))
    st.cell(row=r, column=15).number_format = "0.0"
    st.cell(row=r, column=16, value=f'=IF(O{r}="","",IF(O{r}>=85,"A",IF(O{r}>=70,"B",IF(O{r}>=55,"C","D"))))')
st["N4"].comment = Comment("Problem score = % of bank solved scaled so that solving 70% of the bank earns 100 (the course target). Capped at 100.", "Course")
st["P4"].comment = Comment("Grade bands: A >= 85, B >= 70, C >= 55, else D. Adjust to your institution's policy.", "Course")
st.freeze_panes = "C5"

st.conditional_formatting.add("O5:O45", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=100, color="5B9BD5"))
st.conditional_formatting.add("J5:J45", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="70AD47"))
st.conditional_formatting.add("H5:H45", ColorScaleRule(start_type="num", start_value=-100, start_color="F8696B", mid_type="num", mid_value=0, mid_color="FFFFFF", end_type="num", end_value=400, end_color="63BE7B"))
for g, col in (("A", "C6EFCE"), ("B", "DDEBF7"), ("C", "FFEB9C"), ("D", "F8CBAD")):
    st.conditional_formatting.add("P5:P45", CellIsRule(operator="equal", formula=[f'"{g}"'], fill=PatternFill("solid", start_color=col, end_color=col), font=Font(name=F, bold=True)))

# ================= Lecture Explorer =================
le = wb.create_sheet("Lecture Explorer", 1)
le["A1"] = "Lecture Explorer"; le["A1"].font = Font(name=F, bold=True, size=16, color="1F3864")
le["A2"] = "Pick a lecture number in the yellow cell. The lecture's details and problems appear below; click 'Open' to go to the problem."
le["A2"].font = Font(name=F, italic=True, size=9, color="595959")
for col, w in zip("ABCDEFGHI", [4, 20, 16, 44, 14, 24, 10, 14, 14]):
    le.column_dimensions[col].width = w
body(le.cell(row=5, column=2, value="Select lecture ▶"), bold=True)
c = le.cell(row=5, column=3, value=1); c.fill = INPUT_FILL; c.font = Font(name=F, bold=True, size=14, color="0000FF")
c.alignment = Alignment(horizontal="center", vertical="center"); c.border = BORDER
le.row_dimensions[5].height = 26
dvl = DataValidation(type="list", formula1="='Lecture Plan'!$A$5:$A$44", allow_blank=False)
dvl.prompt = "Choose lecture 1-40"; dvl.promptTitle = "Lecture"
le.add_data_validation(dvl); dvl.add("C5")
fields = [("Topic", 4), ("Module", 3), ("Week", 2), ("Subtopics", 6), ("Learning outcomes", 7), ("Session format", 8),
          (f"{LANGNAME} focus", 9), ("Project milestone", 14)]
for k, (lbl, colno) in enumerate(fields):
    r = 7 + k
    body(le.cell(row=r, column=2, value=lbl), bold=True); le.cell(row=r, column=2).fill = SUB_FILL
    col = get_column_letter(colno)
    c = le.cell(row=r, column=3, value=f"=IFERROR(INDEX('Lecture Plan'!${col}$5:${col}$44,MATCH($C$5,'Lecture Plan'!$A$5:$A$44,0))&\"\",\"\")")
    body(c, bold=(lbl == "Topic"))
    le.merge_cells(start_row=r, start_column=3, end_row=r, end_column=9)
    le.row_dimensions[r].height = 36 if lbl in ("Subtopics", "Learning outcomes", "Session format", f"{LANGNAME} focus") else 20
r0 = 7 + len(fields) + 1
le.cell(row=r0, column=2, value="Problems for this lecture").font = Font(name=F, bold=True, size=11, color="1F3864")
hdr = ["#", "Problem ID", "Problem name", "Platform", "Type", "Difficulty", "Link", "Status (edit in Problem Bank)"]
for j, h in enumerate(hdr, 2):
    c = le.cell(row=r0 + 1, column=j, value=h); c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = HDR_FILL; c.border = BORDER
    c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
le.column_dimensions["I"].width = 18
PB = "'Problem Bank'!"
rng = lambda col: f"{PB}${col}$5:${col}${pend}"
for n in range(1, 16):
    r = r0 + 1 + n
    m = f"MATCH({n},{rng('O')},0)"
    vals = [n,
            f"=IFERROR(INDEX({rng('A')},{m}),\"\")",
            f"=IFERROR(INDEX({rng('D')},{m}),\"\")",
            f"=IFERROR(INDEX({rng('E')},{m}),\"\")",
            f"=IFERROR(INDEX({rng('G')},{m}),\"\")",
            f"=IFERROR(INDEX({rng('H')},{m}),\"\")",
            f"=IFERROR(HYPERLINK(INDEX({rng('F')},{m}),\"Open ↗\"),\"\")",
            f"=IFERROR(INDEX({rng('K')},{m}),\"\")"]
    for j, v in enumerate(vals, 2):
        c = le.cell(row=r, column=j, value=v); body(c)
    le.cell(row=r, column=8).font = Font(name=F, size=10, color="0563C1", underline="single")
    le.cell(row=r, column=2).value = f'=IF(C{r}="","",{n})'
last = r0 + 16
for s_, col in STATUS_COL.items():
    le.conditional_formatting.add(f"I{r0+2}:I{last}", CellIsRule(operator="equal", formula=[f'"{s_}"'], fill=PatternFill("solid", start_color=col, end_color=col)))
for d_, col in (("Easy", "E2EFDA"), ("Medium", "FFF2CC"), ("Hard", "FCE4D6")):
    le.conditional_formatting.add(f"G{r0+2}:G{last}", CellIsRule(operator="equal", formula=[f'"{d_}"'], fill=PatternFill("solid", start_color=col, end_color=col)))
body(le.cell(row=last + 2, column=2, value="Solved here"), bold=True)
c = le.cell(row=last + 2, column=3, value=f'=COUNTIF(I{r0+2}:I{last},"Solved")+COUNTIF(I{r0+2}:I{last},"Upsolved")'); body(c)
body(le.cell(row=last + 2, column=4, value=f'=COUNTIF(C{r0+2}:C{last},"P*")&" problems in this lecture"'))
le.sheet_view.showGridLines = False

# ================= Home dashboard =================
hm = wb.create_sheet("Home", 0)
hm["B2"] = f"DSA & Competitive Programming: {LANGNAME} Track"
hm["B2"].font = Font(name=F, bold=True, size=18, color="1F3864")
hm["B3"] = "Course home. Click a tile to open a sheet. Progress updates as Status is set in the Problem Bank."
hm["B3"].font = Font(name=F, italic=True, size=10, color="595959")
for col, w in zip("ABCDEFGH", [2, 30, 14, 14, 14, 30, 2, 30]):
    hm.column_dimensions[col].width = w
nav = [("Course Overview", "Parameters, weights, rules"), ("Lecture Explorer", "Pick a lecture, see its problems"),
       ("Lecture Plan", "All 40 lectures"), ("Problem Bank", f"{NPROB} problems + status"),
       ("Contests & Assessments", "Contests, OAs, rating goals"), ("Projects", "7 projects + rubrics"),
       ("Placement Module", "OA, LLD, interviews, resume"), (f"{LANGNAME} Toolkit", "Containers, idioms, pitfalls"),
       ("Student Tracker", "Class roster & grading")]
NAV_FILL = PatternFill("solid", start_color="2F5597")
hm.cell(row=5, column=8, value="Go to").font = Font(name=F, bold=True, size=12, color="1F3864")
for k, (sheet, desc) in enumerate(nav):
    r = 6 + k
    c = hm.cell(row=r, column=8, value=f"▶  {sheet}")
    c.hyperlink = f"#'{sheet}'!A1"; c.fill = NAV_FILL; c.font = Font(name=F, bold=True, color="FFFFFF", size=11)
    c.alignment = Alignment(vertical="center", indent=1); c.border = Border(bottom=Side(style="thick", color="FFFFFF"))
    hm.row_dimensions[r].height = 24
    d = hm.cell(row=r, column=9, value=desc); d.font = Font(name=F, size=9, color="595959"); d.alignment = Alignment(vertical="center")
hm.column_dimensions["I"].width = 30
# overall progress
hm.cell(row=5, column=2, value="Overall progress").font = Font(name=F, bold=True, size=12, color="1F3864")
solved = lambda extra="": f'COUNTIFS({rng("K")},"Solved"{extra})+COUNTIFS({rng("K")},"Upsolved"{extra})'
kpis = [("Problems solved", f"={solved()}", "0"), ("Total problems", f"=COUNTA({rng('A')})", "0"),
        ("% complete", "=IFERROR(C6/C7,0)", "0%"), ("Marked 'Revisit'", f'=COUNTIF({rng("K")},"Revisit")', "0")]
for k, (lbl, f, fmt) in enumerate(kpis):
    r = 6 + k
    body(hm.cell(row=r, column=2, value=lbl), bold=True)
    c = hm.cell(row=r, column=3, value=f); body(c, bold=True); c.number_format = fmt
hm.conditional_formatting.add("C8", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="70AD47"))
# by module
r = 11
hm.cell(row=r, column=2, value="Progress by module").font = Font(name=F, bold=True, size=12, color="1F3864"); r += 1
for j, h in enumerate(["Module", "Problems", "Solved", "% done", "Lectures"], 2):
    c = hm.cell(row=r, column=j, value=h); c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = HDR_FILL; c.border = BORDER
r += 1; ms = r
for m in mods:
    lecs = [l[0] for l in L if l[1] == m]
    body(hm.cell(row=r, column=2, value=m), bold=True); hm.cell(row=r, column=2).fill = MOD_FILLS[m]
    body(hm.cell(row=r, column=3, value=f'=COUNTIF({rng("N")},B{r})'))
    body(hm.cell(row=r, column=4, value=f'={solved(f",{rng(chr(78))},B{r}")}'))
    c = hm.cell(row=r, column=5, value=f"=IFERROR(D{r}/C{r},0)"); body(c); c.number_format = "0%"
    body(hm.cell(row=r, column=6, value=f"L{lecs[0]}-L{lecs[-1]}" if len(lecs) > 1 else f"L{lecs[0]}"))
    r += 1
hm.conditional_formatting.add(f"E{ms}:E{r-1}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="5B9BD5"))
# by difficulty & platform
r += 1
hm.cell(row=r, column=2, value="By difficulty & platform").font = Font(name=F, bold=True, size=12, color="1F3864"); r += 1
for j, h in enumerate(["Group", "Problems", "Solved", "% done"], 2):
    c = hm.cell(row=r, column=j, value=h); c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = HDR_FILL; c.border = BORDER
r += 1; ds = r
for grp, col in [("Easy", "H"), ("Medium", "H"), ("Hard", "H"), ("CSES", "E"), ("LeetCode", "E"), ("Codeforces", "E"), ("AtCoder", "E")]:
    body(hm.cell(row=r, column=2, value=grp), bold=True)
    body(hm.cell(row=r, column=3, value=f'=COUNTIF({rng(col)},B{r})'))
    body(hm.cell(row=r, column=4, value=f'={solved(f",{rng(col)},B{r}")}'))
    c = hm.cell(row=r, column=5, value=f"=IFERROR(D{r}/C{r},0)"); body(c); c.number_format = "0%"
    r += 1
hm.conditional_formatting.add(f"E{ds}:E{r-1}", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="ED7D31"))
hm.sheet_view.showGridLines = False

# back-to-home links
for s in wb.worksheets:
    if s.title == "Home": continue
    c = s["A3"]; c.value = "⌂ Back to Home"; c.hyperlink = "#'Home'!A1"
    c.font = Font(name=F, size=9, bold=True, color="0563C1", underline="single")
    s.sheet_view.showGridLines = False
wb.active = 0
wb.save(OUT)

# export data for the web portal
if os.environ.get("EXPORT_JSON"):
    out = dict(lang=LANGNAME, lectures=[dict(no=l[0], module=l[1], topic=l[2], sub=l[3], out=l[4], kind=l[5],
                format=FORMAT[l[5]], note=LANG[LANGNAME][l[0]], milestone=PROJECT_MILESTONE.get(l[0], "")) for l in L],
               problems=probs, projects=[dict(no=p[0], name=p[1], cat=p[2], lecs=p[3], kick=p[4], due=p[5], concepts=p[6],
                desc=p[7], miles=p[8], rubric=p[9], stack=stack[p[0]]) for p in projects],
               kit=kit, contests=contests, live=live, placement=items, platforms=plats, weights=weights)
    json.dump(out, open(os.environ["EXPORT_JSON"], "w"), ensure_ascii=False)
print(OUT, "lectures", NLEC, "problems", NPROB)
