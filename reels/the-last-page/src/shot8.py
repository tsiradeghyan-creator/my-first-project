"""Shot 8 - The Great Bird (0:44-0:52). The flock pulls together into one colossal bird made of pages,
gives one enormous wingbeat with real weight, then tears across the sky in a sweeping arc, leaving a
trail of light, mist and loose paper."""
import numpy as np, cv2, math
from core import *
from fx import *
from bg_tower import cumulus, comp
from shot7 import dawn_sky

N = 192
PAPER = [hexc(c)[:3] for c in ('#f3e6c8', '#ecdcb6', '#f7eedb', '#e2cfa4', '#efe0c0', '#d9c39a')]
INK = hexc('#3a2a24')[:3]

BODY = np.array([[-0.62, 0.04], [-0.3, -0.1], [0.1, -0.14], [0.42, -0.12], [0.62, -0.22], [0.78, -0.2], [0.98, -0.12],
                 [0.8, -0.06], [0.62, 0.02], [0.4, 0.12], [0.0, 0.16], [-0.35, 0.14]])
WING = np.array([[0.0, 0.0], [0.15, -0.3], [0.08, -0.7], [-0.15, -1.1], [-0.38, -1.42], [-0.5, -1.38], [-0.52, -1.2],
                 [-0.6, -1.14], [-0.6, -0.95], [-0.7, -0.86], [-0.66, -0.66], [-0.76, -0.55], [-0.68, -0.36], [-0.72, -0.2], [-0.5, 0.05]])
TAIL = np.array([[-0.55, -0.02], [-1.02, -0.2], [-1.12, -0.06], [-1.1, 0.1], [-1.02, 0.22], [-0.55, 0.12]])
SHOULDER = np.array([0.12, -0.08])


def _rot(P, a, o):
    P = P - o
    return np.stack([P[:, 0] * math.cos(a) - P[:, 1] * math.sin(a), P[:, 0] * math.sin(a) + P[:, 1] * math.cos(a)], 1) + o


WING = _rot(WING, -0.6, SHOULDER) * np.array([1.0, 0.9])


def inside(poly, pts):
    from matplotlib.path import Path as MP
    return MP(poly).contains_points(pts)


def make_pages(rng, poly, n, size, angfn, part):
    x0, y0 = poly.min(0)
    x1, y1 = poly.max(0)
    pts = []
    while len(pts) < n:
        cand = rng.uniform([x0, y0], [x1, y1], (n * 3, 2))
        ok = cand[inside(poly, cand)]
        pts.extend(ok.tolist())
    pts = np.array(pts[:n])
    pages = []
    for p in pts:
        pages.append(dict(p=p, ang=angfn(p) + rng.normal(0, 0.2), w=size * rng.uniform(0.75, 1.2), h=size * rng.uniform(1.1, 1.5),
                          col=PAPER[rng.integers(len(PAPER))] * rng.uniform(0.92, 1.04), seed=int(rng.integers(1e6)),
                          sketch=rng.random() < 0.18, part=part,
                          start=np.array([rng.uniform(-0.3, 1.3) * W, rng.uniform(-0.2, 1.0) * H]),
                          arrive=rng.uniform(0.3, 2.3), curl=rng.uniform(0, 0.4)))
    # order by y so lower pages overlap like shingles
    pages.sort(key=lambda d: d['p'][1])
    return pages


