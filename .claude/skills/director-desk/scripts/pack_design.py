#!/usr/bin/env python3
"""Maghakian document design system for the Script Pack: HTML + CSS -> PDF through headless Chromium.

Brand: black #000, white #FFF, graphite #111, one red accent #D90429. Noto Serif Armenian for titles,
Noto Sans Armenian for text (Latin/Cyrillic fall back to Noto Serif / Noto Sans). Handwritten logo PNGs.
Two page systems: A4 documents (running header with the recipient, footer with page numbers) and
16:9 decks (one idea per slide, text auto-fits its box).
"""
import base64
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def _asset_dir(sub, name):
    for d in (os.path.join(HERE, "..", sub), HERE, "/mnt/data", os.getcwd()):
        if os.path.exists(os.path.join(d, name)):
            return os.path.abspath(d)
    return os.path.abspath(os.path.join(HERE, "..", sub))


FONTS = _asset_dir("fonts", "NotoSansArmenian.ttf")
ASSETS = _asset_dir("assets", "maghakian_logo_dark.png")


def _logo(kind):
    p = os.path.join(ASSETS, f"maghakian_logo_{kind}.png")
    if not os.path.exists(p):
        return ""
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


# ---------------------------------------------------------------- labels
LBL = {
    "hy": {
        "synopsis": "Համառոտ բովանդակություն", "synopsis_long": "Ընդարձակ բովանդակություն", "characters": "Կերպարներ",
        "why_now": "Ինչու հիմա", "comps": "Համեմատելի նախագծեր", "scale": "Արտադրության ծավալ", "logline": "Լոգլայն",
        "world": "Աշխարհը", "tone": "Տոն և ոճ", "season_arc": "Սեզոնի աղեղ", "episodes": "Սերիաներ",
        "audience": "Լսարան", "team": "Թիմ", "pages": "էջ", "scenes": "տեսարան", "sets": "լոկացիա",
        "roles": "խոսող դեր", "minutes": "րոպե", "episodes_n": "սերիա", "lines": "ռեպլիկ", "words": "բառ",
        "lead": "Գլխավոր", "supporting": "Երկրորդական", "day player": "Էպիզոդիկ", "non-speaking": "Առանց խոսքի",
        "episode": "Սերիա", "scene": "Տեսարան", "length": "Երկարություն", "time": "Ժամանակ", "cast": "Կերպարներ",
        "content": "Բովանդակություն", "location": "Լոկացիա", "ie": "Ներս/Դրս", "int": "Ներս", "ext": "Դրս",
        "day": "Ցերեկ", "night": "Գիշեր/երեկո", "age": "Տարիք", "role": "Դեր", "eps": "Սերիաներ",
        "overview": "Տեսարանների ցանկ", "breakdown": "Արտադրական breakdown", "casting": "Կաստինգ breakdown",
        "contents": "Փաթեթի բովանդակություն", "recipient": "Ում համար", "inside": "Ինչ կա ներսում",
        "sides": "Լսումների տեքստ", "sides_note": "Տեսարաններ, որտեղ կերպարն ամենաշատն է խոսում",
        "application": "Հայտ", "one_pager": "One-pager", "bible": "Սերիալի բիբլիա", "deck": "Պիչ դեք",
        "ep_synopses": "Սերիաների բովանդակություն", "by_episode": "Ըստ սերիաների", "char_x_ep": "Կերպարներ × սերիաներ",
        "ext_night": "Դրսի գիշերային տեսարաններ", "int_pages": "էջ ներսում", "ext_pages": "էջ դրսում",
        "speaking": "խոսող դեր", "eighths": "1/8 էջ", "first": "Առաջին հայտնվելը", "for": "Համար",
        "thanks": "Շնորհակալություն", "written_by": "Սցենարի հեղինակ",
    },
    "ru": {
        "synopsis": "Синопсис", "synopsis_long": "Расширенный синопсис", "characters": "Персонажи",
        "why_now": "Почему сейчас", "comps": "Референсы", "scale": "Масштаб производства", "logline": "Логлайн",
        "world": "Мир", "tone": "Тон и стиль", "season_arc": "Арка сезона", "episodes": "Серии",
        "audience": "Аудитория", "team": "Команда", "pages": "стр.", "scenes": "сцен", "sets": "локаций",
        "roles": "ролей со словами", "minutes": "мин", "episodes_n": "серий", "lines": "реплик", "words": "слов",
        "lead": "Главная", "supporting": "Второстепенная", "day player": "Эпизод", "non-speaking": "Без слов",
        "episode": "Серия", "scene": "Сцена", "length": "Объём", "time": "Время", "cast": "Персонажи",
        "content": "Содержание", "location": "Локация", "ie": "Инт/Нат", "int": "Инт", "ext": "Нат",
        "day": "День", "night": "Ночь/вечер", "age": "Возраст", "role": "Роль", "eps": "Серии",
        "overview": "Поэпизодный план", "breakdown": "Производственный разбор", "casting": "Кастинг",
        "contents": "Состав пакета", "recipient": "Для кого", "inside": "Что внутри",
        "sides": "Сцены для проб", "sides_note": "Сцены, где у персонажа больше всего текста",
        "application": "Заявка", "one_pager": "One-pager", "bible": "Библия сериала", "deck": "Питч-дек",
        "ep_synopses": "Синопсисы серий", "by_episode": "По сериям", "char_x_ep": "Персонажи × серии",
        "ext_night": "Натурные ночные сцены", "int_pages": "стр. в интерьере", "ext_pages": "стр. на натуре",
        "speaking": "ролей со словами", "eighths": "1/8 стр.", "first": "Первое появление", "for": "Для",
        "thanks": "Спасибо", "written_by": "Автор сценария",
    },
    "en": {
        "synopsis": "Synopsis", "synopsis_long": "Extended synopsis", "characters": "Characters",
        "why_now": "Why now", "comps": "Comparables", "scale": "Production scale", "logline": "Logline",
        "world": "The world", "tone": "Tone & style", "season_arc": "Season arc", "episodes": "Episodes",
        "audience": "Audience", "team": "Team", "pages": "pages", "scenes": "scenes", "sets": "sets",
        "roles": "speaking roles", "minutes": "min", "episodes_n": "episodes", "lines": "lines", "words": "words",
        "lead": "Lead", "supporting": "Supporting", "day player": "Day player", "non-speaking": "Non-speaking",
        "episode": "Episode", "scene": "Scene", "length": "Length", "time": "Time", "cast": "Cast",
        "content": "Content", "location": "Location", "ie": "Int/Ext", "int": "Int", "ext": "Ext",
        "day": "Day", "night": "Night/evening", "age": "Age", "role": "Role", "eps": "Episodes",
        "overview": "Scene overview", "breakdown": "Production breakdown", "casting": "Casting breakdown",
        "contents": "Package contents", "recipient": "For", "inside": "Inside",
        "sides": "Audition sides", "sides_note": "Scenes where the character speaks the most",
        "application": "Application", "one_pager": "One-pager", "bible": "Series bible", "deck": "Pitch deck",
        "ep_synopses": "Episode synopses", "by_episode": "By episode", "char_x_ep": "Characters × episodes",
        "ext_night": "Exterior night scenes", "int_pages": "pages interior", "ext_pages": "pages exterior",
        "speaking": "speaking roles", "eighths": "1/8 pages", "first": "First appearance", "for": "For",
        "thanks": "Thank you", "written_by": "Written by",
    },
}


