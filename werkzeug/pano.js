// Panorama-Buehne: Laufen und Springen durch breite Szenen, Verfolgung am Zielort
const PANO=__PANO__,PJAGD=__PJAGD__;
Object.assign(PANO,__PANO2__);Object.assign(PJAGD,__PJAGD2__);
const PPR={kiste:[172,159,1],stapel:[181,295,.86],fass:[161,229,1],bank:[318,248,.5],sperre:[260,179,1],saeule:[183,411,0]};
const PTON={nacht:'rgba(28,44,96,.36)',dunkel:'rgba(22,30,58,.3)',abend:'rgba(120,60,30,.2)',warm:'rgba(150,90,20,.16)'};
const PIMG={};function pimg(s){return PIMG[s]||(PIMG[s]=Object.assign(new Image(),{src:s}));}
const pseq=(n,k)=>Array.from({length:k},(x,i)=>pimg('pano/'+n+String(i).padStart(2,'0')+'.webp'));
let PA=null,PSP=null,PL=null,heroTo='';
Object.keys(PANO).forEach(id=>{if(PANO[id].h)HOT[id]=PANO[id].h.map(h=>[h[0],0,0,h[2]]);});
function panoKill(){if(PA){if(PA.o.id)PL={id:PA.o.id,x:PA.H.x,dir:PA.H.dir,from:PA.o.from,t:performance.now()};cancelAnimationFrame(PA.raf);removeEventListener('resize',PA.size);PA.cv.remove();PA.pad.forEach(x=>x.remove());PA=null;}document.body.classList.remove('pano');}
function panoObjs(list,U){return (list||[]).map(o=>{const p=PPR[o[0]];return {n:o[0],x:o[1],solid:p[2]>0,w:p[0]*U*.84,h:p[1]*U*p[2],dw:p[0]*U,dh:p[1]*U,im:pimg('pano/p_'+o[0]+'.webp')};});}
function panoMake(o){panoKill();const sc=$('scene'),cv=document.createElement('canvas');cv.className='pano';cv.setAttribute('role','img');cv.setAttribute('aria-label',o.alt);
  if(!PSP)PSP={idle:pimg('pano/h_idle.webp'),run:pseq('v_run',36),jmp:pseq('v_jmp',24),lnd:pseq('v_lnd',11),dieb:pseq('v_dieb',21)};
  const mk=(c,t,l)=>{const b=document.createElement('button');b.type='button';b.className='pbtn '+c;b.textContent=t;b.setAttribute('aria-label',l);return b;};
  const bl=mk('l','◀','Nach links laufen'),br=mk('r','▶','Nach rechts laufen'),bj=mk('j','▲','Springen'),ba=mk('a','','Aktion');ba.hidden=true;
  sc.append(cv,bl,br,ba,bj);document.body.classList.add('pano');if(o.T&&document.activeElement&&document.activeElement.blur)document.activeElement.blur();
  const P=PA={cv,g:cv.getContext('2d'),pad:[bl,br,ba,bj],o,W:1,Hh:1,cam:0,keys:{},last:0,tint:new Map(),landT:0,wasAir:false,near:null,
    world:o.world,gy:o.gy,hh:o.hh,U:o.hh/520,z:o.z||1,img:pimg(o.img),ton:PTON[o.ton]||'',ents:o.ents||[],objs:[],T:o.T||null,
    H:{x:o.from<0?.08:o.from>0?o.world-.08:o.start||.3,y:0,vy:0,vx:0,dir:o.from>0?-1:1,run:0,dist:0,on:null,target:null,after:null}};
  P.objs=panoObjs(o.props,P.U);
  P.size=()=>{const r=cv.getBoundingClientRect(),d=Math.min(2,devicePixelRatio||1);cv.width=Math.max(2,Math.round(r.width*d));cv.height=Math.max(2,Math.round(r.height*d));P.Hh=cv.height;P.W=cv.width/cv.height;};
  P.size();addEventListener('resize',P.size);P.cam=Math.max(0,Math.min(P.world-P.W,P.H.x-P.W*.4));
  const hold=(b,code)=>{const on=e=>{e.preventDefault();e.stopPropagation();P.keys[code]=1;P.H.target=null;b.classList.add('on');},off=()=>{P.keys[code]=0;b.classList.remove('on');};b.addEventListener('pointerdown',on);['pointerup','pointercancel','pointerleave'].forEach(n=>b.addEventListener(n,off));b.addEventListener('contextmenu',e=>e.preventDefault());b.addEventListener('pointerup',e=>e.stopPropagation());};
  hold(bl,'L');hold(br,'R');
  bj.addEventListener('pointerdown',e=>{e.preventDefault();e.stopPropagation();panoJump();});bj.addEventListener('pointerup',e=>e.stopPropagation());
  ba.addEventListener('pointerdown',e=>e.stopPropagation());ba.addEventListener('pointerup',e=>e.stopPropagation());ba.onclick=()=>panoAct();
  cv.addEventListener('pointerdown',e=>{if(P.T&&P.T.st!=='run')return;const r=cv.getBoundingClientRect(),wx=P.cam+(e.clientX-r.left)/r.height,H=P.H;H.after=null;
    const en=!P.T&&P.ents.filter(n=>!n.gone&&Math.abs(wx-n.x)<(n.r||.09)).sort((a,b)=>Math.abs(wx-a.x)-Math.abs(wx-b.x))[0];
    if(en){H.target=en.t==='exit'?en.x:en.x+(H.x<en.x?-1:1)*(en.off||.12);H.after=()=>panoDo(en);}else H.target=Math.max(.06,Math.min(P.world-.06,wx));});
  P.raf=requestAnimationFrame(t=>{P.last=t;panoLoop(t);});return P;}
