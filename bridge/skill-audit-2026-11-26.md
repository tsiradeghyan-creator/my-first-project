# Skill audit, 2026-11-26 (Cloud, read-only)

Five reviewers read all 29 skills in `.claude/skills/`, the 9 agents in `.claude/agents/` and the related scripts, about 530k words. They changed no files. Every skill was checked the same way:
1. wording that current Claude models over-apply (CRITICAL / MUST / ALL-CAPS, "if in doubt use X");
2. stale model facts (the important ones verified on the web);
3. broken files and old-laptop paths;
4. contradictions with CLAUDE.md and other skills;
5. dead weight.

Cloud re-checked by hand the HIGH findings marked ✔.

Severity:
- **HIGH:** gives a wrong or broken result today.
- **MED:** likely to degrade output.
- **LOW:** cleanup.

## 0. One decision for Tigran first

**film-crew for a single shot.** CLAUDE.md (2026-11-03) says film-crew runs first for every visual or video prompt, even one shot. The skills say something else:
- film-crew's own description says "Not for one isolated prompt (seedance-25-director…)";
- its routing evals expect seedance, cinema or banana first;
- none of the six prompt skills calls film-crew for one shot;
- skill-router says "always first".

Either film-crew gets a short single-shot mode and all prompt skills defer to it, or the rule is narrowed to multi-shot work. Fix the skills only after this is decided.

## 1. HIGH: broken or wrong today

| # | Skill | Problem | Fix |
|---|---|---|---|
| 1 ✔ | maghakian-brand | `references/full-guide.md:37-46` uses the old purple palette (`#6450D2`, `#0D0D0D`, "Never use pure #FFFFFF"). Every template on lines 115-267 and 409 is purple. The figures say "46 projects, 2,200+ episodes, 2017–2026"; business.md says 48 / 2,300+ / since 2016. The old name "Maghakian Script Writing Agency" is still used. | Rewrite to #000/#FFF/#111 + #D90429, «Maghakian Scripts», business.md figures. |
| 2 | content-zavod (canon in zavod-om) | Same purple/gold palette (`identity-guard.md:15`, `carousel-template.md:59`, `motion-design.md:45`) and "47 projects, ~2,270". The core router paths (`~/zavod-om/ZAVODOM.md`, `lib/content_router.py`) do not exist outside the old laptop. | Fix in the zavod-om repo, not here: sync overwrites this copy. |
| 3 ✔ | higgsfield | `scripts/seedance_lint.py --preflight --model seedance_2_5` → `ERROR: unknown model 'seedance_2_5'`. The "always preflight" rule breaks for 2.5. `specs/model-specs.yaml` is a 2026-07-05 snapshot with no 2.5. | Re-snapshot the specs with 2.5, or skip the lint for 2.5. |
| 4 | higgsfield | About 20 places still default to `seedance_2_0`: motion-design:85,108; router full-guide:98 (Fast Path "Kling 3.0 or Seedance 2.0"); seedance, seedance-vfx, facs, shotlist-director and cinema guides. Higgsfield has had Seedance 2.5 since 2026-08-06 (30 s, 4K, 50 refs), and Kling 4.0 and Cinema Studio 4.0 also exist. | Default to 2.5 via seedance-25-director; mark the 2.0 guides as 2.0-only. |
| 5 | higgsfield | `scripts/validate.py` fails with 73 issues since the 2026-08-25 slimming moved routing into `references/full-guide.md`. | Point the validator at the full guide. |
| 6 ✔ | cinema-worldbuilder-pro-2.0 | `full-guide.md:49,75` say "@image1–@image9, hard cap 9 — Seedance hard cap" (2.0 limits). `:34` says "Default to Seedance if they don't care", while skill-router uses this skill for non-Seedance engines. | Remove the Seedance row and send Seedance work to seedance-25-director; ask for the engine instead. |
| 7 | shortfilm-prompt | Built for Seedance 2.0 ("single-shot ≤ 15s", "use Seedance 2.0, not Fast") and recommends Sora 2 (API closed 2026-09-24). | See verdicts: fold into film-crew. |
| 8 | gpt-image-prompting | `references/api-reference.md:90` offers `background: transparent` with gpt-image-2, which returns 400 since 2026-09-30. | Note: transparent only on gpt-image-1.5, otherwise cut out afterwards. |
| 9 ✔ | film-crew agents | All 7 department agents (`film-director.md:9` etc.) and `film-style-researcher.md:8,26` read and write `~/.claude/skills/film-crew/...`, the old laptop's folder. | Use the repo path `.claude/skills/film-crew/`. |
| 10 ✔ | fal-ai-media | `full-guide.md:117,159` `fal-ai/seedance-1-0-pro` does not exist; `:146` `fal-ai/veo-3` should be `fal-ai/veo3.1`; `:132` the Kling v3 id needs `/text-to-video`, and `"5s"` should be `"5"`; `:73-75` Nano Banana Pro takes `aspect_ratio`/`resolution`, not `image_size`/`guidance_scale`. Tool names are from a third-party MCP, not fal's official one. | Rewrite the guide; default to `bytedance/seedance-2.5/...`. |
| 11 | auto-learn, trend-scout, zavod-scout, consolidate-memory, media-memory | They ran from the old Mac, so they are dead now:<br>• LaunchAgents are gone;<br>• `~/.claude/trend-scout-run.sh` and the zavod-scout runner were never committed;<br>• the media-memory hook lived in the laptop's user settings;<br>• trend-scout's Obsidian path was blocked by macOS privacy anyway.<br>auto-learn last ran 2026-10-31. | See section 4. |
| 12 | agent-reach | It makes you read a guide that needs CLIs not installed anywhere now (agent-reach, mcporter, twitter-cli, yt-dlp…). Its "MUST USE" trigger takes over all research. | Run `agent-reach doctor` first, fall back to web tools, narrow the trigger. |
| 13 | cli-hub | `:120` `.claude/skills-library/cli-anything/...` does not exist. | Fix the path, or have the install script create it. |

