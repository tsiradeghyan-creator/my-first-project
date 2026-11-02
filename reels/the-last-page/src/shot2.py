"""Shot 2 - The Reading Hall (0:07-0:14). Shelves into darkness, a moonbeam, the fox pads in."""
import numpy as np, cv2, math
from core import *
from fx import *
from fox import *

N = 168
FLOOR = int(H * 0.86)


def fox_pose(t):
    """Fox timing: walk in (0-4.5s), settle, lower head and set lantern down, look up."""
    x_end = 372.0
    T_STOP = 4.5
    speed = 92.0
    if t < T_STOP - 0.6:
        x = x_end - speed * (T_STOP - 0.3 - t)
        moving = 1.0
    else:
        u = ease(t, T_STOP - 0.6, T_STOP, 'out')
        x = x_end - speed * 0.3 * (1 - u)
        moving = 1 - u
    phase = (t / 0.55) % 1.0
    p = dict(x=x, y=FLOOR + 30, s=1.25, mouth=0.25, tail_a=0.3, tail_curl=0.25)
    if moving > 0.01:
        wf = walk_feet(phase, stride=40 * moving, lift=8 * moving)
        p.update(wf)
        p['tail_lag'] = 0.25 * math.sin(phase * 2 * math.pi * 2 - 1.2) * moving
        p['head_y'] = 1.5 * math.cos(phase * 4 * math.pi) * moving
        p['ear_l'] = 0.05 * math.sin(phase * 4 * math.pi - 0.8) * moving
    # settle overshoot after the stop
    st = t - T_STOP
    if st > 0:
        p['crouch'] = 0.25 * math.exp(-st * 6) * math.sin(st * 14)
        p['tail_lag'] = 0.35 * math.exp(-st * 4) * math.sin(st * 9)
    # lower head to set the lantern down
    k = keyed(t, [(4.55, dict(hy=0, ht=0, cr=0)), (5.15, dict(hy=13, ht=0.55, cr=0.45)), (5.45, dict(hy=13, ht=0.55, cr=0.45)),
                  (6.05, dict(hy=-7, ht=-0.62, cr=0.0)), (7.0, dict(hy=-8, ht=-0.66, cr=0.0))])
    p['head_y'] = p.get('head_y', 0) + k['hy']
    p['head_tilt'] = k['ht']
    p['crouch'] = p.get('crouch', 0) + k['cr']
    if t > 5.4:
        p['mouth'] = 0.0
    if t > 6.0:   # ears perk up one after the other, looking up into the dark
        p['ear_l'] = -0.25 * ease(t, 6.0, 6.25)
        p['ear_r'] = -0.2 * ease(t, 6.25, 6.5)
        p['tail_a'] = 0.3 + 0.2 * ease(t, 6.0, 6.6)
    return p


class Shot:
    def __init__(self, seed=11):
        rng = np.random.default_rng(seed)
        h, w = H, W
        img, bm = shelves_base(w, h, rng, shelf_h=46, top_dark=0.82, tint=(0.78, 0.8, 1.08))
        img[FLOOR:] = vgrad(h - FLOOR, w, [(0, hexc('#2a2838')), (1, hexc('#141320'))])
        # stone flags
        for k in range(0, w, 140):
            cv2.line(img, (k, FLOOR + 2), (int(k + (k - w / 2) * 0.35), h), (0.09, 0.09, 0.13), 1, cv2.LINE_AA)
        for yy in (FLOOR + 22, FLOOR + 52):
            cv2.line(img, (0, yy), (w, yy), (0.1, 0.1, 0.14), 1, cv2.LINE_AA)
        self.shaft = moon_shaft(h, w, w * 0.74, 430, 90, 250, hexc('#9fb2ff'), 0.36, soft=26)
        img += self.shaft * 0.85
        self.bg = gouache(img, rng, hue_jit=0.006, val_jit=0.02, passes=((14, 0.45), (7, 0.55), (3.5, 0.7), (2, 0.75))).astype(np.float32) / 255
        self.shaft_m = self.shaft[..., 2] / (self.shaft[..., 2].max() + 1e-6)
        self.dust = Dust(rng, 110, (300, 0, 1000, h), vel=(-3, 5), size=(0.3, 0.9))

    def frame(self, f):
        t = f / FPS
        ta = on_twos(f) / FPS           # character animation on twos
        h, w = H, W
        img = self.bg.copy()
        p = fox_pose(ta)
        # lantern: carried (swinging from the mouth) until 5.3s, then it sits on the floor
        if ta < 5.3:
            anc = side_anchor(p)
            ph = (ta / 0.55) % 1
            swing = 0.18 * math.sin(ph * 4 * math.pi - 1.0) * (1 if ta < 4.4 else math.exp(-(ta - 4.4) * 3))
            lpos = (anc[0], anc[1])
            ldown = None
        else:
            ldown = (side_anchor(fox_pose(5.3))[0], FLOOR + 30 - 30)
            lpos = None
        lc = (lpos[0], lpos[1] + 18) if lpos else (ldown[0], ldown[1] + 18)
        flick = 0.9 + 0.1 * math.sin(ta * 19) * math.sin(ta * 7.1)
        # warm pool of lantern light on floor and lower shelves
        img = glow(img, lc[0], lc[1] + 10, 120, hexc('#ff9a4a'), 0.22 * flick)
        img = glow(img, lc[0], FLOOR + 30, 60, hexc('#ffb060'), 0.18 * flick)

        def draw(c):
            draw_side_fox(c, p, 'moon', seed=on_twos(f) // 2, lw=1.0)
            if lpos:
                draw_lantern(c, lpos[0], lpos[1], 0.95, swing, 0, ta, 1)
            else:
                draw_lantern(c, ldown[0], ldown[1], 0.95, 0.0, 0, ta, 1)
        a = layer(draw)
        a = light_layer(a, ambient=(0.62, 0.66, 0.92), lights=[(lc[0], lc[1], 70, hexc('#ffb36a'), 0.9 * flick)],
                        rim=(-2, -1, hexc('#9fb2ff'), 0.35))
        # contact shadow
        sh = np.zeros((h, w), np.float32)
        cv2.ellipse(sh, (int(p['x'] - 5), FLOOR + 31), (70, 6), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
        img *= (1 - cv2.GaussianBlur(sh, (0, 0), 4) * 0.45)[..., None]
        over(img, a)
        # dust in the moonbeam
        def dd(c):
            self.dust.draw(c, ta, hexc('#dfe6ff'), mask_fn=lambda x, y: self.shaft_m[int(min(h - 1, max(0, y))), int(min(w - 1, max(0, x)))] * 1.2, alpha=0.45)
        d = layer(dd)
        over(img, d)
        img = bloom(img, 0.75, 10, 0.3)
        # slow push in
        z = 1.0 + 0.035 * ease(t, 0, 7, 'lin')
        M = cv2.getRotationMatrix2D((w * 0.36, h * 0.7), 0, z)
        img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return post(to8(img), 1000 + f, grain=0.016, vignette=0.3)
