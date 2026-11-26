---
name: trend-scout
description: Daily global trend radar — researches worldwide content/creator trends (Reels/TikTok/IG formats, viral audio, X/Twitter, YouTube long-form, podcasts, film/TV industry, platform changes, newly released AI models/tools, storytelling patterns, and GitHub repos that could strengthen the zavod) and maintains the memory/trends-radar.md page in my-first-project so any production session can use fresh trend intel. Use when the user runs /trend-scout, asks "ինչ տրենդներ կան", "what's trending", or when producing content that should ride current trends. Covers global trends only; the user has asked to leave out an Armenian-market focus. Not for facts about the studio's own projects, buyers, funds or Armenian industry news (use auto-learn).
metadata:
  version: 1.1.0
  updated: 2026-11-26
---

# Trend Scout — Global Trend Radar

## Purpose
Keep a continuously fresh picture of **global** content trends so the content-zavod
and any other session can pull trend intel on demand. The user's rule: worldwide
trends only — Armenian-market trends are explicitly out of scope.

## Directory
```
.claude/skills/trend-scout/
  SKILL.md          ← this file
```

## Schedule (cloud-only since 2026-11-26)
Tigran works cloud-only now (no local Mac setup). A cloud scheduled task starts a fresh
session three times a week (Mon, Wed, Fri morning, Yerevan time) and runs the procedure below.
The old Mac runner and LaunchAgent are retired; `scripts/trend-scout-run.sh` is kept only as
an archive in case a Mac is used again.

## Output — single source of truth
`memory/trends-radar.md` in my-first-project. Write it directly in the repo, then commit and
push to main with a NOTES.md line. The repo's `memory/` is the source of memory now (the
laptop sync is retired), so Cloud writes there.

Structure of the page (keep these sections, newest entries on top, every entry dated):

1. **🔥 Hot right now** — trends peaking this week (formats, audio, memes, hooks)
2. **📈 Rising** — early signals worth testing before they peak
3. **📉 Fading** — trends to stop using
4. **🛠 Platform & algorithm news** — IG/TikTok/YouTube/X feature or ranking changes
5. **🤖 AI & tools** — newly released AI models/tools worldwide that would benefit
   our production if adopted. Only tools that exist and are usable — when a tool is
   discontinued (e.g. Sora, dead 2026), delete its entries instead of tracking it.
6. **🎬 Film, TV & long-form** — film/series industry moves, YouTube long-form and
   podcast trends, streaming-platform shifts, storytelling formats that travel
7. **🧰 Repos for the zavod** — GitHub repos/frameworks that could strengthen
   ZavodOM (pipelines, agents, video tooling, prompt systems). For each: 1 line on
   what it is + what the zavod could steal. Leave the zavod itself unchanged here: flag
   the repo and leave adoption to zavod-scout / the user.
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
1. Read the current `memory/trends-radar.md` (create it if missing).
2. Web-search each beat with **current-month** queries (e.g. "trending reels formats
   <Month Year>"). Global/English sources.
3. **Deduplicate:** skip anything already on the page; only add genuinely new
   findings or move an entry between sections (Rising → Hot → Fading) with an
   updated date.
4. Move entries older than 30 days to Archive; delete Archive entries older than 90 days.
5. Update the page and add a dated `## [YYYY-MM-DD] trend-scout run` line (1-3 lines: what
   changed) at the top of the page's run log.
6. Keep the page small — max ~15 entries per live section; quality over volume.

## How other sessions consume it
- content-zavod / any content production: read `memory/trends-radar.md` before
  ideation when the task benefits from trend awareness.
- User asks "ինչ տրենդներ կան" / "what's trending": answer from the page first,
  refresh with live search only if the page is stale (>2 days since last entry).

## Manual usage
Ask for a trend-scout run ("/trend-scout") and follow the run procedure above. There is no
runner script to call until one is recreated on the new computer.