## 2. MED: will degrade output

- **Shouty wording** ("CRITICAL", "MUST", "NON-NEGOTIABLE", forced "Sound good?" rounds):
  - banana-pro full-guide (69 hits);
  - cinema-worldbuilder full-guide;
  - jackvsai-fashion;
  - higgsfield-character-design;
  - graphify full-guide:205;
  - llm-council full-guide:3;
  - agent-reach.

  Keep the rules but state them calmly, with the reason.
- **Trigger collisions:**
  - Multi-shot work: film-crew, shortfilm-prompt, cinema-worldbuilder, higgsfield-shotlist-director and higgsfield-character-design.
  - "Post / carousel / reel / screenplay": content-zavod, copywriting, mini-scenario, director-desk and ani-screenwriting-workflow.
  - Decisions: llm-council, the Roast Room and bab-production.
  - Social and SEO: seo-audit and ani-digital-marketing.
  - mini-scenario uses `/help` and `/export` as triggers, which are built-in Claude Code commands.
- **Duplicates:**
  - content-zavod/gpt-image-prompting is a byte-identical copy of the top-level skill.
  - higgsfield-gpt-image-2 duplicates gpt-image-prompting.
  - higgsfield-vibe-motion duplicates remotion-video-creation.
  - higgsfield-content-factory duplicates content-zavod.
  - higgsfield-image-shots duplicates banana-pro.
  - maghakian-brand exists both locally and as an account skill.
- **gpt-image-prompting** sends engine-neutral stills to content-zavod, but skill-router says banana-pro.
- **banana-pro:** `full-guide.md:12` says mid-gray backdrop, while `:355` says white. Nano Banana 2 is now on Higgsfield.
- **director-desk:** the description is 1,365 characters (limit 1,024), so trigger words may be cut. The ChatGPT pack lacks fonts and Chromium.
- **film-crew:** `evals/routing.json` r03, r04, r06 and r09 bake in the old routing. The 12 seed style cards are "from knowledge, not source-checked", against the skill's own rule.
- **Old model facts:**
  - Sora is still listed in cinema-worldbuilder, shortfilm, higgsfield-models and content-zavod.
  - content-zavod's ai-tools-directory still lists DALL·E 3.
  - Kling 3.0 is named where 4.0 exists (app only, API not announced).
- **seo-audit:** recommends Google's Mobile-Friendly Test (retired Dec 2023) and delegates to skills that are not installed.
- **copywriting:** links page-cro, popup-cro and ab-test-setup, which are not installed.
- **skill-router:** the map misses auto-learn, cli-hub, consolidate-memory, graphify, media-memory and zavod-scout.
- **skill-library:** the DAILY list misses film-crew, seedance-25, skill-router, studio, director-desk, bab, banana-pro, cinema-worldbuilder and cli-hub.
- **auto-learn and consolidate-memory:** their filters wrote junk into memory (`| status | Current |`, `&nbsp;`, regex fragments).

## 3. Verdict per skill

| Verdict | Skills |
|---|---|
| **KEEP AS IS** | seedance-25-director (current facts, calm style; it only needs the film-crew line and to drop the `~/Downloads` docx path), bab-production (refresh state notes), studio, remotion-video-creation, film-continuity-verifier agent, 12 thin higgsfield sub-skills |
| **LIGHT EDIT** | film-crew, skill-router, director-desk, banana-pro-director-2.0, cinema-worldbuilder-pro-2.0, gpt-image-prompting, jackvsai-fashion, copywriting, mini-scenario, seo-audit, higgsfield (router, motion-design, stack, seedance family, character-design), film-style-researcher agent, auto-learn, trend-scout, zavod-scout, skill-library, agent-reach, graphify, cli-hub, media-memory (restore its hook) |
| **REWRITE** | maghakian-brand (palette, name, figures), content-zavod (at the zavod-om canon), fal-ai-media guide, consolidate-memory (extraction), 9 boilerplate higgsfield wrappers (merge into the router) |
| **CANDIDATE TO DELETE** | shortfilm-prompt (fold its genre templates into film-crew first), llm-council (the Roast Room replaces it), higgsfield-shotlist-director (duplicates film-crew), 7 film-crew department agents (film-crew runs departments in one context and never dispatches them) |

