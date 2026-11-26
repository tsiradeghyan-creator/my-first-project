#!/usr/bin/env python3
"""Judge repeated runs (from run.py --reps N --out <dir>) blind, and tally per task.

Usage: python3 judge2.py --out out-v2
Writes <out>/judge.json and prints wins and mean scores per base task.
"""
import argparse, json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from judge import HERE, final_part, judge, order

CRIT = ["model_fit", "craft", "brief_fidelity", "copy_ready"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = HERE / a.out
    tasks = {t["id"]: t for t in json.loads((HERE / "tasks.json").read_text())}
    ids = sorted({p.name.rsplit("-", 1)[0] for p in d.glob("*-with.json")})
    items = []
    for rid in ids:
        base = rid.split("-r")[0]
        o = order(rid)
        v = [final_part(json.loads((d / f"{rid}-{arm}.json").read_text())["final"]) for arm in o]
        items.append((rid, base, o, v))
    with ThreadPoolExecutor(5) as ex:
        verdicts = list(ex.map(lambda it: judge(tasks[it[1]], it[3][0], it[3][1]), items))
    res, tally = {}, defaultdict(lambda: {"with": 0, "without": 0, "tie": 0,
                                          "score": {"with": [], "without": []}})
    for (rid, base, o, _), v in zip(items, verdicts):
        res[rid] = {"order": o, **v}
        if "error" in v:
            print(rid, "judge error")
            continue
        w = v["winner"]
        tally[base]["tie" if w == "tie" else o[int(w) - 1]] += 1
        for slot, arm in zip(("v1", "v2"), o):
            tally[base]["score"][arm].append(sum(v[slot][c] for c in CRIT))
    (d / "judge.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    for base, t in tally.items():
        mean = {k: round(sum(x) / len(x), 1) if x else None for k, x in t["score"].items()}
        print(f"{base}: with wins {t['with']}, without wins {t['without']}, ties {t['tie']} | "
              f"mean total with {mean['with']} vs without {mean['without']} (max 20)")


if __name__ == "__main__":
    main()
