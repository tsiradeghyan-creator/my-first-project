#!/usr/bin/env python3
"""
Auto-Learn Skill — Nightly web research to update ~/.memory/ with new findings.

Modes:
  research (default) — search web, append verified findings to new_learnings
  promote            — weekly: move confirmed learnings to main sections

Usage:
  python3 auto-learn.py [--mode research|promote] [--test] [--topics N]
"""

import json
import os
import re
import ssl
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ── Paths ─────────────────────────────────────────────────────────────────────
HOME = Path.home()
MEMORY_DIR = HOME / ".memory"
LONG_TERM  = MEMORY_DIR / "long-term-memory.md"
PROJECT    = MEMORY_DIR / "project-memory.md"
SKILL_DIR  = HOME / ".claude" / "skills" / "auto-learn"
LOG_FILE   = SKILL_DIR / "auto-learn.log"

# ── Config ────────────────────────────────────────────────────────────────────

def _tavily_key() -> str:
    """Env var first, then the key already configured for the tavily-search MCP
    server in ~/.claude.json.

    Root cause of this skill's three dead months (2026-04-21 → 2026-07-25): the env
    var was never set for the cron/launchd context, so every run silently fell through
    to Google News RSS and returned 0 results. Reading the existing MCP config avoids
    keeping a second plaintext copy of the key anywhere.
    """
    key = os.environ.get("TAVILY_API_KEY", "")
    if key:
        return key
    try:
        import json as _json
        cfg = _json.loads((HOME / ".claude.json").read_text())
        scopes = [cfg.get("mcpServers", {})]
        scopes += [p.get("mcpServers", {}) or {} for p in cfg.get("projects", {}).values()]
        for scope in scopes:
            env = (scope.get("tavily-search", {}) or {}).get("env", {}) or {}
            if env.get("TAVILY_API_KEY"):
                return env["TAVILY_API_KEY"]
    except Exception:
        pass
    return ""


def wait_for_network(attempts: int = 10, delay: int = 30) -> bool:
    """A launchd job that fires right after wake often has no DNS yet — that is what
    produced 'nodename nor servname provided' on every historical run. Wait it out
    instead of burning the whole run."""
    import socket
    for i in range(attempts):
        try:
            socket.create_connection(("1.1.1.1", 443), timeout=5).close()
            return True
        except OSError:
            if i == 0:
                log("No network yet — waiting for it to come up…")
            time.sleep(delay)
    log("Network never came up — aborting this run")
    return False


TAVILY_KEY           = _tavily_key()
MAX_RESULTS_PER_QUERY = 5
MAX_SAVES_PER_TOPIC   = 2   # don't flood with too many entries per topic
PROMOTE_AGE_DAYS      = 7   # entries older than this get promoted to main memory

NEW_LEARNINGS_HEADER  = "## New Learnings"
NEW_LEARNINGS_COMMENT = "<!-- Auto-updated by auto-learn. Reviewed weekly by --mode promote. -->"
TRUSTED_GLOBAL_DOMAINS = [
    "variety.com",
    "deadline.com",
    "hollywoodreporter.com",
    "screendaily.com",
    "indiewire.com",
    "filmmakermagazine.com",
    "cartoonbrew.com",
    "animationmagazine.net",
    "tubefilter.com",
    "digiday.com",
    "adage.com",
    "adweek.com",
    "campaignlive.co.uk",
    "campaignasia.com",
    "thedrum.com",
    "lbbonline.com",
    "shots.net",
    "warc.com",
    "socialmediatoday.com",
    "later.com",
    "buffer.com",
    "hootsuite.com",
    "thinkwithgoogle.com",
    "blog.youtube",
    "newsroom.tiktok.com",
    "about.instagram.com",
    "creators.instagram.com",
    "business.instagram.com",
    "techcrunch.com",
    "theverge.com",
    "wired.com",
    "github.com",
    "news.ycombinator.com",
    "reddit.com",
]


def _year_terms() -> tuple[str, str]:
    """Use current-year queries, with last year as a secondary context term.

    The old topic list was pinned to 2025 and over-weighted Armenian-market searches.
    Auto-learn's job is now the user's global radar: cinema, content, marketing,
    creative industries, advertising, and platform trends worldwide.
    """
    year = datetime.now().year
    return str(year), str(year - 1)


