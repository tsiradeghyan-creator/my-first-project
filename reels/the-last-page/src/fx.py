"""Shared painted sets and effects: library shelves, lectern book, dust, light shafts, lantern,
paper birds, pages, pampas grass, post-processing."""
import math
import numpy as np
import cv2
import skia
from core import *

BOOK_COLS = ['#7a3b34', '#5b2f2b', '#3e4f45', '#2f4057', '#6b5a3a', '#8a6b3f', '#4b3a52', '#5f6b4a',
             '#9a7b55', '#3a3530', '#6e2f2a', '#2c3a3a', '#8c5a3c', '#544a3c', '#41485e', '#7b6d58']


def shelves_base(w, h, rng, shelf_h=58, x0=0, top_dark=0.75, moss=0.18, wood='#3b2a22', back='#1b1820',
                 tint=(1, 1, 1), perspective=None):
    """Base image (float RGB) for a wall of shelves holding thousands of unique books.
    Returns rgb and a 'book mask' (where books are)."""
    img = np.zeros((h, w, 3), np.float32) + hexc(back)[:3]
    s = surface(w, h)
    c = s.getCanvas()
    c.drawImage(np_to_image((img * 255).astype(np.uint8)), 0, 0)
    bm = surface(w, h)
    cb = bm.getCanvas()
    cb.clear(skia.ColorBLACK)
    upr_w = 14
    bay = 230
    y = h - 30
    rowi = 0
    while y > -shelf_h:
        top = y - shelf_h
        x = -rng.uniform(0, 40)
        while x < w:
            if (x % bay) < upr_w:
                x += upr_w
                continue
            bw = rng.uniform(5, 15) * (1.6 if rng.random() < 0.07 else 1.0)
            bh = shelf_h * rng.uniform(0.62, 0.94)
            gap = rng.random() < 0.035
            if gap:
                x += rng.uniform(6, 22)
                continue
            lean = 0.0
            if rng.random() < 0.08:
                lean = rng.uniform(-0.35, 0.35)
            col = hexc(BOOK_COLS[rng.integers(len(BOOK_COLS))])[:3] * rng.uniform(0.7, 1.15)
            # sun-faded tops and spines
            fade = rng.random() < 0.25
            c.save()
            c.translate(x + bw / 2, y)
            c.rotate(math.degrees(lean))
            sag = rng.uniform(0, 1.5)
            pts = [(-bw / 2, 0), (-bw / 2 + sag, -bh), (bw / 2 + sag, -bh - rng.uniform(-1, 1)), (bw / 2, 0)]
            c.drawPath(poly_path(pts, True, False), paint_(col))
            if fade:
                c.drawRect(skia.Rect(-bw / 2 + sag, -bh, bw / 2 + sag, -bh * rng.uniform(0.55, 0.8)), paint_(col * 0.5 + 0.35, 0.55))
            # bands and a label: every spine is its own design
            nb = rng.integers(0, 4)
            for k in range(nb):
                by_ = -bh * rng.uniform(0.1, 0.9)
                c.drawRect(skia.Rect(-bw / 2, by_, bw / 2, by_ + rng.uniform(0.8, 2.2)), paint_(hexc('#b79a5b')[:3] * rng.uniform(0.6, 1.0), 0.85))
            if rng.random() < 0.4 and bw > 7:
                ly = -bh * rng.uniform(0.45, 0.7)
                c.drawRect(skia.Rect(-bw / 2 + 1.5, ly, bw / 2 - 1.5, ly + rng.uniform(5, 10)), paint_(hexc('#d8c8a0')[:3] * rng.uniform(0.5, 0.9), 0.8))
            # cool edge on one side (light comes from the right window)
            c.drawRect(skia.Rect(bw / 2 - max(1.2, bw * 0.18), -bh, bw / 2, 0), paint_(col * 1.25 + 0.04, 0.7))
            c.drawRect(skia.Rect(-bw / 2, -bh, -bw / 2 + max(1.0, bw * 0.2), 0), paint_(col * 0.55, 0.8))
            c.restore()
            cb.save()
            cb.translate(x + bw / 2, y)
            cb.rotate(math.degrees(lean))
            cb.drawRect(skia.Rect(-bw / 2, -bh, bw / 2, 0), paint_((1, 1, 1)))
            cb.restore()
            # moss creeping along some spines
            if rng.random() < moss and rowi < 4:
                for _ in range(rng.integers(4, 14)):
                    mx = x + rng.uniform(0, bw)
                    my = y - rng.uniform(0, bh * 0.5)
                    c.drawCircle(mx, my, rng.uniform(1, 2.6), paint_(hexc('#4f6a3a')[:3] * rng.uniform(0.6, 1.2), 0.85))
            x += bw + (rng.uniform(0, 1.5) if rng.random() < 0.3 else 0)
        # shelf plank
        c.drawRect(skia.Rect(0, y, w, y + 9), paint_(hexc(wood)[:3] * 1.25))
        c.drawRect(skia.Rect(0, y + 7, w, y + 11), paint_(hexc(wood)[:3] * 0.6))
        y = top - 11
        rowi += 1
    # uprights
    for bx in np.arange(0, w + bay, bay):
        c.drawRect(skia.Rect(bx, 0, bx + upr_w, h), paint_(hexc(wood)[:3]))
        c.drawRect(skia.Rect(bx + upr_w - 3, 0, bx + upr_w, h), paint_(hexc(wood)[:3] * 1.4))
    out = surf_to_np(s)[:, :, :3].astype(np.float32) / 255
    mask = surf_to_np(bm)[:, :, 0].astype(np.float32) / 255
    # climb into darkness
    yy = np.linspace(0, 1, h)[:, None, None]
    dark = np.clip(1 - (1 - yy) * top_dark * 1.25, 0.08, 1)
    out = out * dark * np.asarray(tint)
    return out, mask


