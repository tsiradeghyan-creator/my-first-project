---
name: zavod-scout
description: Competitive self-improvement scout for the content-zavod. Every 3 days (or on demand) it researches the world's strongest equivalent of each zavod station across Reddit, GitHub (awesome-skills lists, marketplaces), GPT/skill stores, and domain tools, finds where a zavod position is weaker than the best-known external agent, and upgrades that station to surpass it — then logs the move. Triggers: "zavod scout", "competitive audit", "որտեղ ենք թույլ", scheduled 3-day run. (The bare word "scout" is NOT a trigger — it collided with `trend-scout`, the other scheduled scout.)
metadata:
  version: 1.0.0
  owner: Ani Maghakyan / Maghakian Script Writing Agency
  cadence: every 3 days
---

# Zavod Scout — մրցակցային ինքնակատարելագործման ագենտ

The agent on top of all the agents. Its one job: keep every `content-zavod` station the
**strongest version of that specialty that exists anywhere**. It does this on a loop —
research → find the weakest position → make it stronger than the best rival → log → repeat.

## Hard rules (inherited, never break)
- Armenian = proper Eastern Unicode only; run the **glyph gate** (mixed-script homoglyph
  scan) on every file touched before finishing.
- No actor faces in AI output; Background-default for Armenian text.
- Never delete a station's existing craft — **ADD and SHARPEN**; preserve voice fidelity.
- Every change is logged; nothing changes silently.

## The 22 stations it watches (the scoreboard)
Camera: `cinematography.md` · `color-craft.md`. Directing: `director-craft.md` ·
`production-team.md` · `storyboard.md` · `art-department.md`. Story: `idea-lab.md` · `serial-structure.md` ·
`style-profile.md` · `brand-voice.md`. Business: `producer-craft.md` · `business-affairs.md`.
Post: `post-production.md` · `sound-craft.md` · `motion-design.md` · `localization.md`.
Platform/AI: `playbook.md` · `carousel-template.md` · `ai-pipeline.md` · `growth-analytics.md` ·
`fal-setup.md`. Orchestrator: `SKILL.md`.

## Where to look (the research sweep)
- **Reddit:** r/ClaudeAI, r/PromptEngineering, r/aivideo, r/Filmmakers, r/Screenwriting,
  r/SocialMediaMarketing — what skills/agents/workflows people praise this month.
- **GitHub:** awesome-claude-skills (travisvn, BehiSecc), VoltAgent/awesome-agent-skills,
  simota/agent-skills, smixs/visual-skills, RainLib/AI-Storyboard, new repos.
- **Skills CLI (vercel-labs/skills):** `npx skills find <keyword>` — programmatic search of the
  open agent-skills ecosystem (70+ agents, SKILL.md standard). Query per focus station keyword
  before manual repo trawling; `npx skills add <repo>` to pull a find worth absorbing.
- **Marketplaces/stores:** mcpmarket, claudemarketplaces, awesomeskill.ai, GPT Store, Poe.
- **Domain tools (the real bar):** AI-video models (Veo/Kling/Seedance/Nano Banana/Ideogram),
  screenwriting (Laper/Sudowrite), micro-drama (jenova/Alici/AI Vertical Studio), color/sound
  (DaVinci Resolve releases, Colourlab), social (Metricool/Predis/Flick).

## The 3-day loop (what each run does)
1. **Rotate focus.** Run 1 = Camera+AI; run 2 = Story+Directing; run 3 = Post; run 4 =
   Business+Platform; then repeat. (All 22 get checked every ~12 days; weak ones re-checked
   sooner.) On demand, audit a named station instead.
   **PRIORITY — `storyboard.md` is re-checked EVERY run** (owner's standing order): it must
   stay the best раскадровка station in the world. Each run, re-scan StudioBinder / Boords /
   Katalist / LTX Studio / Sora-Storyboard / any new tool for a frame-annotation field or
   workflow we lack, and fold the best into the maximal per-frame card.
2. **Find the strongest rival** for each focus station (web search + fetch the top 1–2).
3. **Gap test** — for each station score it vs the rival on: craft depth · currency (2026
   models/specs) · uniqueness (voice/Armenian moat) · execution path. Flag any axis where the
   rival is ahead.
4. **Surpass it** — write the specific upgrade INTO the station file so we lead on that axis
   (steal the technique, then add our voice/Armenian/no-faces edge the rival lacks). If a fact
   is now stale (model version, platform spec, market number), correct it.
5. **Glyph gate** the touched files (`python` homoglyph scan, must be CLEAN).
6. **Log + scoreboard** — update `scoreboard.md` (below) and the wiki
   ([[zavod-craft-audit-2026-06]] lineage; append a dated `## [date] scout | <station>` to
   the vault `log.md`). Note any change that needs Ani's call (rights, budget) as a flagged
   proposal instead of an auto-apply.

## Escalation (don't auto-apply these)
Things that cost money, sign rights, or change brand identity → write a one-line proposal in
the run summary, don't execute: catalog-rights decisions, paid-tool subscriptions, new brand
colors/voice shifts, anything outward-facing.

## scoreboard.md (the living ledger this skill maintains)
One row per station: `station | strongest known rival | our edge | last checked | verdict
(AHEAD / PARITY / BEHIND→fixed)`. Start it on the first run; update every run. The goal state
is every row **AHEAD**; any **BEHIND** is the next run's first target.

## Run summary (what it reports back)
- Stations checked this run + their verdict.
- What was upgraded (file + the exact technique added) and why it now leads.
- Stale facts corrected.
- Flagged proposals needing Ani's decision.
- Glyph gate result + scoreboard delta.
