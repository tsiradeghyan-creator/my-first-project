---
name: skill-library
description: Router to the skill-library archive (`~/.claude/skills-library/` on the laptop, `.claude/skills-library/` in the repo/Cloud; 267 folders, 251 of them top-level skills, moved out of the default context on 2026-07-02 by agent-sort). Use when a task needs an off-stack capability — e.g. a dev framework (django/laravel/spring/kotlin/swift/react…), a domain vertical (healthcare, logistics, billing, energy), crypto/web3, agency personas, integrations (jira, datadog, clickhouse, x-api), meta/agentic patterns (blueprint, eval-harness, autonomous-loops), or any skill not in the DAILY set. Search the library, read the matching SKILL.md, and follow it in place.
metadata:
  version: 1.1.0
---

# Skill Library Router

The full ECC skill collection lives in `~/.claude/skills-library/` on the laptop and in
`.claude/skills-library/` in this repo (the path to use on Cloud). It was moved there by agent-sort
on 2026-07-02 to stop ~250 irrelevant skill descriptions loading into every session.
Nothing was deleted — every skill is intact and usable.

**267 top-level folders, 251 of them skills with their own SKILL.md** (counted in the repo copy
on 2026-11-26). The other 16 are support or collection folders: `agents`, `docs`, `hooks`, `pdf`,
`schema`, `screenshots`, `scripts` have no SKILL.md at all, while `design-ops`, `design-research`,
`designer-toolkit`, `extensions`, `interaction-design`, `prototyping-testing`, `skills` (the
claude-seo pack: `seo-audit`, `seo-schema`, `seo-geo`…), `ui-design` and `ux-strategy` are *collections*
holding 77 nested skills. Search recursively, not just one level deep.

## DAILY set (already loaded from `.claude/skills/`, so there is no need to search the library for these; 29 on 2026-11-26)
agent-reach · auto-learn · bab-production · banana-pro-director-2.0 · cinema-worldbuilder-pro-2.0 ·
cli-hub · consolidate-memory · content-zavod · copywriting · director-desk · fal-ai-media · film-crew ·
gpt-image-prompting · graphify · higgsfield · jackvsai-fashion-campaign-prompt-framework · llm-council ·
maghakian-brand · media-memory · mini-scenario · remotion-video-creation · seedance-25-director ·
seo-audit · shortfilm-prompt · skill-library · skill-router · studio · trend-scout · zavod-scout

## How to use the library
Commands below use the laptop path; on Cloud replace `~/.claude/skills-library/` with `.claude/skills-library/`.
1. Find a candidate:
   `ls ~/.claude/skills-library/ | grep -i <keyword>`
   or search descriptions:
   `grep -ril --include=SKILL.md "<keyword>" ~/.claude/skills-library/` (recursive, so nested skills are found)
2. Read the matching `~/.claude/skills-library/<name>/SKILL.md` and follow it in place.
3. If a library skill becomes a regular need, promote it into the repo's `.claude/skills/<name>/`
   (copy it from the library, then commit and push so both sides get it).

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
