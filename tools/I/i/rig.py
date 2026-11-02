"""-I- rig: turn a still image of a person into a deformable puppet.

Pose landmarks + segmentation (mediapipe, offline models bundled in the wheel) give a 2D skeleton
and a matte. The matte is filled with a triangle mesh; every vertex gets smooth weights to the
bones (linear blend skinning). The person is inpainted out of a copy of the image to give a clean
background plate. Faces get their own 478-point mesh for speech and blinks.
"""
import json
import math
import os
import numpy as np
import cv2
from scipy.spatial import Delaunay

# mediapipe pose ids
LM = dict(nose=0, l_eye=2, r_eye=5, l_ear=7, r_ear=8, l_shoulder=11, r_shoulder=12, l_elbow=13, r_elbow=14,
          l_wrist=15, r_wrist=16, l_hip=23, r_hip=24, l_knee=25, r_knee=26, l_ankle=27, r_ankle=28,
          l_foot=31, r_foot=32)

# bone: (pivot joint, end joint, parent bone)
BONES = [
    ('root', 'pelvis', 'neck', None),
    ('spine', 'pelvis', 'neck', 'root'),
    ('head', 'neck', 'head', 'spine'),
    ('l_upper_arm', 'l_shoulder', 'l_elbow', 'spine'),
    ('l_forearm', 'l_elbow', 'l_wrist', 'l_upper_arm'),
    ('r_upper_arm', 'r_shoulder', 'r_elbow', 'spine'),
    ('r_forearm', 'r_elbow', 'r_wrist', 'r_upper_arm'),
    ('l_thigh', 'l_hip', 'l_knee', 'root'),
    ('l_shin', 'l_knee', 'l_ankle', 'l_thigh'),
    ('l_foot', 'l_ankle', 'l_foot', 'l_shin'),
    ('r_thigh', 'r_hip', 'r_knee', 'root'),
    ('r_shin', 'r_knee', 'r_ankle', 'r_thigh'),
    ('r_foot', 'r_ankle', 'r_foot', 'r_shin'),
]
BONE_NAMES = [b[0] for b in BONES]


def _mp():
    import mediapipe as mp
    return mp


def detect(img_bgr):
    """Pose joints (dict), visibility, z, matte, face landmarks (478x2 or None)."""
    mp = _mp()
    h, w = img_bgr.shape[:2]
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    joints, vis, z, mask, face = {}, {}, {}, None, None
    with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=True) as P:
        r = P.process(rgb)
        if r.pose_landmarks:
            L = r.pose_landmarks.landmark
            for k, i in LM.items():
                joints[k] = np.array([L[i].x * w, L[i].y * h], np.float32)
                vis[k] = float(L[i].visibility)
                z[k] = float(L[i].z)
            mask = r.segmentation_mask.astype(np.float32)
    with mp.solutions.face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True, max_num_faces=1) as F:
        fr = F.process(rgb)
        if fr.multi_face_landmarks:
            face = np.array([[l.x * w, l.y * h] for l in fr.multi_face_landmarks[0].landmark], np.float32)
    return joints, vis, z, mask, face


