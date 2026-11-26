/* ---------- Büro, Laufbahn, Zellentrakt ---------- */
let MODE='title',META={cases:[],arrested:[],money:0,intro:0,lvl:'l',neu:''},RING=false,AC=null,tk=0;
try{const m=JSON.parse(localStorage.getItem('am-meta')||'null');if(m&&m.cases)META=Object.assign(META,m);}catch(e){}
if(LV[META.lvl])LVL=META.lvl;
const save=()=>{try{localStorage.setItem('am-meta',JSON.stringify(META));}catch(e){}};
const RANKS=[[0,'Anwärterin'],[1,'Ermittlerin'],[3,'Sonderermittlerin'],[5,'Chefermittlerin'],[8,'Leitende Ermittlerin']];
const solved=()=>META.cases.filter(c=>c.w).length;
const rank=n=>RANKS.filter(r=>n>=r[0]).pop()[1];
const zslug=n=>'z_'+n.split(' ').pop().toLowerCase();
const PRIS={brandt:'Glück gehabt, Frau Ermittlerin. Beim nächsten Mal bin ich schneller.',montecalvo:'Ein Missverständnis. Mein Anwalt klärt das beim Abendessen.',holt:'Wie lange dauert das hier? Ich habe einen Liegeplatz, der kostet.',wolkow:'Sie haben gut gespielt. Aber die Partie ist noch nicht zu Ende.',oduya:'Ohne die Gitter würden Sie nicht so nah herankommen.',ravensburg:'Ich habe nur den Wagen gefahren. Na gut, und den Rest auch.',lindqvist:'Vesper holt uns nicht heraus. Vesper holt nie jemanden heraus.',aldani:'Diese Zelle ist eine Zumutung. Kein Samt, kein Spiegel, kein Publikum.'};
const HUB=[['Telefon',39,37,'tel'],['Pinnwand',16,72,'board'],['Aktenschrank',88,35,'cab'],['Dienstmarke',92,86,'badge']];
const CELLPOS=[[12,5,58,0],[25,5,58,1],[37,4,60,0],[49,5,58,1],[60,4,58,0],[72,5,58,1],[83,4,58,1],[93,5,56,0],[6,20,46,0],[18,21,45,1],[31,20,46,0],[43,21,45,1],[55,20,46,0],[66,21,45,1],[78,20,46,0],[89,21,45,1]];
function ring(){if(!voiceOn)return;try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();const t=AC.currentTime;[0,.5].forEach(o=>{[440,480].forEach(f=>{const os=AC.createOscillator(),g=AC.createGain();os.frequency.value=f;os.type='sine';g.gain.setValueAtTime(0,t+o);g.gain.linearRampToValueAtTime(.07,t+o+.03);g.gain.setValueAtTime(.07,t+o+.33);g.gain.linearRampToValueAtTime(0,t+o+.38);os.connect(g);g.connect(AC.destination);os.start(t+o);os.stop(t+o+.4);});});}catch(e){}}
function el(tag,cls,txt){const e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e;}
function sheet(title,body,cls){closeSheet();const s=el('div','sheet');s.id='sheet';s.setAttribute('role','dialog');s.setAttribute('aria-label',title);const i=el('div','in '+(cls||''));const h=el('div','sh');h.append(el('h2','',title));const x=el('button','tog','Schließen');x.type='button';x.onclick=closeSheet;h.append(x);i.append(h,body);s.append(i);const t0=performance.now();s.addEventListener('click',e=>{if(performance.now()-t0<500){e.stopPropagation();e.preventDefault();}},true);s.onclick=e=>{if(e.target===s)closeSheet();};document.body.append(s);s._fit=()=>{const L=i.querySelector('.pins')||(body.classList.contains('lst')&&body.querySelector('.row')?body:null);if(L)pager(i,L,.7);else fitZoom(i,.3);};s._fit();x.focus();}
function closeSheet(){const s=$('sheet');if(s)s.remove();}
function hubSay(text,clips){say('Direktorin Halberg','am Telefon',text,clips);}
const active=()=>S.started&&!S.over;
function office(kind,promo,done){if(MODE==='case'&&active()){if(S.busy)return;S.back=S.scene;}MODE='office';document.body.dataset.mode='office';const act=active()&&!kind;if(!act){S.started=false;S.over=false;S.busy=false;S.decoy=null;}closeSheet();$('titlecard').classList.add('gone');document.querySelectorAll('.stampbig,.card,.raid').forEach(x=>x.remove());figKey='';
  setScene('buero','Büro Meridian','Zentrale');RING=!done&&!act;
  if(act){stopAudio();say('Büro Meridian','Zentrale','Der Fall läuft weiter. Hier können Sie in Ruhe an der Pinnwand nachdenken. Die Uhr steht, solange Sie im Büro sind.');render();return;}
  if(kind==='win')hubSay('Willkommen zurück. Saubere Arbeit. Die Akte wandert in den Schrank, die Prämie auf Ihr Konto.'+(promo?'\n\nUnd noch etwas: Sie sind befördert worden. Glückwunsch. Ihr neuer Rang: '+rank(solved())+'.':'')+(done?'\n\nDas war das letzte Mitglied. Der Zirkel ist zerschlagen. Nur Vesper Nachtigall fehlt uns noch. Aber das ist eine andere Akte.':''),['h_win'].concat(promo?['h_rank']:[],done?['h_end']:[]));
  else if(kind==='lose')hubSay('Das ging daneben. Die Akte bleibt offen. Schlafen Sie eine Nacht darüber, dann machen wir weiter.',['h_lose']);
  else if(!META.intro){META.intro=1;save();hubSay('Willkommen im Büro Meridian. Sehen Sie sich in Ruhe um: Pinnwand, Aktenschrank, Zellentrakt. Wenn das Telefon klingelt, wird es ernst.',['h_office']);}
  else say('Büro Meridian','Zentrale','Das Telefon klingelt.');
  render();if(done)setTimeout(ending,1200);}
