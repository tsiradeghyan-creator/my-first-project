#!/usr/bin/env python3
"""KIT Scenarist / Ani-style .docx -> Fountain, without touching the text.

Reads paragraph styles from the KIT export (SCENE HEADING, NOTE, CHARACTER, DIALOG, ACTION) and Ani's
house layout:
    1. ՏԵՍԱՐԱՆ                      (SCENE HEADING, or NOTE "15.1 ՏԵՍԱՐԱՆ")
    ՎԻԼՈՅԻ ՏՈՒՆ։ ՀՅՈՒՐԱՍԵՆՅԱԿ։ ԵՐԵԿՈ   (NOTE: location + time)
    ՎԻԼՈ, ՍԱՌԱ /ՎԻԼՈՅԻ ԿԻՆ/, ՄԱՍՈՎԿԱ (NOTE: cast of the scene)
    1984Թ                           (NOTE or CHARACTER: period super)
    ՎԻԿԱ /ՆԵՂՎԱԾ/                   (CHARACTER with parenthetical)
    Պապա /խառնված/ մամ՞,,,          (DIALOG with inline /directions/)
    ՊԵՐԵԽՈԴ, ՖԼԵՇԲԵՔԻ ՍԿԻԶԲ ...      (CHARACTER with no dialogue: transition / super)

Output: Fountain with forced scene headings ".LOCATION - TIME #N#", "= CAST: ..." lines (non-printing,
used by the breakdown), dialogue parentheticals on their own lines. Words, punctuation (",,,", "՞")
and order stay exactly as Ani wrote them.

Usage: python3 kit_docx_to_fountain.py ep1.docx [ep2.docx ...] [--outdir DIR] [--series "84-ի ամառը"]
"""
import argparse
import os
import re
import sys

TIME_WORDS = ["ՑԵՐԵԿ", "ԵՐԵԿՈ", "ԳԻՇԵՐ", "ԱՌԱՎՈՏ", "ԻՐԻԿՈՒՆ", "ԿԵՍՕՐ", "ԱՐՇԱԼՈՒՅՍ", "ՄԱՅՐԱՄՈՒՏ",
              "ԼՈՒՍԱԲԱՑ", "ՎԱՂ ԱՌԱՎՈՏ", "ՈՒՇ ԳԻՇԵՐ", "ДЕНЬ", "НОЧЬ", "ВЕЧЕР", "УТРО", "DAY", "NIGHT"]
SCENE_NOTE = re.compile(r"^(\d+(?:\.\d+)?\.?\s*)?ՏԵՍԱՐԱ\S*(.*)$", re.I)
PERIOD = re.compile(r"^\d{2,4}\s*Թ\.?$")
TRANSITION = re.compile(r"^(ՊԵՐԵԽՈԴ|ԿՏՐՈՒՄ|ՄԹՆՈՒՄ|ԱՆՑՈՒՄ)\b|:$|։$")


def up(s):
    return s.upper()


def split_slash(text):
    """'a /b/ c' -> [('d','a'),('p','b'),('d','c')]"""
    out, pos = [], 0
    for m in re.finditer(r"/([^/]+)/", text):
        pre = text[pos:m.start()].strip()
        if pre:
            out.append(("d", pre))
        out.append(("p", m.group(1).strip()))
        pos = m.end()
    rest = text[pos:].strip()
    if rest:
        out.append(("d", rest))
    return out


def cast_names(line):
    """'ՍԱՌԱ /ՎԻԼՈՅԻ ԿԻՆ/, /ԵՐԻՏԱՍԱՐԴ/ ՌՈԲԵՐՏ' -> ['ՍԱՌԱ (ՎԻԼՈՅԻ ԿԻՆ)', 'ՌՈԲԵՐՏ (ԵՐԻՏԱՍԱՐԴ)']
    Descriptors are kept in brackets; the breakdown matches on the name before the bracket."""
    names = []
    chunks, buf, inside = [], "", False
    for ch in line:                       # split on commas outside /.../
        if ch == "/":
            inside = not inside
        if ch == "," and not inside:
            chunks.append(buf)
            buf = ""
        else:
            buf += ch
    chunks.append(buf)
    for part in chunks:
        part = part.strip().strip(",")
        if not part:
            continue
        descr = [d.strip() for d in re.findall(r"/([^/]+)/?", part)]
        name = re.sub(r"/[^/]*/?", " ", part).strip()
        name = re.sub(r"\s+", " ", up(name))
        names.append(f"{name} ({', '.join(up(d) for d in descr)})" if descr else name)
    return [n for n in names if n]


