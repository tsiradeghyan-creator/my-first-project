"""Tigran the Great — trailer v3. Everything taken from The King (2019) trailer reference:
- colour: per-shot Lab transfer to the reference's measured exterior / interior statistics (ref_stats.npy), full chroma
- transitions: hard cuts; act breaks = fade to black (0.8 s) / card hard-in / shot fades up from black (0.6 s)
- titles: credits in a wide-tracked geometric sans (Montserrat 500), title in a Didone italic (Playfair Display italic)
  revealed by a soft left-to-right wipe, as in the reference
- sound: the clips' own recorded audio carries the trailer; music is only a low bowed drone + two sub hits
No stills, no zooms on stills. Source = ungraded originals.
"""
import os, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(ROOT); C = P + "/clips/"
T = "/root/.claude/uploads/2d65cf01-17eb-5529-814a-566d525666fd/2a209d2f-Tigran_the_Great_trailer_SFX.mp4"
if not os.path.exists(T): T = P + "/teaser_v1_original.mp4"
TMP = os.environ.get("TMPDIR_TRAILER", "/tmp/trailer_v3"); os.makedirs(TMP, exist_ok=True)
W, H, FPS, SR = 1280, 720, 24, 48000
SANS = ROOT + "/fonts/montserrat-latin-500-normal.woff2"; SERIF = ROOT + "/fonts/playfair-display-latin-400-italic.woff2"
REF = np.load(ROOT + "/ref_stats.npy")  # rows ext,int: meanL,a,b,stdL,a,b

E = []
def clip(src, a, b, sp=1.0, bed=None, own=True, fi=0, fo=0, g=0):
    E.append(dict(k="clip", src=src, a=a, b=b, sp=sp, d=(b - a) / sp, bed=bed, own=own, fi=fi, fo=fo, g=g))
def card(text, d): E.append(dict(k="card", text=text, d=d))
def black(d): E.append(dict(k="black", d=d))
def title(d): E.append(dict(k="title", d=d))

black(1.0)
clip(C + "V1_ararat_rider.mp4", 0.8, 6.6, fi=1.2, g=-6)
card("FROM THE CASPIAN SEA\nTO THE MEDITERRANEAN", 2.6)
clip(T, 9.08, 9.92, fi=0.6, own=False, bed=("V4_lictors_horse.mp4", 3.6, -8))
clip(T, 10.08, 11.12, 0.8, own=False, bed=("V4_lictors_horse.mp4", 4.5, -12))
clip(T, 11.28, 12.12, 0.8, own=False, bed=("V4_lictors_horse.mp4", 5.8, -12))
card("ONE KING\nRULED OVER KINGS", 2.4)
clip(T, 12.28, 13.62, fi=0.6, own=False, bed=("V1_ararat_rider.mp4", 1.0, -7))
clip(T, 13.78, 14.62, own=False, bed=("V1_ararat_rider.mp4", 3.0, -8))
clip(T, 14.78, 16.12, own=False, bed=("V6_crown.mp4", 0.5, -14))
clip(T, 16.24, 16.66, 0.5, own=False, fo=0.6, bed=("V6_crown.mp4", 2.0, -14))
card("THEN ROME CAME", 2.2)
clip(C + "V4_lictors_horse.mp4", 3.6, 6.9, fi=0.6, g=-3)
clip(T, 16.78, 17.62, own=False, bed=("V3_cavalry_fall.mp4", 6.0, -16))
clip(T, 17.78, 18.62, own=False, bed=("V3_cavalry_fall.mp4", 6.8, -14))
clip(T, 3.08, 6.02, own=False, bed=("V2_city_burning_try1.mp4", 0.2, -15))
clip(T, 6.18, 8.92, own=False, fo=0.8, bed=("V2_city_burning_try1.mp4", 1.2, -15))
card("AND HIS OWN SON\nSTOOD WITH ROME", 2.6)
clip(C + "V2_fire_cut.mp4", 0.1, 2.9, fi=0.6, g=-2)
clip(C + "V3_cavalry_fall.mp4", 2.9, 4.5, g=0)
clip(C + "V3_cavalry_fall.mp4", 4.6, 5.9, g=0)
black(0.25)
clip(T, 18.78, 19.62, 0.6, own=False, bed=("V1_ararat_rider.mp4", 5.0, -14))
clip(C + "V5_dreamina.mp4", 0.8, 5.0, 0.8, own=False, fi=0.6, bed=("V2_city_burning_try1.mp4", 1.0, -30))
clip(C + "V6_crown.mp4", 1.0, 7.9, fo=1.0, g=-2)
black(2.0)
title(5.5)
card("COMING SOON", 2.6)