def _ssl_context() -> ssl.SSLContext:
    """Build a certificate context that works in launchd/Homebrew Python.

    This Mac's Python 3.14 can point OpenSSL at `/usr/local/etc/openssl@3/cert.pem`,
    which is absent, causing `CERTIFICATE_VERIFY_FAILED` for Tavily and Google News.
    Prefer certifi if installed, otherwise use the system/Homebrew bundles that exist
    on this machine.
    """
    try:
        import certifi  # type: ignore
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass
    for candidate in (
        "/etc/ssl/cert.pem",
        "/usr/local/etc/ca-certificates/cert.pem",
        "/opt/homebrew/etc/ca-certificates/cert.pem",
    ):
        if Path(candidate).exists():
            return ssl.create_default_context(cafile=candidate)
    return ssl.create_default_context()


# ── Logging ───────────────────────────────────────────────────────────────────

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(line)


# ── Topic Extraction ──────────────────────────────────────────────────────────

def extract_topics() -> list:
    """
    Build a list of search queries from long-term-memory.md and project-memory.md.
    Returns varied global queries: world cinema, platform strategy, advertising,
    creative industries, content trends, and production tools.
    """
    topics = []
    proj_text = PROJECT.read_text("utf-8") if PROJECT.exists() else ""
    lt_text   = LONG_TERM.read_text("utf-8") if LONG_TERM.exists() else ""
    combined  = proj_text + "\n" + lt_text

    year, prev_year = _year_terms()

    # ── Always-on global industry topics ─────────────────────────────────────
    base = [
        f"global film industry trends {year} streaming production screenwriting",
        f"world cinema festival market trends {year} film production",
        f"global TV series production trends {year} scripted drama microdrama",
        f"global advertising industry trends {year} creative campaigns agencies",
        f"global marketing trends {year} social media content strategy",
        f"global creative industry trends {year} design entertainment production",
        f"global content trends {year} short form video creator economy",
        f"instagram tiktok youtube x algorithm updates creators {year}",
        f"youtube long form podcast trends creators {year}",
        f"screenwriting storytelling trends {year} television film social video",
        f"AI video production tools film advertising {year}",
        f"AI agents content production marketing creative workflows {year}",
        f"reddit screenwriting filmmaking marketing community hot posts {year}",
        f"hackernews storytelling creative tools AI media {year}",
        f"wikipedia articles for creation approval tips creatives {year}",
        f"social media SEO personal brand filmmaker {year}",
        f"armenian screenwriting industry news {year}",
        f"armenian tv series production trends {year}",
    ]
    topics.extend(base)

    # ── Extract series titles from project memory ─────────────────────────────
    for pattern in [
        r"Summer of '84", r"84-ի Ամառը", r"Blockade", r"Блокада",
        r"Diary of Helen", r"Paper Dream",
    ]:
        if re.search(pattern, combined, re.IGNORECASE):
            clean = re.sub(r"[^\w\s'-]", "", pattern)
            topics.append(f"{clean} armenian series reception reviews {year} {prev_year}")

    # ── Extract platform-specific topics if mentioned ─────────────────────────
    if "Wikipedia" in combined or "Knowledge Panel" in combined:
        topics.append(f"google knowledge panel for screenwriters strategy {year}")
    if "Wikidata" in combined:
        topics.append(f"wikidata entity creation tips for creatives {year}")
    if "Telegram" in combined:
        topics.append(f"telegram channel growth strategy creators {year}")
    if "Reddit" in combined:
        topics.append(f"reddit AMA screenwriting promotion strategy {year}")

    # ── SEO keyword expansion ─────────────────────────────────────────────────
    seo_kw = re.findall(r'`([^`]+)`', lt_text)
    for kw in seo_kw[:3]:  # limit to top 3
        if len(kw) > 5 and not kw.startswith("#"):
            topics.append(f"{kw} latest news {year} site:reddit.com OR site:news.ycombinator.com")

    # Deduplicate preserving order
    seen, result = set(), []
    for t in topics:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result


# ── Search Backends ───────────────────────────────────────────────────────────

def search_tavily(query: str) -> list:
    """Tavily API — primary backend when TAVILY_API_KEY is set."""
    try:
        import urllib.request
        payload = json.dumps({
            "api_key": TAVILY_KEY,
            "query": query,
            "search_depth": "basic",
            "include_answer": False,
            "max_results": MAX_RESULTS_PER_QUERY,
            "include_domains": TRUSTED_GLOBAL_DOMAINS,
        }).encode()
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=15, context=_ssl_context()) as resp:
            data = json.loads(resp.read())
        return [
            {
                "title":   r.get("title", ""),
                "url":     r.get("url", ""),
                "snippet": r.get("content", "")[:400],
                "backend": "tavily",
            }
            for r in data.get("results", [])
        ]
    except Exception as e:
        log(f"Tavily error ({query[:40]}): {e}")
        return []


