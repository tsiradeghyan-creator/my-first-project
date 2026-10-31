---
name: eval-harness
description: Eval-driven development for AI work — define pass/fail criteria before building, then measure code changes, prompts, skills and agents with code, rule, model and human graders and pass@k / pass^k metrics. Use when setting success criteria for an agent task, checking that a skill or prompt change did not regress, comparing models, or deciding whether a skill earns its place versus no skill at all.
origin: ECC — revised 2026-10-15 (removed `/eval` commands that never existed; added skill and prompt evals with a no-skill baseline)
tools: Read, Write, Edit, Bash, Grep, Glob
---

# Eval Harness

Evals are the unit tests of AI work. Write them **before** the change, run them often, and keep them in the repo next to what they test.

## When to activate

- Defining what "done" means for an agent task before it starts
- Changing a prompt, skill, or agent and needing proof it did not get worse
- Choosing between models, or checking that a new model did not break an old workflow
- Deciding whether a skill actually helps (compare with versus without it)

## Eval types

**Capability evals**: can it now do something it could not before?

```markdown
[CAPABILITY EVAL: feature-name]
Task: what should be accomplished
Success criteria:
  - [ ] criterion 1
  - [ ] criterion 2
Expected output: description
```

**Regression evals**: does everything that worked still work?

```markdown
[REGRESSION EVAL: feature-name]
Baseline: git SHA or checkpoint
Tests: existing-1 PASS/FAIL · existing-2 PASS/FAIL
Result: X/Y passed (previously Y/Y)
```

## Graders: prefer the cheapest one that is reliable

| Grader | Use for | Example |
|---|---|---|
| Code | Anything checkable by program | `grep -q "export function handleAuth" src/auth.ts`, `npm test`, `npm run build`, JSON schema validation |
| Rule | Format and constraint checks | Regex on output, length limits, "contains no Latin letters inside Armenian words" |
| Model (LLM judge) | Open-ended quality | Rubric prompt below; a small model (`haiku`) is usually enough |
| Human | Security, taste, anything ambiguous or high-stakes | Flag with risk level; never auto-approve security |

Model-grader rubric template:

```markdown
You are grading, not writing. Do not rewrite the output.
Criteria (score each 1–5 with one line of evidence):
1. Solves the stated task
2. <domain criterion>
3. <domain criterion>
Return JSON: {"scores": {...}, "pass": true|false, "reason": "..."}
Pass only if every criterion ≥ 4.
```

Make a model grader trustworthy:
- Include one good and one bad scored example.
- Grade **blind**: the judge should not know which variant (old or new, with or without the skill) produced the output.
- Spot-check about 10% of its verdicts by hand. A judge that never fails anything is broken.

## Metrics

- **pass@k**: at least one success in k attempts. pass@1 is direct reliability, pass@3 is reliability with retries.
- **pass^k**: all k attempts succeed. This is the stability bar for anything that runs unattended.

Default thresholds: capability evals pass@3 ≥ 0.90; regression evals on release-critical paths pass^3 = 1.00.

Track **cost and latency** next to the pass rate. A change that adds 2 points of quality at 3× the cost is a decision for the human, not an automatic win.

## Workflow

1. **Define** before building: write `evals/<feature>.md` with the capability and regression evals and the thresholds.
2. **Implement.**
3. **Evaluate**: run each eval k times and record PASS or FAIL per run in `evals/<feature>.log` (date, git SHA, model, result, cost).
4. **Report** in this shape:

```
EVAL REPORT: feature-xyz        2026-10-15 · abc1234 · model=opus
Capability   create-user PASS (pass@1) · validate-email PASS (pass@2)    2/2
Regression   login-flow PASS · logout-flow PASS                          2/2  (pass^3)
pass@1 50% · pass@3 100% · cost $0.42 · median latency 38 s
Status: READY FOR REVIEW
```

Layout:

```
evals/
  <feature>.md        # definition
  <feature>.log       # run history
  baseline.json       # regression baselines (expected outputs or scores)
  results/<date>/     # raw outputs, kept for blind re-grading
```

## Evaluating skills, prompts and agents

A skill is only worth its context cost if it beats **no skill**. Always run a baseline arm:

1. Pick 5–10 realistic prompts the skill should handle, plus 2–3 it should **not** trigger on.
2. Run each prompt k = 3 times with the skill, then the same with it removed (or with the previous version).
3. Grade both arms blind with the same graders.
4. Keep the change only if the with-skill arm wins on the criteria that matter, at acceptable cost. Note the delta in the skill's changelog.

Headless runs for this use `claude -p "<prompt>" --model <alias> < /dev/null` with a kill timer, so one hung run cannot stall the suite.

**Tooling**
- `claude plugin eval` runs eval cases (`evals/**/case.yaml`, or `prompt.md` plus `graders/*.md`) against a plugin or skills directory. It runs a no-plugin baseline arm, uses `haiku` as the default judge, and can cap spend with `--max-cost-usd`. It was **early access** and not enabled on this account on 2026-10-15; check again with `claude plugin eval --help` before relying on it.
- Local precedent: `~/zavod-om/tests/eval/` already has golden scenarios, golden outputs, and a replay harness with deterministic (exact match) and stochastic (threshold) modes. Extend that instead of starting a parallel system for zavod skills.

## Anti-patterns

- Overfitting prompts or skills to the exact eval examples. Keep a held-out set.
- Measuring only happy paths.
- A judge that knows which variant it is grading.
- Flaky graders in a release gate.
- Chasing pass rate while cost and latency drift.
- Evals that take so long nobody runs them.

## Worked example: adding authentication

```markdown
## EVAL: add-authentication
Capability
- [ ] register with email and password
- [ ] log in with valid credentials; invalid ones rejected with a clear error
- [ ] session survives a reload; logout clears it
Regression
- [ ] public routes still reachable · API responses unchanged · schema compatible
Graders: code (tests and a curl script) for all; human review of the session and cookie flags
Thresholds: capability pass@3 ≥ 0.9 · regression pass^3 = 1.0
```

Report → `Capability 5/5 (pass@3 100%) · Regression 3/3 (pass^3 100%) · Status: SHIP IT`
