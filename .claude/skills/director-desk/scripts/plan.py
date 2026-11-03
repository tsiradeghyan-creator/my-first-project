#!/usr/bin/env python3
"""Production plan for a series, in the studio's own format (season scene list -> day breakdowns).

The studio works like this: a season workbook with one sheet per episode (Սերիա/տես., Նկարահանման վայր,
Ռեժիմ, Դերասաններ, Էջ, Ռեքվիզիտ, Օր = story day, X = flashback; green row = shot). The director/admin picks
scenes for a shooting day into a day sheet, and the scene texts of that day go into one Word file.

  1) master   python3 plan.py master season.xlsx --out plan/ [--aliases plan/aliases.json]
              -> plan/master.xlsx: Բոլորը, one sheet per episode, Ֆլեշբեկ, Չնկարված (by set, for planning),
                 Դերասաններ (cast list with numbers + empty actor/phone columns), Օբյեկտներ, Ստուգում
                 plan/aliases.json: name and location merges found automatically. Edit it and rerun.
  2) day      python3 plan.py day plan/master.xlsx --scenes "8/10,5/3,10/1" --date 18.06 [--day 12]
                 [--texts ep*.docx day*.docx] [--title "Series"] --out plan/
              -> <date> ռազբիվկա.xlsx (day sheet + actors, props, costume, transport, check sheets),
                 <date> ռազբիվկա.pdf (branded print), <date> տեքստեր.docx (scene texts in day order)

Nothing is invented: every value comes from the workbook or the scripts; guesses are listed in Ստուգում.
"""
import argparse
import collections
import copy
import difflib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

GREEN = "FF00B050"
COLS = ["Սերիա/տես․", "Նկարահանման վայր", "Ռեժիմ", "Դերասաններ", "Էջ", "Ռեքվիզիտ", "Օր",
        "Ներս/Դրս", "Օբյեկտ", "Դեր. №", "Մասսովկա / էպիզոդ", "Հագուստ", "Տրանսպորտ", "Փլեյսմենթ",
        "Նշումներ", "Կարգավիճակ", "Ամսաթիվ"]
KEY = ["id", "loc", "mode", "cast", "pages", "props", "day", "ie", "set", "castno", "extras", "costume",
       "transport", "placement", "notes", "status", "date"]

COSTUME = ["ՀԱԳՈՒՍՏ", "ԿՈՍՏՅՈՒՄ", "ԽԱԼԱԹ", "ԶԳԵՍՏ", "ՇԱՊԻԿ", "ԿՈՇԻԿ", "ՀԱԳԱԾ", "ՀԱԳՆՎԱԾ", "ԳԼԽԱՐԿ",
           "ՎԵՐԱՐԿՈՒ", "ԲԱՃԿՈՆ", "ՇԱԼՎԱՐ", "ՓԵՂՈՒՅՑ", "ՀԱՄԱԶԳԵՍՏ", "ԿՈՍՏՅՈՒՄՈՎ"]
TRANSPORT = ["ՄԵՔԵՆԱ", "ՏԱՔՍԻ", "ՏԱՔՈՍԻ", "ԱՎՏՈԲՈՒՍ", "ԳՆԱՑՔ", "ՄՈՏՈՑԻԿԼ", "ՀԵԾԱՆԻՎ", "ՄԻԿՐՈԱՎՏՈԲՈՒՍ"]
PLACEMENT = ["ՓԼԵՅՍՄԵՆԹ", "ՓԼԵՅՄԵՆԹ", "ՓԼԵՅՍՄԵՆՏ"]
EXTRAS = ["ՄԱՍՍՈՎԿԱ", "ՄԱՍՈՎԿԱ", "ԲՆԱԿԻՉՆԵՐ", "ԱՇԽԱՏՈՂՆԵՐ", "ԿՈԼԵԳԱՆԵՐ", "ԶԲՈՍԱՇՐՋԻԿՆԵՐ", "ՀՅՈՒՐԵՐ",
          "ԱՆՑՈՐԴՆԵՐ", "ՈՒՍԱՆՈՂՆԵՐ", "ԲԱՆՎՈՐ", "ԶԻՆՎՈՐԱԿԱՆՆԵՐ"]
YOUNG = "ԵՐԻՏԱՍԱՐԴ"


