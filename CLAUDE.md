# Shared workspace: Tigran / Maghakian Scripts
This repo is shared between Claude Code in VS Code on Tigran's laptop and Claude Code cloud sessions (claude.ai/code). Neither side can see the other's chat. GitHub is the only shared memory.
- At the start of every session: git pull origin main, then read NOTES.md (newest entry first) and check BRIDGE.md for OPEN messages addressed to your side. Mention them to Tigran.
- BRIDGE.md is the mailbox between the two sides. `/bridge` reads and answers it, `/bridge <question>` sends a new question. Follow its rules.
- At the end of every session that changed anything: add an entry at the top of NOTES.md (date, which side: "VS Code" or "Cloud", what you did, what is left), then commit and push to main.
- Skills live in .claude/skills/. When you add or change a skill, push it so the other side gets it.
- Studio facts: maghakian-roast-room/business.md. Brand: black #000000, white #FFFFFF, graphite #111111, one red accent #D90429.
- Never commit API keys, tokens or passwords.
- The Roast Room (AI advisory council) is in maghakian-roast-room/. Run councils from inside that folder.
