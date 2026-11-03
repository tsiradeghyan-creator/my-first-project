#!/usr/bin/env python3
"""Script Pack: one script (or a season of episodes) -> every document each recipient needs.

Two steps, because the facts are counted by code and the prose is written by Claude (or the GPT):

  1) facts   python3 pack.py facts ep*.fountain --out pack/
             -> pack/facts.md + facts.json: scenes, synopsis lines, characters (scenes, lines,
                words, episodes, age and intro line from the action), pages, runtime, locations.
             Claude reads facts.md + the script and writes pack/pack.md (format: references/pack.md).

  2) build   python3 pack.py build ep*.fountain --texts pack/pack.md --out pack/ [--preset sundance_feature]
             -> 01_producer/      logline_synopsis.pdf, one_pager.pdf
                02_platform/      series_bible.pdf (deck; pitch_deck.pdf for a feature), episode_synopses.pdf
                03_production/    script PDF/DOCX/FDX + breakdown per episode, season breakdown
                04_casting/       casting_breakdown.pdf/.csv/.md, sides/<NAME>.pdf
                05_international/ one_pager_en.pdf (if *_en sections exist)
                06_competition/   application_<preset>.pdf
                CHECK.md          word counts against each preset's limits, missing documents

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
    "generic": {"name": "Producer / platform default",
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


# Section headings in the documents, by --lang (05_international is always English).
HEAD = {
    "hy": {"Synopsis": "Համառոտ բովանդակություն", "Synopsis (long)": "Ընդարձակ բովանդակություն",
           "Characters": "Կերպարներ", "Why now": "Ինչու հիմա", "Comparables": "Համեմատելի նախագծեր",
           "Scale": "Արտադրության ծավալ", "Production scale": "Արտադրության ծավալ", "Logline": "Լոգլայն",
           "World": "Աշխարհը", "Tone & style": "Տոն և ոճ", "Season arc": "Սեզոնի աղեղ", "Episodes": "Սերիաներ",
           "Audience": "Լսարան", "Team": "Թիմ", "Casting breakdown": "Կաստինգ",
           "scenes": "տեսարան", "lines": "ռեպլիկ", "episodes": "սերիաներ", "pages": "էջ", "min": "րոպե",
           "script": "սցենար", "main sets": "հիմնական լոկացիա", "speaking roles": "խոսող դեր", "leads": "գլխավոր",
           "lead": "գլխավոր", "supporting": "երկրորդական", "day player": "էպիզոդիկ", "non-speaking": "առանց խոսքի"},
    "ru": {"Synopsis": "Синопсис", "Synopsis (long)": "Расширенный синопсис", "Characters": "Персонажи",
           "Why now": "Почему сейчас", "Comparables": "Референсы", "Scale": "Масштаб производства",
           "Production scale": "Масштаб производства", "Logline": "Логлайн", "World": "Мир",
           "Tone & style": "Тон и стиль", "Season arc": "Арка сезона", "Episodes": "Серии", "Audience": "Аудитория",
           "Team": "Команда", "Casting breakdown": "Кастинг", "scenes": "сцен", "lines": "реплик",
           "episodes": "серии", "pages": "стр.", "min": "мин", "script": "сценарий", "main sets": "основных локаций",
           "speaking roles": "ролей со словами", "leads": "главных", "lead": "главная", "supporting": "второстепенная",
           "day player": "эпизодическая", "non-speaking": "без слов"},
}


def tr(lang, k):
    return HEAD.get(lang, {}).get(k, k)


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


def write_md(path, meta, sections):
    L = ["---"] + [f"{k}: {v}" for k, v in meta.items() if v] + ["---"]
    for t, body in sections:
        if body.strip():
            L += [f"## {t}", body.strip(), ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def render(md, layout="doc", compact=False):
    cmd = [sys.executable, os.path.join(HERE, "treatment_pdf.py"), md, "--layout", layout]
    if compact:
        cmd.append("--compact")
    else:
        logo = os.path.join(sp.find_asset("assets", "maghakian_logo_light.png"), "maghakian_logo_light.png")
        if os.path.exists(logo):
            cmd += ["--logo", logo]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    return md[:-3] + ".pdf"


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


def write_sides(eps, chars, outdir, per_char, paper, logo):
    os.makedirs(outdir, exist_ok=True)
    made = []
    lpp = int(round((sp.PAPER[paper][1] - 2.0) * 6))
    for c in chars:
        if c["role"] not in ("lead", "supporting") or c["lines"] == 0:
            continue
        cand = []
        for ei, ep in enumerate(eps):
            for sb in scene_blocks(ep):
                n = sum(1 for b in sb if b["type"] == "dialogue_block" and sp.char_name(b["character"]) == c["name"])
                if n:
                    w = sum(sum(words(t) for k, t in b["lines"] if k == "dialogue") for b in sb
                            if b["type"] == "dialogue_block" and sp.char_name(b["character"]) == c["name"])
                    cand.append((n * 3 + w / 20, ei, sb))
        best = sorted(cand, key=lambda x: -x[0])[:per_char]
        best.sort(key=lambda x: (x[1], int(re.sub(r"\D", "", x[2][0]["number"]) or 0)))
        blocks = []
        for _, ei, sb in best:
            blocks += sb
        title = {"title": [f"SIDES · {c['name']}"],
                 "credit": [" · ".join(sorted({eps[ei]['label'] for _, ei, _ in best}))],
                 "author": ["Maghakian Scripts"]}
        pages = sp.paginate(blocks, lpp, sp.LABELS["hy"])
        fn = os.path.join(outdir, re.sub(r"[^\wԱ-Ֆա-ֆ-]+", "_", c["name"]) + ".pdf")
        sp.write_pdf(fn, title, blocks, pages, paper, True, sp.LABELS["hy"], logo)
        made.append((c["name"], fn, len(best)))
    return made


# ---------------------------------------------------------------- build
def cmd_build(a):
    eps = [load(p, a.paper) for p in a.files]
    chars = collect(eps)
    meta, S = parse_pack(a.texts)
    title = meta.get("title") or " ".join(eps[0]["title"].get("title", [])) or eps[0]["label"]
    pages = sum(e["pages"] for e in eps)
    nsc = sum(len(e["scenes"]) for e in eps)
    fmt = meta.get("format", "")
    base = {"title": title, "format": fmt, "contact": meta.get("contact", "Maghakian Scripts · maghakianscripts.com")}
    out = a.out
    D = {k: os.path.join(out, k) for k in ("01_producer", "02_platform", "03_production", "04_casting",
                                           "05_international", "06_competition")}
    for d in D.values():
        os.makedirs(d, exist_ok=True)
    made, missing = [], []
    logo = None if a.no_logo else sp.DEFAULT_LOGO

    def need(*keys):
        for k in keys:
            if not S.get(k):
                missing.append(k)
        return all(S.get(k) for k in keys)

    # scale line from the script itself
    locs = {}
    for e in eps:
        for s in e["scenes"]:
            locs.setdefault(sp.split_set(s["location"])[0] if hasattr(sp, "split_set") else s["location"], 0)
    speaking = [c for c in chars if c["lines"]]
    def scale_for(lg):
        t = lambda k: tr(lg, k)  # noqa: E731
        return (f"- {len(eps)} {t('episodes') if len(eps) > 1 else t('script')} · {pages} {t('pages')} · ≈ {pages} {t('min')}\n"
                f"- {nsc} {t('scenes')} · {len(locs)} {t('main sets')} · {len(speaking)} {t('speaking roles')} "
                f"({sum(1 for c in chars if c['role'] == 'lead')} {t('leads')})")
    scale = scale_for(a.lang)
    H = lambda k: tr(a.lang, k)  # noqa: E731

    # 01 producer
    if need("logline", "synopsis_paragraph"):
        md = os.path.join(D["01_producer"], "one_pager.md")
        char_short = "\n".join(f"- **{n}**: {t.splitlines()[0]}" for n, t in subsections(S.get("characters", ""))[:5])
        write_md(md, {**base, "logline": S["logline"]},
                 [(H("Synopsis"), S["synopsis_paragraph"]), (H("Characters"), char_short),
                  (H("Why now"), S.get("why_now", "")), (H("Comparables"), S.get("comps", "")), (H("Scale"), scale)])
        made.append(render(md, "doc", compact=True))
    if need("synopsis_page"):
        md = os.path.join(D["01_producer"], "logline_synopsis.md")
        write_md(md, {**base, "logline": S.get("logline", "")},
                 [(H("Synopsis"), S["synopsis_page"]), (H("Synopsis (long)"), S.get("synopsis_long", ""))])
        made.append(render(md, "doc", compact=True))

    # 02 platform: series bible / treatment deck
    series = len(eps) > 1 or bool(S.get("episodes"))
    if series:
        need("world", "season_arc")
    if S.get("world") or S.get("characters"):
        sec = [(H("Logline"), f"> {S.get('logline', '')}"), (H("World"), S.get("world", "")),
               (H("Tone & style"), S.get("tone", ""))]
        for n, t in subsections(S.get("characters", "")):
            sec.append((n, t))
        sec += [(H("Season arc"), S.get("season_arc", "")), (H("Episodes"), S.get("episodes", "")),
                (H("Audience"), S.get("audience", "")), (H("Why now"), S.get("why_now", "")),
                (H("Comparables"), S.get("comps", "")), (H("Production scale"), scale), (H("Team"), S.get("team", ""))]
        md = os.path.join(D["02_platform"], "series_bible.md" if series else "pitch_deck.md")
        write_md(md, {**base, "logline": S.get("logline", "")}, sec)
        made.append(render(md, "deck"))
    if S.get("episodes"):
        md = os.path.join(D["02_platform"], "episode_synopses.md")
        write_md(md, {**base, "logline": S.get("logline", "")}, [(H("Episodes"), S["episodes"])])
        made.append(render(md, "doc", compact=True))
    elif len(eps) > 1:
        missing.append("episodes")

    # 03 production: formatted scripts + breakdowns
    for e in eps:
        stem = os.path.join(D["03_production"], e["label"])
        subprocess.run([sys.executable, os.path.join(HERE, "screenplay.py"), e["path"], "--out", stem,
                        "--pdf", "--docx", "--fdx", "--report", "--csv", "--paper", a.paper, "--lang", a.lang]
                       + (["--no-logo"] if a.no_logo else []), check=True, stdout=subprocess.DEVNULL)
        made.append(stem + ".pdf")
    if len(eps) > 1:
        subprocess.run([sys.executable, os.path.join(HERE, "season.py")] + [e["path"] for e in eps]
                       + ["--out", os.path.join(D["03_production"], "season")], check=True, stdout=subprocess.DEVNULL)
        made.append(os.path.join(D["03_production"], "season.md"))

    # 04 casting
    desc = dict(subsections(S.get("characters", "")))
    desc_up = {k.upper(): v for k, v in desc.items()}
    rows = []
    for c in chars:
        d = desc_up.get(c["name"].upper(), "")
        rows.append({"name": c["name"], "role": c["role"], "age": c["age"], "scenes": len(c["scenes"]),
                     "lines": c["lines"], "words": c["words"],
                     "episodes": ",".join(str(e + 1) for e in sorted(c["episodes"])),
                     "description": d.replace("\n", " ") if d else c["intro"]})
    with open(os.path.join(D["04_casting"], "casting_breakdown.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["name"])
        w.writeheader()
        w.writerows(rows)
    sec = []
    for r in rows:
        if r["role"] == "non-speaking" and not r["description"]:
            continue
        head = f"{r['name']}" + (f", {r['age']}" if r["age"] else "")
        sec.append((head, f"*{H(r['role'])} · {r['scenes']} {H('scenes')} · {r['lines']} {H('lines')}"
                          + (f" · {H('episodes')} {r['episodes']}" if len(eps) > 1 else "") + "*\n\n" + r["description"]))
    md = os.path.join(D["04_casting"], "casting_breakdown.md")
    write_md(md, {**base, "format": (fmt + " · " if fmt else "") + H("Casting breakdown")}, sec)
    made.append(render(md, "doc", compact=True))
    for nm, fn, n in write_sides(eps, chars, os.path.join(D["04_casting"], "sides"), a.sides, a.paper, logo):
        made.append(fn)

    # 05 international
    if S.get("logline_en") and (S.get("synopsis_paragraph_en") or S.get("synopsis_page_en")):
        md = os.path.join(D["05_international"], "one_pager_en.md")
        cen = "\n".join(f"- **{n}**: {t.splitlines()[0]}" for n, t in subsections(S.get("characters_en", ""))[:5])
        write_md(md, {**base, "format": meta.get("format_en", fmt), "logline": S["logline_en"]},
                 [("Synopsis", S.get("synopsis_page_en") or S.get("synopsis_paragraph_en")), ("Characters", cen),
                  ("Scale", scale_for("en"))])
        made.append(render(md, "doc", compact=True))
    else:
        missing.append("logline_en + synopsis_*_en (05_international)")

    # 06 competition
    p = PRESETS[a.preset]
    en = p.get("en")  # these rules want English: use the *_en texts when they exist
    HP = (lambda k: k) if en else H  # noqa: E731
    sec = []
    for k in p["docs"]:
        src = k if k.endswith("_en") or not en or not S.get(k + "_en") else k + "_en"
        if k == "characters":
            bios = subsections(S.get(src, ""))[:p.get("max_bios", 5)]
            sec.append((HP("Characters"), "\n\n".join(f"### {n}\n{t}" for n, t in bios)))
        else:
            sec.append((HP(KNOWN.get(k, k).split(" (")[0]), S.get(src, "")))
        if not S.get(src):
            missing.append(f"{src} (preset {a.preset})")
        elif en and not k.endswith("_en") and not S.get(k + "_en"):
            missing.append(f"{k}_en (preset {a.preset} wants English)")
    md = os.path.join(D["06_competition"], f"application_{a.preset}.md")
    write_md(md, {**base, "format": f"{fmt} · {p['name']}" if fmt else p["name"]}, sec)
    made.append(render(md, "doc", compact=True))

    # CHECK.md
    L = [f"# Check · {title}", "", f"Script: {len(eps)} file(s), {pages} pages, {nsc} scenes, {len(chars)} characters.", "",
         "## Word limits", "", "| Text | Words | " + " | ".join(PRESETS) + " |", "|---|---|" + "---|" * len(PRESETS)]
    for k in KNOWN:
        if not S.get(k):
            continue
        if k in ("characters", "characters_en"):
            items = subsections(S[k])
            for n, t in items:
                cells = []
                for pr in PRESETS.values():
                    lim = pr["limits"].get("bio")
                    cells.append("" if not lim else ("✅" if words(t) <= lim else f"❌ >{lim}"))
                L.append(f"| bio: {n} | {words(t)} | " + " | ".join(cells) + " |")
            continue
        n = words(S[k])
        cells = []
        for pr in PRESETS.values():
            lim = pr["limits"].get(k)
            cells.append("" if not lim else ("✅" if n <= lim else f"❌ >{lim}"))
        L.append(f"| {k} | {n} | " + " | ".join(cells) + " |")
    L += ["", "## Missing", ""] + ([f"- {m}" for m in dict.fromkeys(missing)] or ["- nothing"])
    unknown_desc = [c["name"] for c in chars if c["role"] in ("lead", "supporting") and c["name"].upper() not in desc_up]
    if unknown_desc:
        L += ["", "## Characters without a description in pack.md", ""] + [f"- {n}" for n in unknown_desc]
    L += ["", "## Files", ""] + [f"- {os.path.relpath(m, out)}" for m in made]
    with open(os.path.join(out, "CHECK.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"built {len(made)} files in {out}/  (see CHECK.md; missing: {len(set(missing))})")


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
