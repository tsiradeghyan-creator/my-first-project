---
name: skill-library
description: Router to the ~/.claude/skills-library/ archive (252 ECC skills moved out of the default context on 2026-07-02 by agent-sort). Use when a task needs an off-stack capability — e.g. a dev framework (django/laravel/spring/kotlin/swift/react…), a domain vertical (healthcare, logistics, billing, energy), crypto/web3, agency personas, integrations (jira, datadog, clickhouse, x-api), meta/agentic patterns (blueprint, eval-harness, autonomous-loops), or any skill not in the DAILY set. Search the library, read the matching SKILL.md, and follow it in place.
metadata:
  version: 1.1.0
---

# Skill Library Router

The full ECC skill collection lives in `~/.claude/skills-library/` (moved there by agent-sort
on 2026-07-02 to stop ~250 irrelevant skill descriptions loading into every session).
Nothing was deleted — every skill is intact and usable.

**252 top-level skills** (verified 2026-07-25). 17 further top-level directories are
support/spill folders rather than skills — `agents`, `docs`, `hooks`, `pdf`, `schema`,
`schema`, `screenshots`, `scripts` have no SKILL.md at all, while `design-ops`,
`design-research`, `designer-toolkit`, `extensions`, `interaction-design`,
`prototyping-testing`, `skills`, `ui-design`, `ux-strategy` and `ruflo` are *collections*
holding nested skills (ruflo alone nests 266). Search recursively, not just one level deep.

## DAILY set (already loaded — never search the library for these; all 20)
agent-reach · auto-learn · consolidate-memory · content-zavod · copywriting · fal-ai-media ·
gpt-image-prompting · graphify · higgsfield · jackvsai-fashion-campaign-prompt-framework ·
llm-council · maghakian-brand · media-memory · mini-scenario · remotion-video-creation ·
seo-audit · shortfilm-prompt · skill-library · trend-scout · zavod-scout

## How to use the library
1. Find a candidate:
   `ls ~/.claude/skills-library/ | grep -i <keyword>`
   or search descriptions:
   `grep -ril "<keyword>" ~/.claude/skills-library/*/SKILL.md`
2. Read the matching `~/.claude/skills-library/<name>/SKILL.md` and follow it in place.
3. If a library skill becomes a regular need, promote it back:
   `mv ~/.claude/skills-library/<name> ~/.claude/skills/`

## Output Contract

- Report the selected library skill path and why it matches the request.
- If no good match exists, say that plainly and continue with the best local capability.
- If promotion is useful, recommend it separately; do not move files without explicit approval.

## Verification

- Search recursively, because some archives contain nested skills.
- Read the selected `SKILL.md` before applying it.
- Treat archived platform/model/API facts as stale unless verified against current sources.

## Safety Boundaries

- Do not install, promote, delete, or move archived skills without explicit approval.
- Do not run archived scripts until their skill instructions and safety boundaries are read.
- Prefer active daily skills when they already cover the task.

## What's in the library (groups)
- **Dev stacks**: django, laravel, springboot, kotlin, swift(ui), rust, golang, perl, cpp, csharp,
  dotnet, react, nextjs, nuxt4, mui, bun, postgres, docker, nestjs, python-*, e2e/webapp-testing…
- **Domain verticals**: healthcare-*, hipaa, logistics, customs, carrier, inventory, returns,
  production-scheduling, quality-nonconformance, energy-procurement, finance/customer-billing…
- **Crypto/web3**: defi-amm-security, evm-token-decimals, nodejs-keccak256, agent-payment-x402,
  llm-trading-agent-security
- **Agency personas**: account-director, campaign-manager, media-planner, project-manager,
  brand-strategist, creative-director, copywriter-agent, content-creator, visual-designer,
  web-builder, seo-specialist…
- **Integrations**: jira(-integration), datadog-cli, clickhouse-io, composio, connect,
  github-ops, google-workspace-ops, x-api, exa-search, perplexity, gemini, codex…
- **Content/marketing (overlaps the zavod)**: brand-voice, content-engine, content-strategy,
  article-writing, humanizer, copy-editing, crosspost, meme-factory, twitter-algorithm-optimizer…
- **Meta/agentic**: blueprint, autonomous-loops, eval-harness, agent-eval, agent-sort,
  configure-ecc, skill-stocktake, context-budget, council, commit-work, code-review…
- **ECC repo files** (not skills): install/uninstall scripts, CHANGELOG, docs/, schema/,
  screenshots/, agents/, hooks/, scripts/ — kept for reference only.
