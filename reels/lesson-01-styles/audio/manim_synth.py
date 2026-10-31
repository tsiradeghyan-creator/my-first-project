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
def softpiano(f,len_=3.0,v=1.0):
    n=int(len_*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for k,a in ((1,1),(2,0.35),(3,0.12),(4,0.05)): x+=a*np.sin(2*np.pi*f*k*t)*np.exp(-t*(0.8+k*0.6))
    return lp(x,0.35)*(1-np.exp(-t*120))*v*0.3
# echo/reverb by feedback delays
def place(sig,t,g,pan):
    add(sig,t,g,pan); add(sig,t+0.33,g*0.35,-pan); add(sig,t+0.66,g*0.15,pan)
# gentle progression: Fmaj7 - Am7 - Dm9 - Bbmaj7 (curious, warm)
prog=[[174.61,220,261.63,329.63],[220,261.63,329.63,392],[146.83,174.61,220,261.63,329.63],[116.54,146.83,174.61,220]]
bar=2.8; t=0.0; b=0
while t<fr(1575):
    ch=prog[b%4]
    add(pad([ch[0]/2,ch[0]],bar+0.8,0.25),t)
    order=[0,2,1,3,2,1] if b%2==0 else [0,1,2,3,1,2]
    for k,idx in enumerate(order):
        f=ch[idx%len(ch)]*(2 if k>=3 else 1)
        place(softpiano(f,2.5,0.8 if k else 1.0),t+k*bar/6,0.6,(-1)**k*0.3)
    t+=bar; b+=1
# soft "pop" for each scene change
for s_ in [195,405,570,675,840,945,1110,1245,1410]:
    n=int(0.4*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*880*tt)*np.exp(-tt*12)*0.15,fr(s_),0.7)
add(pad([174.61,220,261.63,349.23],3.5,0.45),fr(1575)); place(softpiano(698.46,3,0.9),fr(1575)+0.2,0.7,0)
mix=np.stack([L,R],1); mix=np.tanh(mix*1.0); mix/=np.max(np.abs(mix))*1.12
with wave.open('/tmp/dr/music/manim_bed.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
print('ok')