def moon_shaft(h, w, x_top, x_bot, width_top, width_bot, color, strength=0.5, soft=18):
    """Light shaft mask (float), additive."""
    pts = [(x_top - width_top / 2, -10), (x_top + width_top / 2, -10), (x_bot + width_bot / 2, h + 10), (x_bot - width_bot / 2, h + 10)]
    m = poly_mask(h, w, pts, feather=soft, smooth=False)
    yy = np.linspace(0, 1, h)[:, None]
    m *= (0.55 + 0.45 * yy)
    return m[..., None] * np.asarray(color[:3]) * strength


class Dust:
    """Drifting dust motes; drawn on twos with slight sparkle."""

    def __init__(self, rng, n, box, vel=(4, -2), size=(0.6, 1.8)):
        self.p = np.stack([rng.uniform(box[0], box[2], n), rng.uniform(box[1], box[3], n)], 1)
        self.v = rng.normal(0, 1, (n, 2)) * 3 + np.array(vel)
        self.r = rng.uniform(*size, n)
        self.ph = rng.uniform(0, 6.28, n)
        self.box = box

    def draw(self, c, t, color, mask_fn=None, alpha=0.8):
        bx = self.box
        pos = self.p + self.v * t + np.stack([np.sin(t * 0.7 + self.ph) * 6, np.cos(t * 0.5 + self.ph) * 4], 1)
        pos[:, 0] = bx[0] + (pos[:, 0] - bx[0]) % (bx[2] - bx[0])
        pos[:, 1] = bx[1] + (pos[:, 1] - bx[1]) % (bx[3] - bx[1])
        for (x, y), r, ph in zip(pos, self.r, self.ph):
            k = mask_fn(x, y) if mask_fn else 1.0
            if k <= 0.02:
                continue
            a = alpha * k * (0.6 + 0.4 * math.sin(t * 3 + ph * 3))
            c.drawCircle(float(x), float(y), float(r * 2.2), paint_(color, a * 0.25, blur=1.5))
            c.drawCircle(float(x), float(y), float(r), paint_(color, a))


