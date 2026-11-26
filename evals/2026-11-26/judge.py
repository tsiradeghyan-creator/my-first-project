#!/usr/bin/env python3
"""Blind judging for the with/without eval.

1. For each task, the two outputs get a random order (seeded, reproducible): variant 1 / variant 2.
   The mapping is saved to key.json (do not show it to the human grader before voting).
2. A model judge scores both variants on a 4-criterion rubric without knowing which is which.
3. blind.md is written for Tigran: task + the two FINAL sections, no labels.

Usage: python3 judge.py [--no-judge]
"""
import argparse, hashlib, json, re, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent

RUBRIC = """You are a strict senior reviewer of AI image/video prompts for a film and TV studio.
Two variants answer the same brief. Score each from 1 to 5 on:
1. model_fit: correct for the target model today (real parameters, limits, reference syntax; nothing invented).
2. craft: specific, filmable direction (camera, lens, light, blocking, composition, sound where relevant).
3. brief_fidelity: delivers everything the brief asks, respects given facts and brand, no contradictions.
4. copy_ready: can be pasted and run as is; clear, not bloated.
Then pick the winner ("1", "2" or "tie") and give one sentence why.
Reply with JSON only: {"v1":{"model_fit":n,"craft":n,"brief_fidelity":n,"copy_ready":n},
"v2":{...}, "winner":"1|2|tie", "why":"..."}"""


def final_part(text: str) -> str:
    m = re.search(r"^#{1,3}\s*FINAL\b.*$", text, re.M)
    return text[m.end():].strip() if m else text.strip()


def order(task_id: str) -> list:
    h = int(hashlib.sha256(("maghakian-eval-" + task_id).encode()).hexdigest(), 16)
    return ["with", "without"] if h % 2 == 0 else ["without", "with"]


def judge(task, v1, v2):
    prompt = (f"{RUBRIC}\n\nBRIEF:\n{task['task']}\n\n===== VARIANT 1 =====\n{v1}\n\n"
              f"===== VARIANT 2 =====\n{v2}\n")
    tmp = tempfile.mkdtemp(prefix="judge-")
    p = subprocess.run(["claude", "-p", prompt, "--disable-slash-commands", "--strict-mcp-config",
                        "--disallowedTools", "Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Agent,Skill"],
                       cwd=tmp, capture_output=True, text=True, timeout=900)
    m = re.search(r"\{.*\}", p.stdout, re.S)
    try:
        return json.loads(m.group(0))
    except Exception:
        return {"error": p.stdout[-500:] + p.stderr[-500:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-judge", action="store_true")
    a = ap.parse_args()
    tasks = json.loads((HERE / "tasks.json").read_text())
    key, items = {}, []
    for t in tasks:
        o = order(t["id"])
        recs = {arm: json.loads((HERE / "out" / f"{t['id']}-{arm}.json").read_text()) for arm in o}
        key[t["id"]] = {"1": o[0], "2": o[1]}
        items.append((t, final_part(recs[o[0]]["final"]), final_part(recs[o[1]]["final"])))
    (HERE / "key.json").write_text(json.dumps(key, indent=1))

    lines = ["# Կույր համեմատություն / Blind comparison (2026-11-26)", "",
             "Ամեն առաջադրանքի համար երկու տարբերակ կա։ Մեկը գրվել է քո skill-երով, մյուսը՝ առանց։ "
             "Չգիտես որն է որը։ Կարդա և գրիր ինձ, օրինակ՝ `S1: 2, S2: 1, S3: հավասար …`։", ""]
    for t, v1, v2 in items:
        lines += [f"---", f"## {t['id']}", f"**Առաջադրանք:** {t['task']}", "",
                  "### Տարբերակ 1", "", v1, "", "### Տարբերակ 2", "", v2, ""]
    (HERE / "blind.md").write_text("\n".join(lines))
    if a.no_judge:
        return
    with ThreadPoolExecutor(5) as ex:
        verdicts = list(ex.map(lambda it: judge(*it), items))
    res = {t["id"]: v for (t, _, _), v in zip(items, verdicts)}
    (HERE / "judge.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