def location_line(s):
    """'ԾԵՐԱՆՈՑ։ ՀԱՆԳՍՏԻ ՍԵՆՅԱԿ, ՑԵՐԵԿ' / 'ԴԱՏԱՐԱՆ/ՄԻՋԱՆՑՔ։ ՑԵՐԵԿ' -> 'ԾԵՐԱՆՈՑ, ՀԱՆԳՍՏԻ ՍԵՆՅԱԿ - ՑԵՐԵԿ'
    Only separators change (one style for every scene); the words stay as written."""
    s = up(s.strip()).strip(" ,.։")
    s = re.sub(r"\s*/([^/]+)/\s*", r" (\1) ", s)            # /ԱՌԱՋԻՆ ՀԱՐԿ/ -> (ԱՌԱՋԻՆ ՀԱՐԿ)
    s = re.sub(r"ԻՆՉ-ՈՐ", "ԻՆՉ\u2011ՈՐ", s)                # keep "ինչ-որ" whole (non-breaking hyphen)
    parts = [p.strip().replace("\u2011", "-") for p in re.split(r"\s*[։:;.,/]\s*|\s+-\s+|(?<=\S)-(?=\S)", s) if p and p.strip()]
    tod = ""
    if len(parts) >= 2 and any(parts[-1].startswith(w) for w in TIME_WORDS):
        tod = parts.pop()
    loc = ", ".join(parts)
    return f"{loc} - {tod}" if tod else loc


# INT/EXT guess (Ani's format has none). Exterior stems win over interior ones.
EXT_STEMS = ["ԲԱԿ", "ՓՈՂՈՑ", "ՃԱՆԱՊԱՐՀ", "ԾՈՎԱՓ", "ԱՅԳԻ", "ԶԲՈՍԱՅԳԻ", "ՈՐՍԻ", "ՋՐԱՌԱՏ", "ԶՐԱՌԱՏ",
             "ՄՈՏԱԿԱՅՔ", "ՇՐՋԱԿԱՅՔ", "ԴԱՇՏ", "ԱՆՏԱՌ", "ԳԵՏ", "ՀՐԱՊԱՐԱԿ", "ՏԱՆԻՔ", "ՊԱՏՇԳԱՄԲ", "ՍԱՐ", "ԼԻՃ",
             "ԿԱՌԱՄԱՏՈՒՅՑ", "ԳԵՐԵԶՄԱՆՈՑ", "ԿԱՄՈՒՐՋ", "ԲԵՆԶԱԼՑԱԿԱՅԱՆ", "ԿԱՅԱՆԱՏԵՂԻ", "ԹԱՂԱՄԱՍ", "ՄԱՅԹ",
             "ԱՓ", "ԳՅՈՒՂԱՄԻՋ", "ՄՈՒՏՔ", "ԴԱՐՊԱՍ", "ԽԱՂԱՀՐԱՊԱՐԱԿ", "ԱՎՏՈԿԱՅԱՆ", "ԿԱՅԱՐԱՆԻ ՀԱՐԹԱԿ"]
