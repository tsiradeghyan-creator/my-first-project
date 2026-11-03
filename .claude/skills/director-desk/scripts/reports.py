#!/usr/bin/env python3
"""Branded reports from project.xlsx (+ master.xlsx): finance, progress, payroll.

Design rules (one place, used by every report):
  * type scale 1.25 (major third) on a 9 pt base: 9 · 11.25 · 14 · 17.5 · 22 · 27.5 · 34 pt
  * spacing on a 4 pt grid; A4 margins 24/19/20 mm
  * one red: only the main figure of the page and overruns; everything else black/graphite/grey
  * numbers: tabular, right-aligned, thin-space thousands, currency after the number
  * hero row first (the answer), then the breakdown, then the detail tables
"""
import collections
import datetime as dt
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack_design as dz  # noqa: E402
import production as pr  # noqa: E402

E = dz.esc
M = pr.money

CSS = """<style>
.hero{display:grid;grid-template-columns:1.618fr 1fr 1fr 1fr;gap:0 16pt;margin:4pt 0 18pt;align-items:end}
.hero .k{border-top:1.6pt solid #000;padding-top:8pt}
.hero .k .v{font-family:var(--serif);font-weight:700;font-size:22pt;line-height:1.05;color:#000;
font-variant-numeric:tabular-nums;white-space:nowrap}
.hero .k.main{border-top-color:var(--red)}
.hero .k.main .v{font-size:34pt;color:var(--red)}
.hero .k .l{font-size:6.6pt;letter-spacing:.16em;text-transform:uppercase;color:var(--grey);margin-top:6pt}
.hero .k .s{font-size:8pt;color:var(--grey);margin-top:2pt}
table.ledger{font-size:8.4pt}
table.ledger td.num,table.ledger th.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
table.ledger tr.sub td{font-weight:650;color:#000;border-bottom:.6pt solid #000;padding-top:9pt}
table.ledger tr.tot td{font-size:9.5pt;font-weight:700;color:#000;border-top:1.2pt solid #000;border-bottom:0;padding-top:7pt}
table.ledger tr.tot td.num{color:var(--red)}
.bars .b{display:grid;grid-template-columns:120pt 1fr 78pt;gap:10pt;align-items:center;padding:3.5pt 0;
border-bottom:.6pt solid var(--line);font-size:8.6pt}
.bars .t{height:7pt;background:var(--soft);position:relative}
.bars .t i{position:absolute;left:0;top:0;bottom:0;background:#111}
.bars .b.first .t i{background:var(--red)}
.bars .v{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.progress{height:10pt;background:var(--soft);margin:2pt 0 4pt;position:relative}
.progress i{position:absolute;left:0;top:0;bottom:0;background:#000}
.lede{font-family:var(--serif);font-size:11.25pt;line-height:1.5;color:#000;margin:0 0 12pt;max-width:150mm}
.meta{font-size:7.4pt;color:var(--grey);margin-top:-2pt}
</style>"""


def hero(items):
    """items: (value, label, sub) — first one is the main answer (red)."""
    return '<div class="hero">' + "".join(
        f'<div class="k{" main" if i == 0 else ""}"><div class="v">{v}</div><div class="l">{E(l)}</div>'
        f'{"<div class=s>" + E(s) + "</div>" if s else ""}</div>' for i, (v, l, s) in enumerate(items)) + "</div>"


def bars(items, fmt=None):
    fmt = fmt or M
    mx = max([v for _, v in items] or [1]) or 1
    return '<div class="bars">' + "".join(
        f'<div class="b{" first" if i == 0 else ""}"><span>{E(k)}</span><span class="t"><i style="width:{v / mx * 100:.1f}%">'
        f'</i></span><span class="v">{fmt(v)}</span></div>' for i, (k, v) in enumerate(items)) + "</div>"


def period_days(S, period, date):
    days = list(S["by_day"].keys())
    if period == "all" or not date:
        return days, "Ամբողջ նախագիծ"
    if period == "day":
        return [d for d in days if d == date], f"Օր · {pr.dstr(date)}"
    if period == "week":
        w = date.isocalendar()[:2]
        mon = date - dt.timedelta(days=date.weekday())
        return ([d for d in days if d.isocalendar()[:2] == w],
                f"Շաբաթ {w[1]} · {mon:%d.%m}–{mon + dt.timedelta(days=6):%d.%m.%Y}")
    if period == "month":
        lab = next(iter(v["label"] for k, v in S["by_month"].items() if k == (date.year, date.month)), "")
        return [d for d in days if (d.year, d.month) == (date.year, date.month)], lab or f"{date:%m.%Y}"
    raise ValueError(period)


