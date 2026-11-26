#!/usr/bin/env bash
# Restore Tigran's workspace on a new Mac: tools, logins, repos, ~/.memory,
# skills library, the scheduled LaunchAgents, and the key / MCP checklist.
#
# Usage:
#   bash scripts/setup-new-mac.sh                       # dry run: prints what it would do
#   bash scripts/setup-new-mac.sh --apply               # does it
#   bash scripts/setup-new-mac.sh --apply --with-cli-anything   # also runs install-cli-anything.sh
#
# Safe to run again: it skips what is already in place and never overwrites an existing
# file without keeping a .bak copy. It never writes API keys anywhere; it only prints
# where they go. Written for macOS /bin/bash 3.2 (no bash-4 features).
# Checklist in plain English: scripts/NEW-MAC.md.

# Literal "~/..." and "$(...)" appear only in printed messages, on purpose:
# shellcheck disable=SC2088,SC2016
set -euo pipefail

# ---------------------------------------------------------------- options
APPLY=0
WITH_CLI_ANYTHING=0
for arg in "$@"; do
  case "$arg" in
    --apply) APPLY=1 ;;
    --with-cli-anything) WITH_CLI_ANYTHING=1 ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg (use --apply, --with-cli-anything, --help)" >&2; exit 2 ;;
  esac
done

GH_OWNER="tsiradeghyan-creator"
REPO="$HOME/my-first-project"
ZAVOD="$HOME/zavod-om"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"   # the checkout this script runs from
AGENTS_DIR="$HOME/Library/LaunchAgents"
LOG_DIR="$HOME/Library/Logs"
BACKUP_DIR="$HOME/.setup-new-mac-backups"   # .bak copies of replaced plists (kept out of LaunchAgents)
STAMP="$(date '+%Y%m%d-%H%M%S')"
UID_N="$(id -u)"

# ---------------------------------------------------------------- helpers
say()  { printf '%s\n' "$*"; }
head1() { printf '\n== %s\n' "$*"; }
note() { printf '   %s\n' "$*"; }
warn() { printf '   WARNING: %s\n' "$*"; }

# run CMD...: dry run prints it, --apply prints and runs it.
run() {
  if [ "$APPLY" = 1 ]; then
    printf '   + %s\n' "$*"
    "$@"
  else
    printf '   [dry-run] %s\n' "$*"
  fi
}

# Status table rows (parallel arrays; bash 3.2 has no associative arrays).
ST_NAME=(); ST_STATE=(); ST_NOTE=()
status() { ST_NAME+=("$1"); ST_STATE+=("$2"); ST_NOTE+=("${3:-}"); }

# Keep a .bak copy of FILE before it is replaced: FILE.bak, or FILE.bak.<stamp> if that exists.
backup_file() {
  local f="$1" dest="${2:-}"
  [ -e "$f" ] || return 0
  if [ -z "$dest" ]; then
    dest="$f.bak"
    if [ -e "$dest" ]; then dest="$f.bak.$STAMP"; fi
  fi
  run cp -p "$f" "$dest"
}

# Copy SRC to DST; if DST exists and differs, back it up first; if identical, do nothing.
safe_copy() {
  local src="$1" dst="$2"
  if [ -e "$dst" ]; then
    if cmp -s "$src" "$dst"; then
      note "unchanged: $dst"
      return 0
    fi
    backup_file "$dst"
  fi
  run cp -p "$src" "$dst"
}

