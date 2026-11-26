#!/bin/bash
# Headless trend-scout run (global trend radar). Replaces the lost ~/.claude/trend-scout-run.sh.
# Scheduled by ~/Library/LaunchAgents/com.maghakian.trend-scout.plist (daily 08:30),
# created by scripts/setup-new-mac.sh. Manual run: bash ~/my-first-project/scripts/trend-scout-run.sh
#
# Output: ~/.memory/trends-radar.md. scripts/sync-from-laptop.sh copies it into the repo's
# memory/ at 23:40, so this run itself commits nothing.
# Permissions: acceptEdits (file edits are auto-approved inside the repo and ~/.memory),
# plus web search/fetch. Anything else that would ask is refused, because nobody answers
# prompts in a -p run.

set -uo pipefail
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export LANG="${LANG:-en_US.UTF-8}"

REPO="$HOME/my-first-project"
LOG_DIR="$HOME/Library/Logs"
LOG="$LOG_DIR/trend-scout.log"
LOCK="/tmp/trend-scout-run.lock"

mkdir -p "$LOG_DIR" "$HOME/.memory"
exec >>"$LOG" 2>&1
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

if ! mkdir "$LOCK" 2>/dev/null; then
  log "another trend-scout run is active (lock $LOCK), skipping"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

log "=== trend-scout start ==="

if ! curl -sfI -m 15 https://github.com >/dev/null; then
  log "network unreachable, skipping this run"
  exit 0
fi

command -v claude >/dev/null || { log "ERROR: claude CLI not found in PATH ($PATH)"; exit 1; }
cd "$REPO" || { log "ERROR: repo not found at $REPO"; exit 1; }

# Fresh skill text. A failed pull is not fatal: the run only writes ~/.memory.
git pull --ff-only -q origin main || log "WARNING: git pull --ff-only failed, running with the local copy"

claude -p "/trend-scout" \
  --permission-mode acceptEdits \
  --add-dir "$HOME/.memory" \
  --allowedTools "Read,Edit,Write,Glob,Grep,WebSearch,WebFetch" \
  --append-system-prompt "This is the scheduled headless trend-scout run on Tigran's Mac. Follow the trend-scout run procedure. Write only $HOME/.memory/trends-radar.md (create it if missing). Do not edit NOTES.md, BRIDGE.md or any repo file, and do not commit or push: the nightly sync copies ~/.memory into the repo. End with a 1-3 line summary of what changed."
rc=$?

log "=== trend-scout end (exit $rc) ==="
exit $rc
