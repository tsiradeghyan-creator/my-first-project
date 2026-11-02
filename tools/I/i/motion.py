"""-I- motion: 2D forward kinematics, linear blend skinning and a library of procedural motions.

A pose is a dict of local bone angle offsets (radians, + = clockwise on screen), optional bone length
scales ('<bone>_len'), and root channels: root_dx, root_dy (px in rig image space), root_rot, root_scale.
Motions are functions (t, rig, **params) -> pose. Clips layer additively with fades.
"""
import math
import numpy as np
from .rig import BONES

IDX = {b[0]: i for i, b in enumerate(BONES)}


def _rot(a, p):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, p[0] - c * p[0] + s * p[1]], [s, c, p[1] - s * p[0] - c * p[1]], [0, 0, 1]], np.float64)


def _axial(k, p, ang):
    """Scale by k along direction ang about point p."""
    c, s = math.cos(ang), math.sin(ang)
    R = np.array([[c, -s], [s, c]])
    S = R @ np.diag([k, 1.0]) @ R.T
    M = np.eye(3)
    M[:2, :2] = S
    M[:2, 2] = p - S @ p
    return M


def bone_transforms(rig, pose):
    J = rig.joints
    T = {}
    for name, a, b, parent in BONES:
        p = J[a]
        ang = pose.get(name, 0.0)
        L = np.eye(3)
        k = pose.get(name + '_len', 1.0)
        if k != 1.0:
            d = J[b] - J[a]
            L = _axial(k, p, math.atan2(d[1], d[0])) @ L
        L = _rot(ang, p) @ L
        if parent is None:
            s = pose.get('root_scale', 1.0)
            Sm = np.array([[s, 0, p[0] - s * p[0]], [0, s, p[1] - s * p[1]], [0, 0, 1]])
            Tr = np.array([[1, 0, pose.get('root_dx', 0.0)], [0, 1, pose.get('root_dy', 0.0)], [0, 0, 1]])
            T[name] = Tr @ Sm @ _rot(pose.get('root_rot', 0.0), p) @ L
        else:
            T[name] = T[parent] @ L
    return T


def skin(rig, pose):
    T = bone_transforms(rig, pose)
    V = np.hstack([rig.verts, np.ones((len(rig.verts), 1))])
    out = np.zeros((len(V), 2))
    for name, *_ in BONES:
        w = rig.weights[:, IDX[name]]
        nz = w > 1e-4
        if nz.any():
            out[nz] += w[nz, None] * (V[nz] @ T[name].T)[:, :2]
    return out.astype(np.float32), T


def joint_pos(rig, T, joint):
    for name, a, b, parent in BONES:
        if b == joint:
            p = rig.joints[b]
            return (T[name] @ np.array([p[0], p[1], 1.0]))[:2]
    p = rig.joints[joint]
    return (T['root'] @ np.array([p[0], p[1], 1.0]))[:2]


def abs_angle(rig, bone):
    for name, a, b, parent in BONES:
        if name == bone:
            d = rig.joints[b] - rig.joints[a]
            return math.atan2(d[1], d[0])


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def leg_len(rig):
    J = rig.joints
    return float(np.linalg.norm(J['l_hip'] - J['l_knee']) + np.linalg.norm(J['l_knee'] - J['l_ankle']))


# ------------------------------------------------------------------ motion library
def idle(t, rig, amount=1.0):
    br = math.sin(2 * math.pi * t / 4.2)
    return dict(spine=0.008 * br * amount, head=0.012 * math.sin(2 * math.pi * t / 5.3 + 1) * amount,
                l_upper_arm=0.01 * br * amount, r_upper_arm=-0.01 * br * amount, root_dy=-0.6 * br * amount)


def walk(t, rig, speed=1.0, stride=1.0, direction=None):
    f = rig.facing if direction is None else direction
    P = 1.1 / speed
    ph = 2 * math.pi * t / P
    s, c = math.sin(ph), math.cos(ph)
    LL = leg_len(rig)
    if rig.frontal:
        k_l, k_r = max(0, c), max(0, -c)
        return dict(l_thigh_len=1 - 0.08 * k_l, r_thigh_len=1 - 0.08 * k_r, l_shin_len=1 - 0.2 * k_l, r_shin_len=1 - 0.2 * k_r,
                    l_thigh=0.05 * k_l, r_thigh=-0.05 * k_r, root_rot=0.025 * s, root_dy=-LL * 0.025 * abs(math.cos(ph)),
                    l_upper_arm=0.1 * s, r_upper_arm=0.1 * s, l_upper_arm_len=1 - 0.08 * max(0, s), r_upper_arm_len=1 - 0.08 * max(0, -s),
                    spine=-0.02 * s, head=0.02 * s, root_scale=1 + 0.022 * speed * stride * t)
    A = 0.36 * stride
    return dict(l_thigh=-f * A * s, r_thigh=f * A * s,
                l_shin=f * 0.7 * max(0, c) ** 1.4, r_shin=f * 0.7 * max(0, -c) ** 1.4,
                l_foot=-f * 0.25 * max(0, -s), r_foot=-f * 0.25 * max(0, s),
                l_upper_arm=f * 0.32 * s * stride, r_upper_arm=-f * 0.32 * s * stride,
                l_forearm=-f * (0.18 + 0.15 * max(0, -s)), r_forearm=-f * (0.18 + 0.15 * max(0, s)),
                spine=-f * 0.035, head=f * 0.02 * math.cos(2 * ph),
                root_dy=-LL * 0.035 * math.cos(2 * ph), root_dx=f * 1.35 * LL * stride / P * t)


