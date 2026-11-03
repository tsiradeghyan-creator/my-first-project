#!/usr/bin/env python3
"""Project workbook: crew & cast with rates, attendance per shooting day, expenses, and cost/progress reports.

project.xlsx is the single source of truth. The admin may edit it by hand (rates, names, ticks, expenses);
every command re-reads it.
  Կազմ           people: department, position, name, character (actors), rate, rate type, phone
  Ներկայություն  one column per shooting day, 1 = was on set (like a Day Out of Days, with live formulas)
  Օրեր           one row per shooting day: scenes, pages, people cost, expenses, total (formulas)
  Ծախսեր         expenses: date, category, description, payee, amount, paid by, receipt
  Ամփոփ          totals by day, week, month and the whole project (refreshed by `report`)
"""
import collections
import datetime as dt
import os
import re
import shutil

CUR = "֏"
RATE_TYPES = ["Օրական", "Ամսական", "Միանգամյա"]
CATEGORIES = ["Լոկացիա", "Տրանսպորտ", "Վառելիք", "Սնունդ", "Ռեկվիզիտ", "Հագուստ", "Գրիմ", "Տեխնիկա",
              "Մասսովկա", "Կապ", "Այլ"]
CREW = [  # department, position (Armenian series crew, edit freely in the workbook)
    ("Ռեժիսուրա", "Ռեժիսոր"), ("Ռեժիսուրա", "Երկրորդ ռեժիսոր"), ("Ռեժիսուրա", "Ռեժիսորի օգնական"),
    ("Ռեժիսուրա", "Սցենարի սուպերվայզեր"), ("Պրոդյուսերական", "Գլխավոր պրոդյուսեր"),
    ("Պրոդյուսերական", "Լայն-պրոդյուսեր"), ("Պրոդյուսերական", "Ֆիլմի տնօրեն"), ("Պրոդյուսերական", "Ադմինիստրատոր"),
    ("Կամերա", "Օպերատոր"), ("Կամերա", "Օպերատորի օգնական"), ("Լույս", "Լուսավորող (գաֆեր)"),
    ("Լույս", "Լուսավորողի օգնական"), ("Ձայն", "Ձայնի օպերատոր"), ("Ձայն", "Բում-օպերատոր"),
    ("Նկարչական", "Նկարիչ-բեմադրիչ"), ("Նկարչական", "Ռեկվիզիտոր"), ("Կոստյում", "Կոստյումեր"),
    ("Գրիմ", "Գրիմեր"), ("Տրանսպորտ", "Վարորդ"), ("Տրանսպորտ", "Վարորդ 2"), ("Կեյթերինգ", "Կեյթերինգ"),
    ("Հետարտադրություն", "Մոնտաժող"), ("Լուսանկար", "Լուսանկարիչ"),
]


# House numbers and market prices (Tigran, 2026-11-03). The admin fills/updates the empty cells.
PRICE_LIST = [
    ("Էջ օրական (սերիալ)", "էջ / օր", None, None, "13–30", "Տիգրան, 2026-11-03"),
    ("Հերթափոխ", "ժամ", None, None, "12", "Տիգրան, 2026-11-03"),
    ("Մեքենա (տեղափոխում)", "կմ", 150, None, "≥ 150 ֏/կմ", "Տիգրան. նվազագույնը"),
    ("Սնունդ", "մարդ / օր", None, None, "1 ճաշ բոլորին", "+ թեյ, սուրճ, քաղցր՝ առանձին"),
    ("Թեյ, սուրճ, քաղցր", "օր", None, None, "", ""),
    ("Տուն / բնակարան (լոկացիա)", "օր", None, None, "", "Գինը բանակցային է. նույն տունը՝ $100-ից $1000"),
    ("Տեխնիկայի մեքենա", "օր", None, None, "", ""),
    ("Տաքսի (քաղաքում)", "ուղևորություն", None, None, "", ""),
    ("Վառելիք", "լիտր", None, None, "", ""),
    ("Մասսովկա", "մարդ / օր", None, None, "", ""),
]