def render(body, out, who, title):
    with dz.Renderer() as RN:
        RN.pdf(dz.page(CSS + body, "doc", title, who, title), out,
               html_dir=os.path.join(os.path.dirname(os.path.abspath(out)), "_html"))
    return out


def mast(doc, title, sub=""):
    return (f'<header class="mast" style="padding-bottom:10pt"><div class="doc">{E(doc)}</div>'
            f'<h1 style="font-size:27.5pt">{E(title)}</h1>{"<div class=fmt>" + E(sub) + "</div>" if sub else ""}</header>')


# ---------------------------------------------------------------- finance
def finance(project, out, period="all", date=None, who="ԳԼԽԱՎՈՐ ՊՐՈԴՅՈՒՍԵՐ · EXECUTIVE PRODUCER", title="",
            purpose=""):
    P = pr.load(project)
    S = pr.compute(P)
    days, label = period_days(S, period, date)
    sel = [S["by_day"][d] for d in days]
    shoot = [d for d in days if S["by_day"][d]["shoot"]]
    people = sum(v["people"] for v in sel)
    exp = sum(v["exp"] for v in sel)
    fixed = 0
    if period == "month":
        fixed = S["monthly"]
    elif period == "all":
        fixed = S["monthly"] * S["months"] + S["flat"]
    total = people + exp + fixed
    pages = sum(S["by_day"][d]["pages"] for d in shoot)
    b = mast("Ծախսերի հաշվետվություն", label, title)
    if purpose:
        b += f'<p class="lede">{E(purpose)}</p>'
    b += hero([(M(total), "Ընդամենը ծախս", label),
               (len(shoot), "Նկարահանման օր", ""),
               (M(total / len(shoot)) if shoot else "—", "Միջինը օրական", ""),
               (M(total / pages) if pages else "—", "Մեկ էջի արժեքը", f"{pages:g} էջ")])
    # structure: people by department + expense categories
    dep = collections.Counter()
    for d in days:
        for pid in P["pres"].get(d, ()):
            p = S["people"].get(pid)
            if p and p["type"] == "Օրական":
                dep[p["dep"]] += p["rate"]
    if fixed:
        dep["Ամսական / միանգամյա"] += fixed
    cat = collections.Counter()
    for e in P["exps"]:
        if e["date"] in days or period == "all":
            cat[e["cat"]] += e["amount"]
    b += dz.h2("01", "Ինչի վրա է գնացել")
    struct = sorted(([f"Կազմ · {k}", v] for k, v in dep.items() if v), key=lambda x: -x[1]) + \
        sorted(([k, v] for k, v in cat.items() if v), key=lambda x: -x[1])
    struct.sort(key=lambda x: -x[1])
    b += bars(struct) if struct else '<p class="note">Դրույքներ և ծախսեր դեռ լրացված չեն։</p>'
    # by day
    b += dz.h2("02", "Ըստ օրերի")
    rows = "".join(f'<tr><td>{pr.dstr(d)}</td><td class="num">{S["by_day"][d]["no"] or ""}</td>'
                   f'<td class="num">{S["by_day"][d]["pages"]:g}</td><td class="num">{S["by_day"][d]["n"]}</td>'
                   f'<td class="num">{M(S["by_day"][d]["people"])}</td><td class="num">{M(S["by_day"][d]["exp"])}</td>'
                   f'<td class="num"><b>{M(S["by_day"][d]["total"])}</b></td></tr>' for d in days)
    rows += (f'<tr class="tot"><td>Ընդամենը</td><td></td><td class="num">{pages:g}</td><td></td>'
             f'<td class="num">{M(people)}</td><td class="num">{M(exp)}</td><td class="num">{M(people + exp)}</td></tr>')
    if fixed:
        rows += f'<tr><td colspan="6">+ ամսական / միանգամյա վճարներ</td><td class="num">{M(fixed)}</td></tr>'
    b += ('<table class="ledger"><thead><tr><th>Ամսաթիվ</th><th class="num">Նկ. օր</th><th class="num">Էջ</th>'
          '<th class="num">Մարդ</th><th class="num">Կազմ</th><th class="num">Այլ ծախսեր</th>'
          f'<th class="num">Ընդամենը</th></tr></thead><tbody>{rows}</tbody></table>')
    # expenses ledger
    ex = [e for e in P["exps"] if e["date"] in days or period == "all"]
    if ex:
        b += dz.h2("03", "Ծախսերի մատյան")
        rows = "".join(f'<tr><td>{pr.dstr(e["date"])}</td><td>{E(e["cat"])}</td><td>{E(e["desc"])}</td>'
                       f'<td>{E(e["payee"])}</td><td>{E(e["by"])}</td><td class="num">{M(e["amount"])}</td>'
                       f'<td class="note">{"✓ չեկ" if e["receipt"] else ""}</td></tr>' for e in sorted(ex, key=lambda e: e["date"]))
        rows += f'<tr class="tot"><td colspan="5">Ընդամենը</td><td class="num">{M(sum(e["amount"] for e in ex))}</td><td></td></tr>'
        b += ('<table class="ledger"><thead><tr><th>Ամսաթիվ</th><th>Կատեգորիա</th><th>Նկարագրություն</th>'
              '<th>Ում / որտեղ</th><th>Վճարող</th><th class="num">Գումար</th><th></th></tr></thead>'
              f'<tbody>{rows}</tbody></table>')
    b += payroll_table(P, S, days, "04")
    return render(b, out, who, f"Ծախսեր · {label}")


