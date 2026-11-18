import json,os,urllib.request as U
from base64 import b85decode as D
E=os.environ["MAKEFUN_ENV_URL"]
PH=[0,0,1,1,2,4,0]
X=int.from_bytes(D('x7+P@yWMWATMQ=q5n(TzjfTSsXRe!V*URl*GhWX3+x1{I9Z=X*0%KS*^Xd!_X}8<$cDvnf6c~vmbH!jT)6913&0;XxZs+R(WwTt57xejRw4N_XboPFzC9ydbLyaHRbNFNGWB?88#JtETEZYn=o2g(qUhk&!32`?bkH-V{b~PRkINa@Wwww=1B<gN5qOmwc5^t|wY!+PhP_7(j^-Ae#u^Fz{)2&`9S&Vku)j+71OoqGJSgY6UrmN*(FPaYc8`ferA8^<+GJ8Pbk|}ipjl!Z3$<zsrw-{|Fd$mri+774V*>E!)?PkOAa<mtXcC+DZE|*Mp>)miOnNAl}9+fYZ4JT6uldfBEw=^1!vf-|zbNzTYT}_md>2$Lh43%ohT&J5$g-WqZve?Ykdd*g}A5Ip_{b0dctX8wFT%uo3R$}3Jx7+P@yWMU)oo>gw;c7Wu4R^EMYCN5-R;%G|!XGbp%k_HKEY+z@PN(xYn~Wa2?YG<QcDvnfE)z@!i=9NN7|nKz!BQ~WjkmMKV6j>c*z4tDGTiU?+v#Gj*iLt&#Z<4_>qdLMOr+J!)pCg}FdEE8li6gmSnZah$y_s=ZpXvbWHlVmr`y?RHr-Cg+u?Ay+U<7B-EuXXZf2X=W-}PAR-?&YG#u_`o8@A)+6_me(QLMx?N*!BWVoCzXRFm{IUEm%!`*N?oi3NN*=#!=Z)d~laJ*fQx7+D*EEg<gYsFMBSW6~@ty(e{FQ@D6a<QQAC>#=hxZlsHEGmbwoDO*$`gAg%u($*UZ?xYJ2=wiICKin5n!QpkT8_ud*<>->&iCu-Xfd1b2mI-1wcig26asO(-jC-q8hNuGuh%2~b{|$OM&spV'),'little')
Q=[(((X>>(7*i))&127)-0)*3-167 for i in range(768)]
M0=[82,337,365,477,1025,0]
E0=[94,281,297,512,936,0]
MG=[[0]*64]+[[M0[a]+Q[a*64+i]for i in range(64)]for a in range(6)]
EG=[[0]*64]+[[E0[a]+Q[384+a*64+i]for i in range(64)]for a in range(6)]
H=[0]*4096
def jumps(offs,lim):
	return[[t for t in(s+o for o in offs)if 0<=t<64 and abs(t%8-s%8)<=lim]for s in range(64)]
KJ=jumps([-17,-15,-10,-6,6,10,15,17],2)
GJ=jumps([-9,-8,-7,-1,1,7,8,9],1)
def rays(s):
	out=[]
	for d in(1,-1,8,-8,9,-9,7,-7):
		r=[]
		t=s
		while True:
			u=t+d
			if not 0<=u<64 or abs(u%8-t%8)>1:
				break
			r.append(u)
			t=u
		out.append(r)
	return out
RA=[rays(s)for s in range(64)]
CRM=[15]*64
CRM[0]=13
CRM[7]=14
CRM[4]=12
CRM[56]=7
CRM[63]=11
CRM[60]=3
FM={c:i for i,c in enumerate("pnbrqk",1)}
B=[0]*64
side=1
cast=15
ep=-1
tt={}
nodes=0
stop=False
LIMIT=250000
INF=10**7
MATE=10**6
KIL=[[0,0]for _ in range(64)]
PTH=[0]*128
HIS=[]
hm=0
def init(fen):
	global B,side,cast,ep,ph,hm
	p=fen.split()
	B=[0]*64
	for i,row in enumerate(p[0].split("/")):
		f=0
		for c in row:
			if c.isdigit():
				f+=int(c)
			else:
				B[(7-i)*8+f]=FM[c.lower()]*(1 if c.isupper()else-1)
				f+=1
	side=1 if p[1]=="w" else-1
	cast=0
	if "K" in p[2]:cast|=1
	if "Q" in p[2]:cast|=2
	if "k" in p[2]:cast|=4
	if "q" in p[2]:cast|=8
	ep=-1 if p[3]=="-" else(ord(p[3][0])-97)+(int(p[3][1])-1)*8
	ph=sum(PH[abs(p)]for p in B)
	hm=int(p[4])if len(p)>4 else 0
def att(s,by):
	b=B
	for t in(s-8*by-1,s-8*by+1):
		if 0<=t<64 and abs(t%8-s%8)==1 and b[t]==by:
			return True
	for t in KJ[s]:
		if b[t]==2*by:
			return True
	for t in GJ[s]:
		if b[t]==6*by:
			return True
	for i,r in enumerate(RA[s]):
		for t in r:
			q=b[t]
			if q:
				if q*by>0:
					a=abs(q)
					if a==5 or(a==4 and i<4)or(a==3 and i>=4):
						return True
				break
	return False
