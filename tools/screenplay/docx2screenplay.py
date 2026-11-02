"""Word script (Maghakian house styles) -> industry screenplay: Fountain, PDF, Final Draft (.fdx) + a check report.

Usage: python docx2screenplay.py SCRIPT.docx OUT_DIR [--title "..."] [--author "..."]

Reads the paragraph styles used in the studio's scripts (SCENE HEADING / NOTE / CHARACTER / DIALOG /
ACTION) and lays the text out in standard screenplay format (A4, 12 pt monospaced, standard indents,
scene numbers in both margins, (ՇԱՐ.) when a speech continues on the next page). The author's words
are not changed; only formatting: ",,," -> "…", /parentheticals/ -> (parentheticals).
"""
import re, sys, os, collections, argparse, html
import docx
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
TRANSITION_WORDS = ('ՊԵՐԵԽՈԴ', 'ԱՆՑՈՒՄ', 'ՕՐԸ ՓՈԽՎՈՒՄ Է', 'ՖԼԵՇԲԵՔ', 'ՄԹՆՈՒՄ', 'CUT TO', 'FADE')


def clean(t):
    t = t.replace(' ', ' ').strip()
    t = re.sub(r',{2,}', '…', t)
    t = re.sub(r'\.{3,}', '…', t)
    t = re.sub(r'\s+', ' ', t)
    return t


def parse(path):
    d = docx.Document(path)
    paras = [(p.style.name, clean(p.text)) for p in d.paragraphs if p.text.strip()]
    els = []          # (type, text, extra)
    i = 0
    scene_no = None
    while i < len(paras):
        st, t = paras[i]
        nxt = paras[i + 1] if i + 1 < len(paras) else (None, '')
        if st == 'SCENE HEADING':
            m = re.match(r'(\d+)', t)
            scene_no = m.group(1) if m else ''
            # gather the following NOTE lines: first = place/time, second = who is in the scene; a year may come first
            sub, j = [], i + 1
            year = None
            while j < len(paras) and (paras[j][0] == 'NOTE' or (paras[j][0] == 'CHARACTER' and re.fullmatch(r'\d{4}\s*Թ\.?', paras[j][1]))):
                if paras[j][0] == 'CHARACTER':
                    year = paras[j][1]
                else:
                    sub.append(paras[j][1])
                j += 1
            place = sub[0].rstrip('։.') if sub else t
            place = re.sub(r'\s*։\s*', ' — ', place) if '։' in place else place
            els.append(('scene', place.upper(), scene_no))
            if year:
                els.append(('super', re.sub(r'(\d{4})\s*Թ\.?', r'\1 Թ.', year), None))
            if len(sub) > 1:
                els.append(('cast', ', '.join(sub[1:]), None))
            i = j
            continue
        if st == 'CHARACTER':
            if nxt[0] == 'DIALOG':
                els.append(('character', t.upper(), None))
                dlg = nxt[1]
                m = re.match(r'^/([^/]+)/\s*(.*)$', dlg)
                if m:
                    els.append(('paren', '(' + m.group(1).strip() + ')', None))
                    dlg = m.group(2)
                dlg = re.sub(r'\s*/([^/]+)/\s*', lambda mm: ' (' + mm.group(1).strip() + ') ', dlg).strip()
                if dlg:
                    els.append(('dialogue', dlg, None))
                i += 2
                continue
            els.append(('transition', t.rstrip('։').upper() + ':', None))
            i += 1
            continue
        if st == 'DIALOG':   # dialogue without a character above it
            els.append(('dialogue', t, None))
        elif st == 'NOTE':
            els.append(('action', t, None))
        elif st == 'Normal' and i == 0:
            els.append(('title', t, None))
        else:
            els.append(('action', t, None))
        i += 1
    return els, paras


