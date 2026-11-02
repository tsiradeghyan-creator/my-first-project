"""Shot 5 - The Library Stirs (0:25-0:32). Hard cuts between held key poses as the tension builds."""
import numpy as np, cv2, math
from core import *
from fx import *
from fox import *

N = 168
CUTS = [(0, 38), (38, 72), (72, 106), (106, 142), (142, 168)]   # a b c d e


def book_row(rng, x0, x1, base_y, shelf_h):
    books = []
    x = x0
    while x < x1:
        bw = rng.uniform(14, 34)
        bh = shelf_h * rng.uniform(0.66, 0.95)
        col = hexc(BOOK_COLS[rng.integers(len(BOOK_COLS))])[:3] * rng.uniform(0.75, 1.15)
        books.append(dict(x=x, w=bw, h=bh, col=col, lean=rng.uniform(-0.03, 0.03), bands=rng.integers(1, 4),
                          ph=rng.uniform(0, 6.28), label=rng.random() < 0.5, moss=rng.random() < 0.2))
        x += bw + (rng.uniform(1, 3) if rng.random() < 0.3 else 0.5)
    return books


def draw_book(c, b, base_y, dx=0.0, rot=0.0, lit=1.0):
    c.save()
    c.translate(b['x'] + b['w'] / 2 + dx, base_y)
    c.rotate(math.degrees(b['lean'] + rot))
    w, h = b['w'], b['h']
    col = b['col'] * lit
    c.drawRect(skia.Rect(-w / 2, -h, w / 2, 0), paint_(col))
    c.drawRect(skia.Rect(w / 2 - w * 0.2, -h, w / 2, 0), paint_(col * 1.3, 0.8))
    c.drawRect(skia.Rect(-w / 2, -h, -w / 2 + w * 0.22, 0), paint_(col * 0.55, 0.9))
    r = np.random.default_rng(int(b['x'] * 10) + 1000)
    for k in range(b['bands']):
        y = -h * r.uniform(0.12, 0.88)
        c.drawRect(skia.Rect(-w / 2, y, w / 2, y + r.uniform(1.5, 3.5)), paint_(hexc('#b8995a')[:3] * lit, 0.85))
    if b['label']:
        y = -h * 0.62
        c.drawRect(skia.Rect(-w / 2 + 3, y, w / 2 - 3, y + 16), paint_(hexc('#d6c69e')[:3] * 0.8 * lit, 0.85))
    if b['moss']:
        for k in range(10):
            c.drawCircle(float(r.uniform(-w / 2, w / 2)), float(-r.uniform(0, h * 0.4)), float(r.uniform(1.5, 3.5)), paint_(hexc('#55703c')[:3] * lit, 0.85))
    c.drawRect(skia.Rect(-w / 2, -h, w / 2, 0), paint_(hexc('#1c1418'), 0.9, stroke=True, width=1.2))
    c.restore()


class Stream:
    """A thin stream of dust sifting down from a shelf edge."""

    def __init__(self, rng, x, y, n=40):
        self.x, self.y = x, y
        self.off = rng.uniform(0, 1, n)
        self.dx = rng.normal(0, 3.0, n)
        self.r = rng.uniform(0.5, 1.4, n)

    def draw(self, c, t, t0, col, length=300):
        if t < t0:
            return
        age = t - t0
        for o, dx, r in zip(self.off, self.dx, self.r):
            u = (o + age * 0.6) % 1.0
            if u * 1.0 > age * 1.5:
                continue
            y = self.y + (u ** 1.6) * length
            x = self.x + dx * u * 4
            c.drawCircle(float(x), float(y), float(r), paint_(col, 0.4 * (1 - u)))
            c.drawPath(poly_path([(x, y - 5 * r), (x, y)], False, False), paint_(col, 0.25 * (1 - u), stroke=True, width=r))


