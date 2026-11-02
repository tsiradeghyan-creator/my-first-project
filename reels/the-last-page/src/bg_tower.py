"""Shot 1 / 7 / 8 world: the library tower above the sea of clouds. Painted layers."""
import numpy as np
import cv2
from core import *


def cloud_sea(h, w, rng, top_y, light, shade, rim, scale=90, seed_off=0, density=0.5, bright=1.0):
    """Ghibli-like cumulus band: rounded billows with lit tops and cool undersides.
    Returns (rgb, alpha)."""
    n = value_noise(h, w, scale, rng, octaves=5, persistence=0.55)
    yy = np.linspace(0, 1, h)[:, None]
    # billow profile: the band thickens toward the bottom of the frame
    top = top_y + (n[0:1, :] - 0.5) * 0.0
    prof = np.clip((yy * h - top_y) / (h - top_y + 1e-6), 0, 1)
    field = (n * 0.9 + prof * 0.9 - (1 - density)).astype(np.float32)
    alpha = np.clip((field - 0.45) * 7, 0, 1)
    # billow tops: carve rounded bumps along the upper edge
    bumps = value_noise(h, w, scale * 0.45, rng, octaves=3)
    alpha *= np.clip((field + bumps * 0.25 - 0.5) * 6, 0, 1)
    # shading: light from above, height derivative of field
    gy = cv2.Sobel(cv2.GaussianBlur(field, (0, 0), 6), cv2.CV_32F, 0, 1)
    lit = np.clip(-gy * 18 + 0.35, 0, 1)
    lit = cv2.GaussianBlur(lit, (0, 0), 2)
    # cel-ish banding (painted clouds have soft but decisive value steps)
    lit = np.round(lit * 4) / 4 * 0.6 + lit * 0.4
    rgb = mix(np.asarray(shade[:3])[None, None], np.asarray(light[:3])[None, None], lit[..., None])
    # warm rim on the very top edge
    edge = np.clip(alpha - cv2.erode(alpha, np.ones((5, 5))), 0, 1)
    rgb = rgb * (1 - edge[..., None] * 0.6) + np.asarray(rim[:3]) * edge[..., None] * 0.6
    return rgb.astype(np.float32) * bright, alpha.astype(np.float32)


def comp(dst, rgb, a):
    dst[:] = dst * (1 - a[..., None]) + rgb * a[..., None]


