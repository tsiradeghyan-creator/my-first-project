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
# beat starts (s) -> piano motif notes (D minor, rising per beat)
beats=[(5.0,[146.83,220.0]),(8.6,[130.81,196.0]),(12.4,[116.54,174.61]),(16.5,[110.0,164.81])]
# 0-5: hook — single low note + pad
add(piano(73.42,4),0.3,0.9); add(pad([146.83,174.61,220],5.0,0.25),0)
# ticking clock 5.0 -> 20.2, speeding up with stakes
t=5.0
while t<20.2:
    p=(t-5.0)/15.2; step=0.5-0.25*p**1.5
    add(tick(int((t-5)/step)%2==0),t,0.35+0.3*p,0.2); t+=step
for bt,(a,b) in beats:
    add(piano(a,3.5),bt,1.0,-0.2); add(piano(b,3.0,0.7),bt+0.5,0.8,0.2); add(sub(a/2,3.4),bt,0.6)
# riser into the turn
HIT=20.2; rn=int(3.0*SR); rt=np.arange(rn)/SR/3.0
x=rng.standard_normal(rn); y=np.empty(rn); s=0.0
for i in range(rn): s+=(0.01+0.4*rt[i]**2)*(x[i]-s); y[i]=s
add(y*rt**2*1.2+np.sin(2*np.pi*np.cumsum(150+600*rt**2)/SR)*rt**3*0.2,HIT-3.0,0.8)
add(impact(4.0,1.0),HIT)
# 20.9-26.0 change: warm resolve, F major -> C
add(pad([174.61,220,261.63],2.6,0.35),20.9); add(pad([130.81,196,261.63,329.63],2.8,0.35),23.3)
for k,f in enumerate([349.23,440,523.25,659.25,523.25,440]): add(piano(f,1.5,0.5),21.0+k*0.8,0.6,(-1)**k*0.3)
# 26.0-29.4: silence (graphics stripped) — only faint room tone
add(lp(rng.standard_normal(int(3.4*SR)),0.02)*0.15,26.0)
# 29.4 story: everything back
add(impact(3.0,0.8),29.4); add(pad([146.83,220,293.66,349.23],4.0,0.4),29.4)
# credentials 31.4-37.8: pulse + motif
t=31.4; k=0
while t<37.8:
    add(sub(73.42,0.45),t,0.5); add(tick(True),t+0.25,0.2,0.3)
    if k%2==0: add(piano([293.66,349.23,440,523.25][(k//2)%4],1.2,0.5),t,0.6,-0.3)
    t+=0.5; k+=1
# logo
add(impact(4.0,0.7),37.8); add(pad([146.83,220,293.66,369.99],4.5,0.45),37.8); add(piano(587.33,4,0.6),37.9,0.7)
mix=np.stack([L,R],1); mix=np.tanh(mix*1.1); mix/=np.max(np.abs(mix))*1.1
with wave.open('/tmp/dr/music/bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
