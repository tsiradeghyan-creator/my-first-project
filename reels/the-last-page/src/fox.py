"""The fox: an original small red fox kit, drawn as cel shapes with hand-inked lines.

Two model sheets: SIDE (walk, hop, crouch, balcony) and FRONT (close-up face, sitting).
Every pose is a set of drawing parameters; the outlines are rebuilt from scratch for each
drawing (no rigid sprites), traced with line boil, coloured in flat cel paint with one
hard-edged shadow tone, lit from a chosen direction.
"""
import math
import numpy as np
import skia
from core import *

# ---------------------------------------------------------------- palette (lighting variants)
PAL = {
    'moon': dict(fur='#b8573a', fur_s='#7a3330', cream='#d9cfd6', cream_s='#9a90ab', dark='#2c1d26',
                 line='#22141a', eye='#2a1a14', inner='#c88f8a', nose='#1a1014'),
    'lantern': dict(fur='#e07a3c', fur_s='#9c3f2c', cream='#f6e3c4', cream_s='#c79e86', dark='#3a2420',
                    line='#2a160e', eye='#2b1a10', inner='#eaa58c', nose='#1d120c'),
    'dawn': dict(fur='#ee8a43', fur_s='#a8513f', cream='#fbeedb', cream_s='#d3a793', dark='#3f2a28',
                 line='#2e1810', eye='#2b1a10', inner='#f2b49a', nose='#1d120c'),
}


def P(c):
    if isinstance(c, str):
        return hexc(c)
    c = np.asarray(c, np.float32)
    return np.append(c[:3], 1.0).astype(np.float32)


def rot(pts, a, ox=0.0, oy=0.0):
    pts = np.asarray(pts, np.float32)
    ca, sa = math.cos(a), math.sin(a)
    x = pts[:, 0] - ox
    y = pts[:, 1] - oy
    return np.stack([x * ca - y * sa + ox, x * sa + y * ca + oy], 1)


