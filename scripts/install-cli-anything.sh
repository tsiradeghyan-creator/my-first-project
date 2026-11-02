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
      qgis cloudcompare sox xvfb godot3 openrefine lldb xdotool imagemagick ffmpeg libreoffice
  elif command -v brew >/dev/null; then
    brew install ffmpeg sox imagemagick
    brew install --cask blender gimp inkscape kdenlive shotcut audacity krita musescore calibre \
      obs libreoffice qgis freecad godot drawio zotero obsidian || true
  else
    echo "no apt or brew: install the apps by hand"
  fi
  command -v npm >/dev/null && npm install -g -s @mermaid-js/mermaid-cli pm2 || true
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

# Seed cli-hub's registry cache from the checkout. cli-hub falls back to this cache
# when hkuds.github.io is unreachable (the Cloud proxy blocks it).
mkdir -p "$HOME/.cli-hub"
for f in registry public_registry matrix_registry; do
  python3 -c "import json;print(json.dumps({'_cached_at':0,'data':json.load(open('$SRC/$f.json'))}))" \
    > "$HOME/.cli-hub/${f}_cache.json"
done

echo "== 4/4 PATH"
mkdir -p "$BIN"
for f in "$VENV"/bin/cli-anything-* "$VENV"/bin/cli-hub; do [ -e "$f" ] && ln -sf "$f" "$BIN/"; done
case ":$PATH:" in *":$BIN:"*) ;; *) echo "add to your shell rc:  export PATH=\"$BIN:\$PATH\"";; esac
echo "done: $(ls "$BIN" | grep -c '^cli-anything-') CLIs in $BIN"