## 4. To restore on the new computer

- **Folders:**
  - `~/.memory`, `~/.media-memory`, `~/.claude/skills-library`;
  - `~/zavod-om` (git clone);
  - `~/.claude/trend-state/`, `~/.agent-reach/`;
  - `~/.claude/projects` (chat history; consolidate-memory reads it).
- **Scheduled jobs:**

  | Job | When | Runs |
  |---|---|---|
  | `com.tigran.sync-laptop` | 23:40 | the sync script |
  | `com.user.claude-auto-learn` | daily 09:00 | `auto-learn.py` |
  | `com.user.claude-auto-learn-promote` | Sunday 10:00 | `auto-learn.py --mode promote` |
  | `com.user.claude-consolidate-memory` | nightly | memory consolidation |
  | `com.maghakian.trend-scout` | 08:30 | runner lost, rebuild it |
  | zavod-scout | every 3 days | runner lost |

  Alternative: move the research jobs to cloud scheduled tasks.
- **Keys** (names only, never commit):
  - `FAL_KEY` and `TAVILY_API_KEY` (MCP env in `~/.claude.json`);
  - `GOOGLE_API_KEY` / `GEMINI_API_KEY`;
  - `TWITTER_AUTH_TOKEN`, `TWITTER_CT0`;
  - `KADR_SECRET`, `TELEGRAM_BOT_TOKEN`;
  - Higgsfield CLI login.
- **User-level config, not in the repo:**
  - `~/.claude.json` MCP servers: filesystem, fetch, chrome-devtools, fal-ai, tavily-search, magnific;
  - `~/.claude/settings.json` hooks, including the media-memory PostToolUse hook.
- **CLIs:**
  - python3 (+certifi), node, git, ffmpeg, rsync, `gh` (logged in), `claude` (logged in);
  - optional: uv (graphify), the agent-reach stack, `scripts/install-cli-anything.sh`.
- **sync-from-laptop.sh:**
  - Homebrew PATH (:8) and `REPO=$HOME/my-first-project` (:10) are fine on a Mac.
  - `rsync --delete` (:51) overwrites any Cloud edit to content-zavod, so zavod fixes go to zavod-om.

## 5. Suggested order

1. Tigran decides section 0.
2. Fix all HIGH items in one pass. Brand and paths come first, because they affect everything.
3. Run the calm-wording and trigger cleanup on MED items.
4. Delete or fold the candidates.
5. Run real evals (`claude plugin eval --ablation with-without`, or skill-creator) on the top 5 skills: seedance-25-director, film-crew, gpt-image-prompting, banana-pro, cinema-worldbuilder.

## 6. Fix pass, 2026-11-26 (Cloud): status

Tigran chose **option A**: film-crew got a short single-shot mode, and every prompt skill now runs film-crew first and takes its plan as input.

**HIGH items fixed:**

| # | Fix | Check |
|---|---|---|
| 1 | maghakian-brand: new palette, «Maghakian Scripts», 48 / 2,300+ / since 2016, signature wordmark with the logo file paths | |
| 2 | content-zavod: same brand fixes, router fallback, film-crew line, Sora and DALL·E 3 retired | Fixed in the zavod-om canon (pushed to zavod-om main, `00f80f7` and `04c819d`) and mirrored here |
| 3 | higgsfield: `seedance_2_5` added to the specs, so the linter preflight passes | `validate.py` ALL CHECKS PASSED (73 issues before) |
| 4 | Seedance 2.5 is the default; 2.0 guides carry a "2.0 only" note | |
| 5 | cinema-worldbuilder and shortfilm: 2.0 limits and Sora removed | |
| 6 | gpt-image-prompting: transparent-background caveat | Fixed in the canon |
| 7 | film-crew agents use the repo path | |
| 8 | fal-ai-media: ids and parameters verified against fal.ai; official MCP `mcp-relay` with OAuth | |
| 9 | agent-reach checks that its CLI is installed first | |
| 10 | cli-hub path | |
| 11 | zavod-scout and trend-scout: canon and output paths | zavod-scout frontmatter YAML repaired |

**Still open:**
- Scheduled jobs and keys must be rebuilt on the new computer (section 4).
- Two projects are missing from the portfolio lists: the brand list has 46 of 48 and the zavod filmography has 47.
- Hashtag `#MaghakianSWA` → `#MaghakianScripts`?
- The «Խաղալիք» carousel pack keeps its own show palette.
- The director-desk description is 1,365 characters, over the limit (MED).
- Not yet done: the MED and LOW items, the deletions, and the real evals.
