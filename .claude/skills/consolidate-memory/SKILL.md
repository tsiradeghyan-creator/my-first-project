---
name: consolidate-memory
description: Read recent Claude conversation logs (~/.claude/projects/**/*.jsonl), extract decisions, preferences, completed tasks, key facts, and project updates, then update the memory files in ~/.memory/ (recent / long-term / project). Use when the user runs /consolidate-memory or asks to sync, consolidate, or refresh memory.
metadata:
  version: 1.3.0
---

# Consolidate Memory Skill

## Purpose
Read recent Claude conversation logs, extract key decisions/facts/preferences, and update the three memory files in ~/.memory/.

## When to Use
- Manually: `/consolidate-memory` — run on demand to sync memory
- Automatically: once a night, from the LaunchAgent `com.user.claude-consolidate-memory`
  (see Schedule below)

## What It Does
1. Reads ~/.claude/projects/**/*.jsonl from the last 24 hours
2. Extracts: decisions, preferences, completed tasks, key facts, project updates —
   as whole sentences (regex pass) or as a `claude -p` summary (`--summarize`)
3. Updates ~/.memory/recent-memory.md (sliding 48h window)
4. Promotes stable patterns → ~/.memory/long-term-memory.md
5. Updates project statuses in ~/.memory/project-memory.md
6. Archives entries older than 48h from recent-memory

## How to Run Manually

```bash
python3 .claude/skills/consolidate-memory/consolidate.py
```

Options:
```bash
python3 .claude/skills/consolidate-memory/consolidate.py --hours 72     # longer look-back
python3 .claude/skills/consolidate-memory/consolidate.py --dry-run      # print, write nothing
python3 .claude/skills/consolidate-memory/consolidate.py --summarize    # summarise with claude -p
```

## Schedule
One schedule: a nightly macOS LaunchAgent, `com.user.claude-consolidate-memory`, on the
laptop. It is not installed on the new Mac yet; the new-Mac setup recreates it. The job runs:
```
/usr/bin/python3 $HOME/my-first-project/.claude/skills/consolidate-memory/consolidate.py
```
A plist does not expand `$HOME`, so write the full path there. The script writes its own
log to `$HOME/.memory/consolidate.log`, so point the plist's stdout and stderr at a separate
file (or `/dev/null`) to avoid doubled lines. There is no cron entry.

## Extraction modes
- **Regex pass (default, offline).** Splits messages into sentences and keeps a whole
  sentence only when it matches a signal below and reads as a statement on its own:
  at least 6 real words, starts like a sentence, ends with sentence punctuation (`.` `!`
  `?` `։`), no code, tool output, table rows or harness tags (system reminders,
  tool_use / tool_result blocks are skipped), and not a duplicate of a line already in
  memory.
- **`--summarize` (optional).** Sends the recent messages to the local `claude -p` CLI
  (no tools, session not saved) and asks for the same five lists as JSON. The answer goes
  through the same sentence filter. If `claude` is missing, fails, times out or returns
  something other than JSON, the run falls back to the regex pass.

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
python3 .claude/skills/consolidate-memory/evals/test_consolidate_memory.py
```

The evals use temporary conversation logs and temporary memory files. They check
that:

- dry-run does not write `recent-memory.md`, `long-term-memory.md`, or
  `project-memory.md`,
- malformed JSONL lines are ignored safely,
- short/empty extracted fragments, cut-off sentences, code, tool noise and duplicates
  are filtered out (with the junk lines the old pass wrote as cases),
- `--summarize` falls back to the regex pass when `claude` is not on PATH,
- valid preferences and completions are promoted into the expected output
  sections.

## Safety Boundaries

- Read conversation logs only for memory consolidation.
- The default regex pass stays on this machine. `--summarize` sends the recent
  conversation text to Claude through the user's own `claude` CLI; it is opt-in and is
  the only path that leaves the machine. Do not send extracted content anywhere else.
- Do not delete source logs or memory files.
- Do a dry run before major regex, time-window, or promotion changes.