INT_STEMS = ["ՍԵՆՅԱԿ", "ՆՆՋԱՐԱՆ", "ՆՆՋԱՍԵՆՅԱԿ", "ԽՈՀԱՆՈՑ", "ՀՅՈՒՐԱՍԵՆՅԱԿ", "ՄԻՋԱՆՑՔ", "ԲՆԱԿԱՐԱՆ", "ՏՈՒՆ",
             "ԱՌԱՆՁՆԱՏՈՒՆ", "ՌԵՍՏՈՐԱՆ", "ՌԵՍՈՏՈՐԱՆ", "ԲԱՌ", "ՍՐՃԱՐԱՆ", "ՀԻՎԱՆԴԱՆՈՑ", "ԼՈԳԱՐԱՆ", "ԼԱԲՈՐԱՏՈՐԻԱ",
             "ՍՐԱՀ", "ԱՇԽԱՏԱՍԵՆՅԱԿ", "ՆԱԽԱՍՐԱՀ", "ՀԱՄԱՐ", "ԿԻՆՈԹԱՏՐՈՆ", "ԿԻՆՈԹԱՏՈՐՆ", "ԱԿՈՒՄԲ", "ԽԱՆՈՒԹ",
             "ԴԱՏԱՐԱՆ", "ԾԵՐԱՆՈՑ", "ՀԱՆՐԱԿԱՑԱՐԱՆ", "ՀԱՆԱՐԱԿԱՑԱՐ", "ՀՅՈՒՐԱՆՈՑ", "ՀՅՈՒՐՒԱՆՈՑ", "ԲԵՄ", "ՆԿՈՒՂ",
             "ԱՎՏՈՏՆԱԿ", "ՃԱՇԱՐԱՆ", "ՃԱՇԱՍԵՆՅԱԿ", "ՕԴԱՆԱՎԱԿԱՅԱՆ", "ՈՍՏԻԿԱՆՈՒԹՅՈՒՆ", "ԳՐԱՍԵՆՅԱԿ", "ԴԱՍԱՐԱՆ",
             "ՍՐՏԱՐԱՆ", "ԳԵՂԵՑԿՈՒԹՅԱՆ", "ՓԼԵՅՍՄԵՆԹ", "ԿԱՅԱՐԱՆ", "ԵԿԵՂԵՑԻ", "ԽԱՆՈՒԹ", "ՍՊԱՍԱՍՐԱՀ", "ԱՐՀԵՍՏԱՆՈՑ"]
VEHICLE_STEMS = ["ՄԵՔԵՆԱ", "ՏԱՔՍԻ", "ԱՎՏՈԲՈՒՍ", "ԳՆԱՑՔ", "ՄԻԿՐՈԱՎՏՈԲՈՒՍ", "ԻՆՔՆԱԹԻՌ", "ԱՎՏՈ"]


def _hit(tokens, stems, slack=3):
    return any(t.startswith(st) and len(t) - len(st) <= slack for t in tokens for st in stems)


ROOM_STEMS = ["ՍԵՆՅԱԿ", "ՆՆՋԱՐԱՆ", "ՆՆՋԱՍԵՆՅԱԿ", "ԽՈՀԱՆՈՑ", "ՀՅՈՒՐԱՍԵՆՅԱԿ", "ՄԻՋԱՆՑՔ", "ԼՈԳԱՐԱՆ", "ՃԱՇԱՍԵՆՅԱԿ",
              "ԴՈՒՌ", "ԴՌԱՆ", "ԱՇԽԱՏԱՍԵՆՅԱԿ", "ՆԱԽԱՍՐԱՀ", "ՀԱՄԱՐ"]
NEAR = ["ՄՈՏ", "ԴԻՄԱՑ", "ՄՈՏԱԿԱՅՔ", "ՇՐՋԱԿԱՅՔ", "ԵՏԵՎ", "ԵՏՆԱՄԱՍ"]


def _is(tok, stems, slack=3):
    return any(tok.startswith(st) and len(tok) - len(st) <= slack for st in stems)


