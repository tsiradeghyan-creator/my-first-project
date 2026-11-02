"""Tigran the Great - storyboard 09-16 as a 2.5D film, made entirely in code.

Each panel is cut into depth layers (GrabCut-refined polygons), the holes behind the subject are
inpainted, then a virtual camera moves through the layers with proper parallax. Atmosphere and
materials (fire, smoke, embers, ash, water, flags, cloth, splashes, arrows) are simulated on top.
Graded to The King reference used in trailer v3. See SHOT_PLAN.md.
"""
import math, os, subprocess, sys
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
PAN = os.path.join(HERE, '..', 'storyboard', 'panels')
REF = np.load(os.path.join(HERE, '..', 'trailer_v3', 'ref_stats.npy'))
OW, OH, PH = 1280, 720, 536           # output frame, picture height (2.39:1)
FPS = 24
FR = os.environ.get('FRAMES', '/tmp/tigran_frames')
RNG = np.random.default_rng(9)


# ------------------------------------------------------------------ helpers
def ease(t, a=0.0, b=1.0):
    t = np.clip((t - a) / (b - a + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


def grade(img):
    """Lab transfer to The King exterior statistics (as in trailer v3), slightly gentler."""
    lab = cv2.cvtColor(img.astype(np.float32) / 255, cv2.COLOR_BGR2LAB)
    s = lab.reshape(-1, 3)[::7]
    m, sd = s.mean(0), s.std(0) + 1e-3
    ref = REF[0] if m[0] > 30 else REF[1]
    t = (lab - m) / sd * ref[3:] + ref[:3]
    w = np.array([0.7, 0.9, 0.9], np.float32)
    t = lab * (1 - w) + t * w
    t[..., 0] = np.clip(t[..., 0], 0, 100)
    return np.clip(cv2.cvtColor(t.astype(np.float32), cv2.COLOR_LAB2BGR), 0, 1)


def poly_mask(shape, pts, feather=0):
    m = np.zeros(shape[:2], np.uint8)
    cv2.fillPoly(m, [np.int32(pts)], 255, cv2.LINE_AA)
    m = m.astype(np.float32) / 255
    if feather:
        m = cv2.GaussianBlur(m, (0, 0), feather)
    return m


def grabcut(img8, pts, iters=4):
    """Refine a rough polygon into a subject matte."""
    h, w = img8.shape[:2]
    sc = 0.5
    small = cv2.resize(img8, (int(w * sc), int(h * sc)))
    rough = poly_mask(small.shape, np.array(pts) * sc)
    mask = np.full(small.shape[:2], cv2.GC_BGD, np.uint8)
    dil = cv2.dilate((rough > 0.5).astype(np.uint8), np.ones((25, 25), np.uint8))
    ero = cv2.erode((rough > 0.5).astype(np.uint8), np.ones((15, 15), np.uint8))
    mask[dil > 0] = cv2.GC_PR_BGD
    mask[rough > 0.5] = cv2.GC_PR_FGD
    mask[ero > 0] = cv2.GC_FGD
    bg, fg = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(small, mask, None, bg, fg, iters, cv2.GC_INIT_WITH_MASK)
    m = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1.0, 0.0).astype(np.float32)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_LINEAR)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    return cv2.GaussianBlur(m, (0, 0), 1.2)


def inpaint(img, hole):
    """Fill behind a removed subject (half-res Telea, pasted back only in the hole)."""
    h, w = img.shape[:2]
    hole_d = cv2.dilate((hole > 0.15).astype(np.uint8), np.ones((15, 15), np.uint8))
    sc = 0.5
    sm = cv2.resize((img * 255).astype(np.uint8), (int(w * sc), int(h * sc)))
    hm = cv2.resize(hole_d, (int(w * sc), int(h * sc)), interpolation=cv2.INTER_NEAREST)
    f = cv2.inpaint(sm, hm, 9, cv2.INPAINT_TELEA)
    f = cv2.resize(f, (w, h)).astype(np.float32) / 255
    f = cv2.GaussianBlur(f, (0, 0), 2)
    m = cv2.GaussianBlur(hole_d.astype(np.float32), (0, 0), 3)[..., None]
    return img * (1 - m) + f * m


class Plate:
    """A panel split into depth layers. specs: list of (name, polygon|'auto mask', z, grabcut?) near->far
    is NOT required; give them in any order, they are sorted by z (far first)."""

    def __init__(self, panel, specs, z_bg):
        img8 = cv2.imread(os.path.join(PAN, panel))
        self.img = grade(img8)
        self.h, self.w = self.img.shape[:2]
        self.layers = []
        mats = []
        for name, pts, z, gc in specs:
            m = grabcut(img8, pts) if gc else poly_mask(self.img.shape, pts, 1.2)
            mats.append((name, m, z))
        mats.sort(key=lambda d: -d[2])          # far -> near
        # background: everything, inpainted under every layer
        allm = np.zeros((self.h, self.w), np.float32)
        for _, m, _ in mats:
            allm = np.maximum(allm, m)
        self.layers.append(dict(name='bg', rgb=inpaint(self.img, allm), a=np.ones((self.h, self.w), np.float32), z=z_bg))
        for i, (name, m, z) in enumerate(mats):
            nearer = np.zeros_like(m)
            for _, m2, z2 in mats[i + 1:]:
                nearer = np.maximum(nearer, m2)
            rgb = inpaint(self.img, nearer * (1 - m)) if nearer.max() > 0 else self.img
            self.layers.append(dict(name=name, rgb=rgb, a=m, z=z))

    def layer(self, name):
        for L in self.layers:
            if L['name'] == name:
                return L


