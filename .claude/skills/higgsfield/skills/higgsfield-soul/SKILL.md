---
name: higgsfield-soul
description: Soul model guide for Higgsfield character, portrait, outfit, and style workflows. Use when the target engine is Soul or Soul Cinema.
metadata:
  version: 1.1.0
  architecture: progressive-disclosure
---

# Higgsfield Soul ID — Character Consistency

This skill has been converted to progressive disclosure. The complete original craft guide is preserved in `references/full-guide.md`.

## When To Use

Use this skill when the request specifically needs `higgsfield-soul` knowledge inside a Higgsfield media workflow. For broad routing, start from the parent `higgsfield` skill; for final prompt or workflow instructions, read the full guide first.

## Required Reference Loading

Read `references/full-guide.md` before producing final prompts, model instructions, workflow steps, or QA decisions.

For quick navigation, search the full guide for:

- `Workflow`
- `Prompt`
- `Reference`
- `Model`
- `Quality`
- `QA`
- `Safety`
- `Troubleshoot`

## Operating Contract

1. Identify the target output: image, video, audio, character, campaign asset, or pipeline handoff.
2. Identify the target engine/model and do not assert time-sensitive capabilities unless they are current or verified in the active Higgsfield specs.
3. Read only the relevant section of the full guide.
4. Produce a concrete artifact: prompt, prompt repair, routing decision, checklist, or workflow.
5. Include a short verification note tied to the requested artifact.

## Output Contract

Return the smallest useful complete result:

- target engine/model or "not specified",
- mode/workflow selected,
- required references or inputs,
- final prompt or actionable steps,
- QA checks and unresolved risks.

## Verification

Before final answer:

- prompt/workflow matches the selected mode,
- required references are named in order,
- model limits are not guessed when they matter,
- safety-sensitive items are flagged,
- expected output can be checked by the user or a later agent.

## Safety Boundaries

Do not spend credits, publish, modify accounts, approve rights/likeness/location/brand use, or claim a model capability as current without verification. Escalate those decisions to the user.
