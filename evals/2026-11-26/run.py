#!/usr/bin/env python3
"""With/without eval of Tigran's prompt skills.

WITH    = a copy of the workspace (CLAUDE.md, .claude/ skills + agents, business.md, memory/),
          i.e. the real setup a cloud session gets.
WITHOUT = an empty folder, skills and commands disabled (--disable-slash-commands), no CLAUDE.md.
Both arms: same default model, same task text, no web, no MCP servers, non-interactive.

Usage: python3 run.py [--only S1,F2] [--jobs 6]
Writes raw/<id>-<arm>.jsonl and out/<id>-<arm>.json (final text, skills used, cost, time).
"""
import argparse, json, shutil, subprocess, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SUFFIX = ("\n\nThis is a non-interactive run: if you would normally ask a question, state your "
          "assumption and continue. End your reply with the final deliverable (the copy-ready "
          "prompt(s) and settings) under a heading '## FINAL'.")
TOOLS = "Read,Write,Edit,Glob,Grep,Skill"


def workspace(dst: Path) -> None:
    shutil.copy2(REPO / "CLAUDE.md", dst / "CLAUDE.md")
    ign = shutil.ignore_patterns("*.log", "__pycache__", ".github", "evals")
    shutil.copytree(REPO / ".claude/skills", dst / ".claude/skills", ignore=ign)
    shutil.copytree(REPO / ".claude/agents", dst / ".claude/agents")
    (dst / "maghakian-roast-room").mkdir()
    shutil.copy2(REPO / "maghakian-roast-room/business.md", dst / "maghakian-roast-room/business.md")
    shutil.copytree(REPO / "memory", dst / "memory")


def run(task: dict, arm: str) -> dict:
    out = HERE / "out" / f"{task['id']}-{arm}.json"
    if out.exists():
        return json.loads(out.read_text())
    tmp = Path(tempfile.mkdtemp(prefix=f"ev-{task['id']}-{arm}-"))
    cmd = ["claude", "-p", task["task"] + SUFFIX, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--allowedTools", TOOLS,
           "--disallowedTools", "WebSearch,WebFetch,Bash,Agent", "--strict-mcp-config"]
    if arm == "with":
        workspace(tmp)
    else:
        cmd.append("--disable-slash-commands")
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=1200)
        stdout, err = p.stdout, p.stderr[-2000:]
    except subprocess.TimeoutExpired as e:
        stdout, err = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "TIMEOUT"
    (HERE / "raw" / f"{task['id']}-{arm}.jsonl").write_text(stdout)
    final, skills, cost = "", [], None
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use" and c.get("name") == "Skill":
                    skills.append(c.get("input", {}).get("skill") or c.get("input", {}).get("command"))
        if ev.get("type") == "result":
            final = ev.get("result", "") or ""
            cost = ev.get("total_cost_usd")
    rec = {"id": task["id"], "arm": arm, "skills_used": skills, "seconds": round(time.time() - t0),
           "cost_usd": cost, "error": err if not final else "", "final": final}
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=1))
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"done {task['id']}-{arm} {rec['seconds']}s skills={skills} {'OK' if final else 'NO OUTPUT'}", flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    (HERE / "raw").mkdir(exist_ok=True)
    (HERE / "out").mkdir(exist_ok=True)
    tasks = json.loads((HERE / "tasks.json").read_text())
    if a.only:
        keep = set(a.only.split(","))
        tasks = [t for t in tasks if t["id"] in keep]
    jobs = [(t, arm) for t in tasks for arm in ("with", "without")]
    with ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(lambda j: run(*j), jobs))


if __name__ == "__main__":
    main()