def search_google_news_rss(query: str) -> list:
    """Google News RSS — free, no API key, reliable on Python 3.9."""
    import urllib.request, urllib.parse, html as html_mod
    import xml.etree.ElementTree as ET
    try:
        params = urllib.parse.urlencode({"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})
        url = f"https://news.google.com/rss/search?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12, context=_ssl_context()) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        root  = ET.fromstring(raw)
        items = root.findall(".//item")
        results = []
        for item in items[:MAX_RESULTS_PER_QUERY]:
            t_el   = item.find("title")
            d_el   = item.find("description")
            title  = html_mod.unescape(t_el.text or "") if t_el is not None else ""
            desc   = d_el.text or "" if d_el is not None else ""
            url_m  = re.search(r'href="(https?://[^"]+)"', desc)
            url_s  = url_m.group(1) if url_m else ""
            snippet = re.sub(r'<[^>]+>', '', desc).strip()[:400] or title
            # Trim " - Source" suffix from title
            title = re.sub(r'\s*[-–]\s*[^-–]{3,50}$', '', title).strip()
            if url_s:
                results.append({"title": title, "url": url_s, "snippet": snippet, "backend": "google-news"})
        return results
    except Exception as e:
        log(f"Google News RSS error ({query[:40]}): {e}")
        return []


def search_duckduckgo(query: str) -> list:
    """Fallback: ddgs/duckduckgo_search package."""
    import warnings
    for mod_name in ("ddgs", "duckduckgo_search"):
        try:
            m    = __import__(mod_name, fromlist=["DDGS"])
            DDGS = m.DDGS
            out  = []
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with DDGS() as ddgs:
                    for r in ddgs.text(query, max_results=MAX_RESULTS_PER_QUERY):
                        out.append({
                            "title":   r.get("title", ""),
                            "url":     r.get("href", r.get("url", "")),
                            "snippet": r.get("body", r.get("snippet", ""))[:400],
                            "backend": "ddgs-pkg",
                        })
            if out:
                return out
        except Exception:
            continue
    return []


def search_web(query: str) -> list:
    """Tavily (if key set) → Google News RSS → ddgs fallback."""
    if TAVILY_KEY:
        results = search_tavily(query)
        if results:
            return results
        log("Tavily empty, falling back")
    results = search_google_news_rss(query)
    if results:
        return results
    return search_duckduckgo(query)


# ── Deduplication ─────────────────────────────────────────────────────────────

def load_memory_fingerprints() -> set:
    """
    Collect URLs and key 4-gram phrases already stored in all memory files.
    Used to detect duplicate findings before saving.
    """
    fps = set()
    for path in [LONG_TERM, PROJECT]:
        if not path.exists():
            continue
        text = path.read_text("utf-8").lower()
        # All URLs
        for url in re.findall(r'https?://\S+', text):
            fps.add(url.rstrip(").,"))
        # Key 4-grams from bullet lines
        for line in text.splitlines():
            stripped = line.strip().lstrip("-*•").strip()
            words = stripped.split()
            for i in range(len(words) - 3):
                fps.add(" ".join(words[i:i+4]))
    return fps


def is_new(result: dict, fps: set, new_learnings_block: str) -> bool:
    """Return True only if this result isn't already captured."""
    url     = result.get("url", "").lower().rstrip(").,")
    snippet = result.get("snippet", "").lower()

    # URL already in memory or new_learnings
    if url and (url in fps or url in new_learnings_block.lower()):
        return False

    # Snippet 4-gram overlap with memory
    words = snippet.split()
    for i in range(len(words) - 3):
        gram = " ".join(words[i:i+4])
        if gram in fps:
            return False

    return True


_NOISE_PATTERNS = re.compile(
    r'^(introductory|congratulations|welcome|this (page|article|site)|'
    r'sign (up|in)|log in|cookie|privacy policy|all rights reserved|'
    r'click here|read more|learn more|subscribe|please check your network|'
    r'home\s+popular|best of reddit|download\]|download|stay up-to-date)',
    re.IGNORECASE,
)

_NOISE_CONTAINS = re.compile(
    r'(please check your network connection|subscribe for daily|'
    r'stay up-to-date with the latest|reddit rules\s+privacy policy|'
    r'user agreement\s+accessibility|sign up with google|continue in app)',
    re.IGNORECASE,
)

def extract_insight(result: dict) -> str:
    """Pull the most informative sentence from the result snippet."""
    snippet = result.get("snippet", "").strip()
    title   = result.get("title", "").strip()
    url     = result.get("url", "")

    # Reject freelancer/job-board results
    if any(d in url for d in (
        "freelancer.", "fiverr.", "upwork.", "guru.com",
        "event.adweek.com", "l/t?u=", "utm_",
    )):
        return ""

    best = ""
    for sentence in re.split(r'(?<=[.!?])\s+', snippet):
        s = sentence.strip()
        if len(s) < 40 or len(s) > 250:
            continue
        if _NOISE_PATTERNS.match(s):
            continue
        if _NOISE_CONTAINS.search(s):
            continue
        s = re.sub(r'^(Image|Photo)\s+\d+[:\s-]+', '', s, flags=re.IGNORECASE).strip()
        if len(s) < 40 or _NOISE_CONTAINS.search(s):
            continue
        # Prefer sentences with actionable/informational words
        score = sum(1 for w in ("update", "strategy", "algorithm", "tips",
                                "2025", "new", "change", "trend", "best",
                                "result", "improve", "tool", "method")
                    if w in s.lower())
        if score > 0 or len(best) == 0:
            best = s
            if score >= 2:
                break  # good enough

    if best:
        return best

    # Fall back to title (if not noise)
    generic_title = re.compile(
        r'^(ad age: advertising, marketing, media and tech news|'
        r'home|popular|news|explore|best of reddit)$',
        re.IGNORECASE,
    )
    if title and not generic_title.match(title.strip()) \
            and not _NOISE_PATTERNS.match(title) and len(title) > 20:
        return title[:180]
    return ""


# ── New Learnings Section ─────────────────────────────────────────────────────

def get_new_learnings_block() -> str:
    """Return the full New Learnings section from long-term-memory.md."""
    if not LONG_TERM.exists():
        return ""
    text = LONG_TERM.read_text("utf-8")
    if NEW_LEARNINGS_HEADER not in text:
        return ""
    return text[text.index(NEW_LEARNINGS_HEADER):]


def save_learning(entry: dict, dry_run: bool = False):
    """Append one verified finding to the New Learnings section."""
    ts      = datetime.now().strftime("%Y-%m-%d %H:%M")
    insight = entry["insight"].replace("\n", " ").strip()
    line    = (
        f"\n- **[{ts}]** `{entry['query'][:55]}` — "
        f"{insight} "
        f"([source]({entry['url']}))"
    )

    if dry_run:
        print(f"  [DRY-RUN] {line.strip()}")
        return

    text = LONG_TERM.read_text("utf-8") if LONG_TERM.exists() else ""

    if NEW_LEARNINGS_HEADER not in text:
        # Create the section at the bottom
        section_intro = f"\n\n---\n\n{NEW_LEARNINGS_HEADER}\n{NEW_LEARNINGS_COMMENT}"
        text = text.rstrip() + section_intro + line
    else:
        # Find insertion point: right after the header line (+ optional comment line)
        idx = text.index(NEW_LEARNINGS_HEADER)
        nl1 = text.find("\n", idx)
        if nl1 == -1:
            # Header is the very last byte — just append
            text = text + line
        else:
            after_header = nl1 + 1
            # Skip comment line if present
            if text[after_header:after_header + 20].startswith("<!--"):
                nl2 = text.find("\n", after_header)
                after_header = (nl2 + 1) if nl2 != -1 else len(text)
            text = text[:after_header] + line + "\n" + text[after_header:]

    LONG_TERM.write_text(text, "utf-8")
    log(f"  SAVED: {insight[:80]}")


# ── Promote (Weekly) ──────────────────────────────────────────────────────────

def promote_learnings(dry_run: bool = False):
    """
    Weekly pass:
    1. Scan New Learnings for entries older than PROMOTE_AGE_DAYS.
    2. Move them into a '### Auto-promoted' block in Patterns & Preferences.
    3. Remove promoted entries from New Learnings.
    """
    if not LONG_TERM.exists():
        log("long-term-memory.md missing — nothing to promote.")
        return

    text = LONG_TERM.read_text("utf-8")

    if NEW_LEARNINGS_HEADER not in text:
        log("No New Learnings section — nothing to promote.")
        return

    split_at     = text.index(NEW_LEARNINGS_HEADER)
    main_text    = text[:split_at].rstrip()
    learnings    = text[split_at:]

    pattern = re.compile(
        r'- \*\*\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]\*\* '
        r'`([^`]+)` — (.+?) \(\[source\]\(([^\)]+)\)\)'
    )

    now           = datetime.now()
    to_promote    = []
    to_keep_lines = []

    for m in pattern.finditer(learnings):
        ts_str, query, insight, url = m.groups()
        try:
            age = (now - datetime.strptime(ts_str, "%Y-%m-%d %H:%M")).days
        except ValueError:
            to_keep_lines.append(m.group(0))
            continue

        if age >= PROMOTE_AGE_DAYS:
            to_promote.append({"ts": ts_str, "query": query, "insight": insight, "url": url})
        else:
            to_keep_lines.append(m.group(0))

    log(f"Promote pass: {len(to_promote)} ready, {len(to_keep_lines)} staying in new_learnings.")

    if not to_promote:
        log("No entries mature enough yet.")
        return

    if dry_run:
        for p in to_promote:
            print(f"  [DRY-RUN] Promote: {p['insight'][:80]}")
        return

    # Build promoted block
    promoted_md = "\n\n### Auto-promoted from New Learnings\n"
    for p in to_promote:
        promoted_md += f"- [{p['ts']}] {p['insight']} ([source]({p['url']}))\n"

    # Attach to Patterns & Preferences section (or end of main)
    anchor = "## Patterns & Preferences"
    if anchor in main_text:
        # Find the next H2 after Patterns section
        idx  = main_text.index(anchor) + len(anchor)
        nxt  = main_text.find("\n## ", idx)
        ins  = nxt if nxt != -1 else len(main_text)
        main_text = main_text[:ins] + promoted_md + main_text[ins:]
    else:
        main_text += promoted_md

    # Rebuild New Learnings section
    if to_keep_lines:
        kept_block = (
            f"\n\n{NEW_LEARNINGS_HEADER}\n{NEW_LEARNINGS_COMMENT}\n"
            + "".join(f"\n{ln}" for ln in to_keep_lines)
        )
    else:
        kept_block = ""   # fully promoted — clear the section

    LONG_TERM.write_text(main_text + kept_block, "utf-8")
    log(f"Promoted {len(to_promote)} entries. Section {'cleared' if not to_keep_lines else 'trimmed'}.")


# ── Research Loop ─────────────────────────────────────────────────────────────

def run_research(max_topics: int = 6, dry_run: bool = False):
    log(f"=== Auto-Learn RESEARCH (dry={dry_run}) ===")

    topics = extract_topics()[:max_topics]
    log(f"Topics ({len(topics)}): " + " | ".join(t[:40] for t in topics))

    fps              = load_memory_fingerprints()
    new_learnings    = get_new_learnings_block()
    total_saved      = 0
    total_skipped    = 0

    for idx, query in enumerate(topics):
        log(f"[{idx+1}/{len(topics)}] {query[:60]}")
        results = search_web(query)

        if not results:
            log("  No results.")
            continue

        saves_this_topic = 0
        for r in results:
            if not r.get("url") or not r.get("snippet"):
                continue

            if not is_new(r, fps, new_learnings):
                total_skipped += 1
                continue

            insight = extract_insight(r)
            if len(insight) < 25:
                continue

            entry = {"query": query, "insight": insight, "url": r["url"]}
            save_learning(entry, dry_run=dry_run)

            # Update local state so we don't re-save within this run
            fps.add(r["url"].lower())
            new_learnings += r["url"] + insight

            total_saved      += 1
            saves_this_topic += 1
            if saves_this_topic >= MAX_SAVES_PER_TOPIC:
                break

    log(f"=== Done: {total_saved} saved, {total_skipped} skipped ===")


# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    import argparse
    p = argparse.ArgumentParser(description="Auto-Learn Skill")
    p.add_argument("--mode",   choices=["research", "promote"], default="research",
                   help="research=nightly search  promote=weekly consolidation")
    p.add_argument("--test",   action="store_true", help="Dry run — print without saving")
    p.add_argument("--topics", type=int, default=12, help="Max topics per research run")
    args = p.parse_args()

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    if args.mode == "research" and not args.test:
        if not wait_for_network():
            return 1
        log(f"Search backend: {'Tavily' if TAVILY_KEY else 'Google News RSS (no Tavily key found)'}")

    if args.mode == "promote":
        promote_learnings(dry_run=args.test)
    else:
        run_research(max_topics=args.topics, dry_run=args.test)


if __name__ == "__main__":
    main()