function cell(){MODE='cell';document.body.dataset.mode='cell';figKey='';stopAudio();setScene('zelle','Zellentrakt','Büro Meridian');const n=META.arrested.length;
  if(META.neu)hubSay('Im Zellentrakt wird es voller. So gefällt mir das.',['h_cell']);
  else say('Zellentrakt','Büro Meridian',n?n+' von '+ALLSUS.length+' Mitgliedern des Zirkels sitzen ein. Tippen Sie eine Person an.':'Die Zelle ist leer. Noch.');render();}
function stageHub(){const key=MODE+'|'+camOn+'|'+META.arrested.length+'|'+RING;if(key===figKey)return;figKey=key;heroKill();
  document.querySelectorAll('.fig:not(.out),.item,.card,.hot,.bars,.phone,.waves').forEach(f=>f.remove());
  const st=$('cam'+camOn).querySelector('.stg');
  if(MODE==='office')HUB.forEach(h=>{const b=el('button','hot hub'+(h[3]==='tel'&&RING?' ring':''));b.type='button';b.style.left=h[1]+'%';b.style.bottom=h[2]+'%';b.setAttribute('aria-label',h[0]);const f=()=>hub(h[3]);b._act=f;b.onclick=e=>{if(!e||e.detail===0)f();};b.append(el('span','',h[0]));st.append(b);});
  if(MODE==='office'&&RING){st.append(el('i','phone'));const w=el('i','waves');w.append(el('i'),el('i'));st.append(w);}
  if(MODE==='cell'){META.arrested.forEach((n,i)=>{const p=CELLPOS[i%16],sl=zslug(n),f=()=>{say(n,'Zirkel, in Gewahrsam',PRIS[sl.slice(2)]||PRIS2[sl.slice(2)]||'Kein Kommentar.',[],sl);};
      const b=mkFig(sl,p,p[3],'dunkel',n+' ansprechen',n+', Mitglied des Zirkels, in der Zelle',f,'ext pris'+(i%3===1?' pace':'')+(META.neu===n?' arrive':''));st.append(b);});
    const bars=el('i','bars'+(META.neu?' slam':''));st.append(bars);if(META.neu){META.neu='';save();}}
}
function hub(w){if(w==='tel'){if(RING)offers();else say('Büro Meridian','Zentrale',active()?'Halberg ruft erst wieder an, wenn der laufende Fall abgeschlossen ist.':'Die Leitung ist still.');}else if(w==='board')board();else if(w==='cab')cabinet();else if(w==='badge')badge();else if(w==='cell')cell();}
function offers(){const starts=shuffle(Object.keys(CITY).filter(k=>CITY[k].start)).slice(0,3),first=!META.cases.length;
  hubSay(first?'Büro Meridian, Halberg am Apparat. Der Zirkel hat wieder zugeschlagen. Auf meinem Tisch liegen drei Akten. Suchen Sie sich einen Fall aus.':'Halberg hier. Es gibt neue Arbeit für Sie. Drei Akten, Ihre Wahl.',[first?'h_call':'h_call2']);
  const g=el('div','offers');starts.forEach(id=>{const c=CITY[id],b=el('button','offer');b.type='button';b.append(el('small','','AKTE · '+c.name.toUpperCase()),el('b','',c.start.fall),el('span','','Gestohlen: '+c.start.beute+'.'),el('em','','Prämie ab '+BASE[LVL].toLocaleString('de-DE')+' · Stufe '+LV[LVL].n));b.onclick=()=>{closeSheet();startCase(id);};g.append(b);});
  sheet('Welchen Fall übernehmen Sie?',g);}