# ---------------- colour ----------------
def grade_frames(frames):
    labs = [cv2.cvtColor(f.astype(np.float32) / 255, cv2.COLOR_BGR2LAB) for f in frames]
    s = np.concatenate([l.reshape(-1, 3)[::11] for l in labs[:: max(1, len(labs) // 6)]])
    m, sd = s.mean(0), s.std(0) + 1e-3
    ref = REF[0] if m[0] > 30 else REF[1]
    rm, rs = ref[:3], ref[3:]
    wgt = np.array([0.85, 1.0, 1.0], np.float32)
    out = []
    for lab in labs:
        t = (lab - m) / sd * rs + rm
        t = lab * (1 - wgt) + t * wgt
        t[..., 0] = np.clip(t[..., 0], 0, 100)
        bgr = np.clip(cv2.cvtColor(t.astype(np.float32), cv2.COLOR_LAB2BGR), 0, 1)
        out.append((bgr * 255 + .5).astype(np.uint8))
    return out

def read_frames(e, n):
    vf = "setpts=(PTS-STARTPTS)/%f,fps=%d,scale=%d:%d:flags=lanczos" % (e["sp"], FPS, W, H)
    if "V5_dreamina" in e["src"]: vf = "crop=1126:634:0:0," + vf     # crop off the watermark
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(e["a"]), "-i", e["src"], "-t", str(e["b"] - e["a"]), "-vf", vf,
                        "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    f = np.frombuffer(r, np.uint8).reshape(-1, H, W, 3)
    if len(f) < n: f = np.concatenate([f, np.repeat(f[-1:], n - len(f), 0)])
    return list(f[:n])

# ---------------- type ----------------
def tracked(d, cx, y, text, font, track, fill):
    ws = [d.textlength(ch, font=font) for ch in text]; x = cx - (sum(ws) + track * (len(text) - 1)) / 2
    for ch, w in zip(text, ws): d.text((x, y), ch, font=font, fill=fill); x += w + track
    return x

def card_img(text):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(SANS, 21)
    lines = text.split("\n"); lh = 34; y0 = H / 2 - lh * len(lines) / 2
    for i, ln in enumerate(lines): tracked(d, W / 2, y0 + i * lh, ln, f, 12, (232, 232, 232))
    return np.array(im)[:, :, ::-1]

def title_frames(n):
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
    big = ImageFont.truetype(SERIF, 104); small = ImageFont.truetype(SERIF, 30)
    word = "TIGRAN"; ws = [d.textlength(c, font=big) for c in word]; tr = 26
    tw = sum(ws) + tr * (len(word) - 1); sm = "THE GREAT"; sw = sum(d.textlength(c, font=small) for c in sm) + 6 * (len(sm) - 1)
    x0 = W / 2 - (tw + 24 + sw) / 2
    d.text((x0, H / 2 - 70), "", font=big)
    x = x0
    for c, w in zip(word, ws): d.text((x, H / 2 - 74), c, font=big, fill=215); x += w + tr
    x += 24
    for c in sm: d.text((x, H / 2 - 12), c, font=small, fill=215); x += d.textlength(c, font=small) + 6
    a = np.array(im).astype(np.float32) / 255
    xs = np.arange(W)[None, :]; out = []
    for i in range(n):
        t = i / FPS; edge = -250 + (W + 500) * min(1, t / 1.6)          # soft wipe left -> right
        mask = np.clip((edge - xs) / 250, 0, 1)
        fade = min(1, (n - i) / (0.6 * FPS))
        g = (a * mask * fade * 255).astype(np.uint8)
        out.append(np.repeat(g[:, :, None], 3, 2))
    return out

# ---------------- picture ----------------
t = 0.0
for e in E:
    e["n"] = max(1, round(e["d"] * FPS)); e["d"] = e["n"] / FPS; e["t"] = t; t += e["d"]
TOTAL = t
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "%dx%d" % (W, H), "-r", str(FPS),
                        "-i", "-", "-vf", "drawbox=x=0:y=0:w=iw:h=92:color=black:t=fill,drawbox=x=0:y=ih-92:w=iw:h=92:color=black:t=fill,noise=alls=4:allf=t",
                        "-c:v", "libx264", "-crf", "21", "-preset", "slow", "-pix_fmt", "yuv420p", TMP + "/picture.mp4"], stdin=subprocess.PIPE)
for e in E:
    n = e["n"]
    if e["k"] == "clip": fr = grade_frames(read_frames(e, n))
    elif e["k"] == "card": fr = [card_img(e["text"])] * n
    elif e["k"] == "title": fr = title_frames(n)
    else: fr = [np.zeros((H, W, 3), np.uint8)] * n
    for i, f in enumerate(fr):
        k = 1.0
        if e.get("fi"): k = min(k, i / (e["fi"] * FPS))
        if e.get("fo"): k = min(k, (n - 1 - i) / (e["fo"] * FPS))
        enc.stdin.write((f.astype(np.float32) * max(0, k)).astype(np.uint8).tobytes() if k < 1 else f.tobytes())
enc.stdin.close(); enc.wait()

# ---------------- sound ----------------
N = int(TOTAL * SR) + SR; mix = np.zeros((N, 2)); mus = np.zeros((N, 2)); rng = np.random.default_rng(3)
db = lambda x: 10 ** (x / 20)
def audio(src, a, d, sp=1.0):
    af = "atempo=%f" % sp if sp >= 0.5 else "atempo=0.5,atempo=%f" % (sp / 0.5)
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(d * sp + 0.05), "-i", src, "-vn", "-af", af,
                        "-ar", str(SR), "-ac", "2", "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(r, np.float32).reshape(-1, 2).astype(np.float64)
    out = np.zeros((int(d * SR), 2)); out[: min(len(x), len(out))] = x[: len(out)]; return out
def rms_norm(x, target_db):
    r = np.sqrt((x ** 2).mean()) + 1e-9; return x / r * db(target_db)
def ramp(n, fi, fo, edge=0.03):
    e = np.ones(n); a = int(max(fi, edge) * SR); b = int(max(fo, edge) * SR)
    e[:a] *= np.linspace(0, 1, a); e[-b:] *= np.linspace(1, 0, b); return e[:, None]
def put(buf, t0, x, g=1.0):
    i = int(t0 * SR); j = min(N, i + len(x)); buf[i:j] += x[: j - i] * g

for e in E:
    if e["k"] != "clip": continue
    n = int(e["d"] * SR)
    if e["own"]:
        x = rms_norm(audio(e["src"], e["a"], e["d"], e["sp"]), -20 + e["g"])
        put(mix, e["t"], x * ramp(n, e["fi"], e["fo"]))
    if e["bed"]:
        src, a, g = e["bed"]; x = rms_norm(audio(C + src, a, e["d"]), -20 + g)
        put(mix, e["t"], x * ramp(n, max(e["fi"], 0.12), max(e["fo"], 0.12)))

# music: low bowed drone (D) with slow swell + two sub hits. No drums, no risers, no braams.
def bowed(f, d):
    x = np.arange(int(d * SR)) / SR; vib = 1 + 0.004 * np.sin(2 * np.pi * 5.1 * x)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    y = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 9))
    bow = np.convolve(rng.standard_normal(len(x)), np.ones(40) / 40, "same") * 0.15
    return (y + bow) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.11 * x))