def up(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().upper()


def norm_id(s):
    """'5/13a' == '5/13ա' == '5/13 Ա' == '5/13ա ՏԵՍԱՐԱՆ'"""
    s = up(s).replace("ՏԵՍԱՐԱՆ", "")
    s = s.translate(str.maketrans({"A": "Ա", "Z": "Զ", "X": "X", "Y": "Y"}))
    return re.sub(r"[\s.․]+", "", s).replace("Ա", "ա").lower()


def has(text, words):
    t = up(text)
    return any(w in t for w in words)


# ---------------------------------------------------------------- read the season workbook
def read_season(path):
    import openpyxl
    wb = openpyxl.load_workbook(path)
    rows, seen = [], {}
    sheets = sorted(wb.worksheets, key=lambda w: "ՖԼԵՇ" in up(w.title))  # episode sheets first
    for ws in sheets:
        head = [up(c.value) for c in ws[1]]

        def col(*names, default):
            for i, h in enumerate(head):
                if any(n in h for n in names):
                    return i
            return default
        ci = dict(id=col("ՍԵՐԻԱ", default=0), loc=col("ՎԱՅՐ", default=1), mode=col("ՌԵԺԻՄ", default=2),
                  cast=col("ԴԵՐԱՍԱՆ", default=3), pages=col("ԷՋ", default=4), props=col("ՌԵՔՎԻԶԻՏ", "ՌԵԿՎԻԶԻՏ", default=5),
                  day=col("ՕՐ", default=6))
        note = ""
        for r in ws.iter_rows(min_row=2):
            v = [c.value for c in r]
            get = lambda k: v[ci[k]] if ci[k] < len(v) else None  # noqa: E731
            rid = str(get("id") or "").strip()
            if not re.match(r"^\d+\s*/", rid):
                if get("loc") and not get("cast"):
                    note = str(get("loc")).strip()        # separators like "Մեր օրեր", "Օրեր անց"
                continue
            fill = r[0].fill.fgColor.rgb if r[0].fill and r[0].fill.fill_type == "solid" else None
            k = norm_id(rid)
            rec = dict(id=rid, ep=rid.split("/")[0].strip(), loc_raw=str(get("loc") or "").strip(),
                       mode=up(get("mode")), cast_raw=str(get("cast") or "").strip(), pages=get("pages"),
                       props_raw=str(get("props") or "").strip(), day=str(get("day") or "").strip(),
                       shot=fill == GREEN, sheet=ws.title, sep=note)
            if k in seen:                                  # flashback sheet repeats episode rows
                seen[k]["shot"] |= rec["shot"]
                seen[k]["flash_sheet"] = True
                continue
            seen[k] = rec
            rows.append(rec)
    for r in rows:
        try:
            r["pages"] = float(r["pages"])
        except (TypeError, ValueError):
            r["pages"] = None
        r["flash"] = r["day"].upper() in ("X", "Y", "Z") or "ՖԼԵՇ" in up(r["loc_raw"]) or "ՖԼԵՇ" in up(r["sheet"])
    return rows


# ---------------------------------------------------------------- clean one row
def split_cast(raw, flash):
    """-> names, extras, notes. Handles '/ԵՐԻՏԱՍԱՐԴ/ ՌՈԲԵՐՏ', 'ՍՈՆԱ/ՎԱՀԱՆԻ ԿԻՆԸ/', 'ԿԻՆ /ԶԲՈՍԱՇՐՋԻԿՆԵՐ'."""
    s = re.sub(r"[?՚ՙ]", "", raw)
    s = re.sub(r"\.(?=[Ա-Ֆ])", ",", s)
    young_all = bool(re.match(r"^\s*/\s*" + YOUNG + r"\s*/", up(s)))
    s = re.sub(r"^\s*/\s*" + YOUNG + r"\s*/", "", s, flags=re.I)
    names, extras, notes = [], [], []
    toks, buf = [], ""
    pieces = s.split(",")
    for i, pc in enumerate(pieces):
        buf = f"{buf},{pc}" if buf else pc
        open_slash = buf.count("/") % 2 == 1 or buf.count("(") > buf.count(")")
        if open_slash and any("/" in x or ")" in x for x in pieces[i + 1:i + 3]):
            continue
        toks.append(buf)
        buf = ""
    if buf:
        toks.append(buf)
    for tok in toks:
        tok = tok.strip()
        if not tok:
            continue
        m = re.match(r"^([^/(]*)[/(](.*?)[/)]?$", tok)
        base, extra = (m.group(1).strip(), m.group(2).strip(" /()")) if m else (tok, "")
        if not base and extra:
            base, extra = extra, ""
        b = up(base)
        if not b:
            continue
        m2 = re.search(r"\s(\d{1,2})\s*Տ\.?$", b)              # 'ՕԳՆԱԿԱՆ 20 Տ'
        if m2:
            b = b[:m2.start()].strip()
            extra = (extra + " " if extra else "") + m2.group(1) + " տ."
        extra = extra.strip(" ,")
        if len(b.split()) >= 3 and re.search(r"(ՈՒՄ|ԵՆՔ|ՉԿԱ|Է|ԵՆ)$", b):   # a sentence, not a name
            notes.append(base.strip())
            continue
        if extra:
            if has(extra, EXTRAS):
                extras.append(f"{b} ({up(extra)})")
                continue
            notes.append(f"{b}: {extra}")
        if has(b, EXTRAS) or re.search(r"ՆԵՐԸ?$", b) or re.match(r"^(ԵՐԿՈՒ|ԵՐԵՔ|ՉՈՐՍ|\d+)\s", b):
            extras.append(b)
            continue
        if young_all and not b.startswith(YOUNG):
            b = f"{YOUNG} {b}"
        names.append(b)
    return names, extras, notes


def split_props(raw, loc_raw):
    out = dict(props=[], costume=[], transport=[], placement=[], notes=[])
    for p in re.split(r"[,՚]\s*|\.\s+", raw):
        p = p.strip(" ,.?՚ՙ")
        if not p:
            continue
        P = up(p)
        if has(P, PLACEMENT) or "ՌՈՅԱԼ ԱՐՄԵՆԻԱ" in P or ("ԵՐԵՄՅԱՆ" in P and "ՄԵՔԵՆԱ" not in P):
            out["placement"].append(p)
        elif has(P, COSTUME):
            out["costume"].append(p)
        elif has(P, TRANSPORT) and len(P.split()) <= 4:
            out["transport"].append(p)
        elif len(P.split()) >= 5 or re.search(r" (Է|ԵՆ|ԷՐ|ԷԻՆ) |ՏԵՍ[\s,.]|ՍԵՐԻԱ|^\S+ՈՒՄ Է", P):
            out["notes"].append(p)
        else:
            out["props"].append(p)
    if has(loc_raw, PLACEMENT) and not out["placement"]:
        out["placement"].append("✓ (տես վայրը)")
    return out


def clean_loc(raw):
    s = up(raw).replace("ԻՆՉ-ՈՐ", "ԻՆՉՈՐ").replace("ԻՆՉ ՈՐ", "ԻՆՉՈՐ")
    s = re.sub(r"\.(?=[Ա-Ֆ])", ", ", s)
    notes = []
    for pat, note in ((r"\d{4}\s*Թ\.?Վ\.?", None), (r"ՖԼԵՇԲԵ[ՔԿ]", None), (r"ՓԼԵՅ\S*", None), (r"\bԳՏՆԵԼ\b", "գտնել լոկացիա")):
        if re.search(pat, s):
            if note:
                notes.append(note)
            s = re.sub(pat, " ", s)
    s = re.sub(r"\s*[,։:;/\-–—]\s*|\.\s+", ", ", s)
    s = re.sub(r"(^|, )(ՑԵՐԵԿ|ԵՐԵԿՈ|ԳԻՇԵՐ|ԱՌԱՎՈՏ)(?=,|$)", "", s)
    s = re.sub(r"[.․,\s/]+$", "", re.sub(r"^[,\s]+", "", s)).replace("ԻՆՉՈՐ", "ԻՆՉ-ՈՐ")
    s = re.sub(r"(,\s*)+", ", ", s).strip(", ")
    return s, notes


# ---------------------------------------------------------------- aliases (merges) found automatically
def build_aliases(rows, path):
    user = {"names": {}, "locations": {}}
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            user = json.load(f)
    cnt = collections.Counter(n for r in rows for n in r["names"])
    auto_n, maybe = {}, []
    big = [n for n, c in cnt.items() if c >= 5]
    for n in cnt:
        if n in user["names"]:
            continue
        base = n.replace(YOUNG + " ", "")
        pref = YOUNG + " " if n.startswith(YOUNG) else ""
        # short form inside one word: ՌՈԲ -> ՌՈԲԵՐՏ (the long one must be clearly more frequent)
        hits = [b for b in cnt if b != n and b.startswith(pref) and len(base) >= 3
                and b.replace(YOUNG + " ", "").startswith(base) and " " not in b.replace(YOUNG + " ", "")[len(base):]
                and cnt[b] >= 3 * cnt[n]]
        if len(hits) == 1:
            auto_n[n] = hits[0]
            continue
        if n in big or " " in base:
            continue
        close = difflib.get_close_matches(n, big, 1, 0.84)
        if close:
            auto_n[n] = close[0]
    sets = collections.Counter(r["set"] for r in rows)
    auto_l = {}
    for s in sets:
        if s in user["locations"]:
            continue
        close = [c for c in difflib.get_close_matches(s, [x for x in sets if x != s], 3, 0.84) if sets[c] > sets[s]]
        if close:
            auto_l[s] = close[0]
    for a in list(sets):
        for b in sets:
            if a < b and a not in auto_l and b not in auto_l and difflib.SequenceMatcher(None, a, b).ratio() >= 0.7:
                maybe.append(f"{a} ↔ {b}")
    names = {**auto_n, **user["names"]}
    locs = {**auto_l, **user["locations"]}
    if path:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"names": names, "locations": locs,
                       "_how": "Ձախը փոխարինվում է աջով. ավելացրու կամ ջնջիր և նորից գործարկիր master-ը։",
                       "_maybe_same_locations": maybe}, f, ensure_ascii=False, indent=1)
    return names, locs, auto_n, auto_l, maybe


