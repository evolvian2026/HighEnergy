// ---------- Learn: the module handbooks, interactive ----------
// LN = student handbooks (bundled). Teacher guides are read from the database (teacher/M<n>), staff only.
const LN = __LEARN__;
const LV = {mode: "student", open: new Set(), teach: {}, tload: {}, q: ""};
S.learn = Object.assign({mod: LN[0].id, tab: {}, read: {}, chk: {}, quiz: {}, ans: {}}, S.learn || {});
const lmod = id => LN.find(m => m.id === id) || LN[0];
const lblocks = m => m.tabs.flatMap(t => t.blocks);
const lpct = m => { const b = lblocks(m); return b.length ? b.filter(x => S.learn.read[x.id]).length / b.length : 0; };
const lecMod = Object.fromEntries(LN.flatMap(m => m.tabs.filter(t => t.lec).map(t => [t.lec, [m.id, t.key]])));
const stripTags = h => String(h).replace(/<[^>]+>/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/\s+/g, " ");
const lsave = () => { saveLocal(); schedule(); };
const BOOK = `<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/></svg>`;

function curDoc() {
  const m = lmod(S.learn.mod);
  if (LV.mode === "teacher" && R.staff) { const t = LV.teach[m.id]; return t ? {id: m.id, name: m.name, title: t.title, intro: t.intro, tabs: t.tabs, teacher: true} : null; }
  return m;
}
function curTab(doc) {
  const want = S.learn.tab[doc.id + (doc.teacher ? "t" : "")];
  return doc.tabs.find(t => t.key === want) || doc.tabs.find(t => t.blocks.length || t.lead) || doc.tabs[0];
}

function learnRail() {
  $("lrail").innerHTML = LN.map(m => { const p = Math.round(lpct(m) * 100);
    return `<button class="lmod${m.id === S.learn.mod ? " on" : ""}" data-lmod="${m.id}" aria-current="${m.id === S.learn.mod}" style="--mc:${mcol(m.name)}">
      <span class="lm-n">${esc(m.id)}</span><span class="lm-t">${esc(m.name.replace(/^M\d+ /, ""))}</span>
      <span class="lm-p" title="${p}% of sections read"><i style="width:${p}%"></i></span></button>`; }).join("");
  $("lsel").innerHTML = LN.map(m => `<option value="${m.id}"${m.id === S.learn.mod ? " selected" : ""}>${esc(m.name)} (${Math.round(lpct(m) * 100)}% read)</option>`).join("");
}

function blockHtml(b, doc) {
  const isRead = !doc.teacher && !!S.learn.read[b.id];
  let inner = "";
  if (b.kind === "quiz") {
    inner = `<p class="h2sub small">${doc.teacher ? "Model answers for the recap quiz." : "Answer each question in your own words, then rate yourself. Your written answers are saved on this device; your ratings sync with your progress."}</p><ol class="quiz">${b.qs.map((q, i) => {
      const k = b.id + "-" + i, r = S.learn.quiz[k] || "";
      return `<li class="qcard${r ? " r-" + r : ""}"><div class="qq">${q.q}</div>${doc.teacher ? (q.a ? `<details class="qa"><summary>Show answer</summary><div>${q.a}</div></details>` : "")
        : `<textarea class="qans" data-ans="${esc(k)}" rows="2" maxlength="600" placeholder="Your answer…" aria-label="Your answer to question ${i + 1}">${esc(S.learn.ans[k] || "")}</textarea>
        <div class="qrate" role="group" aria-label="How did you do?"><button class="qb" data-quiz="${esc(k)}" data-v="got" aria-pressed="${r === "got"}">I know this</button><button class="qb" data-quiz="${esc(k)}" data-v="unsure" aria-pressed="${r === "unsure"}">Need to review</button></div>`}</li>`; }).join("")}</ol>`;
  } else if (b.kind === "practice") {
    inner = (b.html || "") + `<div class="plist">${b.rows.map(r => { const p = pById[r.pid];
      const row = p ? prow(p, r.lec !== curTab(doc).lec) : `<div class="prow"><span></span><div class="pname"><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.name)}</a></div></div>`;
      return r.hint ? row.replace(/<\/div>\s*<select/, `<details class="hint"><summary>Hint</summary><div>${r.hint}</div></details></div><select`) : row; }).join("")}</div>`;
  } else inner = b.html;
  const tail = doc.teacher ? "" : `<div class="bfoot"><button class="btn${isRead ? "" : " pri"}" data-read="${esc(b.id)}">${isRead ? "Mark as unread" : "Mark as read & continue"}</button></div>`;
  return `<details class="lblk k-${b.kind}${isRead ? " read" : ""}" data-blk="${esc(b.id)}"${LV.open.has(b.id) ? " open" : ""}>
    <summary><span class="lb-dot" aria-hidden="true">${isRead ? CHECK : ""}</span><span class="lb-t">${esc(b.title)}</span>
      ${b.kind === "quiz" ? `<span class="tag">Self-check · ${b.qs.length}</span>` : b.kind === "practice" ? `<span class="tag">${b.rows.length} problems</span>` : ""}
      <svg class="chev" viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg></summary>
    <div class="lb-body">${inner}${tail}</div></details>`;
}

