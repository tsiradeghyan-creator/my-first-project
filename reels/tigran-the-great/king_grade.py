import cv2, numpy as np, sys, os
R="/tmp/kref/"
EXT=["k_1","k_100","k_101.5","k_105","k_11","k_3","k_30","k_5","k_62"]
INT=["i_68","i_7","i_8.5","i_71","k_60","k_98"]
def stats(names):
    px=[]
    for n in names:
        im=cv2.imread(R+n+".png"); h=im.shape[0]; im=im[int(h*.15):int(h*.85)]
        lab=cv2.cvtColor(im.astype(np.float32)/255,cv2.COLOR_BGR2LAB).reshape(-1,3)
        lab=lab[lab[:,0]>2]  # skip pure black
        px.append(lab)
    p=np.concatenate(px); return p.mean(0),p.std(0)
ref={"ext":stats(EXT),"int":stats(INT)}
for k,(m,s) in ref.items(): print(k,"mean L a b",m.round(1),"std",s.round(1))
def transfer(src,dst,kind,amt):
    im=cv2.imread(src); lab=cv2.cvtColor(im.astype(np.float32)/255,cv2.COLOR_BGR2LAB)
    m,s=lab.reshape(-1,3).mean(0),lab.reshape(-1,3).std(0); rm,rs=ref[kind]
    out=(lab-m)/s*rs+rm
    w=np.array([amt,amt*0.55,amt*0.55],np.float32)
    out=lab*(1-w)+out*w
    out[...,0]=np.clip(out[...,0],0,100)
    bgr=cv2.cvtColor(out.astype(np.float32),cv2.COLOR_LAB2BGR)
    bgr=np.clip(bgr,0,1)
    # soft film curve: lift blacks slightly, roll highlights
    bgr=0.03+bgr*0.94
    cv2.imwrite(dst,(bgr*255+0.5).astype(np.uint8))
if __name__=="__main__":
    S="/home/user/my-first-project/reels/tigran-the-great/stills/"; O="/home/user/my-first-project/reels/tigran-the-great/stills_king_grade/"
    os.makedirs(O,exist_ok=True)
    jobs=[("A08_ararat_roman_camp","ext",.8),("B05_city_burning","int",.55),("B04_cataphract_fall","ext",.8),
          ("A09_lictors_pompey_horse","ext",.8),("B11_sword_handover","ext",.75),("B07_crown_hands","int",.7),
          ("B13_crown_in_dirt","int",.7),("B02_shields","ext",.8),("A10_ring_reins","ext",.75)]
    for n,k,a in jobs: transfer(S+n+".png",O+n+"_KING.png",k,a)
