---
name: auto-learn
description: Automated daily web research that keeps ~/.memory/ current — searches global cinema, content, marketing, creative, advertising, platform, AI-tool, and active-project topics, then appends only genuinely new findings. Use when running or debugging the scheduled memory-refresh job, or when the user asks to pull fresh external information into memory.
metadata:
  version: 1.3.0
---

# Auto-Learn Skill

## Purpose
Daily web research that keeps `~/.memory/` current by finding new information
on the user's global work fields and active projects, saving only genuinely new
findings. The standing scope is worldwide: cinema, film/TV production, content,
marketing, creative work, advertising, platform changes, AI tools, and global
trends. Armenian-market topics are included as a small project-specific slice,
not the center of the run.

## Directory
```
~/.claude/skills/auto-learn/
  SKILL.md          ← this file
  auto-learn.py     ← main script
  auto-learn.log    ← run history
```

## Modes

| Mode | Schedule | What it does |
|------|----------|--------------|
| `--mode research` | Daily launchd job, 09:00 | Searches web, saves new findings to `## New Learnings` |
| `--mode promote` | Weekly launchd job, Sunday 10:00 | Moves mature entries (≥7 days) to main memory sections |

## Search Sources
- **Primary:** Tavily API (read from env or the existing Tavily MCP config)
- **Fallback:** Google News RSS, then DuckDuckGo package if present
- **Scope:** worldwide sources, with a broad trusted-source allowlist across film,
  marketing, advertising, creator economy, platforms, AI/tech, Reddit/HN, and GitHub
- **Recurring beats:** global film/TV, world cinema, streaming, microdrama, advertising,
  creative campaigns, creator economy, social content, platform algorithms, AI media
  tools, agent workflows, storytelling, Wikipedia/knowledge-panel strategy, plus a
  limited Armenian project slice.

## Output Format (New Learnings)

Entries are appended to `~/.memory/long-term-memory.md` under `## New Learnings`:

```
- **[2026-04-08 02:15]** `topic query here` — Key insight sentence. ([source](https://...))
```

## Manual Usage

```bash
# Run research now (saves to memory)
python3 ~/.claude/skills/auto-learn/auto-learn.py

# Dry run — print findings without saving
python3 ~/.claude/skills/auto-learn/auto-learn.py --test

# More topics per run (default: 12)
python3 ~/.claude/skills/auto-learn/auto-learn.py --topics 18

# Weekly promote pass (dry run)
python3 ~/.claude/skills/auto-learn/auto-learn.py --mode promote --test

# Check log
tail -50 ~/.claude/skills/auto-learn/auto-learn.log
```

## Launchd Schedule

```
~/Library/LaunchAgents/com.user.claude-auto-learn.plist          # daily 09:00
~/Library/LaunchAgents/com.user.claude-auto-learn-promote.plist  # Sunday 10:00
```

## Tavily API Key (Optional)

Tavily gives significantly better results (especially Reddit/HN filtering):

```bash
# Add to ~/.zshrc or ~/.zprofile
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxx"
```

The script first checks `TAVILY_API_KEY`, then reads the existing Tavily MCP key
from `~/.claude.json`, so launchd does not need a second plaintext key.

## How Deduplication Works

1. All URLs already in `~/.memory/` files are indexed as fingerprints
2. Key 4-gram phrases from existing memory are also indexed
3. Each new result is checked against both — only saved if genuinely new
4. Within one run, already-saved URLs are tracked to avoid duplicates

## Verification

Run the local evals before changing schedule, write behavior, dedupe logic, or
fallback behavior:

```bash
python3 ~/.claude/skills/auto-learn/evals/test_auto_learn.py
```

The evals use temporary memory files and mocked search results. They must prove:

- `--test` / dry-run does not write to long-term memory.
- duplicate URLs already present in memory are not saved again.
- noisy snippets and generic titles are rejected.
- a mocked research pass saves only genuinely new findings.

## Safety Boundaries

- Never publish, post, message, buy, or mutate external accounts.
- Never delete or rewrite memory files outside the explicit append/promote paths.
- Network research may run automatically, but adding new source categories,
  increasing run volume, or changing schedules requires explicit approval.
- Dry-run is mandatory before risky changes to query scope, dedupe, promotion, or
  write behavior.
