# THE LAST PAGE (60 s, 24 fps, 2.39:1)

A 2D anime short made entirely in code from the "Fable 5.5 launch film" prompt Tigran sent (screenshots of an X post, 2026-11-02). No image or video generators: every background is painted by a procedural gouache painter, every character drawing is built from cel shapes and hand-inked lines, the score and sound design are synthesised.

- `THE_LAST_PAGE.html` — the deliverable: one self-contained file, black letterboxed frame, one quiet play button, video and sound embedded.
- `THE_LAST_PAGE.mp4` — the same film as a plain video (easier on a phone).

## How it is made (`src/`)
- `core.py` — noise, the gouache painter (coarse-to-fine opaque strokes that follow the forms), variable-width ink lines with line boil.
- `fx.py` — shelves with thousands of unique books, light shafts, dust, lantern, paper birds, pages, pampas grass, cel layer lighting, post.
- `fox.py` — the fox: side and front model sheets, parameter poses rebuilt for every drawing, hard-edged cel shadow, walk cycle.
- `bg_tower.py` — tower, copper dome, cloud sea (flat value-banded cumulus).
- `shot1.py` … `shot9.py` — the nine shots, timed to the prompt. Characters animate on twos with held keys; blinks and hard key poses on ones.
- `audio.py` — wind, felt-piano motif (original), low strings, creaks, paper roar, orchestral swell, timpani, wingbeat, single last note. ~ -18 LUFS.
- `render.py` / `render_all.sh` — frames; `build_html.py` — packs the HTML.

Rebuild: `PY=python3 FRAMES=/tmp/frames bash src/render_all.sh`, `python3 src/audio.py score.wav`, encode with ffmpeg (see NOTES), `python3 src/build_html.py film.mp4 THE_LAST_PAGE.html`. Needs numpy, scipy, opencv, skia-python, soundfile, matplotlib.

Fonts (OFL): Kaushan Script (title), Yuji Syuku (subtitle line and the 寓話 hanko).
