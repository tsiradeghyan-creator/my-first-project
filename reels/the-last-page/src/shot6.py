"""Shot 6 - The Pages Burst (0:32-0:39). Every book flies open, pages fold into paper birds; a low
angle up the circular stairwell as the flock spirals toward the dome; the copper shutters break
open and the first gold light crashes down the shaft."""
import numpy as np, cv2, math
from core import *
from fx import *

N = 168
CUT_B = 52    # 2.17s
CUT_C = 128   # 5.33s
PAPER_L = hexc('#efe3c4')[:3]
PAPER_S = hexc('#a99a86')[:3]
INK = hexc('#2a2026')[:3]


def morph_page_bird(c, x, y, size, heading, u, phase, var, light, shade, line, alpha=1.0):
    """u=0 flat torn page, u=1 folded paper bird. Hard drawn in-betweens (on twos)."""
    if u < 0.5:
        k = u / 0.5
        draw_page(c, x, y, size * 1.1 * (1 - 0.35 * k), size * 1.4 * (1 - 0.45 * k), heading + k * 0.8, 0.2 + 0.6 * k,
                  mix(shade, light, 0.8), line, alpha, writing=True, seed=int(var['seed']))
    else:
        draw_paper_bird(c, x, y, phase, size * (0.8 + 0.4 * (u - 0.5)), heading, var, light, shade, line, alpha)


