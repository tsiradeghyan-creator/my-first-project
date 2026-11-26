#!/usr/bin/env python3
"""
Consolidate Memory — Nightly Claude conversation log processor.
Reads ~/.claude/projects/**/*.jsonl, extracts key facts,
and updates ~/.memory/*.md files.

Two extraction paths:
  default      — local regex pass that keeps whole sentences only (offline).
  --summarize  — asks the local `claude -p` CLI to summarise the same messages;
                 falls back to the regex pass if the CLI is missing or fails.
"""

import json
import os
import shutil
import subprocess
import sys
import re
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
HOME = Path.home()
MEMORY_DIR = HOME / ".memory"
RECENT_MEM = MEMORY_DIR / "recent-memory.md"
LONG_MEM = MEMORY_DIR / "long-term-memory.md"
PROJECT_MEM = MEMORY_DIR / "project-memory.md"
LOG_FILE = MEMORY_DIR / "consolidate.log"
PROJECTS_DIR = HOME / ".claude" / "projects"

# ── Extraction Patterns ───────────────────────────────────────────────────────
DECISION_PATTERNS = [
    r"(?:decided|going with|chose|will use|from now on|always|never)\s+(.{20,120})",
    r"(?:don't|do not)\s+(?:use|write|add|create)\s+(.{10,80})",
    r"(?:make sure|remember|note that)\s+(.{10,100})",
]

COMPLETION_PATTERNS = [
    r"(?:created|added|completed|finished|done|built|wrote|generated)\s+(.{10,100})",
    r"(?:successfully|✅)\s+(.{5,80})",
]

PREFERENCE_PATTERNS = [
    r"(?:prefer|want|always|never|should)\s+(.{10,100})",
    r"(?:instead of|not like|don't do)\s+(.{10,80})",
]

PROJECT_KEYWORDS = [
    "maghakian", "ani maghakyan", "84-ի", "screenwriter",
    "wikipedia", "instagram", "linkedin", "skill", "memory",
    "seo", "caption", "content plan", "press release",
]


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="Consolidate Claude memory")
    parser.add_argument("--hours", type=int, default=24,
                        help="Look back N hours (default: 24)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print output without writing files")
    parser.add_argument("--summarize", action="store_true",
                        help="Summarise with `claude -p` (falls back to the regex pass)")
    return parser.parse_args()


