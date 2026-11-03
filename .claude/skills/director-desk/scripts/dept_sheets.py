#!/usr/bin/env python3
"""Costume and props sheets for a set of shooting days (from master.xlsx; scripts add detail later).

python3 dept_sheets.py master.xlsx --days days.txt --out DIR [--extra extra.json]
days.txt lines: <day no>|<date>|<scene ids comma separated>
extra.json (optional, written from the scripts): {"<scene id>": {"costume": {"ԱՐՇԱԿ": "..."}, "props": ["..."], "makeup": "..."}}
Outputs: Կոստյում_Ռեկվիզիտ.xlsx (one sheet per day + Կոստյումների պլան + Ռեկվիզիտի ցանկ) and a branded PDF.
Costume plot rule: one change per character per story day (Օր); 1984 flashbacks (X) are period costume.
"""
import argparse, collections, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plan

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("master"); ap.add_argument("--days", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--extra"); ap.add_argument("--title", default="")
    a = ap.parse_args()
    rows = plan.read_master(a.master); by = {plan.norm_id(r["id"]): r for r in rows}
    extra = json.load(open(a.extra, encoding="utf-8")) if a.extra else {}
    X = {plan.norm_id(k): v for k, v in extra.items()}
    days = []
    for ln in open(a.days, encoding="utf-8"):
        if "|" in ln:
            d, date, ids = ln.strip().split("|", 2)
            days.append((d, date, [by[plan.norm_id(i)] for i in ids.split(", ") if plan.norm_id(i) in by]))
    def sday(r):
        v = str(r["day"]).strip()
        return "1984" if v.upper() in ("X", "Y", "Z") else (f"Օր {v}" if v else "?")
    # costume plot: character -> story day -> change number
    plot = collections.OrderedDict(); changes = collections.defaultdict(dict)
    for d, date, rs in days:
        for r in rs:
            for n in r["names"]:
                k = sday(r)
                if k not in changes[n]:
                    changes[n][k] = len(changes[n]) + 1
                plot.setdefault(n, collections.OrderedDict()).setdefault(k, []).append((d, r))
    def skey(k):
        return (-1 if k == "1984" else int(re.sub(r"\D", "", k) or 999))
    for n in changes:                       # number the changes in story order, 1984 first
        for i, k in enumerate(sorted(changes[n], key=skey), 1):
            changes[n][k] = i
        plot[n] = collections.OrderedDict(sorted(plot[n].items(), key=lambda kv: skey(kv[0])))
    props = collections.OrderedDict()
    for d, date, rs in days:
        for r in rs:
            items = [p.strip() for p in str(r["props"]).split(",") if p.strip()] + X.get(plan.norm_id(r["id"]), {}).get("props", [])
            for p in items:
                props.setdefault(p.lower(), [p, []])[1].append((d, r["id"]))
    import openpyxl
    wb = openpyxl.Workbook(); first = True
    for d, date, rs in days:
        ws = wb.active if first else wb.create_sheet(f"Օր {d}"); first = False
        if ws.title == "Sheet": ws.title = f"Օր {d}"
        ws.append([f"Նկարահանման օր {d} · {date}"]); ws.append([])
        ws.append(["Սերիա/տես․", "Վայր", "Ռեժիմ", "Պատմ. օր", "Կերպար", "Կոստյում (փոփոխ. №)", "Կոստյումի նկարագրություն", "Ռեկվիզիտ", "Գրիմ", "Փլեյսմենթ", "Նշումներ"])
        for r in rs:
            ex = X.get(plan.norm_id(r["id"]), {})
            props_s = ", ".join([p for p in [str(r["props"])] if p] + ex.get("props", []))
            for i, n in enumerate(r["names"] or ["—"]):
                cdesc = ex.get("costume", {}).get(n, "") or (str(r["costume"]) if i == 0 else "")
                ws.append([r["id"] if i == 0 else "", r["loc"] if i == 0 else "", r["mode"] if i == 0 else "", sday(r) if i == 0 else "",
                           n, f"{n} #{changes[n].get(sday(r), '')}" if n != "—" else "", cdesc, props_s if i == 0 else "",
                           ex.get("makeup", "") if i == 0 else "", str(r["placement"]) if i == 0 else "", str(r["notes"]) if i == 0 else ""])
        plan._style_sheet(ws, [9, 30, 9, 8, 22, 18, 34, 30, 18, 16, 30], header_row=3)
    ws = wb.create_sheet("Կոստյումների պլան")
    ws.append(["Կերպար", "Փոփոխություն", "Պատմ. օր", "Տեսարաններ (նկարահանման օր)", "Նկարագրություն", "Չափսեր / նշումներ"])
    for n, sd in plot.items():
        for k, lst in sd.items():
            ws.append([n, f"#{changes[n][k]}", k, ", ".join(f"{r['id']} (Օր {d})" for d, r in lst), "", ""])
    plan._style_sheet(ws, [24, 12, 10, 50, 40, 24])
    ws = wb.create_sheet("Ռեկվիզիտի ցանկ")
    ws.append(["Առարկա", "Տեսարաններ", "Նկարահանման օրեր", "Կրկնվող (continuity)", "Ով է պատասխանատու", "Կարգավիճակ"])
    for k, (name, lst) in props.items():
        ws.append([name, ", ".join(i for _, i in lst), ", ".join(sorted({d for d, _ in lst})), "այո" if len(lst) > 1 else "", "", ""])
    plan._style_sheet(ws, [34, 40, 16, 16, 20, 14])
    os.makedirs(a.out, exist_ok=True)
    p = os.path.join(a.out, "Կոստյում_Ռեկվիզիտ.xlsx"); wb.save(p)
    print(f"wrote {p}: {sum(len(r) for _,_,r in days)} scenes, {len(plot)} characters, {sum(len(v) for v in changes.values())} costume changes, {len(props)} props")

if __name__ == "__main__":
    main()