def glow(arr_rgb, cx, cy, r, color, strength):
    h, w = arr_rgb.shape[:2]
    x0, x1 = int(max(0, cx - 3 * r)), int(min(w, cx + 3 * r))
    y0, y1 = int(max(0, cy - 3 * r)), int(min(h, cy + 3 * r))
    if x1 <= x0 or y1 <= y0:
        return arr_rgb
    yy, xx = np.mgrid[y0:y1, x0:x1]
    d2 = ((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r)
    g = np.exp(-d2)[..., None] * strength
    arr_rgb[y0:y1, x0:x1] += g * np.asarray(color[:3])
    return arr_rgb


def draw_lantern(c, x, y, s, swing, flame_lean, t, seed, pal_line='#2a160e', lit=1.0):
    """Small paper lantern hanging from a short handle. (x,y) = top of handle."""
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(swing))
    c.scale(s, s)
    ink = paint_(hexc(pal_line), stroke=True, width=1.3)
    c.drawPath(poly_path([(0, 0), (0, 6)], False, False), ink)
    body = []
    for i in range(16):
        a = 2 * math.pi * i / 16
        body.append((math.cos(a) * 10 * (1 + 0.04 * math.sin(i * 1.7 + seed)), 17 + math.sin(a) * 11))
    path = poly_path(body)
    c.drawPath(path, paint_(mix(hexc('#c7643a'), hexc('#ffd28a'), lit)))
    c.save()
    c.clipPath(path, doAntiAlias=True)
    c.drawCircle(-3, 15, 7, paint_(hexc('#fff0c0'), 0.7 * lit, blur=4))
    for k in (-6, 0, 6):
        c.drawPath(poly_path([(k * 1.0, 6), (k * 1.25, 17), (k * 1.0, 28)], False), paint_(hexc('#a84a2a'), 0.6, stroke=True, width=0.8))
    c.restore()
    c.drawRect(skia.Rect(-5, 4.5, 5, 7.5), paint_(hexc('#3a2420')))
    c.drawRect(skia.Rect(-4, 27.5, 4, 30), paint_(hexc('#3a2420')))
    c.drawPath(path, paint_(hexc(pal_line), stroke=True, width=1.2))
    c.restore()


def draw_flame(c, x, y, s, lean, t):
    """Lantern flame (seen when the lantern sits on the floor, shot 5)."""
    fl = 1 + 0.08 * math.sin(t * 23) + 0.05 * math.sin(t * 37)
    pts = []
    for i in range(14):
        a = math.pi * 2 * i / 14
        r = 1.0 if math.sin(a) > 0 else 0.6
        px = math.cos(a) * 5 * r
        py = math.sin(a) * 6
        if py < 0:
            py *= 3.2 * fl
            px += lean * (-py) * 0.5
        pts.append((x + px * s, y + py * s))
    c.drawPath(poly_path(pts), paint_(hexc('#ffb347'), 0.95))
    inner = [(x + (px - x) * 0.55, y + (py - y) * 0.55 + 2 * s) for px, py in pts]
    c.drawPath(poly_path(inner), paint_(hexc('#fff3c4')))


# ---------------------------------------------------------------- paper birds
def paper_bird_shape(phase, size, tw, var):
    """Origami-ish paper bird drawn in 2D: body, two wings whose fold changes with the flap.
    phase 0..1 flap cycle; tw: heading angle; var: per-bird variation dict.
    Returns list of (polygon, tone) with tone 0..1 (1 = lit paper)."""
    up = math.cos(phase * 2 * math.pi)  # +1 wings up, -1 wings down
    L = size
    body = np.array([[-0.55, 0.0], [-0.1, -0.07], [0.6, -0.02], [0.75, 0.02], [0.1, 0.09]]) * L
    span = 0.95 * var.get('span', 1.0)
    wing_y = -up * 0.75 * span
    near = np.array([[-0.25, 0.0], [0.25, 0.0], [0.05 + var.get('sweep', 0.0), wing_y], [-0.35, wing_y * 0.85]]) * L
    far = np.array([[-0.2, 0.0], [0.2, -0.01], [0.1, wing_y * 0.7], [-0.25, wing_y * 0.62]]) * L
    tail = np.array([[-0.5, 0.0], [-0.85, -0.12], [-0.8, 0.08]]) * L
    R = np.array([[math.cos(tw), -math.sin(tw)], [math.sin(tw), math.cos(tw)]])
    out = []
    for poly, tone in ((far, 0.55 + 0.2 * up), (tail, 0.7), (body, 0.85), (near, 0.75 - 0.25 * up)):
        out.append((poly @ R.T, float(np.clip(tone, 0.25, 1.0))))
    return out


