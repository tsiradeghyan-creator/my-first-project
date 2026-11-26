#!/usr/bin/env python3
"""Smoke evals for auto-learn.

These tests monkeypatch the module paths into a temporary directory so they do
not touch the user's real ~/.memory files.
"""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_DIR / "auto-learn.py"


def load_module():
    spec = importlib.util.spec_from_file_location("auto_learn_under_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sandbox(module, tmp: Path):
    memory = tmp / ".memory"
    memory.mkdir()
    module.MEMORY_DIR = memory
    module.LONG_TERM = memory / "long-term-memory.md"
    module.PROJECT = memory / "project-memory.md"
    module.LOG_FILE = tmp / "auto-learn.log"
    module.LONG_TERM.write_text("# Long Term\n\n## New Learnings\n", encoding="utf-8")
    module.PROJECT.write_text("# Project\n", encoding="utf-8")


def test_dry_run_does_not_write(module):
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        sandbox(module, tmp)
        before = module.LONG_TERM.read_text(encoding="utf-8")
        module.save_learning(
            {
                "query": "global film trends 2026",
                "insight": "A useful and specific insight about production strategy.",
                "url": "https://example.com/a",
            },
            dry_run=True,
        )
        after = module.LONG_TERM.read_text(encoding="utf-8")
        assert before == after


def test_duplicate_url_rejected(module):
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        sandbox(module, tmp)
        module.LONG_TERM.write_text(
            "# Long Term\n\n## New Learnings\n- old ([source](https://example.com/a))\n",
            encoding="utf-8",
        )
        fps = module.load_memory_fingerprints()
        assert not module.is_new(
            {"url": "https://example.com/a", "snippet": "A different useful sentence."},
            fps,
            module.get_new_learnings_block(),
        )


def test_noise_is_rejected(module):
    result = {
        "title": "Home",
        "url": "https://example.com/noise",
        "snippet": "Sign up with Google to continue in app. Privacy policy and user agreement.",
    }
    assert module.extract_insight(result) == ""


# Junk that earlier runs actually saved (see auto-learn.log, 2026-04 to 2026-10).
JUNK_CASES = [
    # markdown table row from a GitHub README
    {"title": "", "url": "https://github.com/x/y",
     "snippet": "| | status | Current | | last\\_updated | 2026-07-02 | | audience | |  |  |  |  |"},
    # Reddit page chrome
    {"title": "", "url": "https://reddit.com/r/Filmmakers/x",
     "snippet": "## Post details r/Filmmakers | 15 upvotes | 50 comments | Posted by u/AlphaZetaM"},
    # slug soup
    {"title": "", "url": "https://example.com/slugs",
     "snippet": "videoweb free-video-generator minimax-ai free-video-creation free-video-tool minimax-video hailuo-ai"},
    # schedule / list fragment
    {"title": "", "url": "https://example.com/list",
     "snippet": "– “Monk in Pieces” (5/7)      – “The Escapees” (5/21)      – “Legend of the Mountain” (6/4)"},
    # pipe-only fragment
    {"title": "| | |", "url": "https://example.com/pipes", "snippet": "| | | | |"},
    # too few real words
    {"title": "", "url": "https://example.com/short",
     "snippet": "Top 10 AI tools 2026 #1 #2 #3 #4 #5 #6 #7 #8 #9 #10 list."},
]


def test_junk_is_rejected(module):
    for case in JUNK_CASES:
        got = module.extract_insight(case)
        assert got == "", f"junk accepted: {got!r} from {case['snippet'][:50]!r}"


def test_rss_entity_is_decoded(module):
    # The headline is kept, the "&nbsp;&nbsp;Source" tail and the entity are not.
    got = module.extract_insight({
        "title": "",
        "url": "https://example.com/rss2",
        "snippet": "Armenian Berlinale title After Dreaming picked up for international sales&nbsp;&nbsp;Screen Daily",
    })
    assert got == "Armenian Berlinale title After Dreaming picked up for international sales", got
    got = module.extract_insight({
        "title": "",
        "url": "https://example.com/rss1",
        "snippet": "The 12 Best AI Avatar Tools for UGC Video Ads&amp;nbsp;&amp;nbsp;TechBullion",
    })
    assert "&" not in got and "nbsp" not in got and "TechBullion" not in got, got
    got = module.extract_insight({
        "title": "UK film production spend dips 11% year-on-year in first quarter | News | Screen",
        "url": "https://example.com/t",
        "snippet": "",
    })
    assert got == "UK film production spend dips 11% year-on-year in first quarter", got


def test_good_sentence_kept(module):
    got = module.extract_insight({
        "title": "",
        "url": "https://example.com/good",
        "snippet": "The fund opens a new development call for scripted series in March. More soon",
    })
    assert got == "The fund opens a new development call for scripted series in March.", got


def test_mock_research_saves_only_new(module):
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        sandbox(module, tmp)
        module.extract_topics = lambda: ["query one"]
        module.search_web = lambda query: [
            {
                "title": "Useful article",
                "url": "https://example.com/new",
                "snippet": "New creator workflows are changing production planning for small teams.",
            },
            {
                "title": "Useful article duplicate",
                "url": "https://example.com/new",
                "snippet": "New creator workflows are changing production planning for small teams.",
            },
        ]
        module.run_research(max_topics=1, dry_run=False)
        text = module.LONG_TERM.read_text(encoding="utf-8")
        assert text.count("https://example.com/new") == 1


def main():
    module = load_module()
    tests = [
        test_dry_run_does_not_write,
        test_duplicate_url_rejected,
        test_noise_is_rejected,
        test_junk_is_rejected,
        test_rss_entity_is_decoded,
        test_good_sentence_kept,
        test_mock_research_saves_only_new,
    ]
    for test in tests:
        test(module)
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