def process(rows, aliases_path):
    from kit_docx_to_fountain import guess_int_ext
    for r in rows:
        r["names"], r["extras"], cnotes = split_cast(r["cast_raw"], r["flash"])
        loc, lnotes = clean_loc(r["loc_raw"])
        parts = [x.strip(" .․,") for x in loc.split(", ") if x.strip(" .․,")]
        loc = ", ".join(parts)
        r["loc"] = loc
        r["set"] = parts[0]
        # 'ՀՅՈՒՐԱՆՈՑԻ ՀԱՄԱՐ' -> set ՀՅՈՒՐԱՆՈՑ when that set exists
        r["_parts"] = parts
        p = split_props(r["props_raw"], r["loc_raw"])
        r.update(props=p["props"], costume=p["costume"], transport=p["transport"], placement=p["placement"],
                 notes=cnotes + lnotes + p["notes"] + ([r["sep"]] if r["sep"] else []))
        ie, sure = guess_int_ext(loc)
        ie = ie.replace(".", "")
        L = up(loc)
        if not sure:
            if any(w in L for w in ("ԳՅՈՒՂ", "ՄԱՅՐՈՒՂԻ", "ՀՈՎԻՏ", "ՏԱՐԱԾՔ", "ՍԻՄՖՈՆԻԱ", "ԳԵՂԱՐԴ", "ՃԱՆԱՊ")):
                ie, sure = "ԴՐՍ", True
            elif any(w in L for w in ("ՍԵՆՅԱԿ", "ՄԵԿՈՒՍԱՐԱՆ", "ՀԱՄԱՐ")):
                ie, sure = "ՆԵՐՍ", True
        r["ie"] = ie + ("" if sure else " ?")
    from screenplay import CITIES
    for r in rows:                                  # 'ԵՐԵՒԱՆ, ԱՅԳԻ' -> set ԱՅԳԻ
        while len(r["_parts"]) > 1 and r["_parts"][0] in CITIES:
            r["_parts"] = r["_parts"][1:]
        r["set"] = r["_parts"][0]
    known = collections.Counter(r["set"] for r in rows)
    for r in rows:
        st = r["set"]
        # 'ՀՅՈՒՐԱՆՈՑԻ ՀԱՄԱՐ' -> ՀՅՈՒՐԱՆՈՑ ; 'ՌՈԲԵՐՏԻ ԱՎՏՈՏՆԱԿԻ ԴԻՄԱՑ' -> ՌՈԲԵՐՏԻ ԱՎՏՈՏՆԱԿ
        best = ""
        for k in known:
            if k != st and known[k] >= 2 and len(k) > len(best) and re.match(re.escape(k) + r"(Ի)?( |$)", st):
                best = k
        if not best:
            w = st.split(" ")
            if len(w) >= 2 and w[0].endswith("Ի"):
                stem = re.sub(r"Ն?Ի$", "", w[0])
                close = difflib.get_close_matches(stem, [k for k in known if known[k] >= 3], 1, 0.8)
                best = close[0] if close else ""
        if best:
            rest = st[len(best):].lstrip("Ի ").strip()
            r["set"] = best
            if rest:
                r["_parts"] = [best, rest] + r["_parts"][1:]
    young_ok = {n.replace(YOUNG + " ", "") for r in rows for n in r["names"] if n.startswith(YOUNG)}
    single = {n for r in rows for n in r["names"] if " " not in n}
    issues = []
    for r in rows:                      # 'ԵՐԻՏԱՍԱՐԴ ՌՈԲԵՐՏ ԱՆՈՒՇ' = two people (missing comma)
        nn = []
        for n in r["names"]:
            bare = n.replace(YOUNG + " ", "").split(" ")
            if len(bare) > 1 and all(b in young_ok or b in single for b in bare) and any(b in young_ok for b in bare):
                pref = YOUNG + " " if n.startswith(YOUNG) else ""
                issues.append(("Ստորակետ", r["id"], f"«{n}» → {', '.join(pref + b for b in bare)}"))
                nn += [pref + b for b in bare]
            else:
                nn.append(n)
        r["names"] = nn
    names, locs, auto_n, auto_l, maybe = build_aliases(rows, aliases_path)
    unsure_ie = {}
    for r in rows:
        nn, made_young = [], []
        for n in r["names"]:
            n = names.get(n, n)
            if r["flash"] and not n.startswith(YOUNG) and n in young_ok:
                made_young.append(n)
                n = names.get(f"{YOUNG} {n}", f"{YOUNG} {n}")
            nn.append(n)
        if made_young:
            issues.append(("Ֆլեշբեք", r["id"], f"{', '.join(made_young)} → {YOUNG} (ֆլեշբեք, ենթադրված)"))
        dup = [n for n, c in collections.Counter(nn).items() if c > 1]
        if dup:
            issues.append(("Կրկնություն", r["id"], "կրկնված անուն. " + ", ".join(dup)))
        r["names"] = list(dict.fromkeys(nn))
        r["set"] = locs.get(r["set"], r["set"])
        if r["pages"] is None:
            issues.append(("Էջ", r["id"], "էջերի քանակը նշված չէ"))
        if not r["day"]:
            issues.append(("Օր", r["id"], "պատմության օրը նշված չէ"))
        if "?" in r["cast_raw"] + r["props_raw"]:
            issues.append(("Բաց հարց", r["id"], "«?» կա. " + (r["cast_raw"] if "?" in r["cast_raw"] else r["props_raw"])))
        if r["ie"].endswith("?"):
            unsure_ie.setdefault(r["loc"], (r["ie"], []))[1].append(r["id"])
    for loc, (ie, ids) in unsure_ie.items():
        issues.append(("Ներս/Դրս", ", ".join(ids), f"{loc} → {ie} (ստուգել)"))
    for a, b in auto_n.items():
        issues.insert(0, ("Անուն", "", f"{a} → {b}"))
    for a, b in auto_l.items():
        issues.insert(0, ("Լոկացիա", "", f"{a} → {b}"))
    for m in maybe:
        issues.append(("Լոկացիա?", "", f"հնարավոր է՝ նույնն են. {m}"))
    cnt = collections.Counter(n for r in rows for n in r["names"])
    order = [n for n, _ in sorted(cnt.items(), key=lambda x: (-x[1], x[0]))]
    num = {n: i + 1 for i, n in enumerate(order)}
    for r in rows:
        r["castno"] = ", ".join(str(num[n]) for n in r["names"])
        r["cast"] = ", ".join(r["names"])
        r["status"] = "Նկարված" if r["shot"] else ""
        r["date"] = r.get("date", "")
    return rows, num, issues