function learn() {
  learnRail();
  const sm = lmod(S.learn.mod);
  $("lmode").hidden = !R.staff;
  $("lm-s").setAttribute("aria-pressed", LV.mode === "student"); $("lm-t").setAttribute("aria-pressed", LV.mode === "teacher");
  const doc = curDoc();
  if (!doc) {
    $("lhead").innerHTML = `<h2>${esc(sm.name)}</h2>`; $("ltabs").innerHTML = "";
    $("lpanel").innerHTML = `<div class="empty">${LV.tload[sm.id] === "missing" ? "No teacher guide has been added for this module yet." : LV.tload[sm.id] === "error" ? "Couldn't load the teacher guide. Check your connection and try again." : "Loading the teacher guide…"}</div>`;
    loadTeacher(sm.id); return;
  }
  const p = lpct(sm), nb = lblocks(sm).length, nr = Math.round(p * nb);
  $("lhead").innerHTML = `<div class="lh-top"><div><span class="eyebrow dark">${doc.teacher ? "Teacher guide · staff only" : "Student handbook"}</span><h2>${esc(doc.title.replace(/:.*$/, ""))}</h2></div>
    ${doc.teacher ? "" : `<div class="lh-prog"><div class="track"><i style="width:${p * 100}%;background:${mcol(sm.name)}"></i></div><span>${nr} of ${nb} sections read</span></div>`}</div>${doc.intro ? `<div class="lintro">${doc.intro}</div>` : ""}`;
  const tab = curTab(doc);
  $("ltabs").innerHTML = doc.tabs.map(t => { const bl = t.blocks, rd = bl.filter(b => S.learn.read[b.id]).length;
    return `<button role="tab" id="lt-${esc(t.key)}" aria-controls="lpanel" aria-selected="${t === tab}" tabindex="${t === tab ? 0 : -1}" data-ltab="${esc(t.key)}">
      ${t.lec ? `<b>L${t.lec}</b>` : ""}<span>${esc(t.label)}</span>${!doc.teacher && bl.length ? `<i class="tp${rd === bl.length ? " full" : ""}">${rd}/${bl.length}</i>` : ""}</button>`; }).join("");
  $("lpanel").setAttribute("aria-labelledby", "lt-" + tab.key);
  const lecRow = tab.lec && !doc.teacher ? (() => { const ps = byLec[tab.lec] || [], d = ps.filter(done).length;
    return `<div class="lctx"><span>Lecture ${tab.lec} · Week ${Math.ceil(tab.lec / 2)} · ${d}/${ps.length} problems solved</span><button class="lnk" data-goto="${tab.lec}">Open in lecture plan</button></div>`; })() : "";
  const ids = tab.blocks.map(b => b.id);
  $("lpanel").innerHTML = lecRow + (tab.lead ? `<div class="lintro">${tab.lead}</div>` : "")
    + (tab.blocks.length ? `<div class="ltools"><button class="lnk" data-lall="1">${ids.every(i => LV.open.has(i)) ? "Collapse all sections" : "Expand all sections"}</button></div>` : "")
    + `<div class="lblks">${tab.blocks.map(b => blockHtml(b, doc)).join("")}</div>`
    + (() => { const i = doc.tabs.indexOf(tab), nx = doc.tabs[i + 1], mi = LN.findIndex(m => m.id === sm.id), nm = LN[mi + 1];
      return `<div class="lnext">${nx ? `<button class="btn" data-ltab="${esc(nx.key)}">Next: ${nx.lec ? "Lecture " + nx.lec : esc(nx.label)} →</button>` : nm && !doc.teacher ? `<button class="btn" data-lmod="${nm.id}">Next module: ${esc(nm.name)} →</button>` : ""}</div>`; })();
  applyChecks();
}
function applyChecks() {
  document.querySelectorAll("#v-learn [data-chk]").forEach(c => { c.checked = !!S.learn.chk[c.dataset.chk]; });
}
// Teacher guides are stored gzip-compressed and base64-encoded ({z}) to keep the documents small.
async function gunzipJson(b64) {
  const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
  const txt = await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"))).text();
  return JSON.parse(txt);
}
async function loadTeacher(mid) {
  if (!R.db || LV.tload[mid] === "busy" || LV.tload[mid] === "missing") return;
  LV.tload[mid] = "busy";
  try {
    const s = await R.db.doc("teacher/" + mid).get();
    let d = s.exists ? s.data() : null;
    if (d && typeof d.z === "string") d = await gunzipJson(d.z);
    if (d && Array.isArray(d.tabs)) { LV.teach[mid] = d; LV.tload[mid] = "ok"; } else LV.tload[mid] = "missing";
  } catch (e) { LV.tload[mid] = "error"; }
  if ($("v-learn").classList.contains("on") && S.learn.mod === mid && LV.mode === "teacher") learn();
}

