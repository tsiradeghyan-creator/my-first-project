#!/bin/bash
# ARCHIVED 2026-11-26: Tigran works cloud-only now; kept only in case a Mac is used again. See CLAUDE.md.
# Daily laptop -> GitHub sync for the shared workspace (VS Code <-> Cloud).
# Copies ~/.memory, ~/.claude/skills-library and the zavod canon snapshots into
# this repo, scans the staged diff for secrets, and pushes to main only if
# something changed. Scheduled by ~/Library/LaunchAgents/com.tigran.sync-laptop.plist.

set -uo pipefail
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

REPO="$HOME/my-first-project"
LOCK="/tmp/sync-laptop.lock"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
fail() { log "ERROR: $*"; exit 1; }

if ! mkdir "$LOCK" 2>/dev/null; then
  log "another sync is running (lock $LOCK), skipping"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

log "=== sync start ==="

# Network precheck: the Mac may wake without Wi-Fi; skip quietly instead of failing.
if ! curl -sfI -m 15 https://github.com >/dev/null; then
  log "github.com unreachable, skipping this run"
  exit 0
fi

cd "$REPO" || fail "repo not found at $REPO"
git pull --ff-only -q origin main || fail "git pull failed (diverged or no access)"

COMMON_EXCLUDES=(--exclude='.git/' --exclude='.env' --exclude='.env.*' --exclude='*.key' --exclude='*.pem'
                 --exclude='node_modules/' --exclude='__pycache__/' --exclude='.DS_Store' --max-size=10m)

# Guard: a missing or empty source must never wipe the repo copy through --delete
# (for example on a new Mac before ~/.memory is restored). Each block below is
# skipped with a log line when its source looks empty.
count_md() { find "$1" -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' '; }
not_empty() { [ -d "$1" ] && [ -n "$(ls -A "$1" 2>/dev/null)" ]; }

# 1. Memory: markdown only (the *.log files are run logs).
MEM_MD=$(count_md "$HOME/.memory")
if [ "$MEM_MD" -ge 2 ]; then
  mkdir -p memory
  rsync -a --delete --include='*.md' --exclude='*' "$HOME/.memory/" memory/ || fail "rsync memory"
else
  log "SKIP memory: ~/.memory is missing or has only $MEM_MD .md file(s); repo memory/ left as is"
fi

# 2. Skills library, without ruflo/ (third-party clone, 196 MB) and two docs whose
#    fake example keys trip the secret scan.
if not_empty "$HOME/.claude/skills-library"; then
  mkdir -p .claude/skills-library
  rsync -a --delete "${COMMON_EXCLUDES[@]}" \
    --exclude='/ruflo/' \
    --exclude='/springboot-security/SKILL.md' \
    --exclude='/composio/rules/setup-api-keys.md' \
    "$HOME/.claude/skills-library/" .claude/skills-library/ || fail "rsync skills-library"
else
  log "SKIP skills-library: ~/.claude/skills-library is missing or empty; repo copy left as is"
fi

# 3. Zavod canon snapshots (canon lives in ~/zavod-om). Needs SKILL.md in both
#    source folders, so an empty or half-cloned canon never wipes the snapshots.
CANON="$HOME/zavod-om/skills/zavod-craft"
if [ -d "$CANON" ] && { [ ! -f "$CANON/SKILL.md" ] || [ ! -f "$CANON/gpt-image-prompting/SKILL.md" ]; }; then
  log "SKIP zavod canon: $CANON has no SKILL.md (or no gpt-image-prompting/SKILL.md); snapshots left as is"
elif [ -d "$CANON" ]; then
  rsync -a --delete "${COMMON_EXCLUDES[@]}" "$CANON/" .claude/skills/content-zavod/ || fail "rsync content-zavod"
  rsync -a --delete "${COMMON_EXCLUDES[@]}" "$CANON/gpt-image-prompting/" .claude/skills/gpt-image-prompting/ || fail "rsync gpt-image-prompting"
else
  log "WARNING: $CANON missing, zavod snapshots not refreshed"
fi

PATHS=(memory .claude/skills-library .claude/skills/content-zavod .claude/skills/gpt-image-prompting)
git add -A -- "${PATHS[@]}"

if git diff --cached --quiet -- "${PATHS[@]}"; then
  log "nothing changed"
  exit 0
fi

git diff --cached --stat -- "${PATHS[@]}" | tail -1

HITS=$(git diff --cached -U0 --no-color -- "${PATHS[@]}" | python3 -I scripts/secret-scan.py --diff)
if [ -n "$HITS" ]; then
  git reset -q -- "${PATHS[@]}"
  log "secret scan found possible secrets, commit aborted:"
  echo "$HITS"
  exit 1
fi

git commit -q -m "Sync from laptop $(date '+%Y-%m-%d')" -- "${PATHS[@]}" || fail "git commit"
git push -q origin main || fail "git push"
log "pushed $(git rev-parse --short HEAD)"