def run(t, rig, speed=1.0, stride=1.0, direction=None):
    f = rig.facing if direction is None else direction
    P = 0.62 / speed
    ph = 2 * math.pi * t / P
    s, c = math.sin(ph), math.cos(ph)
    LL = leg_len(rig)
    A = 0.62 * stride
    return dict(l_thigh=-f * (A * s + 0.12), r_thigh=f * (A * s - 0.12),
                l_shin=f * 1.3 * max(0, c) ** 1.2 + f * 0.2, r_shin=f * 1.3 * max(0, -c) ** 1.2 + f * 0.2,
                l_upper_arm=f * 0.7 * s, r_upper_arm=-f * 0.7 * s, l_forearm=-f * 1.25, r_forearm=-f * 1.25,
                spine=-f * 0.16, head=f * 0.1, root_rot=0.0,
                root_dy=-LL * 0.09 * abs(math.sin(ph)), root_dx=f * 2.6 * LL * stride / P * t)


def aim(rig, bone, target_abs, parent_delta=0.0):
    """Local delta that points a bone at an absolute screen angle."""
    return wrap(target_abs - abs_angle(rig, bone) - parent_delta)


def raise_arm(t, rig, side='r', height=1.0):
    """Lift an arm up and slightly forward (a signal, a salute)."""
    f = rig.facing
    up = -math.pi / 2 - f * 0.35 * (1 - height) - (1 - height) * 0.6 * f
    du = aim(rig, side + '_upper_arm', up)
    df = aim(rig, side + '_forearm', up - f * 0.15, du)
    return {side + '_upper_arm': du, side + '_forearm': df}


def point(t, rig, side='r', angle=0.0):
    f = rig.facing
    target = (0 if f > 0 else math.pi) + angle
    du = aim(rig, side + '_upper_arm', target)
    return {side + '_upper_arm': du, side + '_forearm': aim(rig, side + '_forearm', target, du)}


def look(t, rig, angle=0.0):
    return dict(head=angle)


def nod(t, rig, times=1):
    return dict(head=0.07 * math.sin(math.pi * min(1, t * 2.2 / times) * times * 2))


def crouch(t, rig, depth=0.5):
    f = rig.facing
    LL = leg_len(rig)
    return dict(l_thigh=-f * 0.5 * depth, r_thigh=-f * 0.45 * depth, l_shin=f * 1.0 * depth, r_shin=f * 0.9 * depth,
                spine=-f * 0.25 * depth, root_dy=LL * 0.22 * depth)


MOTIONS = dict(idle=idle, walk=walk, run=run, raise_arm=raise_arm, point=point, look=look, nod=nod, crouch=crouch)


class Clip:
    def __init__(self, name, t0, t1=None, fade=0.25, hold_root=True, **params):
        self.fn = MOTIONS[name]
        self.name, self.t0, self.t1, self.fade, self.params, self.hold_root = name, t0, t1, fade, params, hold_root

    def weight(self, t):
        if t < self.t0:
            return 0.0
        w = min(1.0, (t - self.t0) / self.fade) if self.fade > 0 else 1.0
        if self.t1 is not None and t > self.t1 - self.fade:
            w = min(w, max(0.0, (self.t1 - t) / self.fade)) if self.fade > 0 else float(t <= self.t1)
        return w * w * (3 - 2 * w)


def evaluate(clips, rig, t):
    pose = {}
    for c in clips:
        w = c.weight(t)
        lt = t - c.t0
        if w > 0:
            p = c.fn(lt, rig, **c.params)
            for k, v in p.items():
                if k == 'root_dx':
                    continue
                if k.endswith('_len') or k == 'root_scale':
                    pose[k] = pose.get(k, 1.0) * (1 + (v - 1) * w)
                else:
                    pose[k] = pose.get(k, 0.0) + v * w
        # travel persists after a walk/run ends
        if t >= c.t0 and c.name in ('walk', 'run'):
            te = min(t, c.t1) if c.t1 is not None else t
            pose['root_dx'] = pose.get('root_dx', 0.0) + c.fn(te - c.t0, rig, **c.params).get('root_dx', 0.0)
            if c.t1 is not None and t > c.t1 and 'root_scale' in c.fn(te - c.t0, rig, **c.params):
                pose['root_scale'] = pose.get('root_scale', 1.0) * c.fn(te - c.t0, rig, **c.params)['root_scale']
    return pose
