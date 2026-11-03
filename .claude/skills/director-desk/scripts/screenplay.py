#!/usr/bin/env python3
"""Fountain screenplay -> industry-format PDF ("American" format), DOCX, FDX,
plus a line-producer breakdown (scenes, page eighths, characters, locations).

Works for Armenian, Russian and English (bundled FreeMono = Courier metrics
with Armenian + Cyrillic glyphs).

Usage:
  python3 screenplay.py script.fountain --pdf                 # script.pdf
  python3 screenplay.py script.fountain --all --lang hy       # pdf+docx+fdx+report+csv
  python3 screenplay.py script.fountain --pdf --paper a4 --scene-numbers
"""
import argparse
import csv
import math
import os
import re
import sys
import textwrap
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")

LABELS = {
    "en": {"more": "(MORE)", "contd": "(CONT'D)", "by": "Written by"},
    "ru": {"more": "(ДАЛЬШЕ)", "contd": "(ПРОД.)", "by": "Автор сценария"},
    "hy": {"more": "(ՇԱՐՈՒՆԱԿԵԼԻ)", "contd": "(ՇԱՐ.)", "by": "Սցենարի հեղինակ"},
}

SCENE_RE = re.compile(
    r"^(INT\.?/EXT|INT/EXT|I/E|INT|EXT|EST|"
    r"ИНТ\.?/НАТ|ИНТ|НАТ|ЭКСТ|"
    r"ԻՆՏ\.?/ԷՔՍՏ|ԻՆՏ|ԷՔՍՏ|ՆԵՐՍ\.?/ԴՐՍ|ՆԵՐՍ|ԴՐՍ)[\.\s]",
    re.IGNORECASE,
)
SCENE_NUM_RE = re.compile(r"\s*#([\w.\-]+)#\s*$")

# Layout (inches from the page's left edge). Courier 12 pt = 10 chars/inch, 6 lines/inch.
X = {"scene": 1.5, "action": 1.5, "character": 3.7, "parenthetical": 3.1,
     "dialogue": 2.5, "transition": None, "centered": None}
WIDTH = {"scene": 60, "action": 60, "character": 38, "parenthetical": 24,
         "dialogue": 35, "transition": 60, "centered": 60}
SPACE_BEFORE = {"scene": 1, "action": 1, "character": 1, "transition": 1, "centered": 1}
PAPER = {"letter": (8.5, 11.0), "a4": (8.27, 11.69)}


# ---------------------------------------------------------------- parsing
def clean_inline(s):
    s = re.sub(r"\\([*_])", "\x00\\1", s)
    s = re.sub(r"(\*{1,3}|_)(?=\S)(.+?)(?<=\S)\1", r"\2", s)
    return s.replace("\x00", "")


def is_character_line(line):
    if line.startswith("@"):
        return True
    name = re.sub(r"\(.*?\)", "", line).replace("^", "").strip()
    return (bool(name) and any(c.isalpha() for c in name) and name == name.upper()
            and len(name) <= 40 and not name.endswith(":") and not SCENE_RE.match(name))


