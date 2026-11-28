{
const D = __DATA__;
const STAT = ["Not started","Attempted","Solved","Upsolved","Revisit"];
const KEY = "dsa-course-v1";
const MC = ["#8fd3ff","#ff5c8a","#f6c26b","#7ee0b5","#b9a6ff","#ff9f6e","#5ec8e5","#e98fd0","#a5d66b","#ffd36e","#7fb2ff","#ff7a7a"];
const W = Object.fromEntries(D.weights.map((w, i) => [["contests","problems","projects","mock"][i], w[1]]));
const NP = D.problems.length;

// ---------- local state (always kept, also the offline fallback) ----------
let S = {lang:"cpp", st:{}, prof:{}};
try { const raw = localStorage.getItem(KEY); if (raw) S = Object.assign(S, JSON.parse(raw)); } catch (e) {}
const saveLocal = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} };

const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const $ = id => document.getElementById(id);
const st = p => S.st[p.id] || "Not started";
const isDone = s => s === "Solved" || s === "Upsolved";
const done = p => isDone(st(p));
const mods = [...new Set(D.lectures.map(l => l.module))];
const mcol = m => MC[mods.indexOf(m) % MC.length];
const lecById = Object.fromEntries(D.lectures.map(l => [l.no, l]));
const byLec = {}; D.problems.forEach(p => (byLec[p.lec] ||= []).push(p));
const pById = Object.fromEntries(D.problems.map(p => [p.id, p]));
const handle = h => String(h || "").trim().replace(/[^A-Za-z0-9_.\-]/g, "").slice(0, 40);
const num = v => { const n = Number(v); return Number.isFinite(n) ? Math.max(0, Math.min(100, n)) : null; };
const open = new Set(); let modF = "";
$("nprob").textContent = NP;
let tt; const toast = t => { $("toast").textContent = t; $("toast").classList.add("on"); clearTimeout(tt); tt = setTimeout(() => $("toast").classList.remove("on"), 1800); };

// ---------- shared-data state (Option A pilot) ----------
const R = {db:null, user:null, uid:null, staff:false, ref:null, readOnly:false, ready:false,
  all:{}, scores:{}, names:{}, mine:null, saving:false, dirty:false, timer:null};
function setSync(s, text) {
  $("sync").dataset.s = s; $("synct").textContent = text;
  $("leadsave").textContent = s === "ok" ? "Your progress syncs to the course database, so your teachers can see it." : "Your progress is saved in this browser.";
}

// ---------- readiness maths (same formula as the Excel Student Tracker) ----------
function readiness(stMap, sc) {
  const solved = Object.values(stMap || {}).filter(isDone).length;
  const probScore = Math.min(100, solved / NP * 100 / 0.7);
  const cs = Object.values(sc?.contests || {}).map(num).filter(v => v !== null);
  const contest = cs.length ? cs.reduce((a, b) => a + b, 0) / cs.length : null;
  const proj = num(sc?.projects ?? NaN), mock = num(sc?.mock ?? NaN);
  const score = (contest ?? 0) * W.contests + probScore * W.problems + (proj ?? 0) * W.projects + (mock ?? 0) * W.mock;
  return {solved, pct: solved / NP, probScore, contest, proj, mock, score};
}

const opts = (el, label, vals, keep) => { const cur = el.value; el.innerHTML = `<option value="">${esc(label)}</option>` + vals.map(v => `<option>${esc(v)}</option>`).join(""); if (keep && vals.includes(cur)) el.value = cur; };
opts($("pf-plat"), "Platform", [...new Set(D.problems.map(p => p.plat))]);
opts($("pf-diff"), "Level", ["Easy","Medium","Hard"]);
opts($("pf-typ"), "Type", [...new Set(D.problems.map(p => p.typ))]);
opts($("pf-mod"), "Module", mods);
opts($("pf-st"), "Status", STAT);

const CHECK = `<svg viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>`;
const mini = pc => `<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="none" stroke="var(--soft)" stroke-width="6"/><circle cx="20" cy="20" r="16" fill="none" stroke="var(--pink)" stroke-width="6" stroke-linecap="round" stroke-dasharray="100.5" stroke-dashoffset="${100.5 - pc * 1.005}"/></svg>`;
const prow = (p, showLec) => `<div class="prow st-${st(p).replace(/ /g,"")}">
  <button class="chk${done(p)?" on":""}" data-tog="${esc(p.id)}" aria-pressed="${done(p)}" aria-label="Mark ${esc(p.name)} solved">${CHECK}</button>
  <div class="pname"><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.name)}</a><div class="sub"><span>${esc(p.plat)}</span><span class="tag d-${p.diff}">${p.diff}</span><span class="tag">${esc(p.typ)}</span>${showLec?`<span>L${p.lec}</span>`:""}<span>${esc(p.idea)}</span></div></div>
  <select class="stsel s-${st(p).replace(/ /g,"")}" data-id="${esc(p.id)}" aria-label="Status of ${esc(p.name)}">${STAT.map(s => `<option${st(p)===s?" selected":""}>${s}</option>`).join("")}</select>
  <a class="open" href="${esc(p.url)}" target="_blank" rel="noopener">Open ↗</a></div>`;

