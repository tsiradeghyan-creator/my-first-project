---
name: gan-style-harness
description: "Planner → Generator → Evaluator agent harness for long-running app or frontend builds where quality matters more than cost (roughly $100–200 and hours per project). A separate, strict evaluator tests the live app in a browser and sends feedback until every criterion clears its threshold. Based on Anthropic's 'Harness design for long-running application development' (2026-03-24). Use when a one-line brief must become a polished, working app; not for quick fixes, small edits, or work already specified by tests."
origin: ECC-community — rewritten 2026-10-15 against the source article and the current Claude Code CLI
tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

# GAN-Style Harness

Source: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps), Prithvi Rajasekaran, Anthropic Labs, 2026-03-24.

## Core insight

Agents asked to judge their own work are pathological optimists. Tuning a **separate evaluator** to be skeptical is far easier than teaching a generator to self-critique, so generation and evaluation are split, as in a GAN. The evaluator is still an LLM and still drifts toward leniency, so it has to be calibrated (see *Evaluator*).

## First question: is the evaluator load-bearing?

The article's key finding about simplification: the evaluator only pays for itself when the task sits **beyond what the model does reliably alone**. Inside that range it is overhead.

- With current frontier models (Opus 5.5-class, 2026-10), a single strong session already handles most CRUD apps, landing pages, and refactors. Use one agent.
- Reach for this harness when the brief is big and open-ended (a whole product from one line), when visual quality is the point, or when solo runs keep shipping broken core features.

## When NOT to use

- Quick fixes, single files, refactors: a normal session.
- Work already pinned down by tests: TDD.
- Budgets under about $20: the loop will not have room to iterate.

## Architecture (current default)

```
brief (1–4 sentences)
   │
   ▼
PLANNER ── one pass ──► .gan/spec.md  (product spec + acceptance criteria)
   │
   ▼
GENERATOR ── continuous session, auto-compaction, git commits ──► running app
   │                                                ▲
   ▼                                                │ .gan/feedback-N.md
EVALUATOR ── fresh context, drives the live app ────┘
   │         in a browser, scores every criterion
   ▼
VERDICT: PASS (all criteria ≥ threshold)  or  next round (max N)
```

This is the article's **simplified** harness, the one it settled on for Opus 4.6. Two pieces of the original were dropped as models improved:

- **Context resets**: unnecessary once models stopped showing "context anxiety"; automatic compaction handles long runs.
- **Sprints and per-sprint grading**: the model decomposes work natively, so the evaluator does an end-of-run pass, repeated only if it fails.