def gen(caps=False):
	ms=[]
	b=B
	us=side
	for s in range(64):
		p=b[s]
		if p*us<=0:
			continue
		a=abs(p)
		if a==1:
			r=s>>3
			one=s+8*us
			if not caps and 0<=one<64 and b[one]==0:
				if r==(6 if us>0 else 1):
					ms.append(s|one<<6|4<<12)
				else:
					ms.append(s|one<<6)
					two=s+16*us
					if r==(1 if us>0 else 6)and b[two]==0:
						ms.append(s|two<<6)
			for dd in(8*us-1,8*us+1):
				t=s+dd
				if 0<=t<64 and abs(t%8-s%8)==1 and(b[t]*us<0 or t==ep):
					if t>>3==(7 if us>0 else 0):
						ms.append(s|t<<6|4<<12)
					else:
						ms.append(s|t<<6)
		elif a==2 or a==6:
			for t in(KJ if a==2 else GJ)[s]:
				q=b[t]
				if q*us<=0 and(not caps or q):
					ms.append(s|t<<6)
			if a==6 and not caps:
				if us>0:
					if cast&1 and b[5]==0 and b[6]==0 and b[4]==6 and b[7]==4 and not att(4,-us)and not att(5,-us):
						ms.append(4|6<<6)
					if cast&2 and b[3]==0 and b[2]==0 and b[1]==0 and b[4]==6 and b[0]==4 and not att(4,-us)and not att(3,-us):
						ms.append(4|2<<6)
				else:
					if cast&4 and b[61]==0 and b[62]==0 and b[60]==-6 and b[63]==-4 and not att(60,-us)and not att(61,-us):
						ms.append(60|62<<6)
					if cast&8 and b[59]==0 and b[58]==0 and b[57]==0 and b[60]==-6 and b[56]==-4 and not att(60,-us)and not att(59,-us):
						ms.append(60|58<<6)
		else:
			for i,r in enumerate(RA[s]):
				if(a==3 and i<4)or(a==4 and i>=4):
					continue
				for t in r:
					q=b[t]
					if q==0:
						if not caps:
							ms.append(s|t<<6)
					else:
						if q*us<0:
							ms.append(s|t<<6)
						break
	return ms
def mk(m):
	global side,ep,cast,ph,hm
	f=m&63
	t=m>>6&63
	pr=m>>12
	b=B
	p=b[f]
	cap=b[t]
	if 1<abs(cap)<6:
		ph-=PH[abs(cap)]
	if abs(p)==1 and t==ep and cap==0:
		cap=-side
		b[t-8*side]=0
	ohm=hm
	if abs(p)==1 or cap:
		hm=0
	else:
		hm+=1
	b[t]=side*(pr+1)if pr else p
	if pr:
		ph+=PH[pr+1]
	b[f]=0
	if abs(p)==6 and abs(t-f)==2:
		if t>f:
			b[t-1]=b[t+1]
			b[t+1]=0
		else:
			b[t+1]=b[t-2]
			b[t-2]=0
	old=cast
	cast&=CRM[f]&CRM[t]
	oep=ep
	ep=f+8*side if abs(p)==1 and abs(t-f)==16 else-1
	side=-side
	return(f,t,p,cap,old,oep,ohm)
def um(m,u):
	global side,ep,cast,ph,hm
	f,t,p,cap,old,oep,ohm=u
	side=-side
	b=B
	if m>>12:
		ph-=PH[(m>>12)+1]
	if 1<abs(cap)<6:
		ph+=PH[abs(cap)]
	b[f]=p
	if abs(p)==1 and t==oep and cap:
		b[t]=0
		b[t-8*side]=cap
	else:
		b[t]=cap
	if abs(p)==6 and abs(t-f)==2:
		if t>f:
			b[t+1]=b[t-1]
			b[t-1]=0
		else:
			b[t-2]=b[t+1]
			b[t+1]=0
	cast=old
	ep=oep
	hm=ohm
def key():
	return hash((tuple(B),side,cast,ep))
