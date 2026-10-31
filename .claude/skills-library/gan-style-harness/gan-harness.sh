#!/usr/bin/env bash
# gan-harness.sh — unattended Planner → Generator ⇄ Evaluator loop on `claude -p`.
# See SKILL.md next to this file for the method and every GAN_* variable.
#
#   cd <project> && gan-harness.sh "one-line brief"
#   GAN_DRY_RUN=1 gan-harness.sh "brief"      # print the plan, run nothing
#
# Exit: 0 pass · 1 failed after the iteration cap · 3 precheck failed · 4 a step crashed/timed out
# Headless guards (each one learned the hard way): stdin from /dev/null so an interactive prompt
# fails instead of waiting forever, a kill timer per step, a login/quota precheck, logged exit codes.
set -uo pipefail
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

BRIEF="${1:-}"
DIR="${GAN_PROJECT_DIR:-$PWD}"
MAX_ITER="${GAN_MAX_ITERATIONS:-5}"
THRESHOLD="${GAN_PASS_THRESHOLD:-7}"
CRITERIA="${GAN_EVAL_CRITERIA:-product depth, functionality, visual design, code quality}"
PLANNER_MODEL="${GAN_PLANNER_MODEL:-opus}"
GEN_MODEL="${GAN_GENERATOR_MODEL:-opus}"
EVAL_MODEL="${GAN_EVALUATOR_MODEL:-opus}"
EVAL_MODE="${GAN_EVAL_MODE:-browser}"
BROWSER_TOOLS="${GAN_BROWSER_TOOLS:-mcp__chrome-devtools__*}"
DEV_CMD="${GAN_DEV_SERVER_CMD:-npm run dev}"
PORT="${GAN_DEV_SERVER_PORT:-3000}"
SKIP_PLANNER="${GAN_SKIP_PLANNER:-0}"
STEP_TIMEOUT="${GAN_STEP_TIMEOUT:-5400}"
BUDGET="${GAN_MAX_BUDGET_USD:-}"
DRY="${GAN_DRY_RUN:-0}"

cd "$DIR" || { echo "gan-harness: cannot cd to $DIR" >&2; exit 4; }
H="$DIR/.gan"; mkdir -p "$H"; LOG="$H/run.log"

log() { printf '%s %s\n' "$(date '+%F %T')" "$*" | tee -a "$LOG" >&2; }

if [ -z "$BRIEF" ] && { [ "$SKIP_PLANNER" != 1 ] || [ ! -s "$H/spec.md" ]; }; then
  echo 'usage: gan-harness.sh "one-line brief"   (or GAN_SKIP_PLANNER=1 with an existing .gan/spec.md)' >&2
  exit 2
fi

# A shell-profile ANTHROPIC_MODEL silently overrides model choice; the --model flags below decide.
if [ -n "${ANTHROPIC_MODEL:-}" ]; then log "unsetting ANTHROPIC_MODEL=$ANTHROPIC_MODEL for this run"; unset ANTHROPIC_MODEL; fi

# with_timer SECONDS CMD... — run CMD in the background, kill it after SECONDS, return its exit code.
with_timer() {
  local secs=$1; shift
  "$@" < /dev/null &
  local cpid=$!
  ( sleep "$secs"; kill -TERM "$cpid" 2>/dev/null ) 2>/dev/null &
  local tpid=$!
  wait "$cpid" 2>/dev/null; local rc=$?
  # the sleep first, or it outlives its parent; reaping the timer here keeps bash's "Terminated" notice out of the log
  { pkill -P "$tpid"; kill -TERM "$tpid"; wait "$tpid"; } 2>/dev/null
  return "$rc"
}

# step LABEL MODEL TOOLS PROMPT — one claude -p call with the guards; transcript in .gan/LABEL.out
step() {
  local label=$1 model=$2 tools=$3 prompt=$4
  local args=(-p "$prompt" --model "$model" --permission-mode acceptEdits --allowedTools "$tools")
  [ -n "$BUDGET" ] && args+=(--max-budget-usd "$BUDGET")
  if [ "$DRY" = 1 ]; then log "DRY $label · model=$model · tools=$tools"; return 0; fi
  log "start $label (model=$model)"
  with_timer "$STEP_TIMEOUT" claude "${args[@]}" >> "$H/$label.out" 2>&1
  local rc=$?
  log "end   $label (exit=$rc)"
  [ "$rc" -eq 0 ] || { log "step $label failed — see $H/$label.out"; exit 4; }
}

