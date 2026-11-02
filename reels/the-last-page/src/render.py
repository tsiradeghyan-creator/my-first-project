"""Render frames for one or more shots: python render.py <shot> [start end step] [--preview]"""
import sys, os, importlib, time, cv2
OUT = os.environ.get('FRAMES', '/tmp/claude-0/-home-user-my-first-project/b7ca98c6-d312-5f8a-a4c0-64c0a7cf67a7/scratchpad/frames')
STARTS = dict(shot1=0, shot2=168, shot3=336, shot4=432, shot5=600, shot6=768, shot7=936, shot8=1056, shot9=1248)

if __name__ == '__main__':
    name = sys.argv[1]
    mod = importlib.import_module(name)
    a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    b = int(sys.argv[3]) if len(sys.argv) > 3 else mod.N
    st = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    shot = mod.Shot()
    t1 = time.time()
    for f in range(a, b, st):
        fr = shot.frame(f)
        cv2.imwrite(f'{OUT}/{STARTS[name] + f:05d}.png', cv2.cvtColor(fr, cv2.COLOR_RGB2BGR))
    print(f'{name}: prep {t1 - t0:.1f}s, {len(range(a, b, st))} frames {time.time() - t1:.1f}s')