function header() {
  const all = D.problems, n = all.filter(done).length, pc = Math.round(n / NP * 100);
  $("pct").textContent = pc + "%";
  $("arc").style.strokeDashoffset = 326.7 * (1 - n / NP);
  const c = s => all.filter(p => st(p) === s).length;
  $("stats").innerHTML = [["Solved", n, "#ff5c8a"], ["Attempted", c("Attempted"), "#f6c26b"], ["To revisit", c("Revisit"), "#ff9f6e"], ["Remaining", NP - n, "#8fd3ff"]]
    .map(([l, v, col]) => `<div class="stat"><b>${v}</b><span><i class="dot" style="background:${col}"></i>${l}</span></div>`).join("");
  $("board").innerHTML = mods.map(m => `<div class="mod"><h3>${esc(m.replace(/^M\d+ /, ""))}</h3><div class="tiles">${
    D.lectures.filter(l => l.module === m).map(l => { const ps = byLec[l.no] || [], d = ps.filter(done).length, p = ps.length ? Math.round(d / ps.length * 100) : 0;
      return `<button class="tile${p===100?" done":""}" style="--p:${p}%" data-lec="${l.no}" title="L${l.no}: ${esc(l.topic)} (${d}/${ps.length})" aria-label="Lecture ${l.no}, ${d} of ${ps.length} solved">${l.no}</button>`; }).join("")}</div></div>`).join("");
  const next = all.find(p => !done(p) && p.typ !== "Contest");
  $("cont").innerHTML = next ? `<div><div class="lbl">Continue where you left off</div><a href="${esc(next.url)}" target="_blank" rel="noopener">${esc(next.name)}</a><div class="m">Lecture ${next.lec} · ${esc(lecById[next.lec].topic)} · ${esc(next.plat)}</div></div><button class="btn ghost go" data-goto="${next.lec}">View lecture</button>`
    : `<div><div class="lbl">All done</div><div class="m">Every problem is solved. Time for mock interviews.</div></div>`;
}

function lectures() {
  const q = $("lq").value.toLowerCase(), notes = D.notes[S.lang], L = S.lang === "cpp" ? "C++" : "Java";
  $("lchips").innerHTML = [["", "All modules"], ...mods.map(m => [m, m])].map(([v, t]) => `<button class="chip" data-mod="${esc(v)}" aria-pressed="${modF===v}">${esc(t)}</button>`).join("");
  const list = D.lectures.filter(l => (!modF || l.module === modF) && (!q || (l.topic + " " + l.sub + " " + l.module).toLowerCase().includes(q)));
  $("lcount").textContent = `${list.length} of 40 lectures`;
  $("leclist").innerHTML = list.map(l => {
    const ps = byLec[l.no] || [], d = ps.filter(done).length, pc = ps.length ? d / ps.length * 100 : 0;
    return `<details class="lec${pc===100?" full":""}" id="lec-${l.no}" data-no="${l.no}"${open.has(l.no)?" open":""}><summary>
      <div class="num">${l.no}</div>
      <div><h4>${esc(l.topic)}</h4><div class="meta"><span class="mtag" style="--mc:${mcol(l.module)}"><i></i>${esc(l.module)}</span><span>Week ${Math.ceil(l.no/2)}</span><span>3 hrs</span></div></div>
      <div class="mini">${mini(pc)}<span>${d}/${ps.length}</span><svg class="chev" viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg></div></summary>
      <div class="body">
        <div class="info"><div class="box"><span class="k">Subtopics</span>${esc(l.sub)}</div><div class="box"><span class="k">You will be able to</span>${esc(l.out)}</div><div class="box lang"><span class="k">${L} focus</span>${esc(notes[l.no-1])}</div></div>
        <div class="box" style="margin-bottom:12px"><span class="k">Session plan</span>${esc(l.format).replace(/ \| /g, " · ")}</div>
        ${lecMod[l.no] ? `<button class="btn rdnotes" data-notes="${l.no}">${BOOK} Read the lecture notes</button>` : ""}
        ${l.milestone ? `<div class="ms">Project milestone: ${esc(l.milestone)}</div>` : ""}
        <div class="plist">${ps.map(p => prow(p, false)).join("")}</div></div></details>`;
  }).join("") || `<div class="empty">No lectures match your search.</div>`;
}

function problems() {
  const q = $("pq").value.toLowerCase(), f = id => $(id).value;
  const list = D.problems.filter(p => (!q || (p.name + " " + p.idea + " " + lecById[p.lec].topic).toLowerCase().includes(q))
    && (!f("pf-plat") || p.plat === f("pf-plat")) && (!f("pf-diff") || p.diff === f("pf-diff")) && (!f("pf-typ") || p.typ === f("pf-typ"))
    && (!f("pf-mod") || lecById[p.lec].module === f("pf-mod")) && (!f("pf-st") || st(p) === f("pf-st")));
  $("pcnt").textContent = `${list.length} of ${NP}`;
  $("plist").innerHTML = list.map(p => prow(p, true)).join("") || `<div class="empty">No problems match these filters.</div>`;
}