class Shot:
    def __init__(self, seed=61):
        rng = np.random.default_rng(seed)
        h, w = H, W
        # a: wall of shelves, mid shot
        img, _ = shelves_base(w, h, rng, shelf_h=64, top_dark=0.6, tint=(0.62, 0.64, 0.95))
        self.bgA = gouache(np.clip(img, 0, 1), rng, hue_jit=0.006, val_jit=0.02, passes=((12, 0.45), (6, 0.55), (3, 0.7))).astype(np.float32) / 255
        self.shelf_rows = [h - 30 - k * 75 for k in range(7)]
        # burst particles: pages from random shelf spots
        n = 150
        self.A = dict(x0=rng.uniform(-20, w + 20, n), y0=rng.choice(self.shelf_rows, n) - rng.uniform(10, 50, n),
                      t0=rng.uniform(0.15, 0.7, n), vx=rng.normal(0, 160, n), vy=rng.uniform(-420, -160, n),
                      size=rng.uniform(16, 34, n), ph=rng.uniform(0, 1, n), seed=rng.integers(0, 1e6, n),
                      span=rng.uniform(0.8, 1.2, n), sweep=rng.uniform(-0.2, 0.2, n), ink=rng.random(n))
        # b/c: looking straight up the circular stairwell
        cx, cy = w * 0.5, h * 0.36
        self.center = (cx, cy)
        img = np.zeros((h, w, 3), np.float32) + hexc('#0d0e1a')[:3]
        yy, xx = np.mgrid[0:h, 0:w]
        ang = np.arctan2(yy - cy, xx - cx)
        rad = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 1.15) ** 2)
        rings = [60, 95, 140, 200, 280, 390, 540, 760, 1050]
        for i in range(len(rings) - 1, 0, -1):
            r0, r1 = rings[i - 1], rings[i]
            band = (rad >= r0) & (rad < r1)
            u = (rad - r0) / (r1 - r0)
            # each ring: stone balustrade lip (outer) + shelf band with books (inner)
            shelf = (u > 0.18) & (u < 0.8)
            nseg = int(2 * math.pi * r0 / 9) + 8
            segi = ((ang + math.pi) / (2 * math.pi) * nseg).astype(int)
            bookcol = np.array([hexc(c_)[:3] for c_ in BOOK_COLS])[(segi * 7 + i * 13) % len(BOOK_COLS)]
            vary = (np.sin(segi * 12.9898 + i * 78.233) * 43758.5453) % 1.0
            depth = 0.25 + 0.75 * (i / len(rings))
            col = np.where(shelf[..., None], bookcol * (0.55 + 0.45 * vary[..., None]), hexc('#4a4560')[:3] * (0.7 + 0.5 * u[..., None]))
            img = np.where(band[..., None], col * depth, img)
            # balustrade posts
            posts = (np.abs(((ang + math.pi) / (2 * math.pi) * nseg / 3) % 1 - 0.5) < 0.06) & (u > 0.82)
            img = np.where((band & posts)[..., None], hexc('#6a6688')[:3] * depth, img)
        # dome oculus with closed copper shutters
        inner = rad < rings[0]
        img = np.where(inner[..., None], hexc('#2a4a52')[:3], img)
        self.inner_r = rings[0]
        img = np.clip(img, 0, 1)
        self.bgB = gouache(img, rng, hue_jit=0.006, val_jit=0.025, passes=((12, 0.45), (6, 0.55), (3, 0.65))).astype(np.float32) / 255
        nb = 230
        self.B = dict(r0=rng.uniform(260, 900, nb), a0=rng.uniform(0, 2 * math.pi, nb), spd=rng.uniform(0.7, 1.3, nb),
                      size=rng.uniform(10, 26, nb), ph=rng.uniform(0, 1, nb), seed=rng.integers(0, 1e6, nb),
                      span=rng.uniform(0.8, 1.2, nb), sweep=rng.uniform(-0.2, 0.2, nb), ink=rng.random(nb), dl=rng.uniform(0, 1.2, nb))

    # ------------------------------------------------------------------ a
    def burst(self, f):
        t = f / FPS
        ta = on_twos(f) / FPS
        img = self.bgA.copy()
        A = self.A
        flash = math.exp(-max(0, ta - 0.15) * 6) * (ta > 0.15)
        img = img + flash * 0.25 * hexc('#fff1c8')[:3]

        def draw(c):
            for i in range(len(A['x0'])):
                lt = ta - A['t0'][i]
                if lt < 0:
                    # the book jolts open: a pale sliver of pages on the shelf
                    continue
                x = A['x0'][i] + A['vx'][i] * lt
                y = A['y0'][i] + A['vy'][i] * lt + 90 * lt * lt
                u = min(1.0, lt / 0.4)
                u = round(u * 4) / 4      # hard, drawn in-betweens
                heading = math.atan2(A['vy'][i] + 180 * lt, A['vx'][i]) * 0.4
                var = dict(span=A['span'][i], sweep=A['sweep'][i], ink=A['ink'][i], seed=A['seed'][i])
                morph_page_bird(c, x, y, A['size'][i], heading, u, (A['ph'][i] + lt * 3.5) % 1, var, PAPER_L, PAPER_S, INK)
                # speed lines on the fastest frames
                if lt < 0.12:
                    c.drawPath(poly_path([(x, y), (x - A['vx'][i] * 0.05, y - A['vy'][i] * 0.05)], False, False), paint_(PAPER_L, 0.5, stroke=True, width=2))
        a = layer(draw)
        a = light_layer(a, ambient=(0.85, 0.85, 1.05), rim=(-1, -2, hexc('#ffffff'), 0.25))
        over(img, a)
        return post(to8(img), 6000 + f, grain=0.016, vignette=0.28)

    # ------------------------------------------------------------------ b, c
    def well(self, f):
        t = (f - CUT_B) / FPS
        ta = on_twos(f - CUT_B) / FPS
        h, w = H, W
        cx, cy = self.center
        img = self.bgB.copy()
        B = self.B
        tc = (CUT_C - CUT_B) / FPS
        open_k = ease(ta, tc, tc + 0.5, 'out')          # shutters
        light_k = ease(ta, tc + 0.15, tc + 0.9, 'in')   # gold light crashes down
        # shutters: copper petals that swing outward and break
        def shutters(c):
            for k in range(8):
                a0 = k / 8 * 2 * math.pi + 0.2
                spread = open_k * 1.1
                pts = [(cx, cy)]
                for j in range(6):
                    aa = a0 + j / 5 * (2 * math.pi / 8) * (1 - open_k * 0.5)
                    r = self.inner_r * (1 + open_k * 0.5)
                    pts.append((cx + math.cos(aa + spread * 0.3) * r, cy + math.sin(aa + spread * 0.3) * r / 1.15))
                pts = np.array(pts)
                pts = cx + (pts - [cx, cy]) * 1.0 + np.array([math.cos(a0 + 0.4), math.sin(a0 + 0.4)]) * open_k * 40
                pts[:, 1] = cy + (pts[:, 1] - cy)
                col = mix(hexc('#3a6a6a'), hexc('#c08a50'), open_k * 0.6)
                c.drawPath(poly_path(pts, True, False), paint_(col, 1 - open_k * 0.85))
                c.drawPath(poly_path(pts, True, False), paint_(INK, (1 - open_k) * 0.9, stroke=True, width=1.5))
        if open_k > 0:
            hole = np.zeros((h, w), np.float32)
            cv2.ellipse(hole, (int(cx), int(cy)), (int(self.inner_r * (0.4 + open_k * 0.7)), int(self.inner_r * (0.4 + open_k * 0.7) / 1.15)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
            hole = cv2.GaussianBlur(hole, (0, 0), 3)
            img = img * (1 - hole[..., None]) + hole[..., None] * hexc('#fff3c8')[:3]
        over(img, light_layer(layer(shutters), ambient=(0.8, 0.8, 0.95)))

        # the flock: a rising vortex - birds orbit and spiral inward (= upward) toward the dome
        def flock(c):
            order = np.argsort(-B['r0'])
            for i in order:
                lt = ta - B['dl'][i] * 0.6
                if lt < 0:
                    continue
                prog = 1 - math.exp(-lt * 0.55 * B['spd'][i])
                r = B['r0'][i] * (1 - prog * 0.92)
                a = B['a0'][i] + lt * 1.6 * B['spd'][i] * (1 + 2.5 * prog)
                x = cx + math.cos(a) * r
                y = cy + math.sin(a) * r / 1.15
                size = B['size'][i] * (0.3 + 0.7 * (r / 700) ** 0.8) * 2.6
                if size < 2.5:
                    continue
                heading = a + math.pi / 2 + 0.35
                var = dict(span=B['span'][i], sweep=B['sweep'][i], ink=B['ink'][i], seed=B['seed'][i])
                tone_l = mix(PAPER_L, hexc('#fff0c0')[:3], light_k)
                tone_s = mix(PAPER_S, hexc('#6a4a3a')[:3], light_k)
                draw_paper_bird(c, x, y, (B['ph'][i] + lt * 3.2) % 1, size, heading, var, tone_l, tone_s, INK, 1.0)
        a = layer(flock)
        a = light_layer(a, ambient=mix(np.array([0.78, 0.8, 1.0]), np.array([0.8, 0.62, 0.42]), light_k),
                        rim=(int(math.copysign(1, 0)), 1, hexc('#ffe1a0'), 0.6 * light_k))
        over(img, a)
        if light_k > 0:
            # god rays down the shaft (radial from the oculus), warm flood, then grade gold
            yy, xx = np.mgrid[0:h, 0:w]
            ang = np.arctan2(yy - cy, xx - cx)
            rays = 0.35 + 0.65 * (0.5 + 0.5 * np.sin(ang * 17 + 1.3) * np.sin(ang * 5.0 + 0.4)) ** 2
            d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
            fall = np.exp(-d / (300 + 600 * light_k))
            img = img + (rays * fall * light_k * 0.5)[..., None] * hexc('#ffd88a')[:3]
            img = img * mix(np.ones(3), np.array([1.15, 0.98, 0.72]), light_k * 0.7)
            img = glow(img, cx, cy, 120 * (0.5 + light_k), hexc('#fff2c0'), 0.7 * light_k)
        img = bloom(img, 0.8, 16, 0.3 + 0.25 * light_k)
        # slow, rising camera rotation as we stare up the well
        M = cv2.getRotationMatrix2D((cx, cy), -t * 2.5, 1.12 + 0.04 * t)
        img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        return post(to8(img), 6100 + f, grain=0.014, vignette=0.3)

    def frame(self, f):
        if f < CUT_B:
            return self.burst(f)
        return self.well(f)
