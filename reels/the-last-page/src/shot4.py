"""Shot 4 - The Blank Book (0:18-0:25). The fox hops up, one paw on the empty page; a single line of
ink draws itself into a tiny bird, which shivers, peels off the page and flaps away."""
import numpy as np, cv2, math
from core import *
from fx import *
from fox import *

N = 168
# right page corners (screen): gutter-top, outer-top, outer-bottom, gutter-bottom
RP = np.array([[640, 228], [1010, 238], [1150, 452], [645, 440]], np.float32)
LP = np.array([[640, 228], [270, 238], [130, 452], [645, 440]], np.float32)
TABLE_Y = 470

BIRD = np.array([(0.02, 0.93), (0.06, 0.84), (0.12, 0.70), (0.22, 0.62), (0.32, 0.58), (0.38, 0.5), (0.44, 0.35), (0.5, 0.2), (0.56, 0.1),
                 (0.555, 0.25), (0.535, 0.4), (0.56, 0.47), (0.62, 0.42), (0.68, 0.37), (0.74, 0.38), (0.82, 0.43),
                 (0.74, 0.47), (0.68, 0.53), (0.58, 0.6), (0.46, 0.64), (0.34, 0.66), (0.24, 0.68), (0.14, 0.77)], np.float32)
WING = slice(5, 11)
EYE = np.array([0.705, 0.425], np.float32)


def page_map(uv, quad=RP):
    uv = np.atleast_2d(uv)
    u, v = uv[:, 0:1], uv[:, 1:2]
    top = quad[0] * (1 - u) + quad[1] * u
    bot = quad[3] * (1 - u) + quad[2] * u
    return top * (1 - v) + bot * v


def fox_pose(t, f):
    p = dict(s=0.95, tail_a=0.3, tail_curl=0.3)
    land = np.array([600.0, 432.0])
    start = np.array([110.0, 640.0])
    T0, T1 = 0.6, 1.12
    if t < T0:   # anticipation: sink down, ears forward
        k = ease(t, 0.0, T0)
        p.update(x=start[0], y=start[1], crouch=0.9 * k, lean=-0.3 * k, head_y=4 * k, tail_a=0.3 - 0.25 * k)
    elif t < T1:  # the hop: an arc, body stretched, legs trailing, tail lagging
        u = (t - T0) / (T1 - T0)
        pos = start * (1 - u) + land * u + np.array([0, -170 * math.sin(math.pi * u)])
        p.update(x=pos[0], y=pos[1], lean=0.9 - 1.6 * u, crouch=-0.2, fl_x=14 * (1 - u), fl_y=10, fr_x=10, fr_y=8,
                 bl_x=-16 * (1 - u), bl_y=6 + 6 * u, br_x=-20 * (1 - u), br_y=4, tail_lag=-0.6 * (1 - u) + 0.3 * u, tail_a=0.1)
    else:        # land, squash, settle
        st = t - T1
        p.update(x=land[0], y=land[1], crouch=0.8 * math.exp(-st * 7) + 0.1, squash=0.3 * math.exp(-st * 9),
                 tail_lag=0.4 * math.exp(-st * 4) * math.sin(st * 10))
        # lean forward, raise the paw, place it on the right page
        k = keyed(t, [(1.6, dict(fx=0, fy=0, hy=0, ht=0)), (1.95, dict(fx=10, fy=14, hy=4, ht=0.25)),
                      (2.3, dict(fx=34, fy=4, hy=6, ht=0.35)), (2.35, dict(fx=34, fy=2, hy=6, ht=0.38))])
        p['fl_x'], p['fl_y'] = k['fx'], k['fy']
        p['head_y'], p['head_tilt'] = k['hy'], k['ht']
        p['lean'] = 0.25 * ease(t, 1.6, 2.3)
        # follow the new bird with the eyes and head, ears up
        if t > 4.6:
            kk = keyed(t, [(4.6, dict(ht=0.38, hy=6)), (5.6, dict(ht=0.05, hy=-2)), (6.5, dict(ht=-0.6, hy=-8))])
            p['head_tilt'], p['head_y'] = kk['ht'], kk['hy']
            p['ear_l'] = -0.3 * ease(t, 5.0, 5.3)
            p['ear_r'] = -0.25 * ease(t, 5.2, 5.5)
            p['tail_a'] = 0.3 + 0.3 * ease(t, 5.6, 6.2)
    return p


def brush_path(pts, prog, wmax, rng_seed):
    """Reveal a brush stroke up to arc-length fraction prog."""
    pts = resample(pts, 220, closed=False)
    n = max(2, int(len(pts) * prog))
    sub = pts[:n]
    t = np.linspace(0, 1, len(pts))[:n]
    # pressure: confident press at the start, lighter through the curves, a lift at the end
    pr = (0.55 + 0.45 * np.sin(np.pi * np.clip(t * 1.1, 0, 1)) ** 0.5) * (1 - 0.5 * np.clip((t - 0.85) / 0.15, 0, 1))
    w = wmax * pr
    d = np.gradient(sub, axis=0)
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6
    L = sub + nrm * w[:, None] / 2
    R = sub - nrm * w[:, None] / 2
    return poly_path(np.vstack([L, R[::-1]]), True, True), sub


