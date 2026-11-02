"""Original score and sound design for THE LAST PAGE, synthesised from scratch (numpy/scipy).

Wind and near-silence -> a lone felt-piano motif when the fox appears -> low strings and creaking
wood in the tremor -> one beat of total silence -> a roar of fluttering paper -> full orchestral
swell at sunrise -> the piano motif at full scale at the climax -> a single soft piano note as the
ink touches the last page.
"""
import numpy as np
from scipy import signal
import soundfile as sf

SR = 48000
DUR = 60.0
N = int(SR * DUR)
rng = np.random.default_rng(5)


def T(s):
    return int(s * SR)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env_adsr(n, a, d, s, r, sr=SR):
    a, d, r = int(a * sr), int(d * sr), int(r * sr)
    sus = max(0, n - a - d - r)
    e = np.concatenate([np.linspace(0, 1, max(1, a)), np.linspace(1, s, max(1, d)), np.full(sus, s), np.linspace(s, 0, max(1, r))])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))


def lp(x, fc, order=2):
    sos = signal.butter(order, min(fc, SR * 0.45), 'low', fs=SR, output='sos')
    return signal.sosfilt(sos, x)


def hp(x, fc, order=2):
    sos = signal.butter(order, fc, 'high', fs=SR, output='sos')
    return signal.sosfilt(sos, x)


def bp(x, f0, f1, order=2):
    sos = signal.butter(order, [f0, min(f1, SR * 0.45)], 'band', fs=SR, output='sos')
    return signal.sosfilt(sos, x)


class Bus:
    def __init__(self):
        self.L = np.zeros(N + SR * 8)
        self.R = np.zeros(N + SR * 8)

    def add(self, x, t, gain=1.0, pan=0.0):
        i = T(t)
        if i >= len(self.L):
            return
        x = x[:len(self.L) - i] * gain
        gl = np.cos((pan + 1) * np.pi / 4)
        gr = np.sin((pan + 1) * np.pi / 4)
        self.L[i:i + len(x)] += x * gl * 1.414
        self.R[i:i + len(x)] += x * gr * 1.414


def reverb_ir(seconds, damp=4000, pre=0.015, seed=0):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    irs = []
    for ch in range(2):
        noise = r.normal(0, 1, n)
        noise = lp(noise, damp)
        e = np.exp(-6.9 * t / seconds)
        ir = noise * e
        ir[:int(pre * SR)] = 0
        irs.append(ir / np.sqrt(np.sum(ir ** 2)))
    return irs


def apply_reverb(bus, ir, wet):
    out = []
    for x, h in zip((bus.L, bus.R), ir):
        y = signal.fftconvolve(x, h)[:len(x)]
        out.append(x * (1 - wet * 0.5) + y * wet)
    return out


# ------------------------------------------------------------------ instruments
def felt_piano(midi, dur, vel=0.6, bright=0.5):
    f = mtof(midi)
    n = T(dur + 2.5)
    t = np.arange(n) / SR
    y = np.zeros(n)
    B = 0.00035
    for k in range(1, 12):
        fk = k * f * np.sqrt(1 + B * k * k)
        if fk > 9000:
            break
        amp = (1.0 / k ** 1.25) * (bright if k > 3 else 1.0)
        dec = 0.6 + 0.35 * k * (f / 300) ** 0.5
        for det in (-0.6, 0.6):   # unison strings, slow beating
            y += amp * 0.5 * np.sin(2 * np.pi * (fk + det * 0.15 * k) * t + rng.uniform(0, 6.28)) * np.exp(-t * dec)
    att = np.clip(t / 0.012, 0, 1)
    rel = np.clip((dur + 0.35 - t) / 0.35, 0, 1) * 0.85 + 0.15 * np.exp(-np.clip(t - dur, 0, None) * 2.5)
    y *= att * np.minimum(1, rel + np.exp(-np.clip(t - dur, 0, None) * 1.2) * 0)
    # felt: a soft thump of the hammer and dark tone
    thump = lp(rng.normal(0, 1, T(0.03)), 600) * np.exp(-np.arange(T(0.03)) / (0.006 * SR))
    y[:len(thump)] += thump * 0.4
    y = lp(y, 1800 + 2500 * vel * bright)
    return y * vel * 0.35


