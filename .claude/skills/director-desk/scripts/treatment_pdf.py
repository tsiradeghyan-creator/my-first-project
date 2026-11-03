#!/usr/bin/env python3
"""Treatment / pitch deck: Markdown -> branded PDF (Maghakian look: black, white, graphite, one red).

Markdown format:
---
title: ԳԻՇԵՐԱՅԻՆ ԳՆԱՑՔ
format: Drama series · 8 × 45'
logline: One sentence.
cover: images/cover.jpg        # optional, relative to the .md
contact: maghakianscripts.com · hello@...
---
## Synopsis                    # every "##" starts a new page
Paragraphs, **bold**, *italic*.
- bullets
### Sub-heading
![](images/anna.jpg)           # first image of a section goes to the right column (if text is short)
> pull quote                    # big quote line, red bar

Usage: python3 treatment_pdf.py treatment.md [--out deck.pdf] [--layout deck|doc] [--logo logo.png]
  deck = A4 landscape, one idea per page (pitch deck)
  doc  = A4 portrait, flowing text (classic treatment)
  --compact = no black cover, title + format + logline on top of page 1, sections flow without
              page breaks (one-pager, synopsis, casting breakdown, lab application). Use with --layout doc.
"""
import argparse
import os
import re
import sys
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = next((d for d in (os.path.join(HERE, "..", "fonts"), HERE, "/mnt/data", os.getcwd())
                 if os.path.exists(os.path.join(d, "DejaVuSans.ttf"))), os.path.join(HERE, "..", "fonts"))
BLACK, WHITE, GRAPHITE, RED, GREY = "#000000", "#FFFFFF", "#111111", "#D90429", "#7A7A7A"


def parse_md(text):
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                meta[k.strip().lower()] = v.split(" #")[0].strip()
        text = text[m.end():]
    sections, cur = [], None
    for ln in text.splitlines():
        if ln.startswith("## "):
            cur = {"title": ln[3:].strip(), "items": []}
            sections.append(cur)
            continue
        if cur is None:
            cur = {"title": "", "items": []}
            sections.append(cur)
        cur["items"].append(ln)
    return meta, sections


def inline(s):
    s = escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"<i>\1</i>", s)
    return s


