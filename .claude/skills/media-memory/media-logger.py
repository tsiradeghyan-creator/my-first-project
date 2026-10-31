#!/usr/bin/env python3
"""
Media Memory Logger — auto-logs media files to ~/.media-memory/.
Called by PostToolUse hook OR manually via CLI.
"""

import json
import os
import sys
import fcntl
import shutil
import hashlib
import argparse
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Paths ────────────────────────────────────────────────────────────────────
HOME = Path.home()
MEDIA_DIR = HOME / ".media-memory"
FILES_DIR = MEDIA_DIR / "files"
INDEX_MD = MEDIA_DIR / "index.md"
METADATA_JSON = MEDIA_DIR / "metadata.json"
LOG_FILE = MEDIA_DIR / "log.txt"

MEDIA_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".heic",
    ".pdf",
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    ".mp3", ".wav", ".aac", ".flac", ".m4a",
    ".svg", ".psd", ".ai",
}

TYPE_CATEGORIES = {
    "image": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".heic", ".svg", ".psd", ".ai"},
    "pdf": {".pdf"},
    "video": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "audio": {".mp3", ".wav", ".aac", ".flac", ".m4a"},
}


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def human_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}" if unit != "B" else f"{size_bytes} B"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]  # short hash for readability


def get_category(ext: str) -> str:
    for cat, exts in TYPE_CATEGORIES.items():
        if ext in exts:
            return cat
    return "other"


def load_metadata() -> list:
    """Read the index. Never raise on a damaged file — a hook that dies here is a
    hook that stops logging silently, which is exactly how this went dead for five
    weeks in 2026-06/07."""
    if not METADATA_JSON.exists():
        return []
    try:
        with open(METADATA_JSON) as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        damaged = METADATA_JSON.with_suffix(".json.damaged")
        try:
            METADATA_JSON.replace(damaged)
            print(f"media-logger: metadata was corrupt, moved to {damaged}", file=sys.stderr)
        except OSError:
            pass
        return []


def save_metadata(entries: list):
    """Atomic write under an exclusive lock.

    The PostToolUse hook is declared async and fires on every Read|Write, so several
    invocations can overlap. The previous plain `open(...,"w")` let two writers
    interleave and produced a metadata.json ending in `] }\n]` — unparseable, which
    silently killed all media logging from 2026-06-19 until 2026-07-25.
    """
    lock_path = METADATA_JSON.with_suffix(".json.lock")
    with open(lock_path, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tmp = METADATA_JSON.with_suffix(".json.tmp")
        with open(tmp, "w") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, METADATA_JSON)
        fcntl.flock(lock, fcntl.LOCK_UN)


def is_duplicate(path: Path, entries: list) -> bool:
    """Check if file already logged by path."""
    path_str = str(path)
    return any(e.get("path") == path_str for e in entries)


def log_file(
    file_path: str,
    description: str = "",
    tags: list[str] = None,
    copy: bool = False,
    session_id: str = "",
) -> Optional[dict]:
    """Log a single media file to metadata and index."""
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        log(f"SKIP: file not found: {path}")
        return None

    ext = path.suffix.lower()
    if ext not in MEDIA_EXTENSIONS:
        log(f"SKIP: not a media file: {path.name}")
        return None

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    FILES_DIR.mkdir(parents=True, exist_ok=True)

    entries = load_metadata()

    if is_duplicate(path, entries):
        log(f"SKIP: already logged: {path.name}")
        return None

    stat = path.stat()
    file_hash = sha256(path)
    mime = mimetypes.guess_type(str(path))[0] or f"application/{ext[1:]}"
    category = get_category(ext)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uid = f"{file_hash}_{datetime.now().strftime('%H%M%S')}"

    copied_to = ""
    if copy:
        dest = FILES_DIR / f"{path.stem}_{file_hash}{ext}"
        shutil.copy2(path, dest)
        copied_to = str(dest)
        log(f"Copied to {dest}")

    entry = {
        "id": uid,
        "filename": path.name,
        "path": str(path),
        "type": mime,
        "category": category,
        "ext": ext,
        "size_bytes": stat.st_size,
        "size_human": human_size(stat.st_size),
        "sha256": file_hash,
        "timestamp": ts,
        "session_id": session_id,
        "description": description,
        "tags": tags or [],
        "copied_to": copied_to,
    }

    entries.append(entry)
    save_metadata(entries)
    update_index(entries)
    log(f"Logged: {path.name} ({category}, {human_size(stat.st_size)})")

    return entry