def string_ens(midi, dur, att=0.6, rel=0.8, vib=5.2, trem=0.0, bright=2200, voices=6):
    f0 = mtof(midi)
    n = T(dur + rel)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for v in range(voices):
        det = 2 ** (rng.normal(0, 7) / 1200)
        vb = 1 + 0.0035 * np.sin(2 * np.pi * (vib + rng.normal(0, 0.3)) * t + rng.uniform(0, 6))
        ph = np.cumsum(f0 * det * vb) / SR
        saw = 2 * (ph % 1) - 1
        y += saw
    y /= voices
    y = lp(y, bright, 2)
    y = lp(y, bright * 1.5, 1)
    e = env_adsr(n, att, 0.2, 0.9, rel)
    if trem > 0:
        e *= 0.75 + 0.25 * np.sin(2 * np.pi * trem * t)
    return y * e * 0.22


def brass(midi, dur, att=0.25, rel=0.5, level=1.0):
    f0 = mtof(midi)
    n = T(dur + rel)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for v in range(3):
        ph = np.cumsum(f0 * 2 ** (rng.normal(0, 5) / 1200) * (1 + 0.002 * np.sin(2 * np.pi * 4.8 * t))) / SR
        y += 2 * (ph % 1) - 1
    e = env_adsr(n, att, 0.3, 0.85, rel)
    # the filter opens with the swell: brassy
    out = np.zeros(n)
    blk = T(0.05)
    zi = None
    for i in range(0, n, blk):
        fc = 400 + 2600 * e[i] * level
        sos = signal.butter(2, fc, 'low', fs=SR, output='sos')
        if zi is None:
            zi = signal.sosfilt_zi(sos) * 0
        seg, zi = signal.sosfilt(sos, y[i:i + blk], zi=zi)
        out[i:i + blk] = seg
    return out * e * 0.16 * level


def timpani(midi, vel=1.0, dur=2.5):
    f = mtof(midi)
    n = T(dur)
    t = np.arange(n) / SR
    pitch = f * (1 + 0.06 * np.exp(-t * 18))
    y = np.sin(2 * np.pi * np.cumsum(pitch) / SR) * np.exp(-t * 2.2)
    y += 0.5 * np.sin(2 * np.pi * np.cumsum(pitch * 1.5) / SR) * np.exp(-t * 3.5)
    y += lp(rng.normal(0, 1, n), 300) * np.exp(-t * 25) * 0.6
    return y * vel * 0.5


def noise_env(dur, shape):
    n = T(dur)
    return rng.normal(0, 1, n) * shape(np.arange(n) / SR)


# ------------------------------------------------------------------ sound effects
def wind(dur, base=300, gusts=((0, 0.5),), seed=1):
    r = np.random.default_rng(seed)
    n = T(dur)
    x = r.normal(0, 1, n)
    x = np.cumsum(x)                   # brown-ish
    x = hp(x - np.mean(x), 40)
    x /= np.std(x) + 1e-9
    t = np.arange(n) / SR
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t + 1) * np.sin(2 * np.pi * 0.047 * t)
    out = np.zeros(n)
    blk = T(0.04)
    zi = None
    for i in range(0, n, blk):
        fc = base * (0.7 + 0.8 * lfo[i])
        sos = signal.butter(2, [fc * 0.6, fc * 2.2], 'band', fs=SR, output='sos')
        if zi is None:
            zi = signal.sosfilt_zi(sos) * 0
        seg, zi = signal.sosfilt(sos, x[i:i + blk], zi=zi)
        out[i:i + blk] = seg
    # a faint whistling edge
    wh = np.sin(2 * np.pi * np.cumsum(base * 3.1 * (1 + 0.08 * lfo)) / SR) * (lfo ** 3) * 0.02
    return (out / (np.std(out) + 1e-9) * 0.12 * lfo + wh)