def L(lang, k):
    return LBL.get(lang, LBL["en"]).get(k, LBL["en"].get(k, k))


# Recipients: folder number, Armenian position, English position, what they get (hy, en).
RECIPIENTS = [
    ("01", "ՊՐՈԴՅՈՒՍԵՐ", "Producer", "One-pager, լոգլայն և համառոտ բովանդակություն",
     "One-pager, logline and synopsis"),
    ("02", "ՊԼԱՏՖՈՐՄ", "Platform", "Պիչ դեք կամ սերիալի բիբլիա, սերիաների բովանդակություն",
     "Pitch deck or series bible, episode synopses"),
    ("03", "ՌԵԺԻՍՈՐ", "Director", "Սցենարը (PDF, Word, Final Draft) և տեսարանների ցանկ",
     "Script (PDF, Word, Final Draft) and scene overview"),
    ("04", "ԼԱՅՆ-ՊՐՈԴՅՈՒՍԵՐ", "Line Producer", "Արտադրական breakdown, լոկացիաներ, աղյուսակ",
     "Production breakdown, locations, spreadsheet"),
    ("05", "ԿԱՍՏԻՆԳ-ԴԻՐԵԿՏՈՐ", "Casting Director", "Դերերի ցուցակ նկարագրություններով, աղյուսակ",
     "Role list with descriptions, spreadsheet"),
    ("06", "ԴԵՐԱՍԱՆՆԵՐ", "Actors", "Լսումների տեքստեր ամեն դերի համար", "Audition sides for each role"),
    ("07", "ՄԻՋԱԶԳԱՅԻՆ", "International", "Անգլերեն one-pager միջազգային գործընկերների համար",
     "English one-pager for international partners"),
    ("08", "ՄՐՑՈՒՅԹ-ՖՈՆԴ", "Competition & Fund", "Հայտ՝ ըստ մրցույթի կանոնների", "Application per the rules"),
]


