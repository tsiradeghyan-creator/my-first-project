---
name: higgsfield-workspaces
description: "Use when the user is unsure which Higgsfield workspace fits a task, including Cinema Studio, Lipsync Studio, Draw/Sketch to Video, trend workspaces, Click to Ad, and Audio."
user-invocable: true
metadata:
  tags: [higgsfield_workspaces, routing, verification, workflow]
  version: 1.3.0
  updated: 2026-08-25
---

# Higgsfield Workspaces

This concise entrypoint routes the task and defines the contract. The complete older playbook is preserved in `references/full-guide.md`.

## Required Reference

Read `references/full-guide.md` before producing user-facing output from this skill.

## Operating Contract

- Read `references/full-guide.md` before recommending a workspace.
- Choose by production problem before choosing a model.
- Verify current workspace names, plan limits, and UI availability when the user is about to spend time or credits.

## Output Contract

- Recommended workspace and one backup option.
- Inputs the user needs to prepare.
- A short handoff to the next Higgsfield sub-skill when needed.

## Verification

- Confirm routed references/templates/tools exist before relying on them.
- Verify time-sensitive model, platform, pricing, workspace, or UI facts before presenting them as current.
- Run the smallest useful smoke check, lint, or self-check available for the workflow.

## Safety Boundaries

- Get explicit approval before spending credits, publishing, uploading sensitive/private media, or changing account state.
- Do not use private likeness, voice, identity, confidential business context, or copyrighted material without clear authorization.
- Do not delete, overwrite, or move user files unless explicitly asked.
