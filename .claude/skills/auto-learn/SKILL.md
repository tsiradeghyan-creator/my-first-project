---
name: auto-learn
description: Automated daily web research that keeps ~/.memory/ current with facts about the studio's active projects and work — series reception, buyers and platforms, development funds, labs and festival deadlines, Armenian and diaspora industry news, children's publishing, Wikipedia and knowledge-panel work — and appends only genuinely new findings. Use when running or debugging the scheduled memory-refresh job, or when the user asks to pull fresh external information about the studio's projects into memory. Not for global content, platform or AI-tool trends (use trend-scout).
metadata:
  version: 1.4.0
---

# Auto-Learn Skill

## Purpose
Daily web research that keeps `~/.memory/` current by finding new information
on the studio's active projects and on facts the studio can act on, saving only
genuinely new findings.

Lane split with `trend-scout`:
- **auto-learn (this skill):** active projects (reception of our series), buyers and
  platforms commissioning scripted series, development funds, labs, festival and
  market deadlines, Armenian and diaspora industry news, children's publishing,
  Wikipedia / knowledge-panel work. Results go to `~/.memory/long-term-memory.md`.
- **trend-scout:** global trends — formats, platforms and algorithms, creator
  economy, new AI tools, storytelling patterns. Results go to `memory/trends-radar.md`.
  Armenian-market topics stay here, since trend-scout covers global trends only.

## Directory
```
.claude/skills/auto-learn/
  SKILL.md          ← this file
  auto-learn.py     ← main script
  auto-learn.log    ← run history (written next to the script)
  evals/            ← offline tests
```

## Modes

| Mode | Schedule | What it does |
|------|----------|--------------|
| `--mode research` | Daily launchd job, 09:00 | Searches web, saves new findings to `## New Learnings` |
| `--mode promote` | Weekly launchd job, Sunday 10:00 | Moves mature entries (≥7 days) to main memory sections |

## Search Sources
- **Primary:** Tavily API (read from env or the existing Tavily MCP config)
- **Fallback:** Google News RSS, then DuckDuckGo package if present
- **Scope:** a trusted-source allowlist for Tavily (trade press, co-production and
  publishing press, Armenian diaspora press, Reddit/HN, GitHub)
- **Recurring beats, in this order:** active project titles found in project memory
  (reception and reviews), then studio topics — development funds and labs, festival and
  market deadlines, platforms and broadcasters buying scripted series, Russian-language
  platform commissions, Armenian and diaspora film/TV news and funding, children's
  publishing (print on demand, Armenian children's books), Wikipedia / Wikidata /
  knowledge-panel work. Project topics run first so `--topics` never cuts them off.

## Noise filter

Before saving, each snippet is cleaned (HTML entities such as `&nbsp;` decoded, tags and
markdown escapes removed, " | News | Site" breadcrumbs trimmed) and rejected if it is a
markdown table row or pipe fragment, a list or schedule fragment, slug soup, a sentence
cut off at the snippet limit, or has fewer than 6 real words. The evals hold the junk
cases that earlier runs saved.

## Output Format (New Learnings)

Entries are appended to `~/.memory/long-term-memory.md` under `## New Learnings`:

```
- **[2026-04-08 02:15]** `topic query here` — Key insight sentence. ([source](https://...))
```

## Manual Usage

```bash
# Run research now (saves to memory)
python3 .claude/skills/auto-learn/auto-learn.py

# Dry run — print findings without saving
python3 .claude/skills/auto-learn/auto-learn.py --test

# More topics per run (default: 12)
python3 .claude/skills/auto-learn/auto-learn.py --topics 18

# Weekly promote pass (dry run)
python3 .claude/skills/auto-learn/auto-learn.py --mode promote --test

# Check log
tail -50 .claude/skills/auto-learn/auto-learn.log
```

## Launchd Schedule

These LaunchAgents ran on the old Mac and are not installed on the new one yet; the
new-Mac setup recreates them.

```
~/Library/LaunchAgents/com.user.claude-auto-learn.plist          # daily 09:00
~/Library/LaunchAgents/com.user.claude-auto-learn-promote.plist  # Sunday 10:00
```

## Tavily API Key (Optional)

Tavily gives better results than the free fallbacks. `auto-learn.py` looks for the key
in two places, in this order:

1. the `TAVILY_API_KEY` environment variable of the process that runs it;
2. the `env.TAVILY_API_KEY` of the `tavily-search` MCP server in `~/.claude.json`
   (top-level `mcpServers` or any project's `mcpServers`).

Use option 2: set the key once in the `tavily-search` MCP server entry in
`~/.claude.json` and both Claude Code and the scheduled job use it. A LaunchAgent does not
read `~/.zshrc`, so a key exported there is not seen by the scheduled run. Never commit
the key. With no key the script falls back to Google News RSS.

## How Deduplication Works

1. All URLs already in `~/.memory/` files are indexed as fingerprints
2. Key 4-gram phrases from existing memory are also indexed
3. Each new result is checked against both — only saved if genuinely new
4. Within one run, already-saved URLs are tracked to avoid duplicates

## Verification

Run the local evals before changing schedule, write behavior, dedupe logic, or
fallback behavior:

```bash
python3 .claude/skills/auto-learn/evals/test_auto_learn.py
```

The evals use temporary memory files and mocked search results. They check that:

- `--test` / dry-run does not write to long-term memory.
- duplicate URLs already present in memory are not saved again.
- noisy snippets, generic titles and the junk cases from past runs (table rows,
  `&nbsp;` text, slug soup, list fragments) are rejected.
- a mocked research pass saves only genuinely new findings.

## Safety Boundaries

- Never publish, post, message, buy, or mutate external accounts.
- Never delete or rewrite memory files outside the explicit append/promote paths.
- Network research may run automatically, but adding new source categories,
  increasing run volume, or changing schedules requires explicit approval.
- Do a dry run before risky changes to query scope, dedupe, promotion, or
  write behavior.