def read_recent_jsonl(hours: int) -> list[dict]:
    """Read all messages from JSONL files modified in the last N hours."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    messages = []

    if not PROJECTS_DIR.exists():
        log(f"WARNING: {PROJECTS_DIR} not found")
        return messages

    for jsonl_file in PROJECTS_DIR.rglob("*.jsonl"):
        mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            continue

        with open(jsonl_file, encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if obj.get("type") in ("user", "assistant"):
                        ts_raw = obj.get("timestamp", "")
                        try:
                            ts = datetime.fromisoformat(
                                ts_raw.replace("Z", "+00:00"))
                        except Exception:
                            ts = datetime.now(timezone.utc)

                        if ts >= cutoff:
                            role = obj.get("type")
                            msg = obj.get("message", {})
                            content = msg.get("content", "")
                            if obj.get("isMeta"):
                                continue
                            if isinstance(content, list):
                                # Text blocks only: tool_use / tool_result /
                                # thinking blocks are tool noise, not facts.
                                texts = []
                                for block in content:
                                    if isinstance(block, dict):
                                        if block.get("type", "text") == "text":
                                            texts.append(block.get("text", ""))
                                    elif isinstance(block, str):
                                        texts.append(block)
                                content = "\n".join(texts)
                            content = strip_harness(content if isinstance(content, str) else "")
                            if not content:
                                continue

                            messages.append({
                                "role": role,
                                "content": content[:4000],
                                "timestamp": ts,
                                "file": jsonl_file.name,
                            })
                except json.JSONDecodeError:
                    continue

    messages.sort(key=lambda x: x["timestamp"])
    log(f"Read {len(messages)} messages from last {hours}h")
    return messages


MIN_WORDS = 6          # a kept fact needs at least this many real words
MAX_SENTENCE = 300     # longer "sentences" are usually pasted blobs

_TAG_BLOCK = re.compile(
    r"<(system-reminder|command-[a-z-]+|local-command-[a-z-]+|bash-[a-z-]+|"
    r"task-notification|user-prompt-submit-hook)\b[^>]*>.*?</\1>",
    re.DOTALL,
)
_CODE_FENCE = re.compile(r"```.*?(```|$)", re.DOTALL)
_TOOL_NOISE = re.compile(
    r"(tool_use|tool_result|<[a-z_-]+>|</[a-z_-]+>|Traceback|Exit code|"
    r"\[DRY-RUN\]|stdout|stderr|"
    r"^\s*(?-i:def|class|import|const|let|var|function)\s+\w+\s*[(=:{]|"
    r"^\s*[$#>]\s|=>|\{\s*\"|\":\s)",
    re.IGNORECASE,
)
_SENTENCE_END = (".", "!", "?", "\u0589", "»", '"', "”", ")")   # \u0589 = Armenian full stop


def strip_harness(text: str) -> str:
    """Remove harness tags (system reminders, slash-command echoes) and code
    fences, so only what a person or the assistant wrote is left."""
    text = _TAG_BLOCK.sub(" ", text or "")
    text = _CODE_FENCE.sub(" ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    """Split on sentence ends and on line breaks; strip list and heading marks."""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("|"):          # markdown table rows
            continue
        line = re.sub(r"^([-*•·]|\d+[.)]|#{1,6})\s+", "", line)
        line = line.replace("**", "").replace("__", "")
        for part in re.split(r"(?<=[.!?\u0589])\s+", line):
            part = part.strip()
            if part:
                out.append(part)
    return out


def _real_words(text: str) -> int:
    return sum(1 for w in text.split() if w.strip(".,;:!?«»\"“”()'’`").isalpha())


def is_fact_sentence(s: str, require_start: bool = True) -> bool:
    """A kept fact reads as a whole statement on its own.

    Drops: fragments under MIN_WORDS real words, mid-sentence cut-offs
    (no sentence end, or a lowercase continuation start), code and tool noise,
    pipe fragments, and over-long pasted blobs."""
    s = s.strip()
    if not s or len(s) > MAX_SENTENCE:
        return False
    if _real_words(s) < MIN_WORDS:
        return False
    if s.count("|") >= 2 or s.count("`") >= 4:
        return False
    if _TOOL_NOISE.search(s):
        return False
    symbols = sum(1 for c in s if c in "{}[]<>=;$\\/_|~^")
    if symbols / len(s) > 0.08:
        return False
    if s.endswith(("...", "…", ":", ",", ";", "—", "-")):
        return False
    if not s.endswith(_SENTENCE_END):
        return False
    if require_start:
        c = s[0]
        if not (c.isupper() or c.isdigit() or "\u0531" <= c <= "\u0587" or c in "«\"“"):
            return False
    return True


def _norm(text: str) -> str:
    """Key for duplicate checks: lowercase letters and digits only."""
    body = re.sub(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] (User: )?", "", text)
    return re.sub(r"[\W_]+", "", body.lower())[:80]


def _dedupe(items: list[str]) -> list[str]:
    seen, out = set(), []
    for it in items:
        key = _norm(it)
        if key and key not in seen:
            seen.add(key)
            out.append(it)
    return out


def _matching_sentences(content: str, patterns: list[str], limit: int) -> list[str]:
    """Whole sentences that match any pattern (not the regex capture, which
    used to start mid-sentence)."""
    keys = [re.compile(r"(?<!\w)" + p.split("\\s+(")[0], re.IGNORECASE) for p in patterns]
    found = []
    for sent in split_sentences(content):
        if any(k.search(sent) for k in keys) and is_fact_sentence(sent):
            found.append(sent)
            if len(found) >= limit:
                break
    return found


def extract_facts(messages: list[dict]) -> dict:
    """Extract key facts from messages, as whole sentences."""
    decisions = []
    completions = []
    preferences = []
    project_updates = []
    user_topics = []

    for msg in messages:
        content = msg["content"]
        role = msg["role"]
        ts = msg["timestamp"].strftime("%Y-%m-%d %H:%M")

        # User messages — extract topics and requests
        if role == "user":
            # Short user messages = direct requests (kept whole, looser filter)
            flat = " ".join(content.split())
            if len(flat) < 300 and _real_words(flat) >= 4 and not _TOOL_NOISE.search(flat):
                user_topics.append(f"[{ts}] User: {flat[:150]}")

            for sent in _matching_sentences(content, PREFERENCE_PATTERNS, 2):
                preferences.append(f"[{ts}] {sent}")

        # Assistant messages — extract completions and decisions
        if role == "assistant":
            for sent in _matching_sentences(content, COMPLETION_PATTERNS, 3):
                completions.append(f"[{ts}] {sent}")

            for sent in _matching_sentences(content, DECISION_PATTERNS, 2):
                decisions.append(f"[{ts}] {sent}")

            # Project-related updates: first good sentence naming a keyword
            for sent in split_sentences(content):
                low = sent.lower()
                if any(kw in low for kw in PROJECT_KEYWORDS) and is_fact_sentence(sent):
                    project_updates.append(f"[{ts}] {sent}")
                    break

    return {
        "decisions": _dedupe(decisions)[:15],
        "completions": _dedupe(completions)[:20],
        "preferences": _dedupe(preferences)[:10],
        "project_updates": _dedupe(project_updates)[:15],
        "user_topics": _dedupe(user_topics)[:10],
    }


SUMMARY_KEYS = ("decisions", "completions", "preferences", "project_updates", "user_topics")
SUMMARY_PROMPT = """You are consolidating a person's memory from their recent Claude Code conversations (given on stdin).
Return ONLY one JSON object, no prose, with these keys, each a list of short whole sentences:
- "decisions": decisions taken and rules set ("from now on ...").
- "completions": work that was finished, with the file or project it touched.
- "preferences": stable preferences and corrections the user stated.
- "project_updates": status changes of named projects.
- "user_topics": what the user asked for, one line each.
Each sentence must stand on its own (no fragments, no code, no tool output), at most 30 words.
Skip anything already obvious or trivial. Use the language the user used. At most 10 items per key."""


def summarize_with_claude(messages: list[dict], timeout: int = 300):
    """Optional: summarise with the local `claude -p` CLI.

    Returns a facts dict like extract_facts(), or None when the CLI is missing,
    fails, or returns something that is not the expected JSON — the caller then
    uses the regex pass. Sessions are not persisted, so this call does not show
    up in tomorrow's logs."""
    exe = shutil.which("claude")
    if not exe:
        log("--summarize: `claude` CLI not found, using the regex pass")
        return None

    lines = [f"[{m['timestamp'].strftime('%Y-%m-%d %H:%M')}] {m['role']}: {m['content']}"
             for m in messages]
    transcript = "\n\n".join(lines)[-60000:]    # newest ~60k chars
    try:
        proc = subprocess.run(
            [exe, "-p", SUMMARY_PROMPT, "--no-session-persistence", "--tools", ""],
            input=transcript, capture_output=True, text=True, timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        log(f"--summarize: claude call failed ({e}), using the regex pass")
        return None
    if proc.returncode != 0:
        log(f"--summarize: claude exited {proc.returncode}, using the regex pass")
        return None

    out = proc.stdout
    try:
        data = json.loads(out[out.index("{"):out.rindex("}") + 1])
    except (ValueError, json.JSONDecodeError):
        log("--summarize: reply was not JSON, using the regex pass")
        return None

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    facts = {}
    for key in SUMMARY_KEYS:
        items = data.get(key, []) if isinstance(data, dict) else []
        items = [" ".join(str(i).split()) for i in items if isinstance(i, str)]
        if key == "user_topics":
            items = [f"[{stamp}] User: {i[:150]}" for i in items if _real_words(i) >= 3]
        else:
            items = [i if i.endswith(_SENTENCE_END) else i + "." for i in items]
            items = [f"[{stamp}] {i}" for i in items if is_fact_sentence(i, require_start=False)]
        facts[key] = _dedupe(items)[:15]
    log("--summarize: used claude -p summary")
    return facts


def update_recent_memory(facts: dict, dry_run: bool):
    """Overwrite the rolling 48h section of recent-memory.md."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")

    sections = []

    if facts["user_topics"]:
        sections.append("### Recent User Requests\n" +
                        "\n".join(f"- {t}" for t in facts["user_topics"]))

    if facts["completions"]:
        sections.append("### Completed This Session\n" +
                        "\n".join(f"- {c}" for c in facts["completions"]))

    if facts["decisions"]:
        sections.append("### Decisions Made\n" +
                        "\n".join(f"- {d}" for d in facts["decisions"]))

    if facts["project_updates"]:
        sections.append("### Project Activity\n" +
                        "\n".join(f"- {p}" for p in facts["project_updates"]))

    new_log_entry = f"\n### {today} (auto-updated {now})\n" + \
                    "\n\n".join(sections)

    if not RECENT_MEM.exists():
        content = f"# Recent Memory — Sliding 48h Context\n"
    else:
        content = RECENT_MEM.read_text(encoding="utf-8")

    # Replace or append the Rolling 48h Log section
    log_marker = "## Rolling 48h Log"
    if log_marker in content:
        before, _, _ = content.partition(log_marker)
        content = before + log_marker + new_log_entry
    else:
        content += f"\n\n{log_marker}{new_log_entry}"

    # Update last-updated header
    content = re.sub(
        r"<!-- Last updated:.*?-->",
        f"<!-- Last updated: {today} -->",
        content
    )

    if dry_run:
        print("\n=== RECENT MEMORY (would write) ===")
        print(content[-1500:])
    else:
        RECENT_MEM.write_text(content, encoding="utf-8")
        log(f"Updated {RECENT_MEM}")


def promote_to_long_term(facts: dict, dry_run: bool):
    """
    Append stable preferences/decisions to long-term memory.
    Only adds items not already present.
    """
    if not facts["preferences"] and not facts["decisions"]:
        log("Nothing new to promote to long-term memory")
        return

    if not LONG_MEM.exists():
        log(f"WARNING: {LONG_MEM} not found, skipping promotion")
        return

    existing = LONG_MEM.read_text(encoding="utf-8")
    existing_keys = {_norm(l) for l in existing.splitlines() if l.startswith("- ")}
    new_entries = []

    for pref in facts["preferences"]:
        # Remove timestamp prefix for dedup check
        clean = re.sub(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] ", "", pref)
        if clean[:40] not in existing and _norm(clean) not in existing_keys:
            new_entries.append(f"- {clean}")

    if not new_entries:
        log("No new entries to promote to long-term")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    addition = f"\n\n### Auto-promoted {today}\n" + "\n".join(new_entries)

    if dry_run:
        print("\n=== LONG-TERM PROMOTION (would append) ===")
        print(addition)
    else:
        with open(LONG_MEM, "a", encoding="utf-8") as f:
            f.write(addition)
        log(f"Promoted {len(new_entries)} entries to long-term memory")


def update_project_memory(facts: dict, dry_run: bool):
    """Add a session summary to project-memory.md."""
    if not facts["completions"] and not facts["project_updates"]:
        log("No project updates to write")
        return

    if not PROJECT_MEM.exists():
        log(f"WARNING: {PROJECT_MEM} not found, skipping")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")

    content = PROJECT_MEM.read_text(encoding="utf-8")
    existing = {_norm(l) for l in content.splitlines() if l.startswith("- ")}

    def _fresh(items):
        out = []
        for it in items[:8]:
            clean = re.sub(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] ", "", it)
            if _norm(clean) not in existing:
                existing.add(_norm(clean))
                out.append(f"- {clean}")
        return out

    lines = []
    done = _fresh(facts["completions"])
    if done:
        lines += ["**Completed:**"] + done
    proj = _fresh(facts["project_updates"])
    if proj:
        lines += ["**Project activity:**"] + proj
    if not lines:
        log("No new project lines to write")
        return

    entry = f"\n\n---\n### Session Log — {today} {now}\n" + "\n".join(lines)

    # Update "Last updated" in project memory
    content = re.sub(
        r"\*\*Last updated:\*\* \d{4}-\d{2}-\d{2}",
        f"**Last updated:** {today}",
        content
    )

    if dry_run:
        print("\n=== PROJECT MEMORY (would append) ===")
        print(entry)
    else:
        with open(PROJECT_MEM, "a", encoding="utf-8") as f:
            f.write(entry)
        log(f"Updated {PROJECT_MEM}")


def main():
    args = parse_args()
    log(f"=== Consolidate Memory START (lookback={args.hours}h, dry_run={args.dry_run}) ===")

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    messages = read_recent_jsonl(hours=args.hours)

    if not messages:
        log("No recent messages found — nothing to consolidate")
        return

    facts = summarize_with_claude(messages) if args.summarize else None
    if facts is None:
        facts = extract_facts(messages)
    log(f"Extracted: {len(facts['decisions'])} decisions, "
        f"{len(facts['completions'])} completions, "
        f"{len(facts['preferences'])} preferences, "
        f"{len(facts['project_updates'])} project updates")

    update_recent_memory(facts, dry_run=args.dry_run)
    promote_to_long_term(facts, dry_run=args.dry_run)
    update_project_memory(facts, dry_run=args.dry_run)

    log("=== Consolidate Memory COMPLETE ===\n")


if __name__ == "__main__":
    main()