# ---------------------------------------------------------------- xlsx writing
def _style_sheet(ws, widths, header_row=1):
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    thin = Side(style="thin", color="D0D0D0")
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[ws.cell(row=header_row, column=i).column_letter].width = w
    for c in ws[header_row]:
        c.font = Font(name="Sylfaen", bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor="111111")
        c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[header_row].height = 30
    ws.freeze_panes = ws.cell(row=header_row + 1, column=2)
    for row in ws.iter_rows(min_row=header_row + 1):
        for c in row:
            c.font = Font(name="Sylfaen", size=10, bold=c.font.bold)
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c.border = Border(bottom=thin)
    ws.auto_filter.ref = f"A{header_row}:{ws.cell(row=header_row, column=ws.max_column).column_letter}{ws.max_row}"


WIDTHS = [9, 42, 9, 40, 6, 34, 6, 10, 22, 9, 26, 24, 18, 16, 34, 11, 10]


def scene_rows(ws, rows, start=1):
    from openpyxl.styles import PatternFill
    ws.append(COLS)
    for r in rows:
        vals = []
        for k in KEY:
            v = r.get(k, "")
            if isinstance(v, list):
                v = ", ".join(v)
            if k == "loc":
                v = r["loc"]
            vals.append(v)
        ws.append(vals)
        fill = PatternFill("solid", fgColor="00B050" if r["shot"] else "FFFF00")
        ws.cell(row=ws.max_row, column=1).fill = fill
        if r["mode"] in ("ԵՐԵԿՈ", "ԳԻՇԵՐ"):
            ws.cell(row=ws.max_row, column=3).fill = PatternFill("solid", fgColor="DDE7F5")
    ws.append([""] * 4 + [f"=SUM(E2:E{ws.max_row})"])
    _style_sheet(ws, WIDTHS)