const BASE={l:1000,m:1800,s:3000};
function startCase(id){RING=false;let free=ALLSUS.filter(s=>!META.arrested.includes(s.name));if(!free.length)free=ALLSUS.slice();const cu=free[Math.floor(Math.random()*free.length)];
  SUSPECTS=shuffle(free.filter(x=>x!==cu)).slice(0,7).concat(cu).sort((a,b)=>a.name.localeCompare(b.name,'de'));newGame(id);S.culprit=cu;begin();}
function backToOffice(){const win=!!S.win,rest=Math.max(0,DEAD-S.t),p=win?BASE[LVL]+25*rest:0,c0=CITY[S.route[0]],before=rank(solved());
  META.cases.unshift({f:c0.start.fall,c:c0.name,b:c0.start.beute,w:win,who:S.culprit.name,ha:S.warrant||'',rest,lvl:LVL,p,d:new Date().toLocaleDateString('de-DE')});
  let done=false;if(win){META.money+=p;if(!META.arrested.includes(S.culprit.name)){META.arrested.push(S.culprit.name);META.neu=S.culprit.name;}done=META.arrested.length>=ALLSUS.length&&!META.end;if(done)META.end=1;}
  save();office(win?'win':'lose',rank(solved())!==before,done);}
function ending(){const d=el('div','lst');d.append(el('p','','Alle '+ALLSUS.length+' Mitglieder des Zirkels sitzen im Zellentrakt. Die Beute aus '+solved()+' Fällen ist sichergestellt.'),el('p','','Ihr Rang: '+rank(solved())+' · Prämien gesamt: '+META.money.toLocaleString('de-DE')),el('p','','Sie können weiter Fälle übernehmen. Vesper Nachtigall ist noch frei.'));sheet('Der Zirkel ist zerschlagen',d);}
function resume(){if(!active())return;MODE='case';document.body.dataset.mode='case';figKey='';closeSheet();stopAudio();const c=cityNow();
  if(S.decoy)setScene('flughafen','Flughafen',CITY[S.decoy].name+', '+CITY[S.decoy].land);else{const k=+String(S.back||c.id+'0').slice(-1)||0;setScene(c.id+k,c.orte[k].ort,c.name+', '+c.land);}
  say('Direktorin Halberg','per Funk','Zurück im Einsatz. Die Frist läuft.');render();}
function board(){const d=el('div','cork'),act=active();
  if(act){const c0=CITY[S.route[0]];d.append(el('h3','','Laufender Fall: '+c0.start.fall));const g=el('div','pins');
    if(!S.notes.length)g.append(el('p','nopin',LV[LVL].notes?'Noch keine Hinweise. Befragen Sie Zeugen und sehen Sie sich um.':'Auf Stufe Schwer hängt hier nur, was Sie sich selbst merken.'));
    S.notes.slice().reverse().forEach((n,i)=>{const p=el('div','pin'+(n.zeuge==='Fundstück'?' fund':''));p.style.setProperty('--r',((i*37)%7-3)+'deg');p.append(el('small','',n.stadt+' · '+n.zeuge),el('span','',n.text));g.append(p);});d.append(g);
    if(S.warrant)d.append(el('p','stmp','Haftbefehl: '+S.warrant));}
  d.append(el('h3','',act?'Verdächtige in diesem Fall':'Der Zirkel'));const m=act&&LV[LVL].count?matches():ALLSUS,z=el('div','mug');
  (act?SUSPECTS:ALLSUS).forEach(s=>{const a=META.arrested.includes(s.name),c=el('div','mg'+(a?' in':'')+(!a&&!m.includes(s)?' off':''));const im=new Image();im.src='figuren/'+zslug(s.name)+'.webp';im.alt='Zirkel-Mitglied '+s.name;im.loading='lazy';c.append(im,el('b','',s.name),el('small','',a?'in Gewahrsam':(act&&LV[LVL].count&&!m.includes(s)?'passt nicht':'auf freiem Fuß')));z.append(c);});
  d.append(z);sheet('Pinnwand',d,'corkin');}