def payroll_table(P, S, days, no):
    rows, total, last = "", 0, None
    people = sorted(S["people"].values(), key=lambda p: (p["dep"], p["pos"]))
    for p in people:
        n = sum(1 for d in days if p["id"] in P["pres"].get(d, ()))
        if p["type"] == "Օրական":
            due = n * p["rate"]
        else:
            continue
        if not n:
            continue
        if p["dep"] != last:
            rows += f'<tr class="sub"><td colspan="5">{E(p["dep"])}</td></tr>'
            last = p["dep"]
        who = p["name"] or "—"
        role = p["char"] if p["dep"] == "Դերասաններ" else p["pos"]
        rows += (f'<tr><td>{E(role)}</td><td>{E(who)}</td><td class="num">{n}</td>'
                 f'<td class="num">{M(p["rate"]) if p["rate"] else "—"}</td><td class="num">{M(due)}</td></tr>')
        total += due
    if not rows:
        return ""
    rows += f'<tr class="tot"><td colspan="4">Ընդամենը կազմ</td><td class="num">{M(total)}</td></tr>'
    return (dz.h2(no, "Կազմ. օրեր և վճարներ") + '<table class="ledger"><thead><tr><th>Պաշտոն / դեր</th><th>Անուն</th>'
            '<th class="num">Օր</th><th class="num">Դրույք</th><th class="num">Վճարվելիք</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>')


def payroll(project, out, period="all", date=None, who="ՀԱՇՎԱՊԱՀ · ACCOUNTANT", title=""):
    P = pr.load(project)
    S = pr.compute(P)
    days, label = period_days(S, period, date)
    tot = sum(sum(1 for d in days if p["id"] in P["pres"].get(d, ())) * p["rate"]
              for p in S["people"].values() if p["type"] == "Օրական")
    fixed = [p for p in S["people"].values() if p["type"] != "Օրական" and p["rate"]]
    b = mast("Վճարների ցուցակ", label, title)
    b += hero([(M(tot), "Օրական վճարներ", label), (sum(1 for d in days if S["by_day"][d]["shoot"]), "Նկարահանման օր", ""),
               (len({i for d in days for i in P["pres"].get(d, ())}), "Մարդ", ""), (len(fixed), "Ամսական / միանգամյա", "")])
    b += payroll_table(P, S, days, "01")
    if fixed:
        rows = "".join(f'<tr><td>{E(p["pos"])}</td><td>{E(p["name"] or "—")}</td><td>{E(p["type"])}</td>'
                       f'<td class="num">{M(p["rate"])}</td></tr>' for p in fixed)
        b += (dz.h2("02", "Ամսական և միանգամյա") + '<table class="ledger"><thead><tr><th>Պաշտոն</th><th>Անուն</th>'
              f'<th>Տեսակ</th><th class="num">Գումար</th></tr></thead><tbody>{rows}</tbody></table>')
    return render(b, out, who, f"Վճարներ · {label}")