def parse(text):
    text = text.replace("\r\n", "\n").replace("\t", "    ")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)        # boneyard
    text = re.sub(r"\[\[.*?\]\]", "", text, flags=re.S)       # notes
    lines = text.split("\n")

    title = {}
    i = 0
    if lines and re.match(r"^[A-Za-zА-Яа-яԱ-Ֆա-ֆ][^:]{0,30}:", lines[0].strip()):
        key = None
        while i < len(lines) and lines[i].strip():
            ln = lines[i]
            m = re.match(r"^([^:\s][^:]{0,30}):\s*(.*)$", ln)
            if m and not ln.startswith((" ", "\t")):
                key = m.group(1).strip().lower()
                title[key] = [m.group(2).strip()] if m.group(2).strip() else []
            elif key:
                title[key].append(ln.strip())
            i += 1

    blocks = []
    prev_blank = True
    n = len(lines)
    while i < n:
        raw = lines[i].rstrip()
        s = raw.strip()
        nxt_blank = i + 1 >= n or not lines[i + 1].strip()
        if not s:
            prev_blank = True
            i += 1
            continue
        if re.fullmatch(r"={3,}", s):
            blocks.append({"type": "page_break"})
        elif s.startswith("#"):
            blocks.append({"type": "section", "text": s.lstrip("#").strip(),
                           "level": len(s) - len(s.lstrip("#"))})
        elif s.startswith("=") and not s.startswith("=="):
            blocks.append({"type": "synopsis", "text": s[1:].strip()})
        elif (s.startswith(".") and not s.startswith("..")) or (prev_blank and SCENE_RE.match(s)):
            h = s[1:] if s.startswith(".") else s
            num = None
            m = SCENE_NUM_RE.search(h)
            if m:
                num, h = m.group(1), h[:m.start()]
            blocks.append({"type": "scene", "text": clean_inline(h.strip()).upper(), "number": num})
        elif s.startswith(">") and s.endswith("<"):
            blocks.append({"type": "centered", "text": clean_inline(s[1:-1].strip())})
        elif s.startswith(">"):
            blocks.append({"type": "transition", "text": clean_inline(s[1:].strip()).upper()})
        elif (prev_blank and nxt_blank and s == s.upper() and s.endswith(("TO:", "ЗТМ.", "ЗТМ:"))
              and not s.startswith("!")):
            blocks.append({"type": "transition", "text": s})
        elif not s.startswith("!") and prev_blank and not nxt_blank and is_character_line(s):
            name = s[1:] if s.startswith("@") else s
            dual = name.endswith("^")
            name = name.rstrip("^").strip()
            dlg = {"type": "dialogue_block", "character": name, "lines": [], "dual": dual}
            i += 1
            while i < n and lines[i].strip():
                t = lines[i].strip()
                if t.startswith("(") and t.endswith(")"):
                    dlg["lines"].append(("parenthetical", clean_inline(t)))
                else:
                    dlg["lines"].append(("dialogue", clean_inline(t)))
                i += 1
            blocks.append(dlg)
            prev_blank = False
            continue
        else:
            buf = []
            while i < n and lines[i].strip():
                t = lines[i].rstrip()
                t = t[1:] if t.lstrip().startswith(("!", "~")) and t.lstrip() == t else t
                buf.append(clean_inline(t.strip()) if not t.startswith("    ") else clean_inline(t))
                i += 1
            blocks.append({"type": "action", "lines": buf})
            prev_blank = False
            continue
        prev_blank = False
        i += 1

    # number scenes
    k = 0
    for b in blocks:
        if b["type"] == "scene":
            k += 1
            if not b.get("number"):
                b["number"] = str(k)
    return title, blocks


def char_name(cue):
    return re.sub(r"\(.*?\)", "", cue).replace("^", "").strip()


def split_heading(h):
    ie = ""
    m = SCENE_RE.match(h)
    rest = h
    if m:
        ie = m.group(1).upper()
        rest = h[m.end():].strip(" .")
    parts = re.split(r"\s+[-–—]\s+", rest)
    loc = parts[0].strip()
    tod = parts[-1].strip() if len(parts) > 1 else ""
    return ie, loc, tod


# ---------------------------------------------------------------- pagination
def wrap(text, width):
    if not text:
        return [""]
    return textwrap.wrap(text, width, break_long_words=True, break_on_hyphens=False) or [""]