def draw_paper_bird(c, x, y, phase, size, heading, var, light_col, shade_col, line_col, alpha=1.0, lw=0.9):
    for poly, tone in paper_bird_shape(phase, size, heading, var):
        q = poly + np.array([x, y])
        col = mix(shade_col, light_col, tone)
        path = poly_path(q, True, False)
        c.drawPath(path, paint_(col, alpha))
        if size > 7:
            c.drawPath(path, paint_(line_col, alpha * 0.9, stroke=True, width=lw))
    if size > 14 and var.get('ink', 0) > 0.5:
        # faded handwriting on the near wing
        q = paper_bird_shape(phase, size, heading, var)[-1][0] + np.array([x, y])
        for k in range(3):
            a = q[0] * (1 - (k + 1) / 4) + q[3] * ((k + 1) / 4)
            b = q[1] * (1 - (k + 1) / 4) + q[2] * ((k + 1) / 4)
            c.drawPath(poly_path([a, a * 0.5 + b * 0.5 + [0, 0.6], b], False), paint_(line_col, alpha * 0.35, stroke=True, width=0.6))


def draw_page(c, x, y, w_, h_, rot_, curl, col, line_col, alpha=1.0, writing=True, seed=0):
    """A loose book page with a curled corner and faded lines of writing."""
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot_))
    pts = [(-w_ / 2, -h_ / 2), (w_ / 2 - curl * w_ * 0.3, -h_ / 2), (w_ / 2, -h_ / 2 + curl * h_ * 0.25), (w_ / 2, h_ / 2), (-w_ / 2, h_ / 2)]
    path = poly_path(pts, True, False)
    c.drawPath(path, paint_(col, alpha))
    if curl > 0.05:
        c.drawPath(poly_path([(w_ / 2 - curl * w_ * 0.3, -h_ / 2), (w_ / 2, -h_ / 2 + curl * h_ * 0.25), (w_ / 2 - curl * w_ * 0.28, -h_ / 2 + curl * h_ * 0.22)], True, False), paint_(np.asarray(col) * 0.8, alpha))
    if writing and w_ > 10:
        r = np.random.default_rng(seed)
        n = int(h_ / 3.2)
        for k in range(1, n):
            yy = -h_ / 2 + k * h_ / n
            x1 = w_ / 2 - 2 - r.uniform(0, w_ * 0.3)
            c.drawPath(poly_path([(-w_ / 2 + 2, yy), (x1, yy + r.normal(0, 0.3))], False, False), paint_(line_col, alpha * 0.28, stroke=True, width=0.5))
    if w_ > 12:
        c.drawPath(path, paint_(line_col, alpha * 0.8, stroke=True, width=0.8))
    c.restore()


# ---------------------------------------------------------------- pampas grass
def draw_pampas(c, base_x, base_y, height, t, wind, seed, plume_col, stem_col, n=7, gust=0.0, line_col=None, lit_col=None):
    """Pampas grass: thin stems, feathery plumes that lag behind the stem (overlapping action)."""
    r = np.random.default_rng(seed)
    lit_col = plume_col * 1.35 if lit_col is None else lit_col
    for i in range(n):
        bx = base_x + r.normal(0, 22)
        hh = height * r.uniform(0.7, 1.1)
        ph = r.uniform(0, 6.28)
        sway = wind * (math.sin(t * 1.3 + ph) * 0.5 + 0.5 + gust) * r.uniform(0.6, 1.2)
        pts = []
        for k in range(12):
            u = k / 11
            lag = math.sin(t * 1.3 + ph - u * 1.2)
            x = bx + sway * hh * 0.32 * u * u + lag * u * u * hh * 0.05
            y = base_y - hh * u
            pts.append((x, y))
        pts = np.array(pts)
        c.drawPath(ink_ribbon(pts[:9], 2.2, 1.0, 2.0), paint_(stem_col))
        # leaves at the base
        for k in range(3):
            lv = np.array([pts[0] + [r.normal(0, 4), 0], pts[2] + [r.normal(0, 12) + sway * 10, r.normal(0, 6)], pts[3] + [r.choice([-1, 1]) * hh * 0.2 + sway * 20, hh * 0.05]])
            c.drawPath(ink_ribbon(lv, 3, 0.5, 3.5), paint_(stem_col))
        plume = pts[6:]
        d = plume[-1] - plume[0]
        L = np.linalg.norm(d) + 1e-6
        nrm = np.array([-d[1], d[0]]) / L
        prof = np.sin(np.linspace(0.15, np.pi, len(plume))) ** 0.8 * hh * 0.055
        left = plume + nrm * prof[:, None] * (1 + 0.25 * sway)
        right = plume - nrm * prof[:, None] * (1 - 0.15 * sway)
        shape = np.vstack([left, right[::-1]])
        c.drawPath(poly_path(shape), paint_(plume_col, 0.95))
        # feathery fringe and lit strands
        for k in range(40):
            u = r.uniform(0.05, 1)
            idx = u * (len(plume) - 1)
            i0 = int(idx)
            i1 = min(i0 + 1, len(plume) - 1)
            p0 = plume[i0] * (1 - (idx - i0)) + plume[i1] * (idx - i0)
            side = r.choice([-1, 1])
            w0 = np.interp(idx, np.arange(len(prof)), prof)
            q0 = p0 + nrm * side * w0 * r.uniform(0.2, 0.9)
            q1 = q0 + nrm * side * w0 * r.uniform(0.3, 0.8) + d / L * hh * 0.05 + np.array([sway * 5, 0])
            col = lit_col if side < 0 else plume_col * 0.8
            c.drawPath(poly_path([q0, (q0 + q1) / 2 + r.normal(0, 1, 2), q1], False), paint_(col, 0.7, stroke=True, width=r.uniform(0.8, 1.8)))