if [ "$DRY" != 1 ]; then
  if ! with_timer 90 claude -p "Reply with exactly: ok" --model haiku --max-turns 1 > /dev/null 2>&1; then
    log "precheck failed: not logged in, out of quota, or claude missing — nothing was run"
    exit 3
  fi
fi

log "=== run start · dir=$DIR · max=$MAX_ITER · threshold=$THRESHOLD · mode=$EVAL_MODE"

BUILD_TOOLS="Read,Write,Edit,Glob,Grep,Bash"
if [ "$EVAL_MODE" = browser ]; then
  EVAL_TOOLS="Read,Write,Glob,Grep,Bash,$BROWSER_TOOLS"
  RUN_HINT="Make sure \`$DEV_CMD\` starts the app on port $PORT."
  HOW_TO_TEST="Start the app with \`$DEV_CMD\` in the background (port $PORT) if it is not already running, then use it through the browser tools the way a user would: open every page, click every feature named in the acceptance criteria, fill forms with good and bad input, try error and empty states, reload to check persistence. Check API responses and stored data where the spec implies them. Stop any server you started before you finish."
else
  EVAL_TOOLS="Read,Write,Glob,Grep,Bash"
  RUN_HINT="Make sure the build and tests run from the command line, and say how in the README."
  HOW_TO_TEST="Run the project's build, lint and test commands, exercise the CLI or API directly with realistic and malformed input, and read the code for each acceptance criterion."
fi

if [ "$SKIP_PLANNER" != 1 ]; then
  step plan "$PLANNER_MODEL" "Read,Write,Glob,Grep" \
"You are the PLANNER in a planner / generator / evaluator harness. Expand the brief below into a product spec and write it to .gan/spec.md.
Be ambitious about scope. Stay at product and design level: features, user stories, visual language, and AI features where they genuinely fit. Do NOT prescribe implementation details; the generator decides those.
End the spec with '## Acceptance criteria', grouped under exactly these criteria: $CRITERIA. Give each group concrete, testable checks the evaluator can verify by using the app.
Brief: $BRIEF"
fi

for i in $(seq 1 "$MAX_ITER"); do
  prev=$((i - 1))
  if [ "$prev" -ge 1 ] && [ -f "$H/feedback-$prev.md" ]; then
    FEEDBACK="Read .gan/feedback-$prev.md first. Fix every issue it lists before adding anything new; the evaluator will re-test all of them."
  else
    FEEDBACK="This is the first build round."
  fi
  step "gen-$i" "$GEN_MODEL" "$BUILD_TOOLS" \
"You are the GENERATOR in a planner / generator / evaluator harness. Read .gan/spec.md and build the app it describes in the current directory. $FEEDBACK
Work feature by feature and commit to git at milestones (run 'git init' first if there is no repository). $RUN_HINT Do not grade your own work; a separate evaluator will. Finish by writing a short list of what changed this round to .gan/gen-$i.md."

  step "eval-$i" "$EVAL_MODEL" "$EVAL_TOOLS" \
"You are the EVALUATOR, a strict QA engineer who did not write this app. Grade it against the acceptance criteria in .gan/spec.md. $HOW_TO_TEST
Score each of these criteria from 1 to 10: $CRITERIA. Anchors: 1-3 broken or generic template, 4-6 happy path only and unremarkable, 7-8 distinctive and polished with edge cases handled, 9-10 senior professional work. Back every score with evidence: what you did and what happened. Models grading model-built work drift toward leniency, so when unsure, score lower.
Do NOT change any project file and do NOT suggest code. List concrete problems, worst first, each with the steps that reproduce it.
Write everything to .gan/feedback-$i.md. Its LAST line must be exactly 'VERDICT: PASS' if every criterion scored $THRESHOLD or higher, otherwise exactly 'VERDICT: FAIL'."

  [ "$DRY" = 1 ] && continue
  verdict="$(grep -oE 'VERDICT:[[:space:]]*(PASS|FAIL)' "$H/feedback-$i.md" 2>/dev/null | tail -n 1 | tr -d '[:space:]')"
  log "round $i verdict: ${verdict:-missing}"
  if [ "$verdict" = "VERDICT:PASS" ]; then log "=== PASS after $i round(s)"; exit 0; fi
done

[ "$DRY" = 1 ] && { log "=== dry run complete"; exit 0; }
log "=== FAIL: no pass after $MAX_ITER round(s) — read .gan/feedback-$MAX_ITER.md"
exit 1
