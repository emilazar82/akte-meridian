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
function sheet(title,body,cls){closeSheet();const s=el('div','sheet');s.id='sheet';s.setAttribute('role','dialog');s.setAttribute('aria-label',title);const i=el('div','in '+(cls||''));const h=el('div','sh');h.append(el('h2','',title));const x=el('button','tog','Schließen');x.type='button';x.onclick=closeSheet;h.append(x);i.append(h,body);s.append(i);const t0=performance.now();s.addEventListener('click',e=>{if(performance.now()-t0<500){e.stopPropagation();e.preventDefault();}},true);s.onclick=e=>{if(e.target===s)closeSheet();};document.body.append(s);x.focus();}
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
    TRAVEL.forEach(mo=>{const c=mo.c(h),b=el('button','');b.type='button';b.append(el('b','',mo.n),el('span','',mo.d),el('em','',mo.t(h)+' h · '+(c?c.toLocaleString('de-DE'):'gratis')));b.disabled=c>S.cash+META.money;b.onclick=()=>book(k,mo);opt.append(b);});};
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
