Նոր Mac-ի կարգավորում. սկզբում գործարկիր սկրիպտը առանց `--apply`, ստուգիր, հետո՝ `--apply`։

# New Mac checklist

The old Mac ran the scheduled jobs and held `~/.memory`, the skills library and the logins.
`scripts/setup-new-mac.sh` rebuilds all of that. It never writes an API key; it only tells you where each one goes.

## 1. Get the repo onto the Mac (once)
1. Open Terminal.
2. Install Homebrew:
   `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   Then run the two `eval` lines it prints at the end.
3. Log in to GitHub and clone the repo:
   `brew install gh && gh auth login && gh repo clone tsiradeghyan-creator/my-first-project ~/my-first-project`

## 2. Run the setup script
1. Dry run. It prints what it would do and changes nothing:
   `bash ~/my-first-project/scripts/setup-new-mac.sh`
2. Do it:
   `bash ~/my-first-project/scripts/setup-new-mac.sh --apply`
3. Optional, large apps (BRIDGE C6). Add `--with-cli-anything`.
4. Read the status table at the end. Fix every `ACTION` row, then run step 2 again. A second run is safe: it skips what is done and keeps a `.bak` of any file it replaces.

What the script does:
- Installs git, node, python, rsync, ffmpeg, gh and uv.
- Checks the `claude` CLI. If it is missing, install it yourself with `curl -fsSL https://claude.ai/install.sh | bash`, then run `claude` once to log in.
- Clones `zavod-om` to `~/zavod-om`.
- Restores `~/.memory` and `~/.claude/skills-library` from the repo. The repo copies are the newest ones; the last laptop sync was 2026-11-23.
- Creates the 6 scheduled jobs, with the old names:

| Job | When | Log in `~/Library/Logs/` |
|---|---|---|
| `com.user.claude-consolidate-memory` | daily 23:10 | `consolidate-memory.log` |
| `com.tigran.sync-laptop` | daily 23:40 | `sync-laptop.log` |
| `com.maghakian.trend-scout` | daily 08:30 | `trend-scout.log` |
| `com.user.claude-auto-learn` | daily 09:00 | `auto-learn.log` |
| `com.user.claude-auto-learn-promote` | Sunday 10:00 | `auto-learn-promote.log` |
| `com.maghakian.zavod-scout` | every 3 days | `zavod-scout.log` |

## 3. By hand, after the script
- [ ] `git config --global user.name` and `user.email`, if the script asked for them. Without them the 23:40 sync cannot commit.
- [ ] fal.ai: `claude mcp add --scope user --transport http fal-ai https://mcp.fal.ai/mcp-relay`, then `/mcp` inside Claude Code to log in. `FAL_KEY` is no longer needed.
- [ ] Re-add the other MCP servers with the `claude mcp add` lines printed in step 8: filesystem, fetch, chrome-devtools, tavily-search and magnific. Put the Tavily key in the tavily-search entry. auto-learn reads it from there, because a scheduled job does not see `~/.zshrc`.
- [ ] Keys, as names only. Paste each value into the file named in step 7 of the script output: `GOOGLE_API_KEY`/`GEMINI_API_KEY`, `TWITTER_AUTH_TOKEN`/`TWITTER_CT0`, `KADR_SECRET` and `TELEGRAM_BOT_TOKEN`. Never put a key in the repo or in a chat.
- [ ] Higgsfield: `brew install higgsfield-ai/tap/higgsfield`, then `higgsfield auth login`.
- [ ] media-memory hook: merge the JSON printed in step 8 into `~/.claude/settings.json`. Keep a `.bak` of that file first.
- [ ] Test one job now: `launchctl kickstart -p gui/$(id -u)/com.user.claude-consolidate-memory`, then read its log.
- [ ] Run each scout once by hand and read its log:
  - `bash ~/my-first-project/scripts/trend-scout-run.sh`, log `~/Library/Logs/trend-scout.log`;
  - `bash ~/my-first-project/scripts/zavod-scout-run.sh`, log `~/Library/Logs/zavod-scout.log`.

## macOS privacy (Full Disk Access)
macOS blocks scheduled jobs from `~/Documents`, `~/Desktop` and `~/Downloads`. The old trend-scout failed this way when it wrote into the Obsidian vault under `~/Documents`.
- The jobs now write only to `~/.memory`, `~/my-first-project` and `~/zavod-om`, so they need nothing extra.
  - trend-scout writes `~/.memory/trends-radar.md`, and the 23:40 sync copies it into the repo's `memory/`.
- If you ever point a job at `~/Documents`, give it Full Disk Access: System Settings > Privacy & Security > Full Disk Access.
  - Add `/bin/bash` and the python3 shown in the script output (for example `/opt/homebrew/bin/python3`).
  - For the scouts, also add `~/.local/bin/claude`.

## Not coming back
- `~/.claude/projects` (old chat history) stayed on the old Mac, so consolidate-memory starts from new chats only.
- `~/.media-memory` pointed at files on the old Mac, so it starts empty.
- `~/.claude/trend-state/` and `~/.agent-reach/` start empty. Run `agent-reach` setup again if you use it.

## Safety
- The 23:40 sync now skips `~/.memory` if it has fewer than 2 `.md` files. It also skips the skills library or the zavod canon if either is missing or empty. An empty folder on a new Mac can no longer wipe the repo copies.
- The scouts run `claude -p` in `acceptEdits` mode. They can edit files in their folders, search the web and run the commands listed in each runner script. Anything else is refused.