def refine_matte(img_bgr, soft):
    """GrabCut around the network's matte for crisper edges."""
    h, w = soft.shape
    m = np.full((h, w), cv2.GC_BGD, np.uint8)
    m[soft > 0.05] = cv2.GC_PR_BGD
    m[soft > 0.4] = cv2.GC_PR_FGD
    m[soft > 0.85] = cv2.GC_FGD
    if (m == cv2.GC_FGD).sum() < 50:
        return soft
    bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
    try:
        cv2.grabCut(img_bgr, m, None, bg, fg, 3, cv2.GC_INIT_WITH_MASK)
    except cv2.error:
        return soft
    hard = np.where((m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD), 1.0, 0.0).astype(np.float32)
    hard = cv2.morphologyEx(hard, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats((hard > 0.5).astype(np.uint8))
    if n > 1:
        big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
        hard = (lab == big).astype(np.float32)
    # never lose what the network is sure about (light robes, linings), never keep what it rejects
    hard = np.maximum(hard, (soft > 0.35).astype(np.float32)) * (soft > 0.03)
    hard = cv2.morphologyEx(hard, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return cv2.GaussianBlur(hard, (0, 0), 1.0)


def seg_dist(p, a, b):
    ab = b - a
    t = np.clip(((p - a) @ ab) / (ab @ ab + 1e-6), 0, 1)
    q = a + t[:, None] * ab
    return np.linalg.norm(p - q, axis=1)


class Rig:
    def __init__(self, path=None):
        self.path = path

    # ------------------------------------------------------------ build
    @classmethod
    def build(cls, image_path, joints_override=None, spacing=None, matte=None):
        img = cv2.imread(image_path)
        h, w = img.shape[:2]
        joints, vis, z, soft, face = detect(img)
        if joints_override:
            for k, v in joints_override.items():
                joints[k] = np.array(v, np.float32)
                vis[k] = 1.0
        if not joints:
            raise RuntimeError('-I-: no person found; pass joints_override (see README)')
        if soft is None:
            soft = np.zeros((h, w), np.float32)
        mask = matte if matte is not None else refine_matte(img, soft)
        r = cls(image_path)
        r.img = img.astype(np.float32) / 255
        r.h, r.w = h, w
        r.mask = mask
        r.soft = soft
        r.vis, r.z = vis, z
        j = dict(joints)
        j['pelvis'] = (j['l_hip'] + j['r_hip']) / 2
        j['neck'] = (j['l_shoulder'] + j['r_shoulder']) / 2
        # head end: above the nose by the nose-neck distance
        up = j['nose'] - j['neck']
        j['head'] = j['nose'] + up * 0.6
        r.joints = j
        r.face = face
        r.facing = 1 if (j['nose'][0] - j['neck'][0]) >= -2 else -1
        r.frontal = abs(j['l_shoulder'][0] - j['r_shoulder'][0]) > 0.5 * np.linalg.norm(j['neck'] - j['pelvis'])
        r._mesh(spacing)
        r._weights()
        r._bg()
        return r

    def _mesh(self, spacing):
        m = (self.mask > 0.5).astype(np.uint8)
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            raise RuntimeError('-I-: empty matte')
        size = max(xs.max() - xs.min(), ys.max() - ys.min())
        sp = spacing or max(6, int(size / 45))
        pts = []
        cnts, _ = cv2.findContours(cv2.dilate(m, np.ones((5, 5), np.uint8)), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in cnts:
            c = c.reshape(-1, 2)
            step = max(1, int(sp * 0.6))
            pts += c[::step].tolist()
        gy, gx = np.mgrid[ys.min():ys.max():sp, xs.min():xs.max():sp]
        g = np.stack([gx.ravel(), gy.ravel()], 1)
        g = g[m[g[:, 1].astype(int), g[:, 0].astype(int)] > 0]
        pts += g.tolist()
        # extra density around joints so elbows/knees bend cleanly
        for k in ('l_elbow', 'r_elbow', 'l_knee', 'r_knee', 'l_shoulder', 'r_shoulder', 'l_hip', 'r_hip', 'neck'):
            c = self.joints[k]
            for a in np.linspace(0, 2 * np.pi, 10, endpoint=False):
                for rr in (sp * 0.5, sp):
                    q = c + rr * np.array([math.cos(a), math.sin(a)])
                    if 0 <= q[0] < self.w and 0 <= q[1] < self.h and m[int(q[1]), int(q[0])]:
                        pts.append(q.tolist())
        pts = np.unique(np.round(np.array(pts, np.float32), 1), axis=0)
        tri = Delaunay(pts)
        tris = tri.simplices
        cen = pts[tris].mean(1)
        md = cv2.dilate(m, np.ones((3, 3), np.uint8))
        keep = md[np.clip(cen[:, 1].astype(int), 0, self.h - 1), np.clip(cen[:, 0].astype(int), 0, self.w - 1)] > 0
        # drop long sliver triangles that bridge gaps (between legs, arm and body)
        e = np.stack([np.linalg.norm(pts[tris[:, a]] - pts[tris[:, b]], axis=1) for a, b in ((0, 1), (1, 2), (2, 0))], 1)
        keep &= e.max(1) < sp * 2.6
        self.verts = pts
        self.tris = tris[keep]

    def _weights(self):
        V = self.verts
        D = []
        L = np.linalg.norm(self.joints['neck'] - self.joints['pelvis']) + 1e-6
        for name, a, b, parent in BONES:
            pa, pb = self.joints[a], self.joints[b]
            d = seg_dist(V, pa, pb)
            if name == 'root':
                d = d + L * 0.25          # root only takes what nothing else claims (robes, capes)
            if name == 'head':
                d = d * 0.7
            if self.vis.get(b.replace('pelvis', 'l_hip'), 1.0) < 0.3 and name not in ('root', 'spine', 'head'):
                d = d + L * 2             # invisible limb: barely influences anything
            D.append(d)
        D = np.stack(D, 1)
        W = 1.0 / (D / L + 0.02) ** 4
        # keep the strongest 3
        idx = np.argsort(-W, axis=1)[:, 3:]
        np.put_along_axis(W, idx, 0, axis=1)
        self.weights = (W / W.sum(1, keepdims=True)).astype(np.float32)
        # draw order: far-side limbs first, then torso, then near-side limbs (mediapipe z: smaller = nearer)
        dom = np.argmax(self.weights[self.tris].sum(1), axis=1)
        key = np.zeros(len(self.tris))
        for i, (name, a, b, p) in enumerate(BONES):
            if name.startswith(('l_', 'r_')):
                zz = self.z.get(b, self.z.get(a, 0.0))
                key[dom == i] = zz
        self.tris = self.tris[np.argsort(-key, kind='stable')]

    def _bg(self):
        hole = cv2.dilate(((self.mask > 0.1) | (self.soft > 0.08)).astype(np.uint8), np.ones((25, 25), np.uint8))
        sc = 0.5
        sm = cv2.resize((self.img * 255).astype(np.uint8), (int(self.w * sc), int(self.h * sc)))
        hm = cv2.resize(hole, (sm.shape[1], sm.shape[0]), interpolation=cv2.INTER_NEAREST)
        try:   # Fourier-series inpainting rebuilds texture far better than Telea on big holes
            valid = (1 - hm).astype(np.uint8)
            f = np.zeros_like(sm)
            cv2.xphoto.inpaint(sm, valid, f, cv2.xphoto.INPAINT_FSR_FAST)
        except Exception:
            f = cv2.inpaint(sm, hm, 12, cv2.INPAINT_TELEA)
        f = cv2.GaussianBlur(cv2.resize(f, (self.w, self.h)).astype(np.float32) / 255, (0, 0), 1.2)
        m = cv2.GaussianBlur(hole.astype(np.float32), (0, 0), 4)[..., None]
        self.bg = self.img * (1 - m) + f * m

    # ------------------------------------------------------------ persistence
    def save(self, d):
        os.makedirs(d, exist_ok=True)
        np.savez_compressed(os.path.join(d, 'rig.npz'), img=self.img, mask=self.mask, bg=self.bg, verts=self.verts,
                            tris=self.tris, weights=self.weights, face=self.face if self.face is not None else np.zeros((0, 2)))
        meta = dict(path=self.path, joints={k: v.tolist() for k, v in self.joints.items()}, vis=self.vis, z=self.z,
                    facing=self.facing, frontal=bool(self.frontal), h=self.h, w=self.w)
        json.dump(meta, open(os.path.join(d, 'rig.json'), 'w'), indent=1)

    @classmethod
    def load(cls, d):
        z = np.load(os.path.join(d, 'rig.npz'))
        meta = json.load(open(os.path.join(d, 'rig.json')))
        r = cls(meta['path'])
        r.img, r.mask, r.bg, r.verts, r.tris, r.weights = z['img'], z['mask'], z['bg'], z['verts'], z['tris'], z['weights']
        r.face = z['face'] if len(z['face']) else None
        r.joints = {k: np.array(v, np.float32) for k, v in meta['joints'].items()}
        r.vis, r.z, r.facing, r.frontal, r.h, r.w = meta['vis'], meta['z'], meta['facing'], meta['frontal'], meta['h'], meta['w']
        return r

    def debug(self, out):
        v = (self.img * 255).astype(np.uint8).copy()
        for t in self.tris:
            cv2.polylines(v, [np.int32(self.verts[t])], True, (0, 255, 255), 1)
        for name, a, b, p in BONES:
            cv2.line(v, tuple(np.int32(self.joints[a])), tuple(np.int32(self.joints[b])), (0, 0, 255), 3)
        cv2.imwrite(out, v)