def money(v):
    v = round(float(v or 0))
    return f"{v:,}".replace(",", " ") + f" {CUR}"


def parse_date(s, year=None):
    if isinstance(s, (dt.date, dt.datetime)):
        return s.date() if isinstance(s, dt.datetime) else s
    s = str(s).strip()
    for fmt in ("%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    m = re.match(r"^(\d{1,2})[./](\d{1,2})$", s)
    if m:
        return dt.date(year or dt.date.today().year, int(m.group(2)), int(m.group(1)))
    raise ValueError(f"date? {s}")


def dstr(d):
    return d.strftime("%d.%m.%Y")


# ---------------------------------------------------------------- workbook io
def _styles():
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    return Font, PatternFill, Alignment, Border, Side


def _head(ws, cols, widths):
    Font, PatternFill, Alignment, Border, Side = _styles()
    ws.append(cols)
    for i, c in enumerate(ws[1]):
        c.font = Font(name="Sylfaen", bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor="111111")
        c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[c.column_letter].width = widths[i] if i < len(widths) else 12
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"


def init_project(master, out, title=""):
    import openpyxl
    from openpyxl.worksheet.datavalidation import DataValidation
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Կազմ"
    _head(ws, ["ID", "Բաժին", "Պաշտոն", "Անուն Ազգանուն", "Կերպար", "Դրույք " + CUR, "Դրույքի տեսակ",
               "Հեռախոս", "Նշում"], [6, 16, 24, 26, 24, 13, 14, 15, 24])
    i = 0
    for dep, pos in CREW:
        i += 1
        ws.append([f"C{i:02d}", dep, pos, "", "", None, "Օրական", "", ""])
    if master and os.path.exists(master):
        mw = openpyxl.load_workbook(master)
        if "Դերասաններ" in mw.sheetnames:
            for r in mw["Դերասաններ"].iter_rows(min_row=2, values_only=True):
                if r[0] and r[1]:
                    ws.append([f"A{int(r[0]):02d}", "Դերասաններ", "Դերասան", "", r[1], None, "Օրական", "", ""])
    dv = DataValidation(type="list", formula1='"' + ",".join(RATE_TYPES) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"G2:G{ws.max_row + 200}")
    for row in ws.iter_rows(min_row=2, min_col=6, max_col=6):
        for c in row:
            c.number_format = '#,##0'
    att = wb.create_sheet("Ներկայություն")
    _head(att, ["ID", "Պաշտոն", "Անուն / կերպար", "Դրույք", "Տեսակ", "Օրեր", "Վճարվելիք " + CUR],
          [6, 22, 24, 11, 10, 7, 14])
    for r in range(2, ws.max_row + 1):
        att.append([f"=Կազմ!A{r}", f"=Կազմ!C{r}", f'=IF(Կազմ!D{r}<>"",Կազմ!D{r},Կազմ!E{r})',
                    f"=Կազմ!F{r}", f"=Կազմ!G{r}", None, None])
    days = wb.create_sheet("Օրեր")
    _head(days, ["Ամսաթիվ", "Նկ. օր №", "Տեսարաններ", "Էջ", "Մարդիկ", "Կազմի ծախս " + CUR,
                 "Այլ ծախսեր " + CUR, "Ընդամենը " + CUR], [12, 9, 50, 7, 8, 15, 15, 15])
    ex = wb.create_sheet("Ծախսեր")
    _head(ex, ["Ամսաթիվ", "Կատեգորիա", "Նկարագրություն", "Ում / որտեղ", "Գումար " + CUR, "Վճարող",
               "Չեկ", "Նշում"], [12, 14, 40, 22, 14, 16, 26, 22])
    dv2 = DataValidation(type="list", formula1='"' + ",".join(CATEGORIES) + '"', allow_blank=True)
    ex.add_data_validation(dv2)
    dv2.add("B2:B2000")
    pl = wb.create_sheet("Գնացուցակ")
    _head(pl, ["Ինչ", "Միավոր", "Նվազագույն " + CUR, "Առավելագույն " + CUR, "Մեր նորմա", "Աղբյուր / նշում"],
          [34, 16, 14, 14, 18, 50])
    for row in PRICE_LIST:
        pl.append(list(row))
    sm = wb.create_sheet("Ամփոփ")
    sm.append([title or "Նախագիծ"])
    wb.properties.title = title or "Project"
    wb.save(out)
    _refresh(out)
    return out


def load(path):
    import openpyxl
    wb = openpyxl.load_workbook(path)
    people = []
    for r in wb["Կազմ"].iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        people.append(dict(id=str(r[0]), dep=r[1] or "", pos=r[2] or "", name=r[3] or "", char=r[4] or "",
                           rate=float(r[5] or 0), type=r[6] or "Օրական", phone=r[7] or ""))
    att = wb["Ներկայություն"]
    dates = []
    for c in att[1][7:]:
        if c.value:
            try:
                dates.append(parse_date(c.value))
            except ValueError:
                dates.append(None)
    pres = collections.defaultdict(set)              # date -> {person id}
    for ri, row in enumerate(att.iter_rows(min_row=2, values_only=True)):
        if ri >= len(people):
            break
        for j, d in enumerate(dates):
            v = row[7 + j] if 7 + j < len(row) else None
            if d and v not in (None, "", 0, "0"):
                pres[d].add(people[ri]["id"])
    days = []
    for r in wb["Օրեր"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            days.append(dict(date=parse_date(r[0]), no=r[1], scenes=r[2] or "", pages=float(r[3] or 0)))
    exps = []
    for r in wb["Ծախսեր"].iter_rows(min_row=2, values_only=True):
        if r[0] and r[4]:
            exps.append(dict(date=parse_date(r[0]), cat=r[1] or "Այլ", desc=r[2] or "", payee=r[3] or "",
                             amount=float(r[4]), by=r[5] or "", receipt=r[6] or "", note=r[7] or ""))
    return dict(people=people, dates=dates, pres=pres, days=days, exps=exps)


def _refresh(path):
    """Rewrite the formula columns and the Ամփոփ sheet from the data in the workbook."""
    import openpyxl
    from openpyxl.utils import get_column_letter as L
    Font, PatternFill, Alignment, Border, Side = _styles()
    P = load(path)
    wb = openpyxl.load_workbook(path)
    att, days = wb["Ներկայություն"], wb["Օրեր"]
    n = len(P["people"])
    last = L(7 + max(1, len(P["dates"])))
    for r in range(2, n + 2):
        att[f"F{r}"] = f"=COUNTIF(H{r}:{last}{r},\">0\")"
        att[f"G{r}"] = f'=IF(E{r}="Օրական",D{r}*F{r},IF(E{r}="Ամսական",D{r},D{r}))'
        att[f"G{r}"].number_format = "#,##0"
    for j, d in enumerate(P["dates"]):
        col = L(8 + j)
        att.column_dimensions[col].width = 6.5
        c = att[f"{col}1"]
        c.alignment = Alignment(text_rotation=90, horizontal="center")
    att.row_dimensions[1].height = 70
    for r in range(2, days.max_row + 1):
        d = days[f"A{r}"].value
        if not d:
            continue
        col = None
        for j, dd in enumerate(P["dates"]):
            if dd == parse_date(d):
                col = L(8 + j)
        if col:
            days[f"E{r}"] = f"=COUNTIF(Ներկայություն!{col}2:{col}{n + 1},\">0\")"
            days[f"F{r}"] = (f'=SUMPRODUCT((Ներկայություն!{col}2:{col}{n + 1}>0)*(Ներկայություն!E2:E{n + 1}="Օրական")'
                             f"*Ներկայություն!D2:D{n + 1})")
        days[f"G{r}"] = f"=SUMIFS(Ծախսեր!E:E,Ծախսեր!A:A,A{r})"
        days[f"H{r}"] = f"=F{r}+G{r}"
        for k in "FGH":
            days[f"{k}{r}"].number_format = "#,##0"
        days[f"A{r}"].number_format = "DD.MM.YYYY"
    for r in range(2, wb["Ծախսեր"].max_row + 1):
        wb["Ծախսեր"][f"E{r}"].number_format = "#,##0"
        wb["Ծախսեր"][f"A{r}"].number_format = "DD.MM.YYYY"
    # summary values
    S = compute(P)
    if "Ամփոփ" in wb.sheetnames:
        del wb["Ամփոփ"]
    sm = wb.create_sheet("Ամփոփ")
    sm.append(["Ամփոփ", "", "", "", "", "Թարմացված՝ " + dt.datetime.now().strftime("%d.%m.%Y %H:%M")])
    sm["A1"].font = Font(name="Sylfaen", bold=True, size=14)
    sm.append([])
    sm.append(["Ընդամենը նախագիծ", money(S["total"]), "", "Նկարահանման օրեր", len(S["by_day"]),
               "", "Էջ", S["pages"]])
    sm["B3"].font = Font(name="Sylfaen", bold=True, size=13, color="D90429")
    for title, rows in (("Ըստ շաբաթների", S["by_week"]), ("Ըստ ամիսների", S["by_month"])):
        sm.append([])
        sm.append([title, "Օրեր", "Էջ", "Կազմ", "Այլ ծախսեր", "Ամսական/միանգամյա", "Ընդամենը"])
        sm[f"A{sm.max_row}"].font = Font(name="Sylfaen", bold=True)
        for k, v in rows.items():
            sm.append([v["label"], v["days"], v["pages"], v["people"], v["exp"], v.get("fixed", 0), v["total"]])
    sm.append([])
    sm.append(["Ըստ օրերի", "Նկ. օր", "Էջ", "Կազմ", "Այլ ծախսեր", "", "Ընդամենը"])
    sm[f"A{sm.max_row}"].font = Font(name="Sylfaen", bold=True)
    for d, v in S["by_day"].items():
        sm.append([dstr(d), v["no"], v["pages"], v["people"], v["exp"], "", v["total"]])
    for row in sm.iter_rows(min_row=4):
        for c in row:
            if isinstance(c.value, (int, float)) and c.column > 3:
                c.number_format = "#,##0"
    for col, w in zip("ABCDEFGH", (26, 16, 8, 16, 16, 20, 16, 8)):
        sm.column_dimensions[col].width = w
    wb.move_sheet("Ամփոփ", offset=-(len(wb.sheetnames) - 1))
    wb.save(path)
    return S


def compute(P):
    rate = {p["id"]: p for p in P["people"]}
    by_day = collections.OrderedDict()
    dayinfo = {d["date"]: d for d in P["days"]}
    alld = sorted(set(P["dates"]) | set(dayinfo) | {e["date"] for e in P["exps"]})
    for d in alld:
        ppl = sum(rate[i]["rate"] for i in P["pres"].get(d, ()) if i in rate and rate[i]["type"] == "Օրական")
        exp = sum(e["amount"] for e in P["exps"] if e["date"] == d)
        di = dayinfo.get(d, {})
        by_day[d] = dict(no=di.get("no", ""), pages=di.get("pages", 0), people=ppl, exp=exp, total=ppl + exp,
                         shoot=d in dayinfo, n=len(P["pres"].get(d, ())))
    months = sorted({(d.year, d.month) for d in alld})
    monthly = sum(p["rate"] for p in P["people"] if p["type"] == "Ամսական")
    flat = sum(p["rate"] for p in P["people"] if p["type"] == "Միանգամյա" and p["rate"])

    def agg(keyf, labelf, fixed=None):
        out = collections.OrderedDict()
        for d, v in by_day.items():
            k = keyf(d)
            o = out.setdefault(k, dict(label=labelf(d), days=0, pages=0, people=0, exp=0, total=0, fixed=0))
            o["days"] += v["shoot"]
            o["pages"] += v["pages"]
            o["people"] += v["people"]
            o["exp"] += v["exp"]
            o["total"] += v["total"]
        if fixed:
            for o in out.values():
                o["fixed"] = fixed
                o["total"] += fixed
        return out

    def wk(d):
        mon = d - dt.timedelta(days=d.weekday())
        return f"Շաբաթ {d.isocalendar()[1]} · {mon:%d.%m}–{mon + dt.timedelta(days=6):%d.%m}"
    MONTHS = ["", "Հունվար", "Փետրվար", "Մարտ", "Ապրիլ", "Մայիս", "Հունիս", "Հուլիս", "Օգոստոս", "Սեպտեմբեր",
              "Հոկտեմբեր", "Նոյեմբեր", "Դեկտեմբեր"]
    by_week = agg(lambda d: d.isocalendar()[:2], wk)
    by_month = agg(lambda d: (d.year, d.month), lambda d: f"{MONTHS[d.month]} {d.year}", monthly)
    total = sum(v["total"] for v in by_day.values()) + monthly * len(months) + flat
    by_cat = collections.Counter()
    for e in P["exps"]:
        by_cat[e["cat"]] += e["amount"]
    people_cost = collections.OrderedDict()
    for p in P["people"]:
        dcount = sum(1 for d in P["pres"] if p["id"] in P["pres"][d])
        due = p["rate"] * dcount if p["type"] == "Օրական" else (p["rate"] * len(months) if p["type"] == "Ամսական"
                                                                else p["rate"])
        people_cost[p["id"]] = dict(p, days=dcount, due=due)
    return dict(by_day=by_day, by_week=by_week, by_month=by_month, total=total, monthly=monthly, flat=flat,
                months=len(months), by_cat=by_cat, people=people_cost,
                pages=sum(d["pages"] for d in P["days"]), exp_total=sum(e["amount"] for e in P["exps"]))


# ---------------------------------------------------------------- write operations
def log_day(path, date, no, scenes, pages, characters, crew="all"):
    """Add a shooting day: row in Օրեր + attendance column (actors by character, crew with daily rates)."""
    import openpyxl
    from openpyxl.utils import get_column_letter as L
    wb = openpyxl.load_workbook(path)
    att, days, ppl = wb["Ներկայություն"], wb["Օրեր"], wb["Կազմ"]
    col = None
    for c in att[1][7:]:
        if c.value and parse_date(c.value) == date:
            col = c.column
    if col is None:
        col = max(8, att.max_column + 1)
        att.cell(row=1, column=col, value=dstr(date))
    chars = {str(c).strip().upper() for c in characters}
    missing = set(chars)
    for r in range(2, ppl.max_row + 1):
        pid, dep, ch, typ = (ppl[f"A{r}"].value, ppl[f"B{r}"].value, str(ppl[f"E{r}"].value or "").strip().upper(),
                             ppl[f"G{r}"].value or "Օրական")
        if not pid:
            continue
        here = (ch and ch in chars) or (dep != "Դերասաններ" and crew == "all" and typ == "Օրական")
        att.cell(row=r, column=col, value=1 if here else None)
        missing.discard(ch)
    for r in range(2, days.max_row + 1):
        if days[f"A{r}"].value and parse_date(days[f"A{r}"].value) == date:
            days.delete_rows(r)
            break
    days.append([date, no, scenes, pages])
    rows = list(days.iter_rows(min_row=2, values_only=True))
    rows.sort(key=lambda x: parse_date(x[0]) if x[0] else dt.date.max)
    days.delete_rows(2, days.max_row)
    for x in rows:
        days.append(list(x[:4]))
    wb.save(path)
    _refresh(path)
    return sorted(missing)


def add_expense(path, date, cat, amount, desc="", payee="", by="", receipt="", note=""):
    import openpyxl
    wb = openpyxl.load_workbook(path)
    ex = wb["Ծախսեր"]
    rec = ""
    if receipt and os.path.exists(receipt):
        rdir = os.path.join(os.path.dirname(os.path.abspath(path)), "Չեկեր")
        os.makedirs(rdir, exist_ok=True)
        rec = f"{dstr(date)} {cat} {os.path.basename(receipt)}"
        shutil.copy(receipt, os.path.join(rdir, rec))
        rec = "Չեկեր/" + rec
    ex.append([date, cat, desc, payee, float(amount), by, rec, note])
    wb.save(path)
    _refresh(path)
