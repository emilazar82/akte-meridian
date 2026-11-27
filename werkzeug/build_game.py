import json,re,os
from figdata import FIG,EX,IATA,CUR
from harddata import HARD,NIX
from hotdata import HOT
D=json.load(open('data.json'));C=D['C']
old=open('../index_v2.html').read() if os.path.exists('../index_v2.html') else open('../index.html').read()
if not os.path.exists('../index_v2.html'): open('../index_v2.html','w').write(old)
head=old[:old.index('<script>')]
mask=re.search(r"const LAND='([0-9a-f]+)'",old).group(1)
mid=old[old.index('/* ---------- Szene ---------- */'):old.index('/* ---------- Spiel ---------- */')]
mid=mid.replace("if(id==='wien0')el.setAttribute('data-police','');","if(id==='wien0'&&S&&S.route[0]==='wien')el.setAttribute('data-police','');")
mid=mid.replace("const show=()=>{$('cam'+camOn).classList.remove('on');el.classList.add('on');camOn=next;};","const show=()=>{$('cam'+camOn).classList.remove('on');el.classList.add('on');camOn=next;stageFig();};")
assert 'stageFig();};' in mid
mid=mid.replace("const a=COORD[from],b=COORD[to];","const a=CITY[from].co,b=CITY[to].co;").replace("g.fillText(n,p[0]+","g.fillText(CITY[n].name,p[0]+").replace("g.fillText('Flug nach '+to,34,58);","g.fillText('Flug nach '+CITY[to].name,34,58);")
assert "CITY[from].co" in mid and "CITY[n].name" in mid and "CITY[to].name,34" in mid
dur=json.load(open('dur3.json')) if os.path.exists('dur3.json') else {}
cities={}
for c in C.values():
    cities[c['id']]=dict(id=c['id'],name=c['name'],land=c['land'],co=c['co'],attr=c['attr'],trait=c['trait'],nxt=c['nxt'],hint=c['hint'],
        iata=IATA[c['id']],hard=HARD[c['id']],nix=NIX[c['id']],cur=CUR.get(c['id'],''),
        orte=[dict(ort=w['ort'],zeuge=w['zeuge'],rolle=w['rolle'],p=w['p']) for w in c['orte']],start=c['start'])
OV={'wien>istanbul':['Kurz vor dem Alarm fragte mich jemand nach einer Stadt, die auf zwei Kontinenten liegt. Komische Frage für ein Museum.','Die Person hat Euro in Lira getauscht und wollte wissen, wann die Fähren über den Bosporus fahren.','Auf dem Tisch lag ein Reiseführer. Vorn drauf eine rote Flagge mit weißem Halbmond und Stern.'],
'istanbul>kairo':['Bezahlen wollte sie mit ägyptischen Pfund. Die nehme ich nicht, also ist sie weitergezogen.','Sie fragte, wie man am schnellsten an den Nil kommt. Von hier aus mit dem Schiff jedenfalls nicht.','Sie erzählte von Pyramiden, die man vom Stadtrand aus sehen kann. Da wollte sie als Nächstes hin.'],
'kairo>mumbai':['Sie hat Safran gekauft und mit Rupien bezahlen wollen. Rupien, hier in Kairo!','Sie will in die Stadt am Arabischen Meer, in der mehr Filme gedreht werden als irgendwo sonst.','Im Besucherbuch hat jemand eine Flagge gezeichnet: Safrangelb, Weiß und Grün, in der Mitte ein blaues Rad.'],
'mumbai>tokio':['Sie hat mich gefragt, wo man hier Yen bekommt. Ich habe sie zur Bank am Hafen geschickt.','Sie hofft auf klares Wetter, sagte sie. Sie will unbedingt den Fuji sehen.','An ihrem Koffer klebte ein Aufkleber: weiße Flagge mit einem roten Kreis in der Mitte.'],
'tokio>lima':['Sie stand vor mir in der Wechselstube und wollte Sol. Die Angestellte musste erst nachschlagen, welches Land das ist.','Sie will in eine Hauptstadt am Pazifik. Von dort brechen die Leute nach Machu Picchu auf.','Sie suchte einen Anstecker mit einer Flagge: drei senkrechte Streifen, rot, weiß, rot.']}
FOV={'lima':['Jemand, auf den das passt, ist eben hier vorbeigerannt. Passen Sie auf sich auf.','So jemand hat gerade nach einem Frachter gefragt, der heute Nacht ausläuft. Sie sind ganz nah dran.','Vor zehn Minuten wollte jemand ein goldenes Salzfass schätzen lassen. Die Person kann nicht weit sein.']}
FOV['lima'][2]='__GEN__'