def paginate(blocks, lines_per_page, labels):
    """Returns pages: list of rows. Row = (kind, text, scene_idx) or None for blank."""
    pages, page = [], []
    scene_idx = -1

    def room():
        return lines_per_page - len(page)

    def new_page():
        nonlocal page
        pages.append(page)
        page = []

    def sp(kind):
        return 0 if not page else SPACE_BEFORE.get(kind, 0)

    def put(rows):
        for r in rows:
            page.append(r)

    renderable = [b for b in blocks if b["type"] not in ("section", "synopsis")]
    for bi, b in enumerate(renderable):
        t = b["type"]
        if t == "page_break":
            if page:
                new_page()
            continue
        if t == "scene":
            scene_idx += 1
            rows = [("scene", ln, scene_idx) for ln in wrap(b["text"], WIDTH["scene"])]
            need = sp("scene") + len(rows) + 2
            if room() < need:
                new_page()
            put([None] * sp("scene"))
            put(rows)
            continue
        if t in ("action", "transition", "centered"):
            if t == "action":
                rows = []
                for ln in b["lines"]:
                    rows += [("action", w, scene_idx) for w in wrap(ln, WIDTH["action"])]
            else:
                rows = [(t, w, scene_idx) for w in wrap(b["text"], WIDTH[t])]
            s = sp(t)
            if room() >= s + len(rows):
                put([None] * s)
                put(rows)
            elif t == "action" and room() - s >= 2 and len(rows) - (room() - s) >= 2:
                k = room() - s
                put([None] * s)
                put(rows[:k])
                new_page()
                put(rows[k:])
            else:
                new_page()
                put(rows)
            continue
        if t == "dialogue_block":
            cue = b["character"]
            body = []
            for kind, txt in b["lines"]:
                body += [(kind, w, scene_idx) for w in wrap(txt, WIDTH[kind])]
            head = [("character", cue, scene_idx)]
            s = sp("character")
            if room() >= s + 1 + len(body):
                put([None] * s)
                put(head + body)
                continue
            avail = room() - s - 1 - 1  # cue + (MORE)
            if avail >= 2 and len(body) - avail >= 1:
                # split on a dialogue line, not right after a parenthetical
                k = avail
                while k > 1 and body[k - 1][0] == "parenthetical":
                    k -= 1
                put([None] * s)
                put(head + body[:k] + [("more", labels["more"], scene_idx)])
                new_page()
                contd = labels["contd"]
                put([("character", f"{char_name(cue)} {contd}", scene_idx)] + body[k:])
            else:
                new_page()
                put(head + body)
    if page:
        pages.append(page)
    return pages


# ---------------------------------------------------------------- PDF
def register_font():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont("ScriptMono", os.path.join(FONT_DIR, "FreeMono.ttf")))
    return "ScriptMono"


def write_pdf(path, title, blocks, pages, paper, scene_numbers, labels):
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    font = register_font()
    pw, ph = PAPER[paper]
    c = canvas.Canvas(path, pagesize=(pw * inch, ph * inch))
    meta_title = " ".join(title.get("title", [])) or os.path.splitext(os.path.basename(path))[0]
    c.setTitle(meta_title)
    c.setAuthor(", ".join(title.get("author", title.get("authors", []))))
    lh = 12  # pt per line
    right_edge = pw - 1.0

    def text_at(x_in, y_pt, s):
        c.drawString(x_in * inch, y_pt, s)

    def right_at(x_in, y_pt, s):
        c.drawRightString(x_in * inch, y_pt, s)

    def center_at(y_pt, s, x0=1.5, x1=None):
        x1 = x1 if x1 is not None else right_edge
        c.drawCentredString((x0 + x1) / 2 * inch, y_pt, s)

    # title page
    if title:
        c.setFont(font, 12)
        y = ph * inch * 0.62
        for ln in title.get("title", []):
            center_at(y, clean_inline(ln).upper())
            y -= lh
        y -= lh * 2
        credit = title.get("credit", [labels["by"]])
        for ln in credit:
            center_at(y, ln)
            y -= lh
        y -= lh
        for ln in title.get("author", title.get("authors", [])):
            center_at(y, ln)
            y -= lh
        for key in ("source", "notes"):
            for ln in title.get(key, []):
                y -= lh
                center_at(y, ln)
        y = 1.0 * inch + lh * 4
        for ln in title.get("contact", []):
            text_at(1.5, y, ln)
            y -= lh
        y = 1.0 * inch + lh * 4
        for key in ("draft date", "date"):
            for ln in title.get(key, []):
                right_at(right_edge, y, ln)
                y -= lh
        c.showPage()

    top = ph * inch - 1.0 * inch
    for pi, rows in enumerate(pages, start=1):
        c.setFont(font, 12)
        if pi > 1:
            right_at(right_edge, ph * inch - 0.5 * inch, f"{pi}.")
        y = top - lh  # first baseline
        for r in rows:
            if r is not None:
                kind, txt, sidx = r
                if kind in ("transition",):
                    right_at(right_edge, y, txt)
                elif kind == "centered":
                    center_at(y, txt)
                elif kind == "more":
                    text_at(X["character"], y, txt)
                else:
                    text_at(X[kind], y, txt)
                if kind == "scene" and scene_numbers and _first_scene_row(rows, r):
                    num = _scene_number(blocks, sidx)
                    right_at(1.3, y, num)
                    text_at(right_edge + 0.15, y, num)
            y -= lh
        c.showPage()
    c.save()


