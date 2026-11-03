#!/usr/bin/env python3
"""Script Pack: one script (or a season of episodes) -> every document each recipient needs.

Two steps, because the facts are counted by code and the prose is written by Claude (or the GPT):

  1) facts   python3 pack.py facts ep*.fountain --out pack/
             -> pack/facts.md + facts.json: scenes, synopsis lines, characters (scenes, lines,
                words, episodes, age and intro line from the action), pages, runtime, locations.
             Claude reads facts.md + the script and writes pack/pack.md (format: references/pack.md).

  2) build   python3 pack.py build ep*.fountain --texts pack/pack.md --out pack/ [--preset sundance_feature]
             -> 00 <title> — contents.pdf       cover + who gets what
                01 ՊՐՈԴՅՈՒՍԵՐ · Producer         one-pager (always 1 page), synopsis
                02 ՊԼԱՏՖՈՐՄ · Platform           pitch deck / series bible (16:9), episode synopses
                03 ՌԵԺԻՍՈՐ · Director             script PDF/DOCX/FDX, scene overview
                04 ԼԱՅՆ-ՊՐՈԴՅՈՒՍԵՐ · Line Producer production breakdown, scenes CSV, season CSV
                05 ԿԱՍՏԻՆԳ-ԴԻՐԵԿՏՈՐ · Casting Dir. casting breakdown, CSV
                06 ԴԵՐԱՍԱՆՆԵՐ · Actors            sides per role (branded cover + real scenes)
                07 ՄԻՋԱԶԳԱՅԻՆ · International     English one-pager
                08 ՄՐՑՈՒՅԹ-ՖՈՆԴ · Competition     application per preset, word counts shown
                _internal (do not send)/          CHECK.md, HTML sources, breakdown md
             Design: pack_design.py (HTML/CSS -> PDF via headless Chromium, Noto Serif/Sans Armenian).

Only facts from the script go into numbers; nothing is invented. Sides are cut from the real scenes.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import screenplay as sp  # noqa: E402

# Limits from real submission rules (research 2026-11-03, see references/pack.md for sources).
PRESETS = {
    "sundance_feature": {"name": "Sundance Feature Film Program",
                         "limits": {"logline": 75, "synopsis_page": 750, "bio": 150},
                         "max_bios": 3, "docs": ["logline", "synopsis_page", "characters"], "en": True},
    "sundance_microseries": {"name": "Sundance Collab Micro-Series",
                             "limits": {"logline": 75, "synopsis_page": 500},
                             "docs": ["logline", "synopsis_page", "world", "episodes"], "en": True},
    "eurimages": {"name": "Eurimages co-production (synopsis 1 page, English)",
                  "limits": {"synopsis_page_en": 500},
                  "docs": ["logline_en", "synopsis_page_en"], "en": True},
    "generic": {"name": "Producer & platform",
                "limits": {"logline": 50, "synopsis_paragraph": 150, "synopsis_page": 600, "bio": 120},
                "docs": ["logline", "synopsis_paragraph", "synopsis_page", "characters"]},
}

KNOWN = {
    "logline": "Logline", "tagline": "Tagline", "synopsis_paragraph": "Synopsis (paragraph)",
    "synopsis_page": "Synopsis (1 page)", "synopsis_long": "Synopsis (long)", "characters": "Characters",
    "world": "World", "tone": "Tone & style", "season_arc": "Season arc", "episodes": "Episodes",
    "why_now": "Why now", "audience": "Audience", "comps": "Comparables", "team": "Team",
    "logline_en": "Logline (EN)", "synopsis_paragraph_en": "Synopsis (EN, paragraph)",
    "synopsis_page_en": "Synopsis (EN, 1 page)", "characters_en": "Characters (EN)",
}


# ---------------------------------------------------------------- facts
def load(path, paper="letter"):
    with open(path, encoding="utf-8-sig") as f:
        title, blocks = sp.parse(sp.strip_marks(f.read()))
    lpp = int(round((sp.PAPER[paper][1] - 2.0) * 6))
    pages = sp.paginate(blocks, lpp, sp.LABELS["hy"])
    scenes = sp.breakdown(blocks, pages, lpp)
    return {"path": path, "label": os.path.splitext(os.path.basename(path))[0], "title": title,
            "blocks": blocks, "pages": len(pages), "scenes": scenes}


def words(s):
    return len(re.findall(r"\w+(?:[-'՚’]\w+)*", s))


def collect(eps):
    chars = {}
    for ei, ep in enumerate(eps):
        cur = -1
        for b in ep["blocks"]:
            if b["type"] == "scene":
                cur += 1
            elif b["type"] == "dialogue_block":
                nm = sp.char_name(b["character"])
                c = chars.setdefault(nm, {"name": nm, "scenes": set(), "lines": 0, "words": 0,
                                          "episodes": set(), "age": "", "intro": ""})
                c["lines"] += 1
                c["words"] += sum(words(t) for k, t in b["lines"] if k == "dialogue")
                c["episodes"].add(ei)
        for sc_i, sc in enumerate(ep["scenes"]):
            for nm in sc["characters"]:
                c = chars.setdefault(nm, {"name": nm, "scenes": set(), "lines": 0, "words": 0,
                                          "episodes": set(), "age": "", "intro": ""})
                c["scenes"].add((ei, sc_i))
                c["episodes"].add(ei)
    # age + intro line: "ԱՐԱՄԸ (30) ներս է մտնում" / "ANNA (40s) enters"
    for ep in eps:
        for b in ep["blocks"]:
            if b["type"] != "action":
                continue
            text = " ".join(b["lines"])
            for nm, c in chars.items():
                if c["intro"]:
                    continue
                m = re.search(re.escape(nm) + r"[Ա-ՖA-ZА-Я]{0,3}\s*\(([^)]{1,12})\)", text)
                if m:
                    c["age"] = m.group(1).strip()
                    sent = re.split(r"(?<=[։.!?])\s+", text)
                    c["intro"] = next((s for s in sent if nm in s), text)[:240]
    total = sum(len(e["scenes"]) for e in eps) or 1
    ranked = sorted(chars.values(), key=lambda c: (-len(c["scenes"]), -c["lines"], c["name"]))
    for i, c in enumerate(ranked):
        n = len(c["scenes"])
        if c["lines"] == 0:
            c["role"] = "non-speaking"
        elif i < 2 or n >= 0.3 * total:
            c["role"] = "lead"
        elif n >= 3 or len(c["episodes"]) > 1:
            c["role"] = "supporting"
        else:
            c["role"] = "day player"
    return ranked


def cmd_facts(a):
    eps = [load(p, a.paper) for p in a.files]
    os.makedirs(a.out, exist_ok=True)
    chars = collect(eps)
    title = " ".join(eps[0]["title"].get("title", [])) or eps[0]["label"]
    pages = sum(e["pages"] for e in eps)
    L = [f"# Facts · {title}", "",
         f"Episodes: {len(eps)} · pages: {pages} · runtime ≈ {pages} min · scenes: {sum(len(e['scenes']) for e in eps)}",
         "", "Write pack.md from these facts and the script itself. Do not add events that are not in the script.", ""]
    L += ["## Characters", "", "| # | Name | Role | Scenes | Lines | Words | Episodes | Age | Intro (from action) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for i, c in enumerate(chars, 1):
        L.append(f"| {i} | {c['name']} | {c['role']} | {len(c['scenes'])} | {c['lines']} | {c['words']} | "
                 f"{','.join(str(e + 1) for e in sorted(c['episodes']))} | {c['age']} | {c['intro'].replace('|', '/')} |")
    for ei, ep in enumerate(eps, 1):
        L += ["", f"## Episode {ei}: {ep['label']} · {ep['pages']} p.", ""]
        cur = -1
        first_action = {}
        for b in ep["blocks"]:
            if b["type"] == "scene":
                cur += 1
            elif b["type"] == "action" and cur >= 0 and cur not in first_action:
                first_action[cur] = " ".join(b["lines"])[:200]
        for si, sc in enumerate(ep["scenes"]):
            what = sc["synopsis"] or first_action.get(si, "")
            L.append(f"- **{sc['number']}. {sc['heading']}** ({sc['length']}) · {', '.join(sc['characters'])} · {what}")
    with open(os.path.join(a.out, "facts.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    js = [{k: (sorted(v) if isinstance(v, set) else v) for k, v in c.items()} for c in chars]
    with open(os.path.join(a.out, "facts.json"), "w", encoding="utf-8") as f:
        json.dump({"title": title, "pages": pages, "episodes": [e["label"] for e in eps], "characters": js,
                   "scenes": [[{k: v for k, v in s.items()} for s in e["scenes"]] for e in eps]},
                  f, ensure_ascii=False, indent=1, default=list)
    print(f"wrote {a.out}/facts.md  ({len(chars)} characters, {pages} pages)")


# ---------------------------------------------------------------- pack.md
def parse_pack(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                meta[k.strip().lower()] = v.strip()
        text = text[m.end():]
    secs, cur = {}, None
    for ln in text.splitlines():
        mm = re.match(r"^##\s+(\w+)\s*$", ln)
        if mm:
            cur = mm.group(1).lower()
            secs[cur] = []
        elif cur:
            secs[cur].append(ln)
    return meta, {k: "\n".join(v).strip() for k, v in secs.items()}


def subsections(body):
    """'### NAME\\ntext' -> [(NAME, text)]"""
    out, cur = [], None
    for ln in body.splitlines():
        if ln.startswith("### "):
            cur = [ln[4:].strip(), []]
            out.append(cur)
        elif cur:
            cur[1].append(ln)
    return [(n, "\n".join(t).strip()) for n, t in out]


# ---------------------------------------------------------------- sides
def scene_blocks(ep):
    out, cur = [], None
    for b in ep["blocks"]:
        if b["type"] == "scene":
            cur = [b]
            out.append(cur)
        elif cur is not None and b["type"] not in ("section", "page_break"):
            cur.append(b)
    return out


def pick_sides(eps, c, per_char):
    cand = []
    for ei, ep in enumerate(eps):
        for si, sb in enumerate(scene_blocks(ep)):
            mine = [b for b in sb if b["type"] == "dialogue_block" and sp.char_name(b["character"]) == c["name"]]
            if mine:
                w = sum(sum(words(t) for k, t in b["lines"] if k == "dialogue") for b in mine)
                cand.append((len(mine) * 3 + w / 20, ei, si, sb))
    best = sorted(cand, key=lambda x: -x[0])[:per_char]
    return sorted(best, key=lambda x: (x[1], x[2]))


def safe(s):
    return re.sub(r'[\\/:*?"<>|]+', "", s).strip()


# ---------------------------------------------------------------- build
def cmd_build(a):
    import pack_design as dz
    eps = [load(p, a.paper) for p in a.files]
    chars = collect(eps)
    meta, S = parse_pack(a.texts)
    lang = a.lang
    T = lambda k: dz.L(lang, k)  # noqa: E731
    title = meta.get("title") or " ".join(eps[0]["title"].get("title", [])) or eps[0]["label"]
    pages = sum(e["pages"] for e in eps)
    allsc = [s for e in eps for s in e["scenes"]]
    nsc = len(allsc)
    fmt = meta.get("format", "")
    series = len(eps) > 1 or bool(S.get("episodes"))
    sets = {}
    for ei, e in enumerate(eps):
        for s in e["scenes"]:
            st = sp.split_set(s["location"])[0]
            d = sets.setdefault(st, {"scenes": 0, "eighths": 0, "ie": set(), "eps": set(), "night": 0})
            d["scenes"] += 1
            d["eighths"] += s["eighths"]
            d["ie"].add(T("ext") if sp.is_ext(s["int_ext"]) else T("int"))
            d["eps"].add(ei + 1)
            d["night"] += sp.is_night(s["time"])
    speaking = [c for c in chars if c["lines"]]
    leads = [c for c in chars if c["role"] == "lead"]
    out = os.path.abspath(a.out)
    R = {r[0]: r for r in dz.RECIPIENTS}
    D = {k: os.path.join(out, dz.folder_name(r)) for k, r in R.items()}
    internal = os.path.join(out, "_internal (do not send)")
    os.makedirs(internal, exist_ok=True)
    made, missing = [], []
    desc = {k.upper(): v for k, v in subsections(S.get("characters", ""))}
    hy_list, en_list = subsections(S.get("characters", "")), subsections(S.get("characters_en", ""))
    en_of = {h[0].upper(): e for h, e in zip(hy_list, en_list)}   # same order in both sections

    def need(*keys):
        for k in keys:
            if not S.get(k):
                missing.append(k)
        return all(S.get(k) for k in keys)

    def fname(folder, doc):
        os.makedirs(D[folder], exist_ok=True)
        return os.path.join(D[folder], safe(f"{title} — {doc}") + ".pdf")

    def run(folder, lg=None):
        return dz.recipient_label(R[folder], lg or lang), title

    def stat_items(lg):
        t = lambda k: dz.L(lg, k)  # noqa: E731
        it = [(pages, f"{t('pages')} · ≈ {pages} {t('minutes')}"), (nsc, t("scenes")), (len(sets), t("sets")),
              (len(speaking), t("roles"))]
        if len(eps) > 1:
            it = [(len(eps), t("episodes_n"))] + it[:3]
        return it

    def char_meta(c, lg):
        t = lambda k: dz.L(lg, k)  # noqa: E731
        m = [dz.chip(t(c["role"]), dz.ROLE_CLS[c["role"]])]
        if c["age"]:
            m.append(f"<span>{t('age')} {dz.esc(c['age'])}</span>")
        m.append(f"<span>{len(c['scenes'])} {t('scenes')}</span>")
        if len(eps) > 1:
            m.append(f"<span>{t('eps')} {','.join(str(e + 1) for e in sorted(c['episodes']))}</span>")
        return m

    def char_cards(lg, dmap, only_described=True, limit=None):
        items = []
        for c in chars:
            d = dmap.get(c["name"].upper(), "")
            if only_described and not d:
                continue
            items.append((c["name"], char_meta(c, lg), d or c["intro"]))
        return dz.cards(items[:limit] if limit else items)

    def tcls(text):
        n = words(text)
        if re.search(r"^\s*[-*•] ", text, re.M):
            return "body"
        return "state" if n <= 60 else ("body" if n <= 170 else "body long cols2")

    with dz.Renderer() as RN:
        def doc(folder, docname, body, lg=None, kind="doc"):
            who, right = run(folder, lg)
            fn = fname(folder, docname)
            RN.pdf(dz.page(body, kind, f"{title} — {docname}", who, right), fn, kind,
                   html_dir=os.path.join(internal, "html"))
            made.append(fn)
            return fn

        # 01 producer
        if need("logline", "synopsis_paragraph"):
            b = dz.masthead(title, fmt, T("one_pager"), S["logline"])
            b += dz.h2("01", T("synopsis")) + dz.md(S["synopsis_paragraph"])
            b += dz.h2("02", T("characters")) + char_cards(lang, desc, limit=4)
            n = 3
            for k in ("why_now", "comps"):
                if S.get(k):
                    b += dz.h2(f"{n:02d}", T(k)) + dz.md(S[k])
                    n += 1
            b += dz.h2(f"{n:02d}", T("scale")) + dz.stats(stat_items(lang))
            doc("01", "One-pager", b, kind="onepage")
        if need("synopsis_page"):
            b = dz.masthead(title, fmt, f"{T('logline')} · {T('synopsis')}", S.get("logline", ""))
            b += dz.h2("01", T("synopsis")) + dz.md(S["synopsis_page"])
            if S.get("synopsis_long"):
                b += dz.h2("02", T("synopsis_long")) + dz.md(S["synopsis_long"])
            doc("01", "Synopsis", b)

        # 02 platform: deck / bible
        if series:
            need("world", "season_arc")
        if S.get("logline") and (S.get("world") or S.get("characters")):
            dname = T("bible") if series else T("deck")
            lw = dz.logo_img("dark")
            slides, k = [], [0]

            def foot():
                k[0] += 1
                return (title, "", f"{k[0]:02d}")

            cov = meta.get("cover")
            covbg = ""
            if cov:
                cp = cov if os.path.isabs(cov) else os.path.join(os.path.dirname(os.path.abspath(a.texts)), cov)
                if os.path.exists(cp):
                    covbg = f'<div class="bg" style="background-image:url(\'file://{cp}\')"></div><div class="shade"></div>'
            slides.append(dz.slide(f'{covbg}<div class="doc">{dz.esc(dname)}</div>{dz.logo_img("light", "logo")}'
                                   f'<div class="in"><div class="tri"></div><h1>{dz.esc(title)}</h1>'
                                   f'<div class="fmt">{dz.esc(fmt)}</div>'
                                   f'<div class="lg">{dz.inline(S.get("tagline", ""))}</div></div>',
                                   dark=True, cls="s-cover"))
            sec = 0

            def nxt():
                nonlocal sec
                sec += 1
                return f"{sec:02d}"

            slides.append(dz.slide(dz.kicker(nxt(), T("logline")) + f'<div class="fit big">{dz.inline(S["logline"])}</div>',
                                   foot=foot()))
            syn = S.get("synopsis_paragraph") or S.get("synopsis_page", "")
            if syn:
                slides.append(dz.slide(dz.kicker(nxt(), T("synopsis")) + f'<div class="fit {tcls(syn)}">{dz.md(syn)}</div>',
                                       foot=foot()))
            for key in ("world", "tone"):
                if S.get(key):
                    slides.append(dz.slide(dz.kicker(nxt(), T(key)) + f'<div class="fit {tcls(S[key])}">{dz.md(S[key])}</div>',
                                           foot=foot()))
            cno = nxt()
            for c in chars:
                d = desc.get(c["name"].upper())
                if not d:
                    continue
                meta_html = "".join(f"<div>{m}</div>" if not m.startswith("<span class=\"chip") else m
                                    for m in char_meta(c, lang))
                slides.append(dz.slide(dz.kicker(cno, T("characters")) +
                                       f'<div class="char"><div><div class="nm">{dz.esc(c["name"].title() if lang == "en" else c["name"])}</div>'
                                       f'<div class="meta">{meta_html}</div></div>'
                                       f'<div class="fit body">{dz.md(d)}</div></div>', foot=foot()))
            if S.get("season_arc"):
                slides.append(dz.slide(dz.kicker(nxt(), T("season_arc")) +
                                       f'<div class="fit {tcls(S["season_arc"])}">{dz.md(S["season_arc"])}</div>', foot=foot()))
            if S.get("episodes"):
                eno = nxt()
                epl = subsections(S["episodes"])
                for i in range(0, len(epl), 4):
                    cells = "".join(f'<div class="e"><div class="k">{dz.esc(n)}</div>{dz.md(t)}</div>'
                                    for n, t in epl[i:i + 4])
                    slides.append(dz.slide(dz.kicker(eno, T("episodes")) + f'<div class="fit eps">{cells}</div>',
                                           foot=foot()))
            nums = "".join(f'<div><div class="v">{v}</div><div class="l">{dz.esc(l)}</div></div>'
                           for v, l in stat_items(lang))
            slides.append(dz.slide(dz.kicker(nxt(), T("scale")) + f'<div class="nums">{nums}</div>', dark=True,
                                   foot=foot()))
            for key in ("audience", "why_now", "comps", "team"):
                if S.get(key):
                    slides.append(dz.slide(dz.kicker(nxt(), T(key)) + f'<div class="fit {tcls(S[key])}">{dz.md(S[key])}</div>',
                                           foot=foot()))
            slides.append(dz.slide(f'{dz.logo_img("light")}<div class="t">{dz.esc(title)}</div>'
                                   f'<div class="c">{dz.esc(meta.get("contact", "maghakianscripts.com"))}</div>',
                                   dark=True, cls="end"))
            doc("02", "Series bible" if series else "Pitch deck", "".join(slides), kind="deck")
        if S.get("episodes"):
            b = dz.masthead(title, fmt, T("ep_synopses"), S.get("logline", ""))
            for i, (n, t) in enumerate(subsections(S["episodes"]), 1):
                b += f'<div class="ep"><div class="k">{dz.esc(n)}</div><div>{dz.md(t)}</div></div>'
            doc("02", "Episode synopses", b)
        elif len(eps) > 1:
            missing.append("episodes")

        # 03 director: formatted script + scene overview
        for ei, e in enumerate(eps):
            stem = os.path.join(D["03"], safe(f"{title} — {T('episode')} {ei + 1:02d}") if len(eps) > 1
                                else safe(f"{title} — Script"))
            os.makedirs(D["03"], exist_ok=True)
            subprocess.run([sys.executable, os.path.join(HERE, "screenplay.py"), e["path"], "--out", stem,
                            "--pdf", "--docx", "--fdx", "--report", "--csv", "--paper", a.paper, "--lang", lang]
                           + (["--no-logo"] if a.no_logo else []), check=True, stdout=subprocess.DEVNULL)
            for ext in ("_breakdown.md",):
                if os.path.exists(stem + ext):
                    os.replace(stem + ext, os.path.join(internal, os.path.basename(stem) + ext))
            if os.path.exists(stem + "_breakdown.csv"):
                os.makedirs(D["04"], exist_ok=True)
                os.replace(stem + "_breakdown.csv",
                           os.path.join(D["04"], os.path.basename(stem).replace("Script", "Scenes") + " — scenes.csv"
                                        if len(eps) > 1 else os.path.basename(stem).replace("Script", "Scenes") + ".csv"))
            made.append(stem + ".pdf")
        b = dz.masthead(title, fmt, T("overview"))
        b += dz.stats(stat_items(lang))
        for ei, e in enumerate(eps):
            if len(eps) > 1:
                b += dz.h2(f"{ei + 1:02d}", f"{T('episode')} {ei + 1} · {e['pages']} {T('pages')}")
            first = {}
            cur = -1
            for bl in e["blocks"]:
                if bl["type"] == "scene":
                    cur += 1
                elif bl["type"] == "action" and cur >= 0 and cur not in first:
                    first[cur] = " ".join(bl["lines"])
            rows = "".join(
                f'<tr><td class="n">{dz.esc(s["number"])}</td><td><b>{dz.esc(s["heading"])}</b><br>'
                f'<span class="note">{dz.esc((s["synopsis"] or first.get(i, ""))[:260])}</span></td>'
                f'<td>{dz.esc(", ".join(s["characters"]))}</td><td class="num">{dz.esc(s["length"])}</td></tr>'
                for i, s in enumerate(e["scenes"]))
            b += (f'<table><thead><tr><th>#</th><th>{T("scene")} · {T("content")}</th><th>{T("cast")}</th>'
                  f'<th class="num">{T("length")}</th></tr></thead><tbody>{rows}</tbody></table>')
        doc("03", "Scene overview", b)

        # 04 line producer: breakdown
        ext = [s for s in allsc if sp.is_ext(s["int_ext"])]
        inn = [s for s in allsc if not sp.is_ext(s["int_ext"])]
        b = dz.masthead(title, fmt, T("breakdown"))
        b += dz.stats([(pages, f"{T('pages')} · ≈ {pages} {T('minutes')}"), (nsc, T("scenes")), (len(sets), T("sets")),
                       (len(speaking), T("roles"))])
        b += dz.stats([(sp.eighths_str(sum(s["eighths"] for s in inn)), T("int_pages")),
                       (sp.eighths_str(sum(s["eighths"] for s in ext)), T("ext_pages")),
                       (sum(1 for s in allsc if sp.is_night(s["time"])), T("night")),
                       (sum(1 for s in ext if sp.is_night(s["time"])), T("ext_night"))])
        b += dz.h2("01", T("location"))
        rows = "".join(
            f'<tr><td><b>{dz.esc(st)}</b></td><td>{"".join(dz.chip(x, "ext" if x == T("ext") else "int") + " " for x in sorted(d["ie"]))}</td>'
            f'<td class="num">{d["scenes"]}</td><td class="num">{sp.eighths_str(d["eighths"])}</td>'
            f'<td class="num">{d["night"] or ""}</td>'
            + (f'<td>{",".join(map(str, sorted(d["eps"])))}</td>' if len(eps) > 1 else "") + "</tr>"
            for st, d in sorted(sets.items(), key=lambda x: -x[1]["eighths"]))
        b += (f'<table><thead><tr><th>{T("location")}</th><th>{T("ie")}</th><th class="num">{T("scenes")}</th>'
              f'<th class="num">{T("pages")}</th><th class="num">{T("night")}</th>'
              + (f'<th>{T("eps")}</th>' if len(eps) > 1 else "") + f'</tr></thead><tbody>{rows}</tbody></table>')
        b += dz.h2("02", T("characters"))
        rows = "".join(
            f'<tr><td><b>{dz.esc(c["name"])}</b></td><td>{dz.chip(T(c["role"]), dz.ROLE_CLS[c["role"]])}</td>'
            f'<td class="num">{len(c["scenes"])}</td><td class="num">{c["lines"]}</td>'
            + (f'<td>{",".join(str(x + 1) for x in sorted(c["episodes"]))}</td>' if len(eps) > 1 else "") + "</tr>"
            for c in chars)
        b += (f'<table><thead><tr><th>{T("role")}</th><th></th><th class="num">{T("scenes")}</th>'
              f'<th class="num">{T("lines")}</th>' + (f'<th>{T("eps")}</th>' if len(eps) > 1 else "")
              + f'</tr></thead><tbody>{rows}</tbody></table>')
        for ei, e in enumerate(eps):
            b += dz.h2(f"{ei + 3:02d}", (f"{T('episode')} {ei + 1} · " if len(eps) > 1 else "") + T("scenes"))
            rows = "".join(
                f'<tr><td class="n">{dz.esc(s["number"])}</td>'
                f'<td>{dz.chip(T("ext") if sp.is_ext(s["int_ext"]) else T("int"), "ext" if sp.is_ext(s["int_ext"]) else "int")}</td>'
                f'<td><b>{dz.esc(s["location"])}</b></td>'
                f'<td>{dz.chip(s["time"], "night") if sp.is_night(s["time"]) else dz.esc(s["time"])}</td>'
                f'<td>{dz.esc(", ".join(s["characters"]))}</td><td class="num">{dz.esc(s["length"])}</td></tr>'
                for s in e["scenes"])
            b += (f'<table><thead><tr><th>#</th><th>{T("ie")}</th><th>{T("location")}</th><th>{T("time")}</th>'
                  f'<th>{T("cast")}</th><th class="num">{T("length")}</th></tr></thead><tbody>{rows}</tbody></table>')
        doc("04", "Production breakdown", b)
        if len(eps) > 1:
            subprocess.run([sys.executable, os.path.join(HERE, "season.py")] + [e["path"] for e in eps]
                           + ["--out", os.path.join(internal, "season")], check=True, stdout=subprocess.DEVNULL)
            if os.path.exists(os.path.join(internal, "season.csv")):
                os.replace(os.path.join(internal, "season.csv"), os.path.join(D["04"], safe(f"{title} — Season") + ".csv"))

        # 05 casting
        rows = []
        for c in chars:
            d = desc.get(c["name"].upper(), "")
            rows.append({"name": c["name"], "role": c["role"], "age": c["age"], "scenes": len(c["scenes"]),
                         "lines": c["lines"], "words": c["words"],
                         "episodes": ",".join(str(e + 1) for e in sorted(c["episodes"])),
                         "description": d.replace("\n", " ") if d else c["intro"]})
        os.makedirs(D["05"], exist_ok=True)
        with open(os.path.join(D["05"], safe(f"{title} — Casting") + ".csv"), "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["name"])
            w.writeheader()
            w.writerows(rows)
        b = dz.masthead(title, fmt, T("casting"))
        b += dz.stats([(len(leads), T("lead")), (sum(1 for c in chars if c["role"] == "supporting"), T("supporting")),
                       (sum(1 for c in chars if c["role"] == "day player"), T("day player")),
                       (sum(1 for c in chars if c["role"] == "non-speaking"), T("non-speaking"))])
        groups = [("lead", "supporting"), ("day player", "non-speaking")]
        for gi, g in enumerate(groups, 1):
            items = [(c["name"], char_meta(c, lang), desc.get(c["name"].upper()) or c["intro"])
                     for c in chars if c["role"] in g]
            if items:
                b += dz.h2(f"{gi:02d}", " · ".join(T(x) for x in g)) + dz.cards(items, one=(gi == 1))
        doc("05", "Casting breakdown", b)

        # 06 actors: sides with a branded cover
        from pypdf import PdfReader, PdfWriter
        lpp = int(round((sp.PAPER[a.paper][1] - 2.0) * 6))
        for c in chars:
            if c["role"] not in ("lead", "supporting") or c["lines"] == 0:
                continue
            best = pick_sides(eps, c, a.sides)
            blocks = [bl for *_, sb in best for bl in sb]
            raw = os.path.join(internal, safe(c["name"]) + "_sides_raw.pdf")
            sp.write_pdf(raw, {}, blocks, sp.paginate(blocks, lpp, sp.LABELS[lang if lang in sp.LABELS else "hy"]),
                         a.paper, True, sp.LABELS[lang if lang in sp.LABELS else "hy"], None)
            rows = "".join(
                f'<tr><td class="n">{dz.esc(sb[0]["number"])}</td><td><b>{dz.esc(sb[0]["text"])}</b></td>'
                + (f'<td>{T("episode")} {ei + 1}</td>' if len(eps) > 1 else "") + "</tr>"
                for _, ei, si, sb in best)
            d = desc.get(c["name"].upper()) or c["intro"]
            b = dz.masthead(title, fmt, T("sides"))
            b += (f'<div class="cards one"><div class="card"><div class="nm" style="font-size:24pt">{dz.esc(c["name"])}</div>'
                  f'<div class="meta">{"".join(char_meta(c, lang))}</div>{dz.md(d)}</div></div>')
            b += dz.h2("01", T("sides_note")) + f'<table><tbody>{rows}</tbody></table>'
            cov = os.path.join(internal, safe(c["name"]) + "_cover.pdf")
            who, right = run("06")
            RN.pdf(dz.page(b, "doc", c["name"], who, right), cov, html_dir=os.path.join(internal, "html"))
            wtr = PdfWriter()
            for pth in (cov, raw):
                for pg in PdfReader(pth).pages:
                    wtr.add_page(pg)
            fn = fname("06", f"Sides — {c['name']}")
            with open(fn, "wb") as f:
                wtr.write(f)
            os.remove(cov)
            os.remove(raw)
            made.append(fn)

        # 07 international (English)
        if S.get("logline_en") and (S.get("synopsis_paragraph_en") or S.get("synopsis_page_en")):
            b = dz.masthead(meta.get("title_en", title), meta.get("format_en", fmt), "One-pager", S["logline_en"])
            b += dz.h2("01", "Synopsis") + dz.md(S.get("synopsis_page_en") or S["synopsis_paragraph_en"])
            if en_of:
                items = [(en_of[c["name"].upper()][0], char_meta(c, "en"), en_of[c["name"].upper()][1])
                         for c in chars if c["name"].upper() in en_of][:4]
                b += dz.h2("02", "Characters") + dz.cards(items)
            b += dz.h2("03", "Production scale") + dz.stats(stat_items("en"))
            doc("07", "One-pager (EN)", b, lg="en", kind="onepage")
        else:
            missing.append("logline_en + synopsis_*_en (07 International)")

        # 08 competition / fund
        p = PRESETS[a.preset]
        en = p.get("en")
        lg = "en" if en else lang
        b = dz.masthead(meta.get("title_en", title) if en else title, meta.get("format_en", fmt) if en else fmt,
                        f"{dz.L(lg, 'application')} · {p['name']}")
        for i, k in enumerate(p["docs"], 1):
            src = k if k.endswith("_en") or not en or not S.get(k + "_en") else k + "_en"
            base = k[:-3] if k.endswith("_en") else k
            if not S.get(src):
                missing.append(f"{src} (preset {a.preset})")
            elif en and not k.endswith("_en") and not S.get(k + "_en"):
                missing.append(f"{k}_en (preset {a.preset} wants English)")
            if base == "characters":
                bios = subsections(S.get(src, ""))[:p.get("max_bios", 5)]
                lim = p["limits"].get("bio")
                items = []
                for n, t in bios:
                    wc = words(t)
                    items.append((n, [dz.chip(f"{wc}{' / ' + str(lim) if lim else ''} {dz.L(lg, 'words')}",
                                              "over" if lim and wc > lim else "ok")], t))
                b += dz.h2(f"{i:02d}", dz.L(lg, "characters")) + dz.cards(items, one=True)
                continue
            txt = S.get(src, "")
            lim = p["limits"].get(k) or p["limits"].get(src)
            wc = words(txt)
            badge = dz.chip(f"{wc}{' / ' + str(lim) if lim else ''} {dz.L(lg, 'words')}",
                            "over" if lim and wc > lim else "ok") if txt else ""
            label = dz.L(lg, {"synopsis_page": "synopsis", "synopsis_paragraph": "synopsis"}.get(base, base))
            b += dz.h2(f"{i:02d}", label) + f'<div class="wc">{badge}</div>' + dz.md(txt)
        doc("08", f"Application — {p['name']}", b, lg=lg)

        # 00 index
        cov = (f'<div class="cover"><div><div class="kick">{dz.esc(T("contents"))}</div><h1>{dz.esc(title)}</h1>'
             f'<div class="fmt">{dz.esc(fmt)}</div><div class="logline">{dz.inline(S.get("logline", ""))}</div></div>'
             f'<div class="bot"><span>{dz.esc(meta.get("contact", "Maghakian Scripts · maghakianscripts.com"))}</span>'
             f'{dz.logo_img("light")}</div></div>')
        b = dz.masthead(title, fmt, T("contents")) + '<div class="toc">'
        for r in dz.RECIPIENTS:
            if not os.path.isdir(D[r[0]]):
                continue
            files = sorted(f for f in os.listdir(D[r[0]]) if not f.startswith("."))
            files_html = "<br>".join(dz.esc(f.replace(f"{title} — ", "")) for f in files)
            b += (f'<div class="row"><div class="no">{r[0]}</div><div><div class="who">{dz.esc(r[1])}</div>'
                  f'<div class="en">{dz.esc(r[2])}</div></div><div class="files"><b>{dz.esc(r[3] if lang != "en" else r[4])}</b>'
                  f'<br>{files_html}</div></div>')
        b += "</div>"
        idx = os.path.join(out, safe(f"00 {title} — {T('contents')}") + ".pdf")
        hd = os.path.join(internal, "html")
        c1, c2 = os.path.join(internal, "_cover.pdf"), os.path.join(internal, "_toc.pdf")
        RN.pdf(dz.page(cov, "cover", title), c1, "cover", html_dir=hd)
        RN.pdf(dz.page(b, "doc", title, T("contents"), title), c2, html_dir=hd)
        wtr = PdfWriter()
        for pth in (c1, c2):
            for pg in PdfReader(pth).pages:
                wtr.add_page(pg)
        with open(idx, "wb") as f:
            wtr.write(f)
        os.remove(c1)
        os.remove(c2)
        made.insert(0, idx)

    # CHECK.md (internal)
    Lc = [f"# Check · {title}", "", f"Script: {len(eps)} file(s), {pages} pages, {nsc} scenes, {len(chars)} characters.",
          "", "## Word limits", "", "| Text | Words | " + " | ".join(PRESETS) + " |", "|---|---|" + "---|" * len(PRESETS)]
    for k in KNOWN:
        if not S.get(k):
            continue
        items = subsections(S[k]) if k in ("characters", "characters_en") else [(None, S[k])]
        for n, t in items:
            wc = words(t)
            key = "bio" if n else k
            cells = []
            for pr in PRESETS.values():
                lim = pr["limits"].get(key)
                cells.append("" if not lim else ("✅" if wc <= lim else f"❌ >{lim}"))
            Lc.append(f"| {'bio: ' + n if n else k} | {wc} | " + " | ".join(cells) + " |")
    Lc += ["", "## Missing", ""] + ([f"- {m}" for m in dict.fromkeys(missing)] or ["- nothing"])
    nodesc = [c["name"] for c in chars if c["role"] in ("lead", "supporting") and c["name"].upper() not in desc]
    if nodesc:
        Lc += ["", "## Leads/supporting without a description in pack.md", ""] + [f"- {n}" for n in nodesc]
    Lc += ["", "## Files", ""] + [f"- {os.path.relpath(m, out)}" for m in made]
    with open(os.path.join(internal, "CHECK.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(Lc) + "\n")
    print(f"built {len(made)} files in {out}/  (internal/CHECK.md; missing: {len(set(missing))})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("facts")
    f.add_argument("files", nargs="+")
    f.add_argument("--out", default="pack")
    f.add_argument("--paper", choices=sp.PAPER, default="letter")
    b = sub.add_parser("build")
    b.add_argument("files", nargs="+")
    b.add_argument("--texts", required=True, help="pack.md written from facts.md")
    b.add_argument("--out", default="pack")
    b.add_argument("--preset", choices=PRESETS, default="generic")
    b.add_argument("--sides", type=int, default=3, help="scenes per character in sides")
    b.add_argument("--paper", choices=sp.PAPER, default="letter")
    b.add_argument("--lang", choices=sp.LABELS, default="hy")
    b.add_argument("--no-logo", action="store_true")
    a = ap.parse_args()
    return cmd_facts(a) if a.cmd == "facts" else cmd_build(a)


if __name__ == "__main__":
    sys.exit(main())