def paper_flutter(dur, density, bright=1.0, seed=2, size=1.0):
    """Granular paper: many short rustles. density = grains per second (array or scalar)."""
    r = np.random.default_rng(seed)
    n = T(dur)
    y = np.zeros(n)
    t = 0.0
    while t < dur:
        d = density(t) if callable(density) else density
        if d <= 0.1:
            t += 0.02
            continue
        t += r.exponential(1.0 / d)
        if t >= dur:
            break
        gl = r.uniform(0.008, 0.045) * size
        g = r.normal(0, 1, T(gl))
        g *= np.exp(-np.arange(len(g)) / (len(g) * 0.3))
        lo = r.uniform(900, 2500) * bright
        g = bp(g, lo, lo * r.uniform(1.8, 3.5))
        i = T(t)
        y[i:i + len(g)] += g[:n - i] * r.uniform(0.3, 1.0)
    return y * 0.5


def footstep(vel=0.5):
    n = T(0.09)
    tt = np.arange(n) / SR
    y = lp(rng.normal(0, 1, n), 900) * np.exp(-tt * 70) + np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 50) * 0.6
    y += bp(rng.normal(0, 1, n), 2000, 5000) * np.exp(-tt * 150) * 0.15   # a little claw tick
    return y * vel * 0.6


def creak(dur, f0, f1, seed=3, rough=0.25):
    """Wood creak: a stick-slip pulse train through resonant body modes."""
    r = np.random.default_rng(seed)
    n = T(dur)
    t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur) * (1 + rough * lp(r.normal(0, 1, n), 8) * 3)
    ph = np.cumsum(np.abs(f)) / SR
    pulses = (np.diff(np.floor(ph), prepend=0) > 0).astype(float) * r.uniform(0.4, 1.0, n)
    y = np.zeros(n)
    for fr, q, g in ((310, 12, 1.0), (760, 14, 0.7), (1450, 16, 0.4), (2300, 18, 0.2)):
        b, a = signal.iirpeak(fr, q, fs=SR)
        y += signal.lfilter(b, a, pulses) * g
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.6
    return y * e * 0.18


def rattle(dur, rate, seed=4):
    r = np.random.default_rng(seed)
    n = T(dur)
    y = np.zeros(n)
    t = 0.0
    while t < dur:
        t += r.exponential(1.0 / rate)
        k = r.normal(0, 1, T(0.012)) * np.exp(-np.arange(T(0.012)) / (0.002 * SR))
        k = bp(k, r.uniform(300, 600), r.uniform(900, 1600))
        i = T(t)
        if i < n:
            y[i:i + len(k)] += k[:n - i] * r.uniform(0.3, 1)
    return y * 0.6


def whoosh(dur, f0, f1, level=1.0, seed=6, lowness=1.0):
    r = np.random.default_rng(seed)
    n = T(dur)
    x = r.normal(0, 1, n)
    t = np.arange(n) / SR
    out = np.zeros(n)
    blk = T(0.02)
    zi = None
    for i in range(0, n, blk):
        u = i / n
        fc = f0 * (f1 / f0) ** u
        sos = signal.butter(2, [fc * 0.5, fc * 1.6], 'band', fs=SR, output='sos')
        if zi is None:
            zi = signal.sosfilt_zi(sos) * 0
        seg, zi = signal.sosfilt(sos, x[i:i + blk], zi=zi)
        out[i:i + blk] = seg
    e = np.sin(np.pi * t / dur) ** 1.5
    return out / (np.std(out) + 1e-9) * e * 0.2 * level


def wingbeat():
    n = T(1.4)
    t = np.arange(n) / SR
    body = lp(rng.normal(0, 1, n), 260) * (np.clip(t / 0.25, 0, 1) * np.exp(-np.clip(t - 0.25, 0, None) * 4))
    sub = np.sin(2 * np.pi * np.cumsum(46 * (1 - 0.2 * t)) / SR) * np.exp(-np.clip(t - 0.3, 0, None) * 3) * np.clip(t / 0.2, 0, 1)
    rush = paper_flutter(1.4, lambda tt: 900 * np.exp(-((tt - 0.35) / 0.25) ** 2), bright=0.8, seed=12, size=1.6)
    return (body / (np.std(body) + 1e-9) * 0.35 + sub * 0.55 + rush * 0.8)


