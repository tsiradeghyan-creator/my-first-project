"""Core drawing tools for THE LAST PAGE: noise, gouache painter, hand-inked lines, compositing."""
import math
import numpy as np
import cv2
import skia

W, H = 1280, 536          # 2.39:1 picture area
FPS = 24


# ---------------------------------------------------------------- colour helpers
def hexc(h, a=1.0):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [a], np.float32)


def mix(a, b, t):
    return np.asarray(a) * (1 - t) + np.asarray(b) * t


def sk(c, a=None):
    c = np.clip(np.asarray(c, np.float32), 0, 1)
    al = c[3] if (a is None and len(c) > 3) else (1.0 if a is None else a)
    return skia.Color4f(float(c[0]), float(c[1]), float(c[2]), float(al))


# ---------------------------------------------------------------- noise
def value_noise(h, w, scale, rng, octaves=4, persistence=0.5):
    """fbm value noise in [0,1], shape (h,w)."""
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    s = scale
    for _ in range(octaves):
        gh, gw = max(2, int(h / s) + 2), max(2, int(w / s) + 2)
        g = rng.random((gh, gw)).astype(np.float32)
        up = cv2.resize(g, (int(gw * s), int(gh * s)), interpolation=cv2.INTER_CUBIC)
        out += amp * up[:h, :w]
        tot += amp
        amp *= persistence
        s /= 2
        if s < 1.5:
            break
    out /= tot
    out = (out - out.min()) / (np.ptp(out) + 1e-6)
    return out


# ---------------------------------------------------------------- skia surfaces
def surface(w=W, h=H):
    return skia.Surface(w, h)


def surf_to_np(surf):
    img = surf.makeImageSnapshot()
    a = img.toarray(colorType=skia.kRGBA_8888_ColorType)
    return a


def np_to_image(arr):
    """arr uint8 HxWx3 or HxWx4 (RGBA, straight alpha)."""
    if arr.shape[2] == 3:
        arr = np.dstack([arr, np.full(arr.shape[:2], 255, np.uint8)])
    arr = np.ascontiguousarray(arr)
    return skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType,
                                alphaType=skia.kUnpremul_AlphaType)


def paint_(color, alpha=1.0, stroke=False, width=1.0, blur=0.0, aa=True, blend=None):
    p = skia.Paint(AntiAlias=aa, Color4f=sk(color, alpha))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(width)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur > 0:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if blend is not None:
        p.setBlendMode(blend)
    return p


def poly_path(pts, closed=True, smooth=True):
    """Catmull-Rom smoothed path through points (hand-drawn curves, not geometric)."""
    pts = np.asarray(pts, np.float32)
    path = skia.Path()
    n = len(pts)
    if n < 2:
        return path
    if not smooth or n < 3:
        path.moveTo(*pts[0])
        for p in pts[1:]:
            path.lineTo(*p)
        if closed:
            path.close()
        return path
    path.moveTo(*pts[0])
    rng_ = range(n) if closed else range(n - 1)
    for i in rng_:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = p1 + (p2 - p0) / 6
        c2 = p2 - (p3 - p1) / 6
        path.cubicTo(*c1, *c2, *p2)
    if closed:
        path.close()
    return path


def resample(pts, n, closed=True):
    pts = np.asarray(pts, np.float32)
    if closed:
        pts = np.vstack([pts, pts[:1]])
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    d = np.concatenate([[0], np.cumsum(seg)])
    t = np.linspace(0, d[-1], n, endpoint=not closed)
    x = np.interp(t, d, pts[:, 0])
    y = np.interp(t, d, pts[:, 1])
    return np.stack([x, y], 1)