function statics() {
  const sk = D.stacks[S.lang], L = S.lang === "cpp" ? "C++" : "Java";
  $("projcards").innerHTML = D.projects.map((p, i) => `<article class="card"><div class="top"><div class="badge">${esc(p.no)}</div><div><h4>${esc(p.name)}</h4><div class="meta"><span>${esc(p.cat)}</span><span>Kickoff ${esc(p.kick)}</span><span>Due ${esc(p.due)}</span></div></div></div>
    <p>${esc(p.desc)}</p><dl class="kv"><dt>DSA used</dt><dd>${esc(p.concepts)}</dd><dt>Lectures</dt><dd>${esc(p.lecs)}</dd><dt>Milestones</dt><dd>${esc(p.miles).replace(/ \| /g, " → ")}</dd><dt>${L} stack</dt><dd>${esc(sk[i])}</dd><dt>Rubric</dt><dd>${esc(p.rubric)}</dd></dl></article>`).join("");
  $("tk-tab").textContent = `${L} toolkit`; $("tk-h").textContent = `${L} toolkit`;
  $("tktb").innerHTML = D.kit[S.lang].map(r => `<tr><td data-l="Need"><b>${esc(r[0])}</b></td><td data-l="Tool"><code>${esc(r[1])}</code></td><td data-l="Cost">${esc(r[2])}</td><td data-l="Watch out">${esc(r[3])}</td></tr>`).join("");
  $("l-cpp").setAttribute("aria-pressed", S.lang === "cpp"); $("l-java").setAttribute("aria-pressed", S.lang === "java");
}

function once() {
  $("ctl").innerHTML = D.contests.map(c => `<div><div class="pin">L${c[1]}</div><b>${esc(c[0])}</b><span>${esc(c[5])} · ${esc(c[3])}</span></div>`).join("");
  $("ctb").innerHTML = D.contests.map(c => `<tr><td data-l="Assessment"><b>${esc(c[0])}</b></td><td data-l="Lecture">L${c[1]}</td><td data-l="Format">${esc(c[2])}</td><td data-l="Syllabus">${esc(c[3])}</td><td data-l="Source">${esc(c[4])}</td><td data-l="Duration">${esc(c[5])}</td></tr>`).join("");
  $("live").innerHTML = D.live.map(c => `<article class="card"><h4>${esc(c[0])}</h4><p class="h2sub" style="margin:0">${esc(c[1])} · ${esc(c[2])}</p><a class="open" style="padding:0" href="${esc(c[3])}" target="_blank" rel="noopener">See schedule ↗</a></article>`).join("");
  $("wts").innerHTML = D.weights.map(w => `<div class="wb"><div class="row">${esc(w[0])}<span>${Math.round(w[1]*100)}%</span></div><div class="track"><i style="width:${w[1]*100}%"></i></div><p>${esc(w[2])}</p></div>`).join("");
  const areas = [...new Set(D.placement.map(r => r[0]))];
  $("pm").innerHTML = areas.map(a => `<article class="card"><h4>${esc(a)}</h4>${D.placement.filter(r => r[0] === a).map(r => `<div style="border-top:1px solid var(--line);padding-top:10px"><b>${esc(r[1])}</b> <span class="tag">${esc(r[3])}</span><p style="margin:4px 0 2px">${esc(r[2])}</p><span class="h2sub" style="font-size:14px">Check: ${esc(r[4])}</span></div>`).join("")}</article>`).join("");
  $("refs").innerHTML = D.platforms.map(r => `<article class="card"><h4>${esc(r[0])}</h4><p>${esc(r[1])}</p><a class="open" style="padding:0" href="${esc(r[2])}" target="_blank" rel="noopener">Open ↗</a></article>`).join("");
}

function scoreView(sc, stMap) {
  const r = readiness(stMap, sc), f = v => v === null ? "–" : Math.round(v);
  const cs = D.contests.map((c, i) => `<span class="tag">${esc(c[0])}: ${f(num(sc?.contests?.["c" + (i + 1)] ?? NaN))}</span>`).join("");
  return `<div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin:10px 0"><div><div class="rd">${Math.round(r.score)}</div><span class="h2sub" style="font-size:13px">Readiness / 100</span></div>
    <div class="pillrow" style="flex:1">${cs}<span class="tag">Projects: ${f(r.proj)}</span><span class="tag">Mock OA &amp; interviews: ${f(r.mock)}</span><span class="tag">Problem score: ${Math.round(r.probScore)}</span></div></div>`;
}