def update_index(entries: list):
    """Regenerate index.md from all metadata entries."""
    # Stats
    total = len(entries)
    by_cat = {}
    total_bytes = 0
    for e in entries:
        cat = e.get("category", "other")
        by_cat[cat] = by_cat.get(cat, 0) + 1
        total_bytes += e.get("size_bytes", 0)

    stats_line = (
        f"- Total files logged: {total}\n"
        f"- Images: {by_cat.get('image', 0)} | "
        f"PDFs: {by_cat.get('pdf', 0)} | "
        f"Videos: {by_cat.get('video', 0)} | "
        f"Audio: {by_cat.get('audio', 0)} | "
        f"Other: {by_cat.get('other', 0)}\n"
        f"- Total size: {human_size(total_bytes)}"
    )

    today = datetime.now().strftime("%Y-%m-%d")

    # Build entries section
    entry_lines = []
    for e in reversed(entries):  # newest first
        tags_str = " ".join(f"`{t}`" for t in e.get("tags", []))
        desc = e.get("description", "")
        entry_lines.append(
            f"### {e['filename']}\n"
            f"- **Date:** {e['timestamp']}\n"
            f"- **Type:** {e['type']} ({e['size_human']})\n"
            f"- **Path:** `{e['path']}`\n"
            + (f"- **Description:** {desc}\n" if desc else "")
            + (f"- **Tags:** {tags_str}\n" if tags_str else "")
            + (f"- **Copied to:** `{e['copied_to']}`\n" if e.get("copied_to") else "")
            + f"- **Hash:** `{e['sha256']}`"
        )

    entries_section = "\n\n".join(entry_lines) if entry_lines else (
        "*No media files logged yet.*"
    )

    content = f"""# Media Memory Index
<!-- Auto-updated by media-logger.py. Do not edit manually. -->
<!-- Last updated: {today} -->

## Stats
{stats_line}

---

## Entries

{entries_section}

---

## Search Tips
```bash
python3 ~/.claude/skills/media-memory/media-logger.py --search "keyword"
python3 ~/.claude/skills/media-memory/media-logger.py --list
python3 ~/.claude/skills/media-memory/media-logger.py --stats
```
"""
    INDEX_MD.write_text(content, encoding="utf-8")


def search(query: str) -> list:
    """Search entries by filename, description, tags, or path."""
    entries = load_metadata()
    q = query.lower()
    results = []
    for e in entries:
        searchable = " ".join([
            e.get("filename", ""),
            e.get("description", ""),
            e.get("path", ""),
            " ".join(e.get("tags", [])),
            e.get("type", ""),
        ]).lower()
        if q in searchable:
            results.append(e)
    return results


def print_stats():
    entries = load_metadata()
    total = len(entries)
    by_cat = {}
    total_bytes = 0
    for e in entries:
        cat = e.get("category", "other")
        by_cat[cat] = by_cat.get(cat, 0) + 1
        total_bytes += e.get("size_bytes", 0)

    print(f"\n📁 Media Memory Stats")
    print(f"   Total files : {total}")
    print(f"   Images      : {by_cat.get('image', 0)}")
    print(f"   PDFs        : {by_cat.get('pdf', 0)}")
    print(f"   Videos      : {by_cat.get('video', 0)}")
    print(f"   Audio       : {by_cat.get('audio', 0)}")
    print(f"   Other       : {by_cat.get('other', 0)}")
    print(f"   Total size  : {human_size(total_bytes)}")
    print(f"   Index       : {INDEX_MD}")


def parse_args():
    parser = argparse.ArgumentParser(description="Media Memory Logger")
    parser.add_argument("--file", help="Path to media file to log")
    parser.add_argument("--desc", default="", help="Description of the file")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--copy", action="store_true",
                        help="Copy file to ~/.media-memory/files/")
    parser.add_argument("--session", default="", help="Claude session ID")
    parser.add_argument("--search", help="Search the index by keyword")
    parser.add_argument("--list", action="store_true", help="List all logged files")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    # Hook mode: receives JSON via stdin (PostToolUse hook)
    parser.add_argument("--hook", action="store_true",
                        help="Hook mode: read tool call JSON from stdin")
    return parser.parse_args()


def hook_mode():
    """
    Called by PostToolUse hook. Reads JSON from stdin:
    { "tool_name": "Read", "tool_input": { "file_path": "..." }, ... }
    """
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # not JSON, ignore

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only care about Read and Write tools
    if tool_name not in ("Read", "Write"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    if not file_path:
        sys.exit(0)

    ext = Path(file_path).suffix.lower()
    if ext not in MEDIA_EXTENSIONS:
        sys.exit(0)

    session_id = data.get("session_id", "")
    entry = log_file(
        file_path=file_path,
        description=f"Auto-logged via {tool_name} tool",
        tags=["auto-logged"],
        copy=False,
        session_id=session_id,
    )

    if entry:
        print(f"[media-memory] Logged: {entry['filename']} ({entry['size_human']})")

    sys.exit(0)


def main():
    args = parse_args()

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    FILES_DIR.mkdir(parents=True, exist_ok=True)

    if args.hook:
        hook_mode()
        return

    if args.stats:
        print_stats()
        return

    if args.list:
        entries = load_metadata()
        if not entries:
            print("No media files logged yet.")
            return
        for e in entries:
            print(f"[{e['timestamp']}] {e['filename']} ({e['size_human']}) — {e.get('description','')}")
        return

    if args.search:
        results = search(args.search)
        if not results:
            print(f"No results for '{args.search}'")
            return
        print(f"Found {len(results)} result(s) for '{args.search}':")
        for e in results:
            print(f"  • {e['filename']} ({e['timestamp']}) — {e.get('description','')}")
            if e.get("tags"):
                print(f"    tags: {', '.join(e['tags'])}")
        return

    if args.file:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        entry = log_file(
            file_path=args.file,
            description=args.desc,
            tags=tags,
            copy=args.copy,
            session_id=args.session,
        )
        if entry:
            print(f"✅ Logged: {entry['filename']} ({entry['size_human']})")
            print(f"   Category : {entry['category']}")
            print(f"   Hash     : {entry['sha256']}")
            print(f"   Index    : {INDEX_MD}")
        return

    # No args — show stats
    print_stats()


if __name__ == "__main__":
    main()
