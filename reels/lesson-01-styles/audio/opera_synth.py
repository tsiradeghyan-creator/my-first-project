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

DUR=56.0
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
fr=lambda x: x/30.0
def strings(fs,len_,g=0.3):
    n=int(len_*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for f in fs:
        for d in (-0.003,0,0.003):
            vib=1+0.004*np.sin(2*np.pi*5*t+d*1000)
            ph=2*np.pi*np.cumsum(f*(1+d)*vib)/SR
            saw=np.zeros(n)
            for h in range(1,8): saw+=np.sin(h*ph)/h
            x+=saw
    x=lp(x/len(fs)/3,0.08)
    return x*np.minimum(1,t/0.6)*np.minimum(1,(len_-t)/0.8)*g
def pizz(f,g=1.0):
    n=int(0.6*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+0.4*np.sin(4*np.pi*f*t))*np.exp(-t*9)*g*0.4
def timp(len_=1.2,f=65):
    n=int(len_*SR); t=np.arange(n)/SR
    return np.tanh(1.3*(np.sin(2*np.pi*f*t)*np.exp(-t*2.5)+lp(rng.standard_normal(n),0.1)*np.exp(-t*12)*0.4))*0.9
def harp_gliss(t0,up=True):
    notes=[146.83,164.81,174.61,196,220,246.94,261.63,293.66,329.63,349.23,392,440,493.88,523.25,587.33]
    if not up: notes=notes[::-1]
    for i,f in enumerate(notes):
        n=int(1.5*SR); tt=np.arange(n)/SR
        add((np.sin(2*np.pi*f*tt)+0.3*np.sin(4*np.pi*f*tt))*np.exp(-tt*3)*0.18,t0+i*0.035,0.8,(i/15-0.5))
# chord plan in D minor, one chord per act
prog=[[146.83,174.61,220],[116.54,146.83,174.61],[130.81,164.81,196],[110,138.59,164.81],[146.83,174.61,220],[174.61,220,261.63],[116.54,146.83,174.61],[110,138.59,164.81],[146.83,185,220],[146.83,174.61,220]]
starts=[0,195,405,570,675,840,945,1110,1245,1410]
for i,s_ in enumerate(starts):
    e=(starts[i+1] if i+1<len(starts) else 1575)
    add(strings(prog[i],fr(e-s_)+0.6,0.35 if i!=7 else 0.5),fr(s_))
    add(strings([prog[i][0]/2],fr(e-s_)+0.6,0.3),fr(s_))
    # pizzicato walking pattern
    t=fr(s_); k=0
    while t<fr(e)-0.2:
        add(pizz(prog[i][k%3]*2,0.8),t,0.6,(-1)**k*0.3); t+=0.36 if i!=6 else 0.24; k+=1
# curtains: timpani roll + harp glissando on reopen
for c in [195,405,675,945,1245]:
    for r in range(8): add(timp(0.4,70),fr(c)-0.45+r*0.05,0.25)
    add(timp(1.6,62),fr(c),0.8); harp_gliss(fr(c)+0.1)
add(timp(2.0,55),fr(945+95),1.0)
# curtain call: big chord + applause
add(strings([146.83,220,293.66,369.99,440],4.0,0.55),fr(1575)); add(timp(2.0,60),fr(1575),0.9)
n=int(3.0*SR); ap=np.zeros(n)
for k in range(1400):
    i=int(rng.uniform(0,n-800)); ap[i:i+600]+=lp(rng.standard_normal(600),0.5)*np.exp(-np.arange(600)/80)*rng.uniform(0.2,1)
add(ap*np.minimum(1,np.arange(n)/SR/0.8)*0.12,fr(1575)+0.4,0.7)
mix=np.stack([L,R],1); mix=np.tanh(mix*1.05); mix/=np.max(np.abs(mix))*1.1
with wave.open('/tmp/dr/music/opera_bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok')