Reintroduce sprints, with a negotiated **sprint contract** (the generator and evaluator agree on what "done" means before code is written; the article's Sprint 3 had 27 criteria), only if a run keeps failing in the same place.

## The three agents

**Planner.** Expands the brief into a product spec. Ambitious about scope, and stays at product and design level: features, user stories, visual language, AI features where they fit. It does **not** prescribe implementation. It writes the acceptance criteria the evaluator will grade against.

**Generator.** Builds feature by feature, commits to git at milestones, keeps the dev server runnable, and at the start of each round reads the latest feedback file before writing anything new. It never grades itself.

**Evaluator.** QA, not the author. It starts the app and **uses** it the way a user would: clicks every feature, fills forms, tries error states, checks API and database state. Then it scores each criterion with evidence. It only critiques; it never fixes. Each round runs in a fresh context, so it does not inherit the generator's rationalizations.

Browser tooling for the evaluator, in order of preference on this machine:
- `chrome-devtools` MCP: already installed at user level; tools `mcp__chrome-devtools__*`.
- Playwright MCP, which the article used: `claude mcp add playwright -- npx @playwright/mcp@latest`, tools `mcp__playwright__*`.
- For an APIs-only or CLI target, use `code-only` mode: tests, lint, and build instead of a browser.

## Criteria and grading

**Use hard thresholds per criterion, not a weighted average.** In the article, failing any one criterion failed the round. A weighted mean lets a broken feature hide behind pretty design.

Full-stack preset (the article's): `product depth, functionality, visual design, code quality`.
Frontend preset: `design quality, originality, craft, functionality`. Weight design quality and originality highest in the evaluator's attention; models already handle craft and functionality fairly well by default.

Score anchors (1–10):

| Score | Meaning |
|---|---|
| 1–3 | Broken, missing, or generic template / "AI slop" |
| 4–6 | Works on the happy path, unremarkable, rough edges |
| 7–8 | Distinctive and polished; edge cases handled |
| 9–10 | Could pass for senior professional work |

Default pass: **every criterion ≥ 7**.

**Calibrate the evaluator.** Put two or three short scored examples in its prompt (one 4, one 7, one 9, each with the reasons) and require evidence for every score: what was clicked and what happened. An evaluator that passes round 1 is almost always too lenient. Tighten it before trusting it.

## Running it

### A. Inside Claude Code (recommended for supervised runs)

The main session orchestrates. Spawn each role as a subagent with the Agent tool and pass work through files, never through chat:

1. Planner subagent (`model: opus`) → writes `.gan/spec.md`.
2. Generator subagent (`model: opus`) → builds; reads `.gan/feedback-N.md` if present.
3. Evaluator subagent (`model: opus`, a **new** agent each round) → writes `.gan/feedback-N.md`, whose last line is `VERDICT: PASS` or `VERDICT: FAIL`.
4. Repeat 2–3 until PASS or the iteration cap. Stop early and ask the human if scores plateau for 3 rounds.

### B. Unattended: `gan-harness.sh`

The bundled script runs the same loop on `claude -p`, with the four guards every headless run needs: `< /dev/null`, a kill timer per step, a login and quota precheck, and exit codes logged.

```bash
cd ~/my-app                                   # a git repo, or an empty dir
~/.claude/skills-library/gan-style-harness/gan-harness.sh "A kanban board for film pre-production with shot lists"
GAN_DRY_RUN=1 …/gan-harness.sh "brief"        # print the plan, run nothing
```

Artifacts go to `./.gan/`: `spec.md`, `feedback-N.md`, per-step `*.out` transcripts, and `run.log`.
Exit codes: `0` pass, `1` failed after the iteration cap, `2` usage error, `3` precheck failed (not logged in or out of quota), `4` a step crashed or timed out.

| Variable | Default | Meaning |
|---|---|---|
| `GAN_MAX_ITERATIONS` | `5` | Generator ⇄ evaluator rounds |
| `GAN_PASS_THRESHOLD` | `7` | Minimum score for **every** criterion |
| `GAN_EVAL_CRITERIA` | full-stack preset | Comma-separated criteria |
| `GAN_PLANNER_MODEL` / `GAN_GENERATOR_MODEL` / `GAN_EVALUATOR_MODEL` | `opus` | Model aliases, so they follow the newest model |
| `GAN_EVAL_MODE` | `browser` | `browser` or `code-only` |
| `GAN_BROWSER_TOOLS` | `mcp__chrome-devtools__*` | Use `mcp__playwright__*` for Playwright |
| `GAN_DEV_SERVER_CMD` / `GAN_DEV_SERVER_PORT` | `npm run dev` / `3000` | How the evaluator starts the app |
| `GAN_SKIP_PLANNER` | `0` | `1` = use an existing `.gan/spec.md` |
| `GAN_STEP_TIMEOUT` | `5400` | Seconds before a step is killed |
| `GAN_MAX_BUDGET_USD` | unset | Per-step `--max-budget-usd` ceiling |

## Models

Use the aliases `opus`, `sonnet`, and `haiku`, never pinned version numbers. As of 2026-10 they resolve to Opus 5.5, Sonnet 5.5, and Haiku 5.5. The article ran Sonnet 4.5, then Opus 4.5 (the first three-agent harness), then Opus 4.6 (the simplified one). A pinned number in a skill is how this file went stale last time.

A cheaper mix that usually holds up: `opus` for planner and evaluator, `sonnet` for the generator. Check `env | grep ANTHROPIC_MODEL` before unattended runs; a shell-profile pin overrides the model choice silently (the script unsets it).

## Re-test the harness with every new model

Every component encodes an assumption about what the model cannot do alone, and those assumptions go stale. When a new model lands:
1. Read its traces on one realistic brief.
2. Remove **one** component at a time and compare. The article's radical "cut everything" attempt failed and hid which parts mattered.
3. Keep only what is still load-bearing, and add what new capabilities make possible. For example, the article had the generator build in-app agents that drive the app's own features through tools.

"Find the simplest solution possible, and only increase complexity when needed."

## Anti-patterns

1. **Lenient evaluator**: everything passes in round 1. Add scored examples and require evidence.
2. **Evaluator fixes code**: it then grades its own fix. It only critiques.
3. **Feedback passed in chat**: the generator loses it after compaction. Always use files.
4. **Screenshot-only QA**: the evaluator must click, type, and break things.
5. **No iteration cap**: plateaus burn money. Cap rounds and stop after 3 flat rounds.
6. **Weighted-average pass**: a broken feature hides behind good design. Use per-criterion thresholds.

## What the article actually measured

| Run | Model | Time | Cost |
|---|---|---|---|
| Solo agent (retro game maker) | Opus 4.5 | 20 min | $9 |
| Full three-agent harness, same prompt | Opus 4.5 | 6 h | $200 |
| Simplified harness (browser DAW) | Opus 4.6 | 3 h 50 min | $124.70 |

The quality reporting is qualitative. The solo game's core feature did not work. The harness game was playable, but had physics bugs and one level that could not be completed. So expect "works and looks designed", not "production-ready". In the frontend experiments, evaluator scores rose over 5–15 rounds and then plateaued.

## References

- [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Martin Fowler: Harness engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
