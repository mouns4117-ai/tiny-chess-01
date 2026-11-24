import json,os
from urllib.request import *
V=(0,100,320,330,500,900,0)
KN=(-33,-31,-18,-14,14,18,31,33);DG=(-17,-15,15,17);RG=(-16,-1,1,16)
MV=(0,0,KN,DG,RG,DG+RG,DG+RG)
CB={7:1,0:2,119:4,112:8}
B=[0]*128;W=1;CR=0;U=[];J=[0]*2;T={};K=[0]*8
O=lambda m:-V[abs(B[m>>7&127])]
def parse(f):
 p=f.split();b=[0]*128;r=7;q=0
 for ch in p[0]:
  if ch=='/':r-=1;q=0
  elif ch.isdigit():q+=int(ch)
  else:b[r*16+q]=('PNBRQK'.find(ch.upper())+1)*(ch.isupper()*2-1);q+=1
 return b,p[1]=='w',sum(1<<'KQkq'.find(c) for c in p[2] if c!='-')
def atk(s,ww):
 sg=1 if ww else -1
 for d,p in zip(((-15,-17) if ww else (15,17))+KN+DG+RG,(1,1)+(2,)*8+(6,)*8):
  t=s+d
  if not t&0x88 and B[t]==p*sg:return 1
 for d in DG+RG:
  t=s+d
  while not t&0x88:
   c=B[t]
   if c:
    if c*sg in ((3,5),(4,5))[d in RG]:return 1
    break
   t+=d
 return 0
def gen():
 ms=[]
 ap=lambda t:ms.append(s|t<<7|5<<14) if t>>4==7*W else ms.append(s|t<<7)
 for s in range(128):
  if s&0x88:continue
  c=B[s]
  if not c or (c>0)!=W:continue
  p=abs(c)
  if p==1:
   d=32*W-16;t=s+d
   if not t&0x88 and not B[t]:
    ap(t)
    if (s>>4)==6-5*W and not B[t+d]:ap(t+d)
   for o in(-1,1):
    t=s+d+o
    if not t&0x88 and B[t] and (B[t]>0)!=W:ap(t)
  else:
   for d in MV[p]:
    t=s+d
    while not t&0x88:
     if B[t]:ms.append(s|t<<7) if (B[t]>0)!=W else 0;break
     ms.append(s|t<<7)
     if p%4==2:break
     t+=d
 for kf,bt,em in ((4,1,(5,6)),(4,2,(3,2,1)),(116,4,(117,118)),(116,8,(115,114,113))):
  if W==(kf==4) and CR&bt and not any(B[x] for x in em) and not any(atk(x,kf>100) for x in (kf,)+em[:2]):ms.append(kf|em[1]<<7)
 return ms
def make(m):
 global CR,W
 f=m&127;t=m>>7&127;p=m>>14&7;pc=B[f];cap=B[t]
 U.append((m,pc,cap,CR,J[0],J[1]))
 B[t]=pc if not p else p*(pc>0)*2-p;B[f]=0
 if abs(pc)==6:
  J[pc<0]=t
  if abs(t-f)==2:
   rf,rt=(t+1,t-1) if t>f else (t-2,t+1)
   B[rt]=B[rf];B[rf]=0
  CR&=~(3<<2*(pc<0))
 CR&=~(CB.get(f,0)|CB.get(t,0));W=not W
def unmake():
 global CR,W
 m,pc,cap,cr,k0,k1=U.pop()
 f=m&127;t=m>>7&127
 B[f]=pc;B[t]=cap
 if abs(pc)==6 and abs(t-f)==2:
  rf,rt=(t+1,t-1) if t>f else (t-2,t+1)
  B[rf]=B[rt];B[rt]=0
 J[:]=k0,k1;CR=cr;W=not W
ND=0
def ev():
 s=0
 for q in range(128):
  if q&0x88:continue
  c=B[q]
  if not c:continue
  p=abs(c);f=q&7;r=q>>4
  if c<0:r=7-r
  cf=min(f,7-f);cr=4-abs(r-3);v=V[p]+(r*8+cf*2 if p==1 else cf*cr*(4,3,1,2,-12)[p-2])
  s+=v*(c>0)*2-v
 return s if W else -s
def S(d,a,b):
 global ND,W
 ND+=1
 if ND>120000:1/0
 ck=atk(J[1-W],not W);a0=a;tm=0
 if d>0:
  key=(tuple(B),W,CR);te=T.get(key)
  if te:
   tm=te[3]
   if te[0]>=d and (te[1]==0 or te[2]>=b if te[1]==1 else te[2]<=a):return te[2]
  if d>=3 and not ck:
   W=not W;sc=-S(d-3,-b,-b+1);W=not W
   if sc>=b:return sc
 elif not ck:
  st=ev()
  if st>=b:return st
  a=max(a,st)
 ms=gen()
 if d<=0 and not ck:ms=[m for m in ms if B[m>>7&127] or m>>14]
 ms.sort(key=O)
 for x in(K[d%8],tm):
  if x in ms:ms.remove(x);ms.insert(0,x)
 bv=-99999;bm=0
 for m in ms:
  make(m)
  if atk(J[W],W):unmake();continue
  sc=-S(d-1,-b,-a);unmake()
  if sc>bv:bv=sc;bm=m
  a=max(a,sc)
  if a>=b:K[d%8]=m;break
 if bv==-99999:return -9999*ck or (a if d<=0 else 0)
 if d>0 and len(T)<200000:T[key]=(d,(bv<=a0)*2+(bv>=b),bv,bm)
 return bv if d>0 else a
def root(lm):
 global ND
 ND=0;best=lm[0]
 for d in range(1,9):
  try:
   a=bv=-99999;bm=best
   lm.sort(key=lambda m:m!=best)
   for m in lm:
    make(m);sc=-S(d-1,-99999,-a);unmake()
    if sc>bv:bv=sc;bm=m
    a=max(a,sc)
   best=bm
  except:break
 return best
def post(p,dy):
 try:return json.load(urlopen(os.environ['MAKEFUN_ENV_URL']+p,json.dumps(dy).encode()))
 except:return
def u(m):
 p=m>>14&7;return '%c%d%c%d%s'%(97+m%8,(m>>4&7)+1,97+(m>>7)%8,(m>>11&7)+1,'nbrq'[p-2] if p else '')
def main():
 global B,W,CR,J
 while (g:=post('/game',{})) and (st:=g['status'])!='done':
  if st!='your_move':continue
  B,W,CR=parse(g['fen']);J=[B.index(6),B.index(-6)];lg=g['legal_moves'];lm=[]
  for m in gen():
   if u(m) in lg:
    make(m)
    if not atk(J[W],W):lm.append(m)
    unmake()
  post('/move',{'game':g['game'],'move':u(root(lm)) if lm else lg.pop()})
main()
