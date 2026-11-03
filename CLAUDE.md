# Shared workspace: Tigran / Maghakian Scripts
This repo is shared between Claude Code in VS Code on Tigran's laptop and Claude Code cloud sessions (claude.ai/code). Neither side can see the other's chat. GitHub is the only shared memory.
- At the start of every session: git pull origin main, then read NOTES.md (newest entry first) and check BRIDGE.md for OPEN messages addressed to your side. Mention them to Tigran.
- BRIDGE.md is the mailbox between the two sides. `/bridge` reads and answers it, `/bridge <question>` sends a new question. Follow its rules.
- At the end of every session that changed anything: add an entry at the top of NOTES.md (date, which side: "VS Code" or "Cloud", what you did, what is left), then commit and push to main.
- Skills live in .claude/skills/. When you add or change a skill, push it so the other side gets it.
- RULE from Tigran (2026-11-03), both sides: whenever Tigran asks for ANY visual prompt (image/still) or video prompt (Seedance, Veo, Kling, Higgsfield, any model), ALWAYS run the `film-crew` skill first, even for a single shot. Its departments (director, design, costume, DP, editor, camera, sound) shape the prompt; then the model skill (seedance-25-director, banana-pro-director-2.0, cinema-worldbuilder-pro-2.0…) writes the final text. Never skip film-crew because a shot plan already exists; feed that plan into film-crew instead.
- Studio facts: maghakian-roast-room/business.md. Brand: black #000000, white #FFFFFF, graphite #111111, one red accent #D90429.
- Never commit API keys, tokens or passwords.
- The Roast Room (AI advisory council) is in maghakian-roast-room/. Run councils from inside that folder.
- memory/ is a daily snapshot of the laptop's ~/.memory (read-only for Cloud; the laptop is the source).
- .claude/skills-library/ is the archive used by the skill-library skill; on Cloud its path is .claude/skills-library/ in this repo instead of ~/.claude/skills-library/.
- The zavod canon lives in the private repo tsiradeghyan-creator/zavod-om.
- scripts/sync-from-laptop.sh pushes those snapshots from the laptop daily at 23:40; scripts/secret-scan.py checks every commit for secrets.
