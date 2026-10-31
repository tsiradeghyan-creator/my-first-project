---
name: autogpt-agent
description: AutoGPT-style autonomous goal decomposition and execution loop. Use when a goal should be broken into self-directed steps rather than handled turn by turn.
---

# AutoGPT Agent Skill

## Purpose

Autonomous multi-step agent execution inspired by AutoGPT. Given a high-level goal, this skill breaks it into subtasks, executes them with available tools, reflects on results, and iterates until the goal is achieved — all with minimal user intervention.

## When to Invoke

Invoke this skill when the user provides a **high-level goal** that requires:
- Multiple sequential steps to complete
- Autonomous decision-making between steps
- Tool use (web search, file ops, code execution, API calls)
- Self-correction based on intermediate results

Trigger phrases: "do this autonomously", "autogpt mode", "agent mode", "do it step by step automatically", "run as agent", or any large goal with no clear single-step solution.

---

## Agent Loop (THINK → PLAN → ACT → REFLECT → REPEAT)

When this skill is active, follow this loop strictly:

### Phase 1: THINK
Read the goal carefully. Ask yourself:
- What is the final desired state?
- What information do I already have?
- What information do I need to gather first?

Output a short **Goal Summary** (1-2 sentences, no fluff).

### Phase 2: PLAN
Break the goal into **numbered subtasks**. Each subtask must be:
- Atomic (single action)
- Verifiable (has a clear done condition)
- Ordered (dependencies respected)

Format:
```
PLAN:
1. [action] — [why]
2. [action] — [why]
...
N. [action] — [why]
```

Keep plans to 3–10 steps. If the goal is vague, add a first step: "Clarify requirement by [X]".

### Phase 3: ACT
Execute each step using available tools:

| Need | Tool to Use |
|------|------------|
| Search the web | WebSearch or WebFetch |
| Read/write files | Read, Write, Edit |
| Run code | Bash |
| Find files | Glob, Grep |
| Spawn sub-research | Agent (Explore subagent) |

Before each action, print:
```
[STEP N/TOTAL] action description
```

After each action, print a one-line result summary.

### Phase 4: REFLECT
After completing a step, ask:
- Did the step succeed?
- Did the result change what the next step should be?
- Is the overall plan still valid, or does it need adjustment?

If the plan needs adjustment, reprint the updated plan with a note:
```
PLAN UPDATED: [reason]
```

### Phase 5: REPEAT
Continue the loop until:
- All steps are marked done ✓
- Or the goal is fully achieved

Final output:
```
GOAL ACHIEVED: [one-sentence summary of what was accomplished]
```

---

## Memory System

### Short-term Memory (within session)
Maintain a running **Agent Context Block** in your responses:

```
--- AGENT CONTEXT ---
Goal: [original goal]
Steps done: N/M
Current step: [step description]
Key findings: [bullet list of important facts discovered]
---
```

Update this block at each iteration.

### Long-term Memory (persist across sessions)
When the agent completes a significant task, save a memory entry using the memory system at `~/.claude/projects/-Users-apple/memory/`. Save:
- What goal was accomplished
- Key decisions made
- Tools that worked well or failed
- Any reusable outputs (file paths, data)

---

## Block System (Available Capabilities)

Inspired by AutoGPT's block architecture. Use these capability categories:

### Web & Research Blocks
- `WebSearch` — search the web for information
- `WebFetch` — fetch and parse a specific URL
- Scrape structured data from pages

### File & Code Blocks
- `Read` / `Write` / `Edit` — file operations
- `Bash` — run shell commands, scripts, code
- `Glob` / `Grep` — search codebases

### AI & Reasoning Blocks
- `Agent` (Explore) — delegate sub-research tasks
- `Agent` (general-purpose) — delegate complex multi-tool subtasks
- Structured output parsing from LLM responses

### Control Flow Blocks
- Conditional branching (if step fails → alternative path)
- Looping (retry up to 3× on failure)
- Human-in-the-loop (ask user when genuinely blocked)

---

## Error Handling & Retry Logic

1. **Tool failure**: Retry once with adjusted parameters. If it fails again, try an alternative tool.
2. **Ambiguous result**: Mark step as "partial" and proceed with best available info.
3. **Blocked**: If a step is impossible (permission denied, resource unavailable), skip it, note it in the context block, and continue.
4. **Truly stuck**: After 2 failed retries, pause and ask the user one targeted question.

Never silently fail. Always report what happened.

---

## Human-in-the-Loop Checkpoints

Pause and ask the user before:
- Deleting files or making destructive changes
- Pushing to git remotes
- Sending messages or posting content externally
- Spending more than ~5 steps on a single sub-problem

Format:
```
CHECKPOINT: I'm about to [action]. Shall I proceed? (yes/no)
```

---

## Output Format

Structure all agent responses like this:

```
GOAL: [restate goal]

PLAN:
1. ...
2. ...

[STEP 1/N] ...
→ Result: ...

[STEP 2/N] ...
→ Result: ...

...

GOAL ACHIEVED: [summary]
```

Keep each step output tight — one action, one result line. Expand only when the result itself is complex data that the user needs to see.

---

## Example Usage

**User:** "Research the top 5 open-source agent frameworks, compare them, and save a summary to ~/agent-research.md"

**Agent Loop:**
1. THINK: Need to find, compare, and write about 5 OSS agent frameworks
2. PLAN: Search → Fetch details → Compare → Write file
3. ACT: Execute searches, fetch key pages, synthesize, write
4. REFLECT: All data gathered? Comparison complete? File written?
5. DONE: Report file location

---

## Notes

- This skill is inspired by [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) — specifically its autonomous agent loop, block-based tool system, memory architecture, and multi-step task decomposition.
- Unlike AutoGPT's full platform, this skill runs entirely within Claude Code using native tools.
- The skill does NOT require Docker, a separate server, or any installation — it runs in-context.