# ---------------------------------------------------------------- progress
def progress(project, master, out, who="ԳԼԽԱՎՈՐ ՊՐՈԴՅՈՒՍԵՐ · EXECUTIVE PRODUCER", title="", purpose=""):
    import plan
    rows = plan.read_master(master)
    P = pr.load(project) if project and os.path.exists(project) else dict(days=[], pres={}, people=[])
    logged = {plan.norm_id(x) for d in P["days"] for x in re.split(r",\s*", str(d["scenes"])) if x}
    for r in rows:
        r["done"] = r["shot"] or plan.norm_id(r["id"]) in logged
    tot = sum(r["pages"] or 0 for r in rows)
    done = sum(r["pages"] or 0 for r in rows if r["done"])
    ndays = len(P["days"])
    per_day = (sum(d["pages"] for d in P["days"]) / ndays) if ndays else 0
    left = tot - done
    pct = done / tot * 100 if tot else 0
    b = mast("Արտադրության ընթացք", title or "Սեզոն", dt.date.today().strftime("%d.%m.%Y"))
    if purpose:
        b += f'<p class="lede">{E(purpose)}</p>'
    b += hero([(f"{pct:.0f}%", "Նկարված է", f"{done:g} / {tot:g} էջ"),
               (f"{left:g}", "Մնացել է էջ", f"{sum(1 for r in rows if not r['done'])} տեսարան"),
               (f"{per_day:.1f}" if per_day else "—", "Էջ օրական (միջին)", f"{ndays} գրանցված օր"),
               (f"≈ {left / per_day:.0f}" if per_day else "—", "Մնացած օրեր", "ըստ միջին տեմպի")])
    b += f'<div class="progress"><i style="width:{pct:.1f}%"></i></div>'
    # by episode
    eps = collections.OrderedDict()
    for r in sorted(rows, key=lambda r: (int(re.sub(r"\D", "", str(r["id"]).split("/")[0]) or 0))):
        e = eps.setdefault(str(r["id"]).split("/")[0], [0, 0, 0, 0])
        e[0] += 1
        e[1] += r["pages"] or 0
        if r["done"]:
            e[2] += 1
            e[3] += r["pages"] or 0
    trs = "".join(f'<tr><td><b>Սերիա {E(k)}</b></td><td class="num">{v[0]}</td><td class="num">{v[1]:g}</td>'
                  f'<td class="num">{v[3]:g}</td><td class="num">{v[1] - v[3]:g}</td>'
                  f'<td style="width:110pt"><div class="progress" style="margin:0"><i style="width:{(v[3] / v[1] * 100) if v[1] else 0:.0f}%"></i></div></td></tr>'
                  for k, v in eps.items())
    b += dz.h2("01", "Ըստ սերիաների") + (
        '<table class="ledger"><thead><tr><th>Սերիա</th><th class="num">Տեսարան</th><th class="num">Էջ</th>'
        '<th class="num">Նկարված</th><th class="num">Մնացել</th><th></th></tr></thead>'
        f'<tbody>{trs}</tbody></table>')
    # sets left
    sets = collections.Counter()
    for r in rows:
        if not r["done"]:
            sets[r["set"]] += r["pages"] or 0
    b += dz.h2("02", "Մնացած օբյեկտներ (էջ)") + bars([(k, v) for k, v in sets.most_common(12)], fmt=lambda v: f"{v:g} էջ")
    # people: days worked
    if P["people"]:
        S = pr.compute(P)
        ppl = [p for p in S["people"].values() if p["days"]]
        ppl.sort(key=lambda p: -p["days"])
        if ppl:
            trs = "".join(f'<tr><td>{E(p["char"] if p["dep"] == "Դերասաններ" else p["pos"])}</td>'
                          f'<td>{E(p["name"] or "—")}</td><td class="num"><b>{p["days"]}</b></td></tr>' for p in ppl)
            b += dz.h2("03", "Ով քանի օր է աշխատել") + (
                '<table class="ledger"><thead><tr><th>Պաշտոն / դեր</th><th>Անուն</th><th class="num">Օր</th></tr>'
                f'</thead><tbody>{trs}</tbody></table>')
    return render(b, out, who, "Արտադրության ընթացք")