class Shot:
    def __init__(self, seed=81):
        rng = np.random.default_rng(seed)
        h, w = H, W
        sky = dawn_sky(h, w, rng, (180, h * 0.82))
        sky = sky * np.linspace(1.0, 0.96, h)[:, None, None]
        cl = np.zeros((h, w, 3), np.float32)
        ca = np.zeros((h, w), np.float32)
        for (y, r0, r1, n, fl) in [(h * 0.84, 18, 36, 50, 0.45), (h * 0.95, 34, 70, 30, 0.55)]:
            c, a = cumulus(h, w, rng, [dict(y=y, x0=-80, x1=w + 80, r0=r0, r1=r1, n=n, jitter=r0 * 0.5, flat=fl)],
                           hexc('#fff0cc'), hexc('#e6a0a0'), hexc('#7a6aa2'), rim=hexc('#fff4d0'), rim_amt=0.9, lightdir=(-0.45, -0.3))
            comp(cl, c, a)
            ca = np.maximum(ca, a)
        comp(sky, cl, ca)
        # high wisps
        for k in range(8):
            m = np.zeros((h, w), np.float32)
            cv2.ellipse(m, (int(rng.uniform(0, w)), int(rng.uniform(30, 260))), (int(rng.uniform(140, 360)), int(rng.uniform(4, 9))), rng.uniform(-4, 4), 0, 360, 1.0, -1, cv2.LINE_AA)
            comp(sky, np.zeros_like(sky) + hexc('#fbe2c8')[:3], cv2.GaussianBlur(m, (0, 0), 3) * 0.6)
        self.bg = gouache(np.clip(sky, 0, 1), rng, hue_jit=0.006, val_jit=0.016, passes=((24, 0.5), (12, 0.6), (5, 0.7), (2.5, 0.8))).astype(np.float32) / 255
        S = 0.062
        prim = []
        # primary and secondary flight feathers: long pages fanning along the trailing edge
        te = resample(WING[4:15], 16, closed=False)
        for k, q in enumerate(te):
            d = q - SHOULDER
            out = d / (np.linalg.norm(d) + 1e-6)
            ang = math.atan2(out[1], out[0])
            L = 0.16 + 0.1 * (1 - k / 16)
            for j in range(2):
                prim.append(dict(p=q + out * L * 0.35 + rng.normal(0, 0.01, 2), ang=ang + math.pi / 2 + rng.normal(0, 0.08), w=0.06, h=L,
                                 col=PAPER[rng.integers(len(PAPER))], seed=int(rng.integers(1e6)), sketch=False, part='near',
                                 start=np.array([rng.uniform(-0.3, 1.3) * W, rng.uniform(-0.2, 1.0) * H]), arrive=rng.uniform(1.4, 2.4), curl=0.1))
        far = make_pages(rng, WING * 0.92 + [0.02, 0.02], 150, S, lambda p: math.atan2(-p[1], -p[0]) - 1.2, 'far')
        for d in far:
            d['col'] = d['col'] * np.array([0.78, 0.74, 0.86])
        self.pages = (far + make_pages(rng, TAIL, 60, S, lambda p: math.pi / 2 + 0.2, 'body') +
                      make_pages(rng, BODY, 150, S * 0.85, lambda p: math.pi / 2 - 0.1, 'body') + prim +
                      make_pages(rng, WING, 330, S, lambda p: math.atan2(-p[1], -p[0]) - 1.3, 'near'))
        self.loose = []
        self.trail = []
        self.rng = rng

    def bird_xform(self, t):
        """Centre, scale and wing angle of the great bird at time t."""
        if t < 3.9:
            c = np.array([600.0, 300.0]) + np.array([0, 8 * math.sin(t * 1.4)])
            sc = 190.0
        else:
            u = ease(t, 3.9, 8.0, 'in')
            p0, p1, p2 = np.array([600.0, 290.0]), np.array([1000.0, 150.0]), np.array([1650.0, -120.0])
            c = (1 - u) ** 2 * p0 + 2 * (1 - u) * u * p1 + u * u * p2
            sc = 190.0 * (1 - 0.55 * u)
        # wing: gathering hold -> slow rise -> powerful downstroke with overshoot -> flight beats
        if t < 2.6:
            th = 0.35 + 0.05 * math.sin(t * 3)
        elif t < 3.2:
            th = 0.35 + 0.75 * ease(t, 2.6, 3.2, 'inout')
        elif t < 3.55:
            th = 1.1 - 2.05 * ease(t, 3.2, 3.55, 'in')
        elif t < 3.95:
            th = -0.95 + 0.6 * ease(t, 3.55, 3.95, 'out')
        else:
            th = -0.35 + 0.75 * (0.5 + 0.5 * math.cos((t - 3.95) / 1.1 * 2 * math.pi))
        dip = 0.0
        if 3.3 < t < 4.2:   # the bird's weight: it sinks on the downstroke then surges up
            dip = -28 * math.sin(math.pi * (t - 3.3) / 0.9)
        c = c + np.array([0, dip])
        return c, sc, th

    def frame(self, f):
        t = f / FPS
        ta = on_twos(f) / FPS
        h, w = H, W
        img = self.bg.copy()
        c, sc, th = self.bird_xform(ta)
        rng = np.random.default_rng(f)

        def wing_xf(p, part, th):
            q = p - SHOULDER
            a = -(th - 0.35) * (0.8 if part == 'far' else 1.0)
            # wing bends: tip lags (overlapping action) on the fast downstroke
            dist = np.linalg.norm(q)
            a += -0.25 * dist * math.sin(th * 2.0)
            q = np.array([q[0] * math.cos(a) - q[1] * math.sin(a), q[0] * math.sin(a) + q[1] * math.cos(a)])
            if part == 'far':
                q = q * np.array([0.85, 0.7]) + np.array([-0.05, -0.05])
            return q + SHOULDER, a

        # trail of light and mist behind the bird once it flies
        if ta > 3.9:
            pts = []
            for k in range(40):
                tt = ta - k * 0.05
                if tt < 3.9:
                    break
                cc, ss, _ = self.bird_xform(tt)
                pts.append(cc + np.array([-0.4, 0.0]) * ss)
            if len(pts) > 2:
                pts = np.array(pts)

                def trail(cv):
                    path = poly_path(pts, False, True)
                    cv.drawPath(path, paint_(hexc('#fff3d6'), 0.4, stroke=True, width=64, blur=22))
                    cv.drawPath(path, paint_(hexc('#ffffff'), 0.7, stroke=True, width=5, blur=3))
                over(img, layer(trail))
            # shed loose pages from the wing tips
            if f % 2 == 0:
                for k in range(3):
                    tip, _ = wing_xf(WING[4], 'near', th)
                    self.loose.append(dict(p=c + tip * sc + rng.normal(0, 10, 2), v=np.array([rng.uniform(-80, -20), rng.uniform(20, 90)]),
                                           born=ta, rot=rng.uniform(0, 6), vr=rng.normal(0, 4), s=rng.uniform(8, 16), col=PAPER[rng.integers(6)]))
        gather = ta < 2.6

        def draw(cv):
            # loose pages behind
            for L in self.loose:
                age = ta - L['born']
                if age < 0 or age > 4:
                    continue
                pp = L['p'] + L['v'] * age + np.array([0, 20 * age * age])
                draw_page(cv, pp[0], pp[1], L['s'], L['s'] * 1.3, L['rot'] + L['vr'] * age, 0.2, L['col'], INK, max(0, 1 - age / 4), writing=True, seed=3)
            for pg in self.pages:
                part = pg['part']
                if part in ('near', 'far'):
                    q, a = wing_xf(pg['p'], part, th)
                    ang = pg['ang'] + a
                else:
                    q, ang = pg['p'], pg['ang']
                target = c + q * sc
                if gather and ta < pg['arrive']:
                    # still flying in: flutter along a curve toward its place
                    u = ease(ta, 0, pg['arrive'], 'inout')
                    pos = pg['start'] * (1 - u) + target * u + np.array([math.sin(u * 7 + pg['seed']) * 30 * (1 - u), -60 * math.sin(math.pi * u)])
                    draw_paper_bird(cv, pos[0], pos[1], (ta * 3 + pg['seed'] % 7 / 7) % 1, 13, math.atan2(target[1] - pos[1], target[0] - pos[0]) * 0.5,
                                    dict(span=1, sweep=0, ink=1), pg['col'], pg['col'] * 0.62, INK)
                    continue
                pw, ph = pg['w'] * sc, pg['h'] * sc
                tone = 1.0 if part != 'far' else 0.78
                draw_page(cv, target[0], target[1], pw, ph, ang, pg['curl'], pg['col'] * tone, INK * 0.5 + pg['col'] * 0.5, 1.0, writing=True, seed=pg['seed'])
                if pg['sketch'] and pw > 12:
                    cv.save()
                    cv.translate(target[0], target[1])
                    cv.rotate(math.degrees(ang))
                    r = np.random.default_rng(pg['seed'])
                    kind = r.integers(3)
                    if kind == 0:   # a little tree
                        cv.drawPath(poly_path([(0, ph * 0.3), (0, -ph * 0.05)], False, False), paint_(INK, 0.55, stroke=True, width=0.8))
                        cv.drawCircle(0, -ph * 0.15, pw * 0.22, paint_(INK, 0.45, stroke=True, width=0.7))
                    elif kind == 1:  # a moon and a hill
                        cv.drawCircle(pw * 0.15, -ph * 0.2, pw * 0.1, paint_(INK, 0.5, stroke=True, width=0.7))
                        cv.drawPath(poly_path([(-pw * 0.4, ph * 0.25), (0, ph * 0.05), (pw * 0.4, ph * 0.25)], False), paint_(INK, 0.5, stroke=True, width=0.7))
                    else:           # a tiny boat
                        cv.drawPath(poly_path([(-pw * 0.3, 0), (pw * 0.3, 0), (pw * 0.2, ph * 0.1), (-pw * 0.2, ph * 0.1)], True, False), paint_(INK, 0.5, stroke=True, width=0.7))
                        cv.drawPath(poly_path([(0, 0), (0, -ph * 0.25), (pw * 0.18, -ph * 0.02)], False, False), paint_(INK, 0.5, stroke=True, width=0.7))
                    cv.restore()
            if not gather or ta > 2.3:
                hb = c + np.array([[0.62, -0.24], [0.8, -0.24], [1.04, -0.13], [0.82, -0.07], [0.64, -0.04]]) * sc
                cv.drawPath(poly_path(hb, True, True), paint_(hexc('#f6ead0')))
                cv.drawPath(poly_path(hb[1:4], False, True), paint_(INK, 0.9, stroke=True, width=max(1.2, sc * 0.008)))
                cv.drawPath(poly_path(hb[[0, 1]], False, True), paint_(INK, 0.6, stroke=True, width=max(1.0, sc * 0.006)))
                e = c + np.array([0.76, -0.17]) * sc
                cv.drawCircle(float(e[0]), float(e[1]), max(2.0, sc * 0.018), paint_(INK, 1.0))
        a = layer(draw)
        a = light_layer(a, ambient=(1.0, 0.92, 0.84), rim=(-2, -2, hexc('#fff2c8'), 0.6))
        # smear on the fastest downstroke frames: paper blur along the motion
        if 3.25 < ta < 3.55:
            sm = cv2.GaussianBlur(a, (0, 0), 6)
            sm = cv2.warpAffine(sm, np.float32([[1, 0, 0], [0, 1, 26]]), (w, h))
            over(img, sm * 0.45)
        over(img, a)
        # the downstroke pushes a wave of air: mist ring below the bird
        if 3.45 < ta < 4.6:
            rt = ta - 3.45
            m = np.zeros((h, w), np.float32)
            cv2.ellipse(m, (int(c[0]), int(c[1] + 80 + rt * 60)), (int(140 + rt * 520), int(20 + rt * 60)), 0, 0, 360, 1.0, 6, cv2.LINE_AA)
            img = img + cv2.GaussianBlur(m, (0, 0), 8)[..., None] * hexc('#fff6e6')[:3] * 0.5 * math.exp(-rt * 2)
        img = bloom(img, 0.85, 16, 0.3)
        # camera: slight tilt-up following the climb
        M = np.float32([[1.03, 0, -w * 0.015], [0, 1.03, -h * 0.015 + 18 * ease(t, 3.9, 8)]])
        img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        return post(to8(img), 8000 + f, grain=0.012, vignette=0.2)
