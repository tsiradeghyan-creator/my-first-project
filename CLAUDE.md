# Shared workspace: Tigran / Maghakian Scripts
Since 2026-11-26 Tigran works cloud-only: Claude Code cloud sessions (claude.ai/code, web or phone). There is no local Mac or VS Code setup. GitHub is the memory between sessions.
- At the start of every session: git pull origin main, then read NOTES.md (newest entry first) and mention anything open to Tigran.
- At the end of every session that changed anything: add an entry at the top of NOTES.md (date, "Cloud", what you did, what is left), then commit and push to main.
- Skills live in .claude/skills/. When you add or change a skill, push it.
- RULE from Tigran (2026-11-03): whenever Tigran asks for ANY visual prompt (image/still) or video prompt (Seedance, Veo, Kling, Higgsfield, any model), ALWAYS run the `film-crew` skill first, even for a single shot (single-shot mode, added 2026-11-26). Its departments (director, design, costume, DP, editor, camera, sound) shape the prompt; then the model skill (seedance-25-director, banana-pro-director-2.0, cinema-worldbuilder-pro-2.0…) writes the final text. Never skip film-crew because a shot plan already exists; feed that plan into film-crew instead.
- RULE from Tigran (2026-11-03): for ANY task about content, video, image/visual, design, SMM, marketing, copy, pitching, screenwriting or books, run the `skill-router` skill first, without being asked: show him the matching skills he owns (2–5, one line each), recommend one with a reason, then start working. He should never have to name a skill. Keep its map updated when skills change.
- RULE from Tigran (2026-11-03): when a prompt, text or file he will copy changes, always give the WHOLE updated version, ready to copy. Never say "replace line X with Y" or give only the changed part.
- Studio facts: maghakian-roast-room/business.md. Portfolio (48 projects): .claude/skills/maghakian-brand/portfolio.md, source maghakianscripts.com/projects. Brand: black #000000, white #FFFFFF, graphite #111111, one red accent #D90429.
- Never commit API keys, tokens or passwords. Check commits with `git diff --cached -U0 | python3 -I scripts/secret-scan.py --diff`.
- The Roast Room (AI advisory council) is in maghakian-roast-room/. Run councils from inside that folder.
- memory/ is the studio memory (long-term, project, recent, trends-radar). It is the source now: Cloud sessions and the scheduled tasks write it directly and push.
- .claude/skills-library/ is the archive used by the skill-library skill.
- The zavod canon lives in the private repo tsiradeghyan-creator/zavod-om (skills/zavod-craft/). Edit it there (attach with add_repo, clone, push to its main), then copy the changed files into .claude/skills/content-zavod/ (and gpt-image-prompting/ into .claude/skills/gpt-image-prompting/) so the snapshot matches.
- Scheduled cloud tasks (created 2026-11-26, Yerevan time): trend-scout Mon/Wed/Fri, auto-learn Tue, zavod-scout Sat. Each starts a fresh session, writes memory/ or the zavod canon, and pushes.
- Archived (kept in case a Mac is used again, not in use): BRIDGE.md, scripts/sync-from-laptop.sh, scripts/setup-new-mac.sh, scripts/NEW-MAC.md, scripts/trend-scout-run.sh, scripts/zavod-scout-run.sh.
