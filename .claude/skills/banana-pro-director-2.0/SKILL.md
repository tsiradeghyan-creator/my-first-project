---
name: banana-pro-director-2.0
description: Photoreal still-image prompt director for character builds, outfit references, character sheets, scene/environment plates, detail portraits, and outfit replacement across image engines. Use for production-grade image prompts; not for video prompts, API parameter docs, or Higgsfield account/platform questions.
metadata:
  version: 2.1.0
  architecture: progressive-disclosure
---

# Banana Pro Director 2.0 — Image Asset Builder

Produce production-grade photoreal still-image prompts while keeping the heavy craft doctrine in `references/full-guide.md`.

## When To Use

Use this skill for:

- new character face locks,
- character outfit references,
- 6-panel character sheets,
- cinematic scene plates with or without characters,
- pure environment plates,
- high-fidelity detail portraits,
- outfit replacement from two references,
- generic requests like "write me an image prompt" when the output is a still image.

Do not use it for video prompts, OpenAI image API parameters, Higgsfield account/UI questions, or platform credit troubleshooting.

## Required Reference Loading

Read `references/full-guide.md` before writing final prompts. For simple routing or quick diagnosis, use this `SKILL.md` first and open the full guide only after the target mode is known.

Search the full guide for these anchors:

- `TARGET ENGINE ADAPTER`
- `THE WORKFLOW — STRICT ORDER`
- `Mode 0 — Face lock`
- `Mode 1`
- `Mode 2`
- `Mode 3`
- `GPT-2 detail mode`
- `Outfit replacement`
- `THE CINEMA STACK`
- `FINAL QA`

## Operating Contract

1. Establish the target engine once. If unspecified, default to the existing Higgsfield fork unless the user asks for another model.
2. Classify the request into one mode:
   - Mode 0: new character face lock.
   - Mode 1: outfit reference.
   - Mode 2: 6-panel character sheet.
   - Mode 3: scene or environment plate.
   - Mode 4: detail portrait.
   - Mode 5: outfit replacement.
3. If identity/reference fidelity matters, inspect attached references and mirror the locked visual facts before writing the prompt.
4. Preserve strict pipeline order: face lock before outfit, outfit before sheet, no sheet without a base reference.
5. Keep prompt density lean. References carry visible detail; prompt text carries framing, pose, lighting, and constraints.

## Output Contract

Return:

- target engine and mode,
- required reference order,
- one copyable final prompt in a fenced code block,
- optional negative prompt or adapter notes only when the target engine uses them,
- short QA note listing identity, framing, lighting, realism, and rights checks.

## Verification

Before final answer:

- mode matches the user request,
- aspect ratio/framing are explicit,
- reference order and identity anchors are stable,
- no real brand, celebrity, actor likeness, private person, or copyrighted style is introduced without approval,
- prompt avoids plastic/CGI/rendered language unless the user requested non-photoreal style,
- any Armenian text is proper Eastern Armenian Unicode and should be overlay text unless explicitly safe for generation.

## Safety Boundaries

Do not approve spending, publishing, face/likeness rights, brand use, location use, or sensitive claims. Flag them for the user instead.
