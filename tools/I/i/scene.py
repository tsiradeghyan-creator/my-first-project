"""-I- language: a tiny script that turns stills into acted shots.

    -I- 1
    size 1280 536
    fps 24
    letterbox 720

    shot 4.0 "The king speaks"
      actor king ../panels/10.png            # rig is built automatically and cached
      king idle
      king say "Մենք չենք նահանջի։" at 0.4 pitch 25 speed 125
      king blink at 2.6
      camera push 1.06

    shot 5.0 "The messenger walks"
      actor m ../refs/REF_E.png
      m walk speed 0.9 from 0.2 to 4.6
      camera pan -40 0

Actor commands: idle | walk | run | raise_arm side r|l | point side r|l | look ANGLE | nod | crouch
                say "TEXT" [voice hy|en] [pitch P] [speed S] [wav FILE] | blink | brow
Common options: at T | from T0 to T1 | fade F | key value ...
Placement:      actor NAME IMAGE [at X Y] [scale S] [bg own|PATH]   (default: image fills the frame, own clean plate)
Camera:         camera push FACTOR | camera pan DX DY | camera shake AMP
"""
import os, shlex, math, subprocess, hashlib
import numpy as np
import cv2
import skia
import soundfile as sf

from .rig import Rig
from .motion import Clip, evaluate, skin
from .face import Face
from .voice import Speech, SR


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


class Actor:
    def __init__(self, name, image, cache):
        self.name = name
        key = hashlib.md5(open(image, 'rb').read()).hexdigest()[:10]
        d = os.path.join(cache, f'{os.path.basename(image)}_{key}')
        if os.path.exists(os.path.join(d, 'rig.npz')):
            self.rig = Rig.load(d)
        else:
            self.rig = Rig.build(image)
            self.rig.save(d)
            self.rig.debug(os.path.join(d, 'rig_debug.png'))
        self.face = Face(self.rig.face, self.rig.img.shape) if self.rig.face is not None else None
        self.clips, self.speech, self.blinks, self.brows = [], [], [], []
        self.place = None
        self.bg = 'own'
        self.auto_blink = True

    def face_params(self, t):
        p = dict(jaw=0.0, width=0.0, blink=0.0, brow=0.0)
        for (t0, sp) in self.speech:
            q = sp.params(t - t0)
            p['jaw'] = max(p['jaw'], q['jaw'])
            if q['jaw'] > 0:
                p['width'] = q['width']
            if 0 < t - t0 < sp.dur:      # a speaker's brows lift a little on stressed words
                p['brow'] = max(p['brow'], 0.25 * q['jaw'])
        bl = list(self.blinks)
        if self.auto_blink:
            r = np.random.default_rng(abs(hash(self.name)) % 9999)
            tt = r.uniform(0.6, 2.0)
            while tt < 60:
                bl.append(tt)
                tt += r.uniform(2.4, 4.8)
        for b in bl:
            d = t - b
            if 0 <= d < 0.21:            # on ones: close 2 frames, hold 2, open 1
                p['blink'] = max(p['blink'], [0.6, 1.0, 1.0, 1.0, 0.45][min(4, int(d * 24))])
        for (b0, b1, amt) in self.brows:
            if b0 <= t <= b1:
                p['brow'] = max(p['brow'], amt * ease((t - b0) / 0.2) * ease((b1 - t) / 0.2))
        return p


class Shot:
    def __init__(self, dur, title):
        self.dur, self.title = dur, title
        self.actors = []
        self.cam = dict(push=1.0, pan=(0.0, 0.0), shake=0.0)
        self.bg_path = None


def parse_opts(tok):
    o = {}
    i = 0
    rest = []
    while i < len(tok):
        k = tok[i]
        if k == 'at':
            o['at'] = float(tok[i + 1]); i += 2
        elif k == 'from':
            o['from'] = float(tok[i + 1]); i += 2
        elif k == 'to':
            o['to'] = float(tok[i + 1]); i += 2
        elif i + 1 < len(tok) and k.isidentifier() and k not in ('r', 'l'):
            v = tok[i + 1]
            try:
                v = float(v)
            except ValueError:
                pass
            o[k] = v; i += 2
        else:
            rest.append(k); i += 1
    return o, rest


