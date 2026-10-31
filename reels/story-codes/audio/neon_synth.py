import numpy as np, wave
SR=44100; DUR=42.5; N=int(SR*DUR)
L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(3)
def add(sig,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(sig),N-i)
    if n>0:
        L[i:i+n]+=sig[:n]*g*(1-max(0,pan)); R[i:i+n]+=sig[:n]*g*(1+min(0,pan))
def lp(x,a):
    y=np.empty_like(x); s=0.0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
def piano(f,len_=2.5,vel=1.0):
    n=int(len_*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for k,amp in ((1,1),(2,0.45),(3,0.2),(4,0.12),(5,0.06)):
        x+=amp*np.sin(2*np.pi*f*k*t*(1+0.0004*k))*np.exp(-t*(1.2+k*0.7))
    return x*(1-np.exp(-t*400))*vel*0.35
def tick(hi=True):
    n=int(0.03*SR); t=np.arange(n)/SR
    return (rng.standard_normal(n)*0.4+np.sin(2*np.pi*(2400 if hi else 1700)*t))*np.exp(-t*260)*0.5
def sub(f,len_):
    n=int(len_*SR); t=np.arange(n)/SR
    return np.sin(2*np.pi*f*t)*np.minimum(1,t/0.3)*np.minimum(1,(len_-t)/0.4)*0.5
def impact(len_=3.0,g=1.0):
    n=int(len_*SR); t=np.arange(n)/SR
    boom=np.sin(2*np.pi*np.cumsum(28+80*np.exp(-t*9))/SR)*np.exp(-t*1.3)
    crack=lp(rng.standard_normal(n),0.3)*np.exp(-t*7)*0.7
    return np.tanh(1.4*(boom+crack))*g
def pad(fs,len_,g=0.2):
    n=int(len_*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for f in fs:
        for d in (-0.004,0,0.004): x+=np.sin(2*np.pi*f*(1+d)*t)+0.25*np.sin(4*np.pi*f*(1+d)*t)
    return x*np.minimum(1,t/0.8)*np.minimum(1,(len_-t)/1.0)/len(fs)/3*g

DUR=21.5
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
fr=lambda x: x/30.0
S={'hook':0,'title':45,'ponr':120,'ex':300,'rule':450,'cta':540}
bpm=140; beat=60/bpm
def k808(f=49,len_=0.9):
    n=int(len_*SR); t=np.arange(n)/SR
    ph=2*np.pi*np.cumsum(f+120*np.exp(-t*40))/SR
    return np.tanh(2.5*np.sin(ph))*np.exp(-t*2.2)*0.9
def clap():
    n=int(0.25*SR); t=np.arange(n)/SR; x=rng.standard_normal(n); x=x-lp(x,0.2)
    e=np.exp(-t*30)+0.5*np.exp(-np.maximum(0,t-0.012)*30)*(t>0.012)
    return x*e*0.5
def hat(o=False):
    n=int((0.18 if o else 0.04)*SR); t=np.arange(n)/SR; x=rng.standard_normal(n); x=x-lp(x,0.4)
    return x*np.exp(-t*(15 if o else 120))*0.22
def shimmer(len_=1.2):
    n=int(len_*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for f in [2093,2637,3136,3951,4699]: x+=np.sin(2*np.pi*f*t+rng.uniform(0,6))*np.exp(-t*(3+rng.uniform(0,3)))
    return x*0.06
def glass_hit():
    n=int(1.5*SR); t=np.arange(n)/SR
    x=lp(rng.standard_normal(n),0.6)*np.exp(-t*14)*0.8+np.sin(2*np.pi*np.cumsum(60+300*np.exp(-t*20))/SR)*np.exp(-t*5)*0.9
    return np.tanh(1.6*x)+np.concatenate([shimmer(1.5)[:n]])
def whoosh(len_=0.4):
    n=int(len_*SR); t=np.arange(n)/SR; x=rng.standard_normal(n); out=np.empty(n); s=0.0
    for i in range(n): s+=(0.02+0.5*(t[i]/len_)**2)*(x[i]-s); out[i]=s
    return out*(t/len_)**1.5*0.9
def bell(f,len_=0.6):
    n=int(len_*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*8))*np.exp(-t*5)*0.18
def pad2(fs,len_,g):
    n=int(len_*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for f in fs:
        for d in (-0.006,0,0.006):
            ph=2*np.pi*f*(1+d)*t; saw=sum(np.sin(h*ph)/h for h in range(1,6)); x+=saw
    return lp(x/len(fs)/3,0.05)*np.minimum(1,t/0.3)*np.minimum(1,(len_-t)/0.3)*g
# hook: silence-ish riser then GLASS HIT at frame 12
add(whoosh(0.4),0.0,0.6); add(glass_hit(),fr(12),1.0)
# beat from title on: Fm - Db - Ab - Eb (dark, catchy)
roots=[43.65,34.65,51.91,38.89]; chords=[[349.23,415.3,523.25],[277.18,349.23,415.3],[415.3,523.25,622.25],[311.13,392,466.16]]
t=fr(S['title']); b=0
bell_pat=[0,2,1,2,0,2,1,3]
while t<fr(630)-0.1:
    bar=b//8; step=b%8  # 8 eighth-notes per bar
    ci=bar%4; tt=t
    inbreak = fr(S['ponr']+80)<=tt<fr(S['ponr']+92)
    if not inbreak:
        if step in (0,3) or (step==6 and bar%2): add(k808(roots[ci]*1.0+0),tt,0.6)
        if step in (2,6): add(clap(),tt,0.55)
        add(hat(step==7),tt,0.6,0.3)
        if step%2==1: add(hat(),tt+beat/4,0.35,-0.3)
        add(bell(chords[ci][bell_pat[step]%3]*2),tt,0.45,(-1)**step*0.4)
    if step==0: add(pad2(chords[ci],beat*4+0.1,0.22),tt)
    t+=beat/2; b+=1
# section hits
for s_ in ['title','ponr','ex','rule','cta']:
    add(whoosh(0.35),max(0,fr(S[s_])-0.35),0.5); add(shimmer(1.0),fr(S[s_]),0.8)
# the break: riser + shatter
add(whoosh(1.4),fr(S['ponr']+92)-1.4,0.7); add(glass_hit(),fr(S['ponr']+92),1.1)
# chat bubble pops
for o in [20,60,100]:
    n=int(0.12*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*(900+600*np.exp(-tt*30))*tt)*np.exp(-tt*30)*0.4,fr(S['ex']+o),0.7)
# CTA button: bright chord
add(pad2([523.25,659.25,783.99],1.8,0.35),fr(S['cta']+14)); add(glass_hit(),fr(S['cta']+14),0.6)
mix=np.stack([L,R],1); mix=np.tanh(mix*1.2); mix/=np.max(np.abs(mix))*1.08
with wave.open('/tmp/dr/music/neon_bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok')
