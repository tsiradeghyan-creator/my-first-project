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

DUR=45.5
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
add(piano(73.42,4),0.2,0.9); add(pad([146.83,174.61,220],5.0,0.25),0)
for k,f in enumerate([293.66,349.23,440.0]): add(piano(f,1.6,0.5),0.6+k*0.9,0.5,(-1)**k*0.3)
add(impact(3.0,0.6),5.0); add(pad([146.83,220,293.66],6.5,0.3),5.0)
t=5.0
while t<11.5: add(tick(True),t,0.25,0.2); t+=0.5
# conflict collision ~13.8s
rn=int(2.3*SR); rt=np.arange(rn)/SR/2.3; x=rng.standard_normal(rn); y=np.empty(rn); s=0.0
for i in range(rn): s+=(0.01+0.3*rt[i]**2)*(x[i]-s); y[i]=s
add(y*rt**2,11.5,0.6); add(impact(3.0,0.9),13.83)
# five stages, 3.6s each from 17.0
notes=[(146.83,220),(130.81,196),(116.54,174.61),(110.0,164.81),(174.61,261.63)]
t=17.0
while t<35.0:
    p=(t-17.0)/18.0; add(tick(int(t*2)%2==0),t,0.2+0.25*min(1,p*1.4),0.2); t+=0.5-0.2*min(1,p*1.3) if t<30.8 else 0.5
for i,(a,b) in enumerate(notes):
    bt=17.0+i*3.6
    add(piano(a,3.4),bt,1.0,-0.2); add(piano(b,3.0,0.7),bt+0.4,0.8,0.2); add(sub(a/2,3.4),bt,0.5)
    if i==3: add(impact(3.5,1.0),bt+1.2)
# climax riser before stage 4 peak
rn=int(1.8*SR); rt=np.arange(rn)/SR/1.8; x=rng.standard_normal(rn); y=np.empty(rn); s=0.0
for i in range(rn): s+=(0.01+0.4*rt[i]**2)*(x[i]-s); y[i]=s
add(y*rt**2*1.1,27.8+1.2-1.8,0.7)
add(pad([174.61,220,261.63,349.23],3.6,0.35),31.4)
# flat: monotone single note pulses, no harmony
t=35.0
while t<39.5: add(sub(110,0.3),t,0.35); add(tick(False),t,0.18); t+=0.75
add(impact(3.5,0.7),39.5); add(pad([146.83,220,293.66,369.99],5.5,0.45),39.5); add(piano(587.33,4,0.6),41.7,0.7)
mix=np.stack([L,R],1); mix=np.tanh(mix*1.1); mix/=np.max(np.abs(mix))*1.1
with wave.open('/tmp/dr/music/lesson_bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok')
