"""-I- face: speech, blinks and brows on a 478-point face mesh, rendered by textured triangles.
The mouth opens onto a painted cavity (with a hint of teeth); the outer ring of the mesh is pinned so
the warp never shows a seam."""
import numpy as np
import cv2
import skia
from scipy.spatial import Delaunay

UPPER_INNER = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
LOWER_INNER = [308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 78]
UPPER_OUTER = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
LOWER_OUTER = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
EYE_PAIRS = [(386, 374), (385, 380), (384, 381), (398, 382), (387, 373), (388, 390), (466, 249),
             (159, 145), (158, 153), (157, 154), (173, 155), (160, 144), (161, 163), (246, 7)]
IRIS = list(range(468, 478))
BROWS = [336, 296, 334, 293, 300, 276, 283, 282, 295, 285, 107, 66, 105, 63, 70, 46, 53, 52, 65, 55]


class Face:
    def __init__(self, landmarks, img_shape):
        self.L0 = landmarks.astype(np.float32)
        h, w = img_shape[:2]
        x0, y0 = self.L0.min(0)
        x1, y1 = self.L0.max(0)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rw, rh = (x1 - x0) * 0.8, (y1 - y0) * 0.85
        ring = np.array([[cx + rw * np.cos(a), cy + rh * np.sin(a)] for a in np.linspace(0, 2 * np.pi, 28, endpoint=False)], np.float32)
        ring[:, 0] = np.clip(ring[:, 0], 0, w - 1)
        ring[:, 1] = np.clip(ring[:, 1], 0, h - 1)
        self.pts0 = np.vstack([self.L0, ring])
        self.n = len(self.L0)
        tri = Delaunay(self.pts0).simplices
        self.tris = tri
        self.F = float(np.linalg.norm(self.L0[10] - self.L0[152]))       # face height
        self.mouth_c = self.L0[[13, 14]].mean(0)
        self.chin = self.L0[152]
        fw = float(np.linalg.norm(self.L0[234] - self.L0[454]))
        L = self.L0
        dy = L[:, 1] - self.mouth_c[1]
        span = max(1.0, self.chin[1] - self.mouth_c[1])
        lat = np.exp(-((L[:, 0] - self.mouth_c[0]) / (0.42 * fw)) ** 2)
        self.w_jaw = np.clip(dy / span * 1.3, 0, 1) ** 0.7 * lat
        self.w_jaw[LOWER_INNER] = 1.0
        self.w_jaw[LOWER_OUTER[1:-1]] = np.maximum(self.w_jaw[LOWER_OUTER[1:-1]], 0.95)
        self.w_jaw[[78, 308, 61, 291]] = 0.45
        d61 = np.linalg.norm(L - L[61], axis=1)
        d291 = np.linalg.norm(L - L[291], axis=1)
        r = 0.08 * self.F
        self.w_left = np.exp(-(d61 / r) ** 2)
        self.w_right = np.exp(-(d291 / r) ** 2)

    def deform(self, jaw=0.0, width=0.0, blink=0.0, brow=0.0):
        P = self.pts0.copy()
        L = P[:self.n]
        F = self.F
        L[:, 1] += self.w_jaw * jaw * 0.11 * F
        L[UPPER_INNER, 1] -= jaw * 0.012 * F
        L[:, 0] -= self.w_left * width * 0.035 * F
        L[:, 0] += self.w_right * width * 0.035 * F
        if blink > 0:
            for u, d in EYE_PAIRS:
                L[u] = L[u] * (1 - blink * 0.92) + L[d] * blink * 0.92
            L[IRIS, 1] += blink * 0.012 * F
        if brow:
            L[BROWS, 1] -= brow * 0.025 * F
        return P

    def render(self, tex_img, params, surface_cache=None):
        """tex_img: float BGR rig image; returns animated copy (float BGR)."""
        h, w = tex_img.shape[:2]
        P = self.deform(**params)
        jaw = params.get('jaw', 0.0)
        rgba = np.dstack([(np.clip(tex_img[..., ::-1], 0, 1) * 255).astype(np.uint8), np.full((h, w), 255, np.uint8)])
        img = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)
        s = skia.Surface(w, h)
        c = s.getCanvas()
        c.drawImage(img, 0, 0)
        sh = img.makeShader(skia.TileMode.kClamp, skia.TileMode.kClamp)
        pos = [skia.Point(float(x), float(y)) for x, y in P]
        uv = [skia.Point(float(x), float(y)) for x, y in self.pts0]
        idx = [int(i) for i in self.tris.ravel()]
        v = skia.Vertices(skia.Vertices.kTriangles_VertexMode, pos, uv, None, idx)
        c.drawVertices(v, skia.Paint(AntiAlias=True, Shader=sh))
        if jaw > 0.04:
            up = P[UPPER_INNER]
            lo = P[LOWER_INNER[1:-1]]
            # the visible opening grows from the centre: shrink toward the lip line at small openings
            k = min(1.0, jaw / 0.35)
            ring = np.vstack([up, lo])
            cen = ring.mean(0)
            ring = cen + (ring - cen) * np.array([0.92 + 0.08 * k, k])
            up2, lo2 = ring[:len(up)], ring[len(up):]
            path = _smooth(ring)
            c.drawPath(path, skia.Paint(AntiAlias=True, Color4f=skia.Color4f(0.09, 0.03, 0.03, 0.95),
                                        MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 0.8)))
            if jaw > 0.2:
                h_open = float(np.mean(lo2[:, 1]) - np.mean(up2[:, 1]))
                band = np.vstack([up2, up2[::-1] + np.array([0, h_open * 0.3])])
                c.save()
                c.clipPath(path, doAntiAlias=True)
                c.drawPath(_smooth(band), skia.Paint(AntiAlias=True, Color4f=skia.Color4f(0.72, 0.68, 0.6, 0.8),
                                                     MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.5)))
                c.restore()
        out = s.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3][..., ::-1]
        return out.astype(np.float32) / 255


def _smooth(pts):
    pts = np.asarray(pts, np.float32)
    n = len(pts)
    path = skia.Path()
    path.moveTo(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = p1 + (p2 - p0) / 6
        c2 = p2 - (p3 - p1) / 6
        path.cubicTo(*c1, *c2, *p2)
    path.close()
    return path