function cabinet(){const d=el('div','lst');if(!META.cases.length)d.append(el('p','','Der Schrank ist leer. Ihr erster Fall wartet am Telefon.'));
  META.cases.forEach(c=>{const r=el('div','row '+(c.w?'ok':'no'));r.append(el('b','',c.f),el('span','',c.w?'Gelöst · festgenommen: '+c.who+' · '+c.rest+' h vor Fristende':'Offen · entkommen: '+c.who+(c.ha&&c.ha!==c.who?' · Haftbefehl auf '+c.ha:'')),el('small','',c.d+' · '+c.c+' · Stufe '+LV[c.lvl].n+(c.w?' · Prämie '+c.p.toLocaleString('de-DE'):'')));d.append(r);});sheet('Aktenschrank',d);}
function badge(){const n=solved(),nx=RANKS.find(r=>r[0]>n),d=el('div','lst');d.append(el('p','big',rank(n)),el('p','',n+' gelöste Fälle von '+META.cases.length+' · '+META.arrested.length+' von '+ALLSUS.length+' Zirkel-Mitgliedern gefasst'),el('p','','Prämien gesamt: '+META.money.toLocaleString('de-DE')),el('p','',nx?'Nächster Rang: '+nx[1]+' ab '+nx[0]+' gelösten Fällen':'Höchster Rang erreicht.'));
  const loot=META.cases.filter(c=>c.w);if(loot.length){d.append(el('h3','','Sichergestellte Beute'));const u=el('ul','');loot.forEach(c=>u.append(el('li','',c.b.charAt(0).toUpperCase()+c.b.slice(1)+' ('+c.c+')')));d.append(u);}sheet('Dienstmarke',d);}
function settings(){const d=el('div','lst'),g=el('div','lv');g.setAttribute('role','group');g.setAttribute('aria-label','Schwierigkeit');const info=el('p','hint',LV[LVL].d);
  Object.keys(LV).forEach(k=>{const x=el('button','',LV[k].n);x.type='button';x.setAttribute('aria-pressed',k===(META.lvl||LVL));x.onclick=()=>{META.lvl=k;save();if(MODE!=='case')LVL=k;g.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',b===x));info.textContent=LV[k].d+(MODE==='case'?' Gilt ab dem nächsten Fall.':'');};g.append(x);});
  d.append(el('h3','','Schwierigkeit'),g,info,el('h3','','Spielstand'));const r=el('button','act','Spielstand zurücksetzen');r.type='button';let arm=false;r.onclick=()=>{if(!arm){arm=true;r.textContent='Wirklich alles löschen? Noch einmal tippen.';return;}META={cases:[],arrested:[],money:0,intro:0,lvl:LVL,neu:''};save();closeSheet();office();};d.append(r);sheet('Einstellungen',d);}
/* ---------- Freie Weltkarte, Verkehrsmittel, Reisekasse ---------- */
const TRAVEL=[{n:'Frachtmaschine',d:'Mitflug, kostenlos',t:h=>h+8,c:h=>0},{n:'Linienflug',d:'mit Wartezeit',t:h=>h+2,c:h=>100+15*h},{n:'Charterjet',d:'sofort startklar',t:h=>Math.max(1,Math.round(h*.6)),c:h=>600+90*h}];
function book(to,mode){if(S.over||S.busy)return;const from=S.decoy||cityNow().id,h=hours(from,to),cost=mode.c(h);if(cost>S.cash+META.money)return;
  const a=Math.min(S.cash,cost);S.cash-=a;if(cost>a){META.money-=cost-a;save();}closeSheet();travel(to,mode.t(h),to===S.route[S.i+1]&&!isFinal());}
function worldmap(){if(S.over||S.busy)return;const here=S.decoy||cityNow().id,d=el('div','wm'),cv=document.createElement('canvas');cv.width=960;cv.height=540;cv.setAttribute('role','img');cv.setAttribute('aria-label','Weltkarte mit allen Städten');
  const g=cv.getContext('2d'),chips=el('div','wmc'),opt=el('div','wmo'),info=el('p','wmh','Tippen Sie eine Stadt an. Spesen '+S.cash.toLocaleString('de-DE')+' · Prämien '+META.money.toLocaleString('de-DE'));let sel='';
  const ids=Object.keys(CITY).filter(k=>k!==here).sort((a,b)=>hours(here,a)-hours(here,b));
  const draw=()=>{g.fillStyle='#0b101b';g.fillRect(0,0,960,540);g.fillStyle='#2b3b5a';for(let y=0;y<MH;y++)for(let x=0;x<MW;x++)if(land(x,y)){g.beginPath();g.arc(x*8+4,30+y*8+4,2.3,0,6.3);g.fill();}
    if(sel){const a=proj(...CITY[here].co),b=proj(...CITY[sel].co);g.strokeStyle='rgba(242,180,85,.8)';g.setLineDash([6,7]);g.lineWidth=2.5;g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(b[0],b[1]);g.stroke();g.setLineDash([]);}
    Object.keys(CITY).forEach(k=>{const p=proj(...CITY[k].co),me=k===here,on=k===sel;g.fillStyle=me?'#f2b455':on?'#fff':'#58c7bd';g.beginPath();g.arc(p[0],p[1],me||on?9:7,0,6.3);g.fill();if(me||on){g.strokeStyle=g.fillStyle;g.lineWidth=2;g.beginPath();g.arc(p[0],p[1],15,0,6.3);g.stroke();}
      g.fillStyle=me?'#f2b455':'#eef1f6';g.font=(me||on?'700 ':'500 ')+'24px "IBM Plex Sans",sans-serif';const r=p[0]>780||['paris','marrakesch','peking'].includes(k);g.textAlign=r?'right':'left';g.fillText(CITY[k].name,p[0]+(r?-16:16),p[1]+8);});};
  const pick=k=>{sel=k;draw();chips.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.k===k));opt.innerHTML='';const h=hours(here,k);info.textContent='Nach '+CITY[k].name+', '+CITY[k].land+' · reine Flugzeit '+h+' h · Spesen '+S.cash.toLocaleString('de-DE')+' · Prämien '+META.money.toLocaleString('de-DE');
    TRAVEL.forEach(mo=>{const c=mo.c(h),b=el('button','');b.type='button';b.append(el('b','',mo.n),el('span','',mo.d),el('em','',mo.t(h)+' h · '+(c?c.toLocaleString('de-DE'):'gratis')));b.disabled=c>S.cash+META.money;b.onclick=()=>book(k,mo);opt.append(b);});const sh=$('sheet');if(sh&&sh._fit)sh._fit();};
  ids.forEach(k=>{const b=el('button','',CITY[k].name);b.type='button';b.dataset.k=k;b.setAttribute('aria-pressed','false');b.onclick=()=>pick(k);chips.append(b);});
  cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect(),x=(e.clientX-r.left)/r.width*960,y=(e.clientY-r.top)/r.height*540;let best='',bd=70;ids.forEach(k=>{const p=proj(...CITY[k].co),q=Math.hypot(p[0]-x,p[1]-y);if(q<bd){bd=q;best=k;}});if(best)pick(best);});
  draw();d.append(cv,info,chips,opt);sheet('Weltkarte',d);}