def write_master(rows, num, issues, out):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Բոլորը"
    scene_rows(ws, rows)
    eps = sorted({r["ep"] for r in rows}, key=lambda x: int(re.sub(r"\D", "", x) or 0))
    for e in eps:
        scene_rows(wb.create_sheet(e), [r for r in rows if r["ep"] == e])
    fl = [r for r in rows if r["flash"]]
    if fl:
        scene_rows(wb.create_sheet("Ֆլեշբեկ"), fl)
    left = sorted([r for r in rows if not r["shot"]], key=lambda r: (r["set"], r["mode"], r["ep"]))
    scene_rows(wb.create_sheet("Չնկարված"), left)
    # cast list
    ws = wb.create_sheet("Դերասաններ")
    ws.append(["№", "Կերպար", "Տեսարան", "Էջ", "Մնացած տեսարան", "Մնացած էջ", "Սերիաներ", "Դերասան",
               "Հեռախոս", "Նշումներ"])
    for n, i in sorted(num.items(), key=lambda x: x[1]):
        mine = [r for r in rows if n in r["names"]]
        lf = [r for r in mine if not r["shot"]]
        ws.append([i, n, len(mine), sum(r["pages"] or 0 for r in mine), len(lf), sum(r["pages"] or 0 for r in lf),
                   ", ".join(sorted({r["ep"] for r in mine}, key=lambda x: int(re.sub(r"\D", "", x) or 0))), "", "", ""])
    _style_sheet(ws, [5, 28, 9, 7, 10, 9, 22, 28, 16, 30])
    # sets
    ws = wb.create_sheet("Օբյեկտներ")
    ws.append(["Օբյեկտ", "Ներս/Դրս", "Տեսարան", "Էջ", "Մնացած տեսարան", "Մնացած էջ", "Ցերեկ", "Երեկո",
               "Սերիաներ", "Սենյակներ / մասեր"])
    by = collections.defaultdict(list)
    for r in rows:
        by[r["set"]].append(r)
    for s, rs in sorted(by.items(), key=lambda x: -sum(r["pages"] or 0 for r in x[1] if not r["shot"])):
        lf = [r for r in rs if not r["shot"]]
        ws.append([s, ", ".join(sorted({r["ie"].replace(" ?", "") for r in rs})), len(rs),
                   sum(r["pages"] or 0 for r in rs), len(lf), sum(r["pages"] or 0 for r in lf),
                   sum(1 for r in rs if r["mode"] == "ՑԵՐԵԿ"), sum(1 for r in rs if r["mode"] != "ՑԵՐԵԿ"),
                   ", ".join(sorted({r["ep"] for r in rs}, key=lambda x: int(re.sub(r"\D", "", x) or 0))),
                   "; ".join(sorted({", ".join(r["_parts"][1:]) for r in rs if len(r["_parts"]) > 1}))])
    _style_sheet(ws, [30, 12, 9, 7, 10, 9, 7, 7, 18, 60])
    ws = wb.create_sheet("Ստուգում")
    ws.append(["Տեսակ", "Տեսարան", "Ինչ"])
    for t in issues:
        ws.append(list(t))
    _style_sheet(ws, [14, 10, 100])
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, "master.xlsx")
    wb.save(p)
    return p


