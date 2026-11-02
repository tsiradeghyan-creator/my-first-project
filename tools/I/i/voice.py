"""-I- voice: speech audio (espeak-ng, Eastern Armenian by default, or any recorded/ElevenLabs file)
and a viseme track for lip-sync."""
import os, re, subprocess, tempfile
import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
# viseme: (jaw open, mouth width)
VIS = {'A': (0.95, 0.15), 'E': (0.6, 0.45), 'I': (0.32, 0.6), 'O': (0.7, -0.45), 'U': (0.32, -0.75), 'Y': (0.38, 0.0),
       'M': (0.0, 0.0), 'F': (0.12, 0.1), 'C': (0.24, 0.1), '_': (0.0, 0.0)}
HY = {'ա': 'A', 'ե': 'E', 'է': 'E', 'ի': 'I', 'ո': 'O', 'օ': 'O', 'ը': 'Y', 'մ': 'M', 'բ': 'M', 'պ': 'M', 'փ': 'M',
      'ֆ': 'F', 'վ': 'F', 'ւ': 'U', 'յ': 'I'}
EN = {'a': 'A', 'e': 'E', 'i': 'I', 'o': 'O', 'u': 'U', 'y': 'I', 'm': 'M', 'b': 'M', 'p': 'M', 'f': 'F', 'v': 'F', 'w': 'U'}


def letters_to_visemes(word):
    out = []
    w = word.lower()
    i = 0
    while i < len(w):
        ch = w[i]
        if w[i:i + 2] == 'ու':
            out.append('U')
            i += 2
            continue
        if ch.isalpha():
            out.append(HY.get(ch) or EN.get(ch) or 'C')
        i += 1
    return out or ['C']


def espeak(text, out, voice='hy', speed=135, pitch=30, amp=120):
    raw = out + '.raw.wav'
    subprocess.run(['espeak-ng', '-v', voice, '-s', str(speed), '-p', str(pitch), '-a', str(amp), '-w', raw, text], check=True, capture_output=True)
    y, sr = sf.read(raw)
    os.remove(raw)
    if y.ndim > 1:
        y = y.mean(1)
    y = signal.resample_poly(y, SR, sr)
    # warm it up a little: gentle low-pass and room
    sos = signal.butter(2, 5500, 'low', fs=SR, output='sos')
    y = signal.sosfilt(sos, y)
    ir = np.random.default_rng(0).normal(0, 1, int(0.35 * SR)) * np.exp(-np.arange(int(0.35 * SR)) / (0.07 * SR))
    y = y + signal.fftconvolve(y, ir / np.sqrt((ir ** 2).sum()))[:len(y)] * 0.12
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.8
    sf.write(out, y, SR)
    return out


def envelope(y, fps=100):
    hop = SR // fps
    n = len(y) // hop
    e = np.sqrt(np.array([np.mean(y[i * hop:(i + 1) * hop] ** 2) for i in range(n)]))
    e = e / (np.percentile(e, 95) + 1e-9)
    return np.clip(e, 0, 1.2)


class Speech:
    def __init__(self, text, wav=None, voice='hy', speed=135, pitch=30, workdir=None):
        self.text = text
        d = workdir or tempfile.mkdtemp()
        if wav is None:
            wav = os.path.join(d, 'say_%08x.wav' % (abs(hash((text, voice, speed, pitch))) & 0xffffffff))
            if not os.path.exists(wav):
                espeak(text, wav, voice, speed, pitch)
        y, sr = sf.read(wav)
        if y.ndim > 1:
            y = y.mean(1)
        if sr != SR:
            y = signal.resample_poly(y, SR, sr)
        self.audio = y
        self.dur = len(y) / SR
        self.env = envelope(y)
        voiced = self.env > 0.08
        idx = np.nonzero(voiced)[0]
        t0 = idx[0] / 100 if len(idx) else 0.0
        t1 = idx[-1] / 100 if len(idx) else self.dur
        words = [w for w in re.split(r'\s+', text.strip()) if w]
        vis = [letters_to_visemes(w) for w in words]
        weights = np.array([len(v) + 1.5 for v in vis], np.float32)
        total = t1 - t0
        track = []
        t = t0
        for w, v, wt in zip(words, vis, weights):
            dw = total * wt / weights.sum()
            step = dw / (len(v) + 0.5)
            for k, vv in enumerate(v):
                track.append((t + k * step, vv))
            t += dw
            if re.search(r'[,։.:!?՝]$', w):
                track.append((t - step * 0.4, '_'))
        track.append((t1 + 0.02, '_'))
        self.track = track
        # dense parameter curves at 100 Hz, smoothed for coarticulation
        n = int(self.dur * 100) + 1
        jaw = np.zeros(n)
        wid = np.zeros(n)
        times = [tt for tt, _ in track] + [self.dur + 1]
        for i in range(n):
            tt = i / 100
            k = max(0, np.searchsorted(times, tt, side='right') - 1)
            v = track[min(k, len(track) - 1)][1] if tt >= t0 else '_'
            jaw[i], wid[i] = VIS[v]
        e = np.interp(np.arange(n), np.arange(len(self.env)), self.env)
        jaw = jaw * (0.3 + 0.7 * np.clip(e * 1.4, 0, 1)) * (e > 0.05)
        b = np.ones(5) / 5
        self.jaw = np.convolve(jaw, b, mode='same')
        self.width = np.convolve(wid, b, mode='same')

    def params(self, t):
        i = int(np.clip(t * 100, 0, len(self.jaw) - 1))
        if t < 0 or t > self.dur:
            return dict(jaw=0.0, width=0.0)
        return dict(jaw=float(self.jaw[i]), width=float(self.width[i]))