function renderHub(){const A=$('actions');A.innerHTML='';const hc=$('hubchip');if(hc){hc.textContent='';hc.append(el('span','',rank(solved())),el('span','',META.arrested.length+' von '+ALLSUS.length+' gefasst'),el('span','','Prämien '+META.money.toLocaleString('de-DE')));}
  if(MODE==='title')return;
  if(MODE==='cell'){const b=box('Zellentrakt');b.append(btn('Zurück ins Büro','',()=>office()));A.append(b);return;}
  const b=box('Büro Meridian');if(active())b.append(btn('Zurück zum Fall',cityNow().name,resume,'here'));if(RING)b.append(btn('Telefon abnehmen','es klingelt',()=>hub('tel'),'here'));
  b.append(btn('Pinnwand','',()=>hub('board')),btn('Aktenschrank',META.cases.length?META.cases.length+' Akten':'',()=>hub('cab')),btn('Zellentrakt',META.arrested.length+' von '+ALLSUS.length+(META.neu?' · neu':''),()=>hub('cell')),btn('Dienstmarke',rank(solved()),()=>hub('badge')));A.append(b);}
function boot(){const hd=document.querySelector('header'),hud=document.querySelector('.hud');
  const IC={ton:'<path d="M4 9v6h4l5 4V5L8 9H4z"/><path class="w" d="M16.5 9a4 4 0 010 6M19 6.5a8 8 0 010 11"/><path class="x" d="M17 9l5 6M22 9l-5 6"/>',buero:'<path d="M3 21h18M5 21V5l7-2v18M12 9h7v12M8 8h1M8 12h1M8 16h1M15 13h1M15 17h1"/>',pin:'<path d="M9 4h6l-1 6 3 3H7l3-3-1-6zM12 13v7"/>',gear:'<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>'};
  const ib=(k,label,fn,cls)=>{const b=el('button','ib '+(cls||''));b.type='button';b.setAttribute('aria-label',label);b.title=label;b.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+IC[k]+'</svg>';b.onclick=fn;return b;};
  const icons=el('div','icons'),tr=el('div','timerow'),hc=el('div','');hc.id='hubchip';
  tr.innerHTML='<span class="chip tnow">Jetzt <b id="clock"></b></span><span class="tmid">Frist <b id="frist"></b></span><span class="tleft" id="leftchip">noch <b id="remain"></b></span>';
  const vb=ib('ton','Stimmen an oder aus',()=>{voiceOn=!voiceOn;vb.setAttribute('aria-pressed',voiceOn);if(!voiceOn){stopAudio();$('face').classList.remove('talk');}});vb.id='voice';vb.setAttribute('aria-pressed','true');
  icons.append(vb,ib('buero','Ins Büro',()=>{if(active())office();},'casebtn'),ib('pin','Pinnwand',board,'casebtn'),ib('gear','Einstellungen',settings));
  if(hud)hud.remove();hd.append(tr,hc,icons);
  const sb=el('button','act big startbtn','Spiel starten');sb.type='button';sb.onclick=()=>{try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();}catch(e){}sb.remove();office();};$('titlecard').append(sb);
  newGame();MODE='title';document.body.dataset.mode='title';document.querySelector('h1 small').textContent='Büro Meridian';document.querySelector('#titlecard em').textContent='Ein Fall für das Büro Meridian';setScene('buero','','');render();
  setInterval(()=>{tk++;if(MODE==='office'&&RING&&!$('face').classList.contains('talk')&&!$('sheet')&&tk%5===0)ring();},1000);}