function progress() {
  $("mtb").innerHTML = mods.map(m => { const ps = D.problems.filter(p => lecById[p.lec].module === m), d = ps.filter(done).length, pc = Math.round(d / ps.length * 100);
    return `<div class="mrow"><div><b>${esc(m)}</b><div class="track"><i style="width:${pc}%;background:${mcol(m)}"></i></div></div><div class="n">${d}/${ps.length}</div></div>`; }).join("");
  $("code").value = btoa(JSON.stringify(S.st));
  const pf = S.prof || {};
  [["f-roll","roll"],["f-batch","batch"],["f-cf","cf"],["f-lc","lc"],["f-cc","cc"]].forEach(([id, k]) => { if (document.activeElement !== $(id)) $(id).value = pf[k] || ""; });
  $("pfnote").textContent = R.ref ? "Saved to the course database. Your teachers and placement office can see these details and your progress."
    : "Saved in this browser only. Open the portal from the shared link while signed in to share progress with your teachers.";
  $("myscores").hidden = !R.ref;
  if (R.ref) $("mysc").innerHTML = R.mine ? scoreView(R.mine, S.st) + `<p class="h2sub small">Scores are entered by your teachers after each contest, project review and mock interview.</p>`
    : scoreView({}, S.st) + `<p class="h2sub small">No scores entered yet.</p>`;
}