def render_plate(plate, view, focus, zf, dolly=0.0, truck=(0.0, 0.0), warp=None, extra=None):
    """Composite layers into the 2.39 picture.
    view = (cx, cy, vw) panel-space window centre and width; focus = panel point the dolly pushes to;
    dolly: fractional push (0.1 = 10% closer at the focus plane); truck: camera translation (panel px at focus plane)."""
    cx, cy, vw = view
    vh = vw * PH / OW
    k = OW / vw
    out = np.zeros((PH, OW, 3), np.float32)
    for L in plate.layers:
        p = zf / L['z']
        s = 1 + dolly * p
        tx, ty = -truck[0] * p, -truck[1] * p
        # panel -> output affine
        a = k * s
        bx = k * (focus[0] + tx - s * focus[0] - (cx - vw / 2))
        by = k * (focus[1] + ty - s * focus[1] - (cy - vh / 2))
        M = np.float32([[a, 0, bx], [0, a, by]])
        rgb, al = L['rgb'], L['a']
        if warp is not None:
            rgb, al = warp(L, rgb, al)
        r = cv2.warpAffine(rgb, M, (OW, PH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if L['name'] == 'bg':
            out = r
        else:
            aa = cv2.warpAffine(al, M, (OW, PH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            out = out * (1 - aa[..., None]) + r * aa[..., None]
        if extra is not None:
            out = extra(L, out, M)
    return out


def noise_tex(h, w, scale, seed, octaves=4):
    r = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot, s = 1.0, 0.0, scale
    for _ in range(octaves):
        g = r.random((int(h / s) + 3, int(w / s) + 3)).astype(np.float32)
        out += amp * cv2.resize(g, (int(g.shape[1] * s), int(g.shape[0] * s)), interpolation=cv2.INTER_CUBIC)[:h, :w]
        tot += amp
        amp *= 0.5
        s /= 2
        if s < 2:
            break
    out /= tot
    return (out - out.min()) / (np.ptp(out) + 1e-6)


SMOKE = noise_tex(PH * 2, OW * 2, 220, 1, 5)
MIST = noise_tex(PH * 2, OW * 2, 300, 2, 4)


def scroll(tex, ox, oy):
    h, w = tex.shape
    x0, y0 = int(ox) % (w - OW), int(oy) % (h - PH)
    return tex[y0:y0 + PH, x0:x0 + OW]


def smoke(out, t, region, col, amount, speed=(18, -4), tex=None):
    tex = SMOKE if tex is None else tex
    n = scroll(tex, 200 + t * speed[0], 120 + t * speed[1])
    n2 = scroll(tex, 600 - t * speed[0] * 0.6, 300 + t * speed[1] * 0.4)
    a = np.clip((n * 0.6 + n2 * 0.4 - 0.42) * 2.2, 0, 1) * region * amount
    return out * (1 - a[..., None]) + np.asarray(col) * a[..., None]


def fire_mask(img):
    hsv = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hue, s, v = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
    m = ((hue < 28) | (hue > 170)) & (s > 0.45) & (v > 0.62)
    m = m.astype(np.float32) * np.clip((v - 0.55) * 3, 0, 1)
    return cv2.GaussianBlur(m, (0, 0), 1.5)


class Particles:
    def __init__(self, n, box, vel, vjit, size, life, seed, grav=0.0):
        r = np.random.default_rng(seed)
        self.p = np.stack([r.uniform(box[0], box[2], n), r.uniform(box[1], box[3], n)], 1)
        self.v = np.array(vel) + r.normal(0, 1, (n, 2)) * vjit
        self.s = r.uniform(*size, n)
        self.ph = r.uniform(0, 1, n)
        self.life = life
        self.box = box
        self.g = grav

    def pos(self, t):
        u = (self.ph + t / self.life) % 1.0
        age = u * self.life
        p = self.p + self.v * age[:, None] + np.array([0, 0.5 * self.g]) * (age ** 2)[:, None]
        return p, u


def draw_dots(out, pts, sizes, col, alpha, glow=0.0, streak=None):
    layer = np.zeros(out.shape[:2], np.float32)
    for i, (x, y) in enumerate(pts):
        if -10 < x < OW + 10 and -10 < y < PH + 10:
            if streak is not None:
                dx, dy = streak[i]
                cv2.line(layer, (int(x), int(y)), (int(x - dx), int(y - dy)), float(alpha[i]), max(1, int(sizes[i])), cv2.LINE_AA)
            else:
                cv2.circle(layer, (int(x), int(y)), max(1, int(sizes[i])), float(alpha[i]), -1, cv2.LINE_AA)
    if glow > 0:
        layer = layer + cv2.GaussianBlur(layer, (0, 0), 4) * glow
    return out + layer[..., None] * np.asarray(col)


def handheld(t, amp=0.6, f=0.4, seed=0):
    r = np.random.default_rng(seed)
    ph = r.uniform(0, 6.28, 4)
    return (amp * (math.sin(t * f * 6.28 + ph[0]) + 0.5 * math.sin(t * f * 2.3 * 6.28 + ph[1])),
            amp * (math.sin(t * f * 0.8 * 6.28 + ph[2]) + 0.5 * math.sin(t * f * 1.9 * 6.28 + ph[3])))


def flag_warp(rgb, al, mask, pole_x, t, amp=6.0, wl=60.0, speed=7.0, direction=1):
    """Cloth flutter: travelling wave whose amplitude grows away from the pole."""
    h, w = al.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.clip(np.abs(xx - pole_x) / 140.0, 0, 1)
    wave = np.sin((xx - pole_x) * direction / wl * 6.28 - t * speed) * amp * d * mask
    wave2 = np.cos((xx - pole_x) / (wl * 0.6) * 6.28 - t * speed * 1.3) * amp * 0.35 * d * mask
    mx, my = xx + wave2, yy + wave
    rgb2 = cv2.remap(rgb, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    al2 = cv2.remap(al, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    # light catches the folds
    shade = 1 + 0.12 * np.sin((xx - pole_x) * direction / wl * 6.28 - t * speed + 1.2) * d * mask
    return rgb2 * shade[..., None], al2


def cloth_warp(rgb, al, mask, t, amp=2.5, scale=90.0, speed=1.2):
    h, w = al.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = np.sin(yy / scale + t * speed) * amp * mask
    dy = np.sin(xx / (scale * 1.3) + t * speed * 0.8) * amp * 0.5 * mask
    return (cv2.remap(rgb, xx + dx, yy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT),
            cv2.remap(al, xx + dx, yy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT))


def water_warp(rgb, mask, t, flow=(1.0, 0.15), amp=3.0, seed=3):
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = WATER_N
    sx = (xx * 0.5 - t * 60 * flow[0]) % n.shape[1]
    sy = (yy * 0.5 - t * 60 * flow[1]) % n.shape[0]
    nv = cv2.remap(n, sx.astype(np.float32), sy.astype(np.float32), cv2.INTER_LINEAR)
    dx = (nv - 0.5) * amp * 2 * mask
    dy = (nv - 0.5) * amp * mask
    out = cv2.remap(rgb, xx + dx, yy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    spark = np.clip((nv - 0.82) * 6, 0, 1) * mask * 0.25
    return out + spark[..., None]


WATER_N = noise_tex(400, 400, 18, 7, 3)


def finish(pic, f, fade=1.0, grain=0.022):
    """Grain, vignette, letterbox into 1280x720."""
    h, w = pic.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = ((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2
    pic = pic * (1 - 0.28 * np.clip(d - 0.3, 0, 1.4) / 1.4)[..., None]
    g = np.random.default_rng(f).normal(0, grain, (h // 2, w // 2)).astype(np.float32)
    pic = pic + cv2.resize(g, (w, h))[..., None]
    pic = np.clip(pic * fade, 0, 1)
    frame = np.zeros((OH, OW, 3), np.float32)
    y0 = (OH - PH) // 2
    frame[y0:y0 + PH] = pic
    return (frame * 255 + 0.5).astype(np.uint8)


# ================================================================== shots
class S09:
    """Retreat. 40mm, dolly-in on the king, soldiers part around him, the city burns."""
    N = 96

    def __init__(self):
        king = [(650, 100), (700, 28), (765, 95), (770, 170), (790, 250), (870, 300), (905, 420), (940, 600), (985, 843), (370, 843),
                (420, 640), (470, 480), (520, 330), (580, 270), (640, 240), (645, 170)]
        left = [(0, 230), (170, 260), (330, 330), (470, 380), (470, 843), (0, 843)]
        right = [(880, 280), (1280, 300), (1280, 843), (990, 843), (950, 520), (890, 360)]
        self.P = Plate('09.png', [('king', king, 2.0, True), ('left', left, 3.2, True), ('right', right, 3.2, True)], 9.0)
        self.fire = fire_mask(self.P.layer('bg')['rgb'])
        self.cape = poly_mask(self.P.img.shape, [(380, 843), (470, 480), (520, 330), (560, 300), (600, 560), (560, 843)], 20) + \
            poly_mask(self.P.img.shape, [(850, 320), (905, 420), (940, 600), (985, 843), (860, 843), (840, 500)], 20)
        self.embers = Particles(90, (0, 100, OW, PH + 60), (6, -60), 18, (1, 2.4), 3.5, 11)
        self.ash = Particles(70, (0, -40, OW, PH), (-10, 30), 8, (1, 1.8), 4.0, 12)

    def frame(self, f):
        t = f / FPS
        fire = self.fire
        flick = noise_tex  # noqa

        def warp(L, rgb, al):
            if L['name'] == 'bg':
                fl = 1 + 0.35 * np.sin(t * 9 + self.fire * 6) * np.sin(t * 13.7 + 2.0)
                rgb = rgb * (1 + fire[..., None] * (fl[..., None] - 1) * 0.6) + cv2.GaussianBlur(fire, (0, 0), 12)[..., None] * np.array([0.1, 0.35, 0.8]) * 0.45 * fl[..., None]
            if L['name'] == 'king':
                rgb, al = cloth_warp(rgb, al, self.cape, t, amp=2.2, scale=70, speed=1.5)
            return rgb, al

        def extra(L, out, M):
            if L['name'] == 'bg':   # smoke between the city and the soldiers
                reg = np.clip(1.2 - np.linspace(0, 1, PH)[:, None] * 1.4, 0, 1) * np.ones((1, OW))
                out = smoke(out, t, reg, (0.42, 0.42, 0.45), 0.75, speed=(-22, -5))
            return out
        hx, hy = handheld(t, 0.8, 0.35, 1)
        pic = render_plate(self.P, (640 + hx, 300 + hy, 1180), (705, 230), 2.0, dolly=0.12 * ease(t, 0, 4.0), warp=warp, extra=extra)
        p, u = self.embers.pos(t)
        p[:, 0] += np.sin(t * 2 + self.embers.ph * 9) * 12
        pic = draw_dots(pic, p, self.embers.s, (0.25, 0.6, 1.0), (1 - u) * 0.9, glow=1.5)
        p, u = self.ash.pos(t)
        pic = draw_dots(pic, p, self.ash.s, (0.75, 0.75, 0.75), 0.35 * np.sin(np.pi * u))
        return finish(pic, f, fade=ease(t, 0, 0.5) ** 1.2)


class S10:
    """Decision. 85mm close-up, shallow focus, the fire behind slides the other way."""
    N = 72

    def __init__(self):
        king = [(510, 0), (975, 0), (960, 240), (940, 420), (900, 560), (1000, 700), (1110, 843), (0, 843), (0, 620), (150, 560),
                (330, 560), (470, 520), (460, 360), (490, 240)]
        self.P = Plate('10.png', [('king', king, 1.0, True)], 10.0)
        bg = self.P.layer('bg')
        bg['rgb'] = cv2.GaussianBlur(bg['rgb'], (0, 0), 4)
        self.fire = fire_mask(self.P.img) * (1 - self.P.layer('king')['a'])
        self.fire = cv2.GaussianBlur(self.fire, (0, 0), 3)
        self.face = poly_mask(self.P.img.shape, [(470, 300), (930, 300), (900, 680), (480, 680)], 40)
        self.bokeh = Particles(26, (0, 0, OW, PH + 60), (14, -45), 10, (3, 9), 3.0, 21)

    def frame(self, f):
        t = f / FPS

        def warp(L, rgb, al):
            if L['name'] == 'bg':
                fl = 1 + 0.4 * np.sin(t * 8 + self.fire * 5) * np.sin(t * 11.3 + 1)
                rgb = rgb + cv2.GaussianBlur(self.fire, (0, 0), 10)[..., None] * np.array([0.1, 0.35, 0.85]) * 0.35 * fl[..., None]
            else:  # warm, flickering bounce of the fire on the face
                fl = 0.5 + 0.5 * math.sin(t * 7.3) * math.sin(t * 3.1 + 1)
                rgb = rgb * (1 + self.face[..., None] * np.array([0.0, 0.03, 0.08]) * fl)
            return rgb, al
        hx, hy = handheld(t, 0.5, 0.3, 2)
        pic = render_plate(self.P, (700 + hx, 272 + hy, 1250), (720, 400), 1.0, dolly=0.06 * ease(t, 0, 3), truck=(-30 * t / 3, 0), warp=warp)
        p, u = self.bokeh.pos(t)
        lay = np.zeros((PH, OW), np.float32)
        for (x, y), s, uu in zip(p, self.bokeh.s, u):
            cv2.circle(lay, (int(x), int(y)), int(s), float(np.sin(np.pi * uu) * 0.5), -1, cv2.LINE_AA)
        lay = cv2.GaussianBlur(lay, (0, 0), 3)
        pic = pic + lay[..., None] * np.array([0.3, 0.65, 1.0])
        return finish(pic, 1000 + f)


class S11:
    """The river. 24mm extreme wide, lateral truck, river fastest, volleys of arrows left -> right."""
    N = 108

    def __init__(self):
        river = [(0, 520), (260, 500), (620, 470), (820, 460), (840, 560), (1000, 700), (1100, 843), (0, 843)]
        legion = [(820, 470), (900, 400), (1000, 330), (1280, 230), (1280, 843), (1110, 843), (1000, 700), (840, 560)]
        bank = [(0, 185), (560, 225), (860, 330), (850, 460), (560, 480), (0, 525)]
        fg = [(0, 650), (200, 665), (470, 780), (520, 843), (0, 843)]
        self.P = Plate('11.png', [('fg', fg, 1.0, False), ('river', river, 1.6, False), ('legion', legion, 2.2, True), ('bank', bank, 3.5, False)], 20.0)
        self.water = poly_mask(self.P.img.shape, river, 6)
        self.flags = [(poly_mask(self.P.img.shape, [(1088, 305), (1142, 308), (1142, 378), (1088, 375)], 2), 1088),
                      (poly_mask(self.P.img.shape, [(1240, 262), (1280, 262), (1280, 372), (1240, 372)], 2), 1240),
                      (poly_mask(self.P.img.shape, [(1045, 328), (1062, 328), (1062, 366), (1045, 366)], 1), 1045)]
        r = np.random.default_rng(5)
        self.volleys = []
        for v0 in (0.6, 2.4):
            for k in range(26):
                sx, sy = r.uniform(30, 560), r.uniform(200, 300)
                ex, ey = r.uniform(850, 1280), r.uniform(330, 480)
                self.volleys.append((v0 + r.uniform(0, 0.35), sx, sy, ex, ey, r.uniform(0.9, 1.3)))

    def frame(self, f):
        t = f / FPS

        def warp(L, rgb, al):
            if L['name'] == 'river':
                rgb = water_warp(rgb, self.water, t, flow=(1.0, 0.25), amp=3.5)
            if L['name'] == 'legion':
                for m, px in self.flags:
                    rgb, al = flag_warp(rgb, al, m, px, t, amp=3.0, wl=40, speed=8)
            return rgb, al

        def extra(L, out, M):
            if L['name'] == 'bank':
                out = smoke(out, t, np.clip(1 - np.abs(np.linspace(-1, 1, PH)[:, None] + 0.1) * 1.5, 0, 1) * np.ones((1, OW)), (0.78, 0.78, 0.8), 0.35, speed=(25, 0), tex=MIST)
            if L['name'] == 'legion':  # arrows in panel space -> mapped through this layer's affine
                lay = np.zeros((PH, OW), np.float32)
                for (t0, sx, sy, ex, ey, dur) in self.volleys:
                    u = (t - t0) / dur
                    if 0 < u < 1:
                        x = sx + (ex - sx) * u
                        y = sy + (ey - sy) * u - 260 * math.sin(math.pi * u)
                        u2 = max(0, u - 0.03)
                        x2 = sx + (ex - sx) * u2
                        y2 = sy + (ey - sy) * u2 - 260 * math.sin(math.pi * u2)
                        a = np.array([[x, y, 1], [x2, y2, 1]]) @ M.T
                        cv2.line(lay, tuple(np.int32(a[0])), tuple(np.int32(a[1])), 0.8, 1, cv2.LINE_AA)
                out = out * (1 - lay[..., None] * 0.85) + lay[..., None] * 0.08
            return out
        truck = (60 * ease(t, 0, 4.5) - 30, -12 * ease(t, 0, 4.5))
        pic = render_plate(self.P, (640, 430, 1240), (640, 520), 1.6, dolly=0.03 * ease(t, 0, 4.5), truck=truck, warp=warp, extra=extra)
        return finish(pic, 2000 + f)


class S13:
    """Into the river. 100mm macro at water level, fast push, impact, mud and water fly."""
    N = 48

    def __init__(self):
        boot = [(380, 0), (640, 0), (660, 250), (760, 450), (780, 560), (720, 660), (480, 660), (470, 560), (440, 350), (370, 140)]
        self.P = Plate('13.png', [('boot', boot, 1.0, True)], 3.0)
        self.water = poly_mask(self.P.img.shape, [(0, 300), (1280, 300), (1280, 843), (0, 843)], 30) * (1 - self.P.layer('boot')['a'])
        r = np.random.default_rng(13)
        n = 160
        self.drops = dict(p0=np.stack([r.uniform(470, 780, n), r.uniform(560, 660, n)], 1), v=np.stack([r.normal(0, 260, n), -r.uniform(150, 520, n)], 1),
                          s=r.uniform(1.5, 5, n), mud=r.random(n) < 0.55)

    def frame(self, f):
        t = f / FPS
        hit = 0.45

        def warp(L, rgb, al):
            if L['name'] == 'bg':
                rgb = water_warp(rgb, self.water, t, flow=(0.6, 0.1), amp=4.0)
                if t > hit:   # rings spreading from the boot
                    h, w = al.shape
                    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
                    d = np.sqrt(((xx - 620) / 1.0) ** 2 + ((yy - 640) / 0.35) ** 2)
                    R = (t - hit) * 520
                    ring = np.exp(-((d - R) / 18) ** 2) * math.exp(-(t - hit) * 2.5) * self.water
                    rgb = cv2.remap(rgb, xx, yy + ring * 6, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT) + ring[..., None] * 0.08
            return rgb, al
        shake = (0, 0)
        if hit < t < hit + 0.25:
            r = np.random.default_rng(f)
            shake = tuple(r.normal(0, 6 * (1 - (t - hit) / 0.25), 2))
        z = 0.18 * ease(t, 0, 2.0)
        pic = render_plate(self.P, (640 + shake[0], 470 + shake[1], 1230), (600, 520), 1.0, dolly=z, warp=warp)
        if t > hit - 0.04:
            D = self.drops
            age = t - hit + 0.04
            vw = 1230
            k = OW / vw
            p = D['p0'] + D['v'] * age + np.array([0, 0.5 * 1400]) * age * age
            # panel -> picture (approximate the camera)
            s = 1 + z
            pp = (600 + s * (p - [600, 520]) - [640 + shake[0] - vw / 2, 470 + shake[1] - vw * PH / OW / 2]) * k
            alive = p[:, 1] < 760
            lay_m = np.zeros((PH, OW), np.float32)
            lay_w = np.zeros((PH, OW), np.float32)
            for (x, y), sz, mud, al, v in zip(pp, D['s'], D['mud'], alive, D['v']):
                if not al:
                    continue
                target = lay_m if mud else lay_w
                cv2.line(target, (int(x), int(y)), (int(x - v[0] * 0.012), int(y - v[1] * 0.012 + age * 12)), 1.0, max(1, int(sz)), cv2.LINE_AA)
            pic = pic * (1 - lay_m[..., None] * 0.9) + lay_m[..., None] * np.array([0.12, 0.18, 0.24])
            pic = pic + lay_w[..., None] * 0.35
        return finish(pic, 3000 + f)


class S12:
    """The archer. 65mm, slow push while he draws, release: the arrow leaves, shake, whip right."""
    N = 60

    def __init__(self):
        rider = [(130, 700), (150, 560), (240, 420), (380, 380), (450, 350), (460, 180), (560, 60), (720, 45), (800, 0), (985, 0), (1000, 200),
                 (1075, 165), (1075, 205), (1000, 235), (950, 290), (1060, 450), (1110, 560), (1280, 640), (1280, 843), (380, 843), (300, 780), (200, 800)]
        self.P = Plate('12.png', [('rider', rider, 1.0, True)], 6.0)
        L = self.P.layer('rider')
        self.arrow = np.zeros(L['a'].shape, np.float32)
        cv2.line(self.arrow, (735, 189), (1068, 175), 1.0, 7, cv2.LINE_AA)
        self.noarrow = inpaint(L['rgb'], self.arrow)
        self.mane = poly_mask(self.P.img.shape, [(250, 420), (450, 400), (640, 470), (660, 640), (480, 560), (330, 470)], 18)
        self.cloak = poly_mask(self.P.img.shape, [(800, 300), (1060, 400), (1060, 500), (900, 470)], 18)

    def frame(self, f):
        t = f / FPS
        rel = 1.25

        def warp(L, rgb, al):
            if L['name'] == 'rider':
                if t >= rel:
                    rgb = self.noarrow
                    k = math.exp(-(t - rel) * 8)
                    rgb, al = cloth_warp(rgb, al, self.mane + self.cloak, t, amp=2.5 + 3 * k, scale=40, speed=6)
                else:
                    rgb, al = cloth_warp(rgb, al, self.mane + self.cloak, t, amp=2.0, scale=40, speed=4)
            return rgb, al
        shake = (0.0, 0.0)
        whip = 0.0
        if t >= rel:
            r = np.random.default_rng(f)
            k = math.exp(-(t - rel) * 7)
            shake = tuple(r.normal(0, 4 * k, 2))
            whip = 90 * ease(t, rel + 0.05, rel + 0.7)
        hx, hy = handheld(t, 0.6, 0.5, 3)
        pic = render_plate(self.P, (640 + hx + shake[0] + whip, 300 + hy + shake[1], 1260), (760, 300), 1.0, dolly=0.07 * ease(t, 0, rel), truck=(0, 0), warp=warp)
        if t >= rel:   # the arrow streaks away
            u = (t - rel) * 3200
            vw = 1260
            k = OW / vw
            ax0 = (1068 + u - (640 + whip - vw / 2)) * k
            ay0 = (175 - u * 0.03 - (300 - vw * PH / OW / 2)) * k
            lay = np.zeros((PH, OW), np.float32)
            cv2.line(lay, (int(ax0), int(ay0)), (int(ax0 - 260), int(ay0 + 9)), 1.0, 2, cv2.LINE_AA)
            lay = cv2.GaussianBlur(lay, (0, 0), 1.0)
            pic = pic * (1 - lay[..., None] * 0.7) + lay[..., None] * 0.1
        return finish(pic, 4000 + f)


class S15:
    """The hand. 100mm, rack focus cloak -> hand, a heartbeat of light."""
    N = 48

    def __init__(self):
        hand = [(550, 170), (800, 150), (870, 250), (860, 400), (900, 450), (960, 560), (970, 700), (900, 760), (820, 700), (700, 560), (650, 420), (560, 330)]
        self.P = Plate('15.png', [('hand', hand, 1.0, True)], 1.6)
        self.blur_hand = cv2.GaussianBlur(self.P.layer('hand')['rgb'], (0, 0), 5)
        self.sharp_bg = self.P.layer('bg')['rgb']
        self.blur_bg = cv2.GaussianBlur(self.sharp_bg, (0, 0), 5)

    def frame(self, f):
        t = f / FPS
        rf = ease(t, 0.2, 1.1)
        hand = self.P.layer('hand')
        bg = self.P.layer('bg')
        hand_rgb = self.blur_hand * (1 - rf) + hand['img_sharp'] * rf if 'img_sharp' in hand else None
        if hand_rgb is None:
            hand['img_sharp'] = hand['rgb'].copy()
            hand_rgb = self.blur_hand * (1 - rf) + hand['img_sharp'] * rf
        beat = math.exp(-((t - 1.15) / 0.06) ** 2) + 0.6 * math.exp(-((t - 1.5) / 0.06) ** 2)

        def warp(L, rgb, al):
            if L['name'] == 'hand':
                return hand_rgb * (1 + 0.06 * beat), al
            return self.sharp_bg * (1 - rf) + self.blur_bg * rf, al
        pic = render_plate(self.P, (700, 440, 1150), (760, 450), 1.0, dolly=0.03 * ease(t, 0, 2), warp=warp)
        return finish(pic, 5000 + f)


class S14:
    """The signal. 35mm low angle, tilt up + push, banners whip, cloak moves, horn."""
    N = 72

    def __init__(self):
        king = [(0, 520), (60, 470), (200, 440), (220, 340), (225, 215), (300, 140), (380, 100), (450, 220), (460, 320), (470, 420), (560, 420), (700, 400),
                (840, 290), (900, 150), (930, 108), (975, 185), (890, 330), (880, 350), (780, 470), (770, 843), (0, 843)]
        army = [(0, 360), (1280, 360), (1280, 720), (0, 720)]
        self.P = Plate('14.png', [('king', king, 1.2, True), ('army', army, 4.0, False)], 15.0)
        self.flagR = poly_mask(self.P.img.shape, [(992, 150), (1142, 150), (1150, 300), (1180, 420), (1000, 335)], 2)
        self.flagM = poly_mask(self.P.img.shape, [(668, 233), (737, 233), (730, 332), (668, 332)], 2)
        self.cape = poly_mask(self.P.img.shape, [(0, 470), (200, 450), (420, 460), (560, 430), (700, 420), (760, 600), (770, 843), (0, 843)], 30) * \
            (1 - poly_mask(self.P.img.shape, [(170, 560), (500, 560), (500, 843), (170, 843)], 30))

    def frame(self, f):
        t = f / FPS

        def warp(L, rgb, al):
            if L['name'] == 'army' or L['name'] == 'bg':
                rgb, al = flag_warp(rgb, al, self.flagR, 995, t, amp=7, wl=70, speed=9)
                rgb, al = flag_warp(rgb, al, self.flagM, 668, t + 0.3, amp=4, wl=40, speed=9)
            if L['name'] == 'king':
                rgb, al = cloth_warp(rgb, al, self.cape, t, amp=3.0, scale=60, speed=2.2)
            return rgb, al

        def extra(L, out, M):
            if L['name'] == 'bg':   # clouds race
                out = smoke(out, t, np.clip(1 - np.linspace(0, 1, PH)[:, None] * 1.6, 0, 1) * np.ones((1, OW)), (0.82, 0.83, 0.86), 0.35, speed=(40, 0), tex=MIST)
            return out
        hx, hy = handheld(t, 0.5, 0.35, 4)
        cy = 470 - 110 * ease(t, 0, 2.6)
        pic = render_plate(self.P, (620 + hx, cy + hy, 1220), (560, 380), 1.2, dolly=0.08 * ease(t, 0, 3), warp=warp, extra=extra)
        return finish(pic, 6000 + f)


class S16:
    """The counter-attack. Tracking with the standard-bearer, background streaks, gallop bob, spray."""
    N = 108

    def __init__(self):
        rider = [(250, 620), (330, 520), (440, 500), (470, 420), (430, 360), (540, 300), (570, 278), (610, 282), (680, 320), (690, 240), (722, 25),
                 (742, 18), (735, 62), (705, 320), (742, 380), (802, 470), (792, 505), (752, 520), (762, 705), (702, 725), (642, 645), (562, 705),
                 (472, 705), (402, 645), (352, 755), (330, 625)]
        banner = [(415, 115), (722, 58), (705, 245), (500, 272), (470, 250)]
        ground = [(0, 752), (1280, 752), (1280, 843), (0, 843)]
        self.P = Plate('16.png', [('rider', rider, 1.0, True), ('ground', ground, 0.9, False)], 6.0)
        G = self.P.layer('ground')
        G['a'] = poly_mask(self.P.img.shape, ground, 8)
        G['rgb'] = cv2.blur(self.P.img, (41, 1))
        L = self.P.layer('rider')
        bm = poly_mask(self.P.img.shape, banner, 2)
        L['a'] = np.maximum(L['a'], bm)
        L['rgb'] = L['rgb'] * (1 - bm[..., None]) + self.P.img * bm[..., None]
        self.banner = bm
        bg = self.P.layer('bg')
        self.bg_sharp = bg['rgb']
        self.bg_blur = cv2.blur(bg['rgb'], (31, 3))
        r = np.random.default_rng(16)
        n = 220
        self.spray = dict(x0=r.uniform(0, OW, n), y0=r.uniform(PH * 0.72, PH * 0.98, n), v=np.stack([-r.uniform(150, 500, n), -r.uniform(60, 260, n)], 1),
                          s=r.uniform(1, 4, n), ph=r.uniform(0, 1, n), mud=r.random(n) < 0.6)

    def frame(self, f):
        t = f / FPS
        bob = math.sin(t / 0.42 * 2 * math.pi)
        lift = -6 * max(0, bob) + 3 * min(0, bob)

        def warp(L, rgb, al):
            if L['name'] == 'bg':
                M = np.float32([[1, 0, -28 * t], [0, 1, 0]])
                return cv2.warpAffine(self.bg_blur, M, (al.shape[1], al.shape[0]), borderMode=cv2.BORDER_REFLECT), al
            if L['name'] == 'ground':
                M = np.float32([[1, 0, -330 * t], [0, 1, 0]])
                return (cv2.warpAffine(rgb, M, (al.shape[1], al.shape[0]), borderMode=cv2.BORDER_WRAP),
                        cv2.warpAffine(al, M, (al.shape[1], al.shape[0]), borderMode=cv2.BORDER_WRAP))
            if L['name'] == 'rider':
                rgb, al = flag_warp(rgb, al, self.banner, 715, t, amp=8, wl=80, speed=11, direction=-1)
                M = np.float32([[1, 0, 0], [0, 1, lift]])
                rgb = cv2.warpAffine(rgb, M, (rgb.shape[1], rgb.shape[0]), borderMode=cv2.BORDER_REFLECT)
                al = cv2.warpAffine(al, M, (al.shape[1], al.shape[0]))
            return rgb, al

        def extra(L, out, M):
            if L['name'] == 'bg':
                out = smoke(out, t * 3, np.clip(np.linspace(-0.4, 1.0, PH)[:, None], 0, 1) * np.ones((1, OW)), (0.85, 0.86, 0.88), 0.45, speed=(-120, 0), tex=MIST)
            return out
        r = np.random.default_rng(f // 2)
        sh = r.normal(0, 2.2, 2)
        truck = (0, 0)
        pic = render_plate(self.P, (640 + sh[0], 430 + sh[1], 1240), (600, 450), 1.0, dolly=0.04 * ease(t, 0, 4.5), truck=truck, warp=warp, extra=extra)
        S = self.spray
        u = (S['ph'] + t / 0.9) % 1.0
        age = u * 0.9
        x = (S['x0'] - t * 300) % (OW + 200) - 100 + S['v'][:, 0] * age
        y = S['y0'] + S['v'][:, 1] * age + 0.5 * 900 * age * age
        lay_m = np.zeros((PH, OW), np.float32)
        lay_w = np.zeros((PH, OW), np.float32)
        for xi, yi, si, mud, vv, uu in zip(x, y, S['s'], S['mud'], S['v'], u):
            tg = lay_m if mud else lay_w
            cv2.line(tg, (int(xi), int(yi)), (int(xi - vv[0] * 0.02), int(yi - vv[1] * 0.02)), float(1 - uu), max(1, int(si)), cv2.LINE_AA)
        pic = pic * (1 - lay_m[..., None] * 0.85) + lay_m[..., None] * np.array([0.14, 0.2, 0.25])
        pic = pic + lay_w[..., None] * 0.3
        k = 1.0 if t < 4.45 else 0.0          # hard cut to black on the peak
        return finish(pic, 7000 + f, fade=k)


EDIT = [S09, S10, S11, S13, S12, S15, S14, S16]
TAIL_BLACK = 24


def render_all():
    os.makedirs(FR, exist_ok=True)
    idx = 0
    starts = []
    for S in EDIT:
        sh = S()
        starts.append((S.__name__, idx / FPS))
        for f in range(S.N):
            cv2.imwrite(f'{FR}/{idx:05d}.png', sh.frame(f))
            idx += 1
        print(S.__name__, 'done', idx, flush=True)
    blk = np.zeros((OH, OW, 3), np.uint8)
    for _ in range(TAIL_BLACK):
        cv2.imwrite(f'{FR}/{idx:05d}.png', blk)
        idx += 1
    return starts, idx


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'one':
        S = {c.__name__: c for c in EDIT}[sys.argv[2]]
        sh = S()
        os.makedirs(FR, exist_ok=True)
        for f in map(int, sys.argv[3].split(',')):
            cv2.imwrite(f'{FR}/{S.__name__}_{f:03d}.png', sh.frame(f))
    else:
        starts, n = render_all()
        print(starts, n)