COMPACT=r"""
.tabs{display:none}
.cam{transition:opacity 1.1s ease,transform 1.1s cubic-bezier(.3,.1,.2,1)}
.cam.zoom{transform:scale(1.32)}
.mv{container-type:size}
.stg{position:absolute;left:50%;top:50%;width:max(100cqw,177.78cqh);aspect-ratio:16/9;transform:translate(-50%,-50%)}
.fig{position:absolute;padding:0;margin:0;border:0;background:none;cursor:pointer;transform:translateX(-50%);-webkit-tap-highlight-color:transparent;animation:figin .7s cubic-bezier(.2,.8,.3,1) both;z-index:2}
.fig.out{animation:figout .45s ease both;pointer-events:none}
.fig img{height:100%;width:auto;display:block;transform-origin:50% 100%;animation:breathe 3.8s ease-in-out infinite;filter:var(--ton,none) drop-shadow(0 0 0 rgba(242,180,85,0));transition:filter .25s;user-select:none;-webkit-user-drag:none}
.fig.full::before{content:"";position:absolute;left:8%;right:8%;bottom:-2.5%;height:7%;border-radius:50%;background:radial-gradient(rgba(0,0,0,.55),rgba(0,0,0,0) 70%)}
.fig.nacht{--ton:url(#f-nacht)}
.fig.dunkel{--ton:url(#f-dunkel)}
.fig.warm{--ton:url(#f-warm)}
.fig.abend{--ton:url(#f-abend)}
.fig:hover img,.fig:focus-visible img{filter:var(--ton,none) drop-shadow(0 0 7px rgba(242,180,85,.95))}
.fig:focus-visible{outline:none}
.fig.talk img{animation:talk .42s ease-in-out infinite alternate}
.fig.chip img{border-radius:50%;aspect-ratio:1;object-fit:cover;box-shadow:0 0 0 3px var(--teal,#58c7bd),0 6px 18px rgba(0,0,0,.6);animation:none}
.fig.chip{animation:figin .7s both,float 3s ease-in-out .7s infinite}
.bub{position:absolute;left:50%;top:-13%;transform:translateX(-50%);min-width:1.5em;height:1.5em;line-height:1.5em;border-radius:50%;background:var(--amber);color:#1c1405;font:700 clamp(12px,1.6cqw,20px)/1.5 var(--body);font-style:normal;text-align:center;box-shadow:0 3px 10px rgba(0,0,0,.5);animation:hop 1.1s ease-in-out infinite}
.fig.seen .bub,.fig.talk .bub,.fig:disabled .bub{display:none}
.act.here{border-color:var(--amber)}
.scene{touch-action:manipulation}
.fig{translate:calc(var(--px,0)*var(--par,1)*-.5cqw) 0;transition:translate .5s ease-out}
.fig img{animation-delay:var(--d,0s)}
.fig img.flip{scale:-1 1}
.fig.ext img{animation-duration:4.6s}
.chase{position:absolute;inset:0;z-index:40;background:#0b101b;touch-action:none;cursor:pointer;user-select:none;-webkit-user-select:none}
.chase canvas{position:absolute;inset:0;width:100%;height:100%;display:block}
.chint{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:min(86%,420px);background:rgba(13,19,32,.92);border:1px solid var(--amber);border-radius:12px;padding:14px 16px;text-align:center;display:flex;flex-direction:column;gap:6px;pointer-events:none}
.chint b{font-family:var(--display);font-size:22px;color:var(--amber)}.chint span{font-size:14px}.chint em{font-style:normal;font-weight:600;color:var(--teal,#58c7bd);animation:blink 1s ease-in-out infinite}
.cskip{position:absolute;right:8px;top:8px;z-index:2;background:rgba(13,19,32,.85);color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:6px 12px;font:inherit;font-size:12.5px;cursor:pointer;min-height:32px}
@keyframes blink{50%{opacity:.35}}
@media (max-height:620px) and (orientation:portrait){.scene{max-height:32vh!important}body.pano .scene{max-height:44dvh!important}.dialog{max-height:19vh!important}}
.hero{position:absolute;aspect-ratio:328/520;transform:translateX(-50%);pointer-events:none;translate:calc(var(--px,0)*var(--par,1)*-.5cqw) 0;transition:translate .5s ease-out;animation:figin .5s ease both}
.hero img{position:absolute;inset:0;width:100%;height:100%;transform-origin:50% 100%;filter:var(--ton,none);user-select:none;-webkit-user-drag:none;animation:breathe 3.8s ease-in-out infinite}
.hero.flip img{scale:-1 1}
.hero.walk img{animation:herobob .28s ease-in-out infinite}
.hero::before{content:"";position:absolute;left:14%;right:14%;bottom:-2.5%;height:7%;border-radius:50%;background:radial-gradient(rgba(0,0,0,.55),rgba(0,0,0,0) 70%)}
.hero.nacht{--ton:url(#f-nacht)}.hero.dunkel{--ton:url(#f-dunkel)}.hero.warm{--ton:url(#f-warm)}.hero.abend{--ton:url(#f-abend)}
@keyframes herobob{50%{transform:translateY(-1.3%)}}
@media (prefers-reduced-motion:reduce){.hero,.hero img{animation:none!important;translate:none}}
.fig:disabled{cursor:default}
.item{position:absolute;width:5.2%;aspect-ratio:1.5;padding:0;border:0;cursor:pointer;z-index:120;transform:translateX(-50%) rotate(-12deg);background:linear-gradient(135deg,#fdf6e3,#e6d5ad);border-radius:2px;box-shadow:0 2px 6px rgba(0,0,0,.6);animation:glint 1.8s ease-in-out infinite}
.item::after{content:"";position:absolute;inset:18% 14%;border-top:1px solid #8a6f3c;border-bottom:1px solid #8a6f3c}
.item.out,.card.out{display:none}
@keyframes glint{0%,100%{box-shadow:0 2px 6px rgba(0,0,0,.6),0 0 0 0 rgba(242,180,85,.0)}50%{box-shadow:0 2px 6px rgba(0,0,0,.6),0 0 14px 5px rgba(242,180,85,.85)}}
.card{position:absolute;left:50%;top:42%;z-index:6;transform:translate(-50%,-50%) rotate(-4deg);display:flex;flex-direction:column;gap:4px;align-items:flex-start;text-align:left;min-width:44%;max-width:86%;padding:12px 18px;border:0;cursor:pointer;color:#2a2113;background:linear-gradient(180deg,#fbf3dc,#ecdcb4);border-radius:6px;box-shadow:0 14px 40px rgba(0,0,0,.65);font-family:var(--type);animation:cardin .5s cubic-bezier(.2,1.4,.4,1) both}
.card small{font-size:11px;letter-spacing:.18em;color:#7a2f25}
.card b{font-size:clamp(18px,3.4vw,40px);letter-spacing:.06em}.card.beleg b{font-size:clamp(15px,2.4vw,28px)}
.card span{font-size:12px;color:#6b5a3a}
.card.ticket{border-left:10px solid #b5483a}
.card.beleg{border-top:6px dashed #8a6f3c}
@keyframes cardin{from{opacity:0;transform:translate(-50%,20%) rotate(8deg) scale(.6)}to{opacity:1;transform:translate(-50%,-50%) rotate(-4deg)}}
.stampbig.tmp{color:var(--amber);right:auto;left:50%;top:38%;margin-left:-4.2em;animation:stamp .5s cubic-bezier(.2,1.6,.4,1) both,fade .5s 1.6s both}
@keyframes fade{to{opacity:0}}
.raid{position:absolute;inset:0;pointer-events:none;z-index:5;mix-blend-mode:screen;animation:raid .5s steps(1) 6}
@keyframes raid{0%{background:radial-gradient(circle at 20% 60%,rgba(60,110,255,.55),transparent 60%)}50%{background:radial-gradient(circle at 80% 60%,rgba(255,60,60,.5),transparent 60%)}}
.hot{position:absolute;width:11%;aspect-ratio:1;padding:0;border:0;background:none;border-radius:50%;cursor:pointer;transform:translate(-50%,50%);z-index:1;-webkit-tap-highlight-color:transparent}
.hot::after{content:"";position:absolute;left:50%;top:50%;width:9px;height:9px;margin:-4.5px;border-radius:50%;background:#fff3c4;box-shadow:0 0 8px 3px rgba(255,226,150,.9);animation:twinkle 2.6s ease-in-out infinite}
.hot:nth-of-type(2n)::after{animation-delay:-.9s}.hot:nth-of-type(3n)::after{animation-delay:-1.7s}
.hot.seen::after{opacity:.25;animation:none;box-shadow:none}
.hot:hover::after,.hot:focus-visible::after{transform:scale(1.6)}
.hot:focus-visible{outline:2px solid var(--amber)}
body[data-lv="s"] .hot::after{display:none}
@keyframes twinkle{0%,100%{opacity:.25;transform:scale(.6)}50%{opacity:1;transform:scale(1.15)}}
.item{width:8%;animation:glint 1.3s ease-in-out infinite,hopi 1.3s ease-in-out infinite}
@keyframes hopi{50%{margin-bottom:1.2%}}
@media (prefers-reduced-motion:reduce){.hot::after{animation:none!important;opacity:.8}}
header{display:flex;flex-wrap:nowrap;align-items:center;gap:6px 14px}
header h1{flex:0 0 auto}
.icons{display:flex;gap:6px;flex:0 0 auto}
.ib{width:36px;height:36px;border-radius:50%;border:1px solid var(--line);background:transparent;color:#c9d3e6;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;padding:0;transition:border-color .15s,color .15s}
.ib svg{width:18px;height:18px}.ib:hover,.ib:focus-visible{border-color:var(--amber);color:var(--amber)}
.ib[aria-pressed="true"]{border-color:var(--teal);color:var(--teal)}
.ib[aria-pressed="true"] .x,.ib[aria-pressed="false"] .w{display:none}
.timerow,#hubchip{flex:1 1 auto;min-width:0;display:flex;justify-content:flex-end;align-items:baseline;gap:18px;font-size:14px;color:var(--text);white-space:nowrap}
.timerow b,#hubchip b{color:var(--amber);font-weight:600}
.timerow .chip{border:0;background:none;padding:0;border-radius:6px;font-size:inherit}
.timerow .tmid{color:var(--muted);font-size:12.5px}.timerow .tmid b{color:var(--muted);font-weight:400}
.tleft.warn b{color:var(--red)}
#hubchip{display:none;color:var(--muted);font-size:13px}
body:not([data-mode="case"]) #hubchip{display:flex}
body:not([data-mode="case"]) .timerow,body:not([data-mode="case"]) .casebtn,body:not([data-mode="case"]) .akte,body:not([data-mode="case"]) .tabs,body:not([data-mode="case"]) .bar{display:none!important}
body:not([data-mode="case"]) .main{grid-template-columns:minmax(0,1fr)}
body:not([data-mode="case"]) .actions{display:block!important}
body:not([data-mode="case"]) .box{display:flex!important}
.startbtn{margin-top:18px;min-width:min(260px,70%);justify-content:center;pointer-events:auto}
body[data-mode="title"] .actions,body[data-mode="title"] .dialog{visibility:hidden}
.hud .tog,.hud .chip{white-space:nowrap}
.gear .sm{display:none}
.hot.hub{width:15%;z-index:3}
.hot.hub span{position:absolute;left:50%;top:100%;transform:translate(-50%,-30%);white-space:nowrap;font:600 clamp(10px,1.5cqw,15px)/1 var(--body);color:#fff3c4;background:rgba(8,12,20,.72);padding:3px 7px;border-radius:99px;pointer-events:none}
.hot.hub::after{width:12px;height:12px;margin:-6px}
.hot.ring::after{display:none}
.hot.hub::after{width:8px;height:8px;margin:-4px}
.phone{position:absolute;left:34.6%;bottom:30.5%;width:10.4%;height:15%;z-index:2;pointer-events:none;background:url(szenen/buero.webp) 38.62% 64.12%/961.5% 666.7% no-repeat;-webkit-mask-image:radial-gradient(ellipse at 50% 52%,#000 52%,transparent 72%);mask-image:radial-gradient(ellipse at 50% 52%,#000 52%,transparent 72%);animation:vib 1.6s linear infinite;transform-origin:50% 80%}
.phone::after{content:"";position:absolute;inset:0}
@keyframes vib{0%,52%,100%{transform:none}4%,12%,20%,28%,36%,44%{transform:translate(-1.6%,-1%) rotate(-3.2deg)}8%,16%,24%,32%,40%,48%{transform:translate(1.6%,-1%) rotate(3.2deg)}}
.waves{position:absolute;left:39.8%;bottom:45%;width:7%;aspect-ratio:1;z-index:2;pointer-events:none;transform:translateX(-50%)}
.waves i{position:absolute;left:50%;bottom:0;width:60%;aspect-ratio:2;border:2px solid #ffe2a0;border-bottom:0;border-radius:999px 999px 0 0;transform:translateX(-50%);opacity:0;animation:wav 1.6s ease-out infinite}
.waves i:nth-child(2){width:100%;animation-delay:.18s}
@keyframes wav{0%{opacity:0;transform:translateX(-50%) translateY(30%) scale(.6)}15%,45%{opacity:.9}60%,100%{opacity:0;transform:translateX(-50%) translateY(-40%) scale(1)}}
.bars{position:absolute;inset:0;z-index:300;pointer-events:none;background:repeating-linear-gradient(90deg,transparent 0 5.2%,rgba(10,12,16,.92) 5.2% 5.5%,#5d6470 5.5% 6.1%,#2a2f38 6.1% 6.6%,transparent 6.6% 7.2%),linear-gradient(#2a2f38,#2a2f38) 0 12%/100% 1.6% no-repeat,linear-gradient(#2a2f38,#2a2f38) 0 86%/100% 1.6% no-repeat}
.bars.slam{animation:slam .9s cubic-bezier(.6,0,.3,1) 1.4s both}
@keyframes slam{from{transform:translateX(-70%)}80%{transform:translateX(1.2%)}to{transform:none}}
.fig.pris.pace{animation:figin .7s both,pace 11s ease-in-out .7s infinite}
@keyframes pace{0%,100%{margin-left:0}50%{margin-left:5%}}
.fig.pris.arrive{animation:arrive 1.6s cubic-bezier(.3,.7,.3,1) both}
@keyframes arrive{from{opacity:0;transform:translateX(-50%) translateX(-60cqw)}to{opacity:1;transform:translateX(-50%)}}
.sheet{position:fixed;inset:0;z-index:60;background:rgba(5,8,14,.74);display:flex;align-items:center;justify-content:center;padding:10px;animation:rise .25s ease both}
.sheet .in{width:100%;max-width:820px;max-height:100%;overflow:hidden;background:linear-gradient(180deg,#1b2740,#141c2e);border:1px solid var(--line);border-radius:12px;padding:12px 16px 16px;box-shadow:0 24px 70px rgba(0,0,0,.7)}
.sheet .sh{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px}
.sheet h2{font-family:var(--display);font-size:22px;margin:0;color:var(--amber)}
.sheet h3{font-family:var(--type);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--amber);margin:14px 0 8px}
.offers{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}
.offer{display:flex;flex-direction:column;gap:6px;text-align:left;padding:14px;border-radius:8px;border:0;border-left:8px solid #b5483a;background:linear-gradient(180deg,#fbf3dc,#ecdcb4);color:#2a2113;cursor:pointer;font-family:var(--type);transition:transform .15s}
.offer:hover,.offer:focus-visible{transform:translateY(-3px) rotate(-.6deg)}
.offer small{font-size:11px;letter-spacing:.16em;color:#7a2f25}.offer b{font-family:var(--display);font-size:20px;line-height:1.15}.offer span{font-size:13px}.offer em{font-size:12px;color:#6b5a3a;font-style:normal}
.in.corkin{background:#7a5532 radial-gradient(circle at 20% 30%,rgba(255,220,160,.12),transparent 40%);border:10px solid #3d2a17}
.in.corkin h2,.in.corkin h3{color:#ffe9b8}
.pins{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px 12px;padding:6px 2px}
.pin{position:relative;background:#fbf3dc;color:#2a2113;padding:14px 10px 10px;font-family:var(--type);font-size:13px;line-height:1.35;box-shadow:0 4px 10px rgba(0,0,0,.45);transform:rotate(var(--r,0deg));display:flex;flex-direction:column;gap:4px}
.pin::before{content:"";position:absolute;left:50%;top:-5px;width:12px;height:12px;margin-left:-6px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ff8a7a,#a8261b);box-shadow:0 2px 3px rgba(0,0,0,.5)}
.pin small{font-size:10.5px;letter-spacing:.08em;color:#7a2f25;text-transform:uppercase}.pin.fund{background:#e7f1e4}
.nopin,.stmp{color:#ffe9b8;font-family:var(--type);font-size:14px}.stmp{border:2px solid #ffb199;color:#ffb199;display:inline-block;padding:4px 10px;transform:rotate(-2deg)}
.mug{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.mg{position:relative;background:#fbf3dc;color:#2a2113;padding:6px 6px 8px;text-align:center;font-family:var(--type);box-shadow:0 4px 10px rgba(0,0,0,.45);display:flex;flex-direction:column;gap:2px;overflow:hidden}
.mg img{width:100%;height:clamp(38px,11vh,120px);object-fit:cover;object-position:50% 4%;background:#39465c}
.mg b{font-size:12px}.mg small{font-size:10.5px;color:#6b5a3a}
.mg.off{opacity:.45}.mg.in small{color:#a8261b;font-weight:700}
.mg.in::after{content:"";position:absolute;left:-10%;right:-10%;top:38%;height:3px;background:#a8261b;transform:rotate(-24deg)}
.lst{display:flex;flex-direction:column;gap:8px;font-size:15px}.lst p{margin:0}.lst .big{font-family:var(--display);font-size:28px;color:var(--amber)}.lst ul{margin:0;padding-left:18px}
.row{display:flex;flex-direction:column;gap:2px;padding:10px 12px;border-radius:8px;background:#0e1524;border-left:5px solid #7be0a2}.row.no{border-left-color:var(--red)}.row small{color:var(--muted)}
@media (max-width:1100px),(max-height:700px){.mug{grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}.sheet h2{font-size:18px}.hud .tog{font-size:11px;padding:3px 8px}}
@media (prefers-reduced-motion:reduce){.phone,.waves i,.bars.slam,.fig.pris{animation:none!important}.waves i{opacity:.8}}
.wm canvas{width:auto;max-width:100%;max-height:52vh;margin:0 auto;height:auto;display:block;border-radius:8px;background:#0b101b;cursor:pointer;touch-action:manipulation}
.wmc{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.wmc button{background:transparent;color:var(--text);border:1px solid var(--line);border-radius:99px;padding:5px 11px;font:inherit;font-size:13px;cursor:pointer;min-height:32px}
.wmc button[aria-pressed="true"]{background:var(--amber);color:#1c1405;border-color:var(--amber);font-weight:600}
.wmo{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}
.wmo button{display:flex;flex-direction:column;gap:3px;text-align:left;padding:10px 12px;border-radius:8px;border:1px solid var(--line);background:#0e1524;color:var(--text);font:inherit;cursor:pointer}
.wmo button b{font-size:15px}.wmo button span{font-size:13px;color:var(--muted)}.wmo button em{font-style:normal;color:var(--amber);font-size:13px}
.wmo button:disabled{opacity:.45;cursor:default}
.wmh{font-size:13px;color:var(--muted);margin:0 0 8px}
.chip.tick{animation:tick .6s ease}
@keyframes tick{30%{transform:scale(1.12);box-shadow:0 0 14px rgba(242,180,85,.7)}}
@media (prefers-reduced-motion:reduce){.item,.card,.raid,.chip.tick{animation:none!important}.fig{translate:none}}
@keyframes figin{from{opacity:0;transform:translateX(-50%) translateX(9%)}to{opacity:1;transform:translateX(-50%)}}
@keyframes figout{to{opacity:0;transform:translateX(-50%) translateX(-6%)}}
@keyframes breathe{50%{transform:scaleY(1.014) scaleX(.996)}}
@keyframes talk{from{transform:translateY(0) rotate(-.5deg)}to{transform:translateY(-1.3%) rotate(.6deg)}}
@keyframes hop{50%{transform:translateX(-50%) translateY(-28%)}}
@keyframes float{50%{margin-bottom:1.2%}}
@media (prefers-reduced-motion:reduce){.fig,.fig img,.bub{animation:none!important}.cam.zoom{transform:none}}
.lv{display:flex;gap:6px}.lv button{flex:1;min-width:0;background:transparent;color:var(--muted);border:1px solid var(--line);border-radius:8px;padding:8px 4px;font:inherit;font-size:14px;min-height:38px;cursor:pointer}.lv button[aria-pressed="true"]{background:var(--amber);color:#1c1405;border-color:var(--amber);font-weight:600}
#map{object-fit:contain;z-index:4}
[hidden]{display:none!important}
.pano{position:absolute;inset:0;width:100%;height:100%;z-index:5;display:block;touch-action:none;cursor:pointer}
.pbtn{--ps:clamp(38px,8.5vmin,58px);position:absolute;bottom:8px;z-index:8;width:var(--ps);height:var(--ps);padding:0;border-radius:50%;border:2px solid rgba(242,180,85,.8);background:rgba(13,19,32,.72);color:var(--amber);font:inherit;font-size:calc(var(--ps)*.4);line-height:1;cursor:pointer;touch-action:none;user-select:none;-webkit-user-select:none;-webkit-tap-highlight-color:transparent}
.pbtn.on{background:var(--amber);color:#1c1405}
.pbtn.l{left:8px}.pbtn.r{left:calc(16px + var(--ps))}.pbtn.j{right:8px}
.pbtn.a{right:calc(16px + var(--ps));width:auto;padding:0 14px;border-radius:99px;border-color:#58c7bd;color:#58c7bd;font-size:13px;font-weight:600;touch-action:manipulation}
body.flying .pano,body.flying .pbtn{display:none}
body.pano .dialog{z-index:8}body.pano .place{z-index:7;top:8px!important;bottom:auto!important}body.pano .vig{display:none}
.stampbig,.card,.raid{z-index:9}
.act{min-width:0}.act>span{min-width:0;overflow-wrap:anywhere}.act small{white-space:normal;min-width:0;text-align:right;overflow-wrap:anywhere}
.cm{display:flex;flex-direction:column;gap:8px}
.cmm{position:relative;width:min(100%,calc((100dvh - 200px)*1.7778));min-width:240px;aspect-ratio:16/9;margin:0 auto;border-radius:8px;overflow:hidden;box-shadow:0 6px 18px rgba(0,0,0,.5)}
.cmm img{width:100%;height:100%;display:block;object-fit:cover}
.cmp{position:absolute;transform:translate(-50%,calc(-100% - 10px));display:flex;flex-direction:column;align-items:center;background:rgba(13,19,32,.92);color:#f6e7c8;border:1.5px solid var(--amber);border-radius:9px;padding:3px 9px 4px;font:inherit;line-height:1.25;cursor:pointer;white-space:nowrap;z-index:2}
.cmp::after{content:"";position:absolute;left:50%;bottom:-16px;width:12px;height:12px;margin-left:-8px;border-radius:50%;background:#b5483a;border:2px solid #fff;box-shadow:0 2px 4px rgba(0,0,0,.6)}
.cmp b{font-size:13px;font-weight:600}.cmp small{font-size:11px;color:#b9c2d3}
.cmp.dn{transform:translate(-50%,10px)}.cmp.dn::after{bottom:auto;top:-16px}
.cmp.l{transform:translate(-14%,calc(-100% - 10px))}.cmp.l::after{left:14%}.cmp.l.dn{transform:translate(-14%,10px)}
.cmp.r{transform:translate(-86%,calc(-100% - 10px))}.cmp.r::after{left:86%}.cmp.r.dn{transform:translate(-86%,10px)}
.cmp.here{border-color:#58c7bd}.cmp.done b::after{content:" ✓";color:#58c7bd}
.cmp:hover,.cmp:focus-visible{background:var(--amber);color:#1c1405}.cmp:hover small,.cmp:focus-visible small{color:#1c1405}
.cmme{position:absolute;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;background:var(--amber);border:3px solid #1c1405;box-shadow:0 0 0 4px rgba(242,180,85,.45);transition:left .7s ease-in-out,top .7s ease-in-out;z-index:3;pointer-events:none}
@media (max-width:1100px),(max-height:700px){.cmp b{font-size:11.5px}.cmp small{font-size:10px}.cmp{padding:2px 7px 3px}}
@media (prefers-reduced-motion:reduce){.cmme{transition:none}}
@media (max-height:520px) and (orientation:landscape){.cm{display:grid;grid-template-columns:auto minmax(110px,1fr);align-items:center;gap:8px 12px}.cm .wmh{grid-column:1/-1;margin:0}.cmm{width:min(100%,calc((100dvh - 128px)*1.7778))}.cm .act{flex-direction:column;align-items:flex-start}}
.notes li.new{animation-name:fadein}@keyframes fadein{from{opacity:0}to{opacity:1}}
@media (orientation:landscape){.sheet .mug{grid-template-columns:repeat(8,minmax(0,1fr))}}
.sheet{animation-name:fadein}
html,body{height:100%;overflow:hidden}
.wrap{height:100%;height:100dvh}
.pgr{display:flex;align-items:center;justify-content:center;gap:10px;font-size:13px;margin-top:6px}
.pgr button{min-width:40px;min-height:34px;border-radius:8px;border:1px solid currentColor;background:transparent;color:inherit;font:inherit;font-size:18px;line-height:1;cursor:pointer}
.pgr button:disabled{opacity:.3;cursor:default}
.exit{position:absolute;top:58px;z-index:6;display:flex;align-items:center;gap:6px;max-width:42%;padding:7px 12px;border:1px solid rgba(242,180,85,.75);background:rgba(13,19,32,.82);color:#f6e7c8;font:inherit;font-size:13.5px;font-weight:600;cursor:pointer;-webkit-tap-highlight-color:transparent;animation:rise .5s ease .6s both}
.exit span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.exit i{font-style:normal;color:var(--amber);font-size:19px;line-height:1;animation:nudge 1.3s ease-in-out infinite}
.exit.l{left:0;border-left:0;border-radius:0 99px 99px 0;padding-left:8px}
.exit.r{right:0;border-right:0;border-radius:99px 0 0 99px;padding-right:8px;flex-direction:row-reverse}
.exit.r i{animation-name:nudger}
.exit:hover,.exit:focus-visible{background:rgba(242,180,85,.95);color:#1c1405}.exit:hover i,.exit:focus-visible i{color:#1c1405}
body.flying .exit,.exit:disabled{display:none}
@keyframes nudge{50%{transform:translateX(-4px)}}@keyframes nudger{50%{transform:translateX(4px)}}
@media (prefers-reduced-motion:reduce){.exit,.exit i{animation:none!important}}
/* Grosse Fenster: alles auf einer Seite, nichts scrollt */
@media (min-width:1101px) and (min-height:701px){
  .wrap{max-width:1500px;padding:12px 16px;gap:10px}
  .main{flex:1;min-height:0;display:grid;gap:12px;align-items:stretch;grid-template-columns:minmax(0,1fr) minmax(300px,30%);grid-template-rows:minmax(0,1fr) auto;grid-template-areas:"scene akte" "actions akte"}
  body:not([data-mode="case"]) .main{grid-template-areas:"scene" "actions"}
  .left{display:contents}
  .scene{grid-area:scene;aspect-ratio:auto;height:auto;min-height:0}
  .dialog{grid-area:scene;align-self:end;z-index:3;margin:10px;min-height:0;max-height:55%;overflow:hidden;background:rgba(13,19,32,.9);pointer-events:none;transition:opacity .5s}
  .dialog.idle{opacity:0}
  body.flying .dialog,body.flying .place{visibility:hidden}
  .place{top:12px;bottom:auto}
  body.pano .dialog{align-self:start;margin-top:64px;max-height:40%}
  .actions{grid-area:actions;min-height:0;max-height:34vh;overflow:hidden;display:grid;grid-template-columns:minmax(0,3fr) minmax(0,1.2fr);gap:12px}
  body:not([data-mode="case"]) .actions{max-height:30vh}
  .box{padding:10px 12px}
  .box.q{flex-direction:row;flex-wrap:wrap;align-items:stretch}
  .box.q .act:not(.big){flex-direction:column;align-items:flex-start;justify-content:center;gap:1px}
  .box.q>*{flex:1 1 0;min-width:0}.box.q>h2,.box.q>p,.box.q>.lv{flex:1 1 100%}
  .akte{grid-area:akte;min-height:0;overflow:hidden;gap:10px}
}
/* Handy und kleine Fenster: alles auf einem Bildschirm, kein Seiten-Scrollen */
@media (max-width:1100px),(max-height:700px){
  html,body{height:100%;overflow:hidden}
  .wrap{height:100%;max-width:none;padding:6px 8px;gap:5px}
  header{flex-wrap:nowrap;gap:4px 8px}
  h1{font-size:15px;white-space:nowrap}
  h1 small{display:none}
  .hud{gap:4px;flex-wrap:nowrap;justify-content:flex-end;min-width:0}
  .chip,.tog{font-size:11px;padding:3px 8px}
  .bar{height:3px;flex:none}
  .main{flex:1;min-height:0;display:grid;gap:6px;align-items:stretch;grid-template-columns:minmax(0,1fr) minmax(215px,34%);grid-template-rows:auto minmax(0,1fr);grid-template-areas:"scene tabs" "scene panel"}
  .left{display:contents}
  .scene{grid-area:scene;aspect-ratio:auto;height:auto;align-self:stretch;min-height:0;border-radius:8px}
  .dialog{grid-area:scene;align-self:end;z-index:3;margin:6px;min-height:0;max-height:62%;overflow:hidden;padding:8px;gap:8px;background:rgba(13,19,32,.88)}
  body.flying .dialog,body.flying .place{visibility:hidden}
  body.pano .dialog{align-self:start;margin-top:44px;max-height:46%}
  .ib{width:32px;height:32px}.ib svg{width:16px;height:16px}
  .wm canvas{max-height:38vh;width:auto;max-width:100%;margin:0 auto}
  .timerow,#hubchip{font-size:13px;gap:12px}
  .dialog{pointer-events:none;transition:opacity .5s}
  .dialog.idle{opacity:0}
  .item{width:9%}
  .exit{top:46px;font-size:12px;padding:5px 9px;max-width:36%}.exit i{font-size:16px}
  .card{top:36%;padding:8px 12px}
  .face{flex-basis:52px;height:52px;border-radius:8px}
  .who{font-size:13px;margin:0}.who span{font-size:12px}
  .txt{font-size:13.5px;line-height:1.35}
  .place{top:8px;bottom:auto;left:10px;font-size:15px}.place small{font-size:11px}
  .vig{background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(5,8,14,.5) 100%)}
  .titlecard{justify-content:flex-start;padding-top:5%}
  .titlecard b{font-size:clamp(28px,8vw,56px)}
  .stampbig{font-size:19px;top:10%}
  .tabs{grid-area:tabs;display:flex;gap:4px}
  .tabs button{flex:1 1 auto;min-width:0;background:var(--panel);color:var(--muted);border:1px solid var(--line);border-radius:7px;padding:7px 3px;font-size:11.5px;cursor:pointer;white-space:nowrap}
  .tabs button[aria-pressed="true"]{color:#1c1405;background:var(--amber);border-color:var(--amber);font-weight:600}
  .actions,.akte{grid-area:panel;min-height:0;overflow:hidden}
  .actions{display:block}
  .box{padding:8px;gap:6px;min-height:100%}
  .box h2{display:none}
  .act{min-height:38px;padding:6px 10px;font-size:14px}
  .act small{font-size:12px}
  .akte{padding:8px 10px;gap:8px;box-shadow:none}
  .akte h2{display:none}
  .fields{gap:4px 8px;font-size:13px}
  .fields select{min-height:27px;padding:1px 4px;font-size:13px}
  .sus{display:none}.count{margin:0;font-size:13px}
  .warrant{min-height:38px;padding:8px;font-size:13px}
  .stamp,.notes,.empty{font-size:13px}
  body[data-tab="q"] .akte,body[data-tab="r"] .akte,body[data-tab="p"] .actions,body[data-tab="n"] .actions{display:none}
  body[data-tab="q"] .box.r,body[data-tab="r"] .box.q{display:none}
  body[data-tab="p"] #sec-n,body[data-tab="n"] #sec-p,body[data-tab="n"] #sec-k,body[data-tab="n"] .warrant,body[data-tab="n"] .stamp{display:none}
}
@media (max-width:1100px) and (orientation:portrait){
  header{flex-wrap:wrap}
  .wm canvas{max-height:34vh}
  .main{grid-template-columns:minmax(0,1fr);grid-template-rows:auto auto auto minmax(0,1fr);grid-template-areas:"scene" "dialog" "tabs" "panel"}
  .scene{aspect-ratio:auto;height:calc((100vw - 16px)*.5625);max-height:40vh;align-self:start}
  .dialog,body.pano .dialog{grid-area:dialog;margin:0;max-height:26vh;overflow:hidden;align-self:auto;background:var(--panel)}
  body.pano .scene{height:49dvh;max-height:49dvh}
  body.pano .dialog{max-height:19dvh}
  body.pano[data-tab="p"] .dialog,body.pano[data-tab="n"] .dialog{display:none}
  body.pano[data-tab="p"] .main,body.pano[data-tab="n"] .main{grid-template-areas:"scene" "tabs" "panel";grid-template-rows:auto auto minmax(0,1fr)}
  .place{top:auto;bottom:8px}
  header{flex-wrap:wrap}
  .wm canvas{max-height:34vh}
  header h1{flex:1 1 auto}
  .timerow,#hubchip{order:3;flex:1 1 100%;justify-content:space-between;gap:8px}
  body.flying .dialog{visibility:visible}
  .dialog{pointer-events:auto}.dialog.idle{opacity:1}
  .card{top:42%}
}
"""
FX={'wien0':'rain','tokio0':'rain','lima1':'fog','tokio1':'fog','istanbul0':'dust','kairo0':'dust','kairo2':'dust','mumbai2':'dust','wien2':'dust','newyork0':'rain','reykjavik2':'fog','peking2':'fog','marrakesch1':'dust','nairobi0':'dust','rio2':'dust','peking1':'dust','marrakesch0':'fog'}
FIGS=sorted(f[:-5] for f in os.listdir('../figuren') if f.endswith('.webp')) if os.path.isdir('../figuren') else []
sus=re.search(r"const SUSPECTS=\[.*?\n\];\n",old,re.S).group(0)
Z2=json.load(open('zirkel2.json'));Z2OK=all(os.path.exists('../figuren/z_%s.webp'%z[0].split()[-1].lower()) for z in Z2)
_extra=''.join(" ,{name:%s,haar:%s,hobby:%s,fahrzeug:%s,merkmal:%s,essen:%s}\n"%tuple(json.dumps(v,ensure_ascii=False) for v in z[:6]) for z in Z2) if Z2OK else ''
sus=sus.replace('const SUSPECTS=[','const ALLSUS=[').replace('\n];\n','\n'+_extra+'];\nlet SUSPECTS=ALLSUS.slice(0,8);\nconst PRIS2='+json.dumps({z[0].split()[-1].lower():z[7] for z in Z2},ensure_ascii=False)+';\n')
print('Zirkel:',16 if Z2OK else 8)
js=r'''
'use strict';
const ATTR=[['haar','Haarfarbe'],['hobby','Hobby'],['fahrzeug','Fahrzeug'],['merkmal','Merkmal'],['essen','Lieblingsessen']];
const CLUE=__CLUE__;
const FINAL=__FINAL__;
__SUS__const CITY=__CITY__;
const OV=__OV__;
const FOV=__FOV__;
const FX=__FX__;
const DUR=__DUR__;
const FIG=__FIG__, FIGS=__FIGS__, EX=__EX__, HOT=__HOT__;
const LAND='__MASK__';
const DAYS=['Mo','Di','Mi','Do','Fr','Sa','So'], START=9, QH=2;
const LV={l:{n:'Leicht',buf:30,dec:3,len:6,notes:1,count:1,re:1,mark:1,xh:1,d:'Viel Zeit, 4 Reiseziele. Zeugen sind markiert, das Notizbuch schreibt mit.'},
 m:{n:'Mittel',buf:16,dec:4,len:6,notes:1,count:1,re:6,mark:0,xh:1,d:'Knappe Frist, 5 Reiseziele. Den richtigen Zeugen finden Sie selbst.'},
 s:{n:'Schwer',buf:6,dec:5,len:7,notes:0,count:0,re:0,mark:0,xh:2,d:'7 Städte, kryptische Hinweise, kaum Zeitpuffer. Sie notieren selbst und haben nur einen Haftbefehl.'}};
let LVL='l',LEN=6;try{const v=localStorage.getItem('am-stufe');if(LV[v])LVL=v;}catch(e){}
const $=id=>document.getElementById(id);
const calm=matchMedia('(prefers-reduced-motion: reduce)').matches;
const ALT={flughafen:'Leere Ankunftshalle eines Flughafens bei Nacht',buero:'Gemaltes Detektivbüro bei Nacht: Ermittlerin am Schreibtisch mit Telefon, Pinnwand und Aktenschrank',zelle:'Gemalte Arrestzelle im Zellentrakt des Büros Meridian'};
Object.values(CITY).forEach(c=>c.orte.forEach((o,k)=>{ALT[c.id+k]='Gemalter Schauplatz: '+o.ort+' in '+c.name+', '+c.land;}));
let S, typing=null, voiceOn=true, camOn='A', lastNote=0, aq=[], cur=null, DEAD=0;
const AU=new Audio(),SIL='data:audio/wav;base64,UklGRrQBAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YZABAACAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA';AU.preload='auto';
{const u=()=>{if(AU._ok||cur)return;AU._ok=1;AU.src=SIL;const p=AU.play();if(p&&p.then)p.then(()=>{if(!cur)AU.pause();}).catch(()=>{AU._ok=0;});};document.addEventListener('touchend',u,true);document.addEventListener('click',u,true);}
function stopAudio(){aq=[];if(cur){cur.onended=null;cur.onerror=null;try{cur.pause();}catch(e){}cur=null;}}
function nextClip(){const id=aq.shift();if(!id){cur=null;$('face').classList.remove('talk');return;}if(!(id in DUR)){nextClip();return;}cur=AU;AU.src='ton/'+id+'.mp3';cur.onended=nextClip;cur.onerror=nextClip;const p=cur.play();if(p&&p.catch)p.catch(()=>{aq=[];cur=null;$('face').classList.remove('talk');});}
__MID__
/* ---------- Fall würfeln ---------- */
function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function hours(a,b){const r=x=>x*Math.PI/180,A=CITY[a].co,B=CITY[b].co,h=Math.sin(r(B[1]-A[1])/2)**2+Math.cos(r(A[1]))*Math.cos(r(B[1]))*Math.sin(r(B[0]-A[0])/2)**2;return Math.max(2,Math.round(12742*Math.asin(Math.sqrt(h))/800));}
function makeRoute(start){
  const go=path=>{if(path.length===LEN)return path;
    for(const n of shuffle(CITY[path[path.length-1]].nxt)){if(path.includes(n))continue;
      if(path.length<5&&path.some(x=>CITY[x].attr===CITY[n].attr))continue;
      const r=go(path.concat(n));if(r)return r;}
    return null;};
  return go([start]);
}
function step(t,h){t+=h;const hr=t%24;if(hr>=23)t+=24-hr+7;else if(hr<7)t+=7-hr;return t;}
function newGame(fix){
  const LC=LV[LVL],NA=(typeof META==='object'&&fix)?Math.max(0,8-ALLSUS.filter(x=>!META.arrested.includes(x.name)).length):0,BUF=Math.max(4,LC.buf-3*NA);LEN=LC.len;let route=null,start;const starts=Object.keys(CITY).filter(k=>CITY[k].start);
  const ps=fix;
  while(!route){start=ps&&CITY[ps]&&CITY[ps].start?ps:starts[Math.floor(Math.random()*starts.length)];route=makeRoute(start);}
  const others=Object.keys(CITY).filter(k=>!route.includes(k));
  const ziele=route.slice(0,-1).map(()=>shuffle(others).slice(0,Math.min(others.length,LC.dec+Math.floor(NA/3))));
  let t=0;for(let w=0;w<LEN;w++){let u=START;for(let i=0;i<LEN-1;i++){for(let q=0;q<3;q++)u=step(u,QH);if(i===w)u=step(u,1);u=step(u,hours(route[i],route[i+1])+2);}
    if(w===LEN-1)u=step(u,1);u=step(u,QH);u=step(u,QH);t=Math.max(t,u);}{const WB=BUF+walkH()*2*LEN;DEAD=BUF>10?Math.ceil((t+WB)/6)*6:t+WB;}
  document.body.dataset.lv=LVL;
  S={route,ziele,i:0,decoy:null,t:START,seen:{},notes:[],profile:{},warrant:null,culprit:SUSPECTS[Math.floor(Math.random()*SUSPECTS.length)],fin:0,xs:{},hs:{},cash:1500,items:route.slice(0,-1).map((r,n)=>({k:Math.floor(Math.random()*3),h:Math.floor(Math.random()*3),type:(LVL==='s'||!CITY[route[n+1]].cur||Math.random()<.5)?'ticket':'beleg',found:false})),over:false,started:false,busy:false,scene:null};
  ATTR.forEach(a=>S.profile[a[0]]='');lastNote=0;
  document.querySelectorAll('.stampbig,.card,.raid').forEach(x=>x.remove());
  const c=CITY[start],fall='Fall: '+c.start.fall;
  document.querySelector('h1 small').textContent=fall+' · '+LC.n;document.querySelector('#titlecard em').textContent=fall;
  $('titlecard').classList.remove('gone');
  setScene(start+'0','','');
  say('Direktorin Halberg','Büro Meridian','Auf Ihrem Schreibtisch liegt eine neue Akte. Nehmen Sie den Fall an, dann bekommen Sie das Briefing.');
  [start+'0','flughafen'].concat(route.flatMap(r=>[0,1,2].map(k=>r+k))).forEach(id=>{const i=new Image();i.src='szenen/'+id+'.webp';});
  route.forEach(r=>CITY[r].orte.forEach(o=>{const i=new Image();i.src='portraits/'+o.p+'.webp';}));
  render();
}
const cityNow=()=>CITY[S.route[S.i]], isFinal=()=>S.i===LEN-1;
const gh=()=>LV[LVL].mark&&S.items[S.i]&&S.items[S.i].k===0&&!S.items[S.i].found&&!isFinal()?'\n\n(Hier liegt etwas am Boden.)':'';
function begin(){MODE='case';document.body.dataset.mode='case';S.started=true;$('titlecard').classList.add('gone');const c=cityNow();setPlace(c.orte[0].ort,c.name+', '+c.land);
  say('Direktorin Halberg','Büro Meridian',c.start.text+'\n\nDer Tatort gehört Ihnen. Hören Sie sich in der Stadt um.'+gh(),['h_brief_'+c.id,'h_begin']);render();}
function fmt(t){const d=Math.floor(t/24),h=Math.floor(t%24);return DAYS[d%7]+' '+String(h).padStart(2,'0')+':00';}
function advance(h){const b=S.t;S.t+=h;const hr=S.t%24;let slept=false;if(hr>=23){S.t+=24-hr+7;slept=true;}else if(hr<7){S.t+=7-hr;slept=true;}return slept;}
function matches(){return SUSPECTS.filter(s=>!(typeof META==='object'&&MODE==='case'&&META.arrested.includes(s.name))&&ATTR.every(a=>!S.profile[a[0]]||s[a[0]]===S.profile[a[0]]));}
function initials(n){return n.replace('Dr. ','').split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase();}
function say(name,role,text,clips,pslug){
  const w=$('who');w.textContent=name;const sp=document.createElement('span');sp.textContent=role;w.append(sp);
  const f=$('face'),slug=pslug||(name==='Direktorin Halberg'?'halberg':'');
  if(f.dataset.who!==name){f.textContent='';f.dataset.who=name;
    if(slug){const im=new Image();im.src='portraits/'+slug+'.webp';im.alt='Porträt: '+name+', '+role;f.append(im);}else if(name==='Beobachtung')f.innerHTML='<svg viewBox="0 0 24 24" width="55%" height="55%" fill="none" stroke="#0d1320" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg>';else f.textContent=initials(name);
    f.classList.remove('pop');void f.offsetWidth;f.classList.add('pop');}
  S.spk=pslug||'';$('dialog').classList.remove('idle');S.quiet=0;clearInterval(typing);stopAudio();const el=$('txt');
  clips=(clips||[]).filter(c=>c in DUR);
  const speak=voiceOn&&clips.length,secs=speak?clips.reduce((n,c)=>n+DUR[c],0):0;
  if(speak){aq=clips.slice();f.classList.add('talk');nextClip();}
  el._full=text;el.textContent=text;fitAll();
  if(calm)return;
  const t0=performance.now(),total=speak?Math.min(secs*920,text.length*70):text.length*15;el.textContent='';f.classList.add('talk');
  typing=setInterval(()=>{const k=Math.ceil(text.length*Math.min(1,(performance.now()-t0)/total));el.textContent=text.slice(0,k);if(k>=text.length){clearInterval(typing);if(!cur)f.classList.remove('talk');}},30);
}
let figKey='',lastT=-1,HERO=null;
function heroKill(){panoKill();document.querySelectorAll('.exit').forEach(x=>x.remove());if(HERO){cancelAnimationFrame(HERO.raf);HERO.el.remove();HERO=null;}}
function heroPos(){HERO.el.style.left=HERO.x.toFixed(2)+'%';}
function heroFrame(n){[...HERO.el.children].forEach((im,i)=>{im.style.opacity=i===n?1:0;});}
function heroStop(){const H=HERO;H.el.classList.remove('walk');heroFrame(0);if(H.face!=null)H.el.classList.toggle('flip',H.face<H.x);const cb=H.cb;H.cb=null;if(cb)cb();}
function heroVis(){const H=HERO,s=H.el.parentElement.getBoundingClientRect(),q=$('scene').getBoundingClientRect();return [Math.max(0,(q.left-s.left)/s.width*100),Math.min(100,(q.right-s.left)/s.width*100)];}
function heroWalk(to,cb,face,free){const H=HERO;if(!H)return;if(!free){const v=heroVis();to=Math.max(v[0]+4,Math.min(v[1]-4,to));}H.cb=cb||null;H.face=face;H.tx=to;
  const d=Math.abs(to-H.x);if(calm||d<1.5){if(calm){H.x=to;heroPos();}heroStop();return;}
  H.v=Math.max(26,d/1.4);H.dir=to>H.x?1:-1;H.el.classList.add('walk');H.el.classList.toggle('flip',H.dir<0);
  if(H.raf)return;let last=performance.now();const t0=last;
  const step=now=>{if(HERO!==H||!H.el.isConnected){H.raf=0;return;}const dt=Math.min(.1,Math.max(0,(now-last)/1000));last=now;
    H.x+=H.dir*H.v*dt;if((H.tx-H.x)*H.dir<=0){H.x=H.tx;heroPos();H.raf=0;heroStop();return;}
    heroPos();heroFrame([1,2,3,2][Math.floor((now-t0)/140)%4]);H.raf=requestAnimationFrame(step);};
  H.raf=requestAnimationFrame(step);}
function heroMake(st,P){heroKill();const wx=P.w[0],h=document.createElement('div'),b=Math.max(1,P.w[1]-2);h.className='hero '+(P.t||'');
  h.style.bottom=b+'%';h.style.height=Math.min(74,P.w[2]*1.02)+'%';h.style.zIndex=101-Math.round(b);h.style.setProperty('--par',(1.4-b/40).toFixed(2));
  ['s','w1','w2','w3'].forEach((n,i)=>{const im=new Image();im.src='figuren/heldin_'+n+'.webp';im.alt=i?'':'Die Ermittlerin am Schauplatz';im.draggable=false;if(i)im.style.opacity=0;h.append(im);});
  HERO={el:h,x:0,tx:0,raf:0,cb:null};st.append(h);const v=heroVis(),w=v[1]-v[0],left=heroFrom?heroFrom<0:wx>50;heroFrom=0;
  HERO.x=HERO.tx=left?v[0]-8:v[1]+8;heroPos();heroWalk(left?v[0]+w*.14:v[1]-w*.14,null,wx);}
let heroFrom=0;
function mkExit(dir,k,o){const b=document.createElement('button');b.type='button';b.className='exit '+(dir<0?'l':'r');b.setAttribute('aria-label','Szene verlassen, weiter zu '+o.ort);
  const a=document.createElement('i');a.textContent=dir<0?'‹':'›';a.setAttribute('aria-hidden','true');const t=document.createElement('span');t.textContent=o.ort;b.append(a,t);
  const go=()=>{if(S.over||S.busy)return;heroFrom=dir;goTo(k);};
  b._act=()=>{if(S.over||S.busy)return;const H=HERO;if(!H||calm){go();return;}const v=heroVis();heroWalk(dir<0?v[0]-9:v[1]+9,go,null,true);};
  b.onclick=e=>{if(!e||e.detail===0)go();};return b;}
function heroGo(el){const H=HERO;if(!H||!H.el.isConnected||el.classList.contains('exit')){el._act();return;}
  const s=H.el.parentElement.getBoundingClientRect(),r=el.getBoundingClientRect(),cx=(r.left+r.width/2-s.left)/s.width*100,off=el.classList.contains('fig')?Math.max(8,r.width/s.width*50+3):5;
  heroWalk(H.x<cx?cx-off:cx+off,()=>{if(el.isConnected&&!el.disabled&&!el.classList.contains('out')&&!S.over&&!S.busy)el._act();},cx);}
function heroTap(x){const H=HERO;if(!H||!H.el.isConnected)return;const s=H.el.parentElement.getBoundingClientRect();heroWalk((x-s.left)/s.width*100,null,null);}
function mkFig(slug,p,flip,ton,label,alt,fn,cls){
  const has=FIGS.includes(slug),b=document.createElement('button');b.type='button';b.className='fig '+(has?'full ':'chip ')+(ton||'')+' '+(cls||'');b.dataset.p=slug;
  b.style.left=p[0]+'%';b.style.bottom=(has?p[1]:p[1]+p[2]*.55)+'%';b.style.height=(has?p[2]:20)+'%';b.style.zIndex=100-Math.round(p[1]);
  b.style.setProperty('--d',(-(Math.random()*3).toFixed(2))+'s');b.style.setProperty('--par',(1.4-p[1]/40).toFixed(2));
  b.setAttribute('aria-label',label);
  const im=new Image();im.src=(has?'figuren/':'portraits/')+slug+'.webp';im.alt=alt;im.draggable=false;if(flip&&has)im.classList.add('flip');
  b.append(im);b._act=fn;b.onclick=e=>{if(!e||e.detail===0)fn();};return b;}
function stageFig(){
  if(!S)return;if(MODE!=='case'){stageHub();return;}if(PA&&PA.T)return;const id=S.scene||'',city=id.slice(0,-1),k=+id.slice(-1),c=CITY[city],LC=LV[LVL];
  const want=S.started&&!S.decoy&&c&&c.id===cityNow().id?id:'';
  const base=want+'|'+camOn+'|'+S.i+'|'+LVL;
  if(base!==figKey){figKey=base;heroKill();
    document.querySelectorAll('.fig:not(.out),.item,.card,.hot,.phone,.waves,.bars').forEach(f=>{if(f.classList.contains('fig')){f.classList.add('out');setTimeout(()=>f.remove(),500);}else f.remove();});
    if(want){const o=c.orte[k],P=FIG[id]||{w:[66,5,58],t:'',e:[]},st=$('cam'+camOn).querySelector('.stg');
      if(PANO[id]){panoStage(id,k,c,P);}else{
      const w=mkFig(o.p,P.w,0,P.t,'Mit '+o.zeuge+' sprechen, '+o.rolle,o.zeuge+', '+o.rolle+' am Schauplatz '+o.ort,()=>ask(k),'wit');
      if(LC.mark){const bub=document.createElement('i');bub.className='bub';bub.textContent='!';w.append(bub);}
      st.append(w);heroMake(st,P);
      if(!isFinal()||1){$('scene').append(mkExit(-1,(k+2)%3,c.orte[(k+2)%3]),mkExit(1,(k+1)%3,c.orte[(k+1)%3]));}
      (P.e||[]).forEach(e=>{if(!EX[e[0]]||!FIGS.includes(e[0]))return;st.append(mkFig(e[0],[e[1],e[2],e[3]],e[4],P.t,'Mit '+EX[e[0]][0]+' sprechen',EX[e[0]][0]+' am Schauplatz '+o.ort,()=>askExtra(e[0]),'ext'));});
      (HOT[id]||[]).forEach((h,n)=>{const b=document.createElement('button');b.type='button';b.className='hot'+(S.hs[id+n]?' seen':'');b.style.left=h[1]+'%';b.style.bottom=h[2]+'%';b.setAttribute('aria-label',h[0]+' ansehen');b._act=()=>look(id,n,b);b.onclick=e=>{if(!e||e.detail===0)look(id,n,b);};st.append(b);});
      const it=S.items&&S.items[S.i];
      if(LC.mark&&it&&it.k===k&&!it.found&&!isFinal()){const b=document.createElement('button');b.type='button';b.className='item';b.setAttribute('aria-label','Fundstück ansehen');
        const x=P.w[0]+(P.w[0]>50?-24:24);b.style.left=x+'%';b.style.bottom=Math.max(2,P.w[1]-2)+'%';b._act=pick;b.onclick=e=>{if(!e||e.detail===0)pick();};st.append(b);}
      }
    }
  }
  document.querySelectorAll('.fig:not(.out)').forEach(f=>{if(f.classList.contains('wit'))f.classList.toggle('seen',!!S.seen[S.i+'_'+k]);f.disabled=!!S.over||!!S.busy;});
  if(S.t!==lastT){lastT=S.t;const ch=$('clock').parentElement;ch.classList.remove('tick');void ch.offsetWidth;ch.classList.add('tick');}
}
function askExtra(slug){if(S.over||S.busy)return;const e=EX[slug],n=(S.xs[slug]=(S.xs[slug]||0)+1)%2,slept=advance(LV[LVL].xh);
  say(e[0],'Passant',e[2][n]+(slept?'\n\n(Danach haben Sie bis 7 Uhr geschlafen.)':''),['e_'+slug+'_'+n],slug);timeUp();render();}
function look(id,n,b){if(S.over||S.busy)return;const h=HOT[id][n],it=S.items[S.i],k=+id.slice(-1);
  S.hs[id+n]=1;if(b)b.classList.add('seen');
  if(!LV[LVL].mark&&it&&it.k===k&&!it.found&&!isFinal()&&it.h===n){pick(h[0]);return;}
  say('Beobachtung',h[0],h[3]);}
function pick(wo){if(S.over||S.busy)return;const it=S.items[S.i],y=S.route[S.i+1],c=cityNow();it.found=true;advance(1);
  document.querySelectorAll('.item').forEach(x=>x.remove());
  const card=document.createElement('button');card.type='button';card.className='card '+it.type;card.setAttribute('aria-label','Fundstück schließen');
  let txt;
  if(it.type==='ticket'){card.innerHTML='<small>BORDKARTE · ABSCHNITT</small><b>'+c.iata+' → '+CITY[y].iata+'</b><span>Sitz 14C · Gate geschlossen</span>';txt='Abschnitt einer Bordkarte, Strecke '+c.iata+' → '+CITY[y].iata+'.';}
  else{card.innerHTML='<small>WECHSELSTUBE · QUITTUNG</small><b>'+CITY[y].cur+'</b><span>Betrag bar ausgezahlt</span>';txt='Quittung einer Wechselstube, ausgezahlt in: '+CITY[y].cur+'.';}
  card.onclick=e=>{if(!e||e.detail===0)card.remove();};card._t=performance.now();$('scene').append(card);
  note(c.name,'Fundstück',txt);
  say('Direktorin Halberg','per Funk','Gut gesehen. Das hat die gesuchte Person verloren.\n\nFundstück'+(typeof wo==='string'?' ('+wo+')':'')+': '+txt,['h_item']);timeUp();render();}
function walkH(){return LVL==='l'?0:1;}
function goTo(k){if(S.over||S.busy)return;const c=cityNow(),o=c.orte[k];if(S.scene===c.id+k){if(LV[LVL].mark)ask(k);return;}
  if(walkH()){advance(walkH());if(timeUp()){render();return;}}
  stopAudio();document.querySelectorAll('.card').forEach(x=>x.remove());setScene(c.id+k,o.ort,c.name+', '+c.land);
  say('Direktorin Halberg','per Funk',LV[LVL].mark?o.zeuge+' ('+o.rolle+') ist hier. Sprechen Sie die Person an.'+(S.items[S.i]&&S.items[S.i].k===k&&!S.items[S.i].found&&!isFinal()?' Außerdem liegt hier etwas am Boden.':''):'Gesucht wird hier: '+o.rolle+'. Sehen Sie sich um und sprechen Sie die richtige Person an.');render();}
setInterval(()=>{if(!S)return;const cam=$('cam'+camOn);let on=false;
  document.querySelectorAll('.fig:not(.out)').forEach(f=>{const t=$('face').classList.contains('talk')&&S.spk===f.dataset.p;f.classList.toggle('talk',t);
    if(t){on=true;if(!cam.classList.contains('zoom')){const r=cam.getBoundingClientRect(),q=f.getBoundingClientRect();cam.style.transformOrigin=((q.left+q.width/2-r.left)/r.width*100).toFixed(1)+'% '+((q.top+q.height*.3-r.top)/r.height*100).toFixed(1)+'%';}}});
  document.querySelectorAll('.cam').forEach(x=>x.classList.toggle('zoom',on&&x===cam));
  if($('face').classList.contains('talk')||!S.started||S.over)S.quiet=0;else{S.quiet=(S.quiet||0)+160;if(S.quiet>3500)$('dialog').classList.add('idle');}},160);
{let pd=null;const sc=$('scene');
  sc.addEventListener('pointerdown',e=>{pd=[e.clientX,e.clientY,performance.now()];});
  sc.addEventListener('pointerup',e=>{if(!pd)return;const dx=e.clientX-pd[0],dy=e.clientY-pd[1],dt=performance.now()-pd[2];pd=null;if(dx*dx+dy*dy>400||dt>900||!S)return;
    const x=e.clientX,y=e.clientY,card=document.querySelector('.card');
    if(card){if(performance.now()-card._t>350)card.remove();return;}
    const hit=[...document.querySelectorAll('.item,.exit,.fig:not(.out),.hot')].filter(el=>!el.disabled&&el._act).map(el=>{const r=el.getBoundingClientRect(),c=el.classList;
      if(c.contains('hot')){const d=Math.hypot(x-(r.left+r.width/2),y-(r.top+r.height/2)),rad=Math.max(r.width/2,22);return {el,ok:d<=rad,z:d<=rad*.5?500:-1};}
      if(c.contains('exit'))return {el,ok:x>=r.left&&x<=r.right&&y>=r.top-6&&y<=r.bottom+6,z:998};
      if(c.contains('item'))return {el,ok:x>=r.left-14&&x<=r.right+14&&y>=r.top-14&&y<=r.bottom+14,z:999};
      const ix=r.width*.1;return {el,ok:x>=r.left+ix&&x<=r.right-ix&&y>=r.top-4&&y<=r.bottom+4,z:+el.style.zIndex||0};}).filter(o=>o.ok).sort((a,b)=>b.z-a.z)[0];
    if(hit)heroGo(hit.el);else{heroTap(x);$('dialog').classList.remove('idle');S.quiet=0;}});
  sc.addEventListener('pointercancel',()=>{pd=null;});}
$('scene').addEventListener('pointermove',e=>{const r=$('scene').getBoundingClientRect();$('scene').style.setProperty('--px',((e.clientX-r.left)/r.width*2-1).toFixed(3));});
function note(stadt,zeuge,text){if(!LV[LVL].notes)return;S.notes.unshift({stadt,zeuge,text});}
function beute(){return CITY[S.route[0]].start.beute;}
function timeUp(){if(S.t<=DEAD)return false;finish(false,'Die Frist ist abgelaufen. Die Spur ist kalt und der Zirkel hat die Beute außer Landes gebracht.','h_time');return true;}
function finish(win,text,clip){
  if(S.over)return;S.over=true;S.win=win;say('Direktorin Halberg','Büro Meridian',text,[clip]);
  const d=document.createElement('div');d.className='stampbig '+(win?'win':'lose');d.textContent=win?'FALL GELÖST':'FALL VERLOREN';$('scene').append(d);
  if(win){const r=document.createElement('i');r.className='raid';$('scene').append(r);setTimeout(()=>r.remove(),3200);}
}
function line(c,k){
  if(isFinal()){const t=(FOV[c.id]||FINAL)[k];return {text:t,clips:['f_'+c.id+'_'+k]};}
  const y=S.route[S.i+1],ov=OV[c.id+'>'+y];
  if(LVL==='s'&&('x_'+c.id+'_'+y) in DUR){const v=S.culprit[c.attr];
    if(k===c.trait)return {text:CLUE[c.attr][v],clips:['t_'+c.id+'_'+Object.keys(CLUE[c.attr]).indexOf(v)]};
    if(k===(c.trait+1)%3)return {text:CITY[y].hard,clips:['x_'+c.id+'_'+y]};
    return {text:c.nix,clips:['n_'+c.id]};}let text=ov?ov[k]:CITY[y].hint[k];const clips=['d_'+c.id+'_'+k+'_'+y];
  if(c.trait===k){const v=S.culprit[c.attr];text+=' '+CLUE[c.attr][v];clips.push('t_'+c.id+'_'+Object.keys(CLUE[c.attr]).indexOf(v));}
  return {text,clips};
}
function ask(k){
  if(S.over||S.busy)return;
  if(S.decoy){advance(1);say('Flughafenpersonal',CITY[S.decoy].name,'Niemand hier hat jemanden gesehen, auf den Ihre Beschreibung passt. Diese Spur führt ins Leere.',['flughafen']);timeUp();render();return;}
  const c=cityNow(),o=c.orte[k],key=S.i+'_'+k,L=line(c,k);
  setScene(c.id+k,o.ort,c.name+', '+c.land);
  if(S.seen[key]){say(o.zeuge,o.rolle,L.text,L.clips,o.p);return;}
  const slept=advance(QH);S.seen[key]=1;
  if(isFinal()){
    S.fin++;
    if(timeUp()){render();return;}
    if(S.fin<2){say(o.zeuge,o.rolle,L.text,L.clips,o.p);note(c.name,o.zeuge,L.text);render();return;}
    const who=S.culprit.name;
    if(S.warrant===who){say(o.zeuge,o.rolle,L.text,L.clips,o.p);chase(()=>{const rest=Math.max(0,DEAD-S.t);const rang=rest>=30?'Chefermittler':rest>=12?'Sonderermittler':'Ermittler';
      finish(true,'Zugriff! Die gesuchte Person ist festgenommen, die Beute ist sichergestellt. Vesper Nachtigall selbst ist uns wieder entwischt.\n\nFestgenommen: '+who+'. Noch '+rest+' Stunden Luft. Ihr neuer Rang: '+rang+'.','h_win');});}
    else if(!S.warrant){finish(false,'Sie standen der gesuchten Person gegenüber, aber ohne Haftbefehl durfte die Polizei nicht zugreifen. Sie ist entkommen.\n\nEntkommen: '+who+'.','h_nowarrant');}
    else{finish(false,'Ihr Haftbefehl lautete auf den falschen Namen. Die Polizei musste die Person laufen lassen.\n\nHaftbefehl auf '+S.warrant+', vor Ihnen stand '+who+'.','h_wrong');}
    render();return;
  }
  note(c.name,o.zeuge,L.text);
  say(o.zeuge,o.rolle,L.text+(slept?'\n\n(Danach haben Sie bis 7 Uhr geschlafen.)':''),L.clips,o.p);
  timeUp();render();
}
function travel(to,h,correct){
  if(S.over||S.busy)return;
  const c0=cityNow(),from=S.decoy||c0.id;
  S.busy=true;render();let fin=false;
  const land=()=>{if(fin)return;fin=true;
    const slept=advance(h);S.busy=false;document.body.classList.remove('flying');$('map').hidden=true;try{setTab('q');
    if(to===c0.id){S.decoy=null;setScene(c0.id+'0',c0.orte[0].ort,c0.name+', '+c0.land);say('Direktorin Halberg','per Funk','Zurück am letzten sicheren Punkt der Spur. Sehen Sie sich die Hinweise noch einmal genau an.',['h_back']);}
    else if(correct){S.decoy=null;S.i++;const c=cityNow();setScene(c.id+'0',c.orte[0].ort,c.name+', '+c.land);
      if(isFinal())say('Direktorin Halberg','per Funk','Hier endet die Spur. Hören Sie sich um, aber greifen Sie nur mit gültigem Haftbefehl zu.',['h_final']);
      else say('Direktorin Halberg','per Funk','Gute Arbeit. In '+c.name+' wurde die Person gesehen. Hören Sie sich um.'+gh()+(slept?'\n\n(Sie sind erst um 7 Uhr wieder einsatzbereit.)':''),['h_arr_'+c.id]);}
    else{S.decoy=to;setScene('flughafen','Flughafen',CITY[to].name+', '+CITY[to].land);say('Direktorin Halberg','per Funk','Falsche Fährte. Von der gesuchten Person haben wir hier keine einzige Meldung.',['h_decoy']);}
    }finally{timeUp();render();}
  };
  fly(from,to,h,land);setTimeout(land,6500);
}
function issue(){
  const m=matches();if(S.over||S.busy||!S.started||m.length!==1)return;
  const LC=LV[LVL];if(S.warrant&&(!LC.re||S.warrant===m[0].name))return;
  advance(S.warrant?LC.re:1);S.warrant=m[0].name;
  {const d=document.createElement('div');d.className='stampbig tmp';d.textContent='HAFTBEFEHL';$('scene').append(d);setTimeout(()=>d.remove(),2200);}
  say('Direktorin Halberg','per Funk','Der Haftbefehl ist unterschrieben. Ich hoffe, Sie sind sich sicher.'+(isFinal()?'':'\n\n(Folgen Sie jetzt der Spur weiter, bis sie endet. Dort kommt es zum Zugriff.)'),['h_warrant']);
  timeUp();render();
}
function btn(label,small,fn,cls){const b=document.createElement('button');b.type='button';b.className='act'+(cls?' '+cls:'');const s=document.createElement('span');s.textContent=label;b.append(s);if(small){const m=document.createElement('small');m.textContent=small;b.append(m);}b.onclick=fn;b.disabled=!!S.busy;return b;}
function box(title,cls){const d=document.createElement('div');d.className='box '+(cls||'q');const h=document.createElement('h2');h.textContent=title;d.append(h);return d;}
function render(){
  if(MODE!=='case'){renderHub();stageFig();return;}
  const c=cityNow();
  $('clock').textContent=fmt(S.t);
  const rest=Math.max(0,DEAD-S.t);$('remain').textContent=rest+' h';$('frist').textContent=fmt(DEAD);
  $('leftchip').classList.toggle('warn',rest<24);
  const pct=Math.round(rest/(DEAD-START)*100);$('barfill').style.width=pct+'%';$('pbar').setAttribute('aria-valuenow',pct);
  const A=$('actions');A.innerHTML='';
  const LC=LV[LVL];
  if(!S.started){setTab('q');const b=box('Neuer Auftrag');const g=document.createElement('div');g.className='lv';g.setAttribute('role','group');g.setAttribute('aria-label','Schwierigkeit');
    Object.keys(LV).forEach(k=>{const x=document.createElement('button');x.type='button';x.textContent=LV[k].n;x.setAttribute('aria-pressed',k===LVL);x.onclick=()=>{LVL=k;try{localStorage.setItem('am-stufe',k);}catch(e){}newGame();};g.append(x);});
    const p=document.createElement('p');p.className='hint';p.textContent=LC.d;b.append(g,p,btn('Fall annehmen','',begin,'big'));A.append(b);}
  else if(S.over){setTab('q');const b=box(S.win?'Fall gelöst':'Fall verloren');b.append(btn('Zurück ins Büro','',backToOffice,'big'));A.append(b);}
  else if(S.pend){setTab('q');const b=box('Zugriff');const x=btn('Verfolgung aufnehmen','',()=>chase(S.pend),'big');x.disabled=false;b.append(x);A.append(b);}
  else{
    const q=box('Befragen');
    if(S.decoy)q.append(btn('Am Flughafen umhören','1 h',()=>ask(0)));
    else{const k=S.scene.indexOf(c.id)===0?+S.scene.slice(-1):0,o=c.orte[k],done=S.seen[S.i+'_'+k],nd=c.orte.filter((x,j)=>S.seen[S.i+'_'+j]).length;
      q.append(btn(o.ort,done?'notiert':LC.mark?'ansprechen · '+QH+' h':'hier',()=>goTo(k),(done?'done':'')+' here'),btn('Stadtplan','3 Orte · '+nd+' notiert'+(walkH()?' · Weg '+walkH()+' h':''),citymap));}
    const r=box('Reisen','r');
    if(isFinal()&&!S.decoy){const p=document.createElement('p');p.className='hint';p.textContent='Die Spur endet in '+c.name+'. Hier fällt die Entscheidung.';r.append(p);}
    else{const p=document.createElement('p');p.className='hint';p.textContent='Spesen '+S.cash.toLocaleString('de-DE')+' · Prämien '+META.money.toLocaleString('de-DE');r.append(p,btn('Weltkarte öffnen','Ziel und Verkehrsmittel wählen',worldmap,'here'));
      if(S.decoy)r.append(btn('Zurück nach '+c.name,'Linienflug · '+(hours(S.decoy,c.id)+2)+' h',()=>book(c.id,TRAVEL[1])));}
    A.append(q,r);
  }
  const F=$('fields');
  if(!F.children.length){ATTR.forEach(a=>{const l=document.createElement('label');l.htmlFor='p-'+a[0];l.textContent=a[1];const s=document.createElement('select');s.id='p-'+a[0];
    const vals=[...new Set(ALLSUS.map(x=>x[a[0]]))].sort((x,y)=>x.localeCompare(y,'de'));
    s.innerHTML='<option value="">unbekannt</option>';vals.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;s.append(o);});
    s.onchange=()=>{S.profile[a[0]]=s.value;render();};F.append(l,s);});}
  ATTR.forEach(a=>{$('p-'+a[0]).value=S.profile[a[0]];});
  const m=matches(),L=$('sus');L.innerHTML='';
  SUSPECTS.forEach(s=>{const li=document.createElement('li');const inh=META.arrested.includes(s.name);li.textContent=s.name+(inh?' (in Haft)':'');if(inh||(LC.count&&!m.includes(s)))li.className='out';L.append(li);});
  $('count').textContent=m.length===1?'Ein Name bleibt übrig: '+m[0].name+'.':m.length===0?'Niemand passt auf dieses Profil. Prüf deine Einträge.':m.length+' Verdächtige passen noch'+(m.length<=3?': '+m.map(x=>x.name).join(', ')+'.':'.');
  $('count').hidden=!LC.count;
  $('tab-n').textContent='Notizen'+(S.notes.length?' '+S.notes.length:'');
  $('warrant').disabled=S.over||S.busy||!S.started||m.length!==1||(S.warrant&&!LC.re);
  $('stamp').hidden=!S.warrant;$('stamp').textContent=S.warrant?'Haftbefehl ausgestellt auf: '+S.warrant:'';
  const N=$('notes');N.innerHTML='';
  S.notes.forEach((n,i)=>{const li=document.createElement('li');if(i===0&&S.notes.length>lastNote)li.className='new';const b=document.createElement('b');b.textContent=n.stadt+' · '+n.zeuge;li.append(b,n.text);N.append(li);});
  lastNote=S.notes.length;stageFig();
  $('empty').hidden=S.notes.length>0;$('empty').textContent=LC.notes?'Noch keine Hinweise. Befrag die Zeugen in '+CITY[S.route[0]].name+'.':'Auf Stufe Schwer schreibt niemand für Sie mit. Merken Sie sich, was die Zeugen sagen.';
}
function setTab(t){document.body.dataset.tab=t;document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.t===t));if(S)fitAll();}
function fitZoom(box,min){if(!box||!box.clientHeight)return 1;const k=[...box.children];let z=1;k.forEach(c=>c.style.zoom='');
  while((box.scrollHeight>box.clientHeight+1||box.scrollWidth>box.clientWidth+1)&&z>(min||.35)){z=+(z-.05).toFixed(2);k.forEach(c=>c.style.zoom=z);}return z;}
function pager(box,list,min){if(!box||!list||!box.clientHeight)return;const it=[...list.children];let pg=list._pg;
  if(!pg){pg=list._pg=document.createElement('div');pg.className='pgr';const a=document.createElement('button'),l=document.createElement('span'),b=document.createElement('button');a.type=b.type='button';a.textContent='‹';b.textContent='›';a.setAttribute('aria-label','Vorherige Seite');b.setAttribute('aria-label','Nächste Seite');pg.append(a,l,b);list.after(pg);list._st=[];list._s=0;}
  if(list._n!==it.length){list._n=it.length;list._s=0;list._st=[];}
  const s=Math.min(list._s,Math.max(0,it.length-1)),[a,l,b]=pg.children;
  it.forEach((c,i)=>{c.hidden=i!==s;});pg.hidden=it.length<2;
  fitZoom(box,min||.6);let n=it.length?1:0;
  for(let i=s+1;i<it.length;i++){it[i].hidden=false;if(box.scrollHeight>box.clientHeight+1){it[i].hidden=true;break;}n++;}
  if(s===0&&n>=it.length)pg.hidden=true;
  l.textContent=(s+1)+(n>1?'–'+(s+n):'')+' von '+it.length;a.disabled=!s;b.disabled=s+n>=it.length;
  a.onclick=()=>{list._s=list._st.pop()||0;pager(box,list,min);};b.onclick=()=>{list._st.push(s);list._s=s+n;pager(box,list,min);};
  if(box.scrollHeight>box.clientHeight+1){const k=[...box.children];let z=parseFloat(k[0].style.zoom)||1;while(box.scrollHeight>box.clientHeight+1&&z>.3){z=+(z-.05).toFixed(2);k.forEach(c=>c.style.zoom=z);}}}
function fitDialog(){const D=$('dialog'),t=$('txt'),cur=t.textContent,full=t._full&&t._full.length>cur.length;D.style.minHeight='0';if(full)t.textContent=t._full;fitZoom(D,.35);D.style.minHeight=D.offsetHeight+'px';if(full)t.textContent=cur;}
function fitAll(){if(!S)return;
  fitDialog();fitZoom($('actions'),.35);
  const ak=document.querySelector('.akte');if(ak&&ak.clientHeight)pager(ak,$('notes'),.7);
  const sh=$('sheet');if(sh&&sh._fit)sh._fit();}
{const r0=render;render=function(){r0();fitAll();};let rt=0;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{if(S){figKey='';render();}},120);});}
document.querySelectorAll('#tabs button').forEach(b=>b.onclick=()=>setTab(b.dataset.t));
$('warrant').onclick=issue;
$('voice').onclick=()=>{voiceOn=!voiceOn;$('voice').setAttribute('aria-pressed',voiceOn);$('voice').textContent=voiceOn?'Stimmen an':'Stimmen aus';if(!voiceOn){stopAudio();$('face').classList.remove('talk');}};
__META__
boot();
if(!calm)requestAnimationFrame(fxLoop);
'''
FOV['lima'][2]='Die Person, die Sie suchen, kann nicht weit sein. Beeilen Sie sich.' if 'f_lima_2' in dur and False else 'Vor zehn Minuten wollte jemand hier etwas Wertvolles schätzen lassen. Die Person kann nicht weit sein.'
J=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
import panodata
EX_X=[.78,2.25,1.1];PANO2={};PJAGD2={}
PROPS=json.load(open('../pano/props.json'));PPR2={};PSOLID={}
for _c,_l in PROPS.items():
    PSOLID[_c]=[]
    for _i,(_w,_h) in enumerate(_l):
        _f=0 if _h>300 else 1;PPR2[_c+str(_i)]=[_w,_h,_f]
        if _f:PSOLID[_c].append(_c+str(_i))