class Film:
    def __init__(self, path):
        self.path = path
        self.base = os.path.dirname(os.path.abspath(path))
        self.cache = os.path.join(self.base, '.i_cache')
        self.W, self.H, self.fps, self.box = 1280, 536, 24, None
        self.shots = []
        self.parse(open(path, encoding='utf-8').read())

    def p(self, rel):
        return rel if os.path.isabs(rel) else os.path.normpath(os.path.join(self.base, rel))

    def parse(self, src):
        shot = None
        actors = {}
        for raw in src.splitlines():
            line = raw.split('#')[0].strip() if not raw.strip().startswith('"') else raw.strip()
            if '"' in raw:
                line = raw.strip()
                if line.startswith('#'):
                    continue
            if not line or line.startswith('-I-'):
                continue
            tok = shlex.split(line, comments=True)
            if not tok:
                continue
            cmd = tok[0]
            if cmd == 'size':
                self.W, self.H = int(tok[1]), int(tok[2])
            elif cmd == 'fps':
                self.fps = int(tok[1])
            elif cmd == 'letterbox':
                self.box = int(tok[1])
            elif cmd == 'shot':
                shot = Shot(float(tok[1]), tok[2] if len(tok) > 2 else '')
                self.shots.append(shot)
                actors = {}
            elif cmd == 'bg':
                shot.bg_path = self.p(tok[1])
            elif cmd == 'camera':
                if tok[1] == 'push':
                    shot.cam['push'] = float(tok[2])
                elif tok[1] == 'pan':
                    shot.cam['pan'] = (float(tok[2]), float(tok[3]))
                elif tok[1] == 'shake':
                    shot.cam['shake'] = float(tok[2])
            elif cmd == 'actor':
                a = Actor(tok[1], self.p(tok[2]), self.cache)
                o, _ = parse_opts(tok[3:])
                if 'at' in o or 'scale' in o:
                    a.place = (o.get('at', None), o.get('scale', 1.0))
                if 'x' in o:
                    a.place = ((o['x'], o.get('y', self.H / 2)), o.get('scale', 1.0))
                shot.actors.append(a)
                actors[a.name] = a
            elif cmd in actors:
                a = actors[cmd]
                verb = tok[1]
                o, rest = parse_opts(tok[2:])
                t0 = o.get('from', o.get('at', 0.0))
                t1 = o.get('to', None)
                fade = o.get('fade', 0.25)
                if verb == 'say':
                    text = rest[0]
                    sp = Speech(text, wav=self.p(o['wav']) if 'wav' in o else None, voice=o.get('voice', 'hy'),
                                speed=int(o.get('speed', 135)), pitch=int(o.get('pitch', 30)), workdir=self.cache)
                    a.speech.append((t0, sp))
                elif verb == 'blink':
                    a.blinks += [float(x) for x in rest] + ([o['at']] if 'at' in o else [])
                elif verb == 'brow':
                    a.brows.append((t0, t1 or t0 + 0.8, o.get('amount', 1.0)))
                elif verb == 'still':
                    a.auto_blink = False
                else:
                    params = {}
                    for k in ('speed', 'stride', 'height', 'depth', 'angle', 'amount', 'times'):
                        if k in o:
                            params[k] = o[k]
                    if verb == 'look' and rest:
                        params['angle'] = float(rest[0])
                    if 'side' in o:
                        params['side'] = o['side']
                    elif rest and rest[0] in ('r', 'l'):
                        params['side'] = rest[0]
                    if 'direction' in o:
                        params['direction'] = 1 if o['direction'] in ('right', 1.0) else -1
                    a.clips.append(Clip(verb, t0, t1, fade=fade, **params))

    # ------------------------------------------------------------ rendering
    def placement(self, a):
        """Affine (2x3) from rig image space to frame space."""
        r = a.rig
        if a.place is None:   # cover-fit, centred
            s = max(self.W / r.w, self.H / r.h)
            return np.float32([[s, 0, (self.W - r.w * s) / 2], [0, s, (self.H - r.h * s) / 2]])
        at, sc = a.place
        if at is None:
            at = (self.W / 2, self.H / 2)
        if isinstance(at, float):
            at = (at, self.H / 2)
        s = max(self.W / r.w, self.H / r.h) * sc
        return np.float32([[s, 0, at[0] - r.w * s / 2], [0, s, at[1] - r.h * s / 2]])

    def render_frame(self, shot, t):
        W, H = self.W, self.H
        surf = skia.Surface(W, H)
        c = surf.getCanvas()
        c.clear(skia.ColorBLACK)
        base = None
        if shot.bg_path:
            base = cv2.imread(shot.bg_path).astype(np.float32) / 255
        elif shot.actors:
            a0 = shot.actors[0]
            base = cv2.warpAffine(a0.rig.bg, self.placement(a0), (W, H), borderMode=cv2.BORDER_REFLECT)
        if base is not None:
            if base.shape[:2] != (H, W):
                base = cv2.resize(base, (W, H))
            c.drawImage(_to_skia(base), 0, 0)
        for a in shot.actors:
            r = a.rig
            tex = r.img
            if a.face is not None:
                fp = a.face_params(t)
                if fp['jaw'] > 0.01 or fp['blink'] > 0.01 or fp['brow'] > 0.01:
                    tex = a.face.render(r.img, fp)
            pose = evaluate(a.clips, r, t)
            V, _ = skin(r, pose)
            M = self.placement(a)
            Vf = V @ M[:, :2].T + M[:, 2]
            rgba = np.dstack([tex[..., ::-1], r.mask])
            img = _to_skia(rgba, alpha=True)
            sh = img.makeShader(skia.TileMode.kClamp, skia.TileMode.kClamp)
            pos = [skia.Point(float(x), float(y)) for x, y in Vf]
            uv = [skia.Point(float(x), float(y)) for x, y in r.verts]
            idx = [int(i) for i in r.tris.ravel()]
            v = skia.Vertices(skia.Vertices.kTriangles_VertexMode, pos, uv, None, idx)
            c.drawVertices(v, skia.Paint(AntiAlias=True, Shader=sh))
        out = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3][..., ::-1].astype(np.float32) / 255
        # camera
        k = ease(t / max(shot.dur, 1e-3))
        z = 1 + (shot.cam['push'] - 1) * k
        dx, dy = shot.cam['pan'][0] * k, shot.cam['pan'][1] * k
        if shot.cam['shake']:
            r_ = np.random.default_rng(int(t * self.fps))
            dx += r_.normal(0, shot.cam['shake']); dy += r_.normal(0, shot.cam['shake'])
        if z != 1 or dx or dy:
            Mc = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
            Mc[:, 2] += (dx, dy)
            out = cv2.warpAffine(out, Mc, (W, H), borderMode=cv2.BORDER_REFLECT)
        return out

    def render(self, out_mp4, frames_dir=None):
        frames_dir = frames_dir or os.path.join(self.cache, 'frames')
        os.makedirs(frames_dir, exist_ok=True)
        for f_ in os.listdir(frames_dir):
            os.remove(os.path.join(frames_dir, f_))
        total = sum(s.dur for s in self.shots)
        audio = np.zeros(int((total + 1) * SR))
        n = 0
        t_shot = 0.0
        for si, shot in enumerate(self.shots):
            nf = int(round(shot.dur * self.fps))
            for f in range(nf):
                fr = self.render_frame(shot, f / self.fps)
                if self.box:
                    canvas = np.zeros((self.box, self.W, 3), np.float32)
                    y0 = (self.box - self.H) // 2
                    canvas[y0:y0 + self.H] = fr
                    fr = canvas
                cv2.imwrite(os.path.join(frames_dir, f'{n:05d}.png'), (np.clip(fr, 0, 1) * 255 + 0.5).astype(np.uint8))
                n += 1
            for a in shot.actors:
                for (t0, sp) in a.speech:
                    i = int((t_shot + t0) * SR)
                    seg = sp.audio[:max(0, len(audio) - i)]
                    audio[i:i + len(seg)] += seg
            t_shot += nf / self.fps
            print(f'-I- shot {si + 1}/{len(self.shots)} "{shot.title}" {nf} frames', flush=True)
        wav = os.path.join(self.cache, 'mix.wav')
        sf.write(wav, audio[:int(t_shot * SR)].astype(np.float32), SR)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(self.fps), '-i', os.path.join(frames_dir, '%05d.png'), '-i', wav,
                        '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                        '-shortest', '-movflags', '+faststart', out_mp4], check=True)
        return out_mp4


def _to_skia(arr, alpha=False):
    a = np.clip(arr, 0, 1)
    if not alpha:
        a = np.dstack([a[..., ::-1], np.ones(a.shape[:2])])
    a8 = np.ascontiguousarray((a * 255 + 0.5).astype(np.uint8))
    return skia.Image.fromarray(a8, colorType=skia.kRGBA_8888_ColorType,
                                alphaType=skia.kUnpremul_AlphaType)