count_md() { { find "$1" -maxdepth 1 -type f -name '*.md' 2>/dev/null || true; } | wc -l | tr -d ' '; }
dir_empty() { [ ! -d "$1" ] || [ -z "$(ls -A "$1" 2>/dev/null)" ]; }
xml_escape() { printf '%s' "$1" | sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'; }

if [ "$(uname -s)" != "Darwin" ]; then
  say "This script is for macOS. Detected $(uname -s): continuing in dry-run mode only."
  APPLY=0
fi

if [ "$APPLY" = 1 ]; then
  say "MODE: APPLY (changes will be made)"
else
  say "MODE: DRY RUN (nothing is changed; run again with --apply to do it)"
fi
say "Target home: $HOME"

# ================================================================ 1. Homebrew + formulae
head1 "1. Homebrew and command-line tools"
BREW=""
for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do
  if [ -x "$b" ]; then BREW="$b"; break; fi
done
if [ -z "$BREW" ] && command -v brew >/dev/null 2>&1; then BREW="$(command -v brew)"; fi

if [ -n "$BREW" ]; then
  note "Homebrew found: $BREW"
  status "Homebrew" "ok" "$BREW"
else
  note "Homebrew not found. Official installer (asks for your Mac password):"
  note '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  if [ "$APPLY" = 1 ]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do
      if [ -x "$b" ]; then BREW="$b"; break; fi
    done
    if [ -n "$BREW" ]; then
      status "Homebrew" "installed" "$BREW"
      note "Add brew to your shell (once): echo 'eval \"\$($BREW shellenv)\"' >> ~/.zprofile"
    else
      status "Homebrew" "FAILED" "installer did not leave a brew binary"
    fi
  else
    status "Homebrew" "to install" "Apple Silicon: /opt/homebrew (old Mac used /usr/local)"
  fi
fi

if [ -n "$BREW" ]; then
  eval "$("$BREW" shellenv)"
  BREW_PREFIX="$("$BREW" --prefix)"
else
  if [ "$(uname -m)" = "arm64" ]; then BREW_PREFIX="/opt/homebrew"; else BREW_PREFIX="/usr/local"; fi
fi
export PATH="$HOME/.local/bin:$BREW_PREFIX/bin:$PATH"

FORMULAE="git node python rsync ffmpeg gh uv"
MISSING=""
for f in $FORMULAE; do
  if [ -n "$BREW" ] && "$BREW" ls --versions "$f" >/dev/null 2>&1; then
    note "installed: $f"
  else
    MISSING="$MISSING $f"
  fi
done
MISSING="${MISSING# }"
if [ -z "$MISSING" ]; then
  status "brew formulae" "ok" "$FORMULAE"
else
  note "to install: $MISSING"
  if [ -n "$BREW" ]; then
    # shellcheck disable=SC2086  # word splitting of the formula list is intended
    if run "$BREW" install $MISSING; then
      if [ "$APPLY" = 1 ]; then status "brew formulae" "installed" "$MISSING"; else status "brew formulae" "to install" "$MISSING"; fi
    else
      status "brew formulae" "FAILED" "$MISSING"
    fi
  else
    note "[dry-run] brew install $MISSING   (after Homebrew is installed)"
    status "brew formulae" "to install" "$MISSING"
  fi
fi

# Absolute python3 for the LaunchAgents (launchd has no shell PATH).
PY=""
if [ -x "$BREW_PREFIX/bin/python3" ]; then
  PY="$BREW_PREFIX/bin/python3"
elif command -v python3 >/dev/null 2>&1 && [ "$(command -v python3)" != "/usr/bin/python3" ]; then
  PY="$(command -v python3)"
fi
if [ -n "$PY" ]; then
  note "python3 for scheduled jobs: $PY ($("$PY" --version 2>&1))"
else
  PY="$BREW_PREFIX/bin/python3"
  note "python3 not installed yet; plists will use $PY"
fi

# ================================================================ 2. claude CLI
head1 "2. Claude Code CLI"
CLAUDE_BIN=""
if command -v claude >/dev/null 2>&1; then
  CLAUDE_BIN="$(command -v claude)"
elif [ -x "$HOME/.local/bin/claude" ]; then
  CLAUDE_BIN="$HOME/.local/bin/claude"
fi
if [ -n "$CLAUDE_BIN" ]; then
  note "claude found: $CLAUDE_BIN ($("$CLAUDE_BIN" --version 2>/dev/null || echo 'version unknown'))"
  status "claude CLI" "ok" "$CLAUDE_BIN"
else
  note "claude is not installed. Install it yourself (this script does not pipe it to bash):"
  note "  curl -fsSL https://claude.ai/install.sh | bash"
  note "  (or: brew install --cask claude-code). Then run this script again."
  status "claude CLI" "ACTION" "install with: curl -fsSL https://claude.ai/install.sh | bash"
fi

# ================================================================ 3. logins
head1 "3. Logins (gh, claude, git identity)"
GH_OK=0
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    GH_OK=1
    note "gh is logged in"
  else
    note "gh is not logged in. Run:  gh auth login   (GitHub.com, HTTPS, log in with a web browser)"
    if [ "$APPLY" = 1 ] && [ -t 0 ]; then
      printf '   Run "gh auth login" now? [y/N] '
      read -r ans || ans=""
      if [ "$ans" = "y" ] || [ "$ans" = "Y" ]; then
        gh auth login || true
        gh auth status >/dev/null 2>&1 && GH_OK=1
      fi
    fi
  fi
  if [ "$GH_OK" = 1 ]; then
    # Lets plain git (and the 23:40 sync job) push over HTTPS with the gh login.
    run gh auth setup-git
    status "gh login" "ok" "git uses gh credentials"
  else
    status "gh login" "ACTION" "run: gh auth login, then this script again"
  fi
else
  note "gh not installed yet (step 1)."
  status "gh login" "pending" "gh not installed yet"
fi

if [ -n "$CLAUDE_BIN" ]; then
  if "$CLAUDE_BIN" auth status 2>/dev/null | grep -q '"loggedIn": *true'; then
    note "claude is logged in"
    status "claude login" "ok" ""
  else
    note "claude is not logged in. Run:  claude   (and follow the login), or: claude auth login"
    status "claude login" "ACTION" "run: claude, then log in"
  fi
else
  status "claude login" "pending" "claude not installed yet"
fi

GIT_NAME="$(git config --global user.name 2>/dev/null || true)"
GIT_EMAIL="$(git config --global user.email 2>/dev/null || true)"
if [ -n "$GIT_NAME" ] && [ -n "$GIT_EMAIL" ]; then
  note "git identity: $GIT_NAME"
  status "git identity" "ok" "$GIT_NAME"
else
  note "git has no global name/email; the sync job cannot commit without them. Run:"
  note "  git config --global user.name  \"<your name>\""
  note "  git config --global user.email \"<your GitHub email>\""
  status "git identity" "ACTION" "set git user.name / user.email"
fi

# ================================================================ 4. repos
head1 "4. Repositories"
clone_repo() {
  local name="$1" dest="$2"
  if [ -d "$dest/.git" ]; then
    note "$dest already cloned"
    status "clone $name" "ok" "$dest"
  elif [ -e "$dest" ] && ! dir_empty "$dest"; then
    warn "$dest exists but is not a git checkout; left alone"
    status "clone $name" "ACTION" "$dest exists, not a git repo"
  elif [ "$GH_OK" = 1 ] || [ "$APPLY" = 0 ]; then
    if run gh repo clone "$GH_OWNER/$name" "$dest"; then
      if [ "$APPLY" = 1 ]; then status "clone $name" "cloned" "$dest"; else status "clone $name" "to clone" "$dest"; fi
    else
      status "clone $name" "FAILED" "gh repo clone $GH_OWNER/$name"
    fi
  else
    status "clone $name" "pending" "needs gh login first"
  fi
}
clone_repo my-first-project "$REPO"
clone_repo zavod-om "$ZAVOD"

# Source for restores: ~/my-first-project if present, else the checkout this script runs from.
if [ -d "$REPO/memory" ]; then RESTORE_SRC="$REPO"; else RESTORE_SRC="$SRC_REPO"; fi

# ================================================================ 5. ~/.memory + skills library
head1 "5. Restore ~/.memory and ~/.claude/skills-library (repo snapshots are the newest copies)"
MEM_SRC="$RESTORE_SRC/memory"
MEM_COUNT="$(count_md "$HOME/.memory")"
if [ ! -d "$MEM_SRC" ]; then
  warn "no memory/ snapshot found in $RESTORE_SRC"
  status "~/.memory" "FAILED" "no repo snapshot"
elif [ "$MEM_COUNT" -ge 2 ]; then
  note "~/.memory already has $MEM_COUNT .md files; not touched"
  status "~/.memory" "ok" "$MEM_COUNT .md files"
else
  note "~/.memory is missing or has $MEM_COUNT .md file(s): restoring from $MEM_SRC"
  run mkdir -p "$HOME/.memory"
  for f in "$MEM_SRC"/*.md; do
    [ -e "$f" ] || continue
    safe_copy "$f" "$HOME/.memory/$(basename "$f")"
  done
  if [ "$APPLY" = 1 ]; then status "~/.memory" "restored" "from $MEM_SRC"; else status "~/.memory" "to restore" "from $MEM_SRC"; fi
fi

LIB_SRC="$RESTORE_SRC/.claude/skills-library"
if [ ! -d "$LIB_SRC" ]; then LIB_SRC="$SRC_REPO/.claude/skills-library"; fi
LIB_DST="$HOME/.claude/skills-library"
if [ ! -d "$LIB_SRC" ]; then
  warn "no .claude/skills-library snapshot in $RESTORE_SRC"
  status "skills-library" "FAILED" "no repo snapshot"
elif ! dir_empty "$LIB_DST"; then
  note "$LIB_DST already exists; not touched"
  status "skills-library" "ok" "exists"
else
  note "restoring $LIB_DST from $LIB_SRC (the repo copy has no ruflo/, as on the old Mac's sync)"
  run mkdir -p "$LIB_DST"
  # Destination is empty, so nothing can be overwritten.
  run cp -R "$LIB_SRC/." "$LIB_DST/"
  if [ "$APPLY" = 1 ]; then status "skills-library" "restored" "$LIB_DST"; else status "skills-library" "to restore" "$LIB_DST"; fi
fi

# ================================================================ 6. LaunchAgents
head1 "6. Scheduled jobs (LaunchAgents, old labels kept)"
run mkdir -p "$AGENTS_DIR" "$LOG_DIR" "$BACKUP_DIR"
JOB_PATH="$HOME/.local/bin:$BREW_PREFIX/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
SKILLS="$REPO/.claude/skills"
TMP_PLIST_DIR="$(mktemp -d "${TMPDIR:-/tmp}/setup-new-mac.XXXXXX")"
trap 'rm -rf "$TMP_PLIST_DIR"' EXIT

# write_plist LABEL LOGNAME SCHEDULE_XML ARG... : builds the plist, installs it (with backup)
# and (re)loads it with launchctl bootstrap.
write_plist() {
  local label="$1" logname="$2" sched="$3"; shift 3
  local dst="$AGENTS_DIR/$label.plist" tmp="$TMP_PLIST_DIR/$label.plist" a
  {
    printf '%s\n' '<?xml version="1.0" encoding="UTF-8"?>'
    printf '%s\n' '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
    printf '%s\n' '<plist version="1.0">' '<dict>'
    printf '  <key>Label</key>\n  <string>%s</string>\n' "$label"
    printf '  <key>ProgramArguments</key>\n  <array>\n'
    for a in "$@"; do printf '    <string>%s</string>\n' "$(xml_escape "$a")"; done
    printf '  </array>\n'
    printf '  <key>WorkingDirectory</key>\n  <string>%s</string>\n' "$(xml_escape "$REPO")"
    printf '  <key>EnvironmentVariables</key>\n  <dict>\n'
    printf '    <key>PATH</key>\n    <string>%s</string>\n' "$(xml_escape "$JOB_PATH")"
    printf '    <key>LANG</key>\n    <string>en_US.UTF-8</string>\n'
    printf '    <key>PYTHONIOENCODING</key>\n    <string>utf-8</string>\n'
    printf '  </dict>\n'
    printf '%s\n' "$sched"
    printf '  <key>RunAtLoad</key>\n  <false/>\n'
    printf '  <key>StandardOutPath</key>\n  <string>%s</string>\n' "$(xml_escape "$LOG_DIR/$logname")"
    printf '  <key>StandardErrorPath</key>\n  <string>%s</string>\n' "$(xml_escape "$LOG_DIR/$logname")"
    printf '%s\n' '</dict>' '</plist>'
  } > "$tmp"

  if command -v plutil >/dev/null 2>&1 && ! plutil -lint -s "$tmp"; then
    status "job $label" "FAILED" "generated plist did not lint"
    return 0
  fi

  local changed=1
  if [ -e "$dst" ] && cmp -s "$tmp" "$dst"; then
    changed=0
    note "$label: plist unchanged"
  else
    if [ -e "$dst" ]; then backup_file "$dst" "$BACKUP_DIR/$label.plist.bak.$STAMP"; fi
    run cp "$tmp" "$dst"
  fi

  local loaded=0
  if launchctl print "gui/$UID_N/$label" >/dev/null 2>&1; then loaded=1; fi
  if [ "$loaded" = 1 ] && [ "$changed" = 0 ]; then
    status "job $label" "ok" "loaded, unchanged"
    return 0
  fi
  if [ "$loaded" = 1 ]; then
    run launchctl bootout "gui/$UID_N/$label" || true
  fi
  if run launchctl bootstrap "gui/$UID_N" "$dst"; then
    if [ "$APPLY" = 1 ]; then status "job $label" "loaded" "log: ~/Library/Logs/$logname"; else status "job $label" "to create" "log: ~/Library/Logs/$logname"; fi
  else
    status "job $label" "FAILED" "launchctl bootstrap gui/$UID_N $dst"
  fi
}

daily() { # daily HOUR MINUTE [WEEKDAY]
  printf '  <key>StartCalendarInterval</key>\n  <dict>\n'
  if [ -n "${3:-}" ]; then printf '    <key>Weekday</key>\n    <integer>%s</integer>\n' "$3"; fi
  printf '    <key>Hour</key>\n    <integer>%s</integer>\n    <key>Minute</key>\n    <integer>%s</integer>\n  </dict>' "$1" "$2"
}

for s in sync-from-laptop.sh trend-scout-run.sh zavod-scout-run.sh; do
  if [ ! -f "$SRC_REPO/scripts/$s" ]; then warn "scripts/$s not found in $SRC_REPO (pull the repo first)"; fi
done

write_plist com.tigran.sync-laptop sync-laptop.log "$(daily 23 40)" \
  /bin/bash "$REPO/scripts/sync-from-laptop.sh"
write_plist com.user.claude-auto-learn auto-learn.log "$(daily 9 0)" \
  "$PY" "$SKILLS/auto-learn/auto-learn.py" --mode research
write_plist com.user.claude-auto-learn-promote auto-learn-promote.log "$(daily 10 0 0)" \
  "$PY" "$SKILLS/auto-learn/auto-learn.py" --mode promote
write_plist com.user.claude-consolidate-memory consolidate-memory.log "$(daily 23 10)" \
  "$PY" "$SKILLS/consolidate-memory/consolidate.py"
write_plist com.maghakian.trend-scout trend-scout.launchd.log "$(daily 8 30)" \
  /bin/bash "$REPO/scripts/trend-scout-run.sh"
write_plist com.maghakian.zavod-scout zavod-scout.launchd.log \
  "$(printf '  <key>StartInterval</key>\n  <integer>259200</integer>')" \
  /bin/bash "$REPO/scripts/zavod-scout-run.sh"

note "Test one job now:  launchctl kickstart -p gui/$UID_N/com.user.claude-consolidate-memory"
note "Runner logs: ~/Library/Logs/trend-scout.log, zavod-scout.log. Script logs: $SKILLS/auto-learn/auto-learn.log, ~/.memory/consolidate.log"

# ================================================================ 7. keys (print only)
head1 "7. Keys and logins (printed only; this script never writes a key)"
cat <<EOF
   fal.ai: FAL_KEY is no longer needed. Use fal's official MCP with OAuth:
     claude mcp add --scope user --transport http fal-ai https://mcp.fal.ai/mcp-relay
     then in Claude Code type /mcp, pick fal-ai, and log in in the browser.

   Names only; paste the values yourself, never into the repo or a chat:
   - TAVILY_API_KEY      -> env of the tavily-search MCP server in ~/.claude.json
                            (step 8 command). auto-learn reads it from there.
   - GOOGLE_API_KEY      -> ~/visuals/.env (as on the old Mac); GEMINI_API_KEY is an
     GEMINI_API_KEY         optional alias graphify also reads. Shell use: ~/.zshrc
   - TWITTER_AUTH_TOKEN  -> agent-reach X/Twitter cookies (export from Cookie-Editor).
     TWITTER_CT0            Put both in ~/.zshrc as export lines, or agent-reach's own config.
   - KADR_SECRET         -> ~/kadr/.env.local (KADR app)
   - TELEGRAM_BOT_TOKEN  -> ~/.hermes/.env (Hermes)
   - Higgsfield CLI      -> brew install higgsfield-ai/tap/higgsfield, then: higgsfield auth login
                            (device flow; the CLI keeps its own login)
   Check afterwards that no key landed in ~/my-first-project:
     python3 -I ~/my-first-project/scripts/secret-scan.py --files ~/my-first-project
EOF
status "keys" "ACTION" "add by hand (names in step 7)"

# ================================================================ 8. MCP servers + media-memory hook
head1 "8. MCP servers to re-add (user scope), and the media-memory hook"
cat <<EOF
   claude mcp add --scope user filesystem -- npx -y @modelcontextprotocol/server-filesystem <FOLDER_1> <FOLDER_2>
       (old Mac: ~/Documents and the Obsidian vault; pick your folders)
   claude mcp add --scope user fetch -- uvx mcp-server-fetch
   claude mcp add --scope user chrome-devtools -- npx -y chrome-devtools-mcp@latest --autoConnect
   claude mcp add --scope user tavily-search -e TAVILY_API_KEY=<YOUR_TAVILY_KEY> -- npx -y tavily-mcp@latest
   claude mcp add --scope user --transport http magnific https://mcp.magnific.com
       (OAuth: /mcp in Claude Code, then log in; every generation is metered)
   Check:  claude mcp list
   The repo's own .mcp.json (perplexity, playwright, firecrawl-mcp, glif, chrome-devtools)
   loads by itself inside ~/my-first-project; its keys come from your shell env.

   media-memory PostToolUse hook (see .claude/skills/media-memory/SKILL.md). Merge this
   into ~/.claude/settings.json by hand (keep a .bak of the file first):
   {
     "hooks": {
       "PostToolUse": [
         { "matcher": "Read|Write",
           "hooks": [ { "type": "command", "async": true,
             "command": "$PY $SKILLS/media-memory/media-logger.py --hook" } ] }
       ]
     }
   }
   Old ~/.media-memory pointed at files on the old Mac; it starts fresh here.
EOF
status "MCP servers" "ACTION" "run the claude mcp add lines (step 8)"
status "media-memory hook" "ACTION" "merge into ~/.claude/settings.json"

# ================================================================ 9. CLI-Anything (optional)
head1 "9. CLI-Anything (optional, BRIDGE C6)"
if [ "$WITH_CLI_ANYTHING" = 1 ]; then
  if run bash "$REPO/scripts/install-cli-anything.sh"; then
    if [ "$APPLY" = 1 ]; then status "CLI-Anything" "installed" "add ~/.local/bin to PATH"; else status "CLI-Anything" "to install" "big casks: Blender, GIMP..."; fi
  else
    status "CLI-Anything" "FAILED" "see output above"
  fi
  note "Then: restart Claude Code in the repo, accept the cli-anything plugin, and run"
  note "  cli-hub matrix preflight video-creation   (answer BRIDGE C6 with the summary line)"
else
  note "skipped (add --with-cli-anything to run scripts/install-cli-anything.sh; it installs large apps)"
  status "CLI-Anything" "skipped" "use --with-cli-anything"
fi

# ================================================================ 10. status table
head1 "10. Status"
printf '   %-40s %-11s %s\n' "ITEM" "STATE" "NOTE"
printf '   %-40s %-11s %s\n' "----" "-----" "----"
i=0
while [ "$i" -lt "${#ST_NAME[@]}" ]; do
  printf '   %-40s %-11s %s\n' "${ST_NAME[$i]}" "${ST_STATE[$i]}" "${ST_NOTE[$i]}"
  i=$((i + 1))
done
if [ "$APPLY" = 0 ]; then
  say ""
  say "Dry run only. Re-run with --apply to make these changes."
fi
say ""
say "Next: open scripts/NEW-MAC.md for the manual steps (keys, MCP logins, Full Disk Access)."
