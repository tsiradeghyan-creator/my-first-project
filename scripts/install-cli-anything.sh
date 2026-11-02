#!/usr/bin/env bash
# Install HKUDS/CLI-Anything: CLI-Hub + every agent-harness CLI + the desktop backends they drive.
# Works on the Cloud container (Ubuntu, apt) and on the laptop (macOS, brew).
# Usage: bash scripts/install-cli-anything.sh [--no-apps]
set -uo pipefail
SRC="${CLI_ANYTHING_SRC:-$HOME/.cache/cli-anything-src}"
VENV="${CLI_ANYTHING_VENV:-$HOME/.cli-anything-venv}"
BIN="${CLI_ANYTHING_BIN:-$HOME/.local/bin}"
APPS=1; [ "${1:-}" = "--no-apps" ] && APPS=0

echo "== 1/4 source"
if [ -d "$SRC/.git" ]; then git -C "$SRC" pull -q --ff-only; else git clone -q --depth 1 https://github.com/HKUDS/CLI-Anything.git "$SRC"; fi

echo "== 2/4 backend apps"
if [ $APPS = 1 ]; then
  if command -v apt-get >/dev/null; then
    SUDO=""; [ "$(id -u)" != 0 ] && SUDO=sudo
    $SUDO apt-get update -qq
    DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -q --no-install-recommends \
      blender gimp inkscape kdenlive melt shotcut audacity krita musescore3 calibre obs-studio \
      qgis cloudcompare sox xvfb godot3 openrefine lldb xdotool imagemagick ffmpeg libreoffice \
      libasound2-dev pkg-config python3.12-venv \
      mediainfo openscad qpdf pdftk-java libimage-exiftool-perl plantuml darktable rawtherapee hugo \
      prusa-slicer slic3r colmap vulkan-tools apitrace latexmk texlive-latex-base \
      texlive-latex-recommended texlive-fonts-recommended
  elif command -v brew >/dev/null; then
    brew install ffmpeg sox imagemagick
    brew install --cask blender gimp inkscape kdenlive shotcut audacity krita musescore calibre \
      obs libreoffice qgis freecad godot drawio zotero obsidian || true
  else
    echo "no apt or brew: install the apps by hand"
  fi
  command -v npm >/dev/null && PUPPETEER_SKIP_DOWNLOAD=1 npm install -g -s @mermaid-js/mermaid-cli pm2 || true
  # mmdc needs a Chromium; on Cloud use the preinstalled Playwright one
  C=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux*/chrome 2>/dev/null | head -1)
  [ -n "$C" ] && echo "{\"executablePath\":\"$C\",\"args\":[\"--no-sandbox\"]}" > "$HOME/.puppeteerrc.json"
fi

echo "== 3/4 python CLIs"
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q -U pip setuptools wheel
"$VENV/bin/pip" install -q "$SRC/cli-hub"
ok=0; fail=""
for d in "$SRC"/*/agent-harness; do
  n=$(basename "$(dirname "$d")")
  [ -f "$d/setup.py" ] || [ -f "$d/pyproject.toml" ] || continue
  if "$VENV/bin/pip" install -q "$d" >/dev/null 2>&1; then ok=$((ok+1)); else fail="$fail $n"; fi
done
echo "installed $ok harnesses; failed:${fail:- none}"

# Harnesses that pin Python <3.13 get their own 3.12 venv
PY312=$(command -v python3.12 || true)
if [ -n "$PY312" ]; then
  "$PY312" -m venv "$VENV-py312" && "$VENV-py312/bin/pip" install -q -U pip
  for n in videocaptioner cloudanalyzer; do
    "$VENV-py312/bin/pip" install -q "$SRC/$n/agent-harness" >/dev/null 2>&1 && echo "py3.12: $n ok" || echo "py3.12: $n FAILED"
  done
  # Upstream bug: videocaptioner imports core/review.py, which was never committed
  HERE="$(cd "$(dirname "$0")" && pwd)"
  for D in "$VENV-py312"/lib/python3.*/site-packages/cli_anything/videocaptioner/core; do
    [ -d "$D" ] && [ ! -f "$D/review.py" ] && cp "$HERE/patches/videocaptioner_review.py" "$D/review.py" && echo "patched videocaptioner review.py"
  done
fi
# Free providers the cli-hub workflow matrices look for (video, image, research, 3D)
for pk in yt-dlp you-get spotdl scdl bandcamp-downloader "scenedetect[opencv-headless]" opencv-python-headless \
  moviepy pydub pysubs2 pypdf pdfplumber pdf2image python-docx openpyxl python-pptx reportlab weasyprint \
  cairosvg svgwrite svgpathtools trafilatura readability-lxml lxml duckduckgo-search googlesearch-python \
  habanero bibtexparser pyzotero pylatex pygltflib laspy rawpy ffmpeg-python faster-whisper \
  ffmpeg-quality-metrics librosa soundfile noisereduce build123d cadquery pymeshlab; do
  "$VENV/bin/pip" install -q "$pk" >/dev/null 2>&1 || echo "extra FAILED: $pk"
done
# Sketch is a Node package, not Python
command -v npm >/dev/null && (cd "$SRC/sketch/agent-harness" && npm install -s && npm install -g -s .) >/dev/null 2>&1 && echo "sketch ok"

# Seed cli-hub's registry cache from the checkout. cli-hub falls back to this cache
# when hkuds.github.io is unreachable (the Cloud proxy blocks it).
mkdir -p "$HOME/.cli-hub"
for f in registry public_registry matrix_registry; do
  python3 -c "import json;print(json.dumps({'_cached_at':0,'data':json.load(open('$SRC/$f.json'))}))" \
    > "$HOME/.cli-hub/${f}_cache.json"
done

echo "== 4/4 PATH"
mkdir -p "$BIN"
for f in "$VENV"/bin/cli-anything-* "$VENV-py312"/bin/cli-anything-* "$VENV"/bin/cli-hub \
         "$VENV"/bin/{yt-dlp,you-get,spotdl,scdl,bandcamp-dl,scenedetect,ffmpeg-quality-metrics}; do [ -e "$f" ] && ln -sf "$f" "$BIN/"; done

# Tell cli-hub what is installed (we installed from source, not via `cli-hub install`)
python3 - "$SRC/registry.json" "$BIN" <<'PY'
import json, os, sys
reg, bindir = sys.argv[1], sys.argv[2]
path = os.path.expanduser("~/.cli-hub/installed.json")
data = json.load(open(path)) if os.path.exists(path) else {}
for c in json.load(open(reg))["clis"]:
    ep = c.get("entry_point")
    if ep and os.path.exists(os.path.join(bindir, ep)):
        data[c["name"]] = {"version": c.get("version"), "entry_point": ep, "source": "harness", "strategy": "source"}
json.dump(data, open(path, "w"), indent=2)
print(f"cli-hub knows {len(data)} installed CLIs")
PY
case ":$PATH:" in *":$BIN:"*) ;; *) echo "add to your shell rc:  export PATH=\"$BIN:\$PATH\"";; esac
echo "Mermaid offline (Cloud): python3 scripts/mermaid-local-renderer.py &  export MERMAID_RENDERER_URL=http://127.0.0.1:8765"
echo "done: $(ls "$BIN" | grep -c '^cli-anything-') CLIs in $BIN"
