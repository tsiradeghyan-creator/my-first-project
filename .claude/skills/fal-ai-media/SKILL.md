---
name: fal-ai-media
description: "Use when the user asks to generate or iterate AI media through fal.ai: images, image edits, video, speech, sound effects, or model discovery/cost checks."
user-invocable: true
metadata:
  tags: [fal_ai_media, media, generation, workflow]
  version: 0.3.0
  updated: 2026-11-26
---

# fal.ai Media Generation

Route the request to fal.ai model discovery, cost estimation, generation, or result retrieval without assuming stale model IDs are still current.

## Required Reference

Before acting, read `references/full-guide.md`. It holds the MCP setup, model ids and parameters checked on fal.ai on 2026-11-26 (Seedance 2.5 as the default video model, Kling v3, Veo 3.1, Nano Banana 2 / Pro), and examples. Verify any model names, pricing, platform availability, or resolution limits that may have changed since.

## Film-Crew First

Before writing a prompt, run `film-crew` (single-shot mode for one shot, full mode for several) per CLAUDE.md, and take its plan as input. If a film-crew plan already exists, use it. The model skill (`seedance-25-director`, `banana-pro-director-2.0`, `cinema-worldbuilder-pro-2.0`…) writes the final prompt text; this skill sends it to fal.

## Which MCP Server

- Official hosted fal MCP: `https://mcp.fal.ai/mcp-relay` (OAuth sign-in, no API key). Tools: `search_models`, `get_model_schema`, `get_pricing`, `search_docs`, `recommend_model`, `run_model`, `submit_job`, `check_job`, `get_job_result`, `cancel_job`, `upload_file`.
- Third-party `npx fal-ai-mcp-server` (legacy): tools `search`, `find`, `models`, `generate`, `result`, `status`, `cancel`, `upload`, `estimate_cost`… These names apply only if that package is the one installed.
- Check the connected tool list first; the guide has a name-to-name map.

## Operating Contract

- Use the MCP model search and schema tools (`search_models` / `get_model_schema`, or `search` / `find` on the third-party server) before relying on standing model IDs when a model name, price, parameter, or availability matters.
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
