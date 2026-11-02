"""Subtitle review helpers for cli-anything-videocaptioner.

Upstream HKUDS/CLI-Anything imports this module (core/review.py) but never committed it,
so the CLI crashes on start. This is a stand-in written to match the upstream tests:
build_review_report, ensure_subtitle_consistency, render_preview_frame, review_subtitles.
Installed by scripts/install-cli-anything.sh.
"""
from __future__ import annotations

import difflib
import os
import re
import shutil
import subprocess

_TIME = re.compile(r"^\d{1,2}:\d{2}:\d{2}[,.]\d{1,3}\s*-->")


def _subtitle_text(path: str) -> str:
    lines = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.isdigit() or _TIME.match(line) or line.upper().startswith("WEBVTT"):
                continue
            if line.startswith("Dialogue:"):  # ASS
                line = line.split(",", 9)[-1]
            line = re.sub(r"\{[^}]*\}|<[^>]+>", "", line)
            lines.append(line)
    return " ".join(lines)


def _words(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def build_review_report(subtitle_path: str, script_path: str | None = None,
                        max_diff_ratio: float = 0.12) -> dict:
    if not os.path.exists(subtitle_path):
        raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")
    sub_words = _words(_subtitle_text(subtitle_path))
    report = {"subtitle": os.path.abspath(subtitle_path), "subtitle_words": len(sub_words),
              "status": "pass", "diff_ratio": 0.0, "max_diff_ratio": max_diff_ratio}
    if script_path:
        with open(script_path, encoding="utf-8", errors="replace") as fh:
            script_words = _words(fh.read())
        ratio = 1.0 - difflib.SequenceMatcher(None, sub_words, script_words, autojunk=False).ratio()
        ratio = round(ratio, 4)
        report.update({"script": os.path.abspath(script_path), "script_words": len(script_words),
                       "diff_ratio": ratio, "status": "pass" if ratio <= max_diff_ratio else "fail"})
    return report


def ensure_subtitle_consistency(subtitle_path: str, script_path: str,
                                max_diff_ratio: float = 0.12) -> dict:
    report = build_review_report(subtitle_path, script_path=script_path, max_diff_ratio=max_diff_ratio)
    if report["status"] != "pass":
        raise RuntimeError(
            f"Subtitle/script review failed: drift {report['diff_ratio']:.3f} > {max_diff_ratio:.3f}"
        )
    return report


def render_preview_frame(video_path: str, subtitle_path: str, at: str = "00:00:05.000",
                         output_path: str | None = None) -> str:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not found on PATH")
    output_path = output_path or os.path.splitext(video_path)[0] + "_review.png"
    sub = subtitle_path.replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    cmd = ["ffmpeg", "-y", "-ss", at, "-i", video_path, "-vf", f"subtitles='{sub}'",
           "-frames:v", "1", output_path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip()[-500:] or "ffmpeg failed")
    return output_path


def review_subtitles(subtitle_path: str, script_path: str | None = None, max_diff_ratio: float = 0.12,
                     preview_video: str | None = None, preview_at: str | None = None,
                     preview_output: str | None = None) -> dict:
    report = build_review_report(subtitle_path, script_path=script_path, max_diff_ratio=max_diff_ratio)
    if preview_video:
        report["preview"] = render_preview_frame(preview_video, subtitle_path,
                                                 at=preview_at or "00:00:05.000",
                                                 output_path=preview_output)
    return report