def swell(d, a, r):
    n = int(d * SR); e = np.ones(n); A = int(a * SR); R = int(r * SR); e[:A] = np.linspace(0, 1, A) ** 2; e[-R:] *= np.linspace(1, 0, R); return e
def sub(d=6.0):
    x = np.arange(int(d * SR)) / SR; f = 34 + 26 * np.exp(-x * 5)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 0.9) * np.minimum(1, x / 0.01)
cards = [e for e in E if e["k"] == "card"]; ttl = next(e for e in E if e["k"] == "title")
crown = next(e for e in E if "V6_crown" in e.get("src", "")); tBlack = ttl["t"] - 2.0
rome = next(c for c in cards if "ROME CAME" in c["text"]); son = next(c for c in cards if "OWN SON" in c["text"])
d1 = rome["t"] - 1.0
put(mus, 1.0, (bowed(73.42, d1) * swell(d1, 6, 1.0))[:, None].repeat(2, 1), db(-34))
d2 = tBlack - son["t"]
y = (bowed(73.42, d2) + 0.7 * bowed(110.0, d2) + 0.45 * bowed(146.83, d2)) * swell(d2, 3, 0.05)
put(mus, son["t"], np.stack([y * 0.9, y], 1), db(-33))
put(mus, rome["t"], sub(5.0)[:, None].repeat(2, 1), db(-12))
put(mus, ttl["t"], sub(7.0)[:, None].repeat(2, 1), db(-9))
mix += mus
i0 = int((tBlack + 0.02) * SR); i1 = int(ttl["t"] * SR); f = int(0.05 * SR)
mix[i0 - f:i0] *= np.linspace(1, 0, f)[:, None]; mix[i0:i1] = 0
mix = mix[: int(TOTAL * SR)]
mix.astype(np.float32).tofile(TMP + "/mix.f32")
import re
m = subprocess.run(["ffmpeg", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", TMP + "/mix.f32", "-af", "ebur128", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", m)[-1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", TMP + "/mix.f32",
                "-af", "volume=%.2fdB,alimiter=limit=0.6:attack=2:release=80:level=disabled" % (-16 - I), TMP + "/mix.wav"], check=True)
out = ROOT + "/Tigran_the_Great_trailer_v3.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", TMP + "/picture.mp4", "-i", TMP + "/mix.wav", "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True)
with open(ROOT + "/EDL.txt", "w") as fh:
    for e in E:
        fh.write("%6.2f %5.2f %-5s %s\n" % (e["t"], e["d"], e["k"], e.get("text", "").replace("\n", " / ") if e["k"] == "card" else
                 "%s [%.2f-%.2f] x%.2f fi%.1f fo%.1f bed=%s" % (os.path.basename(e.get("src", "")), e.get("a", 0), e.get("b", 0), e.get("sp", 1), e.get("fi", 0), e.get("fo", 0), e.get("bed")) if e["k"] == "clip" else ""))
print("wrote", out, "%.2f s" % TOTAL)