# ------------------------------------------------------------------ checks for the writer
def report(els, paras):
    out = []
    nums = [int(e[2]) for e in els if e[0] == 'scene' and e[2]]
    missing = sorted(set(range(min(nums), max(nums) + 1)) - set(nums)) if nums else []
    dup = [n for n, c in collections.Counter(nums).items() if c > 1]
    names = collections.Counter(e[1] for e in els if e[0] == 'character')
    out.append(f'- Տեսարաններ՝ {len(nums)} ({min(nums)}–{max(nums)})' if nums else '- Տեսարաններ չկան')
    if missing:
        out.append(f'- **Բացակայող տեսարանի համար՝ {", ".join(map(str, missing))}**')
    if dup:
        out.append(f'- **Կրկնվող համար՝ {", ".join(map(str, dup))}**')
    # near-duplicate character names (same letters, different spelling)
    def key(n):
        return re.sub(r'[ՈՒՒՎԵԷ]', '', n)
    groups = collections.defaultdict(list)
    for n in names:
        groups[key(n)].append(n)
    pairs = [g for g in groups.values() if len(g) > 1]
    import difflib
    flat = list(names)
    for a in flat:
        for b in flat:
            if a < b and difflib.SequenceMatcher(None, a, b).ratio() >= 0.75 and not any(a in g and b in g for g in pairs):
                pairs.append([a, b])
    for g in pairs:
        out.append('- **Անունը տարբեր ձևով է գրված՝ ' + ' / '.join(f'{n} ({names[n]})' for n in g) + '**')
    # cast lines naming people who never speak / speakers missing from the cast line
    out.append('\n**Ռեպլիկների քանակը**\n')
    for n, c in names.most_common():
        out.append(f'- {n}: {c}')
    return '\n'.join(out)


# ------------------------------------------------------------------ Fountain
def fountain(els, title, author):
    L = [f'Title: {title}', f'Credit: Written by', f'Author: {author}', '', '']
    for t, x, n in els:
        if t == 'title':
            continue
        if t == 'scene':
            L += [f'.{x} #{n}#', '']
        elif t in ('super', 'cast'):
            L += [f'!{x}', '']
        elif t == 'action':
            L += [f'!{x}', '']
        elif t == 'character':
            L += [f'@{x}']
        elif t == 'paren':
            L += [x]
        elif t == 'dialogue':
            L += [x, '']
        elif t == 'transition':
            L += [f'> {x}', '']
    return '\n'.join(L) + '\n'


# ------------------------------------------------------------------ Final Draft
def fdx(els, title):
    typ = dict(scene='Scene Heading', action='Action', super='Action', cast='Action', character='Character',
               paren='Parenthetical', dialogue='Dialogue', transition='Transition')
    P = []
    for t, x, n in els:
        if t == 'title':
            continue
        num = f' Number="{n}"' if t == 'scene' and n else ''
        P.append(f'    <Paragraph Type="{typ[t]}"{num}><Text>{html.escape(x)}</Text></Paragraph>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n<FinalDraft DocumentType="Script" Template="No" Version="5">\n'
            '  <Content>\n' + '\n'.join(P) + '\n  </Content>\n</FinalDraft>\n')


# ------------------------------------------------------------------ PDF
INCH = 72.0
PW, PH = A4
CW = 7.224        # DejaVu Sans Mono advance at 12 pt
LH = 12.0
TOP, BOTTOM = 1.0 * INCH, 1.0 * INCH
LAYOUT = {  # left (in), width (chars), style
    'scene': (1.5, 58, 'B'), 'action': (1.5, 60, ''), 'super': (1.5, 60, 'B'), 'cast': (1.5, 60, ''),
    'character': (3.7, 38, ''), 'paren': (3.1, 25, ''), 'dialogue': (2.5, 35, ''), 'transition': (1.5, 60, 'R'),
}


def wrap(text, width):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        while len(w) > width:
            lines.append(w[:width]); w = w[width:]
        if len(cur) + len(w) + (1 if cur else 0) <= width:
            cur = f'{cur} {w}' if cur else w
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines or ['']