function panoJump(){const P=PA;if(!P)return;const H=P.H;if(P.T&&P.T.st!=='run')return;if(H.y===0||H.on){H.vy=-1.12;H.on=null;if(H.y===0)H.y=-.0001;}}
function panoDo(en){if(!PA||!en||en.gone||S.over||S.busy)return;PA.H.dir=en.x>=PA.H.x?1:-1;PA.H.target=null;en.act();}
function panoAct(){const P=PA;if(P&&P.near)panoDo(P.near);}
addEventListener('keydown',e=>{const P=PA;if(!P||$('sheet'))return;const t=document.activeElement&&document.activeElement.tagName;if(t==='SELECT'||t==='INPUT'||t==='TEXTAREA')return;
  const c=e.code,mv=c==='ArrowLeft'||c==='KeyA'?'L':c==='ArrowRight'||c==='KeyD'?'R':'';
  if(mv){e.preventDefault();P.keys[mv]=1;P.H.target=null;}
  else if(c==='ArrowUp'||c==='KeyW'||(c==='Space'&&t!=='BUTTON')){e.preventDefault();panoJump();}
  else if(c==='KeyE'||(c==='Enter'&&t!=='BUTTON'))panoAct();});
addEventListener('keyup',e=>{const P=PA;if(!P)return;const c=e.code;if(c==='ArrowLeft'||c==='KeyA')P.keys.L=0;if(c==='ArrowRight'||c==='KeyD')P.keys.R=0;});
function panoStep(P,dt){const H=P.H,HW=.034,frozen=P.T&&P.T.st!=='run';
  let mv=frozen?0:(P.keys.R?1:0)-(P.keys.L?1:0),top0=.72;
  if(!mv&&H.target!=null&&!frozen){const d=H.target-H.x;if(Math.abs(d)<.014){H.target=null;const a=H.after;H.after=null;if(a)a();}else{mv=d>0?1:-1;top0=Math.min(.72,Math.abs(d)*5+.1);}}
  if(mv)H.dir=mv;
  const feet=-H.y,blk=d=>P.objs.some(o=>{if(!o.solid)return false;const e=o.w/2+HW,n=Math.abs(H.x+d-o.x);return n<e&&n<Math.abs(H.x-o.x)&&feet<o.h-.012;});
  if(mv&&blk(mv*.006)){H.vx=0;H.run=0;if(H.target!=null&&(H.y===0||H.on))panoJump();}
  else{const want=mv*top0,acc=(mv?3.2:4.5)*dt;H.vx+=Math.max(-acc,Math.min(acc,want-H.vx));if(calm)H.vx=want;
    if(Math.abs(H.vx)>.04&&!blk(H.vx*dt)){const nx=Math.max(.04,Math.min(P.world-.04,H.x+H.vx*dt));H.dist+=Math.abs(nx-H.x);H.run=nx!==H.x?1:0;H.x=nx;}
    else{H.run=0;if(Math.abs(H.vx)>.04)H.vx=0;}}
  let top=0,ob=null;P.objs.forEach(b=>{if(b.solid&&Math.abs(H.x-b.x)<b.w/2+HW*.8&&b.h>top){top=b.h;ob=b;}});
  if(H.on&&(!ob||ob!==H.on))H.on=null;
  if(H.y<0&&!H.on||H.vy<0){const py=H.y;H.vy+=2.75*dt;H.y+=H.vy*dt;
    if(H.vy>0&&top>0&&-py>=top-.004&&-H.y<=top){H.y=-top;H.vy=0;H.on=ob;}else if(H.y>=0){H.y=0;H.vy=0;H.on=null;}}
  else if(H.on)H.y=-H.on.h;
  const air=H.y<0&&!H.on;if(P.wasAir&&!air)P.landT=.3;P.wasAir=air;P.landT=Math.max(0,P.landT-dt);
  const T=P.T;
  if(T){if(T.st==='run'){T.x+=T.v*dt;T.dist+=T.v*dt;
      if(T.x-H.x<.12&&Math.abs(H.y)<.2){T.st='caught';T.t=1.3;}else if(T.x>P.world-.15){T.st='lost';T.t=1.3;}}
    else{T.t-=dt;if(T.t<=0&&!T.done){T.done=1;const w=T.st==='caught',cb=T.cb;setTimeout(()=>cb(w),0);}}}
  else{ // Ausgaenge durch Hinauslaufen, naechstes Ziel fuer den Aktionsknopf
    let nr=null,bd=.16;P.ents.forEach(n=>{if(n.gone||n.t==='exit')return;const d=Math.abs(n.x-H.x);if(d<bd){bd=d;nr=n;}});
    P.ents.forEach(n=>{if(n.t==='exit'&&Math.abs(n.x-H.x)<.07&&((n.x<1&&(P.keys.L||H.target===n.x))||(n.x>1&&(P.keys.R||H.target===n.x)))&&!P.left){P.left=1;P.keys={};H.target=null;setTimeout(()=>panoDo(n),0);}});
    P.near=H.y===0&&!S.over&&!S.busy?nr:null;const b=P.pad[2];b.hidden=!P.near;if(P.near&&b.textContent!==P.near.verb)b.textContent=P.near.verb;}
  const want=Math.max(0,Math.min(P.world-P.W,H.x-P.W*(T?.28:H.dir>0?.4:.6)));P.cam+=(want-P.cam)*Math.min(1,dt*(calm?60:3.2));if(P.W>=P.world)P.cam=(P.world-P.W)/2;}
