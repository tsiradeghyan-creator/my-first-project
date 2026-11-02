"""Tigran the Great — trailer v2 (structure after The King trailer).
Picture: teaser v1 (graded) + Veo/Dreamina clips (graded) + graded stills + text cards.
Sound: fully synthesized score + SFX in numpy, plus the clips' own diegetic audio.
Run: python3 -I build_trailer.py   (needs ffmpeg, numpy, Pillow)
"""
import os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(ROOT)
C = P + "/clips/"
ST = P + "/stills_king_grade/"
T = P + "/teaser_v1_KING.mp4"
TMP = os.environ.get("TMPDIR_TRAILER", "/tmp/trailer_build")
os.makedirs(TMP, exist_ok=True)
W, H, FPS, SR = 1280, 720, 24, 48000
LIGHT = "/usr/share/fonts/truetype/inter/Inter-ExtraLight.ttf"
SERIF = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"

def font_path(name):
    out = subprocess.run(["fc-match", "-f", "%{file}", name], capture_output=True, text=True).stdout
    return out
LIGHT = font_path("Inter:style=ExtraLight") or LIGHT

# ---------------- edit decision list ----------------
# (kind, name, args..., duration-in-output)
E = []
def clip(src, a, b, speed=1.0, sfx=None, audio=True):
    E.append(dict(k="clip", src=src, a=a, b=b, sp=speed, d=(b - a) / speed, sfx=sfx, audio=audio))
def still(src, d, z0=1.0, z1=1.08, sfx=None):
    E.append(dict(k="still", src=src, d=d, z0=z0, z1=z1, sfx=sfx))
def card(text, d, sfx=None, big=False):
    E.append(dict(k="card", text=text, d=d, big=big, sfx=sfx))
def black(d, sfx=None):
    E.append(dict(k="black", d=d, sfx=sfx))

# ACT 1 — the world (slow)
black(1.5, "wind_in")
clip(C + "V1_ararat_rider_KING.mp4", 0.8, 6.3, 1.0, "own")
card("FROM THE CASPIAN SEA\nTO THE MEDITERRANEAN", 2.8, "lowhit")
clip(T, 9.08, 9.92, 1.0, "hoof", audio=False)
clip(T, 10.08, 11.12, 0.8, "procession", audio=False)
clip(T, 11.28, 12.12, 0.8, "procession", audio=False)
card("ONE KING RULED\nOVER KINGS", 2.6, "lowhit")
clip(T, 12.28, 13.62, 1.0, "crowd", audio=False)
clip(T, 13.78, 14.62, 1.0, "crowd", audio=False)
clip(T, 14.78, 16.12, 1.0, "hall", audio=False)
clip(T, 16.24, 16.66, 0.5, "hall", audio=False)
# ACT 2 — Rome (pulse)
black(0.6, None)
card("THEN ROME CAME", 2.4, "boom")
clip(C + "V4_pushin_KING.mp4", 0.4, 3.4, 1.0, "own")
clip(T, 16.78, 17.62, 1.0, "march", audio=False)
clip(T, 17.78, 18.62, 1.0, "march", audio=False)
clip(T, 3.08, 6.02, 1.0, "tent", audio=False)
clip(T, 6.18, 8.92, 1.0, "tent", audio=False)
card("AND HIS OWN SON\nSTOOD WITH ROME", 2.8, "boom")
# ACT 3 — fire and battle (fast)
clip(C + "V2_fire_cut_KING.mp4", 0.1, 2.9, 1.0, "own")
clip(C + "V3a_hooves_KING.mp4", 0.0, 1.25, 1.0, "own_hit")
still(ST + "B02_shields_KING.png", 0.5, 1.06, 1.0, "hit")
clip(C + "V3b_dust_KING.mp4", 0.0, 1.1, 1.0, "own_hit")
clip(C + "V3a_hooves_KING.mp4", 1.25, 1.6, 1.0, "own_hit")
# ACT 4 — the surrender (silence, then emotion)
clip(T, 18.78, 19.62, 0.6, "gate", audio=False)
still(ST + "A10_ring_reins_KING.png", 2.2, 1.0, 1.07, None)
clip(C + "V5_sword_KING.mp4", 1.0, 6.2, 1.0, "sword", audio=False)
clip(C + "V6_crown_KING.mp4", 1.0, 7.9, 1.0, "own")
still(ST + "B13_crown_in_dirt_KING.png", 2.6, 1.0, 1.06, None)
black(2.0, None)
card("TIGRAN  THE  GREAT", 5.0, "title", big=True)
card("COMING SOON", 2.4, None)

