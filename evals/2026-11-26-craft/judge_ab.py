#!/usr/bin/env python3
"""Blind pairwise judge for run_ab.py outputs (old vs new skills). Same rubric as evals/2026-11-26/judge.py,
so the judge is not primed with the new prompt-craft vocabulary.
Usage: python3 judge_ab.py
"""
import hashlib, json, sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "2026-11-26"))
from judge import final_part, judge  # noqa: E402

CRIT = ["model_fit", "craft", "brief_fidelity", "copy_ready"]


def order(rid):
    h = int(hashlib.sha256(("craft-ab-" + rid).encode()).hexdigest(), 16)
    return ["old", "new"] if h % 2 == 0 else ["new", "old"]


def main():
    tasks = {t["id"]: t for t in json.loads((HERE / "tasks.json").read_text())}
    ids = sorted({p.name.rsplit("-", 1)[0] for p in (HERE / "out").glob("*-new.json")})
    items = []
    for rid in ids:
        o = order(rid)
        v = [final_part(json.loads((HERE / "out" / f"{rid}-{arm}.json").read_text())["final"]) for arm in o]
        items.append((rid, rid.split("-r")[0], o, v))
    with ThreadPoolExecutor(5) as ex:
        verdicts = list(ex.map(lambda it: judge(tasks[it[1]], it[3][0], it[3][1]), items))
    res, tally = {}, defaultdict(lambda: {"new": 0, "old": 0, "tie": 0, "score": {"new": [], "old": []}})
    for (rid, base, o, _), v in zip(items, verdicts):
        res[rid] = {"order": o, **v}
        if "error" in v:
            print(rid, "judge error"); continue
        w = v["winner"]
        tally[base]["tie" if w == "tie" else o[int(w) - 1]] += 1
        for slot, arm in zip(("v1", "v2"), o):
            tally[base]["score"][arm].append(sum(v[slot][c] for c in CRIT))
    (HERE / "judge.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    tot = {"new": 0, "old": 0, "tie": 0}
    for base, t in sorted(tally.items()):
        m = {k: round(sum(x) / len(x), 1) if x else None for k, x in t["score"].items()}
        for k in tot: tot[k] += t[k]
        print(f"{base}: new {t['new']} / old {t['old']} / tie {t['tie']} | mean new {m['new']} vs old {m['old']}")
    print("TOTAL", tot)


if __name__ == "__main__":
    main()
