"""Shot 9 - The Last Page (0:52-1:00). Pages spiral down through sunbeams; one blank page lands at the
fox's paws. It looks at the page, then at us, and puts its paw down. Ink writes the title."""
import numpy as np, cv2, math
from core import *
from fx import *
from fox import *
from bg_tower import cumulus, comp
from shot7 import dawn_sky

N = 192
CUT = 72
FONTS = '/home/user/my-first-project/reels/the-last-page/fonts/'
INK = hexc('#1c1418')[:3]
PAPERC = hexc('#f2e6c9')[:3]


def text_mask(txt, font_file, size, w, h, x, y, spacing=0.0):
    tf = skia.Typeface.MakeFromFile(FONTS + font_file)
    font = skia.Font(tf, size)
    s = surface(w, h)
    c = s.getCanvas()
    c.clear(skia.ColorBLACK)
    paint = skia.Paint(Color=skia.ColorWHITE, AntiAlias=True)
    if spacing == 0:
        c.drawString(txt, x, y, font, paint)
    else:
        xx = x
        for ch in txt:
            c.drawString(ch, xx, y, font, paint)
            xx += font.measureText(ch) + spacing
    return surf_to_np(s)[..., 0].astype(np.float32) / 255


def measure(txt, font_file, size):
    tf = skia.Typeface.MakeFromFile(FONTS + font_file)
    return skia.Font(tf, size).measureText(txt)


def brush_reveal(mask, prog, x0, x1, rng_noise, soft=28):
    """Reveal an ink mask left to right like one continuous brush stroke, with a wet leading edge."""
    h, w = mask.shape
    xx = np.arange(w)[None, :].astype(np.float32)
    front = x0 + (x1 - x0) * prog
    rv = np.clip((front - xx) / soft + 0.5, 0, 1)
    wet = np.exp(-((xx - front) / (soft * 0.8)) ** 2)
    m = mask * rv
    bleed = cv2.GaussianBlur(m, (0, 0), 1.4)
    m = np.maximum(m, bleed * 0.35)
    m = m * (0.82 + 0.18 * rng_noise)       # dry-brush streaks
    return np.clip(m, 0, 1), wet * mask


def draw_front_sitting(c, x, y, s, p, seed, pal='dawn', tail_flick=0.0):
    """Sitting fox seen from the front: tail curled round the side, chest ruff, two front legs."""
    from fox import Ink, PAL
    k = Ink(c, PAL[pal], seed, light=(0.6, -0.8))
    u = 60 * s
    c.save()
    c.translate(x, y)
    sgn = np.array([[-1, 1]])
    half = np.array([[0.0, 0.62], [0.6, 0.58], [0.82, 0.95], [0.95, 1.3], [1.12, 1.68], [1.22, 2.05], [1.08, 2.32], [0.6, 2.4], [0.0, 2.38]])
    body = np.vstack([half * sgn, half[::-1]]) * u
    k.part(body, 'fur', shade='fur_s', shade_off=0.12)
    # haunches: round thighs folded under the body
    for sg in (-1, 1):
        ang = np.linspace(0, 2 * np.pi, 20, endpoint=False)
        th = np.stack([sg * 0.82 + np.cos(ang) * 0.42, 1.98 + np.sin(ang) * 0.38], 1) * u
        k.part(th, 'fur', shade='fur_s', shade_off=0.2)
    bh = np.array([[0.0, 0.75], [0.45, 0.72], [0.7, 1.05], [0.55, 1.18], [0.66, 1.4], [0.42, 1.48], [0.4, 1.75], [0.0, 1.78]])
    bib = np.vstack([bh * sgn, bh[::-1]]) * u
    k.part(bib, 'cream', shade='cream_s', shade_off=0.06, line=False)
    # front legs, tapered, with rounded paws (the right paw can lift)
    for sg in (-1, 1):
        lift = p.get('paw', 0.0) if sg == 1 else 0.0
        top, bot = 1.32, 2.32 - lift * 0.25
        leg = np.array([[0.1, top], [0.4, top], [0.36, bot - 0.12], [0.42, bot], [0.36, bot + 0.07], [0.12, bot + 0.07], [0.08, bot], [0.13, bot - 0.12]]) * u
        leg[:, 0] *= sg
        k.part(leg, 'fur', shade='fur_s')
        sock = leg.copy()
        sock[0:2, 1] = (bot - 0.42) * u
        sock[0, 0], sock[1, 0] = 0.12 * sg * u, 0.38 * sg * u
        k.part(sock, 'dark', line=False)
        k.outline(k._boil(sock, 0.3), lw=1.0)
        for dx in (0.2, 0.28):
            k.stroke(np.array([[dx * sg, bot + 0.0], [dx * sg, bot + 0.06]]) * u, lw=0.8, col=hexc('#5a4040')[:3])
    # big fluffy tail curled round the right side, in front of the haunch
    tail = np.array([[0.55, 2.38], [1.2, 2.36], [1.75, 2.15], [2.15, 1.7], [2.2, 1.35], [1.95, 1.3], [1.8, 1.62], [1.45, 1.95], [1.0, 2.1], [0.5, 2.15]]) * u
    tail[3:6] += np.array([0.1, -tail_flick * 0.7]) * u
    k.part(tail, 'fur', shade='fur_s', shade_off=0.15)
    tip = np.array([[1.75, 2.15], [2.15, 1.7], [2.2, 1.35], [1.95, 1.3], [1.85, 1.55], [1.62, 1.9]]) * u
    tip[1:4] += np.array([0.1, -tail_flick * 0.7]) * u
    k.part(tip, 'cream', shade='cream_s', line=False)
    k.stroke(tip[[0, 5, 4]], lw=0.9)
    c.restore()
    draw_front_head(c, dict(p, x=x, y=y, s=s), pal, seed=seed, light=(0.6, -0.8), eye_glint=(1.0, 0.95, 0.85))


