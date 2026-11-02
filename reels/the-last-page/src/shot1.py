"""Shot 1 - Before Dawn (0:00-0:07). Black, wind, fade up on the sea of clouds and the tower."""
import numpy as np, cv2, math
from core import *
from fx import *
from bg_tower import *

N = 168


class Shot:
    def __init__(self, seed=7):
        rng = np.random.default_rng(seed)
        h, w = H, W
        sky = vgrad(h, w, [(0, hexc('#10163d')), (0.4, hexc('#262a66')), (0.62, hexc('#4a447f')), (0.74, hexc('#8a6c9c')), (0.82, hexc('#c8909e')), (1, hexc('#50487e'))])
        st = (np.random.default_rng(3).random((h, w)) > 0.9994).astype(np.float32) * np.clip(1 - np.linspace(0, 1.7, h), 0, 1)[:, None]
        sky += cv2.GaussianBlur(st, (0, 0), 0.7)[..., None] * 1.2
        img = sky.copy()
        L = [(h * 0.66, 14, 30, 40, 0.45, '#c99bb2', '#7d6a9e', '#4a4782', None),
             (h * 0.71, 20, 44, 34, 0.5, '#a98fbf', '#625c98', '#393a74', 'tower'),
             (h * 0.80, 30, 64, 26, 0.6, '#8f82bd', '#4f4f8c', '#2b2c63', None)]
        for (y, r0, r1, n, fl, l, m, sd, tag) in L:
            if tag == 'tower':
                tr, ta, self.wins = tower_layer(h, w, rng, cx=w * 0.66, base_y=h * 0.71, scale=0.80)
                comp(img, tr, ta)
            c, a = cumulus(h, w, rng, [dict(y=y, x0=-80, x1=w + 80, r0=r0, r1=r1, n=n, jitter=r0 * 0.5, flat=fl)], hexc(l), hexc(m), hexc(sd), rim=hexc('#f0c3c3'), rim_amt=0.6)
            comp(img, c, a)
        self.bg = gouache(img, rng, hue_jit=0.008, val_jit=0.018, passes=((26, 0.5), (12, 0.6), (5, 0.7), (2.5, 0.8))).astype(np.float32) / 255
        # near cloud bank drifts very slowly (separate painted layer, wider than frame)
        ww = w + 200
        c, a = cumulus(h, ww, rng, [dict(y=h * 0.95, x0=-80, x1=ww + 80, r0=50, r1=95, n=22, jitter=20, flat=0.7)], hexc('#7d76b4'), hexc('#3f4180'), hexc('#222457'), rim=hexc('#e7bdd0'), rim_amt=0.8)
        base = np.zeros((h, ww, 3), np.float32) + hexc('#3f4180')[:3]
        comp(base, c, a)
        self.near = gouache(base, rng, hue_jit=0.008, val_jit=0.018, passes=((26, 0.5), (12, 0.6), (5, 0.7))).astype(np.float32) / 255
        self.near_a = cv2.GaussianBlur(a, (0, 0), 1.0)

    def frame(self, f):
        t = f / FPS
        h, w = H, W
        img = self.bg.copy()
        # one small warm light moves across a window (someone? something? - the fox's lantern)
        wx, wy, ww_, wh = self.wins[4]
        u = ease(t, 2.2, 5.6, 'inout')
        lx = wx - ww_ * 0.9 + u * ww_ * 1.8
        ttw = on_twos(f) / FPS
        flick = 0.85 + 0.15 * math.sin(ttw * 17) * math.sin(ttw * 5.3)
        vis = np.clip((t - 1.8) / 0.4, 0, 1) * np.clip((6.3 - t) / 0.4, 0, 1)
        if vis > 0:
            m = np.zeros((h, w), np.float32)
            pts = [(wx - ww_, wy + wh * 0.7), (wx - ww_, wy - wh * 0.45), (wx, wy - wh * 0.75), (wx + ww_, wy - wh * 0.45), (wx + ww_, wy + wh * 0.7)]
            m = poly_mask(h, w, pts, feather=0.6)
            yy, xx = np.mgrid[0:h, 0:w]
            g = np.exp(-(((xx - lx) / (ww_ * 0.9)) ** 2 + ((yy - wy) / (wh * 0.6)) ** 2))
            img += (m * g * vis * flick)[..., None] * hexc('#ffc06a')[:3] * 1.3
            img = glow(img, lx, wy, 14, hexc('#ff9a4a'), 0.18 * vis * flick)
        # near clouds drift
        off = int(round(100 - t * 4.5))
        nb = self.near[:, off:off + w]
        na = self.near_a[:, off:off + w]
        img = img * (1 - na[..., None]) + nb * na[..., None]
        # foreground pampas grass, silhouetted against the clouds
        def fg(c):
            gust = 0.25 * max(0, math.sin(t * 0.9 - 1.0))
            draw_pampas(c, 80, h + 10, 250, on_twos(f) / FPS, 0.5, 11, hexc('#3a335f')[:3], hexc('#1d1a38')[:3], n=7, gust=gust, lit_col=hexc('#b48fb4')[:3])
            draw_pampas(c, 1200, h + 10, 210, on_twos(f) / FPS + 0.7, 0.5, 12, hexc('#363059')[:3], hexc('#1b1834')[:3], n=6, gust=gust, lit_col=hexc('#a987b0')[:3])
        a = layer(fg)
        a = light_layer(a, rim=(-1, 1, hexc('#d9a2b8'), 0.25))
        over(img, a)
        # black, then fade up (the wind comes first)
        k = ease(t, 0.9, 3.4, 'inout') ** 1.3
        img = fade(img, k)
        return post(to8(img), f, grain=0.014, vignette=0.28)
