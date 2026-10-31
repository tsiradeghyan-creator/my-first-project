# Skill usage on the laptop (answer to C5)

Source: Claude Code session logs in `~/.claude/projects/` on the laptop, read 2026-10-31 by VS Code.
Window: the logs only reach back to **2026-10-02** (Claude Code deletes transcripts older than 30 days by default, `cleanupPeriodDays` is not set), so this covers 30 days, not 60. 57 sessions.
Counted: `Skill` tool calls in main-thread messages plus slash commands Tigran typed. Subagent (sidechain) calls are not counted.

| # | Skill | Total | Via Skill tool | Typed as /command | Sessions |
|---|---|---|---|---|---|
| 1 | seedance-25-director | 9 | 9 | 0 | 9 |
| 2 | film-crew | 5 | 5 | 0 | 5 |
| 3 | gpt-image-prompting | 3 | 3 | 0 | 3 |
| 4 | banana-pro-director-2.0 | 2 | 2 | 0 | 2 |
| 5 | cinema-worldbuilder-pro-2.0 | 2 | 2 | 0 | 2 |
| 6 | agent-reach | 1 | 1 | 0 | 1 |
| 7 | anthropic-skills:maghakian-brand (claude.ai account version) | 1 | 1 | 0 | 1 |
| 8 | fal-ai-media | 1 | 1 | 0 | 1 |

Built-in commands, not skills: `/model` 5, `/compact` 3.

**Zero explicit calls in 30 days:** auto-learn, consolidate-memory, content-zavod, copywriting, graphify, higgsfield, jackvsai-fashion-campaign-prompt-framework, llm-council, maghakian-brand (local copy), media-memory, mini-scenario, remotion-video-creation, seo-audit, shortfilm-prompt, skill-library, trend-scout, zavod-scout.

Caveats:
- auto-learn, consolidate-memory, trend-scout and zavod-scout run as scheduled LaunchAgents on the laptop. Those runs call scripts or headless `claude -p` and do not show up as `Skill` tool calls, so zero here does not mean unused.
- Work done in claude.ai chat, the desktop app or ChatGPT is not in these logs.
