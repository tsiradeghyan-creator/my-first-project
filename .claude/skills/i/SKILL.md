---
name: i
description: "-I- : animate a person in a still image with code — walking, running, talking with Armenian lip-sync, blinking, gestures, camera moves — from a few-line .i script. Use when Tigran asks to make characters in his stills/storyboards move or speak without a video generator, says '-I-', 'I-ով', 'շարժիր կերպարին', 'խոսացրու', or wants an animatic with acting."
---

# -I-

Tool lives in `tools/I/` (read its README for the full language). Pipeline: mediapipe pose+face+segmentation (offline) → triangle-mesh rig with skinning → procedural motions → face mesh visemes → skia render → MP4 with espeak-ng (hy) or supplied voice.

## Setup (fresh Cloud container)
```
python3.12 -m venv /opt/i-env && /opt/i-env/bin/pip install -q mediapipe==0.10.14 skia-python scipy soundfile opencv-contrib-python-headless
apt-get install -y espeak-ng ffmpeg
```
(Python 3.13 has no mediapipe wheel; use 3.12.)

## Use
1. Check the rig: `PYTHONPATH=tools/I /opt/i-env/bin/python -m i rig IMAGE --debug /tmp/rig.png` and look at it.
2. Write a `.i` script next to the images (see `reels/tigran-the-great/I_demo/demo.i`).
3. Render: `PYTHONPATH=tools/I /opt/i-env/bin/python -m i run film.i -o film.mp4`.

## Rules of thumb
- Talking: front or 3/4 close-ups (face must be detected). For a real voice pass `wav FILE` (ElevenLabs).
- Walking: profile figures walk sideways; frontal figures walk toward camera (scale grows).
- Avoid raise_arm when arms are under a cape. Give a clean `bg` when the actor travels far.
- Tell Tigran honestly what reads well and what stretches; check frames before sending.