t = 0.0
for e in E:
    e["t"] = t; t += e["d"]
TOTAL = t
print("total %.2f s, %d events" % (TOTAL, len(E)))

# ---------------- picture ----------------
def tracked(draw, cx, y, text, font, track, fill):
    widths = [draw.textlength(ch, font=font) for ch in text]
    tw = sum(widths) + track * (len(text) - 1)
    x = cx - tw / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill); x += w + track

def card_png(e, path):
    im = Image.new("RGB", (W, H), "black"); d = ImageDraw.Draw(im)
    if e["big"]:
        f = ImageFont.truetype(SERIF, 64)
        tracked(d, W / 2, H / 2 - 44, e["text"], f, 16, (235, 235, 235))
        d.line([(W / 2 - 60, H / 2 + 46), (W / 2 + 60, H / 2 + 46)], fill=(217, 4, 41), width=1)
    else:
        f = ImageFont.truetype(LIGHT, 30)
        lines = e["text"].split("\n"); lh = 52
        y0 = H / 2 - lh * len(lines) / 2
        for i, ln in enumerate(lines):
            tracked(d, W / 2, y0 + i * lh, ln, f, 11, (225, 225, 225))
    im.save(path)

def render(i, e):
    out = "%s/seg%03d.mp4" % (TMP, i)
    enc = ["-an", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", "-r", str(FPS)]
    n = max(1, round(e["d"] * FPS))
    if e["k"] == "clip":
        vf = "setpts=(PTS-STARTPTS)/%f,fps=%d,scale=%d:%d:flags=lanczos,setsar=1" % (e["sp"], FPS, W, H)
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(e["a"]), "-i", e["src"], "-t", str(e["b"] - e["a"]),
               "-vf", vf, "-frames:v", str(n)] + enc + [out]
    elif e["k"] == "still":
        z = "%f+(%f-%f)*on/%d" % (e["z0"], e["z1"], e["z0"], n)
        vf = ("scale=2560:-2,zoompan=z='%s':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=%d:s=%dx%d:fps=%d,setsar=1"
              % (z, n, W, H, FPS))
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", e["src"], "-vf", vf, "-frames:v", str(n)] + enc + [out]
    else:
        png = "%s/card%03d.png" % (TMP, i)
        if e["k"] == "card": card_png(e, png)
        else: Image.new("RGB", (W, H), "black").save(png)
        fade = ""
        if e["k"] == "card":
            fi = 0.6 if e["big"] else 0.35
            fade = ",fade=in:st=0:d=%f,fade=out:st=%f:d=0.35" % (fi, e["d"] - 0.35)
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", png, "-vf", "fps=%d,setsar=1%s" % (FPS, fade),
               "-frames:v", str(n)] + enc + [out]
    subprocess.run(cmd, check=True)
    e["n"] = n
    return out

segs = [render(i, e) for i, e in enumerate(E)] if not os.environ.get('SKIP_PIC') else [None]*len(E)
if os.environ.get('SKIP_PIC'):
    for e in E: e['n'] = max(1, round(e['d'] * FPS))
if not os.environ.get('SKIP_PIC'):
  with open(TMP + "/list.txt", "w") as f:
    for s in segs: f.write("file '%s'\n" % s)
# frame-exact timeline (durations rounded to frames)
t = 0.0
for e in E:
    e["t"] = t; e["d"] = e["n"] / FPS; t += e["d"]
TOTAL = t
pic = TMP + "/picture.mp4"
# letterbox 2.39:1 + fine grain
vf = "drawbox=x=0:y=0:w=iw:h=92:color=black:t=fill,drawbox=x=0:y=ih-92:w=iw:h=92:color=black:t=fill,noise=alls=5:allf=t+u"
if not os.environ.get('SKIP_PIC'): subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", TMP + "/list.txt", "-vf", vf,
                "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS), pic], check=True)

# ---------------- sound ----------------
N = int(TOTAL * SR) + SR
rng = np.random.default_rng(7)
mus = np.zeros((N, 2)); sfx = np.zeros((N, 2)); dia = np.zeros((N, 2))
tt = lambda d: np.arange(int(d * SR)) / SR

