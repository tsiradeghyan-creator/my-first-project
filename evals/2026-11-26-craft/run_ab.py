#!/usr/bin/env python3
"""A/B of two skill versions (git refs) on the same tasks. Arms: old, new.
Each arm gets CLAUDE.md + .claude/skills + .claude/agents from its git ref, plus business.md and memory/.
Usage: python3 run_ab.py --old <ref> --new <ref> [--reps 2] [--jobs 6]
"""
import argparse, io, json, shutil, subprocess, tarfile, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE = Path(__file__).resolve().parent
import os
TASKS = os.environ.get("AB_TASKS", "tasks.json")
OUT = os.environ.get("AB_OUT", "out")
REPO = HERE.parents[1]
SUFFIX = ("\n\nThis is a non-interactive run: if you would normally ask a question, state your assumption and continue. "
          "End your reply with the final deliverable (the copy-ready prompt(s) and settings) under a heading '## FINAL'.")

def extract(ref, dst):
    data = subprocess.run(["git", "-C", str(REPO), "archive", ref, "CLAUDE.md", ".claude/skills", ".claude/agents",
                           "maghakian-roast-room/business.md", "memory"], capture_output=True, check=True).stdout
    tarfile.open(fileobj=io.BytesIO(data)).extractall(dst)

def run(task, arm, ref):
    out = HERE / OUT / f"{task['id']}-{arm}.json"
    if out.exists():
        return
    tmp = Path(tempfile.mkdtemp(prefix=f"ab-{task['id']}-{arm}-"))
    extract(ref, tmp)
    cmd = ["claude", "-p", task["task"] + SUFFIX, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--allowedTools", "Read,Write,Edit,Glob,Grep,Skill",
           "--disallowedTools", "WebSearch,WebFetch,Bash,Agent", "--strict-mcp-config"]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=1500); so = p.stdout
    except subprocess.TimeoutExpired as e:
        so = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    final, skills, cost = "", [], None
    for line in so.splitlines():
        try: ev = json.loads(line)
        except ValueError: continue
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use" and c.get("name") == "Skill":
                    skills.append(c.get("input", {}).get("skill"))
        if ev.get("type") == "result":
            final, cost = ev.get("result", "") or "", ev.get("total_cost_usd")
    out.write_text(json.dumps({"id": task["id"], "arm": arm, "skills_used": skills, "seconds": round(time.time()-t0),
                               "cost_usd": cost, "final": final}, ensure_ascii=False, indent=1))
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"done {task['id']}-{arm} {round(time.time()-t0)}s {skills} {'OK' if final else 'NO OUTPUT'}", flush=True)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--old", required=True); ap.add_argument("--new", required=True)
    ap.add_argument("--reps", type=int, default=2); ap.add_argument("--jobs", type=int, default=6); a = ap.parse_args()
    (HERE / OUT).mkdir(exist_ok=True)
    tasks = json.loads((HERE / TASKS).read_text())
    tasks = [dict(t, id=f"{t['id']}-r{k}") for t in tasks for k in range(1, a.reps + 1)]
    jobs = [(t, arm, ref) for t in tasks for arm, ref in (("old", a.old), ("new", a.new))]
    with ThreadPoolExecutor(a.jobs) as ex: list(ex.map(lambda j: run(*j), jobs))

if __name__ == "__main__":
    main()
