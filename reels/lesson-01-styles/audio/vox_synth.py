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

import json
DUR=56.0
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
fr=lambda x: x/30.0
G={'hook':0,'etym':195,'contest':405,'masks':570,'poet':675,'temple':840,'peri':945,'cath':1110,'today':1245,'arch':1410,'logo':1575}
starts=[0,195,405,570,675,840,945,1110,1245,1410]
def rhodes(f,len_,g=1.0):
    n=int(len_*SR); t=np.arange(n)/SR
    x=np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t)*np.exp(-t*3)+0.1*np.sin(2*np.pi*3*f*t)*np.exp(-t*6)
    trem=1+0.15*np.sin(2*np.pi*4.5*t)
    return x*trem*np.exp(-t*0.9)*(1-np.exp(-t*300))*g*0.25
def softkick(): 
    n=int(0.35*SR); t=np.arange(n)/SR
    return np.sin(2*np.pi*np.cumsum(50+80*np.exp(-t*35))/SR)*np.exp(-t*9)*0.9
def snare():
    n=int(0.25*SR); t=np.arange(n)/SR
    return (lp(rng.standard_normal(n),0.6)*np.exp(-t*18)*0.5+np.sin(2*np.pi*190*t)*np.exp(-t*25)*0.3)
def hat():
    n=int(0.05*SR); t=np.arange(n)/SR; x=rng.standard_normal(n); return (x-lp(x,0.3))*np.exp(-t*90)*0.25
def paper_slap():
    n=int(0.18*SR); t=np.arange(n)/SR
    return (lp(rng.standard_normal(n),0.35)*np.exp(-t*30)*0.7+np.sin(2*np.pi*90*t)*np.exp(-t*40)*0.5)
def whoosh(len_=0.5):
    n=int(len_*SR); t=np.arange(n)/SR; x=rng.standard_normal(n); out=np.empty(n); s=0.0
    for i in range(n):
        a=0.02+0.3*np.sin(np.pi*t[i]/len_); s+=a*(x[i]-s); out[i]=s
    return out*np.sin(np.pi*t/len_)**2*0.9
# vinyl crackle
cr=np.zeros(N)
for k in range(int(DUR*14)):
    i=int(rng.uniform(0,N-200)); cr[i:i+40]+=rng.standard_normal(40)*np.exp(-np.arange(40)/6)*rng.uniform(0.05,0.25)
add(lp(rng.standard_normal(N),0.05)*0.03+cr,0,0.5)
# lo-fi groove 84 bpm with Dm9 - Gm9 - Bbmaj7 - A7 chords
bpm=84; beat=60/bpm; bar=4*beat
chords=[[146.83,174.61,220,261.63,329.63],[196,233.08,293.66,349.23,440],[233.08,293.66,349.23,440],[220,277.18,329.63,392]]
t=0.0; b=0
while t<fr(G['logo'])+bar:
    ch=chords[b%4]
    for k,f in enumerate(ch): add(rhodes(f,bar*1.1,0.9),t+k*0.012,0.6,(-1)**k*0.2)
    for q in range(4):
        tt=t+q*beat
        if q in (0,2) or (q==3 and b%2): add(softkick(),tt+(0.0 if q!=3 else beat/2),0.55)
        if q in (1,3): add(snare(),tt+0.02,0.35,0.1)
        for e in range(2): add(hat(),tt+e*beat/2+(0.03 if e else 0),0.5,0.3)
    add(rhodes(ch[0]/2,bar,1.2),t,0.5)
    t+=bar; b+=1
# camera whooshes + paper slaps per cluster
slap_offsets=[0,6,12,18,30,40,50,60,70,96,110]
for s_ in starts:
    add(whoosh(0.5),max(0,fr(s_)-0.35),0.5)
    for o in slap_offsets: add(paper_slap(),fr(s_+o),0.35,rng.uniform(-0.4,0.4))
# final zoom-out
add(whoosh(1.2),fr(G['logo'])-0.3,0.7); add(paper_slap(),fr(G['logo']+26),0.9)
add(pad([146.83,220,293.66,349.23],3.0,0.4),fr(G['logo']))
mix=np.stack([L,R],1); mix=np.tanh(mix*1.05); mix/=np.max(np.abs(mix))*1.1
with wave.open('/tmp/dr/music/vox_bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok')