def ev():
	s0=s1=0
	b=B
	for i,p in enumerate(b):
		if p:
			a=abs(p)
			if p>0:
				s0+=MG[a][i]
				s1+=EG[a][i]
			else:
				s0-=MG[a][i^56]
				s1-=EG[a][i^56]
	g=ph
	if g>24:
		g=24
	return((s0*g+s1*(24-g))//24)*side
def order(ms,tm,ply):
	b=B
	def sc(m):
		if m==tm:
			return 10**9
		f=m&63
		t=m>>6&63
		q=b[t]
		if q:
			return 10**6+abs(q)*10-abs(b[f])
		if m>>12:
			return 9*10**5
		if m==KIL[ply][0]:
			return 8*10**5
		if m==KIL[ply][1]:
			return 7*10**5
		return H[f*64+t]
	ms.sort(key=sc,reverse=True)
def qs(a,b,ply):
	global nodes,stop
	nodes+=1
	if nodes>=LIMIT:
		stop=True
		return 0
	if hm>=100:
		return 0
	us=side
	chk=att(B.index(6*us),-us)
	best=-MATE
	if not chk:
		best=ev()
		if best>=b:
			return best
		if best>a:
			a=best
	ms=gen(not chk)
	order(ms,0,ply)
	for m in ms:
		u=mk(m)
		if att(B.index(6*us),-us):
			um(m,u)
			continue
		v=-qs(-b,-a,ply+1)
		um(m,u)
		if stop:
			return 0
		if v>best:
			best=v
		if v>a:
			a=v
		if a>=b:
			break
	if chk and best==-MATE:
		return-MATE+ply
	return best
def nega(d,a,b,ply):
	global nodes,stop,side,ep
	nodes+=1
	if nodes>=LIMIT:
		stop=True
		return 0
	k=key()
	if hm>=100 or k in HIS or k in PTH[:ply]:
		return 0
	PTH[ply]=k
	e=tt.get(k)
	tm=0
	if e:
		d0,fl,sc,tm=e
		if sc>MATE-1000:sc-=ply
		elif sc<-MATE+1000:sc+=ply
		if d0>=d:
			if fl==0:
				return sc
			if fl==1 and sc>=b:
				return sc
			if fl==2 and sc<=a:
				return sc
	if d<=0:
		return qs(a,b,ply)
	us=side
	chk=att(B.index(6*us),-us)
	if d>=3 and not chk and ph>6 and abs(b)<MATE-100:
		oep=ep
		ep=-1
		side=-side
		v=-nega(d-3,-b,-b+1,ply+1)
		side=-side
		ep=oep
		if stop:
			return 0
		if v>=b:
			return b
	ms=gen()
	order(ms,tm,ply)
	best=-MATE
	bm=0
	a0=a
	first=True
	for m in ms:
		u=mk(m)
		if att(B.index(6*us),-us):
			um(m,u)
			continue
		if first:
			v=-nega(d-1,-b,-a,ply+1)
		else:
			red=1 if d>=3 and not chk and not(m>>12)and not B[m>>6&63]else 0
			v=-nega(d-1-red,-a-1,-a,ply+1)
			if a<v and(red or v<b)and not stop:
				v=-nega(d-1,-b,-a,ply+1)
		first=False
		um(m,u)
		if stop:
			return 0
		if v>best:
			best=v
			bm=m
		if v>a:
			a=v
		if a>=b:
			if not B[m>>6&63]and not(m>>12):
				H[(m&63)*64+(m>>6&63)]+=d*d
				if KIL[ply][0]!=m:
					KIL[ply][1]=KIL[ply][0]
					KIL[ply][0]=m
			break
	if best==-MATE:
		return-MATE+ply if chk else 0
	fl=0 if best>a0 and best<b else(1 if best>=b else 2)
	s=best
	if s>MATE-1000:s+=ply
	elif s<-MATE+1000:s-=ply
	tt[k]=(d,fl,s,bm)
	return best
def root(d,ms):
	global stop
	k=key()
	PTH[0]=k
	e=tt.get(k)
	order(ms,e[3]if e else 0,0)
	a=-INF
	best=ms[0]
	us=side
	first=True
	for m in ms:
		u=mk(m)
		if att(B.index(6*us),-us):
			um(m,u)
			continue
		if first:
			v=-nega(d-1,-INF,-a,1)
		else:
			v=-nega(d-1,-a-1,-a,1)
			if v>a and not stop:
				v=-nega(d-1,-INF,-a,1)
		first=False
		um(m,u)
		if stop:
			return None
		if v>a:
			a=v
			best=m
	tt[k]=(d,0,a,best)
	return best
def enc(u):
	f=ord(u[0])-97+(int(u[1])-1)*8
	t=ord(u[2])-97+(int(u[3])-1)*8
	pr=" nbrq".find(u[4])if len(u)>4 else 0
	return f|t<<6|pr<<12
def uci(m):
	f=m&63
	t=m>>6&63
	pr=m>>12
	s="abcdefgh"[f%8]+str(f//8+1)+"abcdefgh"[t%8]+str(t//8+1)
	return s+(" nbrq"[pr]if pr else "")
def choose(fen,legal):
	global nodes,stop
	init(fen)
	HIS.append(key())
	tt.clear()
	for x in KIL:
		x[0]=x[1]=0
	for i in range(4096):
		H[i]=0
	nodes=0
	ms=[enc(u)for u in legal]
	best=ms[0]
	for d in range(1,40):
		stop=False
		r=root(d,ms)
		if stop or r is None:
			break
		best=r
		if len(ms)==1 or abs(tt.get(key(),(0,0,0,0))[2])>MATE-1000:
			break
	return uci(best)
def post(path,body):
	req=U.Request(E+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
	with U.urlopen(req)as r:
		return json.load(r)
if __name__=="__main__":
	while True:
		g=post("/game",{})
		if g["status"]=="done":
			break
		HIS.clear()
		while g["status"]=="your_move":
			g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
