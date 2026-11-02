#!/usr/bin/env bash
# Render every shot in 4 parallel workers. FRAMES env var = output dir.
cd "$(dirname "$0")"
P=${PY:-python3}
( $P render.py shot1 && $P render.py shot2 && $P render.py shot3 ) &
( $P render.py shot4 && $P render.py shot5 ) &
( $P render.py shot6 && $P render.py shot7 ) &
( $P render.py shot8 && $P render.py shot9 ) &
wait
