import cv2, numpy as np, subprocess, sys, os
sys.path.insert(0,'/tmp/grade'); 
from grade import ref
src,dst,cutsf=sys.argv[1],sys.argv[2],sys.argv[3]
W,H,FPS=1280,720,int(sys.argv[4]) if len(sys.argv)>4 else 30
DUR=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)-0.05
cuts=[0]+[float(x) for x in open(cutsf)]+[1e9]
# per-shot plan: (ref, amount); shot index 0-based
plan={} if len(sys.argv)>4 else {0:None,1:("int",.5),2:("int",.5),13:None}
def shot_of(t):
    for i in range(len(cuts)-1):
        if cuts[i]<=t<cuts[i+1]: return i
def sample_stats(a,b):
    labs=[]
    for t in np.linspace(a+0.1,min(b,DUR)-0.1,5):
        r=subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",src,"-frames:v","1","-f","rawvideo","-pix_fmt","bgr24","-"],capture_output=True).stdout
        im=np.frombuffer(r,np.uint8).reshape(H,W,3).astype(np.float32)/255
        labs.append(cv2.cvtColor(im,cv2.COLOR_BGR2LAB).reshape(-1,3)[::7])
    p=np.concatenate(labs); return p.mean(0),p.std(0)+1e-3
st={}
for i in range(len(cuts)-2+1):
    if i>=14: break
    if plan.get(i,1) is not None: st[i]=sample_stats(cuts[i],cuts[i+1])
dec=subprocess.Popen(["ffmpeg","-v","error","-i",src,"-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",src,"-map","0:v","-map","1:a","-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-c:a","copy",dst],stdin=subprocess.PIPE)
n=0
while True:
    b=dec.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    i=shot_of(n/FPS); pl=plan.get(i,(os.environ.get("KREF","ext"),float(os.environ.get("KAMT",".8"))))
    if pl is None or i not in st: enc.stdin.write(b)
    else:
        kind,amt=pl; im=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32)/255
        lab=cv2.cvtColor(im,cv2.COLOR_BGR2LAB); m,s=st[i]; rm,rs=ref[kind]
        out=(lab-m)/s*rs+rm; w=np.array([amt,amt*.55,amt*.55],np.float32); out=lab*(1-w)+out*w
        out[...,0]=np.clip(out[...,0],0,100)
        bgr=np.clip(cv2.cvtColor(out,cv2.COLOR_LAB2BGR),0,1)*0.94+0.03
        enc.stdin.write((bgr*255+.5).astype(np.uint8).tobytes())
    n+=1
enc.stdin.close(); enc.wait(); print("frames",n)
