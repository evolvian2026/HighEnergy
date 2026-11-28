"""Turn the module handbooks (course/content/M*-student.md / M*-teacher.md) into portal data.

Usage:  python portal/build_learn.py

Writes:
  portal/learn.json    student handbooks, bundled into both portal builds
  portal/teacher.json  teacher guides, NOT bundled; uploaded to the artifact's database
                       (teacher/M<n>, admin-only) so only staff can read them

Each module becomes {id, title, intro, tabs:[{key, label, lec, blocks:[...]}]}.
A block is one ### section: {id, title, kind, html} where kind is
  "text"     rendered HTML (C++/Java code pairs become a language-switching block)
  "quiz"     {qs:[...]}   self-check questions
  "practice" {rows:[{name,url,typ,level,hint,lec}]}  linked to the problem bank by URL
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "course/content"

ESC_RE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!|<>~^$=])")


def inline(s: str) -> str:
    """Markdown inline -> HTML. Code spans first, then escapes, links, bold, italics."""
    out, parts = [], re.split(r"(`[^`]+`)", s)
    for p in parts:
        if len(p) > 1 and p.startswith("`") and p.endswith("`"):
            out.append("<code>" + html.escape(p[1:-1]) + "</code>")
            continue
        holds = []

        def hold(x):
            holds.append(x)
            return f"\x00{len(holds) - 1}\x00"

        p = ESC_RE.sub(lambda m: hold(html.escape(m.group(1))), p)
        p = html.escape(p, quote=False)

        def link(m):
            text, url = m.group(1), html.unescape(m.group(2))
            if not url.startswith("https://"):
                return text
            return f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{text}</a>'

        p = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, p)
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", p)
        p = re.sub(r"\x00(\d+)\x00", lambda m: holds[int(m.group(1))], p)
        out.append(p)
    return "".join(out)


def tex(src: str) -> str:
    """Very small LaTeX -> HTML for the handful of formula blocks in the handbooks."""
    t = src
    t = re.sub(r"\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}",
               lambda m: "[" + " ; ".join(r.strip().replace("&", " ") for r in m.group(1).split("\\\\")) + "]", t)
    for a, b in [("\\iff", "⇔"), ("\\ne", "≠"), ("\\min", "min"), ("\\max", "max"), ("\\big", ""),
                 ("\\,", " "), ("\\;", " ")]:
        t = t.replace(a, b)
    t = re.sub(r"\\text\{([^}]*)\}", r"\1", t)
    t = html.escape(t, quote=False)
    t = re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", t)
    t = re.sub(r"_([A-Za-z0-9])", r"<sub>\1</sub>", t)
    return re.sub(r"\s+", " ", t).strip()


def plain(s: str) -> str:
    return re.sub(r"<[^>]+>", "", html.unescape(inline(s)))


def split_row(line: str):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    cells, cur, i = [], "", 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cur += "\\|"
            i += 2
            continue
        if line[i] == "|":
            cells.append(cur.strip())
            cur = ""
        else:
            cur += line[i]
        i += 1
    cells.append(cur.strip())
    return cells


def blocks_to_html(lines, check_prefix):
    """Block-level markdown -> HTML string. Returns (html, n_checkboxes)."""
    out, i, n, nchk = [], 0, len(lines), 0
    para = []

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(x.strip() for x in para)) + "</p>")
            para.clear()

    while i < n:
        ln = lines[i]
        s = ln.strip()
        if not s:
            flush_para()
            i += 1
            continue
        if s.startswith("```"):
            flush_para()
            codes = []
            while i < n and lines[i].strip().startswith("```"):
                lang = lines[i].strip()[3:].strip() or "text"
                i += 1
                body = []
                while i < n and not lines[i].strip().startswith("```"):
                    body.append(lines[i])
                    i += 1
                i += 1  # closing fence
                codes.append((lang, "\n".join(body)))
                j = i
                while j < n and not lines[j].strip():
                    j += 1
                if j < n and lines[j].strip().startswith("```") and lang in ("cpp", "java"):
                    nxt = lines[j].strip()[3:].strip()
                    if nxt in ("cpp", "java") and nxt != lang and len(codes) == 1:
                        i = j
                        continue
                break
            langs = {l for l, _ in codes}
            if langs == {"cpp", "java"}:
                pres = "".join(
                    f'<pre class="code" data-lang="{l}"><code>{html.escape(c)}</code></pre>' for l, c in codes)
                out.append(f'<div class="codeswap"><div class="cbar"><span class="cl" role="group" aria-label="Code language"><button type="button" data-clang="cpp">C++</button><button type="button" data-clang="java">Java</button></span>'
                           f'<button class="ccopy" type="button">Copy</button></div>{pres}</div>')
            else:
                for l, c in codes:
                    cls = "math" if l == "latex" else "code"
                    label = {"cpp": "C++", "java": "Java", "latex": "Formula", "bash": "Terminal"}.get(l, "")
                    bar = (f'<div class="cbar"><span>{label}</span><button class="ccopy" type="button">Copy</button></div>'
                           if cls == "code" else "")
                    inner = tex(c) if cls == "math" else html.escape(c)
                    out.append(f'<div class="codeone" data-lang="{l}">{bar}<pre class="{cls}"><code>{inner}</code></pre></div>')
            continue
        if s.startswith("|"):
            flush_para()
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            head = rows[0]
            body = [r for r in rows[1:] if not all(re.fullmatch(r":?-{3,}:?", c) for c in r)]
            has_head = any(c for c in head)
            th = "".join(f"<th>{inline(c)}</th>" for c in head) if has_head else ""
            trs = "".join(
                "<tr>" + "".join(f'<td data-l="{html.escape(plain(head[k]) if k < len(head) else "")}">{inline(c)}</td>'
                                 for k, c in enumerate(r)) + "</tr>" for r in body)
            out.append(f'<div class="tbl scroll"><table class="stack">{"<thead><tr>" + th + "</tr></thead>" if has_head else ""}<tbody>{trs}</tbody></table></div>')
            continue
        m_ul = re.match(r"^[-*] (.*)", s)
        m_ol = re.match(r"^(\d+)\. (.*)", s)
        if m_ul or m_ol:
            flush_para()
            ordered = bool(m_ol)
            items = []
            while i < n:
                t = lines[i].strip()
                mu, mo = re.match(r"^[-*] (.*)", t), re.match(r"^(\d+)\. (.*)", t)
                if ordered and mo:
                    items.append(mo.group(2))
                elif not ordered and mu:
                    items.append(mu.group(1))
                elif t and lines[i].startswith(("  ", "\t")) and items:
                    items[-1] += " " + t
                else:
                    break
                i += 1
            lis = []
            for it in items:
                mc = re.match(r"^\[( |x)\] (.*)", it)
                if mc and not ordered:
                    key = f"{check_prefix}-{nchk}"
                    nchk += 1
                    lis.append(f'<li class="task"><label><input type="checkbox" data-chk="{key}"> <span>{inline(mc.group(2))}</span></label></li>')
                else:
                    lis.append(f"<li>{inline(it)}</li>")
            tag = "ol" if ordered else "ul"
            cls = ' class="tasks"' if any("task" in x for x in lis) else ""
            out.append(f"<{tag}{cls}>{''.join(lis)}</{tag}>")
            continue
        para.append(ln)
        i += 1
    flush_para()
    return "".join(out), nchk


def parse_quiz(lines, with_answers):
    qs = []
    for ln in lines:
        m = re.match(r"^\s*\d+\. (.*)", ln)
        if not m:
            continue
        q = m.group(1).strip()
        if with_answers:
            ma = re.match(r"^(.*?)\s*\*\*(.+)\*\*\s*$", q)
            if ma:
                qs.append({"q": inline(ma.group(1)), "a": inline(ma.group(2))})
                continue
        qs.append({"q": inline(q)})
    return qs


def parse_practice(lines, lec):
    rows = [split_row(l) for l in lines if l.strip().startswith("|")]
    if not rows:
        return None
    head = [plain(c).lower() for c in rows[0]]
    if not head or head[0] != "problem":
        return None
    idx = {h: k for k, h in enumerate(head)}
    out = []
    for r in rows[1:]:
        if all(re.fullmatch(r":?-{3,}:?", c) for c in r):
            continue
        cell = r[0]
        m = re.match(r"^\[(.+?)\]\((https://[^)\s]+)\)", cell)
        get = lambda k: r[idx[k]] if k in idx and idx[k] < len(r) else ""
        out.append({
            "name": plain(m.group(1)) if m else plain(cell),
            "url": m.group(2) if m else "",
            "typ": plain(get("type")),
            "level": plain(get("level")),
            "hint": inline(get("hint") or get("hint after the contest")),
            "lec": int(get("lecture")) if get("lecture").isdigit() else lec,
        })
    return out


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


def parse_doc(path, mid, teacher):
    lines = path.read_text(encoding="utf-8").split("\n")
    title = lines[0].lstrip("# ").strip()
    body = [l for k, l in enumerate(lines[1:], 1) if not (k <= 3 and re.match(r"^\w{3} \d+, \d{4} ·", l.strip()))]
    tabs, intro, cur, sec = [], [], None, None
    for ln in body:
        if ln.startswith("## "):
            h = ln[3:].strip()
            m = re.match(r"^Lecture (\d+): (.*)", h)
            cur = {"key": f"L{m.group(1)}" if m else slug(h), "label": h if not m else m.group(2),
                   "lec": int(m.group(1)) if m else None, "head": h, "secs": []}
            tabs.append(cur)
            sec = None
            continue
        if ln.startswith("### ") and cur is not None:
            sec = {"title": ln[4:].strip(), "lines": []}
            cur["secs"].append(sec)
            continue
        if cur is None:
            intro.append(ln)
        elif sec is None:
            cur.setdefault("lead", []).append(ln)
        else:
            sec["lines"].append(ln)

    res_tabs = []
    for t in tabs:
        blocks = []
        lead_html, _ = blocks_to_html(t.get("lead", []), f"{mid}-{t['key']}-lead")
        for k, s in enumerate(t["secs"]):
            bid = f"{mid}-{t['key']}-{k}"
            ttl = s["title"]
            low = ttl.lower()
            if low.startswith("quiz") or low.startswith("recap quiz"):
                qs = parse_quiz(s["lines"], teacher)
                if qs:
                    blocks.append({"id": bid, "title": plain(ttl), "kind": "quiz", "qs": qs})
                    continue
            if not teacher and ("practice" in low or low.startswith("contest problems") or "set" in low.split()):
                rows = parse_practice(s["lines"], t["lec"])
                if rows:
                    pre = [l for l in s["lines"] if not l.strip().startswith("|")]
                    note, _ = blocks_to_html(pre, bid)
                    blocks.append({"id": bid, "title": plain(ttl), "kind": "practice", "rows": rows, "html": note})
                    continue
            h, _ = blocks_to_html(s["lines"], bid)
            blocks.append({"id": bid, "title": plain(ttl), "kind": "text", "html": h})
        res_tabs.append({"key": t["key"], "label": plain(t["label"]), "head": plain(t["head"]), "lec": t["lec"],
                         "lead": lead_html, "blocks": blocks})
    intro_html, _ = blocks_to_html(intro, f"{mid}-intro")
    return {"title": title, "intro": intro_html, "tabs": res_tabs}


def main():
    data = json.loads((ROOT / "portal/data.json").read_text(encoding="utf-8"))
    mod_names = []
    for l in data["lectures"]:
        if l["module"] not in mod_names:
            mod_names.append(l["module"])
    by_url = {}
    for p in data["problems"]:
        by_url.setdefault(p["url"].rstrip("/"), p["id"])

    learn, teach, stats = [], {}, {"blocks": 0, "linked": 0, "rows": 0}
    for k, name in enumerate(mod_names):
        mid = f"M{k}"
        s = parse_doc(SRC / f"{mid}-student.md", mid, False)
        for t in s["tabs"]:
            for b in t["blocks"]:
                stats["blocks"] += 1
                for r in b.get("rows", []):
                    stats["rows"] += 1
                    r["pid"] = by_url.get(r["url"].rstrip("/"), "")
                    stats["linked"] += bool(r["pid"])
        learn.append({"id": mid, "name": name, "title": s["title"], "intro": s["intro"], "tabs": s["tabs"]})
        tp = SRC / f"{mid}-teacher.md"
        if tp.exists():
            teach[mid] = parse_doc(tp, mid + "t", True)
    (ROOT / "portal/learn.json").write_text(json.dumps(learn, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (ROOT / "portal/teacher.json").write_text(json.dumps(teach, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"learn.json: {len(learn)} modules, {stats['blocks']} sections, practice rows {stats['rows']} "
          f"({stats['linked']} linked to the problem bank)")
    for m, t in teach.items():
        print(f"  teacher {m}: {len(json.dumps(t, ensure_ascii=False).encode()) // 1024} KB")


if __name__ == "__main__":
    main()