def guess_int_ext(loc):
    """-> ('ՆԵՐՍ.' | 'ԴՐՍ.' | 'ՆԵՐՍ./ԴՐՍ.', sure). Reads the location words in order."""
    toks = re.findall(r"[^\W\d_]+", up(loc or ""))
    ext = veh = room = inn = False
    for k, t in enumerate(toks):
        prev, nxt = (toks[k - 1] if k else ""), (toks[k + 1] if k + 1 < len(toks) else "")
        if t in NEAR or _is(t, ["ՄՈՏԱԿԱՅՔ", "ՇՐՋԱԿԱՅՔ", "ԵՏՆԱՄԱՍ"]):
            if _is(prev, ROOM_STEMS):          # ՍԵՆՅԱԿԻ ԴԻՄԱՑ = inside the building
                room = True
            else:
                ext = True
        elif _is(t, EXT_STEMS) and t not in ("ՄՈՏ",):
            ext = True
        elif _is(t, VEHICLE_STEMS):
            if nxt in NEAR:                    # ՄԵՔԵՆԱՅԻ ՄՈՏ = outside, by the car
                ext = True
            else:
                veh = True
        elif _is(t, ROOM_STEMS):
            room = True
        elif _is(t, INT_STEMS):
            inn = True
    if veh and ext:
        return "ՆԵՐՍ./ԴՐՍ.", True
    if ext and room:
        return "ՆԵՐՍ./ԴՐՍ.", False            # e.g. ԽՈՀԱՆՈՑ, ՏԱՆ ԲԱԿ: both, check
    if ext:
        return "ԴՐՍ.", True
    if veh or room or inn:
        return "ՆԵՐՍ.", True
    return "ՆԵՐՍ.", False


def looks_location(s):
    S = up(s)
    return bool(re.search(r"[։:;]", s)) or any(re.search(rf"\b{w}\b", S) for w in TIME_WORDS)


def looks_cast(s):
    return "," in s or (len(s.split()) <= 3 and not re.search(r"[։:.]$", s))


INT_EXT = True