def main():
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
                                    Image, PageBreak, NextPageTemplate, Table, TableStyle,
                                    KeepTogether)
    from reportlab.lib.utils import ImageReader

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md")
    ap.add_argument("--out")
    ap.add_argument("--layout", choices=["deck", "doc"], default="deck")
    ap.add_argument("--logo", help="light (white) logo PNG for the black cover")
    ap.add_argument("--compact", action="store_true", help="no cover, sections flow (one-pager)")
    a = ap.parse_args()

    pdfmetrics.registerFont(TTFont("DD", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DD-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFontFamily("DD", normal="DD", bold="DD-B", italic="DD", boldItalic="DD-B")

    with open(a.md, encoding="utf-8") as f:
        meta, sections = parse_md(f.read())
    base = os.path.dirname(os.path.abspath(a.md))
    out = a.out or os.path.splitext(a.md)[0] + ".pdf"
    deck = a.layout == "deck"
    pw, ph = landscape(A4) if deck else A4
    M = 18 * mm

    def P(name, **kw):
        d = dict(fontName="DD", fontSize=14 if deck else 10.5, leading=20 if deck else 15,
                 textColor=HexColor(GRAPHITE), spaceAfter=7)
        d.update(kw)
        return ParagraphStyle(name, **d)

    st = {
        "h2": P("h2", fontName="DD-B", fontSize=32 if deck else 18, leading=38 if deck else 23,
                textColor=HexColor(BLACK), spaceAfter=4),
        "h3": P("h3", fontName="DD-B", fontSize=16 if deck else 12, leading=21 if deck else 16, textColor=HexColor(BLACK), spaceBefore=8, spaceAfter=3),
        "body": P("body"),
        "bullet": P("bullet", leftIndent=12, bulletIndent=0),
        "quote": P("quote", fontName="DD-B", fontSize=20 if deck else 14, leading=27 if deck else 19,
                   textColor=HexColor(BLACK), leftIndent=4, spaceBefore=6, spaceAfter=6),
    }

    def path_of(p):
        return p if os.path.isabs(p) else os.path.join(base, p)

    def cover(c, doc):
        c.saveState()
        c.setFillColor(HexColor(BLACK))
        c.rect(0, 0, pw, ph, stroke=0, fill=1)
        cv = meta.get("cover")
        if cv and os.path.exists(path_of(cv)):
            im = ImageReader(path_of(cv))
            w0, h0 = im.getSize()
            s = max(pw / w0, ph / h0)
            c.drawImage(im, (pw - w0 * s) / 2, (ph - h0 * s) / 2, w0 * s, h0 * s)
            c.setFillColor(HexColor(BLACK))
            c.setFillAlpha(0.55)
            c.rect(0, 0, pw, ph * 0.55, stroke=0, fill=1)
            c.setFillAlpha(1)
        c.setFillColor(HexColor(WHITE))
        c.setFont("DD-B", 40 if deck else 30)
        y = ph * 0.36
        c.drawString(M, y, meta.get("title", ""))
        # small red triangle accent (brand)
        c.setFillColor(HexColor(RED))
        t = 5 * mm
        x0 = M
        p = c.beginPath()
        ty = y + (19 if deck else 15) * mm
        p.moveTo(x0, ty); p.lineTo(x0 + t, ty); p.lineTo(x0 + t / 2, ty - t * 0.87); p.close()
        c.drawPath(p, stroke=0, fill=1)
        c.setFillColor(HexColor("#BBBBBB"))
        c.setFont("DD", 12)
        c.drawString(M, y - 10 * mm, meta.get("format", ""))
        lg = meta.get("logline", "")
        if lg:
            sty = ParagraphStyle("lg", fontName="DD", fontSize=14, leading=20, textColor=HexColor(WHITE))
            para = Paragraph(inline(lg), sty)
            w, h = para.wrap(pw * (0.62 if deck else 0.8), ph)
            para.drawOn(c, M, y - 16 * mm - h)
        c.setFont("DD", 8.5)
        c.setFillColor(HexColor("#999999"))
        c.drawString(M, 12 * mm, meta.get("contact", "Maghakian Scripts · maghakianscripts.com"))
        if a.logo and os.path.exists(a.logo):
            lr = ImageReader(a.logo)
            iw, ih = lr.getSize()
            lh = 9 * mm
            c.drawImage(lr, pw - M - lh * iw / ih, ph - M - lh, lh * iw / ih, lh, mask="auto")
        c.restoreState()

    def page(c, doc):
        c.saveState()
        c.setFillColor(HexColor(WHITE))
        c.rect(0, 0, pw, ph, stroke=0, fill=1)
        c.setFont("DD", 7.5)
        c.setFillColor(HexColor(GREY))
        c.drawString(M, 9 * mm, f"{meta.get('title', '')} · Maghakian Scripts")
        c.drawRightString(pw - M, 9 * mm, str(doc.page))
        c.setStrokeColor(HexColor(RED))
        c.setLineWidth(1.4)
        c.line(M, ph - M + 4 * mm, M + 16 * mm, ph - M + 4 * mm)
        c.restoreState()

    frame = Frame(M, 16 * mm, pw - 2 * M, ph - M - 16 * mm - 2 * mm, id="f", showBoundary=0)
    doc = BaseDocTemplate(out, pagesize=(pw, ph), leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=16 * mm,
                          title=meta.get("title", "Treatment"), author="Maghakian Scripts")
    if a.compact:
        doc.addPageTemplates([PageTemplate("body", [frame], onPage=page)])
        st["h2"] = P("h2c", fontName="DD-B", fontSize=12.5, leading=17, textColor=HexColor(BLACK),
                     spaceBefore=10, spaceAfter=3)
    else:
        doc.addPageTemplates([PageTemplate("cover", [Frame(0, 0, pw, ph, id="c")], onPage=cover),
                              PageTemplate("body", [frame], onPage=page)])
    fw, fh = frame._width, frame._height

    if a.compact:
        story = [Paragraph(inline(meta.get("title", "")), P("t", fontName="DD-B", fontSize=22, leading=27,
                                                            textColor=HexColor(BLACK), spaceAfter=2))]
        if meta.get("format"):
            story.append(Paragraph(inline(meta["format"]), P("f", fontSize=9.5, textColor=HexColor(GREY))))
        if meta.get("logline"):
            story.append(Table([[Paragraph(inline(meta["logline"]), P("lgc", fontName="DD-B", fontSize=11.5,
                                                                      leading=16, textColor=HexColor(BLACK)))]],
                               colWidths=[fw], style=TableStyle([("LINEBEFORE", (0, 0), (0, 0), 3, HexColor(RED)),
                                                                 ("LEFTPADDING", (0, 0), (0, 0), 10)])))
        story.append(Spacer(1, 4))
    else:
        story = [NextPageTemplate("body"), PageBreak()]
    first = True
    for sec in sections:
        if not sec["title"] and not any(x.strip() for x in sec["items"]):
            continue
        if not first and not a.compact:
            story.append(PageBreak())
        first = False
        flow, images, quotes = [], [], []
        para_buf = []

        def flush():
            if para_buf:
                flow.append(Paragraph(inline(" ".join(para_buf)), st["body"]))
                para_buf.clear()

        for ln in sec["items"]:
            s = ln.strip()
            mi = re.match(r"!\[[^\]]*\]\(([^)]+)\)", s)
            if not s:
                flush()
            elif mi:
                flush()
                images.append(mi.group(1))
            elif s.startswith("### "):
                flush()
                flow.append(Paragraph(inline(s[4:]), st["h3"]))
            elif s.startswith(("- ", "* ", "• ")):
                flush()
                flow.append(Paragraph(inline(s[2:]), st["bullet"], bulletText="•"))
            elif s.startswith(">"):
                flush()
                flow.append(Table([[Paragraph(inline(s.lstrip("> ")), st["quote"])]],
                                  colWidths=[fw * (0.9)],
                                  style=TableStyle([("LINEBEFORE", (0, 0), (0, 0), 3, HexColor(RED)),
                                                    ("LEFTPADDING", (0, 0), (0, 0), 10),
                                                    ("BOTTOMPADDING", (0, 0), (0, 0), 4)])))
                flow.append(Spacer(1, 10))
            else:
                para_buf.append(s)
        flush()

        head = ([Paragraph(inline(sec["title"]), st["h2"])] + ([] if a.compact else [Spacer(1, 6)])
                if sec["title"] else [])
        text_len = sum(len(x) for x in sec["items"])
        imgs_ok = [path_of(p) for p in images if os.path.exists(path_of(p))]

        def img_flow(p, maxw, maxh):
            ir = ImageReader(p)
            w0, h0 = ir.getSize()
            s = min(maxw / w0, maxh / h0)
            return Image(p, w0 * s, h0 * s)

        if imgs_ok and deck and text_len < 1400:
            colw = fw * 0.52
            right = [img_flow(imgs_ok[0], fw - colw - 8 * mm, fh - 30 * mm)]
            for extra in imgs_ok[1:3]:
                right.append(Spacer(1, 4))
                right.append(img_flow(extra, fw - colw - 8 * mm, (fh - 30 * mm) / 2))
            t = Table([[flow, right]], colWidths=[colw, fw - colw],
                      style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                        ("RIGHTPADDING", (0, 0), (0, 0), 8 * mm)]))
            story += head + [t]
        else:
            story += head + flow
            for p in imgs_ok:
                story.append(Spacer(1, 6))
                story.append(img_flow(p, fw, fh * 0.6))
    doc.build(story)
    print("wrote", out)


if __name__ == "__main__":
    sys.exit(main())