class Shot:
    def __init__(self, seed=91):
        rng = np.random.default_rng(seed)
        h, w = H, W
        # A: balcony, sky behind, sunbeams
        sky = dawn_sky(h, w, rng, (1240, 40), warm=0.7)
        cl = np.zeros((h, w, 3), np.float32)
        ca = np.zeros((h, w), np.float32)
        c_, a_ = cumulus(h, w, rng, [dict(y=h * 0.5, x0=-80, x1=w + 80, r0=20, r1=40, n=50, jitter=10, flat=0.45)],
                         hexc('#fff0cc'), hexc('#e6a0a0'), hexc('#8a78a8'), rim=hexc('#fff4d0'), rim_amt=0.9, lightdir=(0.45, -0.3))
        comp(sky, c_, a_)
        par = poly_mask(h, w, np.array([[-10, 300], [w + 10, 288], [w + 10, h + 10], [-10, h + 10]]), smooth=False)
        stone = value_noise(h, w, 7, rng, octaves=3)
        comp(sky, mix(hexc('#e2b896')[:3], hexc('#8a6c7a')[:3], np.clip(stone * 0.5 + (np.arange(h)[:, None] - 300) / 300, 0, 1)[..., None]), par)
        cap = poly_mask(h, w, np.array([[-10, 292], [w + 10, 280], [w + 10, 300], [-10, 312]]), smooth=False)
        comp(sky, np.zeros_like(sky) + hexc('#ffdcb4')[:3], cap)
        floor = poly_mask(h, w, np.array([[-10, 420], [w + 10, 420], [w + 10, h + 10], [-10, h + 10]]), smooth=False)
        comp(sky, vgrad(h, w, [(0, hexc('#c89a86')), (1, hexc('#a07a7c'))]), floor)
        self.bgA = gouache(np.clip(sky, 0, 1), rng, hue_jit=0.006, val_jit=0.02, passes=((20, 0.5), (10, 0.6), (5, 0.7), (2.5, 0.8))).astype(np.float32) / 255
        n = 50
        self.fall = dict(x=rng.uniform(-100, w + 100, n), y0=rng.uniform(-600, -40, n), r=rng.uniform(30, 120, n), sp=rng.uniform(40, 90, n),
                         ph=rng.uniform(0, 6.28, n), s=rng.uniform(12, 26, n), col=[PAPER for PAPER in [hexc('#f3e6c8')[:3]] * n], seed=rng.integers(0, 1e6, n))
        # B: the page, top-down, filling the frame
        pg = np.zeros((h, w, 3), np.float32) + hexc('#b08878')[:3]
        stone = value_noise(h, w, 9, rng, octaves=3)
        pg = pg * (0.85 + 0.25 * stone[..., None])
        page = np.array([[150, 24], [1150, 14], [1162, 518], [138, 526]])
        self.page_m = poly_mask(h, w, page, smooth=False)
        fib = value_noise(h, w, 2.5, rng, octaves=2)
        fib = cv2.resize(cv2.resize(fib, (w // 4, h)), (w, h))
        papr = PAPERC * (0.95 + 0.06 * fib[..., None])
        sh = cv2.GaussianBlur(self.page_m, (0, 0), 10)
        pg *= (1 - 0.35 * np.roll(np.roll(sh, 8, 0), 10, 1))[..., None]
        comp(pg, papr, self.page_m)
        self.bgB = gouache(np.clip(pg, 0, 1), rng, hue_jit=0.004, val_jit=0.012, passes=((18, 0.35), (9, 0.4))).astype(np.float32) / 255
        # title masks
        tw = measure('Fable 5.5', 'KaushanScript-Regular.ttf', 150)
        self.tx0 = (w - tw) / 2 - 40
        self.title = text_mask('Fable 5.5', 'KaushanScript-Regular.ttf', 150, w, h, self.tx0, 250)
        lw_ = measure('Every story begins with a blank page.', 'YujiSyuku-Regular.ttf', 34)
        self.lx0 = (w - lw_) / 2
        self.line = text_mask('Every story begins with a blank page.', 'YujiSyuku-Regular.ttf', 34, w, h, self.lx0, 420)
        # hanko seal: red square, characters knocked out in paper
        self.hx, self.hy, self.hs = int(self.tx0 + tw + 30), 196, 78
        seal = np.zeros((h, w), np.float32)
        cv2.rectangle(seal, (self.hx, self.hy), (self.hx + self.hs, self.hy + self.hs), 1.0, -1, cv2.LINE_AA)
        ch1 = text_mask('寓', 'YujiSyuku-Regular.ttf', 34, w, h, self.hx + 4, self.hy + 36)
        ch2 = text_mask('話', 'YujiSyuku-Regular.ttf', 34, w, h, self.hx + 4, self.hy + 72)
        ch3 = text_mask('寓', 'YujiSyuku-Regular.ttf', 34, w, h, self.hx + 40, self.hy + 36) * 0
        chars = np.clip(text_mask('寓', 'YujiSyuku-Regular.ttf', 36, w, h, self.hx + 21, self.hy + 37) + text_mask('話', 'YujiSyuku-Regular.ttf', 36, w, h, self.hx + 21, self.hy + 73), 0, 1)
        inner = np.zeros((h, w), np.float32)
        cv2.rectangle(inner, (self.hx + 5, self.hy + 5), (self.hx + self.hs - 5, self.hy + self.hs - 5), 1.0, 2, cv2.LINE_AA)
        stamp_tex = (value_noise(h, w, 2, rng, octaves=2) > 0.18).astype(np.float32)
        self.seal = np.clip(seal - chars - inner, 0, 1) * (0.75 + 0.25 * stamp_tex)
        self.noise = value_noise(h, w, 3, rng, octaves=2)
        self.noise = cv2.resize(cv2.resize(self.noise, (w, h // 6)), (w, h))

    # ------------------------------------------------------------------ A
    def balcony(self, f):
        t = f / FPS
        ta = on_twos(f) / FPS
        h, w = H, W
        img = self.bgA.copy()
        # sunbeams slanting down from the upper right
        for k, (x0, wd) in enumerate([(900, 120), (1080, 80), (700, 60)]):
            m = poly_mask(h, w, np.array([[x0, -10], [x0 + wd, -10], [x0 + wd - 520, h + 10], [x0 - 520, h + 10]]), feather=20, smooth=False)
            img += (m * (0.12 + 0.03 * math.sin(t * 1.3 + k)))[..., None] * hexc('#fff0c8')[:3]
        # the fox: looks at the page that lands at its paws, then at us
        landed = ta > 1.5
        kk = keyed(ta, [(0, dict(ly=-0.6, lx=0.4, tilt=0.0)), (1.2, dict(ly=-0.4, lx=0.2, tilt=0.0)), (1.6, dict(ly=1.0, lx=-0.1, tilt=-0.05)),
                        (2.1, dict(ly=1.0, lx=-0.1, tilt=-0.05)), (2.45, dict(ly=0.0, lx=0.0, tilt=0.06)), (3.0, dict(ly=0.0, lx=0.0, tilt=0.06))])
        p = dict(look_y=kk['ly'], look_x=kk['lx'], tilt=kk['tilt'], ear_l=-0.1 * math.sin(ta * 2.0), ear_r=0.0,
                 catch=1.0)
        if 1.5 < ta < 1.62:
            p['ear_l'] = 0.4   # a flick as the page lands
        bf = f - int(2.25 * FPS)
        p['blink_l'] = p['blink_r'] = {0: 0.5, 1: 1.0, 2: 1.0, 3: 0.5}.get(bf, 0.0)

        def draw(c):
            # falling pages behind the fox
            F = self.fall
            for i in range(len(F['x'])):
                yy = F['y0'][i] + F['sp'][i] * ta * 2.2
                x = F['x'][i] + math.sin(ta * 1.6 + F['ph'][i]) * F['r'][i] * 0.6
                rot = math.sin(ta * 2.2 + F['ph'][i]) * 0.9
                if -50 < yy < h + 50:
                    draw_page(c, x, yy, F['s'][i], F['s'][i] * 1.3, rot, 0.25, hexc('#f3e6c8')[:3], hexc('#5a4438')[:3], 1.0, writing=True, seed=int(F['seed'][i]))
            draw_front_sitting(c, 640, 196, 1.55, p, seed=on_twos(f) // 2)
            # THE page: spirals down and lands at the paws, blank
            if ta < 1.5:
                u = ease(ta, 0, 1.5, 'out')
                x = 640 + math.sin(ta * 4.2) * 150 * (1 - u)
                yy = -60 + (488 + 60) * u
                rot = math.sin(ta * 5) * 0.8 * (1 - u) + 0.1
                draw_page(c, x, yy, 76, 98 - 46 * u, rot, 0.3 * (1 - u), hexc('#f7eedb')[:3], hexc('#5a4438')[:3], 1.0, writing=False)
            else:
                draw_page(c, 640, 488, 78, 52, 0.08, 0.0, hexc('#f7eedb')[:3], hexc('#5a4438')[:3], 1.0, writing=False)
        a = layer(draw)
        a = light_layer(a, ambient=(1.0, 0.9, 0.85), rim=(2, -2, hexc('#ffe9b8'), 0.7))
        over(img, a)
        img = bloom(img, 0.85, 14, 0.3)
        return post(to8(img), 9000 + f, grain=0.012, vignette=0.22)

    # ------------------------------------------------------------------ B
    def page(self, f):
        t = (f - CUT) / FPS
        ta = on_twos(f - CUT) / FPS
        h, w = H, W
        img = self.bgB.copy()
        # paw: steps in from the top, presses, lifts away
        k = keyed(ta, [(0.0, dict(py=-220)), (0.45, dict(py=150)), (0.5, dict(py=158)), (1.35, dict(py=158)), (1.9, dict(py=-260))])
        paw_xy = (self.tx0 + 18, k['py'])
        # ink blooms from under the paw
        if ta > 0.5:
            bl = ease(ta, 0.5, 0.9, 'out')
            spot = np.zeros((h, w), np.float32)
            cv2.circle(spot, (int(paw_xy[0] + 20), int(paw_xy[1] + 70)), int(6 + bl * 16), 1.0, -1, cv2.LINE_AA)
            spot = cv2.GaussianBlur(spot, (0, 0), 2) * (1 - ease(ta, 0.9, 1.3)) * 0.9
            img = img * (1 - spot[..., None]) + INK * spot[..., None]
        if ta > 0.7:
            prog = ease(ta, 0.7, 2.1, 'inout')
            m, wet = brush_reveal(self.title, prog, self.tx0 - 10, self.tx0 + measure('Fable 5.5', 'KaushanScript-Regular.ttf', 150) + 20, self.noise)
            img = img * (1 - m[..., None]) + INK * m[..., None]
        # hanko presses in
        if ta > 2.3:
            sk_ = 1.0 + 0.12 * (1 - ease(ta, 2.3, 2.42, 'out'))
            a = min(1.0, (ta - 2.3) / 0.08)
            seal = self.seal
            if sk_ > 1.001:
                M = cv2.getRotationMatrix2D((self.hx + self.hs / 2, self.hy + self.hs / 2), -3, sk_)
                seal = cv2.warpAffine(seal, M, (w, h))
            else:
                M = cv2.getRotationMatrix2D((self.hx + self.hs / 2, self.hy + self.hs / 2), -3, 1.0)
                seal = cv2.warpAffine(seal, M, (w, h))
            img = img * (1 - seal[..., None] * a * 0.92) + hexc('#c8281e')[:3] * seal[..., None] * a * 0.92
        if ta > 2.6:
            prog = ease(ta, 2.6, 3.7, 'inout')
            m, _ = brush_reveal(self.line, prog, self.lx0 - 10, W - self.lx0 + 10, self.noise, soft=20)
            img = img * (1 - m[..., None] * 0.92) + INK * m[..., None] * 0.92

        def draw(c):
            # the paw (seen from above): dark sock, toe pads pressing
            if -200 < paw_xy[1] < h:
                x, y = paw_xy
                from fox import Ink, PAL
                kk = Ink(c, PAL['dawn'], on_twos(f), light=(0.6, -0.8))
                leg = np.array([[x - 46, y - 300], [x + 62, y - 300], [x + 64, y + 30], [x + 52, y + 80], [x + 10, y + 96], [x - 32, y + 82], [x - 46, y + 30]])
                kk.part(leg, 'fur', shade='fur_s', shade_off=0.1)
                sock = np.array([[x - 46, y - 30], [x + 64, y - 30], [x + 64, y + 30], [x + 52, y + 80], [x + 10, y + 96], [x - 32, y + 82], [x - 46, y + 30]])
                kk.part(sock, 'dark', line=False)
                kk.outline(kk._boil(sock, 0.3), lw=1.5)
                for dx in (-14, 4, 22, 38):
                    kk.stroke(np.array([[x + dx, y + 60], [x + dx + 1, y + 82]]), lw=1.0, col=hexc('#5a4040')[:3])
            # the tail flicks once across the corner
            if 6.65 - CUT / FPS + 3.0 < ta + 3.0 and 3.65 < ta < 4.2:
                u = (ta - 3.65) / 0.55
                sweep = math.sin(math.pi * u)
                from fox import Ink, PAL
                kk = Ink(c, PAL['dawn'], on_twos(f), light=(0.6, -0.8))
                base = np.array([w + 60, -40.0])
                spine = np.array([base + [-math.cos(0.6 + a * 0.15) * 260 * a * sweep, math.sin(0.4 + a * 0.3) * 200 * a * sweep] for a in np.linspace(0, 1, 9)])
                wid = np.array([70, 70, 66, 60, 54, 46, 36, 22, 4.0])
                from fox import limb
                tail = limb(spine, wid)
                kk.part(tail, 'fur', shade='fur_s')
                kk.part(limb(spine[5:], wid[5:]), 'cream', shade='cream_s', line=False)
        a = layer(draw)
        a = light_layer(a, ambient=(1.0, 0.94, 0.88))
        # the paw's soft shadow on the paper
        if -200 < paw_xy[1] < h:
            shm = np.zeros((h, w), np.float32)
            cv2.ellipse(shm, (int(paw_xy[0] + 22), int(paw_xy[1] + 70)), (60, 40), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
            lift = abs(k['py'] - 158) / 300
            shm = cv2.GaussianBlur(np.roll(shm, int(-20 - lift * 60), 1), (0, 0), 10 + lift * 20) * (0.35 - lift * 0.2)
            img *= (1 - np.clip(shm, 0, 1))[..., None]
        over(img, a)
        # fade to paper, then black
        fp = ease(ta, 4.2, 4.6)
        img = img * (1 - fp) + PAPERC * fp
        fb = ease(ta, 4.6, 5.0)
        img = img * (1 - fb)
        return post(to8(img), 9100 + f, grain=0.01 * (1 - fb), vignette=0.18 * (1 - fp))

    def frame(self, f):
        return self.balcony(f) if f < CUT else self.page(f)