def pdf(els, path, title, author):
    pdfmetrics.registerFont(TTFont('Mono', FONT))
    pdfmetrics.registerFont(TTFont('MonoB', FONT_B))
    c = rl_canvas.Canvas(path, pagesize=A4)
    c.setTitle(title)
    c.setAuthor(author)
    # title page
    c.setFont('MonoB', 14)
    c.drawCentredString(PW / 2, PH * 0.6, title.upper())
    c.setFont('Mono', 12)
    c.drawCentredString(PW / 2, PH * 0.6 - 36, 'Հեղինակ՝')
    c.drawCentredString(PW / 2, PH * 0.6 - 54, author)
    c.drawString(1.5 * INCH, 1.2 * INCH, 'Maghakian Scripts · maghakianscripts.com')
    c.showPage()
    # blocks: keep a character with its first lines; split long speeches with (ՇԱՐ.)
    blocks, cur = [], []
    for e in els:
        if e[0] == 'title':
            continue
        if e[0] in ('character', 'scene', 'action', 'super', 'cast', 'transition') and cur:
            blocks.append(cur); cur = []
        cur.append(e)
    if cur:
        blocks.append(cur)
    page = 1
    y = PH - TOP
    usable_bottom = BOTTOM

    def header():
        if page > 1:
            c.setFont('Mono', 12)
            c.drawRightString(PW - 1.0 * INCH, PH - 0.5 * INCH, f'{page}.')

    def lines_of(e):
        left, width, sty = LAYOUT[e[0]]
        return wrap(e[1], width)

    def draw_el(e, ln, y):
        left, width, sty = LAYOUT[e[0]]
        c.setFont('MonoB' if sty == 'B' else 'Mono', 12)
        if sty == 'R':
            c.drawRightString(PW - 1.0 * INCH, y, ln)
        else:
            c.drawString(left * INCH, y, ln)
        if e[0] == 'scene' and e[2]:
            c.setFont('MonoB', 12)
            c.drawString(0.9 * INCH, y, e[2])
            c.drawRightString(PW - 0.6 * INCH, y, e[2])

    header()
    prev_type = None
    for b in blocks:
        gap = 2 if b[0][0] == 'scene' else 1
        need = sum(len(lines_of(e)) for e in b) + gap
        if b[0][0] == 'scene':
            need = min(need, gap + 1 + 4)       # a heading needs at least a few lines after it
        if y - need * LH < usable_bottom and prev_type is not None:
            # long speech: split with (ՇԱՐ.)
            if b[0][0] == 'character' and sum(len(lines_of(e)) for e in b) > 6 and y - (gap + 4) * LH > usable_bottom:
                y -= gap * LH
                name = b[0][1]
                for e in b:
                    for ln in lines_of(e):
                        if y - 2 * LH < usable_bottom:
                            c.setFont('Mono', 12); c.drawString(3.7 * INCH, y, '(ՇԱՐ.)')
                            c.showPage(); page += 1; header(); y = PH - TOP
                            c.setFont('Mono', 12); c.drawString(3.7 * INCH, y, f'{name} (ՇԱՐ.)'); y -= LH
                        draw_el(e, ln, y); y -= LH
                prev_type = b[-1][0]
                continue
            c.showPage(); page += 1; header(); y = PH - TOP
        elif prev_type is not None:
            y -= gap * LH
        for e in b:
            for ln in lines_of(e):
                if y < usable_bottom:
                    c.showPage(); page += 1; header(); y = PH - TOP
                draw_el(e, ln, y); y -= LH
        prev_type = b[-1][0]
    c.save()
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docx'); ap.add_argument('out')
    ap.add_argument('--title', default=None); ap.add_argument('--author', default='Անի Մաղաքյան')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    els, paras = parse(a.docx)
    title = a.title or next((e[1] for e in els if e[0] == 'title'), os.path.splitext(os.path.basename(a.docx))[0])
    base = os.path.join(a.out, 'screenplay')
    open(base + '.fountain', 'w', encoding='utf-8').write(fountain(els, title, a.author))
    open(base + '.fdx', 'w', encoding='utf-8').write(fdx(els, title))
    pages = pdf(els, base + '.pdf', title, a.author)
    rep = f'# Ստուգում՝ {title}\n\n- Էջեր՝ {pages} (≈ {pages} րոպե էկրանային ժամանակ)\n' + report(els, paras) + '\n'
    open(base + '_report.md', 'w', encoding='utf-8').write(rep)
    print(rep)


if __name__ == '__main__':
    main()
