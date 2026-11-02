"""Sound design + score for storyboard 09-16, synthesised (no samples). Timed to the edit in build.py:
S09 0-4 | S10 4-7 | S11 7-11.5 | S13 11.5-13.5 | S12 13.5-16 | S15 16-18 | S14 18-21 | S16 21-25.45 | black."""
import os, sys
import numpy as np
from scipy import signal
import soundfile as sf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'the-last-page', 'src'))
import audio as A   # synthesis building blocks from THE LAST PAGE
from audio import SR, T, lp, hp, bp, string_ens, brass, timpani, wind, paper_flutter, footstep, creak, rattle, whoosh, reverb_ir

DUR = 26.5
N = int(DUR * SR)
rng = np.random.default_rng(3)


class Bus:
    def __init__(self):
        self.L = np.zeros(N + SR * 6)
        self.R = np.zeros(N + SR * 6)

    def add(self, x, t, g=1.0, pan=0.0):
        i = T(t)
        x = x[:len(self.L) - i] * g
        self.L[i:i + len(x)] += x * np.cos((pan + 1) * np.pi / 4) * 1.414
        self.R[i:i + len(x)] += x * np.sin((pan + 1) * np.pi / 4) * 1.414


def verb(bus, ir, wet):
    return [x * (1 - wet * 0.5) + signal.fftconvolve(x, h)[:len(x)] * wet for x, h in zip((bus.L, bus.R), ir)]


def fire(dur, seed=1):
    r = np.random.default_rng(seed)
    roar = lp(r.normal(0, 1, T(dur)), 400)
    roar = roar / np.std(roar) * 0.05
    crackle = rattle(dur, 28, seed=seed + 1) * 0.5
    pops = np.zeros(T(dur))
    for _ in range(int(dur * 6)):
        i = T(r.uniform(0, dur - 0.05))
        k = bp(r.normal(0, 1, T(0.02)), 1500, 6000) * np.exp(-np.arange(T(0.02)) / (0.003 * SR))
        pops[i:i + len(k)] += k * r.uniform(0.2, 0.8)
    return roar + crackle + pops * 0.4


def splash(level=1.0):
    n = T(0.9)
    t = np.arange(n) / SR
    body = bp(rng.normal(0, 1, n), 300, 3500) * np.exp(-t * 6)
    thump = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18)
    drops = paper_flutter(0.9, lambda tt: 300 * np.exp(-tt * 4), bright=1.6, seed=31) * 0.6
    return (body * 0.35 + thump * 0.6 + drops) * level


def clank():
    n = T(0.6)
    t = np.arange(n) / SR
    y = sum(g * np.sin(2 * np.pi * 900 * r * t) * np.exp(-t * (14 + 6 * k)) for k, (r, g) in enumerate(((1, 1), (2.4, 0.5), (3.9, 0.3))))
    return y * 0.08


def bow_twang():
    n = T(0.5)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 110 * t * (1 + 0.1 * np.exp(-t * 30))) * np.exp(-t * 12) + bp(rng.normal(0, 1, n), 200, 1200) * np.exp(-t * 40) * 0.5
    return y * 0.35


def arrow_whistle(dur=1.0, f0=2400, f1=1500):
    n = T(dur)
    t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15 + bp(rng.normal(0, 1, n), 1200, 5000) * 0.25
    return tone * np.sin(np.pi * t / dur) ** 2 * 0.25


def impact_wood():
    n = T(0.25)
    t = np.arange(n) / SR
    return (lp(rng.normal(0, 1, n), 1200) * np.exp(-t * 35) + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 30) * 0.5) * 0.35


def heartbeat():
    n = T(0.5)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 52 * t) * np.exp(-t * 14) * np.clip(t / 0.01, 0, 1) * 0.9


def war_horn(dur=2.2, midi=50):
    f0 = A.mtof(midi)
    n = T(dur)
    t = np.arange(n) / SR
    f = f0 * (1 + 0.03 * (1 - np.exp(-t * 4))) * (1 + 0.004 * np.sin(2 * np.pi * 5 * t))
    ph = np.cumsum(f) / SR
    raw = sum(np.sin(2 * np.pi * k * ph) / k ** 0.9 for k in range(1, 14))
    e = np.clip(t / 0.35, 0, 1) * np.clip((dur - t) / 0.6, 0, 1)
    out = lp(raw * e, 1600)
    b, a = signal.iirpeak(700, 3, fs=SR)
    out = out + signal.lfilter(b, a, out) * 0.6
    return out * 0.12


def drum(level=1.0, f=62):
    n = T(1.2)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(f * (1 + 0.5 * np.exp(-t * 25))) / SR) * np.exp(-t * 4.5)
    y += lp(rng.normal(0, 1, n), 700) * np.exp(-t * 30) * 0.5
    return y * level * 0.6


def hooves(dur, rate=2.4, seed=8):
    r = np.random.default_rng(seed)
    y = np.zeros(T(dur))
    t = 0.0
    while t < dur:
        for off in (0.0, 0.07, 0.15):     # gallop: three-beat footfall per stride
            i = T(t + off + r.normal(0, 0.008))
            if 0 <= i < len(y):
                k = footstep(r.uniform(0.6, 1.0))
                y[i:i + len(k)] += k[:len(y) - i]
        t += 1.0 / rate * r.uniform(0.85, 1.15) * 0.42 * 2.4
    return y


