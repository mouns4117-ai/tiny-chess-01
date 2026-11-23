import json,os
from urllib.request import urlopen
V=(0,100,320,330,500,900,0)
KN=(-33,-31,-18,-14,14,18,31,33);DG=(-17,-15,15,17);RG=(-16,-1,1,16)
JM=(0,0,KN,0,0,0,DG+RG);DS=(0,0,0,DG,RG,DG+RG,0)
CB={7:1,0:2,119:4,112:8}
B=[0]*128;W=1;CR=0;U=[]
def e(f,t,p=0):return f|t<<7|p<<14
def parse(f):
 p=f.split();b=[0]*128;r=7;q=0
 for ch in p[0]:
  if ch=='/':r-=1;q=0;continue
  if ch.isdigit():q+=int(ch);continue
  b[r*16+q]=('PNBRQK'.find(ch.upper())+1)*(ch.isupper()*2-1);q+=1
 return b,p[1]=='w',sum(1<<i for i,ch in enumerate('KQkq') if ch in p[2])
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
    if c*sg in ((3,5) if d in DG else (4,5)):return 1
    break
   t+=d
 return 0
def gen():
 ms=[]
 ap=lambda t:ms.append(e(s,t,5)) if (t>>4)==7*W else ms.append(e(s,t))
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
   for t in (s+d-1,s+d+1):
    if not t&0x88 and B[t] and (B[t]>0)!=W:ap(t)
  else:
   for d in (JM[p] if p in (2,6) else DS[p]):
    t=s+d
    while not t&0x88:
     if B[t]:
      if (B[t]>0)!=W:ms.append(e(s,t))
      break
     ms.append(e(s,t))
     if p in (2,6):break
     t+=d
 for kf in (4,116):
  for sgn in (1,-1):
   bt=(1 if sgn>0 else 2)<<(2*(kf>100));rf=kf+(3 if sgn>0 else 4)*sgn
   if (kf<100)==W and CR&bt and B[kf]==(6 if kf<100 else -6) and B[rf]==(4 if kf<100 else -4) and all(not B[x] for x in (kf+sgn,kf+2*sgn)+( (kf+3*sgn,) if sgn<0 else ())) and all(not atk(x,kf>100) for x in (kf,kf+sgn,kf+2*sgn)):ms.append(e(kf,kf+2*sgn))
 return ms
def make(m):
 global CR,W
 f=m&127;t=m>>7&127;p=m>>14&7;pc=B[f];cap=B[t]
 U.append((m,pc,cap,CR))
 B[t]=pc if not p else (p if pc>0 else -p);B[f]=0
 if abs(pc)==6 and abs(t-f)==2:
  rf,rt=(t+1,t-1) if t>f else (t-2,t+1)
  B[rt]=B[rf];B[rf]=0
 nc=CR
 if abs(pc)==6:nc&=~(3 if pc>0 else 12)
 nc&=~(CB.get(f,0)|CB.get(t,0))
 CR=nc;W=not W
def unmake():
 global CR,W
 m,pc,cap,cr=U.pop()
 f=m&127;t=m>>7&127
 B[f]=pc;B[t]=cap
 if abs(pc)==6 and abs(t-f)==2:
  rf,rt=(t+1,t-1) if t>f else (t-2,t+1)
  B[rf]=B[rt];B[rt]=0
 CR=cr;W=not W
ND=0;NB=80000;H=set();K=lambda m:-V[abs(B[m>>7&127])]
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
def S(d,a,b,pl):
 global ND
 ND+=1
 if ND>NB:1/0
 ck=atk(B.index(12*W-6),not W)
 if d<=0 and not ck:
  st=ev()
  if st>=b:return st
  a=max(a,st)
  ms=[m for m in gen() if B[m>>7&127] or m>>14];ms.sort(key=K)
 else:
  ms=gen();ms.sort(key=K)
 bv=-99999
 for m in ms:
  make(m)
  if atk(B.index(6-12*W),W):unmake();continue
  sc=-S(d-1,-b,-a,pl+1);unmake()
  bv=max(bv,sc);a=max(a,sc)
  if a>=b:break
 if bv==-99999:return a if d<=0 else -9999+pl if ck else 0
 return bv if d else a
def root(lm):
 global ND
 ND=0;best=lm[0]
 for d in range(1,9):
  try:
   a=bv=-99999;bm=best
   lm.remove(best);lm.insert(0,best)
   for m in lm:
    make(m);sc=-S(d-1,-99999,-a,1);sc-=200*(tuple(B) in H and sc>100);unmake()
    if sc>bv:bv=sc;bm=m
    a=max(a,sc)
   best=bm
  except:break
 make(best);H.add(tuple(B));unmake()
 return best
def post(p,dy):
 try:
  with urlopen(os.environ['MAKEFUN_ENV_URL']+p,json.dumps(dy).encode()) as x:return json.load(x)
 except:return
def uci(m):
 p=m>>14&7
 return '%c%d%c%d%s'%(97+m%8,(m>>4&7)+1,97+(m>>7)%8,(m>>11&7)+1,'nbrq'[p-2] if p else '')
def main():
 global B,W,CR
 while (g:=post('/game',{})) and (st:=g['status'])!='done':
  if st!='your_move':continue
  B,W,CR=parse(g['fen']);lg=g['legal_moves'];lm=[]
  for m in gen():
   if uci(m) in lg:
    make(m)
    if not atk(B.index(6-12*W),W):lm.append(m)
    unmake()
  u=uci(root(lm)) if lm else lg[0]
  post('/move',{'game':g['game'],'move':u})
main()