for _k,(_l,_pl,_fl,_parts,_hot) in panodata.S.items():
    _w,_ex,_hp=panodata.POS[_k];_h=[[n,hp[0],t,hp[1]] for (n,t,e),hp in zip(_hot,_hp)]
    _occ=[_w]+_ex+[hp[0] for hp in _hp]
    _it=max([.55,.9,1.25,1.6,1.95,2.3,2.65],key=lambda x:min(abs(x-o) for o in _occ))
    _city=_k[:-1];_sc=int(_k[-1]);_pp=[];_o2=_occ+[_it,.2,2.8]
    for _j in range(2):
        _x=max([.6,.78,.95,1.1,1.25,1.4,1.55,1.7,1.85,2.0,2.15,2.3,2.45],key=lambda x:min(abs(x-o) for o in _o2))
        if min(abs(_x-o) for o in _o2)>=(.19 if _j else .14):_pp.append([PSOLID[_city][(_sc*2+_j)%len(PSOLID[_city])],_x]);_o2.append(_x)
    PANO2[_k]={'w':_w,'e':[[e[0],_ex[i],1 if _ex[i]>_w else 0] for i,e in enumerate(FIG.get(_k,{}).get('e',[])[:2])],'h':_h,'p':_pp,'it':_it,'gy':.9,'hh':.3,'t':panodata.L[_l][1]}
