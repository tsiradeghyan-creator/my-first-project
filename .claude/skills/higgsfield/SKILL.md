---
name: higgsfield
description: "Use for Higgsfield platform work: routing to sub-skills, model/preset choice, prompt refinement, Cinema Studio, Soul ID, Apps, troubleshooting, credit strategy, specs, and platform verification."
user-invocable: true
metadata:
  tags: [higgsfield, routing, workflow, verification]
  version: 3.21.0
  updated: 2026-08-25
---

# Higgsfield

This is the concise entrypoint. The older full playbook is preserved in `references/full-guide.md` and must be loaded only when this skill is actually routed.

## Required Reference

- `references/full-guide.md`

## Operating Contract

- Read `references/full-guide.md` first, then read the routed sub-skill SKILL.md files for the user's exact task.
- For prompt requests, read `skills/higgsfield-prompt/SKILL.md` plus any relevant camera, style, motion, model, Soul, or Seedance sub-skill.
- `skills/higgsfield-seedance` predates Seedance 2.5. When the model is Seedance 2.5, take prompt craft and limits from the `seedance-25-director` skill (official ByteDance 2.5 guide) and keep this skill for Higgsfield platform specifics, which may differ from Dreamina's limits.
- Verify named model parameters, enums, costs, app names, and platform limits against specs or live tools when they affect success or spend.
- Keep deliverables in the skill workspace folders when handling files.

## Output Contract

- One routing line naming the Higgsfield sub-skills used.
- The requested prompt, workflow, model choice, troubleshooting result, or plan.
- A concise verification/caveat line when platform facts may be stale.

## Verification

- Run the hard-rule checklist from `references/full-guide.md` before delivering.
- Use exact vocabulary from sub-skills/spec files rather than invented preset or parameter names.
- If execution is intended, preflight schema and cost before paid generation.

## Safety Boundaries

- Get explicit approval before spending credits, publishing, uploading private media, or changing account/platform state.
- Do not use private likeness, voice, protected identity, or rights-sensitive material without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
- Treat model names, platform features, prices, schedules, and public claims as time-sensitive.
