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
        test_mock_research_saves_only_new,
    ]
    for test in tests:
        test(module)
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
