#!/usr/bin/env python3
"""Proofreading pass for a Fountain script: apply corrections, produce
  1) <stem>_WORK.docx   working Word version: every change highlighted yellow + Word comment (why),
                         remarks without a change highlighted turquoise + comment
  2) <stem>_FINAL.pdf   clean final version for screenwriters / buyers (logo, American format)
  3) <stem>_FINAL.docx / .fdx / .fountain   clean final text in other formats
  4) <stem>_corrections.md   table of every correction and remark (+ what could not be applied)

The corrections come from a language model (Claude or ChatGPT) that read the script, as JSON:
[
  {"scene": "5", "find": "Հայրիկ՞", "replace": "Հայրի՞կ", "type": "կետադրություն",
   "why": "Հարցական նշանը դրվում է շեշտված վանկի ձայնավորի վրա"},
  {"scene": "12", "find": "ՎՎԻԼՈ", "replace": "ՎԻԼՈ", "type": "տառասխալ", "all": true},
  {"scene": "20", "find": "երկու ամիս", "type": "իմաստ",
   "why": "Սցենար 3-ում ասվում է երեք ամիս. ստուգել"}          # no "replace" = remark only
]
- "find" is copied exactly from the .fountain (one line, no line breaks); "scene" is the number in #…#.
- "all": true replaces every occurrence in that scene (or in the whole script if "scene" is omitted).
- "line": true matches only a whole line (automatic for character cues "@NAME").
Mechanical fixes run automatically first (counted in the report, not highlighted):
  ",,," / ",," / ",,,," -> "..."   ·   Latin ":" after an Armenian word at sentence end -> "։"
  spaces before "։ , ." removed   ·   double spaces -> one.        (--no-auto to skip)

Usage: python3 proofread.py ep01.fountain corrections.json [--out DIR] [--lang hy] [--paper letter]
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARM = "\u0531-\u0587"


def auto_fixes(text):
    counts = {}

    def sub(name, pattern, repl, s, flags=0):
        new, n = re.subn(pattern, repl, s, flags=flags)
        if n:
            counts[name] = counts.get(name, 0) + n
        return new

    out = []
    for line in text.split("\n"):
        if re.match(r"^\w[\w ]{0,30}:", line) and not re.match(rf"^[{ARM}]", line):
            out.append(line)                     # title page keys (Title:, Credit: …)
            continue
        line = sub(",,, / ,, -> ...", r"(?<!,),{2,}(?!,)", "...", line)
        line = sub("Latin ':' -> '։'", rf"(?<=[{ARM}])\s*:(?=\s|$)", "։", line)
        line = sub("space before punctuation", rf"(?<=[{ARM}\w])\s+(?=[։,](\s|$))", "", line)
        line = sub("double spaces", r"(?<=\S) {2,}(?=\S)", " ", line)
        out.append(line)
    return "\n".join(out), counts


def scene_spans(lines):
    """scene number -> (start_line, end_line) in the fountain text"""
    spans, cur, start = {}, None, 0
    for i, ln in enumerate(lines):
        m = re.match(r"^\..*#([\w.\-]+)#\s*$", ln)
        if m:
            if cur is not None and cur not in spans:
                spans[cur] = (start, i)
            cur, start = m.group(1), i
    if cur is not None and cur not in spans:
        spans[cur] = (start, len(lines))
    return spans


def apply(text, corrections):
    lines = text.split("\n")
    spans = scene_spans(lines)
    clean = list(lines)
    marked = list(lines)
    comments, report = {}, []
    for k, c in enumerate(corrections, start=1):
        cid = str(k)
        find = c.get("find", "")
        rep = c.get("replace")
        changed = rep is not None and rep != find
        sc = str(c.get("scene", "")).strip().lstrip("#").rstrip("#")
        lo, hi = spans.get(sc, (0, len(lines))) if sc else (0, len(lines))
        if sc and sc not in spans:
            report.append({**c, "id": cid, "status": "❌ scene not found"})
            continue
        hits = 0
        whole = c.get("line") or find.startswith("@")     # character cues: match the whole line only
        for i in range(lo, hi):
            if not find or find not in clean[i] or (whole and clean[i].strip() != find):
                continue
            if changed:
                n = clean[i].count(find) if c.get("all") else 1
                clean[i] = clean[i].replace(find, rep, n)
            else:
                n = 1
            # marked copy: wrap the new text (or the remarked text) in ⟦id¦…⟧
            target = rep if changed else find
            m_src = marked[i]
            if find in m_src:
                marked[i] = m_src.replace(find, f"⟦{cid}¦{target}⟧", n)
            hits += n
            if not c.get("all"):
                break
        if hits:
            why = c.get("why", "")
            kind = c.get("type", "")
            note = f"{kind}: " if kind else ""
            note += f"«{find}» → «{rep}»" if changed else f"«{find}»"
            if why:
                note += f". {why}"
            comments[cid] = {"text": note, "changed": changed}
            report.append({**c, "id": cid, "status": f"✅ {hits}×" if changed else "💬 remark"})
        else:
            report.append({**c, "id": cid, "status": "❌ text not found"})
    return "\n".join(clean), "\n".join(marked), comments, report


def auto_checks(text):
    """Things a machine finds reliably; listed in the report for the editor to decide."""
    import screenplay as sp
    out = []
    mixed = sorted({w for w in re.findall(r"\S+", text)
                    if re.search(f"[{ARM}]", w) and re.search(r"[A-Za-zА-Яа-яЁё]", w)})
    if mixed:
        out.append("- Լատինական/ռուսական տառ հայերեն բառի մեջ: " + ", ".join(f"«{w}»" for w in mixed[:40]))
    title, blocks = sp.parse(text)
    cur, cast, sc = None, set(), ""
    missing = []
    for b in blocks:
        if b["type"] == "scene":
            cur, cast, sc = b, set(), b.get("number", "")
        elif b["type"] == "synopsis" and b["text"].upper().startswith("CAST:"):
            cast |= {re.sub(r"\(.*?\)", "", n).strip().upper()
                     for n in re.split(r",\s*(?![^()]*\))", b["text"].split(":", 1)[1])}
        elif b["type"] == "dialogue_block" and cast:
            nm = sp.char_name(b["character"]).upper()
            if nm not in cast and not any(nm in c or c in nm for c in cast if c):
                missing.append(f"{sc}: {nm}")
    if missing:
        out.append("- Խոսում է, բայց չկա տեսարանի կերպարների ցուցակում: " + "; ".join(dict.fromkeys(missing)))
    scenes = sp.breakdown(blocks, sp.paginate(blocks, 54, sp.LABELS["hy"]), 54)
    nums = [x["number"] for x in scenes]
    dup = sorted({x for x in nums if nums.count(x) > 1})
    if dup:
        out.append("- Տեսարանի համարը կրկնվում է: " + ", ".join(dup))
    names = {c for x in scenes for c in x["characters"]}
    out += [ln for ln in sp.qa_warnings(list(names), list({x["location"] for x in scenes})) if ln.startswith("- ")]
    return out


def write_corrections_md(path, name, report, auto, checks=()):
    L = [f"# {name}: սրբագրում / corrections", ""]
    if auto:
        L += ["**Ավտոմատ ուղղումներ (Word-ում նշված չեն):** " +
              ", ".join(f"{k}: {v}" for k, v in auto.items()), ""]
    if checks:
        L += ["## Ավտոմատ ստուգումներ (որոշում է խմբագիրը)", ""] + list(checks) + ["", "## Ուղղումներ", ""]
    by = {}
    for r in report:
        by[r.get("type", "")] = by.get(r.get("type", ""), 0) + 1
    L += ["**Ըստ տեսակի:** " + ", ".join(f"{k or '—'}: {v}" for k, v in by.items()), "",
          "| # | Տեսարան | Տեսակ | Էր | Դարձավ | Ինչու | Կարգավիճակ |", "|---|---|---|---|---|---|---|"]
    for r in report:
        def cell(x):
            return str(x or "").replace("|", "\\|").replace("\n", " ")
        L.append(f"| {r['id']} | {cell(r.get('scene'))} | {cell(r.get('type'))} | {cell(r.get('find'))} | "
                 f"{cell(r.get('replace')) if r.get('replace') not in (None, r.get('find')) else '—'} | "
                 f"{cell(r.get('why'))} | {r['status']} |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("corrections", nargs="?", help="JSON list (optional: without it only auto fixes run)")
    ap.add_argument("--out", help="output folder (default: next to the source)")
    ap.add_argument("--lang", default="hy")
    ap.add_argument("--paper", default="letter")
    ap.add_argument("--no-auto", action="store_true")
    ap.add_argument("--logo", help="logo PNG (default: assets/maghakian_logo_dark.png)")
    a = ap.parse_args()

    with open(a.src, encoding="utf-8-sig") as f:
        text = f.read()
    auto = {}
    if not a.no_auto:
        text, auto = auto_fixes(text)
    corrections = []
    if a.corrections:
        with open(a.corrections, encoding="utf-8") as f:
            corrections = json.load(f)
    clean, marked, comments, report = apply(text, corrections)

    outdir = a.out or os.path.dirname(os.path.abspath(a.src))
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.join(outdir, os.path.splitext(os.path.basename(a.src))[0])
    with open(stem + "_FINAL.fountain", "w", encoding="utf-8") as f:
        f.write(clean)
    with open(stem + "_marked.fountain", "w", encoding="utf-8") as f:
        f.write(marked)
    with open(stem + "_comments.json", "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=1)

    sp = [sys.executable, os.path.join(HERE, "screenplay.py")]
    common = ["--lang", a.lang, "--paper", a.paper] + (["--logo", a.logo] if a.logo else [])
    subprocess.run(sp + [stem + "_FINAL.fountain", "--pdf", "--docx", "--fdx", "--report", "--csv",
                         "--out", stem + "_FINAL"] + common, check=True)
    subprocess.run(sp + [stem + "_marked.fountain", "--docx", "--comments", stem + "_comments.json",
                         "--out", stem + "_WORK"] + common, check=True)
    sys.path.insert(0, HERE)
    write_corrections_md(stem + "_corrections.md", os.path.basename(a.src), report, auto, auto_checks(clean))
    for tmp in (stem + "_marked.fountain", stem + "_comments.json"):
        os.remove(tmp)
    ok = sum(1 for r in report if r["status"].startswith(("✅", "💬")))
    print(f"corrections applied: {ok}/{len(report)}; auto: {auto}")
    print("wrote", stem + "_WORK.docx", stem + "_FINAL.pdf", stem + "_corrections.md")


if __name__ == "__main__":
    sys.exit(main())
