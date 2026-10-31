#!/usr/bin/env python3
"""
Consolidate Memory — Nightly Claude conversation log processor.
Reads ~/.claude/projects/**/*.jsonl, extracts key facts,
and updates ~/.memory/*.md files.
"""

import json
import os
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
                            if isinstance(content, list):
                                # Extract text from content blocks
                                texts = []
                                for block in content:
                                    if isinstance(block, dict):
                                        texts.append(
                                            block.get("text", ""))
                                    elif isinstance(block, str):
                                        texts.append(block)
                                content = " ".join(texts)

                            messages.append({
                                "role": role,
                                "content": content[:2000],
                                "timestamp": ts,
                                "file": jsonl_file.name,
                            })
                except json.JSONDecodeError:
                    continue

    messages.sort(key=lambda x: x["timestamp"])
    log(f"Read {len(messages)} messages from last {hours}h")
    return messages


def extract_facts(messages: list[dict]) -> dict:
    """Extract key facts from messages."""
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
            # Short user messages = direct requests
            if len(content) < 300:
                user_topics.append(f"[{ts}] User: {content[:150]}")

            # Check for preference/rule statements
            for pattern in PREFERENCE_PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for m in matches[:2]:
                    preferences.append(f"[{ts}] {m.strip()}")

        # Assistant messages — extract completions and decisions
        if role == "assistant":
            for pattern in COMPLETION_PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for m in matches[:3]:
                    if len(m) > 15:
                        completions.append(f"[{ts}] {m.strip()}")

            for pattern in DECISION_PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for m in matches[:2]:
                    decisions.append(f"[{ts}] {m.strip()}")

            # Project-related updates
            content_lower = content.lower()
            for kw in PROJECT_KEYWORDS:
                if kw in content_lower:
                    # Extract the sentence containing the keyword
                    sentences = content.split(".")
                    for s in sentences:
                        if kw in s.lower() and 20 < len(s) < 200:
                            project_updates.append(
                                f"[{ts}] {s.strip()}")
                            break
                    break

    def _clean(items, require_sentence=False):
        """Drop the two classes of garbage this extractor used to emit.

        1. Empty strings — user messages whose content is a tool result or a
           structured block rather than text produced ten '- ' bullets with nothing
           after them in recent-memory.md.
        2. Mid-sentence fragments — the regex capture groups start wherever the
           pattern matched, so long-term-memory.md filled up with entries like
           '- "and then".', '- wins the tie."' and '- seen real g'. A promoted fact
           has to read as a statement on its own.
        """
        out = []
        for it in items:
            body = re.sub(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] (User: )?", "", it).strip()
            if len(body) < 20:
                continue
            if require_sentence:
                # must start like a new statement, not a continuation
                if not (body[0].isupper() or body[0].isdigit() or "Ա" <= body[0] <= "֏"):
                    continue
                # must not be visibly truncated
                if not body.rstrip().endswith((".", "!", "?", ":", "»", '"', ")")):
                    continue
                if len(body) < 40:
                    continue
            out.append(it)
        return out

    return {
        "decisions": list(dict.fromkeys(_clean(decisions, True)))[:15],
        "completions": list(dict.fromkeys(_clean(completions)))[:20],
        "preferences": list(dict.fromkeys(_clean(preferences, True)))[:10],
        "project_updates": list(dict.fromkeys(_clean(project_updates)))[:15],
        "user_topics": list(dict.fromkeys(_clean(user_topics)))[:10],
    }


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
    new_entries = []

    for pref in facts["preferences"]:
        # Remove timestamp prefix for dedup check
        clean = re.sub(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] ", "", pref)
        if clean[:40] not in existing:
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

    lines = []
    if facts["completions"]:
        lines.append("**Completed:**")
        for c in facts["completions"][:8]:
            clean = re.sub(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] ", "", c)
            lines.append(f"- {clean}")

    entry = f"\n\n---\n### Session Log — {today} {now}\n" + "\n".join(lines)

    # Update "Last updated" in project memory
    content = PROJECT_MEM.read_text(encoding="utf-8")
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