function panoTint(P,im){if(!im.complete||!im.naturalWidth)return null;if(!P.ton)return im;let c=P.tint.get(im);if(c)return c;c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d');x.drawImage(im,0,0);x.globalCompositeOperation='source-atop';x.fillStyle=P.ton;x.fillRect(0,0,c.width,c.height);P.tint.set(im,c);return c;}
function panoDraw(P,now){const g=P.g,Hh=P.Hh,H=P.H,U=P.U,cv=P.cv;
  const spr=(im,x,fy,h,flip,bob)=>{const c=panoTint(P,im);if(!c)return;const w=h*(c.width||c.naturalWidth)/(c.height||c.naturalHeight);g.save();g.translate((x-P.cam)*Hh,(P.gy+fy)*Hh);if(flip)g.scale(-1,1);if(bob)g.scale(1,bob);g.drawImage(c,-w/2*Hh,-h*Hh,w*Hh,h*Hh);g.restore();};
  const shadow=(x,w,y)=>{g.fillStyle='rgba(0,0,0,.4)';g.beginPath();g.ellipse((x-P.cam)*Hh,(P.gy+(y||0))*Hh,Math.max(.001,w)*Hh,.012*Hh,0,0,6.3);g.fill();};
  g.fillStyle='#0b101b';g.fillRect(0,0,cv.width,cv.height);
  const im=P.img,tw=3*P.z;
  if(im.complete&&im.naturalWidth){const s=im.naturalHeight;for(let t=Math.floor(P.cam/tw);t*tw<P.cam+P.W&&t*tw<P.world+tw;t++){g.save();g.translate(Math.round((t*tw-P.cam)*Hh),0);if(t%2){g.translate(tw*Hh,0);g.scale(-1,1);}g.drawImage(im,0,s*(1-1/P.z),im.naturalWidth,s/P.z,0,0,tw*Hh+1,Hh);g.restore();}}
  const br=1+Math.sin(now/900)*.006,fs=Math.max(11,.03*Hh);
  P.objs.filter(o=>!o.solid).forEach(o=>{shadow(o.x,o.dw*.5);spr(o.im,o.x,0,o.dh);});
  P.ents.forEach(n=>{if(n.gone)return;const sx=(n.x-P.cam)*Hh;if(sx<-200||sx>cv.width+200)return;
    if(n.t==='fig'){shadow(n.x,.05);spr(n.im,n.x,0,P.hh*(n.s||1),n.flip!=null?n.flip:H.x<n.x,1+Math.sin(now/1000+n.x*7)*.006);
      if(n.mark&&n.mark()){const by=(P.gy-P.hh*(n.s||1)-.045+Math.sin(now/300)*.006)*Hh;g.fillStyle='#f2b455';g.beginPath();g.arc(sx,by,.024*Hh,0,6.3);g.fill();g.fillStyle='#1c1405';g.font='700 '+(.034*Hh)+'px "IBM Plex Sans",sans-serif';g.textAlign='center';g.textBaseline='middle';g.fillText('!',sx,by+.002*Hh);}}
    else if(n.t==='hot'){const y=(P.gy-(n.y||.2))*Hh,seen=n.seen&&n.seen(),a=seen?.35:.6+.4*Math.sin(now/350);g.strokeStyle='rgba(242,180,85,'+a.toFixed(2)+')';g.lineWidth=Math.max(2,.005*Hh);g.beginPath();g.arc(sx,y,(seen?.016:.02+.004*Math.sin(now/350))*Hh,0,6.3);g.stroke();g.fillStyle='rgba(242,180,85,'+(seen?.3:.9)+')';g.beginPath();g.arc(sx,y,.007*Hh,0,6.3);g.fill();}
    else if(n.t==='item'){const y=(P.gy-.012)*Hh,w=.05*Hh;g.save();g.translate(sx,y);g.rotate(-.12);g.shadowColor='rgba(242,180,85,'+(.6+.4*Math.sin(now/300)).toFixed(2)+')';g.shadowBlur=.03*Hh;g.fillStyle='#fbf3dc';g.fillRect(-w/2,-w*.34,w,w*.34);g.restore();}
    else if(n.t==='exit'){g.font='600 '+fs+'px "IBM Plex Sans",sans-serif';const lab=n.x<1?'‹ '+n.name:n.name+' ›',twd=g.measureText(lab).width+.04*Hh,xx=n.x<1?sx:sx-twd,yy=.3*Hh,hh=fs*1.9;g.fillStyle='rgba(13,19,32,.86)';g.fillRect(xx,yy,twd,hh);g.strokeStyle='#f2b455';g.lineWidth=2;g.strokeRect(xx,yy,twd,hh);g.fillStyle='#f6e7c8';g.textAlign='left';g.textBaseline='middle';g.fillText(lab,xx+.02*Hh,yy+hh/2);}});
  P.objs.filter(o=>o.solid).forEach(o=>{shadow(o.x,o.dw*.5);spr(o.im,o.x,0,o.dh);});
  const T=P.T;
  if(T){let ty=0;P.objs.forEach(o=>{if(!o.solid)return;const d=Math.abs(o.x-T.x);if(d<.16)ty=Math.max(ty,Math.cos(d/.16*1.57)*(o.h+.035));});shadow(T.x,.05*(1-ty*2));spr(PSP.dieb[T.st==='run'?Math.floor(T.dist/.026)%21:8],T.x,-ty,540*U,T.st==='lost');}
  shadow(H.x,.05*(1+H.y*1.5));const air=H.y<0&&!H.on;
  if(air)spr(PSP.jmp[Math.max(0,Math.min(23,Math.round((H.vy+1.12)/2.24*23)))],H.x,H.y,509*U,H.dir<0);
  else if(P.landT>0&&H.run)spr(PSP.lnd[Math.min(10,Math.floor((.3-P.landT)/.3*11))],H.x,H.y,475*U,H.dir<0);
  else if(H.run)spr(PSP.run[Math.floor(H.dist/.0195/(P.hh/.31))%36],H.x,H.y,491*U,H.dir<0);
  else spr(PSP.idle,H.x,H.y,P.hh,H.dir<0,br);
  if(P.near&&P.near.name){const n=P.near;g.font='600 '+fs+'px "IBM Plex Sans",sans-serif';const tw2=g.measureText(n.name).width+.03*Hh,sx=Math.max(tw2/2+4,Math.min(cv.width-tw2/2-4,(n.x-P.cam)*Hh)),yy=(P.gy-P.hh-.13)*Hh;g.fillStyle='rgba(13,19,32,.88)';g.fillRect(sx-tw2/2,yy,tw2,fs*1.7);g.fillStyle='#f6e7c8';g.textAlign='center';g.textBaseline='middle';g.fillText(n.name,sx,yy+fs*.85);}
  if(T){const gap=Math.max(0,T.x-H.x),bw=.36*Hh,bx=cv.width/2-bw/2,by=.05*Hh;g.fillStyle='rgba(13,19,32,.85)';g.fillRect(bx-8,by-6,bw+16,.035*Hh+12);g.fillStyle='#2b3b5a';g.fillRect(bx,by,bw,.035*Hh);g.fillStyle=gap>1?'#b5483a':'#f2b455';g.fillRect(bx,by,bw*Math.min(1,gap/1.6),.035*Hh);g.fillStyle='#eef1f6';g.font='600 '+fs*.8+'px "IBM Plex Sans",sans-serif';g.textAlign='center';g.textBaseline='middle';g.fillText('Abstand',cv.width/2,by+.0185*Hh);
    if(T.st!=='run'){g.fillStyle='rgba(8,12,22,.5)';g.fillRect(0,0,cv.width,cv.height);g.fillStyle=T.st==='caught'?'#f2b455':'#e8796b';g.font='700 '+(.13*Hh)+'px "Playfair Display",Georgia,serif';g.fillText(T.st==='caught'?'Gefasst!':'Entwischt!',cv.width/2,Hh*.45);}}}
function panoLoop(now){const P=PA;if(!P)return;P.raf=requestAnimationFrame(panoLoop);const dt=Math.min(.05,Math.max(0,(now-P.last)/1000));P.last=now;if(P.cv.height<4||Math.abs(P.cv.getBoundingClientRect().height*Math.min(2,devicePixelRatio||1)-P.cv.height)>2)P.size();panoStep(P,dt);panoDraw(P,now);}
// Schauplatz als Panorama aufbauen
function panoStage(id,k,c,F){const cfg=PANO[id],o=c.orte[k],LC=LV[LVL],ents=[],key=S.i+'_'+k;
  ents.push({t:'fig',x:cfg.w,im:pimg('figuren/'+o.p+'.webp'),name:o.zeuge+' · '+o.rolle,verb:'Reden',act:()=>ask(k),mark:()=>LC.mark&&!S.seen[key]});
  (cfg.e||[]).forEach(e=>{if(!EX[e[0]])return;ents.push({t:'fig',x:e[1],flip:e[2]?true:null,s:.97,im:pimg('figuren/'+e[0]+'.webp'),name:EX[e[0]][0],verb:'Reden',act:()=>askExtra(e[0])});});
  (cfg.h||[]).forEach((h,n)=>ents.push({t:'hot',x:h[1],y:h[3]||.22,name:h[0],verb:'Ansehen',off:.06,r:.07,act:()=>look(id,n),seen:()=>S.hs[id+n]}));
  const it=S.items&&S.items[S.i];
  if(LC.mark&&it&&it.k===k&&!it.found&&!isFinal()){const e={t:'item',x:cfg.it||1.9,name:'Fundstück',verb:'Aufheben',off:.05,r:.07,act:()=>{e.gone=1;pick();}};ents.push(e);}
  const l=(k+2)%3,r=(k+1)%3;
  ents.push({t:'exit',x:0,name:c.orte[l].ort,act:()=>{heroFrom=1;heroTo=c.id+l;goTo(l);}},{t:'exit',x:3,name:c.orte[r].ort,act:()=>{heroFrom=-1;heroTo=c.id+r;goTo(r);}});
  let from=0,start=cfg.s||.35;if(heroFrom&&(!heroTo||heroTo===id)){from=heroFrom;heroFrom=0;heroTo='';}const same=PL&&PL.id===id;
  if(!from&&same){if(PL.from&&performance.now()-PL.t<1500&&(PL.x<.2||PL.x>2.8))from=PL.from;else start=PL.x;}
  panoMake({id,img:'pano/'+id+'.webp',world:3,gy:cfg.gy,hh:cfg.hh,ton:F.t,ents,props:cfg.p,from,start,alt:'Spielszene '+o.ort+' in '+c.name+': Die Ermittlerin läuft durch ein breites gemaltes Panorama und kann '+o.zeuge+' ansprechen'});}
// Verfolgung am Zielort
function panoChase(city,done){const J=PJAGD[city];S.busy=true;S.pend=null;render();
  say('Direktorin Halberg','per Funk','Da läuft sie! Hinterher. Springen Sie über alles, was im Weg steht.');
  const world=13.2,props=[];let x=1.9;const kinds=['kiste','sperre','fass','bank'];for(let i=0;x<world-.8;i++){props.push([kinds[i%4],+x.toFixed(2)]);x+=.72+((i*37)%5)*.07;}
  const cb=win=>{panoKill();S.busy=false;figKey='';if(win){done();render();return;}
    S.busy=true;S.pend=done;advance(3);if(timeUp()){S.pend=null;S.busy=false;render();return;}
    say('Direktorin Halberg','per Funk','Entwischt! Die Person ist in einer Seitengasse verschwunden. Das hat uns 3 Stunden gekostet.\n\nUnsere Leute haben sie wieder im Blick. Nehmen Sie die Verfolgung noch einmal auf.');render();};
  panoMake({img:'pano/'+J.img+'.webp',z:J.z,world,gy:J.gy,hh:J.hh,ton:J.ton,props,start:.45,T:{st:'run',x:1.4,v:{l:.58,m:.61,s:.64}[LVL],dist:0,t:0,cb},alt:'Verfolgungsjagd in '+CITY[city].name+': Die Ermittlerin rennt der flüchtenden Person durch eine Straße hinterher'});}