def _first_scene_row(rows, r):
    for x in rows:
        if x is not None and x[0] == "scene" and x[2] == r[2]:
            return x is r
    return False


def _scene_number(blocks, sidx):
    scenes = [b for b in blocks if b["type"] == "scene"]
    return scenes[sidx]["number"] if 0 <= sidx < len(scenes) else ""


# ---------------------------------------------------------------- DOCX / FDX
def write_docx(path, title, blocks, font_name):
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin, sec.right_margin = Inches(1.5), Inches(1.0)
    sec.top_margin, sec.bottom_margin = Inches(1.0), Inches(1.0)
    st = doc.styles["Normal"]
    st.font.name = font_name
    st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    st.paragraph_format.space_after = Pt(0)
    st.paragraph_format.space_before = Pt(0)
    st.paragraph_format.line_spacing = Pt(12)

    def para(text, left=0.0, right=0.0, before=0, align=None):
        p = doc.add_paragraph(text)
        f = p.paragraph_format
        f.left_indent, f.right_indent = Inches(left), Inches(right)
        f.space_before = Pt(12 * before)
        if align:
            p.alignment = align
        return p

    if title:
        for _ in range(18):
            doc.add_paragraph("")
        for ln in title.get("title", []):
            para(clean_inline(ln).upper(), align=WD_ALIGN_PARAGRAPH.CENTER)
        for ln in title.get("credit", []):
            para(ln, before=2, align=WD_ALIGN_PARAGRAPH.CENTER)
        for ln in title.get("author", title.get("authors", [])):
            para(ln, before=1, align=WD_ALIGN_PARAGRAPH.CENTER)
        doc.add_page_break()

    for b in blocks:
        t = b["type"]
        if t == "scene":
            para(b["text"], before=1)
        elif t == "action":
            para("\n".join(b["lines"]), before=1)
        elif t == "transition":
            para(b["text"], before=1, align=WD_ALIGN_PARAGRAPH.RIGHT)
        elif t == "centered":
            para(b["text"], before=1, align=WD_ALIGN_PARAGRAPH.CENTER)
        elif t == "page_break":
            doc.add_page_break()
        elif t == "dialogue_block":
            para(b["character"], left=2.2, before=1)
            for kind, txt in b["lines"]:
                if kind == "parenthetical":
                    para(txt, left=1.6, right=1.9)
                else:
                    para(txt, left=1.0, right=1.5)
    doc.save(path)


