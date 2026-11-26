#!/usr/bin/env python3
"""Compile the BAB Room's data files from the Roast Room (roster, agents, brains, seats.md, business.md).

Run after any seat is rebuilt, then republish the artifact's data files:
  python3 maghakian-roast-room/bab-room/build_data.py
Writes bab-room/data/seats.json and bab-room/data/context.json.
"""
import json, re
from pathlib import Path

ROOM = Path(__file__).resolve().parents[1]
SK = ROOM / ".claude/skills/roast-room"
BAB = ["rhimes", "villeneuve", "blum", "deakins", "vermette", "murch", "levi", "mungiu",
       "bloys", "quinn", "bajaria", "tigran", "lineprod"]
INDUSTRY = ["buyer", "showrunner", "copro", "publisher"]
FILES = ["_hot", "frameworks", "positions", "principles", "stories", "voice", "books"]


def body(md):
    return re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S).strip()


def main():
    roster = json.loads((SK / "roster.json").read_text())
    seats = []
    for s in roster["seats"]:
        agent = ROOM / ".claude/agents" / f"council-{s['key']}.md"
        bdir = SK / "brains" / s["slug"]
        brain = {f: (bdir / f"{f}.md").read_text() for f in FILES if (bdir / f"{f}.md").exists()}
        group = "bab" if s["key"] in BAB else "industry" if s["key"] in INDUSTRY else "other"
        seats.append({k: s.get(k, "") for k in ("key", "name", "short", "initials", "pillar", "question",
                                                 "dimension", "color")} |
                     {"group": group, "agent": body(agent.read_text()) if agent.exists() else "",
                      "words": sum(len(t.split()) for t in brain.values()), "brain": brain})
    order = {k: i for i, k in enumerate(BAB + INDUSTRY)}
    seats.sort(key=lambda s: (order.get(s["key"], 99), s["name"]))
    out = Path(__file__).resolve().parent / "data"
    out.mkdir(exist_ok=True)
    (out / "seats.json").write_text(json.dumps(seats, ensure_ascii=False))
    ctx = {"business": (ROOM / "business.md").read_text(),
           "seats_md": (SK / "references/seats.md").read_text(),
           "default_board": ["rhimes", "villeneuve", "blum", "murch", "bloys", "tigran"]}
    (out / "context.json").write_text(json.dumps(ctx, ensure_ascii=False))
    print(f"{len(seats)} seats, {sum(1 for s in seats if s['group']=='bab')} BAB;",
          f"seats.json {(out/'seats.json').stat().st_size//1024} KB")


if __name__ == "__main__":
    main()
