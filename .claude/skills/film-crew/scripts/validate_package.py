#!/usr/bin/env python3
"""Mechanical gate for a film-crew package. Judgment stays with the model; hard limits live here.

Usage: python3 validate_package.py <project-folder> [--max-call 30] [--json]
Exit 0 = no FAIL, 1 = at least one FAIL. Warnings never fail the gate.
Checks: files present · one card per shot with handoffs and a prompt · one contract per cut with its fields ·
prompts copy-ready (no placeholders, no director names, no XML-like tags) · time slices continuous, from 0, plain
seconds, >= 3 s, within the per-call limit · reference counts within Seedance 2.5 limits · no corrupted characters.
"""
import json, re, sys
from pathlib import Path

FILES = ["00_brief", "01_director", "02_world", "03_costume", "04_camera_light", "05_edit_plan",
         "06_shot_list", "07_sound", "08_storyboard", "09_generation_plan", "10_review"]
CONTRACT_FIELDS = ["a ends", "b starts", "axis", "light", "sound", "generation"]
PLACEHOLDER = re.compile(r"\[paste|verbatim\]|<insert|\{\{|\bTODO\b|\bTBD\b|\[LOOK:|\[SET:|\[LIGHT:|\[SOUND BED:", re.I)
CLOCK = re.compile(r"\b\d{1,2}:\d{2}:\d{2}\b|\[\s*\d{1,2}:\d{2}\s*[-–]")
SLICE = re.compile(r"\[\s*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*s(?:ec(?:onds?)?)?\s*\]", re.I)
CORRUPT = re.compile(r"[֐-׿�]")


def director_names(skill_dir: Path):
    names = {"in the style of"}
    for card in (skill_dir / "styles").glob("*.md") if (skill_dir / "styles").is_dir() else []:
        if card.name.startswith(("_", "README")):
            continue
        first = card.read_text(encoding="utf-8").splitlines()[0]
        full = first.lstrip("# ").split("—")[0].strip()
        if full:
            names.add(full.split()[-1].lower())  # surname: kubrick, tarantino, parajanov…
    names.update({"kubrick", "tarantino", "parajanov", "tarkovsky", "wong kar-wai", "kar-wai", "anderson", "fincher",
                  "villeneuve", "spielberg", "hitchcock", "scorsese", "leone", "coppola", "lynch", "godard",
                  "kurosawa", "bergman", "nolan"})  # works even when styles/ is not next to the script
    return names


def check(folder: Path, max_call: float):
    fails, warns = [], []
    text = {}
    for f in FILES:
        p = folder / f"{f}.md"
        if p.exists():
            text[f] = p.read_text(encoding="utf-8")
        else:
            fails.append(f"missing file {f}.md")

    for name, t in text.items():
        for m in CORRUPT.finditer(t):
            line = t[:m.start()].count("\n") + 1
            fails.append(f"{name}.md:{line} corrupted character U+{ord(m.group()):04X}")

    sb = text.get("08_storyboard", "")
    cards = re.split(r"(?m)^#{2,4}\s+SHOT\s+", sb)[1:]
    n_shots = len(cards)
    if sb and n_shots == 0:
        fails.append("08_storyboard: no '### SHOT n' cards found")
    for i, card in enumerate(cards, 1):
        low = card.lower()
        if i > 1 and "handoff in" not in low:
            fails.append(f"SHOT {i}: no 'Handoff in'")
        if i < n_shots and "handoff out" not in low:
            fails.append(f"SHOT {i}: no 'Handoff out'")
    blocks = re.findall(r"```text\n(.*?)```", sb, re.S)
    if sb and not blocks:
        fails.append("08_storyboard: no ```text prompt blocks")

    names = director_names(Path(__file__).resolve().parent.parent)
    for b_i, b in enumerate(blocks, 1):
        tag = f"prompt #{b_i}"
        if PLACEHOLDER.search(b):
            fails.append(f"{tag}: placeholder left in prompt ({PLACEHOLDER.search(b).group()!r})")
        low = b.lower()
        for n in names:
            if re.search(r"\b" + re.escape(n) + r"\b", low):
                fails.append(f"{tag}: names a director/style ('{n}')")
        if re.search(r"<[A-Za-z][^<>]{0,40}>", b):
            warns.append(f"{tag}: XML-like tag in prompt")
        if CLOCK.search(b):
            fails.append(f"{tag}: clock notation ({CLOCK.search(b).group()!r}) — use plain seconds [0-5s]")
        slices = [(float(a), float(c)) for a, c in SLICE.findall(b)]
        if slices:
            if slices[0][0] != 0:
                fails.append(f"{tag}: first slice starts at {slices[0][0]} s, not 0")
            for (a1, b1), (a2, b2) in zip(slices, slices[1:]):
                if a2 != b1:
                    fails.append(f"{tag}: slices not continuous ({a1}-{b1} then {a2}-{b2})")
            for a, c in slices:
                if c - a < 3:
                    warns.append(f"{tag}: slice {a}-{c}s shorter than 3 s (ok only for a single hit)")
            long_video = "long video" in low or "ultra long" in low
            if slices[-1][1] > max_call and not long_video:
                fails.append(f"{tag}: {slices[-1][1]} s exceeds the per-call limit {max_call} s")
        for kind, cap in (("image", 30), ("video", 10), ("audio", 10)):
            ids = set(re.findall(rf"@{kind}\s*(\d+)", b, re.I))
            if len(ids) > cap:
                fails.append(f"{tag}: {len(ids)} @{kind} references > {cap}")
        letters = [ch for ch in re.sub(r"\{[^}]*\}|\"[^\"]*\"", "", b) if ch.isalpha()]
        if letters and sum(not ch.isascii() for ch in letters) / len(letters) > 0.05:
            warns.append(f"{tag}: prompt body is not mostly English")

    ep = text.get("05_edit_plan", "")
    cuts = re.split(r"(?m)^(?:#{2,4}\s*)?(?:\*\*)?CUT\s+\d+\s*(?:→|->)\s*\d+", ep)
    heads = re.findall(r"(?m)^(?:#{2,4}\s*)?(?:\*\*)?CUT\s+(\d+)\s*(?:→|->)\s*(\d+)", ep)
    if n_shots > 1 and len(heads) < n_shots - 1:
        fails.append(f"05_edit_plan: {len(heads)} cut contracts for {n_shots} shots (need {n_shots - 1})")
    for (a, b), body in zip(heads, cuts[1:]):
        body = body[:2500].lower()
        missing = [f for f in CONTRACT_FIELDS if f not in body]
        if missing:
            fails.append(f"CUT {a}→{b}: contract missing {', '.join(missing)}")

    return {"folder": str(folder), "shots": n_shots, "cuts": len(heads), "prompts": len(blocks),
            "fail": fails, "warn": warns, "pass": not fails}


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    max_call = float(args[args.index("--max-call") + 1]) if "--max-call" in args else 30.0
    res = check(Path(args[0]).expanduser(), max_call)
    if "--json" in args:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print(f"{'PASS' if res['pass'] else 'FAIL'} — {res['shots']} shots, {res['cuts']} cuts, {res['prompts']} prompts")
        for f in res["fail"]:
            print("  FAIL", f)
        for w in res["warn"]:
            print("  warn", w)
    sys.exit(0 if res["pass"] else 1)


if __name__ == "__main__":
    main()