def put(buf, t0, x, g=1.0, pan=0.0):
    i = int(t0 * SR)
    if x.ndim == 1: x = np.stack([x * (1 - max(pan, 0)), x * (1 + min(pan, 0))], 1)
    j = min(N, i + len(x)); buf[i:j] += x[: j - i] * g

def env(n, a, r):
    e = np.ones(n); a = int(a * SR); r = int(r * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e

def bandnoise(d, lo, hi, color=0):
    n = int(d * SR); X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    if color: X[1:] /= (f[1:] / 100.0) ** (0.5 * color)
    y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)

def boom(d=3.0, f0=70, f1=32):
    x = tt(d); f = f1 + (f0 - f1) * np.exp(-x * 6)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 1.6)
    y += bandnoise(d, 30, 400, 1) * np.exp(-x * 9) * 0.5
    return np.tanh(y * 1.6)

def hit(d=1.2):
    x = tt(d)
    return np.tanh((np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-x * 25)) / SR) * np.exp(-x * 4)
                    + bandnoise(d, 200, 6000) * np.exp(-x * 30) * 0.8) * 1.8)

def saw(freq, d, nh=10):
    x = tt(d); return sum(np.sin(2 * np.pi * freq * k * x) / k for k in range(1, nh + 1))

def pad(freqs, d, a=1.5, r=1.5, nh=6):
    y = sum(saw(f * (1 + dt), d, nh) for f in freqs for dt in (-0.003, 0.003))
    lfo = 0.8 + 0.2 * np.sin(2 * np.pi * 0.2 * tt(d))
    return y / (len(freqs) * 2 * 2.0) * env(len(y), a, r) * lfo

def drone(d, f=36.71):
    x = tt(d)
    y = np.sin(2 * np.pi * f * x) + 0.6 * np.sin(2 * np.pi * f * 2 * x) + 0.25 * np.sin(2 * np.pi * f * 3.002 * x)
    return y * (0.75 + 0.25 * np.sin(2 * np.pi * 0.07 * x)) / 1.8

def braam(d=6.0):
    y = sum(saw(f, d, 14) for f in (36.71, 73.42, 110.0, 146.83, 174.61)) / 5
    x = tt(d); return np.tanh(y * 2.2) * np.exp(-x * 0.55) * env(len(x), 0.02, 0.5)

def bell(f, d=4.0):
    x = tt(d)
    return (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(2 * np.pi * f * 2.76 * x) * np.exp(-x * 3)) * np.exp(-x * 1.2) * env(len(x), 0.005, 0.3)

def whoosh(d=1.2):
    n = bandnoise(d, 300, 4000); return n * np.sin(np.linspace(0, np.pi, len(n))) ** 2

def riser(d):
    x = tt(d); f = 80 * 2 ** (x / d * 3)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + bandnoise(d, 1000, 9000) * 0.5) * (x / d) ** 2

def thump(d=0.35, f=48):
    x = tt(d); return np.sin(2 * np.pi * f * x) * np.exp(-x * 14)

def crackle(d, rate=25):
    n = int(d * SR); y = np.zeros(n); k = rng.integers(0, n, int(rate * d))
    y[k] = rng.uniform(-1, 1, len(k)); kern = np.exp(-np.arange(200) / 30) * rng.standard_normal(200)
    y = np.convolve(y, kern)[:n]; return y / (np.abs(y).max() + 1e-9) + bandnoise(d, 80, 600, 1) * 0.25

def audio_of(src, a, b, speed):
    w = TMP + "/a.wav"
    af = "atempo=%f" % speed if speed >= 0.5 else "atempo=0.5,atempo=%f" % (speed / 0.5)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", src, "-af", af,
                    "-ar", str(SR), "-ac", "2", "-f", "f32le", w], check=True)
    return np.fromfile(w, np.float32).reshape(-1, 2).astype(np.float64)

def db(x): return 10 ** (x / 20)

def at(name):  # start time of first card whose text contains name
    return next(e["t"] for e in E if e["k"] == "card" and name in e["text"])

