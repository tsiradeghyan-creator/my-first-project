#!/usr/bin/env python3
"""Storyboard sheet: stills + shot data -> branded PDF (Storyboarder-style pages).

Input JSON:
{
  "title": "Tigran the Great", "subtitle": "Trailer v3 · block 09–16",
  "aspect": "16:9",                       # frame box aspect (16:9, 2.39:1, 9:16, 4:5 ...)
  "columns": 3, "rows": 2,                # optional grid (default 3x2; 9:16 -> 4x1)
  "shots": [
    {"id": "09", "image": "stills/09.jpg", "shot": "MWS → MS", "lens": "40mm",
     "move": "dolly push-in 1.5 m", "action": "King walks against the retreat",
     "duration": "5 s", "sound": "boots, distant fire", "note": "keep crown"}
  ]
}
Image paths are relative to the JSON file. Missing images get an empty frame (sketch it later).

Usage: python3 storyboard_sheet.py shots.json [--out board.pdf] [--paper a4|letter] [--logo logo.png]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")
BLACK, GRAPHITE, RED, GREY = "#000000", "#111111", "#D90429", "#8A8A8A"
FIELDS = [("shot", "Shot"), ("lens", "Lens"), ("move", "Move"), ("action", "Action"),
          ("duration", "Time"), ("sound", "Sound"), ("note", "Note")]


def shrink(path, max_px):
    """Downscale a still to ~220 dpi for its frame box so the PDF stays light."""
    import io
    from PIL import Image
    im = Image.open(path)
    im = im.convert("RGB")
    if im.width > max_px:
        im = im.resize((max_px, round(im.height * max_px / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    buf.seek(0)
    return buf


def aspect_ratio(s):
    a, b = s.replace("x", ":").split(":")
    return float(a) / float(b)


def main():
    from reportlab.lib.pagesizes import A4, letter, landscape
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from xml.sax.saxutils import escape

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json")
    ap.add_argument("--out")
    ap.add_argument("--paper", choices=["a4", "letter"], default="a4")
    ap.add_argument("--logo", help="PNG logo for the header (dark logo on white)")
    a = ap.parse_args()

    pdfmetrics.registerFont(TTFont("DD", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DD-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFontFamily("DD", normal="DD", bold="DD-B", italic="DD", boldItalic="DD-B")

    with open(a.json, encoding="utf-8") as f:
        data = json.load(f)
    base = os.path.dirname(os.path.abspath(a.json))
    shots = data["shots"]
    ar = aspect_ratio(data.get("aspect", "16:9"))
    vertical = ar < 1
    cols = int(data.get("columns", 4 if vertical else 3))
    rows = int(data.get("rows", 1 if vertical else 2))
    out = a.out or os.path.splitext(a.json)[0] + ".pdf"

    pw, ph = landscape(A4 if a.paper == "a4" else letter)
    c = canvas.Canvas(out, pagesize=(pw, ph))
    c.setTitle(f"{data.get('title', 'Storyboard')} · storyboard")
    margin, header_h, footer_h, gap = 12 * mm, 16 * mm, 8 * mm, 6 * mm
    cell_w = (pw - 2 * margin - (cols - 1) * gap) / cols
    cell_h = (ph - 2 * margin - header_h - footer_h - (rows - 1) * gap) / rows
    img_w = cell_w
    img_h = img_w / ar
    max_img_h = cell_h * (0.72 if vertical else 0.58)
    if img_h > max_img_h:
        img_h = max_img_h
        img_w = img_h * ar

    body = ParagraphStyle("b", fontName="DD", fontSize=7.4, leading=9.2, textColor=HexColor(GRAPHITE))
    per_page = cols * rows
    pages = max(1, -(-len(shots) // per_page))

    for p in range(pages):
        # header
        top = ph - margin
        c.setFillColor(HexColor(BLACK))
        c.setFont("DD-B", 15)
        c.drawString(margin, top - 8 * mm, data.get("title", "Storyboard"))
        c.setFont("DD", 9)
        c.setFillColor(HexColor(GREY))
        c.drawString(margin, top - 13 * mm, data.get("subtitle", ""))
        c.setFillColor(HexColor(BLACK))
        if a.logo and os.path.exists(a.logo):
            lr = ImageReader(a.logo)
            iw, ih = lr.getSize()
            lh = 8 * mm
            c.drawImage(lr, pw - margin - lh * iw / ih, top - 10 * mm, lh * iw / ih, lh, mask="auto")
        else:
            c.setFont("DD-B", 9)
            c.drawRightString(pw - margin, top - 8 * mm, "STORYBOARD")
        c.setStrokeColor(HexColor(RED))
        c.setLineWidth(1.2)
        c.line(margin, top - header_h + 1 * mm, margin + 18 * mm, top - header_h + 1 * mm)
        c.setStrokeColor(HexColor("#DDDDDD"))
        c.setLineWidth(0.4)
        c.line(margin + 18 * mm, top - header_h + 1 * mm, pw - margin, top - header_h + 1 * mm)

        for k, shot in enumerate(shots[p * per_page:(p + 1) * per_page]):
            r, col = divmod(k, cols)
            x = margin + col * (cell_w + gap)
            y_top = top - header_h - 3 * mm - r * (cell_h + gap)
            ix = x + (cell_w - img_w) / 2
            iy = y_top - img_h
            # frame
            c.setFillColor(HexColor("#F2F2F2"))
            c.rect(ix, iy, img_w, img_h, stroke=0, fill=1)
            path = shot.get("image")
            if path:
                full = path if os.path.isabs(path) else os.path.join(base, path)
                if os.path.exists(full):
                    im = ImageReader(shrink(full, int(img_w / 72 * 220)))
                    w0, h0 = im.getSize()
                    # cover-crop into the frame box
                    scale = max(img_w / w0, img_h / h0)
                    dw, dh = w0 * scale, h0 * scale
                    c.saveState()
                    pth = c.beginPath()
                    pth.rect(ix, iy, img_w, img_h)
                    c.clipPath(pth, stroke=0, fill=0)
                    c.drawImage(im, ix + (img_w - dw) / 2, iy + (img_h - dh) / 2, dw, dh)
                    c.restoreState()
            c.setStrokeColor(HexColor(BLACK))
            c.setLineWidth(0.6)
            c.rect(ix, iy, img_w, img_h, stroke=1, fill=0)
            # shot number tag
            tag = str(shot.get("id", p * per_page + k + 1))
            c.setFont("DD-B", 8.5)
            tw = c.stringWidth(tag, "DD-B", 8.5) + 4 * mm
            c.setFillColor(HexColor(RED))
            c.rect(ix, iy + img_h - 5.5 * mm, tw, 5.5 * mm, stroke=0, fill=1)
            c.setFillColor(HexColor("#FFFFFF"))
            c.drawString(ix + 2 * mm, iy + img_h - 4 * mm, tag)
            if shot.get("duration"):
                d = str(shot["duration"])
                dw_ = c.stringWidth(d, "DD-B", 8) + 4 * mm
                c.setFillColor(HexColor(BLACK))
                c.rect(ix + img_w - dw_, iy, dw_, 5 * mm, stroke=0, fill=1)
                c.setFillColor(HexColor("#FFFFFF"))
                c.setFont("DD-B", 8)
                c.drawString(ix + img_w - dw_ + 2 * mm, iy + 1.6 * mm, d)
            # text
            parts = []
            for key, label in FIELDS:
                if key == "duration" or not shot.get(key):
                    continue
                parts.append(f"<b>{label}</b>  {escape(str(shot[key]))}")
            para = Paragraph("<br/>".join(parts), body)
            tw_, th_ = para.wrap(img_w, iy - (y_top - cell_h) - 2.5 * mm)
            if th_ > iy - (y_top - cell_h) - 2.5 * mm:
                # shrink to fit
                small = ParagraphStyle("s", parent=body, fontSize=6.4, leading=7.8)
                para = Paragraph("<br/>".join(parts), small)
                tw_, th_ = para.wrap(img_w, 999)
            para.drawOn(c, ix, iy - 2.5 * mm - th_)

        # footer
        c.setFont("DD", 7)
        c.setFillColor(HexColor(GREY))
        c.drawString(margin, margin - 2 * mm, "Maghakian Scripts")
        c.drawRightString(pw - margin, margin - 2 * mm, f"{p + 1} / {pages}")
        c.showPage()
    c.save()
    print("wrote", out, f"({len(shots)} shots, {pages} pages)")


if __name__ == "__main__":
    sys.exit(main())
