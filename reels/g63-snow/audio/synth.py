import numpy as np, wave
SR=44100; DUR=31.2+1.5
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
BEAT=0.6; T0=1.8; DROP=23.4; BREAK=20.4; END=29.4
def add(sig,t,gain=1.0,pan=0.0):
    i=int(t*SR); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*gain*(1-max(0,pan)); R[i:i+n]+=sig[:n]*gain*(1+min(0,pan))
def env(n,a,d):  # attack/decay exp
    t=np.arange(n)/SR; e=1-np.exp(-t/max(a,1e-4)); return e*np.exp(-t/d)
def kick(len_=0.5,f0=140,f1=42):
    n=int(len_*SR); t=np.arange(n)/SR
    f=f1+(f0-f1)*np.exp(-t*30); ph=2*np.pi*np.cumsum(f)/SR
    return np.tanh(1.6*np.sin(ph)*np.exp(-t*7))
def b808(note_hz,len_,glide_from=None):
    n=int(len_*SR); t=np.arange(n)/SR
    f=np.full(n,note_hz)
    if glide_from: f=note_hz+(glide_from-note_hz)*np.exp(-t*12)
    ph=2*np.pi*np.cumsum(f)/SR
    return np.tanh(2.2*np.sin(ph))*np.exp(-t*1.4)*(1-np.exp(-t*200))
def noise(n): return rng.standard_normal(n)
def hp(x,a=0.9):  # simple one-pole highpass
    y=np.zeros_like(x); prev=0; px=0
    for i in range(len(x)): y[i]=a*(prev+x[i]-px); prev=y[i]; px=x[i]
    return y
def lp(x,a):
    y=np.zeros_like(x); s=0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
HAT=hp(noise(int(0.06*SR)),0.97)*env(int(0.06*SR),0.0005,0.012)
OHAT=hp(noise(int(0.25*SR)),0.97)*env(int(0.25*SR),0.001,0.07)
def clap():
    n=int(0.35*SR); x=hp(noise(n),0.85); e=np.zeros(n); t=np.arange(n)/SR
    for o in (0,0.011,0.022): e+=np.where(t>=o,np.exp(-(t-o)/0.012),0)
    e+=np.where(t>=0.03,np.exp(-(t-0.03)/0.12),0)*0.6
    return x*e*0.6
CLAP=clap(); KICK=kick()
def impact(len_=3.0):
    n=int(len_*SR); t=np.arange(n)/SR
    boom=np.sin(2*np.pi*np.cumsum(30+70*np.exp(-t*8))/SR)*np.exp(-t*1.2)
    crack=lp(noise(n),0.25)*np.exp(-t*6)*0.8
    tail=lp(noise(n),0.05)*np.exp(-t*0.9)*0.5
    return np.tanh(1.5*(boom*1.2+crack+tail))
def whoosh(len_=0.7,up=True):
    n=int(len_*SR); t=np.arange(n)/SR; x=noise(n)
    out=np.zeros(n); s=0
    for i in range(n):
        p=t[i]/len_; a=0.02+0.4*(p if up else 1-p)
        s+=a*(x[i]-s); out[i]=s
    shape=np.sin(np.pi*t/len_)**2
    return out*shape*1.2
# chords: Am  F  Dm  E  (dark luxury minor)
A=110.0
prog=[[220.0,261.63,329.63],[174.61,220.0,261.63],[146.83,174.61,220.0],[164.81,207.65,246.94]]
roots=[55.0,43.65,36.71,41.2]
def pad(freqs,len_,bright=0.3):
    n=int(len_*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for f in freqs:
        for det in (-0.006,0,0.006):
            ph=2*np.pi*f*(1+det)*t
            x+=np.sin(ph)+bright*np.sin(2*ph)/2+bright*0.5*np.sin(3*ph)/3
    e=np.minimum(1,t/0.4)*np.minimum(1,(len_-t)/0.5)
    return x*e/len(freqs)/3
def pluck(f,len_=0.5):
    n=int(len_*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+0.4*np.sin(4*np.pi*f*t))*np.exp(-t*6)
BAR=4*BEAT
# intro drone + hook impact
add(pad([110,164.81,220],T0+1.0,0.1),0,0.25)
add(impact(3.5),0.8,0.9)
add(whoosh(1.0,True),T0-1.0,0.5)
# groove
t=T0; b=0
while t<END-0.01:
    bar=int((t-T0)//BAR); beat=int(round((t-T0)/BEAT))%4; ci=bar%4
    in_break = BREAK<=t<DROP
    post = t>=DROP
    if beat==0: add(pad(prog[ci],BAR,0.45 if post else 0.3),t,0.32 if not in_break else 0.4,0)
    if not in_break:
        if beat in (0,) or (beat==2 and bar%2==1): add(KICK,t,0.8)
        if beat==2 and bar%2==0: add(KICK,t+BEAT*0.5,0.7)
        if beat in (1,3): add(CLAP,t,0.55,0.05)
        if beat==0: add(b808(roots[ci],BAR*0.95, roots[ci]*1.5 if post and bar%2==0 else None),t,0.36)
        for k in range(4):  # 16th hats with swing + velocity
            ht=t+k*BEAT/4+(0.018 if k%2 else 0)
            v=0.22 if k%2==0 else 0.12
            if post and k==3 and beat==3: 
                for r in range(3): add(HAT,ht+r*BEAT/12,0.12,0.3)
            else: add(HAT,ht,v,0.3 if k%2 else -0.2)
        if beat==3 and bar%2==1: add(OHAT,t+BEAT/2,0.15,0.3)
        # arp plucks (luxury bells) post-drop and quietly before
        f=prog[ci][(beat+bar)%3]*2
        add(pluck(f),t+BEAT/2,0.09 if post else 0.05,-0.4 if beat%2 else 0.4)
    t+=BEAT
# breakdown riser + snare roll
rn=int((DROP-BREAK)*SR); rt=np.arange(rn)/SR; p=rt/(DROP-BREAK)
riser=np.zeros(rn); s=0; x=noise(rn)
for i in range(rn):
    a=0.01+0.5*p[i]**2; s+=a*(x[i]-s); riser[i]=s
riser*=p**2*1.4
tone=np.sin(2*np.pi*np.cumsum(200+700*p**2)/SR)*p**3*0.25
add(riser+tone,BREAK,0.8)
# snare roll accelerating in last bar
rt0=DROP-BAR; k=0
while True:
    frac=k/32; tt=rt0+BAR*(1-(1-frac)**1.0)*1.0
    if tt>=DROP-0.02 or k>64: break
    add(CLAP,tt,0.15+0.35*(tt-rt0)/BAR,0); k+=1 if (tt-rt0)<BAR/2 else 2
    k+=0
    if k>40: break
add(impact(4.0),DROP,1.1)
add(KICK,DROP,1.0)
# transition whooshes at cuts
for c in (3.6,6.0,11.4,17.4,25.2):
    add(whoosh(0.6,True),c-0.5,0.35,0.0)
# ending: final hit + ringing chord, loop-friendly
add(impact(3.0),END,0.7)
add(pad([220,261.63,329.63,440],3.0,0.2),END,0.35)
mix=np.stack([L,R],1)
# soft clip + normalize
mix=np.tanh(mix*0.9); mix/=np.max(np.abs(mix))*1.12
with wave.open('/tmp/g63/music/bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok', DUR)