# --- diegetic / SFX per event
for e in E:
    s, d = e.get("sfx"), e["d"]
    if e["k"] == "clip" and e.get("audio") and s in ("own", "own_hit"):
        x = audio_of(e["src"], e["a"], e["b"], e["sp"])[: int(d * SR)]
        pk = np.abs(x).max() + 1e-9
        g0 = -20 if "V1_" in e["src"] else (-16 if "V6_" in e["src"] else (-8 if s == "own" else -6))
        x = x / pk * db(g0)
        x *= env(len(x), 0.01, 0.04)[:, None]
        put(dia, e["t"], x)
    if s == "wind_in":
        put(sfx, e["t"], bandnoise(d + 6.0, 100, 1500, 1) * env(int((d + 6.0) * SR), d, 1.5), db(-24))
    elif s == "hoof":
        put(sfx, e["t"] + 0.12, thump(0.5, 60) + bandnoise(0.5, 300, 3000) * np.exp(-tt(0.5) * 25) * 0.4, db(-8))
    elif s == "procession":
        for k in np.arange(0.05, d, 0.42):
            put(sfx, e["t"] + k, thump(0.3, 70) * 0.8 + bandnoise(0.3, 400, 2500) * np.exp(-tt(0.3) * 30) * 0.3, db(-16), rng.uniform(-.3, .3))
        put(sfx, e["t"], bandnoise(d, 150, 900, 1) * env(int(d * SR), .1, .1), db(-30))
    elif s == "crowd":
        put(sfx, e["t"], bandnoise(d, 200, 1200, 1) * env(int(d * SR), .15, .15), db(-24))
    elif s == "hall":
        put(sfx, e["t"], bandnoise(d, 60, 400, 2) * env(int(d * SR), .1, .1), db(-30))
    elif s == "march":
        for k in np.arange(0.0, d, 0.27):
            put(sfx, e["t"] + k, thump(0.25, 55) + bandnoise(0.25, 3000, 9000) * np.exp(-tt(0.25) * 40) * 0.25, db(-10))
    elif s == "tent":
        put(sfx, e["t"], crackle(d) * env(int(d * SR), .2, .2), db(-24))
    elif s == "sword":
        put(sfx, e["t"], bandnoise(d, 60, 500, 2) * env(int(d * SR), .5, .5), db(-34))
        for k, g in ((0.8, -24), (2.6, -20), (3.3, -26)):
            put(sfx, e["t"] + k, bandnoise(0.6, 300, 2500) * np.exp(-tt(0.6) * 6), db(g))   # leather creak
        put(sfx, e["t"] + 3.0, bell(2200, 1.0) * 0.2, db(-26))                              # metal tick
    elif s == "gate":
        x = tt(d + 0.5); cr = np.sin(2 * np.pi * np.cumsum(55 + 25 * np.sin(2 * np.pi * 0.7 * x)) / SR)
        put(sfx, e["t"], (cr * 0.6 + bandnoise(d + 0.5, 100, 2000) * 0.4) * env(len(x), 0.2, 0.4), db(-18))
    if s in ("lowhit",): put(mus, e["t"], boom(2.5, 60, 30), db(-14))
    if s in ("boom",): put(mus, e["t"], boom(3.5), db(-8)); put(sfx, e["t"] - 0.6, whoosh(0.7), db(-22))
    if s in ("own_hit", "hit"): put(mus, e["t"], hit(), db(-6))

# --- score
tR = at("THEN ROME"); tS = at("HIS OWN SON"); tFire = tS + next(e["d"] for e in E if e["k"] == "card" and "HIS OWN SON" in e["text"])
gate = next(e for e in E if e.get("sfx") == "gate"); tGate = gate["t"]
tTitle = at("TIGRAN"); tBlack = tTitle - 2.0
crown = next(e for e in E if "V6" in e.get("src", ""))
# Act 1: drone + Dm pad
put(mus, 1.0, drone(tR - 1.0) * env(int((tR - 1.0) * SR), 3, 1.0), db(-20))
put(mus, at("CASPIAN"), pad([146.83, 174.61, 220.0], tR - at("CASPIAN"), 2.5, 1.2), db(-20))
put(mus, at("RULED"), bell(587.33, 5) * 0.5, db(-22)); put(mus, at("RULED") + 1.2, bell(440, 5) * 0.5, db(-24))
# Act 2: pulse 72 bpm, darker pad
d2 = tFire - tR
put(mus, tR, drone(d2, 36.71) * env(int(d2 * SR), 0.5, 0.3), db(-12))
put(mus, tR + 2.4, pad([116.54, 146.83, 174.61], d2 - 2.4, 2.0, 0.5), db(-21))
for k in np.arange(tR + 2.4, tFire - 0.2, 60 / 72):
    put(mus, k, thump(0.4, 45), db(-9)); put(mus, k + 0.22, thump(0.3, 45), db(-16))
