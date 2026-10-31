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

DUR=52.0
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
fr=lambda x: x/30.0
# hook
add(piano(73.42,3),0.1,0.8); add(pad([146.83,174.61,220],3.5,0.2),0)
# E1 exposition: gentle piano waltz-ish motif
mot=[293.66,349.23,440.0,349.23,392.0,329.63,293.66,261.63]
for k,f in enumerate(mot): add(piano(f,1.4,0.5),fr(105)+0.2+k*0.55,0.55,(-1)**k*0.3)
add(pad([146.83,220,293.66],5.0,0.25),fr(105))
# E2 inciting: poster slap
add(impact(2.5,0.7),fr(255+20)); add(pad([155.56,233.08,311.13],4.5,0.25),fr(255))
t=fr(255+40)
while t<fr(390): add(tick(True),t,0.25,0.2); t+=0.5
# E3 development: accelerating ticks + rising bass
t=fr(390); 
while t<fr(570):
    p=(t-fr(390))/6.0; add(tick(int(t*3)%2==0),t,0.25+0.3*p,0.2); add(sub(55+40*p,0.25),t,0.25+0.2*p); t+=0.45-0.3*min(1,p)
rn=int(2.0*SR); rt=np.arange(rn)/SR/2.0; x=rng.standard_normal(rn); y=np.empty(rn); s=0.0
for i in range(rn): s+=(0.01+0.4*rt[i]**2)*(x[i]-s); y[i]=s
add(y*rt**2*0.9,fr(570)-2.0,0.7)
# E4 climax: cut to silence, curtain swoosh, heartbeats
add(impact(2.0,0.5),fr(570)); 
hb=fr(570+40)
while hb<fr(735):
    add(sub(48,0.18),hb,0.9); add(sub(44,0.16),hb+0.22,0.6); hb+=0.733
# E5 resolution: warm pad + lead melody (the song)
add(impact(3.0,0.6),fr(735)); add(pad([174.61,220,261.63,349.23],5.5,0.4),fr(735))
def lead(f,len_):
    n=int(len_*SR); t=np.arange(n)/SR; vib=1+0.006*np.sin(2*np.pi*5.5*t)*np.minimum(1,t/0.3)
    ph=2*np.pi*np.cumsum(f*vib)/SR
    x=np.sin(ph)+0.3*np.sin(2*ph)+0.12*np.sin(3*ph)
    return x*np.minimum(1,t/0.08)*np.minimum(1,(len_-t)/0.15)*0.22
song=[(523.25,0.6),(587.33,0.3),(659.25,0.9),(587.33,0.3),(523.25,0.6),(440.0,0.9),(523.25,0.6),(659.25,0.6),(698.46,1.2)]
t=fr(735)+0.3
for f,d in song: add(lead(f,d),t,0.8,0.1); t+=d
# rewind: tape chirps
t=fr(900)
for k in range(10):
    n=int(0.2*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*np.cumsum(2400-9000*tt)/SR)*np.exp(-tt*8)*0.25,t,0.6,(-1)**k*0.3); t+=0.24
# recap: one hit per term
for k in range(5):
    tt=fr(975+k*66); add(impact(1.5,0.45 if k!=3 else 0.9),tt); add(piano([293.66,349.23,440.0,587.33,523.25][k],1.8,0.8),tt,0.8)
    add(sub(73.42,2.0),tt,0.4)
# summary + end
add(pad([146.83,220,293.66,349.23],4.0,0.4),fr(1305)); add(impact(3.0,0.6),fr(1425)); add(pad([146.83,220,293.66,369.99],4.0,0.45),fr(1425)); add(piano(587.33,3.5,0.6),fr(1425)+0.2,0.7)
mix=np.stack([L,R],1); mix=np.tanh(mix*1.1); mix/=np.max(np.abs(mix))*1.1
with wave.open('/tmp/dr/music/story_bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok')