// ---------- staff views ----------
const ago = iso => { const t = Date.parse(iso); if (!t) return "never"; const d = Math.floor((Date.now() - t) / 864e5); return d <= 0 ? "today" : d === 1 ? "yesterday" : d + " days ago"; };
const nameOf = uid => R.names[uid] || "Student " + uid.slice(-4);
function students() {
  return Object.entries(R.all).map(([uid, d]) => {
    const stMap = (d && typeof d.st === "object" && d.st) || {};
    const r = readiness(stMap, R.scores[uid]);
    const pr = (d && typeof d.prof === "object" && d.prof) || {};
    return {uid, d, st: stMap, r, name: nameOf(uid), roll: String(pr.roll || "").slice(0, 30), batch: String(pr.batch || "").slice(0, 40),
      cf: handle(pr.cf), lc: handle(pr.lc), cc: handle(pr.cc), at: typeof d?.updatedAt === "string" ? d.updatedAt : ""};
  });
}
function classView() {
  if (!R.staff) return;
  const all = students(), batches = [...new Set(all.map(s => s.batch).filter(Boolean))].sort();
  opts($("cb"), "All batches", batches, true); opts($("rb"), "All batches", batches, true);
  const q = $("cq").value.toLowerCase(), b = $("cb").value, sort = $("cs").value;
  const list = all.filter(s => (!b || s.batch === b) && (!q || [s.name, s.roll, s.cf, s.lc].join(" ").toLowerCase().includes(q)));
  list.sort((x, y) => sort === "name" ? x.name.localeCompare(y.name) : sort === "active" ? (y.at > x.at ? 1 : -1) : sort === "ready" ? y.r.score - x.r.score : y.r.pct - x.r.pct);
  $("ccount").textContent = `${list.length} students`;
  const wk = Date.now() - 7 * 864e5, active = list.filter(s => Date.parse(s.at) > wk).length;
  const avg = list.length ? list.reduce((a, s) => a + s.r.pct, 0) / list.length : 0;
  $("ckpi").innerHTML = [[list.length, "Students"], [Math.round(avg * 100) + "%", "Average completion"], [active, "Active in last 7 days"], [list.length - active, "Inactive 7+ days"]]
    .map(([v, l]) => `<div class="kpi"><b>${v}</b><span>${l}</span></div>`).join("");
  const lecPct = D.lectures.map(l => { const ps = byLec[l.no] || []; if (!list.length || !ps.length) return 0;
    return list.reduce((a, s) => a + ps.filter(p => isDone(s.st[p.id])).length / ps.length, 0) / list.length; });
  $("cheat").innerHTML = D.lectures.map((l, i) => { const p = Math.round(lecPct[i] * 100); return `<div class="hc${p > 55 ? " hi" : ""}" style="--p:${p}%" title="L${l.no} ${esc(l.topic)}: ${p}% solved">${l.no}</div>`; }).join("");
  $("ctbody").innerHTML = list.map(s => `<tr><td data-l="Student"><div class="who"><b>${esc(s.name)}</b><span>${esc(s.roll || "No roll number")}</span></div></td><td data-l="Batch">${esc(s.batch || "–")}</td>
    <td data-l="Solved">${s.r.solved} <span class="h2sub" style="font-size:13px">(${Math.round(s.r.pct * 100)}%)</span></td>
    <td data-l="By module"><div class="strip">${mods.map(m => { const ps = D.problems.filter(p => lecById[p.lec].module === m); const p = Math.round(ps.filter(x => isDone(s.st[x.id])).length / ps.length * 100); return `<i style="--p:${p}%" title="${esc(m)}: ${p}%"></i>`; }).join("")}</div></td>
    <td data-l="Last active">${ago(s.at)}</td><td data-l=""><button class="lnk" data-stu="${esc(s.uid)}">Details</button></td></tr>`).join("")
    || `<tr><td colspan="6" class="h2sub" style="padding:24px">No students yet. Students appear here after they open the portal while signed in.</td></tr>`;
  const started = new Set(D.lectures.filter((l, i) => lecPct[i] > 0).map(l => l.no));
  const hard = D.problems.filter(p => started.has(p.lec) && p.typ !== "Contest").map(p => ({p, rate: list.length ? list.filter(s => isDone(s.st[p.id])).length / list.length : 0, rev: list.filter(s => s.st[p.id] === "Revisit").length}))
    .sort((a, b) => a.rate - b.rate || b.rev - a.rev).slice(0, 8);
  $("chard").innerHTML = hard.map(h => `<div class="hard"><div><a href="${esc(h.p.url)}" target="_blank" rel="noopener" style="color:var(--ink);font-weight:600">${esc(h.p.name)}</a><div class="h2sub" style="font-size:13px;margin:0">L${h.p.lec} · ${esc(h.p.plat)}${h.rev ? ` · ${h.rev} marked revisit` : ""}</div></div><div class="n">${Math.round(h.rate * 100)}%</div></div>`).join("")
    || `<p class="h2sub small">Appears once students start solving.</p>`;
  readinessView();
}
function readyList() {
  const b = $("rb").value, min = Number($("rmin").value) || 0, mp = Number($("rpct").value) || 0, cf = $("rcf").checked;
  return students().filter(s => (!b || s.batch === b) && s.r.score >= min && s.r.pct * 100 >= mp && (!cf || s.cf)).sort((x, y) => y.r.score - x.r.score);
}
function readinessView() {
  if (!R.staff) return;
  const list = readyList(), f = v => v === null ? "–" : Math.round(v);
  $("rcount").textContent = `${list.length} students`;
  $("rbody").innerHTML = list.map((s, i) => `<tr><td data-l="#">${i + 1}</td><td data-l="Student"><div class="who"><b>${esc(s.name)}</b><span>${esc(s.roll)}</span></div></td><td data-l="Batch">${esc(s.batch || "–")}</td>
    <td data-l="Solved">${Math.round(s.r.pct * 100)}%</td><td data-l="Contests">${f(s.r.contest)}</td><td data-l="Projects">${f(s.r.proj)}</td><td data-l="Mock">${f(s.r.mock)}</td>
    <td data-l="Readiness"><b>${Math.round(s.r.score)}</b></td><td data-l="Codeforces">${s.cf ? `<a href="https://codeforces.com/profile/${esc(s.cf)}" target="_blank" rel="noopener">${esc(s.cf)}</a>` : "–"}</td></tr>`).join("")
    || `<tr><td colspan="9" class="h2sub" style="padding:24px">No students match these filters.</td></tr>`;
}
const csvCell = v => { let s = String(v ?? ""); if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
async function exportCsv() {
  const rows = [["Rank","Name","Roll","Batch","Solved","% solved","Contest avg","Projects","Mock","Readiness","Codeforces","LeetCode","CodeChef","Last active"]];
  readyList().forEach((s, i) => rows.push([i + 1, s.name, s.roll, s.batch, s.r.solved, Math.round(s.r.pct * 100), s.r.contest === null ? "" : Math.round(s.r.contest),
    s.r.proj ?? "", s.r.mock ?? "", Math.round(s.r.score), s.cf, s.lc, s.cc, s.at.slice(0, 10)]));
  const csv = rows.map(r => r.map(csvCell).join(",")).join("\n");
  const dl = window.claude?.use ? await window.claude.use("downloads").catch(() => null) : null;
  if (dl) { try { await dl.save({filename: "readiness-shortlist.csv", data: csv}); toast("Shortlist exported"); return; } catch (e) {} }
  $("csvout").hidden = false; $("csvout").value = csv; $("csvout").select();
  try { await navigator.clipboard.writeText(csv); toast("CSV copied to clipboard"); } catch (e) { toast("Copy the CSV below"); }
}
function drawer(uid, keepFocus) {
  const s = students().find(x => x.uid === uid); if (!s) return;
  const sc = R.scores[uid] || {}, revisit = D.problems.filter(p => s.st[p.id] === "Revisit");
  const val = v => { const n = num(v ?? NaN); return n === null ? "" : n; };
  $("dbody").innerHTML = `<h3>${esc(s.name)}</h3><p class="h2sub" style="margin:0">${esc([s.roll, s.batch].filter(Boolean).join(" · ") || "No profile details yet")} · active ${ago(s.at)}</p>
    <div class="pillrow">${s.cf ? `<a class="tag" href="https://codeforces.com/profile/${esc(s.cf)}" target="_blank" rel="noopener">Codeforces: ${esc(s.cf)}</a>` : ""}${s.lc ? `<a class="tag" href="https://leetcode.com/u/${esc(s.lc)}/" target="_blank" rel="noopener">LeetCode: ${esc(s.lc)}</a>` : ""}${s.cc ? `<a class="tag" href="https://www.codechef.com/users/${esc(s.cc)}" target="_blank" rel="noopener">CodeChef: ${esc(s.cc)}</a>` : ""}</div>
    ${scoreView(sc, s.st)}
    <div class="panel" style="margin:12px 0"><b>Progress by module</b>${mods.map(m => { const ps = D.problems.filter(p => lecById[p.lec].module === m), d = ps.filter(x => isDone(s.st[x.id])).length, pc = Math.round(d / ps.length * 100);
      return `<div class="mrow"><div><b>${esc(m)}</b><div class="track"><i style="width:${pc}%;background:${mcol(m)}"></i></div></div><div class="n">${d}/${ps.length}</div></div>`; }).join("")}</div>
    ${revisit.length ? `<div class="panel" style="margin:12px 0"><b>Marked to revisit (${revisit.length})</b>${revisit.slice(0, 12).map(p => `<div class="hard"><span>${esc(p.name)}</span><span class="n">L${p.lec}</span></div>`).join("")}</div>` : ""}
    <form class="panel" id="scform" data-uid="${esc(uid)}"><b>Enter scores (0-100)</b>
      <div class="sc">${D.contests.map((c, i) => `<label>${esc(c[0])}<input type="number" min="0" max="100" step="1" name="c${i + 1}" value="${val(sc.contests?.["c" + (i + 1)])}"></label>`).join("")}
      <label>Projects<input type="number" min="0" max="100" name="projects" value="${val(sc.projects)}"></label><label>Mock OA &amp; interviews<input type="number" min="0" max="100" name="mock" value="${val(sc.mock)}"></label></div>
      <div class="tools"><button class="btn pri" type="submit">Save scores</button></div></form>`;
  $("drawer").hidden = false; $("scrim").hidden = false; if (!keepFocus) $("dclose").focus();
}
// Re-render an open drawer with fresh data, unless a teacher is typing in its score form.
const refreshDrawer = () => { const f = $("scform"); if (!$("drawer").hidden && f && !f.contains(document.activeElement)) drawer(f.dataset.uid, true); };
const closeDrawer = () => { $("drawer").hidden = true; $("scrim").hidden = true; };

const all = () => { header(); lectures(); problems(); statics(); progress(); classView(); applyLang(); learn(); };
const VIEWS = ["learn","lectures","problems","projects","contests","placement","toolkit","progress","class","readiness"];
function route() {
  let v = VIEWS.includes(location.hash.slice(1)) ? location.hash.slice(1) : "learn";
  if ((v === "class" || v === "readiness") && !R.staff) v = "learn";
  VIEWS.forEach(x => $("v-" + x).classList.toggle("on", x === v));
  document.querySelectorAll("nav a").forEach(a => a.getAttribute("href") === "#" + v ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current"));
}

// ---------- remote sync ----------
function remoteBody() {
  const L = S.learn || {};
  return {st: S.st, lang: S.lang, prof: S.prof || {}, learn: {read: L.read || {}, chk: L.chk || {}, quiz: L.quiz || {}},
    read: Object.keys(L.read || {}).length, solved: D.problems.filter(done).length, updatedAt: new Date().toISOString()};
}
async function flush() {
  if (!R.ref || R.readOnly) return;
  if (R.saving) { R.dirty = true; return; }
  R.saving = true; setSync("busy", "Saving…");
  do {
    R.dirty = false;
    let ok = false;
    for (let attempt = 0; attempt < 2 && !ok; attempt++) {
      try { await R.ref.set(remoteBody()); ok = true; }
      catch (e) {
        if (e?.code === "invalid_argument") { R.readOnly = true; setSync("ro", "View-only access: progress saved in this browser"); R.saving = false; progress(); return; }
        if (e?.code === "quota_exceeded") { setSync("err", "Course database is full: tell your teacher"); R.saving = false; return; }
        if (attempt === 0 && (e?.code === "unavailable" || !e?.code)) await new Promise(r => setTimeout(r, 600 + Math.random() * 800));
        else { setSync("err", "Couldn't save to the course database: saved in this browser"); R.saving = false; return; }
      }
    }
  } while (R.dirty);
  R.saving = false; setSync("ok", R.staff ? "Synced · staff view on" : "Synced to the course database");
}
const schedule = () => { if (!R.ref) return; clearTimeout(R.timer); R.timer = setTimeout(flush, 500); };
function onMine(snap) {
  R.ready = true;
  if (snap.exists) {
    const d = snap.data() || {};
    if (!snap.metadata.hasPendingWrites && !R.saving && !R.dirty) {
      const remote = (typeof d.st === "object" && d.st) || {};
      let changed = false;
      const merged = {};
      for (const [k, v] of Object.entries(remote)) if (pById[k] && STAT.includes(v)) merged[k] = v;
      const first = !R.merged;
      if (first) { for (const [k, v] of Object.entries(S.st)) if (!merged[k] && pById[k]) { merged[k] = v; changed = true; } R.merged = true; }
      S.st = merged;
      const rp = (d.prof && typeof d.prof === "object") ? d.prof : {};
      if (first && !Object.keys(rp).length && Object.values(S.prof || {}).some(Boolean)) changed = true;
      else S.prof = {roll: String(rp.roll || "").slice(0, 30), batch: String(rp.batch || "").slice(0, 40), cf: handle(rp.cf), lc: handle(rp.lc), cc: handle(rp.cc)};
      if (d.lang === "cpp" || d.lang === "java") S.lang = d.lang;
      const rl = (d.learn && typeof d.learn === "object") ? d.learn : {};
      for (const f of ["read", "chk", "quiz"]) {
        const src = (rl[f] && typeof rl[f] === "object") ? rl[f] : {}, ok = {};
        for (const [k, v] of Object.entries(src)) if (typeof k === "string" && k.length < 60 && (v === 1 || v === "got" || v === "unsure")) ok[k] = v;
        if (first) { for (const [k, v] of Object.entries(S.learn[f] || {})) if (!(k in ok)) { ok[k] = v; changed = true; } }
        S.learn[f] = ok;
      }
      saveLocal(); header(); lectures(); problems(); statics(); progress(); applyLang(); if ($("v-learn").classList.contains("on")) learn();
      if (changed) schedule();
    }
  } else if (!R.merged) {
    // First visit while signed in: upload whatever this browser already has (nothing is written for an empty profile,
    // so staff who only browse don't show up as students).
    R.merged = true;
    if (Object.keys(S.st).length || Object.values(S.prof || {}).some(Boolean)) schedule();
  }
  if (!R.saving && !R.readOnly) setSync("ok", R.staff ? "Synced · staff view on" : "Synced to the course database");
}
async function connect() {
  const c = window.claude; if (!c?.use) return;
  setSync("busy", "Connecting to the course database…");
  const [db, user] = await Promise.all([c.use("db").catch(() => null), c.use("user").catch(() => null)]);
  if (!db || !user) { setSync("local", "Saved in this browser"); return; }
  const uid = await user.id().catch(() => null);
  if (!uid) { setSync("local", "Saved in this browser (sign in to sync)"); return; }
  Object.assign(R, {db, user, uid});
  R.staff = !!(await user.canEdit().catch(() => false));
  try { const ps = await user.profiles([uid]); R.names[uid] = ps?.[uid]?.name || ""; } catch (e) {}
  R.ref = db.doc("progress/" + uid);
  const slow = setTimeout(() => { if (!R.ready) setSync("err", "Can't reach the course database yet: saving in this browser"); }, 10000);
  R.ref.onSnapshot(s => { clearTimeout(slow); onMine(s); }, e => { clearTimeout(slow); setSync("err", "Lost connection to the course database: saving in this browser"); });
  db.doc("scores/" + uid).onSnapshot(s => { R.mine = s.exists ? s.data() : null; progress(); }, () => {});
  if (R.staff) {
    document.querySelectorAll(".staffonly").forEach(a => a.hidden = false);
    db.collection("progress").onSnapshot(async snap => {
      const next = {}; snap.docs.forEach(d => { next[d.id] = d.data(); }); R.all = next;
      const missing = Object.keys(next).filter(id => !(id in R.names));
      if (missing.length) { try { const ps = await user.profiles(missing); missing.forEach(id => { R.names[id] = ps?.[id]?.name || ""; }); } catch (e) {} }
      classView(); refreshDrawer();
    }, () => toast("Couldn't load class data"));
    db.collection("scores").onSnapshot(snap => { const next = {}; snap.docs.forEach(d => { next[d.id] = d.data(); }); R.scores = next; classView(); refreshDrawer(); }, () => {});
    route(); learn();
  }
  progress();
}

// ---------- events ----------
function setStatus(id, val) {
  if (!pById[id] || !STAT.includes(val)) return;
  if (val === "Not started") delete S.st[id]; else S.st[id] = val;
  saveLocal(); schedule(); header(); progress(); lectures(); if (location.hash === "#problems") problems(); if (location.hash === "#learn" || location.hash === "") learn();
}
function gotoLec(no) {
  open.add(no); modF = ""; $("lq").value = ""; lectures();
  if (location.hash !== "#lectures") location.hash = "lectures"; route();
  requestAnimationFrame(() => $("lec-" + no)?.scrollIntoView({behavior: "smooth", block: "start"}));
}
document.addEventListener("change", e => { const id = e.target.dataset?.id; if (id) { setStatus(id, e.target.value); toast(`${id}: ${e.target.value}`); } });
document.addEventListener("click", e => {
  const t = e.target.closest("[data-tog]"); if (t) { const id = t.dataset.tog, on = isDone(S.st[id]); setStatus(id, on ? "Not started" : "Solved"); toast(on ? "Marked as not started" : "Nice, marked solved"); return; }
  const s = e.target.closest("[data-stu]"); if (s) { drawer(s.dataset.stu); return; }
  const nt = e.target.closest("[data-notes]"); if (nt) { const [m, k] = lecMod[+nt.dataset.notes]; jump(m, k); return; }
  const g = e.target.closest("[data-goto],[data-lec]"); if (g) { gotoLec(+(g.dataset.goto || g.dataset.lec)); return; }
  const c = e.target.closest("[data-mod]"); if (c) { modF = c.dataset.mod; lectures(); }
});
$("leclist").addEventListener("toggle", e => { const n = +e.target.dataset.no; if (!n) return; e.target.open ? open.add(n) : open.delete(n); }, true);
$("expand").addEventListener("click", () => { const anyClosed = [...document.querySelectorAll("#leclist details")].some(d => !d.open);
  document.querySelectorAll("#leclist details").forEach(d => { d.open = anyClosed; const n = +d.dataset.no; anyClosed ? open.add(n) : open.delete(n); }); $("expand").textContent = anyClosed ? "Collapse all" : "Expand all"; });
$("lq").addEventListener("input", lectures);
["pq","pf-plat","pf-diff","pf-typ","pf-mod","pf-st"].forEach(id => $(id).addEventListener("input", problems));
$("pf-reset").addEventListener("click", () => { ["pq","pf-plat","pf-diff","pf-typ","pf-mod","pf-st"].forEach(id => $(id).value = ""); problems(); });
["cq","cb","cs"].forEach(id => $(id).addEventListener("input", classView));
["rb","rmin","rpct","rcf"].forEach(id => $(id).addEventListener("input", readinessView));
$("rexp").addEventListener("click", exportCsv);
$("l-cpp").addEventListener("click", () => { S.lang = "cpp"; saveLocal(); schedule(); statics(); lectures(); applyLang(); toast("Showing the C++ track"); });
$("l-java").addEventListener("click", () => { S.lang = "java"; saveLocal(); schedule(); statics(); lectures(); applyLang(); toast("Showing the Java track"); });
$("pform").addEventListener("submit", e => { e.preventDefault();
  S.prof = {roll: $("f-roll").value.trim().slice(0, 30), batch: $("f-batch").value.trim().slice(0, 40), cf: handle($("f-cf").value), lc: handle($("f-lc").value), cc: handle($("f-cc").value)};
  saveLocal(); schedule(); progress(); toast("Profile saved"); });
$("dbody").addEventListener("submit", async e => {
  if (e.target.id !== "scform") return; e.preventDefault();
  const fd = new FormData(e.target), uid = e.target.dataset.uid, contests = {};
  D.contests.forEach((c, i) => { const v = num(fd.get("c" + (i + 1)) === "" ? NaN : fd.get("c" + (i + 1))); if (v !== null) contests["c" + (i + 1)] = v; });
  const body = {contests, updatedAt: new Date().toISOString(), by: R.uid};
  const pj = num(fd.get("projects") === "" ? NaN : fd.get("projects")), mk = num(fd.get("mock") === "" ? NaN : fd.get("mock"));
  if (pj !== null) body.projects = pj; if (mk !== null) body.mock = mk;
  try { await R.db.doc("scores/" + uid).set(body); R.scores[uid] = body; document.activeElement?.blur(); refreshDrawer(); classView(); toast("Scores saved"); } catch (err) { toast(err?.code === "invalid_argument" ? "You don't have permission to enter scores" : "Couldn't save scores, try again"); }
});
$("dclose").addEventListener("click", closeDrawer); $("scrim").addEventListener("click", closeDrawer);
document.addEventListener("keydown", e => {
  if (e.key === "Escape" && !$("drawer").hidden) { closeDrawer(); return; }
  if (e.key === "/" && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) { e.preventDefault(); location.hash = "problems"; route(); $("pq").focus(); }
});
$("copy").addEventListener("click", async () => { try { await navigator.clipboard.writeText($("code").value); toast("Code copied"); } catch (e) { $("code").select(); toast("Select the code and copy it"); } });
$("load").addEventListener("click", () => { try { const v = JSON.parse(atob($("code").value.trim())); if (typeof v !== "object" || !v || Array.isArray(v)) throw 0; const ok = {}; for (const [k, s] of Object.entries(v)) if (pById[k] && STAT.includes(s)) ok[k] = s; S.st = ok; saveLocal(); schedule(); all(); toast(`Loaded ${Object.keys(ok).length} entries`); } catch (e) { toast("That code could not be read"); } });
let armed = false;
$("reset").addEventListener("click", () => { if (!armed) { armed = true; $("reset").textContent = "Click again to confirm"; setTimeout(() => { armed = false; $("reset").textContent = "Reset"; }, 4000); return; } armed = false; S.st = {}; saveLocal(); schedule(); all(); $("reset").textContent = "Reset"; toast("Progress cleared"); });
__LEARNJS__
window.addEventListener("hashchange", () => { route(); if (location.hash === "#learn") learn(); });
once(); all(); route();
connect();
}