# Act 3: riser over fire, drums under battle
put(mus, tFire, riser(2.8), db(-12))
for k in np.arange(tFire + 1.4, tGate - 0.05, 60 / 140 / 2):
    put(mus, k, thump(0.2, 62) + np.pad(bandnoise(0.12, 2000, 8000) * np.exp(-tt(0.12) * 50) * 0.3, (0, int(0.2 * SR) - int(0.12 * SR))), db(-12), rng.uniform(-.4, .4))
put(mus, tFire, drone(tGate - tFire, 36.71), db(-12))
# Act 4: hard cut to near-silence at gate, then emotional pad Dm - Bb - F - A
tP = tGate + gate["d"]; chords = [[146.83, 174.61, 220.0], [116.54, 146.83, 174.61], [174.61, 220.0, 261.63], [110.0, 138.59, 164.81]]
dP = (tBlack - tP) / 4
for i, ch in enumerate(chords):
    g = -22 + 3 * i
    put(mus, tP + i * dP, pad(ch + [ch[0] / 2], dP + 1.2, 1.2, 1.4), db(g))
put(mus, tP, drone(tBlack - tP, 36.71) * env(int((tBlack - tP) * SR), 2, 0.05), db(-16))
put(mus, crown["t"] + 0.2, bell(587.33, 5), db(-20))
put(mus, crown["t"] + 3.6, bell(698.46, 5), db(-18))   # the crown leaves the hands
put(mus, crown["t"] + 4.4, bell(587.33, 6), db(-19))
put(mus, tBlack - 1.6, riser(1.6), db(-16))
# Title
put(mus, tTitle, braam(6.0), db(-4)); put(mus, tTitle, boom(5.0, 50, 28), db(-4))

mix = mus + sfx + dia
# hard silence for the 2 s black before the title
i0, i1 = int((tBlack + 0.02) * SR), int(tTitle * SR); fade = int(0.04 * SR)
mix[i0 - fade:i0] *= np.linspace(1, 0, fade)[:, None]; mix[i0:i1] = 0
# simple room reverb on music+sfx
ir = rng.standard_normal(int(2.2 * SR)) * np.exp(-np.arange(int(2.2 * SR)) / SR * 3.0); ir /= np.abs(ir).sum() ** 0.5 * 6
wet = np.zeros_like(mix)
L = len(mix) + len(ir); nfft = 1 << (L - 1).bit_length(); IR = np.fft.rfft(ir, nfft)
for c in range(2):
    wet[:, c] = np.fft.irfft(np.fft.rfft(mus[:, c] + sfx[:, c], nfft) * IR, nfft)[: len(mix)]
wet[i0:i1] = 0
mix = mix + wet * 0.35
mix = mix[: int(TOTAL * SR)]
mix *= env(len(mix), 0, 0.8)[:, None]
mix = np.tanh(mix / (np.abs(mix).max() + 1e-9) * 1.4) * 0.89
mix.astype(np.float32).tofile(TMP + "/mix.f32")
import re
m = subprocess.run(["ffmpeg", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", TMP + "/mix.f32", "-af", "ebur128",
                    "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", m)[-1])   # linear gain keeps the dynamics (no loudnorm pumping)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", TMP + "/mix.f32",
                "-af", "volume=%.2fdB,alimiter=limit=0.6:attack=2:release=80:level=disabled" % (-15 - I), "-ar", str(SR), TMP + "/mix.wav"], check=True)

out = ROOT + "/Tigran_the_Great_trailer_v2.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", TMP + "/mix.wav", "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True)
with open(ROOT + "/EDL.txt", "w") as f:
    for e in E:
        f.write("%6.2f  %5.2f  %-5s %s\n" % (e["t"], e["d"], e["k"], e.get("text", "").replace("\n", " / ") or
                                            "%s [%.2f-%.2f] x%.2f" % (os.path.basename(e.get("src", "")), e.get("a", 0), e.get("b", 0), e.get("sp", 1))))
print("wrote", out, "%.2f s" % TOTAL)
