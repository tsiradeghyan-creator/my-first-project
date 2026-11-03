#!/usr/bin/env python3
"""Build the ChatGPT pack (Custom GPT) from the director-desk sources.

Usage: python3 build_pack.py [--out DIR]   -> DIR/Maghakian_Script_Desk_GPT/ and DIR/Maghakian_Script_Desk_GPT.zip
"""
import argparse
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KNOWLEDGE = [
    "scripts/kit_docx_to_fountain.py", "scripts/screenplay.py", "scripts/proofread.py", "scripts/season.py",
    "scripts/pack.py", "scripts/treatment_pdf.py", "references/pack.md", "examples/pack_hy.md",
    "fonts/FreeMono.ttf", "fonts/DejaVuSans.ttf", "fonts/DejaVuSans-Bold.ttf",
    "assets/maghakian_logo_dark.png", "assets/maghakian_logo_light.png",
    "references/proofreading_hy.md", "references/format_spec.md", "examples/sample_hy.fountain",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    dst = os.path.join(a.out, "Maghakian_Script_Desk_GPT")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(os.path.join(dst, "knowledge"))
    for rel in KNOWLEDGE:
        shutil.copy(os.path.join(ROOT, rel), os.path.join(dst, "knowledge", os.path.basename(rel)))
    for f in ("INSTRUCTIONS.md", "HOW_TO_hy.md"):
        shutil.copy(os.path.join(HERE, f), os.path.join(dst, f))
    for lic in ("LICENSE-FreeFont.txt", "LICENSE-DejaVu.txt"):
        shutil.copy(os.path.join(ROOT, "fonts", lic), os.path.join(dst, lic))
    zp = shutil.make_archive(dst, "zip", a.out, "Maghakian_Script_Desk_GPT")
    print("wrote", dst, zp)


if __name__ == "__main__":
    main()