class Shot:
    def __init__(self, seed=31):
        rng = np.random.default_rng(seed)
        h, w = H, W
        img, bm = shelves_base(w, h, rng, shelf_h=52, top_dark=0.85, tint=(0.55, 0.58, 0.85))
        img = cv2.GaussianBlur(img, (0, 0), 2.5)
        # floor
        
        # lectern-table: thick dark wood slab with carved apron
        tb = np.array([[90, TABLE_Y - 8], [1190, TABLE_Y - 8], [1210, TABLE_Y + 16], [70, TABLE_Y + 16]])
        fill_mask(img, poly_mask(h, w, tb, smooth=False), hexc('#5a3a2a'))
        ap = np.array([[100, TABLE_Y + 16], [1180, TABLE_Y + 16], [1170, 560], [110, 560]])
        fill_mask(img, poly_mask(h, w, ap, smooth=False), hexc('#3a2419'))
        for k in range(7):
            x = 140 + k * 150
            pan = np.array([[x, TABLE_Y + 30], [x + 120, TABLE_Y + 30], [x + 118, 560], [x + 2, 560]])
            fill_mask(img, poly_mask(h, w, pan, smooth=False), hexc('#2e1c14'))
            cv2.line(img, (x, TABLE_Y + 30), (x + 120, TABLE_Y + 30), (0.42, 0.28, 0.19), 2, cv2.LINE_AA)
        # the book: cover edges, page block thickness, yellowed pages, gutter shadow
        cover = np.array([[640, 222], [1022, 232], [1166, 460], [645, 448], [114, 460], [258, 232]])
        fill_mask(img, poly_mask(h, w, cover, smooth=False), hexc('#4a2a26'))
        block = np.array([[645, 440], [1150, 452], [1155, 463], [645, 451], [125, 463], [130, 452]])
        fill_mask(img, poly_mask(h, w, block, smooth=False), hexc('#cdb78e'))
        for q in (RP, LP):
            m = poly_mask(h, w, q, smooth=False)
            uu = np.linspace(0, 1, w)[None, :]
            fill_mask(img, m, hexc('#cdbb92'))
        g = np.exp(-((np.arange(w)[None, :] - 650) / 26.0) ** 2)
        img *= (1 - 0.35 * g * poly_mask(h, w, np.vstack([RP, LP]), smooth=False)[..., None]) if False else 1
        gm = poly_mask(h, w, np.array([[624, 228], [656, 228], [664, 440], [628, 440]]), feather=12)
        img *= (1 - 0.35 * gm)[..., None]
        # age: foxing stains on the paper
        for _ in range(40):
            q = RP if rng.random() < 0.5 else LP
            pt = page_map(rng.uniform(0.05, 0.95, 2), q)[0]
            cv2.circle(img, (int(pt[0]), int(pt[1])), int(rng.uniform(2, 7)), (0.8, 0.68, 0.45), -1, cv2.LINE_AA)
        self.base = img
        self.bg = gouache(np.clip(img, 0, 1), rng, hue_jit=0.006, val_jit=0.02, passes=((14, 0.45), (7, 0.55), (3.5, 0.7), (2, 0.75))).astype(np.float32) / 255
        self.dust = Dust(rng, 14, (300, 200, 1100, h), vel=(-2, 4), size=(0.3, 0.8))
        self.lpos = (60, 560)

    def bird_points(self, t, f):
        """Screen points of the ink bird (flat on page -> peeled -> flying)."""
        flat = page_map(BIRD)
        eye = page_map(EYE)[0]
        if t < 4.5:
            return flat, eye, 0.0, 0.0
        r = np.random.default_rng(on_twos(f))
        if t < 5.1:   # shiver
            amp = 1.6 * ease(t, 4.5, 5.0)
            j = r.normal(0, amp, flat.shape)
            return flat + j, eye + j[6], 0.0, 0.0
        # peel: the tail end lifts first, the paper bird rises off the page, then flaps away
        u = ease(t, 5.1, 5.8, 'inout')
        cen = flat.mean(0)
        lifted = (flat - cen) * np.array([0.8, 1.25]) + cen + np.array([0, -40])
        pts = flat * (1 - u) + lifted * u
        # tail-first lift: points with small u (tail) rise earlier
        lag = np.clip(1 - BIRD[:, 0], 0, 1)[:, None]
        pts += np.array([0, -12]) * lag * math.sin(math.pi * u)
        eye2 = eye * (1 - u) + ((eye - cen) * np.array([0.8, 1.25]) + cen + [0, -40]) * u
        fly = max(0.0, t - 5.8)
        if fly > 0:
            path_off = np.array([fly * 260, -fly * 200 - fly * fly * 90])
            pts = pts + path_off
            eye2 = eye2 + path_off
        flap = math.sin((on_twos(f) / FPS) * 2 * math.pi * 4.0) if t > 5.45 else 0.0
        joint = pts[4]
        wing = pts[WING] - joint
        ang = -0.9 * flap
        ca, sa = math.cos(ang), math.sin(ang)
        pts = pts.copy()
        pts[WING] = joint + np.stack([wing[:, 0] * ca - wing[:, 1] * sa, wing[:, 0] * sa + wing[:, 1] * ca * (0.6 + 0.4 * abs(flap))], 1)
        return pts, eye2, u, flap

    def frame(self, f):
        t = f / FPS
        h, w = H, W
        ta = on_twos(f) / FPS
        img = self.bg.copy()
        flick = 0.9 + 0.1 * math.sin(ta * 19) * math.sin(ta * 7.1)
        img = glow(img, self.lpos[0], self.lpos[1], 220, hexc('#ff9548'), 0.28 * flick)
        p = fox_pose(ta, f)
        # ---- ink on the page (drawn into the painted page, under the fox)
        ink_l = layer(lambda c: None)
        if ta >= 2.9:
            prog = ease(ta, 2.9, 4.5, 'inout')
            pts, eye, peel, flap = self.bird_points(ta, f)

            bpts = pts[2:] if peel > 0 else pts

            def draw_ink(c):
                if peel > 0.02:
                    # the drawing lifts away as a paper cut-out of itself
                    cut = poly_path(resample(bpts, 120, closed=False), False, True)
                    pa = min(1.0, peel * 1.6)
                    c.drawPath(cut, paint_(hexc('#2a1e18'), 0.55 * pa, stroke=True, width=21))
                    c.drawPath(cut, paint_(hexc('#d9c79e'), pa, stroke=True, width=18))
                    c.drawPath(cut, paint_(hexc('#efe2bf'), 0.6 * pa, stroke=True, width=8))
                path, sub = brush_path(bpts, prog if peel == 0 else 1.0, 7.0, 3)
                # ink bleed halo, then the stroke itself
                c.drawPath(path, paint_(hexc('#3a3040'), 0.25, blur=1.6))
                c.drawPath(path, paint_(hexc('#1b1620'), 0.96))
                if prog > 0.985 or peel > 0:
                    c.drawCircle(float(eye[0]), float(eye[1]), 3.6, paint_(hexc('#1b1620')))
                if peel == 0 and prog < 1:
                    tip = sub[-1]
                    c.drawCircle(float(tip[0]), float(tip[1]), 4.2, paint_(hexc('#1b1620'), 0.9))
            ink_l = layer(draw_ink)
        # ---- fox and lantern light
        def draw(c):
            draw_side_fox(c, p, 'moon', seed=on_twos(f) // 2)
        a = layer(draw)
        a = light_layer(a, ambient=(0.68, 0.7, 0.95), lights=[(self.lpos[0], self.lpos[1], 260, hexc('#ffaa60'), 0.55 * flick)],
                        rim=(-2, -2, hexc('#a8b6ff'), 0.3))
        # smear frame at take-off: drybrush streaks behind the fox
        if 0.62 <= ta < 0.72:
            sm = cv2.GaussianBlur(a, (0, 0), 5)
            M = np.float32([[1, 0, -30], [0, 1, 35]])
            sm = cv2.warpAffine(sm, M, (w, h))
            over(img, sm * 0.5)
        # fox shadow on the page / floor
        if ta > 1.1:
            sh = np.zeros((h, w), np.float32)
            cv2.ellipse(sh, (int(p['x'] - 4), int(p['y'] + 1)), (50, 6), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
            img *= (1 - cv2.GaussianBlur(sh, (0, 0), 3) * 0.35)[..., None]
        if ta < 2.9 or True:
            over(img, ink_l if ink_l[..., 3].max() > 0 and (ta < 5.1) else np.zeros_like(ink_l))
        over(img, a)
        if ta >= 5.1:
            over(img, ink_l)   # once it peels, the bird is in front of everything
        d = layer(lambda c: self.dust.draw(c, ta, hexc('#e5e9ff'), alpha=0.22))
        over(img, d)
        img = bloom(img, 0.9, 9, 0.2)
        # tiny push toward the page as the ink starts
        z = 1.0 + 0.06 * ease(t, 2.4, 4.6)
        M = cv2.getRotationMatrix2D((800, 340), 0, z)
        img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return post(to8(img), 3000 + f, grain=0.016, vignette=0.3)