def build():
    fx = Bus()
    mu = Bus()
    hbb = Bus()
    # S09/S10: burning city
    fx.add(fire(7.2, 1), 0.0, 1.2, 0.3)
    fx.add(fire(7.2, 5), 0.0, 0.9, -0.4)
    w = wind(26, base=300, seed=2)
    fx.add(w, 0.0, 1.3, 0.0)
    crowd = bp(rng.normal(0, 1, T(7)), 250, 1400)
    fx.add(crowd / np.std(crowd) * 0.03 * np.clip(np.arange(T(7)) / T(1.5), 0, 1), 0.0, 1.0, 0.0)
    mu.add(string_ens(38, 15.5, att=3.0, rel=0.5, bright=800, voices=8) * 1.6, 0.5, 1.0, -0.2)
    mu.add(string_ens(45, 11.5, att=1.5, rel=0.5, bright=900, voices=8) * 1.2, 4.0, 1.0, 0.2)
    # S11 river + volleys
    river = bp(rng.normal(0, 1, T(4.8)), 250, 2500)
    river = river / np.std(river) * 0.07
    fx.add(river * np.clip(np.arange(len(river)) / T(0.2), 0, 1) * np.clip((len(river) - np.arange(len(river))) / T(0.3), 0, 1), 7.0, 1.0, -0.2)
    for v0 in (7.6, 9.4):
        for k in range(10):
            fx.add(bow_twang(), v0 + rng.uniform(0, 0.35), 0.5, -0.7)
        for k in range(6):
            fx.add(arrow_whistle(1.0, rng.uniform(2000, 2800), rng.uniform(1200, 1700)), v0 + 0.1 + rng.uniform(0, 0.3), 1.0, rng.uniform(-0.6, 0.6))
        for k in range(12):
            fx.add(impact_wood(), v0 + 1.05 + rng.uniform(0, 0.4), 0.7, 0.6)
    # S13 the legion steps into the river
    for k in range(5):
        fx.add(lp(footstep(1.0), 400) * 1.5, 11.5 + k * 0.5 - 0.05, 1.0, 0.3)
    fx.add(splash(1.2), 11.93, 1.0, 0.0)
    fx.add(clank(), 11.95, 1.0, 0.2)
    fx.add(lp(rng.normal(0, 1, T(2.0)), 900) * 0.02, 11.5, 1.0, 0.0)
    # S12 the archer draws and releases
    fx.add(creak(1.2, 160, 420, seed=4, rough=0.08) * 1.6, 13.55, 1.0, -0.1)
    fx.add(bow_twang() * 2.0, 14.75, 1.0, 0.0)
    fx.add(whoosh(0.5, 700, 2600, 0.8, seed=9), 14.76, 1.0, 0.5)
    # S15 the hand - two heartbeats
    hbb.add(heartbeat() * 2.2, 17.15, 1.0, 0.0)
    hbb.add(heartbeat() * 1.6, 17.5, 1.0, 0.0)
    mu.add(lp(rng.normal(0, 1, T(2.0)), 60) * 0.3, 16.0, 1.0, 0.0)
    # S14 the signal: war horn and a gust
    fx.add(war_horn(2.4, 50), 18.6, 1.0, 0.0)
    fx.add(war_horn(2.2, 57) * 0.5, 18.75, 1.0, 0.3)
    fx.add(whoosh(1.6, 150, 500, 1.0, seed=10), 18.3, 1.0, -0.3)
    fx.add(paper_flutter(2.8, 70, bright=0.35, seed=11) * 0.5, 18.2, 1.0, 0.4)
    # S16 the counter-attack
    for k in range(9):
        mu.add(drum(1.0 if k % 2 == 0 else 0.7), 21.0 + k * 0.5, 1.0, 0.0)
        if k % 2:
            mu.add(drum(0.5, 90), 21.25 + k * 0.5, 1.0, 0.0)
    fx.add(hooves(4.5) * 1.3, 21.0, 1.0, 0.0)
    roar = bp(rng.normal(0, 1, T(4.5)), 300, 1800)
    roar = roar / np.std(roar) * 0.08 * np.linspace(0.3, 1.0, len(roar))
    fx.add(roar, 21.0, 1.0, 0.0)
    for m in (38, 50, 53, 57, 62):
        mu.add(string_ens(m, 4.45, att=0.4, rel=0.02, bright=3000) * 1.3, 21.0, 1.0, (m - 50) / 30)
    for m in (50, 53, 57):
        mu.add(brass(m, 4.45, att=0.6, rel=0.02, level=1.0), 21.0, 1.0, 0.0)
    mu.add(timpani(38, 1.3), 21.0, 1.0, 0.0)
    # mix
    Lf, Rf = verb(fx, reverb_ir(1.4, 6000, seed=4), 0.2)
    Lm, Rm = verb(mu, reverb_ir(2.4, 5000, seed=5), 0.3)
    L, R = (Lf + Lm)[:N], (Rf + Rm)[:N]
    t = np.arange(N) / SR
    # S15 ducks everything but the heartbeat; the hard cut to silence at 25.45
    duck = 1 - 0.85 * np.clip((t - 16.0) / 0.15, 0, 1) * np.clip((18.0 - t) / 0.1, 0, 1)
    cut = (t < 25.45).astype(float)
    cut = np.convolve(cut, np.ones(48) / 48, mode='same')
    fade_in = np.clip(t / 0.8, 0, 1)
    hb = np.zeros(N)
    L, R = L * duck * cut * fade_in + hbb.L[:N], R * duck * cut * fade_in + hbb.R[:N]
    y = np.stack([L, R], 1)
    rms = np.sqrt(np.mean(y[T(21):T(25)] ** 2))
    y *= 0.21 / (rms + 1e-9)
    pk = np.max(np.abs(y))
    if pk > 0.97:
        y = np.tanh(y / 0.97) * 0.97
    return y.astype(np.float32)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'sound.wav'
    y = build()
    sf.write(out, y, SR, subtype='PCM_24')
    print(out, y.shape, float(np.max(np.abs(y))))