def read_master(path):
    import openpyxl
    wb = openpyxl.load_workbook(path)
    ws = wb["Բոլորը"]
    head = [c.value for c in ws[1]]
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        d = {KEY[i]: (r[i] if r[i] is not None else "") for i in range(min(len(KEY), len(head)))}
        d["shot"] = d["status"] == "Նկարված"
        d["names"] = [x.strip() for x in str(d["cast"]).split(",") if x.strip()]
        d["id"] = str(d["id"])
        try:
            d["pages"] = float(d["pages"])
        except (TypeError, ValueError):
            d["pages"] = None
        rows.append(d)
    return rows


# ---------------------------------------------------------------- day
def texts_index(paths):
    """scene id -> (doc, [paragraph elements]) from KIT .docx (SCENE HEADING style or 'N/M. ՏԵՍԱՐԱՆ')."""
    import docx
    idx = {}
    for p in paths:
        d = docx.Document(p)
        cur = None
        for par in d.paragraphs:
            t = par.text.strip()
            m = re.match(r"^(\d+\s*/\s*[\w,.]+)", t)
            if (par.style.name.upper().startswith("SCENE") or re.search(r"ՏԵՍԱՐԱՆ\s*$", up(t))) and m:
                cur = norm_id(m.group(1).rstrip("."))
                idx.setdefault(cur, (d, p, []))
                if idx[cur][1] != p:
                    cur = None                      # already have this scene from another file
                    continue
            if cur:
                idx[cur][2].append(par._p)
    return idx


def write_day_texts(order, idx, out_path):
    import docx
    first = next((idx[k][0] for k in order if k in idx), None)
    if first is None:
        return []
    doc = docx.Document(idx[next(k for k in order if k in idx)][1])
    body = doc.element.body
    for el in list(body):
        if not el.tag.endswith("sectPr"):
            body.remove(el)
    sect = body[-1] if len(body) else None
    missing = []
    for k in order:
        if k not in idx:
            missing.append(k)
            continue
        for el in idx[k][2]:
            if sect is not None:
                sect.addprevious(copy.deepcopy(el))
            else:
                body.append(copy.deepcopy(el))
    doc.save(out_path)
    return missing


