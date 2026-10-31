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
def lyre(f,len_=2.0,g=1.0):
    n=int(len_*SR); p=max(2,int(SR/f)); buf=rng.uniform(-1,1,p); out=np.empty(n)
    for i in range(n):
        out[i]=buf[i%p]; buf[i%p]=0.996*0.5*(buf[i%p]+buf[(i+1)%p])
    return lp(out,0.5)*g*0.6
def drum(len_=0.6,f0=110):
    n=int(len_*SR); t=np.arange(n)/SR
    body=np.sin(2*np.pi*np.cumsum(f0*0.55+f0*np.exp(-t*20))/SR)*np.exp(-t*6)
    skin=lp(rng.standard_normal(n),0.15)*np.exp(-t*25)*0.5
    return np.tanh(1.5*(body+skin))*0.8
D=146.83  # D phrygian: D Eb F G A Bb C
scale=[D, D*16/15, D*6/5, D*4/3, D*3/2, D*8/5, D*9/5, D*2]
# drone throughout
add(pad([73.42,110.0,146.83],DUR-1,0.35),0)
# lyre arpeggios + frame drum pulse (~92 bpm)
beat=60/92; t=0.0; k=0
while t<fr(1575):
    sec=t
    climax = fr(945)<=sec<fr(1245)
    if not (fr(1110)<=sec<fr(1245) and k%2): add(lyre(scale[[0,2,4,7,4,2,1,3][k%8]],1.8,0.55),t,0.7,(-1)**k*0.35)
    if k%4==0: add(drum(0.7,90),t,0.55 if not climax else 0.8)
    if k%4==2: add(drum(0.4,140),t,0.3)
    if climax and k%2==1: add(drum(0.3,180),t,0.25)
    t+=beat/2 if fr(945)<=sec<fr(1110) else beat; k+=1
# scene hits
for s_ in [195,405,570,675,840,945,1110,1245,1410]:
    add(impact(2.2,0.45),fr(s_)); 
add(impact(3.0,0.8),fr(945+95))  # the turn
# catharsis swell
add(pad([146.83,220,293.66,349.23,440],4.5,0.5),fr(1110))
# final
add(impact(3.5,0.7),fr(1575)); add(pad([146.83,220,293.66,369.99],3.0,0.5),fr(1575))
for i,f in enumerate([D*2,D*3/2*2/2*2,D*2*1.25,D*4]): add(lyre(f,2.5,0.6),fr(1575)+0.15*i,0.7)
mix=np.stack([L,R],1); mix=np.tanh(mix*1.05); mix/=np.max(np.abs(mix))*1.1
with wave.open('/tmp/dr/music/greece_bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok')