def metal_break():
    n = T(2.5)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k, (r_, g) in enumerate(((1, 1), (2.76, 0.6), (5.4, 0.4), (8.93, 0.25), (13.3, 0.15))):
        y += g * np.sin(2 * np.pi * 180 * r_ * t + k) * np.exp(-t * (2.5 + k))
    crack = bp(rng.normal(0, 1, n), 1500, 7000) * np.exp(-t * 18)
    return (y * 0.25 + crack * 0.4)


def ink_brush(dur, seed=7):
    r = np.random.default_rng(seed)
    n = T(dur)
    t = np.arange(n) / SR
    x = r.normal(0, 1, n)
    soft = lp(x, 1200) * 0.7 + bp(x, 2500, 6000) * 0.15
    mod = 0.6 + 0.4 * lp(r.normal(0, 1, n), 6) * 8
    e = np.clip(t / 0.08, 0, 1) * np.clip((dur - t) / 0.2, 0, 1)
    return soft * np.clip(mod, 0.2, 1.4) * e * 0.12


def sniff():
    n = T(0.12)
    t = np.arange(n) / SR
    return bp(rng.normal(0, 1, n), 1500, 6000) * np.sin(np.pi * t / 0.12) ** 2 * 0.12


# ------------------------------------------------------------------ the score
def build():
    sfx_int = Bus()      # interior effects (long hall reverb)
    sfx_ext = Bus()      # exterior effects
    music = Bus()
    beat = 60 / 66

    # 0:00-0:07 wind first, near silence
    w = wind(8.0, base=320, seed=1)
    w *= np.clip(np.arange(len(w)) / (2.5 * SR), 0, 1)
    sfx_ext.add(w, 0.0, 2.0, 0.0)
    sfx_ext.add(wind(8.0, base=520, seed=9) * 0.5, 0.0, 1.4, 0.4)
    # pampas rustle
    sfx_ext.add(paper_flutter(6.5, lambda t: 25 + 20 * np.sin(t * 1.3) ** 2, bright=0.45, seed=21), 0.5, 0.18, -0.5)

    # 0:07 inside: room tone, muffled wind beyond the walls
    room = lp(rng.normal(0, 1, T(25)), 180)
    room = room / np.std(room) * 0.02
    room *= np.clip(np.arange(len(room)) / (0.8 * SR), 0, 1)
    room[T(23.8):] *= np.linspace(1, 0, len(room) - T(23.8))   # the stillness beat
    sfx_int.add(room, 7.0, 1.0, 0.0)
    sfx_int.add(lp(wind(25, base=200, seed=3), 400) * 0.6, 7.0, 0.6, -0.3)
    # paw steps (walk cycle contacts), lantern swing squeak
    for k in range(9):
        for off in (0.0, 0.31):
            tt = 7.0 + 0.2 + k * 0.55 + off
            if tt < 11.35:
                sfx_int.add(footstep(0.45 + 0.1 * rng.random()), tt, 1.8, -0.6 + 0.1 * k)
    for k in range(7):
        sfx_int.add(creak(0.12, 900, 1100, seed=40 + k, rough=0.05) * 0.25, 7.4 + k * 0.55, 1.0, -0.4 + 0.1 * k)
    # lantern set down: a soft wooden knock
    knock = footstep(0.9)
    sfx_int.add(lp(knock, 600), 12.3, 1.0, -0.1)
    # flame: faint crackle under everything inside
    sfx_int.add(rattle(18, 6, seed=8) * 0.06, 7.5, 1.0, -0.2)

    # felt piano motif enters with the fox (7.6s)
    t0 = 7.6
    phraseA = [(0, 74, 1.5, 0.55), (1.5, 73, 0.5, 0.42), (2, 69, 1.0, 0.48), (3, 71, 1.0, 0.45), (4, 66, 3.0, 0.5)]
    lhA = [(0, 50, 4, 0.32), (4, 47, 4, 0.3)]
    phraseB = [(8, 74, 1.0, 0.5), (9, 76, 1.0, 0.48), (10, 78, 1.5, 0.55), (11.5, 76, 0.5, 0.4), (12, 73, 2.5, 0.45)]
    lhB = [(8, 43, 4, 0.3), (12, 45, 3, 0.28)]
    for (b, m, d, v) in phraseA + lhA + phraseB + lhB:
        st = t0 + b * beat
        if st > 20.1:
            continue
        x = felt_piano(m, min(d * beat, 20.2 - st), v)
        # nothing may ring into the silence on the page
        cut = T(20.25 - st)
        if cut < len(x):
            x[cut:] = 0
            fadeN = min(cut, T(0.3))
            x[cut - fadeN:cut] *= np.linspace(1, 0, fadeN)
        music.add(x, st, 2.0, (m - 62) / 30)

    # 0:14 close-up: ear rustles, three sniffs
    sfx_int.add(paper_flutter(0.25, 60, bright=0.3, seed=31) * 0.3, 14.4, 1.0, -0.4)
    sfx_int.add(paper_flutter(0.25, 60, bright=0.3, seed=32) * 0.3, 15.05, 1.0, 0.4)
    for k in range(3):
        sfx_int.add(sniff(), 15.6 + k * 0.27, 1.0, 0.0)

    # 0:18 hop, landing, paw on the page - then silence - then ink
    sfx_int.add(whoosh(0.5, 300, 900, 0.5, seed=33), 18.55, 1.0, -0.3)
    sfx_int.add(footstep(0.8), 19.12, 1.0, 0.0)
    sfx_int.add(footstep(0.4), 19.2, 1.0, 0.1)
    tap = bp(rng.normal(0, 1, T(0.05)), 800, 3000) * np.exp(-np.arange(T(0.05)) / (0.008 * SR))
    sfx_int.add(tap * 0.25, 20.3, 1.0, 0.1)
    sfx_int.add(ink_brush(1.6), 20.9, 1.0, 0.25)
    sfx_int.add(paper_flutter(0.6, lambda t: 120, bright=0.9, seed=34) * 0.35, 22.5, 1.0, 0.3)   # shiver
    tear = bp(rng.normal(0, 1, T(0.7)), 1500, 6000) * np.sin(np.pi * np.arange(T(0.7)) / T(0.7)) ** 2 * 0.15
    sfx_int.add(tear, 23.1, 1.0, 0.3)
    for k in range(9):   # little paper wingbeats
        sfx_int.add(paper_flutter(0.08, 400, bright=1.2, seed=50 + k) * 0.5, 23.45 + k * 0.125, 1.0, 0.3 + k * 0.06)
    for (dt, m) in ((0.0, 81), (0.22, 85), (0.44, 88)):
        music.add(felt_piano(m, 0.8, 0.3, bright=0.7), 23.8 + dt, 1.0, 0.4)

    # 0:25 the library stirs: low strings, creaks, rattles, dust, the flame leans
    music.add(string_ens(38, 5.9, att=2.5, rel=0.05, trem=11, bright=900, voices=8) * 1.4, 25.0, 1.8, -0.2)
    music.add(string_ens(45, 5.9, att=3.0, rel=0.05, trem=12, bright=1100, voices=8) * 1.1, 25.0, 1.8, 0.2)
    sfx_int.add(rattle(1.6, 18, seed=60), 25.1, 0.8, 0.0)
    sfx_int.add(rattle(1.4, 60, seed=61), 26.6, 1.0, 0.0)
    sfx_int.add(paper_flutter(3.0, 80, bright=0.25, seed=62) * 0.3, 25.3, 1.0, 0.1)   # dust sifting
    sfx_int.add(creak(1.8, 45, 85, seed=63), 26.9, 1.6, -0.3)    # a deep creak travels up the tower
    sfx_int.add(creak(1.2, 70, 120, seed=64), 28.2, 1.2, 0.4)
    sfx_int.add(whoosh(1.2, 150, 400, 0.4, seed=65), 28.0, 1.0, 0.0)  # the flame leans
    # 0:30.9 one beat of total stillness - everything cut

    # 0:32 the pages burst
    roar = paper_flutter(7.2, lambda t: 2200 * np.exp(-t * 0.25) + 300, bright=1.0, seed=70, size=1.2)
    roar[:T(0.05)] *= np.linspace(0, 1, T(0.05))
    sfx_int.add(roar, 32.0, 0.65, 0.0)
    sfx_int.add(paper_flutter(7.0, lambda t: 900, bright=0.6, seed=71, size=1.6), 32.05, 0.8, -0.5)
    sfx_int.add(paper_flutter(7.0, lambda t: 900, bright=0.7, seed=72, size=1.6), 32.08, 0.8, 0.5)
    sfx_int.add(whoosh(3.2, 200, 1800, 1.2, seed=73), 34.0, 1.0, 0.0)   # the vortex rises
    sfx_int.add(metal_break(), 37.3, 1.2, 0.0)
    # strings rush upward through the burst
    chords = [(32.0, [47, 54, 59, 62, 66]), (34.0, [43, 50, 55, 59, 62]), (35.5, [45, 52, 57, 61, 64])]
    for (st, notes) in chords:
        for m in notes:
            music.add(string_ens(m, 2.0 if st < 35 else 1.8, att=0.15, rel=0.3, trem=14, bright=2600), st, 0.9, (m - 55) / 25)
    for m in (57, 61, 64):
        music.add(brass(m, 1.8, att=0.8, rel=0.3, level=0.7), 35.5, 1.0, 0.0)

    # 0:37.3 -> 0:44 the swell into sunrise
    swell = [(37.3, 4.2, [38, 50, 57, 62, 66, 69, 74]), (41.5, 2.7, [42, 54, 59, 62, 66, 71, 74])]
    for (st, d, notes) in swell:
        for m in notes:
            music.add(string_ens(m, d, att=1.2 if st < 40 else 0.5, rel=0.6, bright=3200), st, 1.0, (m - 60) / 30)
        for m in notes[1:5]:
            music.add(brass(m, d, att=1.4 if st < 40 else 0.5, rel=0.6, level=1.0), st, 1.0, 0.0)
    for k in range(int(1.6 * 14)):      # timpani roll into the sunrise
        music.add(timpani(38, 0.25 + 0.6 * k / 22, 0.6), 37.4 + k / 14, 1.0, 0.0)
    music.add(timpani(38, 1.2), 39.0, 1.0, 0.0)
    cym = hp(rng.normal(0, 1, T(2.2)), 5000) * np.linspace(0, 1, T(2.2)) ** 3 * 0.12
    music.add(cym, 36.9, 1.0, 0.0)
    sfx_ext.add(wind(6.0, base=420, seed=80) * 1.4, 39.0, 1.0, 0.0)
    sfx_ext.add(whoosh(2.2, 120, 500, 1.4, seed=81, lowness=2), 40.3, 1.0, 0.0)   # ring of wind
    sfx_ext.add(paper_flutter(5, 30, bright=0.5, seed=82) * 0.4, 39, 1.0, 0.4)    # grass and fur

    # 0:44-0:52 climax: the piano motif returns at full scale with the orchestra
    cb = 0.52
    t1 = 44.4
    climax = [(0, 74, 1.5), (1.5, 73, 0.5), (2, 69, 1.0), (3, 71, 1.0), (4, 66, 2.0), (6, 74, 1.0), (7, 76, 1.0), (8, 78, 1.5), (9.5, 76, 0.5), (10, 73, 1.0), (11, 74, 4.0)]
    for (b, m, d) in climax:
        st = t1 + b * cb
        for o in (0, -12, 12):
            music.add(felt_piano(m + o, d * cb + 0.4, 0.85 if o == 0 else 0.55, bright=0.9), st, 1.0, (m + o - 62) / 40)
    prog = [(44.4, 3.1, [38, 50, 57, 62, 66]), (47.5, 1.6, [43, 55, 59, 62, 67]), (49.1, 1.3, [45, 52, 57, 61, 64]), (50.4, 3.6, [38, 50, 57, 62, 66, 69])]
    for (st, d, notes) in prog:
        for m in notes:
            music.add(string_ens(m, d, att=0.35, rel=1.4, bright=3400), st, 1.1, (m - 60) / 30)
        for m in notes[1:4]:
            music.add(brass(m, d, att=0.3, rel=1.2, level=0.9), st, 0.9, 0.0)
    music.add(timpani(38, 1.3), 44.4, 1.0, 0.0)
    music.add(timpani(31, 1.6, 3.5), 47.25, 1.0, 0.0)
    sfx_ext.add(wingbeat(), 46.95, 1.6, 0.0)          # the great wingbeat
    sfx_ext.add(whoosh(4.0, 200, 900, 1.2, seed=90), 47.9, 1.0, 0.0)
    sfx_ext.add(paper_flutter(4.5, lambda t: 500 * np.exp(-t * 0.4), bright=0.8, seed=91), 47.9, 0.7, 0.3)

    # 0:52-1:00 quiet returns
    for m in (62, 66, 69, 74):
        x = string_ens(m, 3.2, att=0.4, rel=2.4, bright=2200, voices=6) * 0.5
        music.add(x, 52.0, 1.0, (m - 66) / 20)
    sfx_ext.add(wind(8.0, base=380, seed=95) * 0.5, 52.0, 1.0, 0.0)
    sfx_ext.add(paper_flutter(3.2, 40, bright=0.55, seed=96) * 0.5, 52.0, 1.0, 0.0)
    sfx_ext.add(tap * 0.2, 53.5, 1.0, 0.0)            # the page lands
    # the ink touches the last page: one single soft piano note
    music.add(felt_piano(74, 3.5, 0.5, bright=0.5), 55.5, 2.2, 0.0)
    sfx_ext.add(ink_brush(1.4, seed=97) * 0.8, 55.7, 1.0, 0.0)
    sfx_ext.add(lp(footstep(0.7), 500), 57.3, 1.0, 0.1)   # the hanko pressed into paper
    sfx_ext.add(ink_brush(1.1, seed=98) * 0.6, 57.6, 1.0, 0.0)
    sfx_ext.add(whoosh(0.5, 400, 1200, 0.35, seed=99), 58.65, 1.0, 0.6)   # tail flick

    # ------------------------------------------------------------------ mix
    Li, Ri = apply_reverb(sfx_int, reverb_ir(3.2, 3500, seed=1), 0.45)
    Le, Re = apply_reverb(sfx_ext, reverb_ir(1.2, 6000, seed=2), 0.18)
    Lm, Rm = apply_reverb(music, reverb_ir(2.6, 5000, seed=3), 0.35)
    L = Li + Le + Lm * 1.1
    R = Ri + Re + Rm * 1.1
    L, R = L[:N], R[:N]
    t = np.arange(N) / SR
    # the stillness: hard silence 30.9-32.0 (room tone almost nothing)
    st = (t > 30.9) & (t < 32.0)
    L[st] *= 0.03
    R[st] *= 0.03
    fo = np.clip((60.0 - t) / 1.2, 0, 1)
    L *= fo
    R *= fo
    y = np.stack([L, R], 1)
    y = hp(y.T, 25).T
    # gentle bus compression, then normalise loudness (~ -16 LUFS by RMS of the loud half)
    rms = np.sqrt(np.mean(y[T(32):T(52)] ** 2))
    y *= 0.12 / (rms + 1e-9)
    peak = np.max(np.abs(y))
    if peak > 0.97:
        y = np.tanh(y / 0.97 * 1.0) * 0.97
    return y.astype(np.float32)


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else 'score.wav'
    y = build()
    sf.write(out, y, SR, subtype='PCM_24')
    print('wrote', out, y.shape, 'peak', float(np.max(np.abs(y))))