def tower_layer(h, w, rng, cx, base_y, scale, time='night'):
    """Stone library tower on a cliff with a cracked copper dome gone green, ivy and pines.
    Returns rgb, alpha, and window positions (for the moving light)."""
    rgb = np.zeros((h, w, 3), np.float32)
    a = np.zeros((h, w), np.float32)
    if time == 'night':
        stone_l, stone_d = hexc('#6f6f93'), hexc('#2e2f4f')
        rock_l, rock_d = hexc('#4a4766'), hexc('#1e1d33')
        cop_l, cop_d = hexc('#5f9a8f'), hexc('#2a4a52')
        pine = hexc('#1b2a35')
        ivy_l, ivy_d = hexc('#3d5a52'), hexc('#1f3036')
    else:  # sunrise
        stone_l, stone_d = hexc('#e9c9a0'), hexc('#7b6a86')
        rock_l, rock_d = hexc('#c79a7e'), hexc('#4d4061')
        cop_l, cop_d = hexc('#9fd0a8'), hexc('#3f6e6e')
        pine = hexc('#33404a')
        ivy_l, ivy_d = hexc('#88a46a'), hexc('#3f5a4c')
    s = scale
    # cliff: jagged rock mass widening downward
    cliff = []
    for i in range(28):
        t = i / 27
        x = cx - 210 * s + 420 * s * t
        y = base_y - (1 - abs(t - 0.5) * 2) ** 0.6 * 70 * s + rng.normal(0, 7 * s)
        cliff.append((x, y))
    cliff += [(cx + 300 * s, h + 40), (cx - 320 * s, h + 40)]
    m = poly_mask(h, w, cliff)
    rock_n = value_noise(h, w, 18 * s, rng, octaves=4)
    xx = np.arange(w)[None, :]
    side = np.clip((xx - (cx - 60 * s)) / (240 * s), 0, 1)  # light from the left
    rr = mix(rock_l[:3], rock_d[:3], np.clip(side * 0.8 + rock_n * 0.4, 0, 1)[..., None])
    comp(rgb, rr, m)
    a = np.maximum(a, m)
    # tower body: slightly tapering cylinder
    tw, th = 78 * s, 250 * s
    top_y = base_y - 40 * s - th
    body = [(cx - tw, base_y - 30 * s), (cx - tw * 0.92, top_y), (cx + tw * 0.92, top_y), (cx + tw, base_y - 30 * s)]
    m = poly_mask(h, w, body, smooth=False)
    u = np.clip((xx - (cx - tw)) / (2 * tw), 0, 1)
    cyl = np.clip(np.sin(u * np.pi * 0.9 + 0.25) * 1.1, 0, 1)  # lit from left
    stone_n = value_noise(h, w, 6 * s, rng, octaves=3)
    yy = np.arange(h)[:, None]
    courses = (np.sin(yy / (7 * s) * np.pi) > 0.85).astype(np.float32) * 0.15
    sh = np.clip(1 - cyl + stone_n * 0.25 + courses, 0, 1)
    tr = mix(stone_l[:3], stone_d[:3], sh[..., None] * np.ones((1, 1, 1)))
    comp(rgb, tr, m)
    a = np.maximum(a, m)
    # gallery ring + corbels under the dome
    ring = [(cx - tw * 1.08, top_y + 10 * s), (cx - tw * 1.08, top_y - 4 * s), (cx + tw * 1.08, top_y - 4 * s), (cx + tw * 1.08, top_y + 10 * s)]
    m = poly_mask(h, w, ring, smooth=False)
    comp(rgb, mix(stone_l[:3], stone_d[:3], np.clip(1 - cyl, 0, 1)[..., None] * 0.9 + 0.1), m)
    # dome
    dome = []
    for i in range(40):
        ang = np.pi * i / 39
        dome.append((cx - np.cos(ang) * tw * 0.98, top_y - 4 * s - np.sin(ang) ** 0.85 * 82 * s))
    m = poly_mask(h, w, dome)
    du = np.clip((xx - (cx - tw)) / (2 * tw), 0, 1)
    dv = np.clip((yy - (top_y - 90 * s)) / (90 * s), 0, 1)
    dsh = np.clip(du * 0.9 + (1 - dv) * -0.2 + 0.05, 0, 1)
    patina = value_noise(h, w, 9 * s, rng, octaves=3)
    dr = mix(cop_l[:3], cop_d[:3], dsh[..., None])
    # old copper: streaks of brown where patina broke away
    streak = (value_noise(h, w, 4 * s, rng, octaves=2) > 0.72).astype(np.float32)
    dr = mix(dr, hexc('#7a5a3e')[:3] * (0.6 if time == 'night' else 1.0), (streak * 0.5)[..., None])
    dr *= (0.9 + patina[..., None] * 0.2)
    # ribs
    for k in range(-3, 4):
        rx = cx + k * tw * 0.3
        rib = np.exp(-((xx - rx) / (1.4 * s)) ** 2) * (yy < top_y)
        dr = dr * (1 - rib[..., None] * 0.35)
    comp(rgb, dr, m)
    a = np.maximum(a, m)
    # crack in the dome
    crack = [(cx + 10 * s, top_y - 80 * s), (cx + 18 * s, top_y - 60 * s), (cx + 12 * s, top_y - 44 * s), (cx + 26 * s, top_y - 22 * s)]
    cm = np.zeros((h, w), np.uint8)
    cv2.polylines(cm, [np.int32(crack)], False, 255, max(1, int(2 * s)), cv2.LINE_AA)
    comp(rgb, np.zeros_like(rgb) + hexc('#121522')[:3], cm.astype(np.float32) / 255)
    # lantern finial
    fm = poly_mask(h, w, [(cx - 6 * s, top_y - 82 * s), (cx, top_y - 104 * s), (cx + 6 * s, top_y - 82 * s)])
    comp(rgb, np.zeros_like(rgb) + cop_d[:3], fm)
    a = np.maximum(a, fm)
    # windows (arched): dark, one will carry the moving light
    wins = []
    for row, wy in enumerate([top_y + 40 * s, top_y + 110 * s, top_y + 180 * s]):
        for k in (-1, 0, 1):
            wx = cx + k * tw * 0.52 - (0.06 * tw if k == 0 else 0)
            ww, wh = 9 * s * (0.75 if k != 0 else 1), 26 * s
            pts = [(wx - ww, wy + wh)]
            for i in range(9):
                ang = np.pi * i / 8
                pts.append((wx - np.cos(ang) * ww, wy - np.sin(ang) * ww))
            pts.append((wx + ww, wy + wh))
            wm = poly_mask(h, w, pts)
            comp(rgb, np.zeros_like(rgb) + hexc('#14152a')[:3], wm)
            wins.append((wx, wy + wh * 0.3, ww, wh))
    # ivy: clustered leaf dabs climbing the left and bottom of the tower
    ivy = np.zeros((h, w), np.float32)
    for _ in range(int(900 * s)):
        y = rng.uniform(top_y + 20 * s, base_y - 20 * s)
        hgt = (base_y - y) / th
        x = cx - tw + abs(rng.normal(0, 30 * s * (0.4 + hgt)))
        if rng.random() < 0.35:
            x = cx + tw - abs(rng.normal(0, 14 * s))
        if rng.random() < hgt * 0.9:
            continue
        cv2.circle(ivy, (int(x), int(y)), max(1, int(rng.uniform(2, 4.5) * s)), 1.0, -1, cv2.LINE_AA)
    ivy = np.minimum(ivy, a)
    ivn = value_noise(h, w, 3 * s, rng, octaves=2)
    comp(rgb, mix(ivy_l[:3], ivy_d[:3], np.clip(ivn * 0.7 + side * 0.4, 0, 1)[..., None]), ivy * 0.95)
    # pines: layered triangular tiers on the cliff
    for k in range(9):
        px = cx + rng.choice([-1, 1]) * rng.uniform(95, 230) * s
        py = base_y - rng.uniform(5, 50) * s
        ph = rng.uniform(70, 150) * s
        pts = []
        tiers = 6
        for tI in range(tiers + 1):
            yv = py - ph * tI / tiers
            wv = (1 - tI / tiers) * ph * 0.32 + 2
            pts.append((px - wv + rng.normal(0, 2 * s), yv + rng.normal(0, 2 * s)))
            pts.append((px - wv * 0.55, yv - ph / tiers * 0.4))
        right = [(2 * px - x, y) for (x, y) in pts[::-1]]
        pm = poly_mask(h, w, pts + right, smooth=False)
        pn = value_noise(h, w, 4 * s, rng, octaves=2)
        pc = mix(pine[:3] * 1.35, pine[:3] * 0.75, np.clip((xx - px) / (ph * 0.3) * 0.5 + 0.5 + pn * 0.3 - 0.15, 0, 1)[..., None])
        comp(rgb, pc, pm)
        a = np.maximum(a, pm)
    return rgb, a, wins