function chase(done){if(window.SKIPCHASE){done();return;}
  S.busy=true;S.pend=null;render();
  const sc=$('scene'),ov=el('div','chase'),cv=document.createElement('canvas'),hint=el('div','chint'),skip=el('button','cskip','Überspringen · 2 h');skip.type='button';
  cv.setAttribute('role','img');cv.setAttribute('aria-label','Verfolgungsjagd: Die Ermittlerin rennt der flüchtenden Person hinterher');
  hint.innerHTML='<b>Die Person flieht!</b><span>Tippen oder Leertaste = springen. Dreimal stolpern und sie entkommt.</span><em>Tippen zum Start</em>';
  ov.append(cv,hint,skip);sc.append(ov);
  say('Direktorin Halberg','per Funk','Sie rennt! Hinterher, lassen Sie sie nicht entkommen.');
  const g=cv.getContext('2d'),H=540;let W=960,k=1;
  const size=()=>{const r=ov.getBoundingClientRect(),d=Math.min(2,devicePixelRatio||1);cv.width=Math.max(2,Math.round(r.width*d));cv.height=Math.max(2,Math.round(r.height*d));k=cv.height/H;W=cv.width/k;};size();
  const ld=n=>{const i=new Image();i.src='figuren/'+n+'.webp';return i;},HF=['heldin_w1','heldin_w2','heldin_w3','heldin_w2'].map(ld),TF=['dieb_1','dieb_2','dieb_3','dieb_4'].map(ld),bg=$('cam'+camOn).querySelector('img');
  const V={l:400,m:470,s:540}[LVL],RATE={l:7.5,m:6.5,s:5.6}[LVL],GY=H*.9;
  let on=false,end=0,gap=100,hits=0,y=0,vy=0,stun=0,dist=0,last=0,raf=0,obs=[],next=700,tEnd=0,flash=0;
  const jump=()=>{if(end)return;if(!on){on=true;hint.remove();last=performance.now();return;}if(y===0){vy=-1080;}};
  const key=e=>{if(e.code==='Space'||e.code==='ArrowUp'||e.code==='Enter'){if(document.activeElement===skip&&e.code!=='ArrowUp')return;e.preventDefault();jump();}};
  const stop=e=>{e.stopPropagation();};
  ov.addEventListener('pointerdown',e=>{e.stopPropagation();if(e.target===skip)return;e.preventDefault();jump();});ov.addEventListener('pointerup',stop);ov.addEventListener('click',stop);
  document.addEventListener('keydown',key);addEventListener('resize',size);
  const close=()=>{cancelAnimationFrame(raf);document.removeEventListener('keydown',key);removeEventListener('resize',size);ov.remove();S.busy=false;};
  const lost=()=>{close();S.busy=true;S.pend=done;advance(3);if(timeUp()){S.pend=null;render();return;}
    say('Direktorin Halberg','per Funk','Entwischt! Die Person ist in einer Seitengasse verschwunden. Das hat uns 3 Stunden gekostet.\n\nUnsere Leute haben sie wieder im Blick. Nehmen Sie die Verfolgung noch einmal auf.');render();};
  skip.onclick=e=>{e.stopPropagation();close();advance(2);if(timeUp()){render();return;}done();render();};
  const ob=(o,x)=>{g.save();g.translate(x,GY);g.lineWidth=3;g.strokeStyle='#1a120a';
    if(o.t===0){g.fillStyle='#8a5a2b';g.fillRect(-o.w/2,-o.h,o.w,o.h);g.strokeRect(-o.w/2,-o.h,o.w,o.h);g.beginPath();g.moveTo(-o.w/2,-o.h);g.lineTo(o.w/2,0);g.moveTo(o.w/2,-o.h);g.lineTo(-o.w/2,0);g.stroke();}
    else if(o.t===1){g.fillStyle='#6b3f1d';g.beginPath();g.ellipse(0,-o.h/2,o.w/2,o.h/2,0,0,6.3);g.fill();g.stroke();g.strokeStyle='#c9a15a';g.beginPath();g.moveTo(-o.w/2+3,-o.h*.7);g.lineTo(o.w/2-3,-o.h*.7);g.moveTo(-o.w/2+3,-o.h*.3);g.lineTo(o.w/2-3,-o.h*.3);g.stroke();}
    else{g.fillStyle='#b5483a';g.fillRect(-o.w/2,-o.h,o.w,o.h*.55);g.strokeRect(-o.w/2,-o.h,o.w,o.h*.55);g.fillStyle='#2a2f38';g.beginPath();g.arc(-o.w*.28,-o.h*.22,o.h*.22,0,6.3);g.arc(o.w*.28,-o.h*.22,o.h*.22,0,6.3);g.fill();}
    g.restore();};
  const spr=(im,x,fy,h,rot,a)=>{if(!im.complete||!im.naturalWidth)return;const w=h*im.naturalWidth/im.naturalHeight;g.save();g.translate(x,fy);if(rot)g.rotate(rot);g.globalAlpha=a;g.drawImage(im,-w/2,-h,w,h);g.restore();};
  const frame=now=>{raf=requestAnimationFrame(frame);const dt=on&&!end?Math.min(.05,Math.max(0,(now-last)/1000)):0;last=now;
    if(dt){dist+=V*dt;gap-=RATE*dt;stun=Math.max(0,stun-dt);flash=Math.max(0,flash-dt);
      vy+=3100*dt;y+=vy*dt;if(y>0){y=0;vy=0;}
      next-=V*dt;if(next<=0){const t=Math.floor(Math.random()*3);obs.push({x:W+80,t,w:[58,46,96][t],h:[58,70,56][t],hit:0});next=Math.max(V*1.05,520+Math.random()*(LVL==='l'?520:LVL==='m'?400:300));}
      const hx=W*.2;obs.forEach(o=>{o.x-=V*dt;if(!o.hit&&Math.abs(o.x-hx)<o.w/2+16&&-y<o.h-8){o.hit=1;hits++;gap+=16;stun=.55;flash=.3;if(navigator.vibrate)try{navigator.vibrate(60);}catch(e){}}});
      obs=obs.filter(o=>o.x>-120);
      if(hits>=3){end=2;tEnd=now;}else if(gap<=0){gap=0;end=1;tEnd=now;}}
    g.setTransform(k,0,0,k,0,0);g.clearRect(0,0,W,H);
    if(bg&&bg.naturalWidth){const tw=H*bg.naturalWidth/bg.naturalHeight,off=(dist*.35)%(2*tw);for(let i=-1,x=-off;x<W;i++,x+=tw){const n=Math.round((x+off)/tw);g.save();if(n%2){g.translate(x+tw,0);g.scale(-1,1);g.drawImage(bg,0,0,tw+1,H);}else g.drawImage(bg,x,0,tw+1,H);g.restore();}}
    g.fillStyle='rgba(8,12,22,.38)';g.fillRect(0,0,W,H);g.fillStyle='rgba(10,13,20,.82)';g.fillRect(0,GY-6,W,H-GY+6);g.fillStyle='rgba(242,180,85,.5)';for(let x=-(dist%120);x<W;x+=120)g.fillRect(x,GY+18,56,5);
    const hx=W*.2,tx=hx+110+(W*.72-110)*Math.min(1.25,gap/100),ti=Math.floor(dist/42)%4,hi=Math.floor(dist/48)%4;
    let ty=0;obs.forEach(o=>{const d=Math.abs(o.x-tx);if(d<110)ty=Math.max(ty,Math.cos(d/110*1.57)*(o.h+30));ob(o,o.x);});
    spr(TF[on?ti:0],end===1?hx+70:tx,GY-ty+4,H*.36,0,1);
    spr(HF[y<0?2:on?hi:1],hx,GY+y+2,H*.44,y<0?-.1:stun?.12:0,stun&&Math.floor(now/70)%2?.45:1);
    if(flash){g.fillStyle='rgba(181,72,58,'+(flash*.9).toFixed(2)+')';g.fillRect(0,0,W,H);}
    g.fillStyle='rgba(13,19,32,.8)';g.fillRect(16,14,220,40);g.fillStyle='#eef1f6';g.font='600 15px "IBM Plex Sans",sans-serif';g.textAlign='left';g.fillText('Abstand',26,39);g.fillStyle='#2b3b5a';g.fillRect(96,27,128,14);g.fillStyle=gap>70?'#b5483a':'#f2b455';g.fillRect(96,27,128*Math.max(0,Math.min(1,gap/125)),14);
    for(let i=0;i<3;i++){g.beginPath();g.arc(266+i*26,34,9,0,6.3);g.fillStyle=i<3-hits?'#58c7bd':'rgba(238,241,246,.2)';g.fill();}
    if(end){g.fillStyle='rgba(8,12,22,.55)';g.fillRect(0,0,W,H);g.fillStyle=end===1?'#f2b455':'#e8796b';g.font='700 64px "Playfair Display",Georgia,serif';g.textAlign='center';g.fillText(end===1?'Gefasst!':'Entwischt!',W/2,H/2);
      if(now-tEnd>1100){if(end===1){close();done();render();}else lost();}}};
  ov._st=()=>({obs,gap,hits,W,y,on,end,V});raf=requestAnimationFrame(frame);}