function learnSearch() {
  const q = $("lsq").value.trim().toLowerCase(); LV.q = q;
  if (q.length < 2) { $("lsres").hidden = true; $("lsres").innerHTML = ""; return; }
  const hits = [];
  for (const m of LN) for (const t of m.tabs) for (const b of t.blocks) {
    const txt = (b.title + " " + stripTags(b.html || "") + " " + (b.qs || []).map(x => stripTags(x.q)).join(" ") + " " + (b.rows || []).map(r => r.name).join(" ")).toLowerCase();
    const at = txt.indexOf(q); if (at < 0) continue;
    const src = txt.slice(Math.max(0, at - 50), at + q.length + 70);
    hits.push({m, t, b, snip: src}); if (hits.length >= 30) break;
  }
  $("lsres").hidden = false;
  $("lsres").innerHTML = hits.length ? hits.map(h => `<button class="lsr" data-jump="${esc(h.m.id)}|${esc(h.t.key)}|${esc(h.b.id)}"><b>${esc(h.b.title)}</b><span>${esc(h.m.id)} · ${h.t.lec ? "Lecture " + h.t.lec : esc(h.t.label)}</span><em>…${esc(h.snip)}…</em></button>`).join("")
    : `<div class="h2sub small" style="padding:10px 14px">Nothing in the handbooks matches “${esc(q)}”.</div>`;
}
function jump(mid, key, bid) {
  S.learn.mod = mid; S.learn.tab[mid] = key; LV.mode = "student"; if (bid) LV.open.add(bid); saveLocal();
  if (location.hash !== "#learn") location.hash = "learn"; route(); learn();
  $("lsres").hidden = true;
  requestAnimationFrame(() => { const el = bid ? document.querySelector(`[data-blk="${CSS.escape(bid)}"]`) : $("ltabs"); el?.scrollIntoView({behavior: "smooth", block: "start"}); });
}

