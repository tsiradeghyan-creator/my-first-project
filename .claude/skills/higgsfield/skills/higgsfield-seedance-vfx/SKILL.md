---
name: higgsfield-seedance-vfx
description: "Use for Seedance video-to-video VFX prompts that preserve a real source clip while changing one requested element, environment, lighting, timing, or added effect."
user-invocable: true
metadata:
  tags: [higgsfield_seedance_vfx, media, generation, workflow]
  version: 1.1.0
  updated: 2026-08-25
---

# Higgsfield Seedance VFX

Preserve the source clip's subject, identity, performance, framing, and camera move while specifying one controlled VFX transformation.

## Required Reference

Before acting, read `references/full-guide.md`. The reference preserves the older detailed playbook, examples, and platform notes. Use it as historical operating knowledge, then verify any model names, pricing, platform availability, or resolution limits that may have changed.

## Operating Contract

- Read `references/full-guide.md` and the linked VFX references before writing the final prompt.
- Inspect the source clip when accessible; derive duration, aspect, subject, lighting, and camera motion from the actual media.
- Lock face, identity, wardrobe, performance, framing, and camera motion unless the user explicitly asks to change them.
- Verify current Seedance mode, resolution, and platform limits before presenting them as hard facts.

## Output Contract

- A plain-text English VFX prompt ready to paste.
- A specs line with duration/aspect/resolution only when verified or clearly marked as assumed.
- A short preservation checklist and any source-media blocker.

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