const PLAN=__PLAN__;
function citymap(){if(S.over||S.busy||S.decoy)return;const c=cityNow(),P=PLAN[c.id],cur=S.scene.indexOf(c.id)===0?+S.scene.slice(-1):0,d=el('div','cm'),m=el('div','cmm'),wh=walkH();
  const im=new Image();im.src='plan/'+c.id+'.webp';im.alt='Gemalter Stadtplan von '+c.name+' mit den drei Schauplätzen';im.draggable=false;m.append(im);
  const me=el('i','cmme');me.style.left=P[cur][0]+'%';me.style.top=P[cur][1]+'%';let gone=false;
  c.orte.forEach((o,k)=>{const dn=S.seen[S.i+'_'+k],b=el('button','cmp'+(k===cur?' here':'')+(dn?' done':'')+(P[k][1]<32?' dn':'')+(P[k][0]<22?' l':P[k][0]>78?' r':''));b.type='button';b.style.left=P[k][0]+'%';b.style.top=P[k][1]+'%';
    b.append(el('b','',o.ort),el('small','',k===cur?'Sie sind hier':(dn?'notiert · ':'')+(wh?wh+' h Fußweg':'hingehen')));
    b.onclick=()=>{if(gone)return;if(k===cur){closeSheet();return;}gone=true;if(calm){closeSheet();goTo(k);return;}me.style.left=P[k][0]+'%';me.style.top=P[k][1]+'%';setTimeout(()=>{closeSheet();goTo(k);},760);};m.append(b);});
  m.append(me);const fl=btn('Zum Flughafen','Weltkarte öffnen',()=>{closeSheet();worldmap();},'here');fl.disabled=isFinal();
  d.append(el('p','wmh',c.name+', '+c.land+' · '+(wh?'Jeder Fußweg kostet '+wh+' Stunde.':'Auf Stufe Leicht kosten Fußwege keine Zeit.')),m,fl);sheet('Stadtplan',d);$('sheet')._fit();const z=parseFloat(d.style.zoom)||1;m.querySelectorAll('.cmp').forEach(b=>{const R=m.getBoundingClientRect();let r=b.getBoundingClientRect();if(r.top<R.top+2){b.classList.add('dn');}else if(r.bottom>R.bottom-2){b.classList.remove('dn');}r=b.getBoundingClientRect();const dx=r.left<R.left+2?R.left+2-r.left:r.right>R.right-2?R.right-2-r.right:0;if(dx)b.style.marginLeft=(dx/z)+'px';});}