def cmd_day(a):
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    rows = read_master(a.master)
    by = {norm_id(r["id"]): r for r in rows}
    want = [s.strip() for s in re.split(r"[;\n]|,(?=\s*\d+\s*/)", a.scenes) if s.strip()]
    order = [norm_id(s) for s in want]
    issues, day = [], []
    shot_ids = []
    for s, k in zip(want, order):
        if k not in by:
            near = [r["id"] for kk, r in by.items() if kk.split("/")[0] == k.split("/")[0]
                    and re.sub(r"\D+$", "", kk) == re.sub(r"\D+$", "", k)]
            issues.append(("Չկա", s, "այս տեսարանը գլխավոր ցուցակում չկա" +
                           (f". գուցե՝ {', '.join(near)}" if near else "")))
            continue
        if order.count(k) > 1 and ("Կրկնություն", s) not in [(i[0], i[1]) for i in issues]:
            issues.append(("Կրկնություն", s, "օրվա ցուցակում երկու անգամ է"))
        r = by[k]
        if r["shot"]:
            shot_ids.append(s)
        day.append(r)
    if shot_ids:
        issues.append(("Նկարված", ", ".join(shot_ids), "գլխավոր ցուցակում արդեն կանաչ են (նկարված)"))
    os.makedirs(a.out, exist_ok=True)
    stem = os.path.join(a.out, f"{a.date} ռազբիվկա")
    # texts
    missing_txt = []
    if a.texts:
        idx = texts_index(a.texts)
        missing_txt = write_day_texts([norm_id(r["id"]) for r in day], idx, os.path.join(a.out, f"{a.date} տեքստեր.docx"))
        for k in missing_txt:
            issues.append(("Տեքստ", next((r["id"] for r in day if norm_id(r["id"]) == k), k), "տեքստը չգտնվեց տրված ֆայլերում"))
    # cast of the day
    cast = collections.OrderedDict()
    for i, r in enumerate(day, 1):
        for n in r["names"]:
            cast.setdefault(n, []).append(i)
    nums = {}
    for r in rows:
        for n, c in zip(r["names"], str(r["castno"]).split(", ")):
            nums.setdefault(n, c)
    pages = sum(r["pages"] or 0 for r in day)
    # xlsx
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ռազբիվկա"
    title = a.title or "Նկարահանման օր"
    ws.append([f"{title} · {a.date}" + (f" · Նկարահանման օր {a.day}" if a.day else "")])
    ws.append([f"Տեսարան՝ {len(day)} · Էջ՝ {pages:g} · Դերասաններ՝ {len(cast)} · Հավաք՝ {a.call or '_____'} · "
               f"Հասցե՝ {a.address or '_____'}"])
    ws.append([])
    head = ["#"] + COLS[:7] + ["Ներս/Դրս", "Մասսովկա / էպիզոդ", "Հագուստ", "Տրանսպորտ", "Փլեյսմենթ", "Նշումներ", "Ժամ"]
    ws.append(head)
    for i, r in enumerate(day, 1):
        ws.append([i, r["id"], r["loc"], r["mode"], r["cast"], r["pages"], r["props"], r["day"], r["ie"],
                   r["extras"], r["costume"], r["transport"], r["placement"], r["notes"], ""])
        if r["mode"] != "ՑԵՐԵԿ":
            for c in ws[ws.max_row]:
                c.fill = PatternFill("solid", fgColor="DDE7F5")
    ws.append(["", "", "", "", "Ընդամենը էջ", f"=SUM(F5:F{ws.max_row})"])
    _style_sheet(ws, [4, 9, 34, 9, 34, 6, 30, 6, 10, 22, 22, 16, 16, 30, 7], header_row=4)
    ws["A1"].font = Font(name="Sylfaen", bold=True, size=14)
    ws["A2"].font = Font(name="Sylfaen", size=10, color="555555")
    ws[f"E{ws.max_row}"].font = Font(name="Sylfaen", bold=True)
    ws[f"F{ws.max_row}"].font = Font(name="Sylfaen", bold=True)
    s2 = wb.create_sheet("Դերասաններ")
    s2.append(["№", "Կերպար", "Տեսարաններ (օրվա հերթականությամբ)", "Էջ", "Դերասան", "Հավաք", "Գրիմ", "Պատրաստ", "Ազատ"])
    for n, idxs in cast.items():
        s2.append([nums.get(n, ""), n, ", ".join(day[i - 1]["id"] for i in idxs),
                   sum(day[i - 1]["pages"] or 0 for i in idxs), "", "", "", "", ""])
    _style_sheet(s2, [5, 26, 36, 6, 24, 9, 9, 9, 9])
    for name, key in (("Ռեկվիզիտ", "props"), ("Հագուստ", "costume"), ("Տրանսպորտ", "transport"), ("Մասսովկա", "extras")):
        s = wb.create_sheet(name)
        s.append(["#", "Սերիա/տես․", "Վայր", "Կերպարներ", name])
        for i, r in enumerate(day, 1):
            if r[key]:
                s.append([i, r["id"], r["loc"], r["cast"], r[key]])
        _style_sheet(s, [4, 10, 34, 34, 50])
    s = wb.create_sheet("Ստուգում")
    s.append(["Տեսակ", "Տեսարան", "Ինչ"])
    for t in issues:
        s.append(list(t))
    _style_sheet(s, [14, 10, 90])
    wb.save(stem + ".xlsx")
    # pdf
    try:
        day_pdf(a, title, day, cast, nums, pages, issues, stem + ".pdf")
    except Exception as e:  # PDF is optional (needs Chromium)
        print("! PDF skipped:", e)
    print(f"day {a.date}: {len(day)} scenes, {pages:g} pages, {len(cast)} cast, issues {len(issues)}")
    for t in issues:
        print("  ", " · ".join(map(str, t)))