def wobble_circle(cx, cy, r, rng, n=28, amt=0.07, flat=1.0):
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    k = rng.normal(0, amt, 5)
    rr = r * (1 + k[0] * np.sin(ang * 2 + k[1] * 9) + k[2] * np.sin(ang * 3 + k[3] * 9) + k[4] * np.sin(ang * 5))
    return np.stack([cx + np.cos(ang) * rr, cy + np.sin(ang) * rr * flat], 1)


def cumulus(h, w, rng, rows, light, mid, shade, rim=None, rim_amt=0.0, lightdir=(-0.3, -0.42)):
    """Painted cumulus in flat value bands (shade / mid / light), crisp lit shapes,
    drawn lobe by lobe back to front like a background painter builds billows."""
    s = surface(w, h)
    c = s.getCanvas()
    c.clear(skia.Color4f(0, 0, 0, 0))
    pl, pm, ps = paint_(light), paint_(mid), paint_(shade)
    for row in rows:
        xs = np.sort(rng.uniform(row['x0'], row['x1'], row['n']))
        for x in xs:
            r = rng.uniform(row['r0'], row['r1'])
            y = row['y'] + rng.normal(0, row.get('jitter', r * 0.25)) - r * 0.35
            for lob in range(rng.integers(2, 5)):
                lr = r * rng.uniform(0.55, 0.95)
                lx = x + rng.normal(0, r * 0.45)
                ly = y + rng.normal(0, r * 0.18) + (r - lr) * 0.6
                fl = row.get('flat', 1.0)
                base = wobble_circle(lx, ly, lr, rng, flat=fl)
                path = poly_path(base)
                c.drawPath(path, ps)
                c.save()
                c.clipPath(path, doAntiAlias=True)
                c.drawPath(poly_path(base + np.array([lightdir[0] * lr * 0.35, lightdir[1] * lr * 0.35])), pm)
                c.drawPath(poly_path(wobble_circle(lx + lightdir[0] * lr * 0.55, ly + lightdir[1] * lr * 0.6 * fl, lr * 0.92, rng, flat=fl)), pl)
                c.restore()
    arr = surf_to_np(s).astype(np.float32) / 255
    a = arr[..., 3]
    rgb = arr[..., :3] / np.maximum(a[..., None], 1e-4)
    if rim is not None and rim_amt > 0:
        edge = np.clip(a - cv2.erode(a, np.ones((3, 3))), 0, 1)
        up = np.clip(-cv2.Sobel(cv2.GaussianBlur(a, (0, 0), 2), cv2.CV_32F, 0, 1) * 3, 0, 1)
        e = (edge * up * rim_amt)[..., None]
        rgb = rgb * (1 - e) + np.asarray(rim[:3]) * e
    return np.clip(rgb, 0, 1), a