def boil(pts, seed, amt=0.6):
    """Line boil: each new drawing is traced again by hand, so points wander slightly."""
    r = np.random.default_rng(seed)
    pts = np.asarray(pts, np.float32)
    n = len(pts)
    k = max(3, n // 6)
    ctrl = r.normal(0, amt, (k, 2)).astype(np.float32)
    idx = np.linspace(0, k - 1, n)
    off = np.stack([np.interp(idx, np.arange(k), ctrl[:, 0]), np.interp(idx, np.arange(k), ctrl[:, 1])], 1)
    return pts + off


def ink_ribbon(pts, w0, w1, wmid=None, closed=False, taper=True):
    """Variable-width ink line as a filled polygon: pressure swells mid-stroke, tapers at ends."""
    pts = np.asarray(pts, np.float32)
    n = len(pts)
    if n < 2:
        return skia.Path()
    if wmid is None:
        wmid = max(w0, w1) * 1.6
    t = np.linspace(0, 1, n)
    if closed:
        w = np.full(n, wmid) * (0.75 + 0.25 * np.sin(t * 6.283 * 2 + 1.3))
    else:
        prof = np.sin(np.pi * t) ** 0.7 if taper else np.ones(n)
        base = w0 * (1 - t) + w1 * t
        w = base + (wmid - base) * prof
    d = np.gradient(pts, axis=0)
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6)
    left = pts + nrm * (w[:, None] / 2)
    right = pts - nrm * (w[:, None] / 2)
    poly = np.vstack([left, right[::-1]])
    return poly_path(poly, closed=True, smooth=True)


