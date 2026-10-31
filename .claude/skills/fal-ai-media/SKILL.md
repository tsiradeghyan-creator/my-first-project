---
name: fal-ai-media
description: "Use when the user asks to generate or iterate AI media through fal.ai: images, image edits, video, speech, sound effects, or model discovery/cost checks."
user-invocable: true
metadata:
  tags: [fal_ai_media, media, generation, workflow]
  version: 0.2.0
  updated: 2026-08-25
---

# fal.ai Media Generation

Route the request to fal.ai model discovery, cost estimation, generation, or result retrieval without assuming stale model IDs are still current.

## Required Reference

Before acting, read `references/full-guide.md`. The reference preserves the older detailed playbook, examples, and platform notes. Use it as historical operating knowledge, then verify any model names, pricing, platform availability, or resolution limits that may have changed.

## Operating Contract

- Use the MCP model search/find tools before relying on standing model IDs when a model name, price, parameter, or availability matters.
- Estimate cost before expensive video/audio generations or batch jobs.
- Upload only files the user provided or explicitly authorized for this workflow.
- Prefer low-cost drafts before high-fidelity final generations.

## Output Contract

- Recommended model or endpoint and why it fits.
- Required inputs and parameters.
- Estimated cost when generation is non-trivial.
- Generation status/result URL or a clear blocker.

## Verification

- Check every copied endpoint, preset, app name, model capability, duration, aspect ratio, and required input against the current tool or platform when it affects spend or success.
- For generated prompts, run a short self-lint: subject locked, action clear, camera/motion clear, style concise, constraints included, and no hidden copyrighted or private likeness dependency.
- For media jobs, confirm job status/result and report failed or partial generations plainly.

## Safety Boundaries

- Get explicit approval before spending paid credits, running batches, publishing outputs, or uploading sensitive/private media.
- Do not imitate a private person's likeness, voice, or identity without clear rights and consent.
- Avoid trademarked characters, protected brand designs, and copyrighted style requests unless the user has rights or asks for a generic alternative.
- Do not delete, overwrite, or move source media unless the user explicitly asks.

## Related Detail

- `references/full-guide.md` — archived full playbook and examples.