class Ink:
    """Draws one cel-painted, hand-inked part."""

    def __init__(self, canvas, pal, seed, scale=1.0, light=(-0.6, -0.8), lw=1.0):
        self.c = canvas
        self.pal = pal
        self.seed = seed
        self.s = scale
        self.light = np.array(light, np.float32) / np.linalg.norm(light)
        self.lw = lw
        self.k = 0

    def _boil(self, pts, amt=0.45):
        self.k += 1
        return boil(resample(pts, max(24, len(pts) * 3)), self.seed * 131 + self.k, amt * self.s)

    def part(self, pts, fill, shade=None, shade_off=0.22, line=True, lw=None, closed=True,
             extra_shade=None, smooth=True, line_col=None):
        pts = np.asarray(pts, np.float32)
        q = self._boil(pts) if closed else pts
        path = poly_path(q, True, smooth)
        self.c.drawPath(path, paint_(P(self.pal[fill])))
        if shade:
            # hard-edged shadow: the part minus itself shifted toward the light
            size = np.ptp(q, axis=0).max()
            off = self.light * size * shade_off
            self.c.save()
            self.c.clipPath(path, doAntiAlias=True)
            sh = skia.Path()
            sh.addRect(-4000, -4000, 8000, 8000)
            lit = poly_path(q + off, True, smooth)
            sh = skia.Op(sh, lit, skia.PathOp.kDifference_PathOp) or sh
            self.c.drawPath(sh, paint_(P(self.pal[shade])))
            if extra_shade is not None:
                self.c.drawPath(poly_path(extra_shade, True), paint_(P(self.pal[shade])))
            self.c.restore()
        if line:
            self.outline(q, lw, line_col)
        return path

    def outline(self, q, lw=None, col=None, closed=True):
        w = (lw or 1.6) * self.s * self.lw
        r = np.random.default_rng(self.seed * 7 + self.k)
        n = len(q)
        # an animator's line breaks into a few strokes with pressure, never one uniform outline
        cuts = sorted(r.choice(np.arange(4, n - 4), size=min(3, max(1, n // 30)), replace=False)) if n > 12 else []
        segs = []
        prev = 0
        for ccut in list(cuts) + [n]:
            segs.append(q[max(0, prev - 1):ccut + 1] if closed else q[prev:ccut + 1])
            prev = ccut
        if closed:
            segs.append(np.vstack([q[-2:], q[:2]]))
        pc = paint_(P(self.pal['line'] if col is None else col))
        for sgm in segs:
            if len(sgm) < 2:
                continue
            ww = w * r.uniform(0.85, 1.15)
            self.c.drawPath(ink_ribbon(sgm, ww * 0.45, ww * 0.45, ww * 1.15), pc)

    def stroke(self, pts, lw=1.4, col=None):
        q = boil(resample(pts, max(12, len(pts) * 4), closed=False), self.seed * 17 + self.k, 0.35 * self.s)
        self.k += 1
        w = lw * self.s * self.lw
        self.c.drawPath(ink_ribbon(q, w * 0.3, w * 0.3, w * 1.1), paint_(P(self.pal['line'] if col is None else col)))


def limb(pts, widths):
    """Tapered limb outline around a centre polyline."""
    pts = resample(np.asarray(pts, np.float32), 16, closed=False)
    wd = np.interp(np.linspace(0, 1, 16), np.linspace(0, 1, len(widths)), widths)
    d = np.gradient(pts, axis=0)
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6
    L = pts + nrm * wd[:, None] / 2
    R = pts - nrm * wd[:, None] / 2
    # rounded paw end
    end = pts[-1]
    ang0 = math.atan2(*(L[-1] - end)[::-1])
    cap = [end + wd[-1] / 2 * np.array([math.cos(ang0 - t), math.sin(ang0 - t)]) for t in np.linspace(0, math.pi, 7)]
    return np.vstack([L, cap, R[::-1]])


def ik2(hip, foot, l1, l2, bend):
    """Two-bone knee position; bend=+1 knee forward, -1 knee backward."""
    hip, foot = np.asarray(hip, np.float32), np.asarray(foot, np.float32)
    d = foot - hip
    L = np.linalg.norm(d) + 1e-6
    L2 = min(L, l1 + l2 - 1e-3)
    a = math.acos(np.clip((l1 * l1 + L2 * L2 - l2 * l2) / (2 * l1 * L2), -1, 1))
    base = math.atan2(d[1], d[0])
    ang = base - bend * a
    return hip + l1 * np.array([math.cos(ang), math.sin(ang)])


# ================================================================= SIDE FOX (faces right)
SIDE_DEFAULT = dict(x=0.0, y=0.0, s=1.0, crouch=0.0, arch=0.0, lean=0.0,
                    head_x=0.0, head_y=0.0, head_tilt=0.0, ear_l=0.0, ear_r=0.0, earflat=0.0,
                    tail_a=0.25, tail_curl=0.3, tail_lag=0.0, blink=0.0, mouth=0.0,
                    fl_x=0.0, fl_y=0.0, fr_x=0.0, fr_y=0.0, bl_x=0.0, bl_y=0.0, br_x=0.0, br_y=0.0,
                    look=0.0, squash=0.0, flip=0)


def draw_side_fox(canvas, prm, pal_name='lantern', seed=0, light=(-0.6, -0.8), lw=1.0, extra=None):
    p = dict(SIDE_DEFAULT)
    p.update(prm)
    pal = PAL[pal_name]
    s = p['s']
    canvas.save()
    canvas.translate(p['x'], p['y'])
    if p['flip']:
        canvas.scale(-1, 1)
    canvas.scale(s, s)
    ink = Ink(canvas, pal, seed, scale=1.0, light=light if not p['flip'] else (-light[0], light[1]), lw=lw / max(s, 0.3) * max(s, 0.3))
    ink.lw = lw / s if s < 1 else lw  # keep line weight visible at small sizes
    sq = p['squash']
    cr = p['crouch'] * 14
    by = -40 + cr + sq * 6               # body centre height above ground
    blen, bht = 50 * (1 + sq * 0.12), 21 * (1 - sq * 0.15)
    chest = np.array([22, by - 2])
    rump = np.array([-26, by - 2 + p['lean'] * 8])
    # ---- body outline (bean with arched back, deep chest, tucked belly)
    arch = p['arch'] * 8
    body = []
    for t in np.linspace(0, 1, 18):       # back: rump -> shoulders
        x = rump[0] + (chest[0] - rump[0]) * t
        y = rump[1] + (chest[1] - rump[1]) * t - bht * (0.8 + 0.25 * math.sin(math.pi * t)) - arch * math.sin(math.pi * t)
        body.append((x, y))
    body += [(chest[0] + 10, chest[1] - 8), (chest[0] + 13, chest[1] + 6), (chest[0] + 6, chest[1] + bht * 0.95)]
    for t in np.linspace(1, 0, 14):       # belly: chest -> rump
        x = rump[0] + (chest[0] - rump[0]) * t
        y = rump[1] + (chest[1] - rump[1]) * t + bht * (0.55 + 0.25 * math.sin(math.pi * (t * 0.8 + 0.2))) - 6 * math.sin(math.pi * t)
        body.append((x, y))
    body += [(rump[0] - 10, rump[1] + 6), (rump[0] - 12, rump[1] - 8)]
    body = np.array(body, np.float32)
    # ---- legs (far pair first, darker)
    gy = 0.0
    hips = {'fl': chest + [2, 8], 'fr': chest + [-4, 8], 'bl': rump + [6, 6], 'br': rump + [0, 6]}
    feet = {'fl': np.array([chest[0] + 4 + p['fl_x'], gy - p['fl_y']]),
            'fr': np.array([chest[0] - 6 + p['fr_x'], gy - p['fr_y']]),
            'bl': np.array([rump[0] + 2 + p['bl_x'], gy - p['bl_y']]),
            'br': np.array([rump[0] - 6 + p['br_x'], gy - p['br_y']])}

    def leg(k, far):
        hip, foot = hips[k], feet[k]
        front = k[0] == 'f'
        if front:
            mid = (hip + foot) / 2
            elbow = mid + [-3.5, -2]
            pts = [hip, elbow, foot + [1.5, -3], foot + [5, 0]]
            wid = [12, 7, 5.5, 6.5]
        else:
            hock = foot + [-5, -11]
            knee = (hip + hock) / 2 + [6, 2]
            pts = [hip + [0, -3], knee, hock, foot + [5, 0]]
            wid = [21, 9, 5.5, 6.5]
        shape = limb(pts, wid)
        pal_fill = 'fur_s' if far else 'fur'
        ink.part(shape, pal_fill, shade=None if far else 'fur_s', shade_off=0.25)
        # dark stockings on the lower leg
        lo = limb([pts[-2] * 0.45 + pts[-3] * 0.55, pts[-2], pts[-1]], [wid[-2] * 1.05, wid[-2], wid[-1]])
        ink.part(lo, 'dark', line=False)
        ink.outline(ink._boil(lo, 0.3), lw=1.2)

    leg('fr', True)
    leg('br', True)
    # ---- tail (behind body), bushy, lagging, white tip
    ta, curl, lag = p['tail_a'], p['tail_curl'], p['tail_lag']
    base = rump + [-6, -6]
    spine = []
    for t in np.linspace(0, 1, 9):
        ang = math.pi - ta - curl * t * 1.2 - lag * t * t * 1.4
        spine.append(base + np.array([math.cos(ang), -math.sin(ang)]) * 62 * t)
    spine = np.array(spine)
    for i in range(1, len(spine)):  # integrate the curve
        pass
    wid = np.array([16, 26, 32, 34, 32, 28, 22, 14, 3], np.float32)
    tail = limb(spine, wid)
    ink.part(tail, 'fur', shade='fur_s', shade_off=0.18)
    tip = limb(spine[5:], wid[5:])
    ink.part(tip, 'cream', shade='cream_s', shade_off=0.18, line=False)
    ink.stroke(spine[4:6] + [[0, -10], [0, 10]], lw=1.0)
    # ---- body
    ink.part(body, 'fur', shade='fur_s', shade_off=0.2)
    # chest bib in cream
    bib = [chest + [-6, -2], chest + [10, -6], chest + [13, 6], chest + [6, bht * 0.9], chest + [-8, bht * 0.7]]
    ink.part(bib, 'cream', shade='cream_s', line=False)
    ink.stroke(np.array([chest + [-6, -2], chest + [-9, 6], chest + [-8, bht * 0.7]]), lw=1.0)
    leg('fl', False)
    leg('bl', False)
    # ---- head
    hx, hy = chest[0] + 14 + p['head_x'], chest[1] - 22 + p['head_y']
    draw_side_head(ink, hx, hy, p)
    if extra:
        extra(canvas, ink, p, (hx, hy))
    canvas.restore()


def draw_side_head(ink, hx, hy, p):
    R = 18.5
    tilt = p['head_tilt'] - p['look'] * 0.5
    def T(pts):
        return rot(np.asarray(pts, np.float32) * R + [hx, hy], tilt, hx, hy)
    # far ear
    ear_poly = lambda bx, a, flat, k: rot(np.array([[bx - 0.45, -0.62], [bx - 0.05 - flat * 0.6, -1.85 + flat * 1.1], [bx + 0.5, -0.78]]) * R + [hx, hy], a - flat * 0.9, hx + bx * R, hy - 0.7 * R)
    ef = p['earflat']
    e2 = rot(ear_poly(0.25, -0.05 + p['ear_r'], ef, 1), tilt, hx, hy)
    ink.part(e2, 'fur_s', smooth=False)
    # skull + muzzle profile
    head = T([(-0.95, 0.35), (-0.98, -0.25), (-0.6, -0.88), (0.05, -1.02), (0.6, -0.8), (0.95, -0.45),
              (1.4, -0.24), (1.78, -0.08), (1.8, 0.1), (1.5, 0.3 + p['mouth'] * 0.1), (1.1, 0.48),
              (0.6, 0.8), (0.1, 1.02), (-0.25, 0.86), (-0.55, 1.0), (-0.8, 0.72)])
    ink.part(head, 'fur', shade='fur_s', shade_off=0.16)
    # cream cheek + lower muzzle
    cheek = T([(1.76, 0.08), (1.5, 0.06), (1.0, 0.12), (0.45, 0.3), (-0.2, 0.45), (-0.5, 0.95), (-0.25, 0.86),
               (0.1, 1.02), (0.6, 0.8), (1.15, 0.5), (1.65, 0.32)])
    ink.part(cheek, 'cream', shade='cream_s', shade_off=0.12, line=False)
    ink.stroke(T([(1.72, 0.1), (1.35, 0.08), (0.9, 0.16), (0.35, 0.36)]), lw=0.9)
    if p['mouth'] > 0.05:
        ink.stroke(T([(1.55, 0.26), (1.25, 0.3 + p['mouth'] * 0.2), (1.0, 0.38)]), lw=1.1)
    # nose
    nose = T([(1.68, -0.12), (1.88, -0.08), (1.9, 0.1), (1.72, 0.14)])
    ink.part(nose, 'nose', line=False)
    # eye: almond, with lid for blink
    ex, ey = 0.66, -0.3
    bl = p['blink']
    if bl > 0.85:
        ink.stroke(T([(ex - 0.2, ey + 0.05), (ex, ey + 0.11), (ex + 0.22, ey + 0.02)]), lw=1.5)
    else:
        op = 1 - bl
        eye = T([(ex - 0.22, ey + 0.04), (ex - 0.05, ey - 0.14 * op), (ex + 0.2, ey - 0.08 * op), (ex + 0.25, ey + 0.03), (ex + 0.02, ey + 0.13 * op)])
        ink.part(eye, 'eye', line=False)
        ink.stroke(T([(ex - 0.25, ey + 0.05), (ex - 0.05, ey - 0.16 * op), (ex + 0.24, ey - 0.08 * op), (ex + 0.3, ey + 0.0)]), lw=1.3)
        hl = T([(ex + 0.03, ey - 0.04 * op)])[0]
        ink.c.drawCircle(float(hl[0]), float(hl[1]), 1.9, paint_(hexc('#fff6e0')))
    # near ear on top
    e1 = rot(ear_poly(-0.25, -0.18 + p['ear_l'], ef, 0), tilt, hx, hy)
    ink.part(e1, 'fur', shade='fur_s', smooth=False)
    inner = e1.copy()
    cen = inner.mean(0)
    inner = cen + (inner - cen) * 0.55 + (inner[1] - cen) * 0.05
    ink.part(inner, 'inner', line=False, smooth=False)
    tipd = np.array([e1[1], e1[1] * 0.7 + e1[0] * 0.3, e1[1] * 0.7 + e1[2] * 0.3])
    ink.part(tipd, 'dark', line=False, smooth=False)


# ================================================================= FRONT FOX (faces camera)
FRONT_DEFAULT = dict(x=0.0, y=0.0, s=1.0, tilt=0.0, ear_l=0.0, ear_r=0.0, earflat=0.0,
                     blink_l=0.0, blink_r=0.0, look_x=0.0, look_y=0.0, nose_up=0.0, nostril=0.0,
                     mouth=0.0, head_turn=0.0, body=False, paw=0.0, tail=0.0, catch=1.0)


def draw_front_head(canvas, prm, pal_name='lantern', seed=0, light=(-0.6, -0.8), lw=1.0, eye_glint=None):
    p = dict(FRONT_DEFAULT)
    p.update(prm)
    pal = PAL[pal_name]
    canvas.save()
    canvas.translate(p['x'], p['y'])
    canvas.rotate(math.degrees(p['tilt']))
    canvas.scale(p['s'], p['s'])
    ink = Ink(canvas, pal, seed, light=light, lw=lw / p['s'] * 1.0)
    R = 60.0
    tu = p['head_turn']  # -1..1 small 3/4 turn

    def T(pts, depth=1.0):
        a = np.asarray(pts, np.float32).copy()
        a[:, 0] = a[:, 0] + tu * depth * 0.18 * (1 - np.abs(a[:, 0]) * 0.3)
        return a * R

    # ears (behind head). swivel = narrow + shift tip, flat = rotate down/outward
    def ear(side, sw, flat):
        sgn = -1 if side == 'l' else 1
        bx = sgn * 0.52
        wdt = 0.36 * (1 - abs(sw) * 0.45)
        tipx = bx + sgn * (0.22 + flat * 0.6) + sw * 0.2
        tipy = -1.55 + flat * 0.85
        outer = np.array([[bx - wdt * 1.25, -0.55], [bx - wdt * 0.85, -1.0], [tipx - 0.03, tipy], [tipx + 0.03, tipy + 0.02], [bx + wdt * 1.0, -0.98], [bx + wdt * 1.3, -0.45]])
        return outer
    for side, sw in (('l', p['ear_l']), ('r', p['ear_r'])):
        o = T(ear(side, sw, p['earflat']), 0.7)
        ink.part(o, 'fur', shade='fur_s', shade_off=0.2)
        cen = o.mean(0)
        inner = cen + (o - cen) * np.array([0.55, 0.7])
        inner[2:4] = o[2:4] * 0.8 + cen * 0.2
        # inner ear fluff shows less when the ear turns away
        ink.part(inner, 'inner', line=False)
        ink.stroke(np.array([inner[0] * 0.5 + inner[5] * 0.5 + [0, 4], cen + [0, -8], inner[2]]), lw=0.8, col=pal['fur_s'])
        tip = np.array([o[2], o[2] * 0.62 + o[1] * 0.38, o[3] * 0.62 + o[4] * 0.38, o[3]])
        ink.part(tip, 'dark', line=False)
    # head mass: broad cheeks with fluffy tufts, narrowing to the muzzle
    head = T([(-0.92, -0.05), (-0.88, -0.5), (-0.62, -0.85), (-0.25, -1.0), (0.25, -1.0), (0.62, -0.85), (0.88, -0.5), (0.92, -0.05),
              (1.22, 0.2), (1.0, 0.27), (1.2, 0.45), (0.92, 0.47), (1.0, 0.62), (0.62, 0.6), (0.3, 0.82), (0.0, 0.88),
              (-0.3, 0.82), (-0.62, 0.6), (-1.0, 0.62), (-0.92, 0.47), (-1.2, 0.45), (-1.0, 0.27), (-1.22, 0.2)])
    ink.part(head, 'fur', shade='fur_s', shade_off=0.14)
    # cream mask: cheeks and muzzle
    mask = T([(-1.16, 0.22), (-0.7, 0.12), (-0.32, 0.06), (-0.14, -0.2), (0.0, -0.3), (0.14, -0.2), (0.32, 0.06),
              (0.7, 0.12), (1.16, 0.22), (1.0, 0.27), (1.18, 0.44), (0.92, 0.46), (0.98, 0.6), (0.62, 0.58), (0.3, 0.8), (0.0, 0.86),
              (-0.3, 0.8), (-0.62, 0.58), (-0.98, 0.6), (-0.92, 0.46), (-1.18, 0.44), (-1.0, 0.27)], 1.1)
    ink.part(mask, 'cream', shade='cream_s', shade_off=0.05, line=False)
    ink.stroke(T([(-1.0, 0.27), (-0.6, 0.13), (-0.3, 0.07)], 1.1), lw=0.9)
    ink.stroke(T([(1.0, 0.27), (0.6, 0.13), (0.3, 0.07)], 1.1), lw=0.9)
    # brow fur marks
    ink.stroke(T([(-0.42, -0.62), (-0.3, -0.7)]), lw=0.8, col=pal['fur_s'])
    ink.stroke(T([(0.42, -0.62), (0.3, -0.7)]), lw=0.8, col=pal['fur_s'])
    # muzzle bridge
    ink.stroke(T([(-0.13, 0.0), (-0.12, 0.28), (-0.15, 0.48)], 1.3), lw=0.8, col=pal['cream_s'])
    # eyes
    for side, bl in (('l', p['blink_l']), ('r', p['blink_r'])):
        sgn = -1 if side == 'l' else 1
        ex, ey = sgn * 0.4, -0.22
        if bl > 0.85:
            ink.stroke(T([(ex - 0.2 * sgn, ey + 0.02), (ex, ey + 0.09), (ex + 0.17 * sgn, ey + 0.03)], 1.05), lw=2.2)
            continue
        op = 1 - bl * 0.9
        eye = T([(ex - 0.2 * sgn, ey + 0.03), (ex - 0.06 * sgn, ey - 0.15 * op), (ex + 0.12 * sgn, ey - 0.13 * op),
                 (ex + 0.21 * sgn, ey - 0.02), (ex + 0.08 * sgn, ey + 0.11 * op), (ex - 0.1 * sgn, ey + 0.1 * op)], 1.05)
        ink.part(eye, 'eye', line=False)
        # iris warm brown + pupil looking around
        cx = ex + p['look_x'] * 0.06
        cy = ey + p['look_y'] * 0.04
        irisp = T([(cx, cy)], 1.05)[0]
        canvas.save()
        canvas.clipPath(poly_path(eye), doAntiAlias=True)
        canvas.drawCircle(float(irisp[0]), float(irisp[1]), 0.115 * R, paint_(hexc('#8a4a22')))
        canvas.drawCircle(float(irisp[0]), float(irisp[1]), 0.07 * R, paint_(hexc('#140a06')))
        # lantern light caught in the eyes
        g = eye_glint or (1.0, 0.82, 0.45)
        canvas.drawCircle(float(irisp[0] - 0.04 * R), float(irisp[1] - 0.045 * R), 0.035 * R * p['catch'], paint_((*g, 1)))
        canvas.drawCircle(float(irisp[0] + 0.035 * R), float(irisp[1] + 0.035 * R), 0.016 * R * p['catch'], paint_((1, 1, 0.95, 1)))
        canvas.restore()
        # upper lid line, heavier at the outer corner
        ink.stroke(T([(ex - 0.23 * sgn, ey + 0.05), (ex - 0.06 * sgn, ey - 0.17 * op), (ex + 0.13 * sgn, ey - 0.15 * op), (ex + 0.25 * sgn, ey - 0.04)], 1.05), lw=2.4)
        ink.stroke(T([(ex + 0.1 * sgn, ey + 0.1 * op), (ex - 0.08 * sgn, ey + 0.1 * op)], 1.05), lw=0.7)
    # nose + mouth
    nu = p['nose_up'] * 0.05
    nf = 1 + p['nostril'] * 0.18
    nose = T([(-0.11 * nf, 0.5 - nu), (0.0, 0.46 - nu), (0.11 * nf, 0.5 - nu), (0.07, 0.58 - nu), (0.0, 0.61 - nu), (-0.07, 0.58 - nu)], 1.3)
    ink.part(nose, 'nose', line=False)
    hl = T([(-0.03, 0.5 - nu)], 1.3)[0]
    canvas.drawCircle(float(hl[0]), float(hl[1]), 0.022 * R, paint_(hexc('#6b5a5a')))
    m = p['mouth']
    ink.stroke(T([(0.0, 0.61 - nu), (0.0, 0.68 + m * 0.04)], 1.3), lw=1.0)
    ink.stroke(T([(-0.16, 0.7), (-0.06, 0.73 + m * 0.06), (0.0, 0.68 + m * 0.04), (0.06, 0.73 + m * 0.06), (0.16, 0.7)], 1.3), lw=1.0)
    canvas.restore()


def side_anchor(prm, local=(1.72, 0.22)):
    """World position of a point on the side head (default: mouth corner, where the lantern hangs)."""
    p = dict(SIDE_DEFAULT)
    p.update(prm)
    s = p['s']
    by = -40 + p['crouch'] * 14 + p['squash'] * 6
    chest = np.array([22, by - 2])
    hx, hy = chest[0] + 14 + p['head_x'], chest[1] - 22 + p['head_y']
    R = 18.5
    tilt = p['head_tilt'] - p['look'] * 0.5
    q = rot(np.array([local], np.float32) * R + [hx, hy], tilt, hx, hy)[0]
    sx = -1 if p['flip'] else 1
    return np.array([p['x'] + q[0] * s * sx, p['y'] + q[1] * s])


def walk_feet(phase, stride=24, lift=7):
    """Foot offsets for a walk cycle. phase in [0,1). Diagonal pairs move together, with a small
    offset (fl leads bl by 0.5, fr by 0.5...). Planted feet slide back at body speed."""
    def foot(ph):
        ph %= 1.0
        if ph < 0.62:      # stance: foot moves back relative to body
            u = ph / 0.62
            return stride * (0.5 - u), 0.0
        u = (ph - 0.62) / 0.38   # swing: lift and reach forward
        x = stride * (-0.5 + u * u * (3 - 2 * u))
        return x, lift * math.sin(math.pi * u)
    d = {}
    for k, off in (('fl', 0.0), ('br', 0.08), ('fr', 0.5), ('bl', 0.58)):
        x, y = foot(phase + off)
        d[k + '_x'], d[k + '_y'] = x, y
    d['squash'] = 0.06 * math.cos(phase * 4 * math.pi)
    return d
