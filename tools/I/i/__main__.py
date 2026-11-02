"""-I- command line.
    python -m i rig IMAGE [--debug OUT.png]     build (and show) a rig
    python -m i run SCRIPT.i -o OUT.mp4         render a -I- script
"""
import argparse
from .rig import Rig
from .scene import Film


def main():
    ap = argparse.ArgumentParser(prog='-I-')
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('rig'); r.add_argument('image'); r.add_argument('--debug'); r.add_argument('--save')
    u = sub.add_parser('run'); u.add_argument('script'); u.add_argument('-o', '--out', default='out.mp4')
    a = ap.parse_args()
    if a.cmd == 'rig':
        rig = Rig.build(a.image)
        print(f'-I- rig: {len(rig.verts)} vertices, {len(rig.tris)} triangles, facing {"right" if rig.facing > 0 else "left"}, '
              f'{"frontal" if rig.frontal else "profile"}, face: {"yes" if rig.face is not None else "no"}')
        if a.debug:
            rig.debug(a.debug)
        if a.save:
            rig.save(a.save)
    else:
        print(Film(a.script).render(a.out))


if __name__ == '__main__':
    main()