def convert(path, series=None):
    import docx
    paras = [(p.style.name.upper(), p.text.strip()) for p in docx.Document(path).paragraphs if p.text.strip()]
    out, title_bits = [], []
    i, n = 0, len(paras)
    scene_auto = 0
    in_header = 0  # >0 while reading the NOTE lines right after a scene heading

    def emit(*lines):
        out.extend(lines)
        out.append("")

    def scene_start(num_txt, extra=""):
        nonlocal scene_auto, in_header
        scene_auto += 1
        num = num_txt.strip(" .") if num_txt and re.match(r"\d", num_txt.strip()) else str(scene_auto)
        # look ahead for location / cast / period NOTEs
        loc, cast, period, tags = None, [], None, []
        extra = extra.strip(" .։")
        if extra and extra.upper() != "X":
            tags.append(extra)                 # e.g. "16. ՏԵՍԱՐԱՆ. /ԼԻԶԱՅԻ ԵՐԵՎԱԿԱՅՈՒԹՅՈՒՆԸ/"
        j = i + 1
        while j < n and j <= i + 4:
            st, tx = paras[j]
            header_like = st == "NOTE" or (st == "ACTION" and tx == up(tx))
            if header_like and not SCENE_NOTE.match(tx):
                if PERIOD.match(tx):
                    period = tx
                elif loc is None and looks_location(tx):
                    loc = tx
                elif loc is None and j + 1 < n and paras[j + 1][0] in ("NOTE", "ACTION") \
                        and looks_location(paras[j + 1][1]):
                    tags.append(tx)            # e.g. ՓԼԵՅՍՄԵՆԹ before the location line
                elif loc is None and "," not in tx and j + 1 < n and paras[j + 1][0] == "NOTE":
                    loc = tx                   # location line without time of day
                elif looks_cast(tx):
                    cast += cast_names(tx)
                else:
                    break
                j += 1
            elif st in ("CHARACTER", "SCENE CHARACTERS") and PERIOD.match(tx):
                period = tx
                j += 1
            elif st == "CHARACTER" and (j + 1 >= n or paras[j + 1][0] != "DIALOG") and loc is None:
                tags.append(tx)                # e.g. ՎԻԼՈՅԻ ԵՐԵՒԱԿԱՅՈՒԹՅՈՒՆ, ՖԼԵՇԲԵՔ
                j += 1
            elif st == "SCENE CHARACTERS":
                cast += cast_names(tx)
                j += 1
            else:
                break
        heading = location_line(loc) if loc else f"ՏԵՍԱՐԱՆ {num}"
        sure = True
        if INT_EXT and loc:
            ie, sure = guess_int_ext(heading)
            heading = f"{ie} {heading}"
        emit(f".{heading} #{num}#")
        if not sure:
            emit("= IE?")
        if cast:
            emit(f"= CAST: {', '.join(dict.fromkeys(cast))}")
        for t in tags:
            emit(f"!{t}")
        if period:
            emit(f"!{period}")
        return j

    while i < n:
        st, tx = paras[i]
        is_scene = st == "SCENE HEADING" or (st == "NOTE" and SCENE_NOTE.match(tx))
        if not out and not is_scene:
            title_bits.append(tx)
            i += 1
            continue
        m = SCENE_NOTE.match(tx) if st in ("SCENE HEADING", "NOTE") else None
        if st == "SCENE HEADING" or m:
            num = m.group(1) if m else re.match(r"^\s*([\d.]+)", tx).group(1) if re.match(r"^\s*\d", tx) else ""
            rest = m.group(2) if m else re.sub(r"^\s*[\d.]*\s*ՏԵՍԱՐԱ\S*", "", tx, flags=re.I)
            i = scene_start(num or "", rest or "")
            continue
        if st == "CHARACTER":
            nxt = paras[i + 1][0] if i + 1 < n else None
            if nxt == "DIALOG":
                parts = split_slash(tx)
                name = " ".join(t for k, t in parts if k == "d") or tx
                cue_par = [t for k, t in parts if k == "p"]
                lines = [f"@{up(name)}"]
                lines += [f"({t.lower()})" for t in cue_par]
                i += 1
                while i < n and paras[i][0] == "DIALOG":
                    for k, t in split_slash(paras[i][1]):
                        lines.append(f"({t})" if k == "p" else t)
                    i += 1
                emit(*lines)
                continue
            if TRANSITION.search(tx) and len(tx) <= 30:
                emit(f"> {tx.rstrip(':։')}")
            else:
                emit(f"!{tx}")
            i += 1
            continue
        if st == "NOTE":
            if looks_cast(tx) and tx == up(tx) and "," in tx:
                emit(f"= CAST: {', '.join(cast_names(tx))}")
            else:
                emit(f"!{tx}")
            i += 1
            continue
        if st == "DIALOG":  # orphan dialogue
            emit(tx)
            i += 1
            continue
        # ACTION / anything else
        emit(("!" + tx) if (tx == up(tx) or tx[0] in ".>=#@~![") else tx)
        i += 1

    ep = None
    for b in title_bits:
        mm = re.search(r"(?:սերիա|серия|episode)\s*(\d+)", b, re.I)
        if mm:
            ep = mm.group(1)
            break
    if ep is None:
        stem = os.path.splitext(os.path.basename(path))[0]
        stem = re.sub(r"^[0-9a-f]{8}-", "", stem)          # upload id prefix
        nums = re.findall(r"\d+", stem)
        ep = nums[-1] if nums else None
    head = []
    t = series or ""
    head.append(f"Title: {t.upper()}" if t else "Title: ")
    head.append(f"Credit: Սերիա {ep}" if ep else "Credit: ")
    head.append("Author: Անի Մաղաքյան")
    head.append("Contact: Maghakian Scripts · maghakianscripts.com")
    if title_bits:
        head.append("Notes: " + " · ".join(title_bits))
    return "\n".join(head) + "\n\n" + "\n".join(out), ep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx", nargs="+")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--series", help="series title for the title page")
    ap.add_argument("--prefix", default="ep", help="output file prefix")
    ap.add_argument("--no-int-ext", action="store_true", help="don't add ՆԵՐՍ./ԴՐՍ. to scene headings")
    a = ap.parse_args()
    global INT_EXT
    INT_EXT = not a.no_int_ext
    os.makedirs(a.outdir, exist_ok=True)
    for p in a.docx:
        text, ep = convert(p, a.series)
        name = f"{a.prefix}{int(ep):02d}.fountain" if ep else os.path.splitext(os.path.basename(p))[0] + ".fountain"
        dst = os.path.join(a.outdir, name)
        with open(dst, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote", dst)


if __name__ == "__main__":
    sys.exit(main())
