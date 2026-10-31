---
name: trend-scout
description: Daily global trend radar — researches worldwide content/creator trends (Reels/TikTok/IG formats, viral audio, X/Twitter, YouTube long-form, podcasts, film/TV industry, platform changes, newly released AI models/tools, storytelling patterns, and GitHub repos that could strengthen the zavod) and maintains the wiki/trends-radar.md page in the Obsidian vault so any production session can use fresh trend intel. Use when the user runs /trend-scout, asks "ինչ տրենդներ կան", "what's trending", or when producing content that should ride current trends. GLOBAL trends only — the user explicitly does NOT want Armenian-market focus.
metadata:
  version: 1.0.0
---

# Trend Scout — Global Trend Radar

## Purpose
Keep a continuously fresh picture of **global** content trends so the content-zavod
and any other session can pull trend intel on demand. The user's rule: worldwide
trends only — Armenian-market trends are explicitly out of scope.

## Directory
```
~/.claude/skills/trend-scout/
  SKILL.md          ← this file
  runs.log          ← launchd run history
~/.claude/trend-scout-run.sh          ← launchd runner (headless claude -p)
~/Library/LaunchAgents/com.maghakian.trend-scout.plist  ← daily 08:30 schedule
```

## Output — single source of truth
`~/Documents/Obsidian Vault/Claude/wiki/trends-radar.md`

Structure of the page (keep these sections, newest entries on top, every entry dated):

1. **🔥 Hot right now** — trends peaking this week (formats, audio, memes, hooks)
2. **📈 Rising** — early signals worth testing before they peak
3. **📉 Fading** — trends to stop using
4. **🛠 Platform & algorithm news** — IG/TikTok/YouTube/X feature or ranking changes
5. **🤖 AI & tools** — NEWLY released AI models/tools worldwide that would benefit
   our production if adopted. Only tools that exist and are usable — when a tool is
   discontinued (e.g. Sora, dead 2026), delete its entries instead of tracking it.
6. **🎬 Film, TV & long-form** — film/series industry moves, YouTube long-form and
   podcast trends, streaming-platform shifts, storytelling formats that travel
7. **🧰 Repos for the zavod** — GitHub repos/frameworks that could strengthen
   ZavodOM (pipelines, agents, video tooling, prompt systems). For each: 1 line on
   what it is + what the zavod could steal. Do NOT modify the zavod here — flag the
   repo and leave adoption to zavod-scout / the user.
8. **🗄 Archive** — entries older than 30 days get moved here (trim archive at 90 days)

Every entry: `- **[YYYY-MM-DD]** insight sentence — why it matters for us. ([source](url))`

## Research beats (each run covers all, ~2-3 searches per beat)
- Short-form video: trending Reels/TikTok formats, hooks, editing styles, audio
- X/Twitter: trending topics/formats among creators, platform changes, what's viral
- YouTube long-form & podcasts: formats, retention tactics, podcast industry moves
- Film & TV industry: streaming/production news, series trends, storytelling shifts
- Creator economy & content marketing: what top creators/agencies are doing
- Platform changes: Instagram, TikTok, YouTube, X algorithm/feature updates
- New AI releases: models/tools just launched worldwide (video, image, audio,
  script, agents) with concrete production value for us; drop discontinued ones
- Zavod-strengthening repos: GitHub (trending, awesome lists, HN Show) — agentic
  video pipelines, content-production frameworks, prompt/eval tooling
- Scriptwriting/storytelling: viral narrative structures, caption/copy patterns

Prioritise sources: Reddit (r/InstagramMarketing, r/Tiktokhelp, r/socialmedia,
r/NewTubers, r/podcasting, r/LocalLLaMA), Hacker News, GitHub trending,
later.com/blog, buffer.com/resources, hootsuite blog, socialmediatoday.com,
variety.com, hollywoodreporter.com, tubefilter.com, YouTube/TikTok creator news.

## Run procedure (scheduled or manual)
1. Read the current `wiki/trends-radar.md` (create it if missing).
2. Web-search each beat with **current-month** queries (e.g. "trending reels formats
   <Month Year>"). Global/English sources.
3. **Deduplicate:** skip anything already on the page; only add genuinely new
   findings or move an entry between sections (Rising → Hot → Fading) with an
   updated date.
4. Move entries older than 30 days to Archive; delete Archive entries older than 90 days.
5. Update the page, append a `## [YYYY-MM-DD] trend-scout run` entry to the vault
   `log.md` (1-3 lines: what changed). Ensure `index.md` has the trends-radar row.
6. Keep the page small — max ~15 entries per live section; quality over volume.

## How other sessions consume it
- content-zavod / any content production: read `wiki/trends-radar.md` before
  ideation when the task benefits from trend awareness.
- User asks "ինչ տրենդներ կան" / "what's trending": answer from the page first,
  refresh with live search only if the page is stale (>2 days since last entry).

## Manual usage
```bash
# Run a scout pass now
zsh ~/.claude/trend-scout-run.sh

# Check run history
tail -50 ~/.claude/skills/trend-scout/runs.log

# Reload the schedule after editing the plist
launchctl unload ~/Library/LaunchAgents/com.maghakian.trend-scout.plist
launchctl load ~/Library/LaunchAgents/com.maghakian.trend-scout.plist
```
