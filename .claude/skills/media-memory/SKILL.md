---
name: media-memory
description: Log and search media files (images, PDFs, video, audio) seen in conversations to ~/.media-memory/ with metadata (path, type, size, SHA256, tags, description). Use when the user runs /media-memory, asks to log or recall a previously seen image/PDF/video/audio file, or wants to search their media history.
metadata:
  version: 1.1.0
---

# Media Memory Skill

## Purpose
Automatically log every media file (image, PDF, video, audio) encountered in conversations to `~/.media-memory/` with full metadata. Makes every media asset searchable and retrievable across sessions.

## Directory Structure
```
~/.media-memory/
  files/          ← copies of media files (optional, toggle with --copy)
  index.md        ← human-readable searchable index
  metadata.json   ← structured metadata (all entries)
  log.txt         ← operation history
```

## When to Use
- Automatically: triggered by PostToolUse hook on Read/Write tool calls (configured in settings.json)
- Manually: `/media-memory` — log a specific file or directory
- Query: `/media-memory search <term>` — find files by tag, type, or description

## Manual Usage

```bash
# Log a specific file
python3 ~/.claude/skills/media-memory/media-logger.py --file /path/to/image.png --desc "Description" --tags "tag1,tag2"

# Log with file copy
python3 ~/.claude/skills/media-memory/media-logger.py --file /path/to/image.png --copy

# Search the index
python3 ~/.claude/skills/media-memory/media-logger.py --search "maghakian"

# Show all entries
python3 ~/.claude/skills/media-memory/media-logger.py --list

# Show stats
python3 ~/.claude/skills/media-memory/media-logger.py --stats
```

## Output Contract

Every successful log operation must leave three consistent records:

1. One structured entry in `~/.media-memory/metadata.json`.
2. A regenerated human index at `~/.media-memory/index.md`.
3. One operation line in `~/.media-memory/log.txt`.

Each metadata entry must include: `id`, `filename`, absolute `path`, MIME `type`,
`category`, `ext`, `size_bytes`, `size_human`, short `sha256`, `timestamp`,
`session_id`, `description`, `tags`, and optional `copied_to`.

Search/list/stats operations are read-only and must not rewrite media files.

## Auto-Hook Behavior
When configured in settings.json, the hook fires after every Read tool call on a media file (png, jpg, jpeg, gif, webp, pdf, mp4, mov, mp3, wav). It logs:
- File path and name
- File type and size
- Timestamp
- SHA256 hash (for deduplication)
- Session ID

Hook mode must fail soft: malformed JSON, unsupported tools, missing paths, missing
files, duplicate paths, and non-media extensions should exit without breaking the
calling conversation.

## Metadata Fields
```json
{
  "id": "unique-id",
  "filename": "image.png",
  "path": "/full/path/to/image.png",
  "type": "image/png",
  "size_bytes": 204800,
  "size_human": "200 KB",
  "sha256": "abc123...",
  "timestamp": "2026-04-07T16:00:00",
  "session_id": "...",
  "description": "User-provided description",
  "tags": ["maghakian", "brand", "logo"],
  "copied_to": "~/.media-memory/files/image_abc123.png"
}
```

## Verification

After changing `media-logger.py`, run:

```bash
python3 -m py_compile ~/.claude/skills/media-memory/media-logger.py
python3 ~/.claude/skills/media-memory/media-logger.py --stats
python3 ~/.claude/skills/media-memory/media-logger.py --search "unlikely-smoke-query"
```

For behavior changes, run the scenarios in `evals/evals.json` manually or with a
small temporary fixture. The important invariants are:

- duplicate paths do not create duplicate entries,
- damaged `metadata.json` is quarantined instead of crashing the hook,
- concurrent writes keep valid JSON,
- `--copy` copies only when explicitly requested,
- hook mode never deletes, moves, or modifies the source media file.

## Safety Boundaries

- Never delete source files or old memory entries unless the user explicitly asks.
- Do not copy large or sensitive media into `~/.media-memory/files/` unless `--copy`
  is explicit.
- Do not infer private tags from sensitive media content; use user-provided tags or
  neutral file metadata.
- Do not expose full paths in a public-facing deliverable unless the user asks for
  local file references.
