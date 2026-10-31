---
name: consolidate-memory
description: Read recent Claude conversation logs (~/.claude/projects/**/*.jsonl), extract decisions, preferences, completed tasks, key facts, and project updates, then update the memory files in ~/.memory/ (recent / long-term / project). Use when the user runs /consolidate-memory or asks to sync, consolidate, or refresh memory.
metadata:
  version: 1.2.0
---

# Consolidate Memory Skill

## Purpose
Read recent Claude conversation logs, extract key decisions/facts/preferences, and update the three memory files in ~/.memory/.

## When to Use
- Manually: `/consolidate-memory` — run on demand to sync memory
- Automatically: runs nightly at 00:00 via cron

## What It Does
1. Reads ~/.claude/projects/**/*.jsonl from the last 24 hours
2. Extracts: decisions, preferences, completed tasks, key facts, project updates
3. Updates ~/.memory/recent-memory.md (sliding 48h window)
4. Promotes stable patterns → ~/.memory/long-term-memory.md
5. Updates project statuses in ~/.memory/project-memory.md
6. Archives entries older than 48h from recent-memory

## How to Run Manually

```bash
python3 ~/.claude/skills/consolidate-memory/consolidate.py
```

Or with date override:
```bash
python3 ~/.claude/skills/consolidate-memory/consolidate.py --hours 72
```

## Cron Schedule
Runs every night at 00:00 (midnight):
```
0 0 * * * python3 /Users/apple/.claude/skills/consolidate-memory/consolidate.py >> /Users/apple/.memory/consolidate.log 2>&1
```

## Output Files
- `~/.memory/recent-memory.md` — last 48h context (rolling)
- `~/.memory/long-term-memory.md` — stable facts & preferences
- `~/.memory/project-memory.md` — active project states
- `~/.memory/consolidate.log` — run history & errors

## Extraction Patterns
The script looks for these signals in conversations:
- **Decisions:** "decided", "going with", "chose", "will use", "from now on"
- **Preferences:** "always", "never", "prefer", "don't want", "make sure"
- **Completions:** "done", "created", "added", "completed", "finished"
- **Projects:** file paths, skill names, brand names, project names
- **Rules:** corrections, feedback, "instead of", "not like that"

## Verification

Run the local evals before changing extraction patterns, dry-run behavior, or
memory write behavior:

```bash
python3 ~/.claude/skills/consolidate-memory/evals/test_consolidate_memory.py
```

The evals use temporary conversation logs and temporary memory files. They must
prove:

- dry-run does not write `recent-memory.md`, `long-term-memory.md`, or
  `project-memory.md`,
- malformed JSONL lines are ignored safely,
- short/empty extracted fragments are filtered out,
- valid preferences and completions are promoted into the expected output
  sections.

## Safety Boundaries

- Read conversation logs only for memory consolidation.
- Do not send extracted content to external services.
- Do not delete source logs or memory files.
- Dry-run is mandatory before major regex, time-window, or promotion changes.