def write_fdx(path, title, blocks):
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="no" ?>',
           '<FinalDraft DocumentType="Script" Template="No" Version="5">', "<Content>"]

    def p(kind, text, number=None):
        attr = f' Number="{escape(number)}"' if number else ""
        out.append(f'<Paragraph Type="{kind}"{attr}><Text>{escape(text)}</Text></Paragraph>')

    for b in blocks:
        t = b["type"]
        if t == "scene":
            p("Scene Heading", b["text"], b.get("number"))
        elif t == "action":
            p("Action", "\n".join(b["lines"]))
        elif t == "transition":
            p("Transition", b["text"])
        elif t == "centered":
            p("Action", b["text"])
        elif t == "dialogue_block":
            p("Character", b["character"])
            for kind, txt in b["lines"]:
                p("Parenthetical" if kind == "parenthetical" else "Dialogue", txt)
    out.append("</Content>")
    if title:
        out.append("<TitlePage><Content>")
        for key in ("title", "credit", "author", "authors", "draft date", "contact"):
            for ln in title.get(key, []):
                out.append(f'<Paragraph Type="General" Alignment="Center"><Text>{escape(ln)}</Text></Paragraph>')
        out.append("</Content></TitlePage>")
    out.append("</FinalDraft>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))


# ---------------------------------------------------------------- breakdown
def eighths_str(e):
    whole, rest = divmod(e, 8)
    if whole and rest:
        return f"{whole} {rest}/8"
    if whole:
        return f"{whole}"
    return f"{rest}/8"


def breakdown(blocks, pages, lines_per_page):
    scenes = [b for b in blocks if b["type"] == "scene"]
    rows_per_scene, first_page = {}, {}
    for pi, rows in enumerate(pages, start=1):
        for r in rows:
            if r is not None and r[2] >= 0:
                rows_per_scene[r[2]] = rows_per_scene.get(r[2], 0) + 1
                first_page.setdefault(r[2], pi)
    # attach characters / synopsis to scenes
    cur, chars, syn = -1, {}, {}
    for b in blocks:
        if b["type"] == "scene":
            cur += 1
            chars[cur] = []
        elif b["type"] == "dialogue_block" and cur >= 0:
            nm = char_name(b["character"])
            if nm not in chars[cur]:
                chars[cur].append(nm)
        elif b["type"] == "synopsis" and cur >= 0:
            syn.setdefault(cur, b["text"])
    out = []
    for idx, sc in enumerate(scenes):
        ie, loc, tod = split_heading(sc["text"])
        n = rows_per_scene.get(idx, 1)
        e = max(1, math.ceil(n / lines_per_page * 8))
        out.append({"number": sc["number"], "heading": sc["text"], "int_ext": ie, "location": loc,
                    "time": tod, "page": first_page.get(idx, ""), "eighths": e,
                    "length": eighths_str(e), "characters": chars.get(idx, []),
                    "synopsis": syn.get(idx, "")})
    return out


def write_report(path, title, blocks, pages, scenes, lang):
    name = " ".join(title.get("title", [])) or "Script"
    total_e = sum(s["eighths"] for s in scenes)
    char_scenes, char_lines = {}, {}
    for b in blocks:
        if b["type"] == "dialogue_block":
            nm = char_name(b["character"])
            char_lines[nm] = char_lines.get(nm, 0) + sum(1 for k, _ in b["lines"] if k == "dialogue")
    for s in scenes:
        for c in s["characters"]:
            char_scenes[c] = char_scenes.get(c, 0) + 1
    locs = {}
    for s in scenes:
        key = (s["location"] or "?")
        d = locs.setdefault(key, {"scenes": 0, "eighths": 0, "ie": set(), "time": set()})
        d["scenes"] += 1
        d["eighths"] += s["eighths"]
        d["ie"].add(s["int_ext"])
        if s["time"]:
            d["time"].add(s["time"])
    L = [f"# {name}: breakdown", "",
         f"- Pages: **{len(pages)}** (≈ {len(pages)} min on screen, 1 page ≈ 1 minute)",
         f"- Scenes: **{len(scenes)}**, total length {eighths_str(total_e)} pages (in eighths)",
         f"- Speaking characters: **{len(char_scenes)}**, locations: **{len(locs)}**", "",
         "## Characters", "", "| Character | Scenes | Dialogue lines |", "|---|---|---|"]
    for c in sorted(char_scenes, key=lambda x: (-char_scenes[x], x)):
        L.append(f"| {c} | {char_scenes[c]} | {char_lines.get(c, 0)} |")
    L += ["", "## Locations", "", "| Location | INT/EXT | Time | Scenes | Pages |", "|---|---|---|---|---|"]
    for k in sorted(locs, key=lambda x: (-locs[x]["eighths"], x)):
        d = locs[k]
        L.append(f"| {k} | {'/'.join(sorted(x for x in d['ie'] if x))} | {', '.join(sorted(d['time']))} "
                 f"| {d['scenes']} | {eighths_str(d['eighths'])} |")
    L += ["", "## Scenes", "", "| # | Heading | Page | Length | Characters |", "|---|---|---|---|---|"]
    for s in scenes:
        L.append(f"| {s['number']} | {s['heading']} | {s['page']} | {s['length']} | {', '.join(s['characters'])} |")
        if s["synopsis"]:
            L.append(f"|  | _{s['synopsis']}_ |  |  |  |")
    sections = [b for b in blocks if b["type"] == "section"]
    if sections:
        L += ["", "## Structure (sections)", ""]
        for b in sections:
            L.append("  " * (b["level"] - 1) + f"- {b['text']}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def write_csv(path, scenes):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["scene", "int_ext", "location", "time", "page", "eighths", "length", "characters", "synopsis"])
        for s in scenes:
            w.writerow([s["number"], s["int_ext"], s["location"], s["time"], s["page"], s["eighths"],
                        s["length"], "; ".join(s["characters"]), s["synopsis"]])


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help=".fountain (or .txt in Fountain syntax)")
    ap.add_argument("--out", help="output path stem (default: next to source)")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--docx", action="store_true")
    ap.add_argument("--fdx", action="store_true")
    ap.add_argument("--report", action="store_true", help="breakdown .md")
    ap.add_argument("--csv", action="store_true", help="scene breakdown .csv (stripboard/schedule)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--paper", choices=PAPER, default="letter")
    ap.add_argument("--lang", choices=LABELS, default="hy", help="labels for (MORE)/(CONT'D)")
    ap.add_argument("--scene-numbers", action="store_true")
    ap.add_argument("--docx-font", default="Courier New")
    a = ap.parse_args()
    if not any([a.pdf, a.docx, a.fdx, a.report, a.csv, a.all]):
        a.pdf = True
    if a.all:
        a.pdf = a.docx = a.fdx = a.report = a.csv = True

    with open(a.src, encoding="utf-8-sig") as f:
        title, blocks = parse(f.read())
    labels = LABELS[a.lang]
    lpp = int(round((PAPER[a.paper][1] - 2.0) * 6))
    pages = paginate(blocks, lpp, labels)
    scenes = breakdown(blocks, pages, lpp)
    stem = a.out or os.path.splitext(a.src)[0]
    made = []
    if a.pdf:
        write_pdf(stem + ".pdf", title, blocks, pages, a.paper, a.scene_numbers, labels); made.append(stem + ".pdf")
    if a.docx:
        write_docx(stem + ".docx", title, blocks, a.docx_font); made.append(stem + ".docx")
    if a.fdx:
        write_fdx(stem + ".fdx", title, blocks); made.append(stem + ".fdx")
    if a.report:
        write_report(stem + "_breakdown.md", title, blocks, pages, scenes, a.lang); made.append(stem + "_breakdown.md")
    if a.csv:
        write_csv(stem + "_breakdown.csv", scenes); made.append(stem + "_breakdown.csv")
    print(f"pages={len(pages)} scenes={len(scenes)} est_runtime≈{len(pages)} min")
    for m in made:
        print("wrote", m)


if __name__ == "__main__":
    sys.exit(main())
