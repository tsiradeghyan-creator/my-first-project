#!/usr/bin/env python3
"""Smoke evals for consolidate-memory using only temporary files."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_DIR / "consolidate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("consolidate_under_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sandbox(module, tmp: Path):
    memory = tmp / ".memory"
    projects = tmp / ".claude" / "projects" / "demo"
    memory.mkdir(parents=True)
    projects.mkdir(parents=True)
    module.MEMORY_DIR = memory
    module.RECENT_MEM = memory / "recent-memory.md"
    module.LONG_MEM = memory / "long-term-memory.md"
    module.PROJECT_MEM = memory / "project-memory.md"
    module.LOG_FILE = memory / "consolidate.log"
    module.PROJECTS_DIR = tmp / ".claude" / "projects"
    module.RECENT_MEM.write_text(
        "# Recent Memory\n<!-- Last updated: 2026-01-01 -->\n\n## Rolling 48h Log\n",
        encoding="utf-8",
    )
    module.LONG_MEM.write_text("# Long Term\n\n## Patterns & Preferences\n", encoding="utf-8")
    module.PROJECT_MEM.write_text("# Project\n\n**Last updated:** 2026-01-01\n", encoding="utf-8")
    return projects / "session.jsonl"


def write_jsonl(path: Path):
    now = datetime.now(timezone.utc).isoformat()
    rows = [
        {
            "type": "user",
            "timestamp": now,
            "message": {
                "content": "I prefer Armenian Unicode in every response because transliteration breaks the brand voice."
            },
        },
        {
            "type": "assistant",
            "timestamp": now,
            "message": {
                "content": "completed Maghakian brand routing update. created a safer memory workflow."
            },
        },
    ]
    with path.open("w", encoding="utf-8") as f:
        f.write("{malformed json\n")
        for row in rows:
            f.write(json.dumps(row) + "\n")


def test_malformed_jsonl_ignored_and_facts_extracted(module):
    with tempfile.TemporaryDirectory() as d:
        path = sandbox(module, Path(d))
        write_jsonl(path)
        messages = module.read_recent_jsonl(hours=24)
        facts = module.extract_facts(messages)
        assert len(messages) == 2
        assert facts["preferences"]
        assert facts["completions"]


def test_dry_run_does_not_write(module):
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        path = sandbox(module, tmp)
        write_jsonl(path)
        facts = module.extract_facts(module.read_recent_jsonl(hours=24))
        before = {
            "recent": module.RECENT_MEM.read_text(encoding="utf-8"),
            "long": module.LONG_MEM.read_text(encoding="utf-8"),
            "project": module.PROJECT_MEM.read_text(encoding="utf-8"),
        }
        module.update_recent_memory(facts, dry_run=True)
        module.promote_to_long_term(facts, dry_run=True)
        module.update_project_memory(facts, dry_run=True)
        after = {
            "recent": module.RECENT_MEM.read_text(encoding="utf-8"),
            "long": module.LONG_MEM.read_text(encoding="utf-8"),
            "project": module.PROJECT_MEM.read_text(encoding="utf-8"),
        }
        assert before == after


def test_real_write_updates_expected_sections(module):
    with tempfile.TemporaryDirectory() as d:
        path = sandbox(module, Path(d))
        write_jsonl(path)
        facts = module.extract_facts(module.read_recent_jsonl(hours=24))
        module.update_recent_memory(facts, dry_run=False)
        module.promote_to_long_term(facts, dry_run=False)
        module.update_project_memory(facts, dry_run=False)
        assert "Recent User Requests" in module.RECENT_MEM.read_text(encoding="utf-8")
        assert "Auto-promoted" in module.LONG_MEM.read_text(encoding="utf-8")
        assert "Session Log" in module.PROJECT_MEM.read_text(encoding="utf-8")


def main():
    module = load_module()
    tests = [
        test_malformed_jsonl_ignored_and_facts_extracted,
        test_dry_run_does_not_write,
        test_real_write_updates_expected_sections,
    ]
    for test in tests:
        test(module)
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
