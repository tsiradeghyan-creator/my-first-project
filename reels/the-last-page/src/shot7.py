"""Shot 7 - Sunrise (0:39-0:44). The sun clears the sea of clouds; the fox, tiny on a stone balcony,
fur and grass whipping in the wind, looks up. A great ring of wind rolls outward across the clouds."""
import numpy as np, cv2, math
from core import *
from fx import *
from fox import *
from bg_tower import cumulus, comp

N = 120
SUN = (430, 0)


def dawn_sky(h, w, rng, sun_xy, warm=1.0):
    sky = vgrad(h, w, [(0, hexc('#2f4a8a')), (0.3, hexc('#7a8fc4')), (0.52, hexc('#f2b38e')), (0.64, hexc('#ffd59a')), (1, hexc('#ffcf9a'))])
    sky = glow(sky, sun_xy[0], sun_xy[1], 190, hexc('#ffd27a'), 0.4 * warm)
    sky = glow(sky, sun_xy[0], sun_xy[1], 90, hexc('#fff0c0'), 0.6 * warm)
    return sky


class Shot:
    def __init__(self, seed=71):
        rng = np.random.default_rng(seed)
        h, w = H, W
        self.horizon = int(h * 0.56)
        sky = dawn_sky(h, w, rng, (SUN[0], self.horizon - 10))
        # far streaks of cloud in the sky
        for k in range(6):
            y = rng.uniform(40, 200)
            x = rng.uniform(0, w)
            m = np.zeros((h, w), np.float32)
            cv2.ellipse(m, (int(x), int(y)), (int(rng.uniform(120, 300)), int(rng.uniform(5, 10))), rng.uniform(-3, 3), 0, 360, 1.0, -1, cv2.LINE_AA)
            m = cv2.GaussianBlur(m, (0, 0), 3)
            comp(sky, np.zeros_like(sky) + hexc('#f6c0a8')[:3], m * 0.7)
        self.sky = gouache(np.clip(sky, 0, 1), rng, hue_jit=0.006, val_jit=0.015, passes=((26, 0.5), (12, 0.6), (5, 0.7))).astype(np.float32) / 255
        # cloud sea, lit gold from the low sun on the left (separate layer so the sun can rise behind it)
        cl = np.zeros((h, w, 3), np.float32)
        ca = np.zeros((h, w), np.float32)
        rows = [(self.horizon + 6, 12, 26, 60, 0.4, '#fff0cc', '#e9a49a', '#8f7aa8'),
                (self.horizon + 30, 20, 40, 44, 0.45, '#ffe8c0', '#e0959a', '#7a6aa2'),
                (self.horizon + 75, 32, 66, 30, 0.55, '#ffdfb4', '#cf8792', '#625b98'),
                (h * 0.97, 60, 110, 18, 0.65, '#fbd2a8', '#b9788c', '#4e4c88')]
        for (y, r0, r1, n, fl, l, m_, sd) in rows:
            c, a = cumulus(h, w, rng, [dict(y=y, x0=-80, x1=w + 80, r0=r0, r1=r1, n=n, jitter=r0 * 0.5, flat=fl)], hexc(l), hexc(m_), hexc(sd),
                           rim=hexc('#fff4d0'), rim_amt=0.9, lightdir=(-0.45, -0.3))
            comp(cl, c, a)
            ca = np.maximum(ca, a)
        base = self.sky.copy()
        comp(base, cl, ca)
        painted = gouache(np.clip(base, 0, 1), rng, hue_jit=0.006, val_jit=0.018, passes=((22, 0.5), (11, 0.6), (5, 0.7), (2.5, 0.8))).astype(np.float32) / 255
        self.clouds = painted
        self.cloud_a = cv2.GaussianBlur(ca, (0, 0), 0.8)
        # stone balcony in the foreground (right), with a slice of tower wall
        fg = np.zeros((h, w, 3), np.float32)
        fa = np.zeros((h, w), np.float32)
        par = np.array([[640, 430], [1290, 418], [1290, h + 5], [600, h + 5]])
        m = poly_mask(h, w, par, smooth=False)
        stone = value_noise(h, w, 6, rng, octaves=3)
        col = mix(hexc('#c99a82')[:3], hexc('#6d566e')[:3], np.clip(stone * 0.6 + (np.arange(h)[:, None] - 430) / 200, 0, 1)[..., None])
        comp(fg, col, m)
        fa = np.maximum(fa, m)
        # parapet top cap lit by the sun
        cap = np.array([[630, 422], [1290, 410], [1290, 432], [636, 444]])
        m = poly_mask(h, w, cap, smooth=False)
        comp(fg, np.zeros_like(fg) + hexc('#ffd1a6')[:3], m)
        fa = np.maximum(fa, m)
        for k in range(8):
            x = 660 + k * 82
            cv2.line(fg, (x, 444), (x - 6, h), (0.35, 0.27, 0.33), 2, cv2.LINE_AA)
        wall = np.array([[1130, -5], [1290, -5], [1290, 420], [1150, 425]])
        m = poly_mask(h, w, wall, smooth=False)
        wn = value_noise(h, w, 8, rng, octaves=3)
        comp(fg, mix(hexc('#a07e86')[:3], hexc('#4e3f5e')[:3], np.clip(wn * 0.5 + 0.4, 0, 1)[..., None]), m)
        fa = np.maximum(fa, m)
        ivy = np.zeros((h, w), np.float32)
        for _ in range(500):
            x = 1140 + abs(rng.normal(0, 40))
            y = rng.uniform(0, 420)
            cv2.circle(ivy, (int(x), int(y)), int(rng.uniform(2, 5)), 1.0, -1, cv2.LINE_AA)
        ivy = np.minimum(ivy, fa)
        comp(fg, np.zeros_like(fg) + hexc('#6f8a4e')[:3], ivy * 0.9)
        base = np.zeros((h, w, 3), np.float32) + hexc('#6d566e')[:3]
        comp(base, fg, fa)
        self.fg = gouache(np.clip(base, 0, 1), rng, hue_jit=0.006, val_jit=0.02, passes=((10, 0.5), (5, 0.6), (2.5, 0.7))).astype(np.float32) / 255
        self.fg_a = fa
        self.grass = [(rng.uniform(680, 1120), 425 + rng.uniform(-6, 4), rng.uniform(18, 34), rng.integers(1e6)) for _ in range(12)]

    def frame(self, f):
        t = f / FPS
        ta = on_twos(f) / FPS
        h, w = H, W
        # the sun clears the cloud sea
        sy = self.horizon + 30 - 70 * ease(t, 0, 4.6, 'out')
        img = dawn_sky(h, w, None, (SUN[0], sy), warm=0.6 + 0.4 * ease(t, 0, 3))
        img = img * 0.35 + self.sky * 0.65
        disk = np.zeros((h, w), np.float32)
        cv2.circle(disk, (SUN[0], int(sy)), 34, 1.0, -1, cv2.LINE_AA)
        img = img * (1 - disk[..., None]) + disk[..., None] * hexc('#fff6dc')[:3]
        img = glow(img, SUN[0], sy, 70, hexc('#fff0c0'), 0.8)
        img = img * (1 - self.cloud_a[..., None]) + self.clouds * self.cloud_a[..., None]
        # ring of wind rolling outward across the clouds (perspective ellipse)
        rt = t - 1.4
        if rt > 0:
            R = 60 + rt * 420
            ring = np.zeros((h, w), np.float32)
            cy = self.horizon + 60
            cv2.ellipse(ring, (720, cy), (int(R), int(R * 0.16)), 0, 180, 360, 1.0, max(2, int(6 + rt * 6)), cv2.LINE_AA)
            cv2.ellipse(ring, (720, cy), (int(R), int(R * 0.16)), 0, 0, 180, 1.0, max(2, int(10 + rt * 10)), cv2.LINE_AA)
            ring = cv2.GaussianBlur(ring, (0, 0), 3 + rt * 2) * math.exp(-rt * 0.7)
            ring *= (np.arange(h)[:, None] > self.horizon - 5)
            img = img + ring[..., None] * hexc('#fff3dc')[:3] * 0.75

            def streaks(c):
                r = np.random.default_rng(int(on_twos(f)))
                for k in range(60):
                    a = r.uniform(0, 2 * math.pi)
                    rr = R * r.uniform(0.92, 1.06)
                    x = 720 + math.cos(a) * rr
                    y = cy + math.sin(a) * rr * 0.16
                    if y < self.horizon:
                        continue
                    dx, dy = math.cos(a) * 26, math.sin(a) * 4
                    c.drawPath(poly_path([(x, y), (x + dx, y + dy)], False, False), paint_(hexc('#fff6e6'), 0.5 * math.exp(-rt * 0.6), stroke=True, width=1.6))
            over(img, layer(streaks))
        img = img * (1 - self.fg_a[..., None]) + self.fg * self.fg_a[..., None]
        # the fox: tiny, facing the sun, fur and grass whipping
        wind = 0.6 + 0.4 * math.sin(ta * 9.0)
        look = ease(t, 1.2, 2.0)
        p = dict(x=860, y=430, s=0.95, flip=1, head_tilt=-0.55 * look, head_y=-4 * look, mouth=0.35 * look,
                 ear_l=0.35 + 0.1 * math.sin(ta * 13), ear_r=0.3 + 0.1 * math.sin(ta * 11 + 1), earflat=0.25,
                 tail_a=0.05, tail_curl=-0.15, tail_lag=-0.35 + 0.25 * math.sin(ta * 12.5), lean=0.1)

        def draw(c):
            for (gx, gy, gh, gs) in self.grass:
                rr = np.random.default_rng(gs)
                for k in range(5):
                    b = gx + rr.normal(0, 5)
                    bend = (0.6 + 0.4 * math.sin(ta * 10 + rr.uniform(0, 6))) * wind
                    pts = [(b, gy), (b + bend * gh * 0.25, gy - gh * 0.5), (b + bend * gh * 0.75, gy - gh * 0.8)]
                    c.drawPath(ink_ribbon(np.array(pts, np.float32), 2.2, 0.3, 2.4), paint_(mix(hexc('#7d8a4a'), hexc('#d9c27a'), rr.random())))
            draw_side_fox(c, p, 'dawn', seed=on_twos(f) // 2, light=(0.7, -0.5), lw=1.2)
        a = layer(draw)
        a = light_layer(a, ambient=(0.85, 0.75, 0.8), rim=(-3, -1, hexc('#ffe2a8'), 0.9))
        over(img, a)
        img = bloom(img, 0.88, 14, 0.25)
        return post(to8(img), 7000 + f, grain=0.012, vignette=0.22)
