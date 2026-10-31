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

fr=lambda x: x/30.0
SC={'hook':0,'title':60,'ponr':130,'ex':330,'rule':450,'cta':530}
DUR=20.5
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
def save(name,drive=1.0):
    global L,R
    mix=np.stack([L,R],1); mix=np.tanh(mix*drive); mix/=np.max(np.abs(mix))*1.1
    with wave.open(name,'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
def marimba(f,len_=0.8,g=1.0):
    n=int(len_*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+0.25*np.sin(2*np.pi*f*4*t)*np.exp(-t*20))*np.exp(-t*6)*g*0.35
def tock(f=900):
    n=int(0.08*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*np.exp(-t*60)*0.5
def thud():
    n=int(0.5*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*np.cumsum(55+90*np.exp(-t*30))/SR)*np.exp(-t*7)*0.9
def whoosh(len_=0.6):
    n=int(len_*SR); t=np.arange(n)/SR; x=rng.standard_normal(n); out=np.empty(n); s=0.0
    for i in range(n): s+=(0.02+0.3*np.sin(np.pi*t[i]/len_))*(x[i]-s); out[i]=s
    return out*np.sin(np.pi*t/len_)**2*0.7

def dkick():
    n=int(0.45*SR); t=np.arange(n)/SR; return np.tanh(4*np.sin(2*np.pi*np.cumsum(45+160*np.exp(-t*35))/SR)*np.exp(-t*6))*0.8
def noiseburst(len_=0.12,g=0.5):
    n=int(len_*SR); t=np.arange(n)/SR; x=rng.standard_normal(n); return np.sign(x)*np.abs(x)**0.5*np.exp(-t*25)*g
def drone(len_):
    n=int(len_*SR); t=np.arange(n)/SR
    return lp(np.sign(np.sin(2*np.pi*55*t))*0.5+np.sin(2*np.pi*55.4*t),0.03)*0.35
bpm=96; beat=60/bpm
add(drone(DUR-0.2),0,0.6)
# hook: op-art spin noise, then hit
add(whoosh(0.45),0,0.7); add(dkick(),fr(14),1.0); add(noiseburst(0.4,0.8),fr(14),0.8)
t=fr(14)+beat; k=0
while t<DUR-0.4:
    if k%4 in (0,3): add(dkick(),t,0.7)
    if k%4==2: add(noiseburst(0.15,0.6),t,0.6,0.1)
    if k%2==1: add(tock(3000),t,0.25,0.3)
    t+=beat/2; k+=1
# strobe zaps on the break
for i in range(6): add(noiseburst(0.06,0.9),fr(SC['ponr']+110+i*4),0.7,(-1)**i*0.4)
add(dkick(),fr(SC['ponr']+110),1.0); add(whoosh(1.0),fr(SC['ponr']+110),0.6)
for s_ in ['title','ex','rule','cta']: add(noiseburst(0.2,0.7),fr(SC[s_]),0.7)
for a in [SC['ex']+14,SC['ex']+54]: add(tock(400),fr(a),0.8)
save('/tmp/dr/music/st_ocular.wav',1.3)
print('ok')