def folder_name(r):
    return f"{r[0]} {r[1]} · {r[2]}"


def recipient_label(r, lang):
    if lang == "en":
        return f"For the {r[2].lower()}"
    return f"{r[1]} · {r[2]}"


# ---------------------------------------------------------------- text helpers
def esc(s):
    return html.escape(s or "", quote=False)


def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![*\w])\*(?!\*)(.+?)\*(?!\w)", r"<i>\1</i>", s)
    return s


def md(text):
    """Small Markdown: paragraphs, ### h3, bullets, > quote, | tables |, **bold**, *italic*."""
    out, para, items, rows = [], [], [], []

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()
        if rows:
            body = [r for r in rows if not re.fullmatch(r"\|?[\s:|-]+\|?", r)]
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in body]
            if cells:
                h = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
                b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
                out.append(f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>")
            rows.clear()

    for ln in (text or "").splitlines():
        s = ln.strip()
        if not s:
            flush()
        elif s.startswith("### "):
            flush()
            out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith(("- ", "* ", "• ")):
            if para:
                flush()
            items.append(s[2:])
        elif s.startswith(">"):
            flush()
            out.append(f"<blockquote>{inline(s.lstrip('> '))}</blockquote>")
        elif s.startswith("|"):
            if para or items:
                flush()
            rows.append(s)
        else:
            if items or rows:
                flush()
            para.append(s)
    flush()
    return "\n".join(out)


# ---------------------------------------------------------------- CSS
def _fontfaces():
    faces = [("MSerif", "NotoSerifArmenian.ttf", "normal", "U+0530-058F, U+FB13-FB17"),
             ("MSerif", "NotoSerif.ttf", "normal", None), ("MSerif", "NotoSerif-Italic.ttf", "italic", None),
             ("MSans", "NotoSansArmenian.ttf", "normal", "U+0530-058F, U+FB13-FB17"),
             ("MSans", "NotoSans.ttf", "normal", None)]
    css = []
    for fam, f, style, rng in faces:
        p = os.path.join(FONTS, f)
        if os.path.exists(p):
            css.append(f"@font-face{{font-family:'{fam}';src:url('file://{p}');font-weight:100 900;"
                       f"font-style:{style};{'unicode-range:' + rng + ';' if rng else ''}}}")
    return "\n".join(css)


BASE_CSS = """
:root{--black:#000;--white:#fff;--graphite:#111;--red:#D90429;--grey:#6E6E6E;--mute:#9A9A9A;--line:#E3E3E0;
--soft:#F6F6F4;--serif:'MSerif',Georgia,serif;--sans:'MSans',Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
body{font-family:var(--sans);color:var(--graphite);font-size:9.6pt;line-height:1.6;font-weight:400;
-webkit-print-color-adjust:exact;print-color-adjust:exact;font-kerning:normal}
b,strong{font-weight:650;color:#000}
p{margin:0 0 7pt}
ul{margin:0 0 8pt;padding-left:0;list-style:none}
li{position:relative;padding-left:13pt;margin-bottom:3pt}
li:before{content:'';position:absolute;left:0;top:.62em;width:5pt;height:1.2pt;background:var(--red)}
blockquote{margin:10pt 0;padding:2pt 0 2pt 12pt;border-left:2.5pt solid var(--red);font-family:var(--serif);
font-size:12.5pt;line-height:1.45;color:#000}
.tri{display:inline-block;width:0;height:0;border-left:5pt solid transparent;border-right:5pt solid transparent;
border-top:8.5pt solid var(--red)}
table{width:100%;border-collapse:collapse;margin:4pt 0 12pt;font-size:8.2pt;line-height:1.4}
th{font-size:6.4pt;letter-spacing:.14em;text-transform:uppercase;color:var(--grey);font-weight:600;text-align:left;
padding:0 8pt 5pt 0;border-bottom:1.2pt solid #000;vertical-align:bottom}
td{padding:5pt 8pt 5pt 0;border-bottom:.6pt solid var(--line);vertical-align:top}
tr{break-inside:avoid}
td.num,th.num{text-align:right;padding-right:10pt;white-space:nowrap;font-variant-numeric:tabular-nums}
td.n{color:var(--grey);white-space:nowrap;font-variant-numeric:tabular-nums}
.chip{display:inline-block;font-size:6.2pt;letter-spacing:.12em;text-transform:uppercase;font-weight:650;
padding:1.6pt 5pt 1.2pt;border-radius:2pt;white-space:nowrap;line-height:1.3}
.chip.lead{background:var(--red);color:#fff}
.chip.supporting{background:#000;color:#fff}
.chip.day,.chip.non{border:.6pt solid #BDBDBD;color:var(--grey)}
.chip.ext{border:.6pt solid #000;color:#000}
.chip.int{background:var(--soft);color:var(--grey)}
.chip.night{background:#000;color:#fff}
.chip.ok{color:#1B7F3B;border:.6pt solid #9BD3AE}
.chip.over{background:var(--red);color:#fff}
"""

DOC_CSS = """
@page{size:A4;margin:24mm 19mm 20mm 19mm}
.onepage{height:252mm;overflow:hidden}
.mast{padding:6pt 0 14pt;margin-bottom:6pt;border-bottom:.6pt solid var(--line)}
.mast .doc{font-size:7pt;letter-spacing:.24em;text-transform:uppercase;color:var(--grey);margin-bottom:10pt}
.mast h1{font-family:var(--serif);font-weight:700;font-size:28pt;line-height:1.08;margin:0 0 6pt;color:#000;
letter-spacing:-.005em}
.mast .fmt{font-size:7.4pt;letter-spacing:.18em;text-transform:uppercase;color:var(--grey)}
.mast .logline{margin:14pt 0 2pt;padding-left:12pt;border-left:2.5pt solid var(--red);font-family:var(--serif);
font-size:13pt;line-height:1.42;font-weight:500;color:#000}
h2{font-size:6.8pt;letter-spacing:.24em;text-transform:uppercase;color:#000;font-weight:700;margin:20pt 0 9pt;
display:flex;align-items:center;gap:8pt;break-after:avoid}
h2 .no{color:var(--red);font-variant-numeric:tabular-nums}
h2:after{content:'';flex:1;height:.6pt;background:var(--line)}
h3{font-family:var(--serif);font-size:12pt;font-weight:700;margin:12pt 0 3pt;color:#000;break-after:avoid}
section{break-inside:auto}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:0 14pt;margin:4pt 0 6pt}
.stat{border-top:1.6pt solid #000;padding-top:6pt}
.stat .v{font-family:var(--serif);font-size:22pt;font-weight:700;line-height:1;color:#000}
.stat .v small{font-size:10pt;color:var(--grey);font-weight:400}
.stat .l{font-size:6.4pt;letter-spacing:.16em;text-transform:uppercase;color:var(--grey);margin-top:4pt}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:14pt 18pt}
.card{border-top:1.2pt solid #000;padding-top:7pt;break-inside:avoid}
.card .nm{font-family:var(--serif);font-size:13pt;font-weight:700;color:#000;line-height:1.15}
.card .meta{margin:4pt 0 6pt;display:flex;gap:5pt;flex-wrap:wrap;align-items:center;font-size:6.6pt;
letter-spacing:.1em;text-transform:uppercase;color:var(--grey)}
.card p{font-size:8.9pt;line-height:1.55}
.cards.one{grid-template-columns:1fr}
.wc{float:right;font-size:6.4pt;letter-spacing:.12em;text-transform:uppercase;color:var(--grey);margin-top:-1pt}
.ep{break-inside:avoid;padding:8pt 0 6pt;border-bottom:.6pt solid var(--line);display:grid;
grid-template-columns:62pt 1fr;gap:12pt}
.ep .k{font-size:6.6pt;letter-spacing:.18em;text-transform:uppercase;color:var(--red);font-weight:700;padding-top:3pt}
.ep .t{font-family:var(--serif);font-size:11.5pt;font-weight:700;color:#000;margin-bottom:2pt}
.toc{margin-top:8pt}
.toc .row{display:grid;grid-template-columns:30pt 1fr 1.25fr;gap:12pt;padding:9pt 0;border-bottom:.6pt solid var(--line);
break-inside:avoid}
.toc .no{font-family:var(--serif);font-size:16pt;font-weight:700;color:var(--red);line-height:1}
.toc .who{font-family:var(--serif);font-size:12pt;font-weight:700;color:#000;line-height:1.2}
.toc .en{font-size:6.6pt;letter-spacing:.16em;text-transform:uppercase;color:var(--grey);margin-top:2pt}
.toc .files{font-size:8pt;color:var(--grey);line-height:1.5}
.toc .files b{color:#000;font-weight:600}
.note{font-size:7.6pt;color:var(--grey)}
.cover{display:flex;flex-direction:column;justify-content:space-between;
background:#000;color:#fff;padding:22mm 18mm 18mm;break-after:page;position:relative}
.cover .kick{font-size:7pt;letter-spacing:.26em;text-transform:uppercase;color:var(--red);font-weight:700}
.cover h1{font-family:var(--serif);font-size:38pt;line-height:1.05;font-weight:700;margin:12pt 0 10pt;color:#fff}
.cover .fmt{font-size:7.6pt;letter-spacing:.2em;text-transform:uppercase;color:#A8A8A8}
.cover .logline{margin-top:18pt;font-family:var(--serif);font-size:13pt;line-height:1.45;color:#E8E8E8;max-width:135mm}
.cover .bot{display:flex;justify-content:space-between;align-items:flex-end;font-size:7pt;letter-spacing:.14em;
text-transform:uppercase;color:#8A8A8A}
.cover img{height:15mm}
"""

DECK_CSS = """
@page{size:13.333in 7.5in;margin:0}
.slide{width:13.333in;height:7.5in;position:relative;overflow:hidden;break-after:page;background:#fff;
padding:.78in .95in .95in;display:flex;flex-direction:column}
.slide:last-child{break-after:auto}
.slide.dark{background:#000;color:#fff}
.slide.dark b{color:#fff}
.kick{font-size:11.5pt;letter-spacing:.26em;text-transform:uppercase;color:var(--red);font-weight:700;
display:flex;align-items:center;gap:10pt;margin-bottom:22pt}
.kick .no{font-variant-numeric:tabular-nums}
.kick:after{content:'';width:46pt;height:1pt;background:var(--red)}
.foot{position:absolute;left:.95in;right:.95in;bottom:.42in;display:flex;justify-content:space-between;
align-items:center;font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--mute)}
.foot img{height:.3in;opacity:.9}
.dark .foot{color:#6F6F6F}
.fit{flex:1;min-height:0;overflow:hidden}
.s-cover{justify-content:flex-end;padding-bottom:1.15in}
.s-cover .bg{position:absolute;inset:0;background-size:cover;background-position:center}
.s-cover .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15) 0%,rgba(0,0,0,.55) 45%,#000 92%)}
.s-cover .in{position:relative;max-width:9.4in}
.s-cover .tri{border-left-width:9pt;border-right-width:9pt;border-top-width:15pt;margin-bottom:16pt}
.s-cover h1{font-family:var(--serif);font-size:74pt;line-height:1;font-weight:700;margin:0 0 16pt;color:#fff;
letter-spacing:-.01em}
.s-cover .fmt{font-size:10pt;letter-spacing:.26em;text-transform:uppercase;color:#A9A9A9;margin-bottom:22pt}
.s-cover .lg{font-family:var(--serif);font-size:17pt;line-height:1.45;color:#E6E6E6;max-width:8.6in}
.s-cover .logo{position:absolute;right:.95in;top:.7in;height:.55in}
.s-cover .doc{position:absolute;left:.95in;top:.78in;font-size:9pt;letter-spacing:.26em;text-transform:uppercase;
color:var(--red);font-weight:700}
.big{font-family:var(--serif);font-size:36pt;line-height:1.28;font-weight:600;color:#000;max-width:10.6in}
.dark .big{color:#fff}
.body{font-size:22pt;line-height:1.5;color:var(--graphite)}
.body.long{font-size:17pt}
.state{font-family:var(--serif);font-size:30pt;line-height:1.35;font-weight:500;color:#000;max-width:10.4in}
.dark .body{color:#D8D8D8}
.body p{margin:0 0 10pt}
.body h3{font-family:var(--serif);font-size:19pt;margin:6pt 0 6pt;color:inherit}
.cols2{column-count:2;column-gap:.55in}
.cols2 p{break-inside:avoid-column}
.char{display:grid;grid-template-columns:4.3in 1fr;gap:.6in;flex:1;min-height:0}
.char .nm{font-family:var(--serif);font-size:58pt;line-height:1.02;font-weight:700;color:#000;word-break:break-word}
.char .meta{margin-top:16pt;display:flex;flex-direction:column;gap:7pt;font-size:9.5pt;letter-spacing:.18em;
text-transform:uppercase;color:var(--grey)}
.char .meta .chip{font-size:8pt;align-self:flex-start;padding:3pt 8pt}
.char .body{border-left:1pt solid var(--line);padding-left:.5in;font-size:24pt;line-height:1.45}
.eps{display:grid;grid-template-columns:1fr 1fr;gap:20pt 46pt;align-content:start}
.eps .e{border-top:1.4pt solid #000;padding-top:9pt}
.eps .k{font-size:8.5pt;letter-spacing:.22em;text-transform:uppercase;color:var(--red);font-weight:700}
.eps .t{font-family:var(--serif);font-size:16pt;font-weight:700;margin:4pt 0 4pt;color:#000}
.eps p{font-size:14pt;line-height:1.5;margin:0}
.nums{display:grid;grid-template-columns:repeat(4,1fr);gap:.4in;margin-top:auto;margin-bottom:.3in}
.nums .v{font-family:var(--serif);font-size:70pt;line-height:1;font-weight:700;color:#fff}
.nums .l{margin-top:12pt;font-size:9.5pt;letter-spacing:.2em;text-transform:uppercase;color:#9B9B9B;
border-top:1pt solid #333;padding-top:10pt}
.end{align-items:center;justify-content:center;text-align:center}
.end img{height:1.25in;margin-bottom:28pt}
.end .c{font-size:10pt;letter-spacing:.26em;text-transform:uppercase;color:#9A9A9A}
.end .t{font-family:var(--serif);font-size:30pt;color:#fff;margin-bottom:16pt}
"""

FIT_JS = """
document.querySelectorAll('.onepage').forEach(el=>{
  if(el.scrollHeight>el.clientHeight){const z=el.clientHeight/el.scrollHeight;
    el.style.height=(el.clientHeight/z)+'px';el.style.zoom=z;}
});
document.querySelectorAll('.fit').forEach(el=>{
  let fs=parseFloat(getComputedStyle(el).fontSize), n=0;
  while(el.scrollHeight>el.clientHeight+1 && fs>9 && n<60){fs*=0.95;el.style.fontSize=fs+'px';
    el.querySelectorAll('*').forEach(c=>{if(c.style)c.style.fontSize='';});n++;}
});
"""


def page(body, kind="doc", title="", run_left="", run_right=""):
    """kind: doc (A4 pages), onepage (A4, scaled to fit one page), cover (A4 full bleed), deck (16:9)."""
    css = _fontfaces() + BASE_CSS + (DECK_CSS if kind == "deck" else DOC_CSS)
    if kind == "onepage":
        body = f'<div class="onepage">{body}</div>'
    if kind == "cover":
        css += "@page{size:A4;margin:0} .cover{height:297mm;margin:0}"
    meta = f'<meta name="run-left" content="{esc(run_left)}"><meta name="run-right" content="{esc(run_right)}">'
    return (f'<!doctype html><html><head><meta charset="utf-8">{meta}<title>{esc(title)}</title>'
            f'<style>{css}</style></head><body>{body}</body></html>')


_HDR_FONT = None


def _header_font():
    global _HDR_FONT
    if _HDR_FONT is None:
        css = ""
        for fam, f in (("H", "NotoSansArmenian.ttf"), ("H", "NotoSans.ttf")):
            p = os.path.join(FONTS, f)
            if os.path.exists(p) and f.startswith("NotoSansArmenian"):
                with open(p, "rb") as fh:
                    css += ("@font-face{font-family:'HA';font-weight:100 900;src:url(data:font/ttf;base64,"
                            + base64.b64encode(fh.read()).decode() + ")}")
        _HDR_FONT = css
    return _HDR_FONT


def header_template(left, right):
    if not (left or right):
        return "<span></span>"
    return (f"<style>{_header_font()}</style>"
            '<div style="width:100%;padding:0 19mm;margin-top:9mm;display:flex;justify-content:space-between;'
            "align-items:center;font-family:'HA',Helvetica,Arial,sans-serif;font-size:6.6px;letter-spacing:1.5px;"
            'text-transform:uppercase;color:#9A9A9A">'
            '<span style="color:#D90429;font-weight:700;display:flex;align-items:center;gap:5px">'
            '<span style="display:inline-block;width:0;height:0;border-left:3.5px solid transparent;'
            'border-right:3.5px solid transparent;border-top:6px solid #D90429"></span>'
            f'{esc(left)}</span><span>{esc(right)}</span></div>')


# ---------------------------------------------------------------- components
def masthead(title, fmt, doc_label, logline=""):
    lg = f'<div class="logline">{inline(logline)}</div>' if logline else ""
    return (f'<header class="mast"><div class="doc">{esc(doc_label)}</div><h1>{esc(title)}</h1>'
            f'<div class="fmt">{esc(fmt)}</div>{lg}</header>')


def h2(no, text):
    return f'<h2><span class="no">{esc(no)}</span>{esc(text)}</h2>'


def stats(items):
    return '<div class="stats">' + "".join(
        f'<div class="stat"><div class="v">{v}</div><div class="l">{esc(l)}</div></div>' for v, l in items) + "</div>"


ROLE_CLS = {"lead": "lead", "supporting": "supporting", "day player": "day", "non-speaking": "non"}


def chip(text, cls):
    return f'<span class="chip {cls}">{esc(text)}</span>'


def cards(items, one=False):
    """items: (name, [meta html], body markdown)"""
    out = []
    for nm, meta, body in items:
        out.append(f'<div class="card"><div class="nm">{esc(nm)}</div><div class="meta">{"".join(meta)}</div>'
                   f'{md(body)}</div>')
    return f'<div class="cards{" one" if one else ""}">' + "".join(out) + "</div>"


# ---------------------------------------------------------------- deck
def slide(inner, dark=False, cls="", foot=("", "", "")):
    fl, logo, n = foot
    f = f'<div class="foot"><span>{esc(fl)}</span>{logo}<span>{esc(n)}</span></div>' if any(foot) else ""
    return f'<section class="slide{" dark" if dark else ""} {cls}">{inner}{f}</section>'


def kicker(no, text):
    return f'<div class="kick"><span class="no">{esc(no)}</span>{esc(text)}</div>'


# ---------------------------------------------------------------- render
class Renderer:
    """HTML -> PDF through headless Chromium: Node Playwright (render_pdf.js), or Python Playwright if installed."""

    def __enter__(self):
        with open(os.path.join(HERE, "fit.js"), "w", encoding="utf-8") as f:
            f.write(FIT_JS)
        return self

    def __exit__(self, *exc):
        return False

    def pdf(self, html_text, out_pdf, kind="doc", footer_left="Maghakian Scripts · maghakianscripts.com",
            html_dir=None):
        import json
        import subprocess
        import tempfile
        html_dir = html_dir or os.path.dirname(out_pdf)
        os.makedirs(html_dir, exist_ok=True)
        hp = os.path.abspath(os.path.join(html_dir, os.path.splitext(os.path.basename(out_pdf))[0] + ".html"))
        with open(hp, "w", encoding="utf-8") as f:
            f.write(html_text)
        foot = ('<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:6.5px;'
                'letter-spacing:1.4px;text-transform:uppercase;color:#9A9A9A;padding:0 19mm;display:flex;'
                f'justify-content:space-between"><span>{esc(footer_left)}</span>'
                '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
        m = re.search(r'name="run-left" content="([^"]*)".*?name="run-right" content="([^"]*)"', html_text, re.S)
        head = header_template(html.unescape(m.group(1)), html.unescape(m.group(2))) if m else "<span></span>"
        job = [{"html": hp, "pdf": os.path.abspath(out_pdf), "kind": kind, "footer": foot, "header": head}]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as t:
            json.dump(job, t)
        try:
            subprocess.run(["node", os.path.join(HERE, "render_pdf.js"), t.name], check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            try:
                self._py(job[0])
            except ImportError:
                print(f"! no Chromium/Playwright here: kept the HTML only ({hp})")
        finally:
            os.unlink(t.name)
        return out_pdf

    def _py(self, j):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            br = p.chromium.launch()
            pg = br.new_page()
            pg.goto("file://" + j["html"])
            pg.evaluate("document.fonts.ready.then(()=>true)")
            pg.evaluate(FIT_JS)
            if j["kind"] == "deck":
                pg.pdf(path=j["pdf"], width="13.333in", height="7.5in", print_background=True,
                       margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, prefer_css_page_size=True)
            elif j["kind"] == "cover":
                pg.pdf(path=j["pdf"], format="A4", print_background=True, prefer_css_page_size=True)
            else:
                pg.pdf(path=j["pdf"], format="A4", print_background=True, display_header_footer=True,
                       header_template=j["header"], footer_template=j["footer"], prefer_css_page_size=True)
            br.close()


def logo_img(kind, cls=""):
    src = _logo(kind)
    return f'<img class="{cls}" src="{src}" alt="Maghakian">' if src else ""