# ---------------------------------------------------------------- gouache painter
def gouache(base, rng, flow=None, passes=((22, 0.55), (11, 0.7), (5, 0.8), (2.6, 0.85)),
            hue_jit=0.025, val_jit=0.05, detail_mask=None, dry=0.35):
    """Repaint a flat base image (float RGB 0..1) with opaque brush strokes.

    Coarse-to-fine: big strokes everywhere, small strokes only where the picture has
    detail, stroke direction follows the forms (perpendicular to the luminance gradient)
    blended with an optional flow field (radians). Returns uint8 RGB.
    """
    h, w = base.shape[:2]
    img8 = (np.clip(base, 0, 1) * 255).astype(np.uint8)
    s = surface(w, h)
    c = s.getCanvas()
    c.drawImage(np_to_image(img8), 0, 0)
    lum = cv2.cvtColor(img8, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    gx = cv2.Sobel(cv2.GaussianBlur(lum, (0, 0), 3), cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(cv2.GaussianBlur(lum, (0, 0), 3), cv2.CV_32F, 0, 1)
    mag = np.sqrt(gx * gx + gy * gy)
    edge_ang = np.arctan2(gy, gx) + np.pi / 2
    mag_n = mag / (np.percentile(mag, 99) + 1e-6)
    blurbase = {r: cv2.GaussianBlur(base, (0, 0), max(0.5, r / 3)) for r, _ in passes}
    p = skia.Paint(AntiAlias=True)
    p.setStyle(skia.Paint.kStroke_Style)
    p.setStrokeCap(skia.Paint.kRound_Cap)
    for pi, (rad, alpha) in enumerate(passes):
        step = rad * 0.9
        ys, xs = np.mgrid[0:h:step, 0:w:step]
        xs = (xs + rng.uniform(-step / 2, step / 2, xs.shape)).ravel()
        ys = (ys + rng.uniform(-step / 2, step / 2, ys.shape)).ravel()
        keep = (xs >= 0) & (xs < w) & (ys >= 0) & (ys < h)
        xs, ys = xs[keep], ys[keep]
        xi, yi = xs.astype(int), ys.astype(int)
        if pi > 0:
            thr = [0, 0.05, 0.12, 0.22][min(pi, 3)]
            m = mag_n[yi, xi]
            if detail_mask is not None:
                m = m + detail_mask[yi, xi]
            sel = (m > thr) | (rng.random(len(xs)) < 0.12)
            xs, ys, xi, yi = xs[sel], ys[sel], xi[sel], yi[sel]
        order = rng.permutation(len(xs))
        bb = blurbase[rad]
        for k in order:
            x, y = xs[k], ys[k]
            col = bb[yi[k], xi[k]].copy()
            v = 1 + rng.normal(0, val_jit)
            col = col * v + rng.normal(0, hue_jit, 3)
            a = edge_ang[yi[k], xi[k]]
            if flow is not None:
                fa = flow[yi[k], xi[k]]
                wgt = min(1.0, mag_n[yi[k], xi[k]] * 2)
                a = math.atan2(math.sin(a) * wgt + math.sin(fa) * (1 - wgt),
                               math.cos(a) * wgt + math.cos(fa) * (1 - wgt))
            a += rng.normal(0, 0.25)
            L = rad * rng.uniform(1.2, 2.6)
            dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2
            bend = rng.normal(0, rad * 0.25)
            path = skia.Path()
            path.moveTo(x - dx, y - dy)
            path.quadTo(x - dy * bend / L * 2, y + dx * bend / L * 2, x + dx, y + dy)
            p.setStrokeWidth(rad * rng.uniform(0.7, 1.15))
            p.setColor4f(sk(col, alpha * rng.uniform(0.75, 1.0)))
            c.drawPath(path, p)
    out = surf_to_np(s)[:, :, :3].astype(np.float32) / 255
    # pigment pooling at stroke edges + paper tooth
    hp = out - cv2.GaussianBlur(out, (0, 0), 2.2)
    out = out + hp * 0.3
    tooth = value_noise(h, w, 3, rng, octaves=2)
    out *= (1 - dry * 0.06) + dry * 0.12 * tooth[..., None]
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


# ---------------------------------------------------------------- base-image helpers (numpy)
def vgrad(h, w, stops):
    """Vertical gradient: stops = [(t, rgb), ...]."""
    t = np.linspace(0, 1, h)[:, None]
    out = np.zeros((h, w, 3), np.float32)
    ts = [s[0] for s in stops]
    for ch in range(3):
        out[..., ch] = np.interp(t, ts, [s[1][ch] for s in stops])
    return out


def fill_mask(img, mask, color, alpha=1.0):
    m = (mask.astype(np.float32) * alpha)[..., None]
    img[:] = img * (1 - m) + np.asarray(color[:3], np.float32) * m


def poly_mask(h, w, pts, feather=0.0, smooth=True):
    s = surface(w, h)
    c = s.getCanvas()
    c.clear(skia.ColorBLACK)
    c.drawPath(poly_path(pts, True, smooth), paint_((1, 1, 1)))
    m = surf_to_np(s)[:, :, 0].astype(np.float32) / 255
    if feather > 0:
        m = cv2.GaussianBlur(m, (0, 0), feather)
    return m


def soft_light(img, cx, cy, r, color, strength):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    g = np.exp(-d * d)[..., None] * strength
    return img + np.asarray(color[:3]) * g


# ---------------------------------------------------------------- timing
def ease(t, a=0.0, b=1.0, kind='inout'):
    """Spacing chart between two keys (slow-in/slow-out like an animator's thirds)."""
    t = np.clip((t - a) / (b - a + 1e-9), 0, 1)
    if kind == 'in':
        return t * t
    if kind == 'out':
        return 1 - (1 - t) ** 2
    if kind == 'lin':
        return t
    return t * t * (3 - 2 * t)


def on_twos(f, n=2):
    return f - (f % n)


def keyed(t, keys):
    """keys: list of (time, value dict). Returns interpolated dict with ease in/out between keys,
    holding before first and after last key."""
    if t <= keys[0][0]:
        return dict(keys[0][1])
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            e = ease(t, t0, t1)
            out = {}
            for k in v0:
                out[k] = v0[k] + (v1.get(k, v0[k]) - v0[k]) * e
            for k in v1:
                if k not in out:
                    out[k] = v1[k]
            return out
    return dict(keys[-1][1])
