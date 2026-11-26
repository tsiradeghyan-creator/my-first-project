#!/bin/bash
# ARCHIVED 2026-11-26: Tigran works cloud-only now; kept only in case a Mac is used again. See CLAUDE.md.
# Headless zavod-scout run (competitive self-improvement of the content-zavod stations).
# Replaces the lost runner from the old Mac. Scheduled by
# ~/Library/LaunchAgents/com.maghakian.zavod-scout.plist (every 3 days, StartInterval 259200),
# created by scripts/setup-new-mac.sh. Manual run: bash ~/my-first-project/scripts/zavod-scout-run.sh
#
# Station edits go to the zavod-om repo (~/zavod-om/skills/zavod-craft/) and are pushed there;
# the scoreboard lives in this repo (.claude/skills/zavod-scout/scoreboard.md).
# Permissions: acceptEdits (file edits auto-approved in the repo and ~/zavod-om), plus web
# search/fetch, git (to push both repos), python3 (glyph gate) and `npx skills find`.
# Anything else that would ask is refused, because nobody answers prompts in a -p run.

set -uo pipefail
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export LANG="${LANG:-en_US.UTF-8}"

REPO="$HOME/my-first-project"
ZAVOD="$HOME/zavod-om"
LOG_DIR="$HOME/Library/Logs"
LOG="$LOG_DIR/zavod-scout.log"
LOCK="/tmp/zavod-scout-run.lock"

mkdir -p "$LOG_DIR"
exec >>"$LOG" 2>&1
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

if ! mkdir "$LOCK" 2>/dev/null; then
  log "another zavod-scout run is active (lock $LOCK), skipping"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

log "=== zavod-scout start ==="

if ! curl -sfI -m 15 https://github.com >/dev/null; then
  log "network unreachable, skipping this run"
  exit 0
fi

command -v claude >/dev/null || { log "ERROR: claude CLI not found in PATH ($PATH)"; exit 1; }
cd "$REPO" || { log "ERROR: repo not found at $REPO"; exit 1; }
[ -d "$ZAVOD/.git" ] || { log "ERROR: zavod-om not cloned at $ZAVOD (station files live there)"; exit 1; }

# Both repos must be current before editing, or the push at the end will be rejected.
git pull --ff-only -q origin main || { log "ERROR: git pull --ff-only failed in $REPO"; exit 1; }
git -C "$ZAVOD" pull --ff-only -q || { log "ERROR: git pull --ff-only failed in $ZAVOD"; exit 1; }

EXTRA_DIRS=(--add-dir "$ZAVOD")
# The wiki log (append-only) if the Obsidian vault is outside ~/Documents.
[ -d "$HOME/ObsidianVault/Claude" ] && EXTRA_DIRS+=(--add-dir "$HOME/ObsidianVault/Claude")

claude -p "/zavod-scout" \
  --permission-mode acceptEdits \
  "${EXTRA_DIRS[@]}" \
  --allowedTools "Read,Edit,Write,Glob,Grep,WebSearch,WebFetch,Bash(git *),Bash(python3 *),Bash(npx skills find *)" \
  --append-system-prompt "This is the scheduled headless zavod-scout run on Tigran's Mac (every 3 days). Follow the zavod-scout 3-day loop. Edit station files only in $ZAVOD/skills/zavod-craft/, then commit and push them in $ZAVOD. In $REPO, update .claude/skills/zavod-scout/scoreboard.md, add a short NOTES.md entry (side: VS Code, scheduled zavod-scout), commit only those two files and push to main. Never edit .claude/skills/content-zavod/ in $REPO. Put escalations (money, rights, brand) in the run summary as proposals; do not apply them."
rc=$?

log "=== zavod-scout end (exit $rc) ==="
exit $rc