class Shot:
    def __init__(self, seed=41):
        rng = np.random.default_rng(seed)
        h, w = H, W
        # a/b: shelf close-up (painted backdrop, trembling row as live drawings)
        img, _ = shelves_base(w, h, rng, shelf_h=120, top_dark=0.45, tint=(0.6, 0.62, 0.9))
        self.rowY = 300
        cv2.rectangle(img, (0, self.rowY - 130), (w, self.rowY), (0.08, 0.07, 0.1), -1)   # shelf back
        cv2.rectangle(img, (0, self.rowY), (w, self.rowY + 14), (0.26, 0.18, 0.15), -1)
        cv2.rectangle(img, (0, self.rowY + 11), (w, self.rowY + 17), (0.13, 0.09, 0.08), -1)
        self.bgA = gouache(np.clip(img, 0, 1), rng, hue_jit=0.006, val_jit=0.02, passes=((12, 0.45), (6, 0.6), (3, 0.7))).astype(np.float32) / 255
        self.row = book_row(rng, -10, w + 10, self.rowY, 122)
        self.hero = min(range(len(self.row)), key=lambda i: abs(self.row[i]['x'] - 610))
        self.streams = [Stream(rng, b['x'] + b['w'] / 2 + rng.normal(0, 4), self.rowY + 16, 26) for b in self.row[::5]]
        # c: lantern on the stone floor
        fl = vgrad(h, w, [(0, hexc('#12111a')), (0.55, hexc('#1d1b27')), (1, hexc('#2a2633'))])
        for k in range(-6, 12):
            x0 = 640 + k * 150
            cv2.line(fl, (int(640 + (x0 - 640) * 0.3), 250), (int(x0), h), (0.1, 0.1, 0.13), 2, cv2.LINE_AA)
        for yy in (300, 360, 450):
            cv2.line(fl, (0, yy), (w, yy), (0.1, 0.1, 0.13), 2, cv2.LINE_AA)
        self.bgC = gouache(fl, rng, hue_jit=0.005, val_jit=0.02, passes=((14, 0.45), (7, 0.55), (3, 0.7))).astype(np.float32) / 255
        # d: fox medium, shelves behind (dark, blurred)
        img, _ = shelves_base(w, h, rng, shelf_h=70, top_dark=0.8, tint=(0.5, 0.52, 0.8))
        img = cv2.GaussianBlur(img, (0, 0), 3)
        img[430:] = vgrad(h - 430, w, [(0, hexc('#25222f')), (1, hexc('#15131c'))])
        self.bgD = gouache(np.clip(img, 0, 1), rng, hue_jit=0.006, val_jit=0.02, passes=((14, 0.45), (7, 0.55))).astype(np.float32) / 255
        # e: the hall, all of it, holding its breath
        img, _ = shelves_base(w, h, rng, shelf_h=40, top_dark=0.9, tint=(0.62, 0.64, 0.95))
        img[int(h * 0.88):] = vgrad(h - int(h * 0.88), w, [(0, hexc('#25232f')), (1, hexc('#121119'))])
        img += moon_shaft(h, w, w * 0.62, w * 0.48, 70, 200, hexc('#9fb2ff'), 0.3, soft=24)
        self.bgE = gouache(np.clip(img, 0, 1), rng, hue_jit=0.006, val_jit=0.02, passes=((14, 0.45), (7, 0.55), (3.5, 0.7))).astype(np.float32) / 255
        self.frozen = None

    def shelf_shot(self, f, t, all_rows):
        img = self.bgA.copy()
        ta = on_twos(f) / FPS
        r = np.random.default_rng(on_twos(f))

        def draw(c):
            for i, b in enumerate(self.row):
                trem = (i == self.hero) or all_rows
                amp = (1.6 if i == self.hero else 1.0) * (0.4 + ease(t, 0.1, 1.2) * 0.6) if trem else 0.0
                if all_rows:
                    amp *= 1.2
                dx = r.normal(0, 1) * amp
                rot = r.normal(0, 0.006) * amp
                draw_book(c, b, self.rowY + 1, dx, rot, lit=0.85)
            ta0 = 0.25 if not all_rows else 0.0
            for k, s in enumerate(self.streams):
                if all_rows or abs(s.x - (self.row[self.hero]['x'] + 10)) < 40:
                    s.draw(c, ta, ta0 + (k % 5) * 0.12, hexc('#b9b3a4'), 150)
        a = layer(draw)
        a = light_layer(a, ambient=(0.62, 0.64, 0.95), rim=(-2, 0, hexc('#9fb2ff'), 0.25))
        over(img, a)
        # tremor: whole frame shudders by a pixel, on twos
        sh = r.normal(0, 0.8 if all_rows else 0.4, 2)
        M = np.float32([[1.02, 0, sh[0] - W * 0.01], [0, 1.02, sh[1] - H * 0.01]])
        img = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        return img

    def frame(self, f):
        t = f / FPS
        ta = on_twos(f) / FPS
        h, w = H, W
        global W_
        if f < CUTS[0][1]:            # a: one book trembles
            img = self.shelf_shot(f, t, False)
            g = 3000
        elif f < CUTS[1][1]:          # b: the whole row
            img = self.shelf_shot(f, t - CUTS[1][0] / FPS, True)
            M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, 0.82)
            img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
            g = 3100
        elif f < CUTS[2][1]:          # c: the flame leans with no wind to move it
            lt = t - CUTS[2][0] / FPS
            img = self.bgC.copy()
            lean = 0.9 * ease(lt, 0.3, 0.9)
            flick = 0.92 + 0.08 * math.sin(ta * 21)
            lx, ly, ls = 640, 292, 6.0
            img = glow(img, lx - lean * 60, ly + 30 * ls - 10, 320, hexc('#ff9a48'), 0.5 * flick)
            img = glow(img, lx, ly + 17 * ls, 120, hexc('#ffc070'), 0.3 * flick)
            sh = np.zeros((h, w), np.float32)
            cv2.ellipse(sh, (lx, int(ly + 30 * ls)), (70, 9), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
            img *= (1 - cv2.GaussianBlur(sh, (0, 0), 4) * 0.5)[..., None]

            def draw(c):
                draw_lantern(c, lx, ly, ls, 0.0, lean, ta, 2)
                c.save()
                c.clipPath(poly_path([(lx + math.cos(a) * 9.5 * ls, ly + (17 + math.sin(a) * 10.5) * ls) for a in np.linspace(0, 6.28, 24)]), doAntiAlias=True)
                draw_flame(c, lx, ly + 23 * ls, ls * 0.95, lean, ta)
                c.restore()
            a = layer(draw)
            over(img, a)
            img = bloom(img, 0.7, 14, 0.45)
            g = 3200
        elif f < CUTS[3][1]:          # d: ears flatten - one hard key, then held
            lt = t - CUTS[3][0] / FPS
            img = self.bgD.copy()
            k = 1.0 if f - CUTS[3][0] >= 6 else (0.0 if f - CUTS[3][0] < 4 else 0.6)
            p = dict(x=560, y=470, s=2.6, earflat=k, crouch=0.85 * k, tail_a=0.3 - 0.55 * k, tail_curl=-0.1 * k,
                     head_y=8 * k, head_tilt=-0.15 + 0.1 * k, lean=-0.2 * k, look=0.2)
            a = layer(lambda c: draw_side_fox(c, p, 'moon', seed=7 if k < 1 else 8))
            a = light_layer(a, ambient=(0.6, 0.62, 0.9), lights=[(120, 520, 300, hexc('#ffaa60'), 0.45)], rim=(-3, -2, hexc('#a8b6ff'), 0.35))
            sh = np.zeros((h, w), np.float32)
            cv2.ellipse(sh, (560, 471), (150, 10), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
            img *= (1 - cv2.GaussianBlur(sh, (0, 0), 5) * 0.45)[..., None]
            over(img, a)
            g = 3300 + (0 if k < 1 else 1)  # held drawing: grain still breathes
            g = 3300 + f
        else:                          # e: total stillness - even the grain holds
            if self.frozen is None:
                self.frozen = post(to8(self.bgE.copy()), 3400, grain=0.016, vignette=0.34)
            return self.frozen
        return post(to8(img), g + f, grain=0.016, vignette=0.32)