$("v-learn").addEventListener("click", async e => {
  const t = e.target;
  const mo = t.closest("[data-lmod]"); if (mo) { S.learn.mod = mo.dataset.lmod; LV.open.clear(); saveLocal(); learn(); toTop(); return; }
  const tb = t.closest("[data-ltab]"); if (tb) { const d = curDoc(); if (!d) return; S.learn.tab[d.id + (d.teacher ? "t" : "")] = tb.dataset.ltab; saveLocal(); learn(); $("lt-" + tb.dataset.ltab)?.focus(); if (tb.closest(".lnext")) toTop(); return; }
  const rd = t.closest("[data-read]"); if (rd) {
    const id = rd.dataset.read, was = !!S.learn.read[id];
    if (was) delete S.learn.read[id]; else S.learn.read[id] = 1;
    LV.open.delete(id);
    if (!was) { const all = [...document.querySelectorAll("#lpanel [data-blk]")].map(x => x.dataset.blk), nx = all[all.indexOf(id) + 1]; if (nx && !S.learn.read[nx]) LV.open.add(nx); }
    lsave(); learn();
    const nxt = !was && [...LV.open].pop(); const el = document.querySelector(`[data-blk="${CSS.escape(nxt || id)}"]`); el?.scrollIntoView({behavior: "smooth", block: "nearest"});
    toast(was ? "Marked as unread" : "Section read"); return;
  }
  const qb = t.closest("[data-quiz]"); if (qb) { const k = qb.dataset.quiz; S.learn.quiz[k] = S.learn.quiz[k] === qb.dataset.v ? "" : qb.dataset.v; if (!S.learn.quiz[k]) delete S.learn.quiz[k]; lsave();
    const li = qb.closest(".qcard"); li.className = "qcard" + (S.learn.quiz[k] ? " r-" + S.learn.quiz[k] : ""); li.querySelectorAll(".qb").forEach(b => b.setAttribute("aria-pressed", b.dataset.v === S.learn.quiz[k])); return; }
  const cl = t.closest("[data-clang]"); if (cl) { S.lang = cl.dataset.clang; saveLocal(); schedule(); statics(); lectures(); applyLang(); toast(S.lang === "cpp" ? "Showing C++ code" : "Showing Java code"); return; }
  const cp = t.closest(".ccopy"); if (cp) { const box = cp.closest(".codeswap,.codeone"), pre = box.querySelector(box.classList.contains("codeswap") ? `pre[data-lang="${S.lang}"]` : "pre");
    try { await navigator.clipboard.writeText(pre.innerText); toast("Code copied"); } catch (err) { const r = document.createRange(); r.selectNodeContents(pre); getSelection().removeAllRanges(); getSelection().addRange(r); toast("Code selected: press Ctrl+C"); } return; }
  const all = t.closest("[data-lall]"); if (all) { const ids = [...document.querySelectorAll("#lpanel [data-blk]")].map(x => x.dataset.blk), openAll = !ids.every(i => LV.open.has(i)); ids.forEach(i => openAll ? LV.open.add(i) : LV.open.delete(i)); learn(); return; }
  const jp = t.closest("[data-jump]"); if (jp) { const [a, b2, c] = jp.dataset.jump.split("|"); $("lsq").value = ""; jump(a, b2, c); return; }
  const ms = t.closest("[data-lmode]"); if (ms) { LV.mode = ms.dataset.lmode; learn(); return; }
});
$("v-learn").addEventListener("toggle", e => { const id = e.target.dataset?.blk; if (!id) return; e.target.open ? LV.open.add(id) : LV.open.delete(id); }, true);
$("v-learn").addEventListener("change", e => {
  const c = e.target.dataset?.chk; if (c) { if (e.target.checked) S.learn.chk[c] = 1; else delete S.learn.chk[c]; lsave(); toast(e.target.checked ? "Checked off" : "Unchecked"); }
});
let ansT; $("v-learn").addEventListener("input", e => { const k = e.target.dataset?.ans; if (!k) return; const v = e.target.value.slice(0, 600); if (v) S.learn.ans[k] = v; else delete S.learn.ans[k]; clearTimeout(ansT); ansT = setTimeout(saveLocal, 400); });
$("ltabs").addEventListener("keydown", e => {
  if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(e.key)) return;
  const tabs = [...$("ltabs").querySelectorAll("[role=tab]")], i = tabs.indexOf(document.activeElement); if (i < 0) return;
  const j = e.key === "Home" ? 0 : e.key === "End" ? tabs.length - 1 : (i + (e.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
  e.preventDefault(); tabs[j].click();
});
$("lsel").addEventListener("change", e => { S.learn.mod = e.target.value; LV.open.clear(); saveLocal(); learn(); toTop(); });
function toTop() { const r = $("v-learn").getBoundingClientRect(); if (r.top < 70) $("v-learn").scrollIntoView({block: "start"}); }
$("lsq").addEventListener("input", learnSearch);
$("lsq").addEventListener("focus", () => { const r = $("lsq").getBoundingClientRect(); if (r.top > innerHeight * 0.45 && innerWidth > 980) $("v-learn").scrollIntoView({block: "start"}); });
document.addEventListener("click", e => { if (!e.target.closest(".lsearch")) $("lsres").hidden = true; });
function applyLang() { document.documentElement.dataset.code = S.lang; }
