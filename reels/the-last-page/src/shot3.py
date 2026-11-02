"""Shot 3 - The Fox (0:14-0:18). Close-up: ears swivel one at a time, sniff, a real anime blink."""
import numpy as np, cv2, math
from core import *
from fx import *
from fox import *

N = 96


def pose(t, f):
    p = dict(x=640, y=300, s=2.75)
    # ears: left swivels toward a sound, then the right, each with a little overshoot
    p['ear_l'] = 0.9 * ease(t, 0.35, 0.6) - 0.25 * ease(t, 0.6, 0.8) - 0.4 * ease(t, 2.9, 3.3)
    p['ear_r'] = -0.8 * ease(t, 1.0, 1.25) + 0.2 * ease(t, 1.25, 1.45) + 0.45 * ease(t, 2.9, 3.3)
    # sniff: three quick lifts of the nose, nostrils flaring (keys on twos)
    if 1.55 < t < 2.35:
        u = (t - 1.55) / 0.8 * 3
        k = max(0.0, math.sin(u * math.pi)) ** 0.6
        p['nose_up'] = k
        p['nostril'] = k
        p['tilt'] = -0.02 * k
    # blink at 2.55s on ones: half, closed, closed, closed, half, open
    seq = {0: 0.55, 1: 1.0, 2: 1.0, 3: 1.0, 4: 0.5}
    bf = f - int(2.55 * FPS)
    b = seq.get(bf, 0.0)
    p['blink_l'] = p['blink_r'] = b
    # curious, a little afraid: eyes drift up toward the dark shelves at the end
    p['look_y'] = -1.0 * ease(t, 3.2, 3.7)
    p['look_x'] = 0.3 * ease(t, 0.4, 0.7) - 0.6 * ease(t, 1.0, 1.4) + 0.3 * ease(t, 3.2, 3.7)
    p['head_turn'] = 0.12 * ease(t, 0.4, 0.7) - 0.2 * ease(t, 1.0, 1.4)
    return p


class Shot:
    def __init__(self, seed=21):
        rng = np.random.default_rng(seed)
        h, w = H, W
        img, bm = shelves_base(w + 400, h + 300, rng, shelf_h=80, top_dark=0.7, tint=(0.75, 0.75, 1.0))
        img = cv2.resize(img[100:100 + h * 2 // 1, 100:100 + w], (w, h))
        img = cv2.GaussianBlur(img, (0, 0), 7)  # deep focus falls off behind the face
        img = glow(img, 180, h + 60, 420, hexc('#ff8a3a'), 0.35)
        self.bg = gouache(np.clip(img, 0, 1), rng, hue_jit=0.006, val_jit=0.015, passes=((18, 0.4), (9, 0.5))).astype(np.float32) / 255
        self.dust = Dust(rng, 40, (0, 0, w, h), vel=(2, -3), size=(0.6, 1.6))

    def frame(self, f):
        t = f / FPS
        h, w = H, W
        img = self.bg.copy()
        ta = on_twos(f) / FPS
        p = pose(ta, f)
        flick = 0.88 + 0.12 * math.sin(ta * 19) * math.sin(ta * 7.1)

        def draw(c):
            from fox import Ink, PAL
            k = Ink(c, PAL['lantern'], on_twos(f), light=(-0.6, -0.8))
            u = 60 * p['s']
            c.save(); c.translate(p['x'], p['y'])
            sgn = np.array([[-1, 1]])
            half = np.array([[0.0, 0.62], [0.62, 0.55], [0.85, 0.95], [1.05, 1.15], [0.98, 1.3], [1.22, 1.6], [1.12, 1.72], [1.35, 2.1], [1.45, 2.9]])
            body = np.vstack([half * sgn, half[::-1]]) * u
            k.part(body, 'fur', shade='fur_s', shade_off=0.12)
            bh = np.array([[0.0, 0.75], [0.45, 0.72], [0.7, 1.05], [0.55, 1.18], [0.74, 1.42], [0.5, 1.5], [0.6, 1.8], [0.3, 1.82], [0.42, 2.2], [0.15, 2.15], [0.2, 2.9]])
            bib = np.vstack([bh * sgn, bh[::-1]]) * u
            k.part(bib, 'cream', shade='cream_s', shade_off=0.06, line=False)
            for sg in (-1, 1):
                k.stroke(np.array([[0.45 * sg, 0.72], [0.7 * sg, 1.05], [0.55 * sg, 1.18], [0.74 * sg, 1.42]]) * u, lw=1.0)
            c.restore()
            draw_front_head(c, p, 'lantern', seed=on_twos(f) // 2, eye_glint=(1.0, 0.8 * flick, 0.45))
        a = layer(draw)
        a = light_layer(a, ambient=(0.55, 0.55, 0.78), lights=[(260, h + 40, 360, hexc('#ffa860'), 0.95 * flick)],
                        rim=(2, -2, hexc('#8fa2ff'), 0.4))
        over(img, a)
        d = layer(lambda c: self.dust.draw(c, ta, hexc('#ffd9a0'), alpha=0.35))
        over(img, d)
        img = bloom(img, 0.8, 8, 0.25)
        return post(to8(img), 2000 + f, grain=0.016, vignette=0.32)