# ---------------------------------------------------------------- post
def post(frame, rng_seed, grain=0.018, vignette=0.22, gamma=1.0):
    f = frame.astype(np.float32) / 255
    h, w = f.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = ((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2
    f *= (1 - vignette * np.clip(d - 0.25, 0, 1.5) / 1.5)[..., None]
    r = np.random.default_rng(rng_seed)
    g = r.normal(0, grain, (h // 2, w // 2)).astype(np.float32)
    g = cv2.resize(g, (w, h), interpolation=cv2.INTER_LINEAR)
    f += g[..., None]
    if gamma != 1.0:
        f = np.clip(f, 0, 1) ** gamma
    return (np.clip(f, 0, 1) * 255).astype(np.uint8)


def bloom(frame_f, thresh=0.72, radius=14, amt=0.35):
    br = np.clip(frame_f - thresh, 0, 1)
    b = cv2.GaussianBlur(br, (0, 0), radius)
    return frame_f + b * amt


# ---------------------------------------------------------------- character layer compositing
def layer(draw_fn, w=W, h=H):
    s = surface(w, h)
    c = s.getCanvas()
    c.clear(skia.Color4f(0, 0, 0, 0))
    draw_fn(c)
    a = surf_to_np(s).astype(np.float32) / 255  # skia hands back straight alpha
    a[..., :3] *= a[..., 3:4]                   # -> premultiplied RGBA
    return a


def light_layer(a, ambient=(1, 1, 1), lights=(), rim=None):
    """Grade a premultiplied RGBA character layer: multiply by ambient colour, add warm/cool
    point lights (only where the character is), optional rim light on the lit edge."""
    rgb = a[..., :3] * np.asarray(ambient, np.float32)
    al = a[..., 3]
    h, w = al.shape
    for (lx, ly, r, col, st) in lights:
        x0, x1 = int(max(0, lx - 3 * r)), int(min(w, lx + 3 * r))
        y0, y1 = int(max(0, ly - 3 * r)), int(min(h, ly + 3 * r))
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1]
        g = np.exp(-(((xx - lx) ** 2 + (yy - ly) ** 2) / (r * r)))[..., None] * st
        rgb[y0:y1, x0:x1] += g * np.asarray(col[:3]) * a[y0:y1, x0:x1, :3] * 1.6
    if rim is not None:
        dx, dy, col, st = rim
        sh = np.roll(np.roll(al, int(dy), 0), int(dx), 1)
        e = np.clip(al - sh, 0, 1)[..., None] * st
        rgb += e * np.asarray(col[:3])
    return np.dstack([np.clip(rgb, 0, None), al])


def over(dst, a):
    """dst float RGB, a premultiplied RGBA float."""
    dst[:] = dst * (1 - a[..., 3:4]) + a[..., :3]
    return dst


def to8(f):
    return (np.clip(f, 0, 1) * 255).astype(np.uint8)


def fade(f, k, col=(0, 0, 0)):
    return f * k + np.asarray(col, np.float32) * (1 - k)
