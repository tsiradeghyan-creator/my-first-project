#!/usr/bin/env python3
"""Season breakdown: several episode .fountain files -> one line-producer overview.

- per episode: pages (≈ minutes), scenes, sets, speaking characters
- sets across the season: in which episodes, total pages → plan shooting blocks by set
- characters × episodes matrix (scenes per episode) → actor days and contracts
- typo / duplicate warnings across the whole season
Writes <out>.md and <out>.csv (scene-level, all episodes, for Sheets).

Usage: python3 season.py ep01.fountain ep02.fountain ... --out season_breakdown [--paper letter|a4]
"""
import argparse
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import screenplay as sp  # noqa: E402


def ep_label(path, title):
    credit = " ".join(title.get("credit", []))
    m = re.search(r"(\d+)", credit) or re.search(r"(\d+)", os.path.basename(path))
    return m.group(1) if m else os.path.basename(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", default="season_breakdown")
    ap.add_argument("--paper", choices=sp.PAPER, default="letter")
    a = ap.parse_args()
    lpp = int(round((sp.PAPER[a.paper][1] - 2.0) * 6))

    eps, all_scenes, series = [], [], ""
    for f in sorted(a.files):
        with open(f, encoding="utf-8-sig") as fh:
            title, blocks = sp.parse(fh.read())
        series = series or " ".join(title.get("title", []))
        pages = sp.paginate(blocks, lpp, sp.LABELS["hy"])
        scenes = sp.breakdown(blocks, pages, lpp)
        ep = ep_label(f, title)
        for s in scenes:
            s["episode"] = ep
        eps.append({"ep": ep, "pages": len(pages), "scenes": scenes})
        all_scenes += scenes

    def ser(e):
        return sp.eighths_str(e)

    L = [f"# {series or 'Season'}: season breakdown", "",
         f"Episodes: **{len(eps)}** · pages: **{sum(e['pages'] for e in eps)}** (≈ minutes) · "
         f"scenes: **{len(all_scenes)}**", "",
         "## Episodes", "", "| Ep | Pages ≈ min | Scenes | Sets | Speaking characters | Product placement |", "|---|---|---|---|---|---|"]
    for e in eps:
        sets = {sp.split_set(s["location"])[0] for s in e["scenes"]}
        spk = {c for s in e["scenes"] for c in s["speaking"]}
        pl = [s["number"] for s in e["scenes"] if s.get("placement")]
        L.append(f"| {e['ep']} | {e['pages']} | {len(e['scenes'])} | {len(sets)} | {len(spk)} | "
                 f"{('sc. ' + ', '.join(pl)) if pl else ''} |")

    # sets across season
    sets = {}
    for s in all_scenes:
        main, room = sp.split_set(s["location"])
        d = sets.setdefault(main, {"eighths": 0, "scenes": 0, "eps": [], "rooms": set(), "time": set()})
        d["eighths"] += s["eighths"]
        d["scenes"] += 1
        if s["episode"] not in d["eps"]:
            d["eps"].append(s["episode"])
        if room:
            d["rooms"].add(room)
        if s["time"]:
            d["time"].add(s["time"])
    L += ["", "## Sets across the season (shoot each set as one block)", "",
          "| Set | Pages | Scenes | Episodes | Time | Rooms |", "|---|---|---|---|---|---|"]
    for k in sorted(sets, key=lambda x: (-sets[x]["eighths"], x)):
        d = sets[k]
        L.append(f"| {k} | {ser(d['eighths'])} | {d['scenes']} | {', '.join(d['eps'])} | "
                 f"{', '.join(sorted(d['time']))} | {' · '.join(sorted(d['rooms']))} |")

    # characters x episodes
    chars = {}
    for s in all_scenes:
        for c in s["characters"]:
            row = chars.setdefault(c, {})
            row[s["episode"]] = row.get(s["episode"], 0) + 1
    ep_ids = [e["ep"] for e in eps]
    L += ["", "## Characters × episodes (scenes per episode)", "",
          "| Character | " + " | ".join(ep_ids) + " | Total |", "|---|" + "---|" * (len(ep_ids) + 1)]
    for c in sorted(chars, key=lambda x: (-sum(chars[x].values()), x)):
        r = chars[c]
        L.append(f"| {c} | " + " | ".join(str(r.get(e, "")) for e in ep_ids) + f" | {sum(r.values())} |")

    L += sp.qa_warnings(list(chars), list({s["location"] for s in all_scenes}))
    with open(a.out + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    with open(a.out + ".csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["episode", "scene", "set", "location", "time", "page", "eighths", "length", "characters", "placement"])
        for s in all_scenes:
            w.writerow([s["episode"], s["number"], sp.split_set(s["location"])[0], s["location"],
                        s["time"], s["page"], s["eighths"], s["length"], "; ".join(s["characters"]),
                        "yes" if s.get("placement") else ""])
    print("wrote", a.out + ".md", a.out + ".csv")


if __name__ == "__main__":
    sys.exit(main())