for _c in panodata.J: PJAGD2[_c]={'img':_c+'_jagd','z':1,'gy':.9,'hh':.3,'ton':'nacht','props':PSOLID[_c]}
js=js.replace('__CLUE__',J(D['CLUE'])).replace('__FINAL__',J(D['FINAL'])).replace('__SUS__',sus).replace('__CITY__',J(cities)).replace('__OV__',J(OV)).replace('__FOV__',J(FOV)).replace('__FX__',J(FX)).replace('__DUR__',J(dur)).replace('__FIG__',J(FIG)).replace('__FIGS__',J(FIGS)).replace('__EX__',J(EX)).replace('__HOT__',J(HOT)).replace('__MASK__',mask).replace('__MID__',mid).replace('__META__',open('meta.js').read()+open('pano.js').read()).replace('__PANO__','{"wien0": {"w": 1.33, "e": [["x_police", 1.76, 1], ["x_oldlady", 0.8, 0]], "h": [["Straßenbahn", 0.25, "Die letzte Bahn ist längst durch. Am Trittbrett klebt frischer Schlamm.", 0.26], ["Museumstreppe", 1.47, "Nasse Fußspuren führen die Treppe herunter und verlieren sich im Regen.", 0.1], ["Markise", 2.75, "Unter der Markise ist das Pflaster trocken. Hier hat jemand eine Weile gewartet.", 0.3]], "p": [["saeule", 0.3], ["bank", 1.02], ["sperre", 1.62], ["saeule", 2.72]], "it": 2.2, "gy": 0.905, "hh": 0.31}, "wien1": {"w": 1.6, "e": [["x_business", 2.5, 1], ["x_porter", 0.75, 0]], "h": [["Schalter", 0.35, "Der Schalter ist geschlossen. Auf der Waage liegt ein vergessener Gepäckanhänger.", 0.2], ["Anzeigetafel", 1.1, "Die Tafel rattert. Der letzte Abendflug ist bereits als abgeflogen markiert.", 0.5], ["Kiosk", 2.35, "Stadtpläne in zwölf Sprachen. Ein Fach ist leer gekauft.", 0.32]], "p": [], "it": 2.05, "gy": 0.86, "hh": 0.29}, "wien2": {"w": 1.3, "e": [["x_reader", 0.6, 0]], "h": [["Garderobe", 0.07, "An einem Haken hängt ein einzelner nasser Schirm.", 0.3], ["Kuchentheke", 1.9, "Sachertorte, Apfelstrudel, Topfengolatsche. Ein Stück Torte fehlt.", 0.24], ["Flügel", 2.7, "Auf dem Notenpult liegt ein Walzer. Die Tasten sind noch warm.", 0.26]], "p": [], "it": 2.3, "gy": 0.93, "hh": 0.33}}').replace('__PJAGD__','{"wien": {"img": "wien_jagd", "z": 2.2, "gy": 0.93, "hh": 0.25, "ton": "nacht"}}').replace('__PLAN__',J({"wien": [[11, 34], [80, 84], [26, 66]], "istanbul": [[45, 60], [50, 84], [83, 50]], "kairo": [[26, 40], [50, 82], [78, 54]], "mumbai": [[25, 84], [62, 55], [33, 22]], "tokio": [[20, 42], [75, 58], [73, 22]], "lima": [[47, 36], [35, 78], [80, 55]], "paris": [[27, 40], [64, 72], [68, 18]], "newyork": [[38, 48], [55, 25], [38, 85]], "rio": [[22, 72], [54, 24], [72, 78]], "sydney": [[56, 54], [88, 45], [25, 76]], "nairobi": [[44, 23], [65, 78], [30, 54]], "peking": [[50, 48], [20, 55], [78, 76]], "marrakesch": [[62, 38], [31, 52], [58, 68]], "reykjavik": [[15, 37], [53, 58], [74, 70]]})).replace('__PPR2__',json.dumps(PPR2)).replace('__PANO2__',json.dumps(PANO2,ensure_ascii=False)).replace('__PJAGD2__',json.dumps(PJAGD2))
head=head.replace('<h1>Akte Meridian<small>Fall 1 · Das Salzfass von Wien</small></h1>','<h1>Akte Meridian<small>Fall</small></h1>').replace('Frist Sa 18:00 · noch <b id="remain">129 h</b>','Frist <b id="frist">Sa 18:00</b> · noch <b id="remain">129 h</b>').replace('<em>Fall 1 · Das Salzfass von Wien</em>','<em>Fall</em>')
head=head.replace('<div class="left">','<nav class="tabs" id="tabs" aria-label="Bereiche"><button type="button" data-t="q" aria-pressed="true">Befragen</button><button type="button" data-t="r" aria-pressed="false">Reisen</button><button type="button" data-t="p" aria-pressed="false">Profil</button><button type="button" data-t="n" id="tab-n" aria-pressed="false">Notizen</button></nav>\n    <div class="left">')
head=head.replace('<section>\n        <h2>Täterprofil</h2>','<section id="sec-p">\n        <h2>Täterprofil</h2>').replace('<section>\n        <h2>Kartei: Der Zirkel</h2>','<section id="sec-k">\n        <h2>Kartei: Der Zirkel</h2>').replace('<section>\n        <h2>Notizbuch</h2>','<section id="sec-n">\n        <h2>Notizbuch</h2>')
assert 'id="sec-p"' in head and 'id="sec-k"' in head and 'id="sec-n"' in head and 'id="tabs"' in head
n0=head.count('<div class="mv"><img')
head=re.sub(r'<div class="mv">(<img[^>]*>)<i class="pulse"></i></div>',r'<div class="mv"><div class="stg">\1<i class="pulse"></i></div></div>',head)
assert head.count('<div class="stg">')==2,n0
_fm=lambda n,r,g,b:'<filter id="f-%s" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="%s 0 0 0 0 0 %s 0 0 0 0 0 %s 0 0 0 0 0 1 0"/></filter>'%(n,r,g,b)
SVGF='<svg width="0" height="0" style="position:absolute" aria-hidden="true">'+_fm('nacht',.5,.6,.92)+_fm('dunkel',.7,.75,.8)+_fm('warm',.98,.86,.66)+_fm('abend',.95,.78,.68)+'</svg>'
head=head.replace('<body>','<body data-tab="q">'+SVGF).replace('</style>',COMPACT+'</style>')
assert 'id="frist"' in head

for _a,_b in [
 ("  if(calm||!a||!b){done();return;}\n  const cv=$('map'),g=cv.getContext('2d');cv.hidden=false;",
  "  if(!a||!b){done();return;}\n  const cv=$('map'),g=cv.getContext('2d');cv.hidden=false;document.body.classList.add('flying');"),
 ("const t0=performance.now(),dur=2100;","const dur=calm?1:2100,t0=performance.now();"),
 ("if(k<1)requestAnimationFrame(frame);else setTimeout(()=>{cv.hidden=true;done();},350);",
  "if(k<1)requestAnimationFrame(frame);else setTimeout(()=>{cv.hidden=true;document.body.classList.remove('flying');done();},calm?1600:450);"),
]:
    assert _a in js,_a
    js=js.replace(_a,_b)
html=head+'<script>'+js+'</script>\n</body>\n</html>\n'
open('../index.html','w').write(html);open('/tmp/g.js','w').write(js);print('ok',len(html))