def day_pdf(a, title, day, cast, nums, pages, issues, out):
    import pack_design as dz
    e = dz.esc
    rows = "".join(
        f'<tr><td class="n">{i}</td><td><b>{e(r["id"])}</b></td><td><b>{e(r["loc"])}</b>'
        f'{"<br><span class=note>" + e(r["ie"]) + "</span>" if r["ie"] else ""}</td>'
        f'<td>{dz.chip(r["mode"], "night") if r["mode"] != "ՑԵՐԵԿ" else e(r["mode"])}</td>'
        f'<td>{e(r["cast"])}{"<br><span class=note>" + e(r["extras"]) + "</span>" if r["extras"] else ""}</td>'
        f'<td class="num">{r["pages"] or "":g}</td>'.replace(":g}", "}") if False else
        f'<tr><td class="n">{i}</td><td><b>{e(r["id"])}</b></td><td><b>{e(r["loc"])}</b>'
        f'{"<br><span class=note>" + e(r["ie"]) + "</span>" if r["ie"] else ""}</td>'
        f'<td>{dz.chip(r["mode"], "night") if r["mode"] != "ՑԵՐԵԿ" else e(r["mode"])}</td>'
        f'<td>{e(r["cast"])}{"<br><span class=note>" + e(r["extras"]) + "</span>" if r["extras"] else ""}</td>'
        f'<td class="num">{("%g" % r["pages"]) if r["pages"] else ""}</td><td class="num">{e(r["day"])}</td>'
        f'<td>{e(r["props"])}</td><td>{e(r["costume"])}</td><td>{e(r["transport"])}</td>'
        f'<td>{e(r["placement"])}</td><td class="note">{e(r["notes"])}</td><td></td></tr>'
        for i, r in enumerate(day, 1))
    table = (f'<table class="day"><thead><tr><th>#</th><th>Սերիա/տես․</th><th>Նկարահանման վայր</th><th>Ռեժիմ</th>'
             f'<th>Դերասաններ</th><th class="num">Էջ</th><th class="num">Օր</th><th>Ռեքվիզիտ</th><th>Հագուստ</th>'
             f'<th>Տրանսպորտ</th><th>Փլեյսմենթ</th><th>Նշումներ</th><th>Ժամ</th></tr></thead><tbody>{rows}'
             f'<tr class="tot"><td></td><td></td><td></td><td></td><td><b>Ընդամենը</b></td>'
             f'<td class="num"><b>{pages:g}</b></td><td colspan="7"></td></tr></tbody></table>')
    head = (f'<header class="mast" style="padding-bottom:8pt"><div class="doc">Օրվա ռազբիվկա'
            f'{" · Նկարահանման օր " + e(str(a.day)) if a.day else ""}</div><h1 style="font-size:22pt">{e(a.date)}'
            f' · {e(title)}</h1></header>')
    st = dz.stats([(len(day), "տեսարան"), (f"{pages:g}", "էջ"), (len(cast), "դերասան"),
                   (e(a.call or "—"), "հավաք")])
    crow = "".join(f'<tr><td class="n">{e(str(nums.get(n, "")))}</td><td><b>{e(n)}</b></td>'
                   f'<td>{e(", ".join(day[i - 1]["id"] for i in ix))}</td><td></td><td></td><td></td></tr>'
                   for n, ix in cast.items())
    ctab = ('<h2><span class="no">02</span>Դերասաններ</h2><table><thead><tr><th>№</th><th>Կերպար</th>'
            '<th>Տեսարաններ</th><th>Դերասան</th><th>Հավաք</th><th>Գրիմ</th></tr></thead>'
            f'<tbody>{crow}</tbody></table>')
    chk = ""
    if issues:
        chk = ('<h2><span class="no">03</span>Ստուգում</h2><ul>' +
               "".join(f"<li><b>{e(t[1])}</b> · {e(t[2])}</li>" for t in issues) + "</ul>")
    css = ("<style>@page{size:A4 landscape;margin:22mm 12mm 16mm 12mm} table.day{font-size:7.4pt}"
           " table.day td{padding:4pt 5pt 4pt 0} .stats{grid-template-columns:repeat(4,1fr)}"
           " tr.tot td{border-top:1.2pt solid #000;border-bottom:0}</style>")
    body = css + head + st + '<h2><span class="no">01</span>Տեսարաններ</h2>' + table + ctab + chk
    with dz.Renderer() as RN:
        RN.pdf(dz.page(body, "doc", f"{a.date} ռազբիվկա", "ՌԵԺԻՍՈՐԻ ՕԳՆԱԿԱՆ · ԱԴՄԻՆ · ՏՆՕՐԵՆ",
                       f"{title} · {a.date}"), out, html_dir=os.path.join(os.path.dirname(out), "_html"))


def cmd_master(a):
    os.makedirs(a.out, exist_ok=True)
    rows = read_season(a.season)
    rows, num, issues = process(rows, a.aliases or os.path.join(a.out, "aliases.json"))
    p = write_master(rows, num, issues, a.out)
    shot = [r for r in rows if r["shot"]]
    print(f"master: {len(rows)} scenes, {sum(r['pages'] or 0 for r in rows):g} pages, shot {len(shot)} "
          f"({sum(r['pages'] or 0 for r in shot):g} p.), cast {len(num)}, sets {len({r['set'] for r in rows})}, "
          f"issues {len(issues)} -> {p}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("master")
    m.add_argument("season")
    m.add_argument("--out", default="plan")
    m.add_argument("--aliases")
    d = sub.add_parser("day")
    d.add_argument("master")
    d.add_argument("--scenes", required=True, help='"8/10, 5/3, 10/1" in shooting order')
    d.add_argument("--date", required=True)
    d.add_argument("--day", help="shooting day number")
    d.add_argument("--call", help="call time")
    d.add_argument("--address")
    d.add_argument("--title")
    d.add_argument("--texts", nargs="*", help="KIT .docx files with the scene texts")
    d.add_argument("--out", default="plan")
    a = ap.parse_args()
    return cmd_master(a) if a.cmd == "master" else cmd_day(a)


if __name__ == "__main__":
    sys.exit(main())
