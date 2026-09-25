(function(){
var FC='https://api.weather.gov/gridpoints/OKX/62,57/forecast';
var GRID='https://api.weather.gov/gridpoints/OKX/62,57';
var AL='https://api.weather.gov/alerts/active?point=40.9387,-73.1182';
var OBS='https://api.weather.gov/stations/KISP/observations?limit=100';
var TD='https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=ThreeVillageLocal&datum=MLLW&station=8514560&time_zone=lst_ldt&units=english&interval=hilo&format=json&range=72&begin_date=';
// storm milestones (Eastern time)
var T_START=new Date('2026-09-25T14:00:00-04:00'), T_PEAK=new Date('2026-09-25T23:22:00-04:00'), T_END=new Date('2026-09-27T23:59:00-04:00');
var SVGNS='http://www.w3.org/2000/svg';
function $(id){return document.getElementById(id)}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var DAYS=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],MON=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'];
function tm(d){var h=d.getHours(),m=d.getMinutes(),ap=h>=12?'PM':'AM';h=h%12||12;return h+(m?':'+(m<10?'0':'')+m:'')+' '+ap}
function stamp(d){return DAYS[d.getDay()]+' '+MON[d.getMonth()]+' '+d.getDate()+', '+tm(d)}
function icon(t){t=(t||'').toLowerCase();
if(/thunder/.test(t))return '&#9928;&#65039;';
if(/rain|shower|drizzle/.test(t))return /wind|breez/.test(t)?'&#127788;&#65039;':'&#127783;&#65039;';
if(/snow/.test(t))return '&#10052;&#65039;';
if(/fog|mist|haze/.test(t))return '&#127787;&#65039;';
if(/partly|mostly sunny/.test(t))return '&#9925;';
if(/cloud|overcast/.test(t))return '&#9729;&#65039;';
if(/sun|clear|fair/.test(t))return '&#9728;&#65039;';
return '&#127780;&#65039;'}
function frac(v){v=Math.round(v*4)/4;var w=Math.floor(v),r=v-w,fr=r===.25?'¼':r===.5?'½':r===.75?'¾':'';return (w||!fr?w:'')+fr}
function amt(t){t=t.replace(/ possible/i,'').trim();var w={'a tenth of an inch':'0.1"','three quarters':'¾"','a half':'½"','a quarter':'¼"','one':'1"','two':'2"','three':'3"','four':'4"'};if(/^less than a tenth/i.test(t))return 'Under 0.1"';var m=t.match(/^(?:between )?(.+?) and (.+?)(?: of an)? inch(?:es)?$/i);var f=function(x){x=x.trim().toLowerCase();return w[x]||(/^[0-9.]+$/.test(x)?x+'"':x)};if(m)return f(m[1])+' to '+f(m[2]);return t}
function get(u){return fetch(u,{headers:{'Accept':'application/geo+json'}}).then(function(r){if(!r.ok)throw r.status;return r.json()})}
function setNum(id,val,dec){var el=$(id);if(!el||val==null||isNaN(val))return;var from=parseFloat(el.textContent);var to=+val;dec=dec||0;
  if(isNaN(from)||!window.requestAnimationFrame){el.textContent=to.toFixed(dec);return}
  if(from.toFixed(dec)!==to.toFixed(dec)){el.classList.remove('stm-flashv');void el.offsetWidth;el.classList.add('stm-flashv')}
  var t0=null,D=900;function step(ts){if(!t0)t0=ts;var p=Math.min((ts-t0)/D,1),e=1-Math.pow(1-p,3);el.textContent=(from+(to-from)*e).toFixed(dec);if(p<1)requestAnimationFrame(step)}requestAnimationFrame(step)}

/* ---------- forecast ---------- */
function forecast(){
return get(FC).then(function(d){
var p=d.properties,per=p.periods||[];
var up=new Date(p.updateTime||p.generatedAt);
if($('stm-upd'))$('stm-upd').textContent='Updated '+stamp(up);
var fc=$('stm-fc');
if(fc&&per.length){
var html='';
per.slice(0,6).forEach(function(x){
var rain=(x.detailedForecast.match(/New (?:rainfall|precipitation) amounts? (?:of )?(?:between )?([^.]+)/i)||[])[1];
var pop=x.probabilityOfPrecipitation&&x.probabilityOfPrecipitation.value!=null?x.probabilityOfPrecipitation.value+'% rain':'';
var gust=(x.detailedForecast.match(/gusts as high as ([0-9]+) mph/i)||[])[1];
html+='<div class="stm-day'+(x.isDaytime?'':' stm-night')+'"><p class="stm-dname">'+esc(x.name)+'</p><p class="stm-dicon">'+icon(x.shortForecast)+'</p><p class="stm-dhi">'+x.temperature+'&deg;</p><p class="stm-dtxt">'+esc(x.shortForecast)+'. Wind '+esc(x.windSpeed)+(gust?', gusts to '+gust+' mph':'')+'.</p><p class="stm-drain">'+esc(rain?amt(rain):(pop||'Dry'))+'</p></div>';
});
fc.innerHTML=html;
}
var maxG=0;
per.slice(0,8).forEach(function(x){var g=x.detailedForecast.match(/gusts as high as ([0-9]+) mph/i);if(g)maxG=Math.max(maxG,+g[1])});
if(maxG&&$('stm-gust')){$('stm-gust').textContent=maxG;$('stm-gustbar').style.width=Math.min(maxG/60,1)*100+'%'}
});
}
/* ---------- storm total rain (NWS numeric grid) ---------- */
function qpf(){return get(GRID).then(function(d){var q=d.properties.quantitativePrecipitation;if(!q||!q.values)return;var now=Date.now(),mm=0;
q.values.forEach(function(v){var st=new Date(v.validTime.split('/')[0]).getTime();if(st>now-6*3600e3&&st<now+96*3600e3)mm+=v.value||0});
var inch=mm/25.4;if(inch<0.1||!$('stm-rain'))return;$('stm-rain').textContent='About '+frac(inch);$('stm-rainbar').style.width=Math.min(inch/6,1)*100+'%'})}
/* ---------- alerts ---------- */
function alerts(){
return get(AL).then(function(d){
var box=$('stm-alerts');if(!box)return;
var f=(d.features||[]).map(function(x){return x.properties}).filter(function(a){return a.event});
if(!f.length){box.innerHTML='<div class="stm-alert stm-a2"><span class="stm-alabel">No Active Alerts</span><span class="stm-atime">For the Three Village area</span><span class="stm-adesc">The National Weather Service has cleared all warnings.</span></div>';return}
var blurb=function(e){return /wind/i.test(e)?'Strong gusts can down trees and power lines':/flood watch|flood warning/i.test(e)?'Shoreline and low road flooding possible':/flood statement|flood advisory/i.test(e)?'Minor flooding in low spots near the water':/warning/i.test(e)?'Take action now':'See weather.gov for details'};
var cls=function(e){return /wind|warning/i.test(e)?'stm-a1':/flood/i.test(e)?'stm-a2':'stm-a3'};
var rank=function(e){return /warning/i.test(e)?0:/watch/i.test(e)?1:/advisory/i.test(e)?2:3};f.sort(function(a,b){return rank(a.event)-rank(b.event)});var seen={},html='';
f.forEach(function(a){if(seen[a.event])return;seen[a.event]=1;if(/coastal flood (watch|warning)/i.test(a.event)){window.stmFlood=[new Date(a.onset||a.effective),new Date(a.ends||a.expires)]}
var s=a.onset?new Date(a.onset):null,e=a.ends||a.expires?new Date(a.ends||a.expires):null;
var when=(s?DAYS[s.getDay()]+' '+tm(s):'Now')+(e?' to '+DAYS[e.getDay()]+' '+tm(e):'');
html+='<div class="stm-alert '+cls(a.event)+'"><span class="stm-alabel">'+esc(a.event)+'</span><span class="stm-atime">'+esc(when)+'</span><span class="stm-adesc">'+esc(blurb(a.event))+'</span></div>'});
box.innerHTML=html;
});
}
/* ---------- tides ---------- */
function tides(){
var n=new Date(),ymd=n.getFullYear()+('0'+(n.getMonth()+1)).slice(-2)+('0'+n.getDate()).slice(-2);
return get(TD+ymd).then(function(d){
var box=$('stm-tides');if(!box||!d.predictions)return;
var highs=d.predictions.filter(function(x){return x.type==='H'&&new Date(x.t.replace(' ','T'))>new Date(Date.now()-3600e3)}).slice(0,4);
if(!highs.length)return;
box.innerHTML=highs.map(function(x){var t=new Date(x.t.replace(' ','T'));var fw=window.stmFlood&&t>=window.stmFlood[0]&&t<=window.stmFlood[1];return '<div class="stm-tide'+(fw?' stm-thigh':'')+'"><p class="stm-tday">'+DAYS[t.getDay()]+' '+MON[t.getMonth()]+' '+t.getDate()+'</p><p class="stm-ttime">'+tm(t)+'</p><p class="stm-tnote">'+(fw?'During the Flood Watch. ':'')+parseFloat(x.v).toFixed(1)+' ft predicted</p></div>'}).join('');
});
}
/* ---------- live weather station ---------- */
var lastObs=null;
function kmh(v){return v==null?null:v*0.621371}
function f(v){return v==null?null:v*9/5+32}
function val(p,k){return p&&p[k]&&p[k].value!=null?p[k].value:null}
function ticks(){var g=$('stm-ticks');if(!g||g.childNodes.length)return;for(var i=0;i<72;i++){var a=i*5*Math.PI/180,big=i%9===0,r1=big?82:86,r2=92;var l=document.createElementNS(SVGNS,'line');
  l.setAttribute('x1',(110+r1*Math.sin(a)).toFixed(1));l.setAttribute('y1',(110-r1*Math.cos(a)).toFixed(1));l.setAttribute('x2',(110+r2*Math.sin(a)).toFixed(1));l.setAttribute('y2',(110-r2*Math.cos(a)).toFixed(1));if(big)l.setAttribute('class','stm-tk');g.appendChild(l)}}
function spark(list){var svg=$('stm-sparksvg');if(!svg)return;var now=Date.now(),pts=list.filter(function(o){return now-o.t<=12*3600e3}).reverse();if(pts.length<2)return;
  var t0=pts[0].t,t1=pts[pts.length-1].t,max=10;pts.forEach(function(o){max=Math.max(max,o.g||0,o.s||0)});max=Math.ceil((max+4)/10)*10;
  var X=function(t){return (t-t0)/(t1-t0||1)*600},Y=function(v){return 125-(v/max)*115};
  var ls='',lg='';pts.forEach(function(o,i){ls+=(i?'L':'M')+X(o.t).toFixed(1)+' '+Y(o.s||0).toFixed(1);lg+=(i?'L':'M')+X(o.t).toFixed(1)+' '+Y(o.g!=null?o.g:(o.s||0)).toFixed(1)});
  var area=ls+'L600 130L0 130Z',last=pts[pts.length-1];
  var grid='';for(var v=10;v<max;v+=10){grid+='<line x1="0" x2="600" y1="'+Y(v).toFixed(1)+'" y2="'+Y(v).toFixed(1)+'" stroke="rgba(255,255,255,.07)" vector-effect="non-scaling-stroke"/><text x="4" y="'+(Y(v)-3).toFixed(1)+'" fill="rgba(200,220,240,.45)" font-size="10">'+v+'</text>'}
  svg.innerHTML='<defs><linearGradient id="stmsa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4de1ff" stop-opacity=".45"/><stop offset="1" stop-color="#4de1ff" stop-opacity="0"/></linearGradient></defs>'+grid+
   '<g class="stm-draw"><path d="'+area+'" fill="url(#stmsa)" class="stm-spa"/><path d="'+lg+'" class="stm-spl stm-spg"/><path d="'+ls+'" class="stm-spl stm-sps"/></g>'+
   '<circle cx="'+X(last.t).toFixed(1)+'" cy="'+Y(last.s||0).toFixed(1)+'" r="4" class="stm-spdot"/>';
  var xs=$('stm-sparkx');if(xs){var h='';for(var k=0;k<5;k++){var t=new Date(t0+(t1-t0)*k/4);h+='<span>'+(k===4?'Now':tm(t))+'</span>'}xs.innerHTML=h}}
function obs(){
return get(OBS).then(function(d){
var feats=(d.features||[]).map(function(x){return x.properties}).filter(function(p){return p&&p.timestamp});if(!feats.length)return;
var p=null;for(var i=0;i<feats.length;i++){if(val(feats[i],'temperature')!=null){p=feats[i];break}}if(!p)p=feats[0];
var p0=new Date(p.timestamp).getTime();function pick(k){for(var i=0;i<feats.length;i++){var q=feats[i];if(p0-new Date(q.timestamp).getTime()>2*3600e3)break;var v=val(q,k);if(v!=null)return v}return null}
var t=f(pick('temperature')),ws=kmh(pick('windSpeed')),wg=kmh(val(p,'windGust')),wd=pick('windDirection'),h=pick('relativeHumidity'),pr=pick('barometricPressure'),dp=f(pick('dewpoint')),vis=pick('visibility');
var feel=f(val(p,'windChill')!=null?val(p,'windChill'):val(p,'heatIndex'));if(feel==null)feel=t;
var dirs=['N','NE','E','SE','S','SW','W','NW'];ticks();
setNum('stm-temp',t,0);setNum('stm-feel',feel,0);setNum('stm-hum',h,0);setNum('stm-dew',dp,0);
if(ws!=null)setNum('stm-wspd',ws,0);
if($('stm-wgst'))$('stm-wgst').textContent=wg!=null?Math.round(wg):'none';
if(wd!=null){if($('stm-wdir'))$('stm-wdir').textContent=dirs[Math.round(wd/45)%8];if($('stm-needle'))$('stm-needle').style.transform='rotate('+wd+'deg)'}
var garc=$('stm-garc');if(garc){var gv=wg!=null?wg:(ws||0);garc.style.strokeDashoffset=(628.3*(1-Math.min(gv/60,1))).toFixed(1)}
var ring=$('stm-humring');if(ring&&h!=null)ring.style.strokeDashoffset=(113.1*(1-h/100)).toFixed(1);
if(pr!=null)setNum('stm-pres',pr/3386.389,2);
if(vis!=null&&$('stm-vis'))$('stm-vis').textContent=Math.round(vis/1609.34*10)/10;
if(p.textDescription){var hr=new Date(p.timestamp).getHours(),night=hr<6||hr>=19,ic=icon(p.textDescription);if(night&&/clear|fair|sunny/i.test(p.textDescription))ic='&#127769;';if(night&&/partly|mostly clear/i.test(p.textDescription))ic='&#9729;&#65039;';if($('stm-cond'))$('stm-cond').textContent=p.textDescription;if($('stm-cicon'))$('stm-cicon').innerHTML=ic}
// pressure trend vs ~3 hours earlier
var tr=$('stm-ptrend');if(tr&&pr!=null){var ref=null,pt=new Date(p.timestamp).getTime();for(var j=0;j<feats.length;j++){var q=feats[j],qt=new Date(q.timestamp).getTime();if(pt-qt>=2.5*3600e3&&val(q,'barometricPressure')!=null){ref=val(q,'barometricPressure');break}}
  if(ref!=null){var diff=(pr-ref)/3386.389;tr.className='stm-ts '+(diff<=-0.02?'stm-down':diff>=0.02?'stm-up':'');tr.innerHTML=(diff<=-0.02?'&#9660; Falling':diff>=0.02?'&#9650; Rising':'&#9644; Steady')+' ('+(diff>0?'+':'')+diff.toFixed(2)+' in 3 hr)'}else{tr.textContent='Trend unavailable'}}
spark(feats.map(function(o){return {t:new Date(o.timestamp).getTime(),s:kmh(val(o,'windSpeed')),g:kmh(val(o,'windGust'))}}).filter(function(o){return o.s!=null}));
lastObs=new Date(p.timestamp);ago();
});
}
function ago(){var el=$('stm-ago');if(!el||!lastObs)return;var m=Math.round((Date.now()-lastObs.getTime())/60000);el.textContent='Observed '+tm(lastObs)+' · '+(m<1?'just now':m===1?'1 min ago':m<90?m+' min ago':Math.round(m/60)+' hr ago')}
/* ---------- hero countdown ---------- */
function pad(n){return (n<10?'0':'')+n}
function countdown(){var cl=$('stm-cl'),cv=$('stm-cv');if(!cl||!cv)return;var now=new Date(),target,label;
  if(now<T_START){target=T_START;label='Storm arrives in'}else if(now<T_PEAK){target=T_PEAK;label='Peak winds &amp; high tide in'}
  else if(now<T_END){cl.innerHTML='Storm in progress';cv.textContent='Stay safe';return}else{cl.innerHTML='Storm has passed';cv.textContent='Cleanup info below';return}
  var s=Math.max(0,Math.floor((target-now)/1000)),d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60),sec=s%60;
  cl.innerHTML=label;cv.textContent=(d?d+'d ':'')+h+'h '+pad(m)+'m '+pad(sec)+'s'}
/* ---------- checklist (remembered on this device) ---------- */
var KEY='stm-check-2026-09';
function prog(){var c=document.querySelectorAll('.stm-cb'),n=0,st=[];for(var i=0;i<c.length;i++){if(c[i].checked){n++;st.push(c[i].id)}}
  var fl=document.querySelector('.stm-progfill');if(fl)fl.style.width=(c.length?n/c.length*100:0)+'%';var t=document.querySelector('.stm-prog');if(t)t.classList.toggle('stm-alldone',n===c.length&&n>0);
  try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
function restore(){try{var st=JSON.parse(localStorage.getItem(KEY)||'[]');st.forEach(function(id){var el=$(id);if(el)el.checked=true})}catch(e){}prog()}
/* ---------- save / share ---------- */
function toast(msg){var t=$('stm-toast');if(!t)return;t.textContent=msg;t.classList.add('stm-show');clearTimeout(toast.h);toast.h=setTimeout(function(){t.classList.remove('stm-show')},3800)}
function save(){var url=location.href.split('#')[0],title=document.title;
  if(navigator.share){navigator.share({title:title,text:'Storm prep guide for Three Village, updated live',url:url}).catch(function(){});return}
  var done=function(){toast('Link copied. Press '+(/Mac/.test(navigator.platform)?'Cmd':'Ctrl')+'+D to bookmark it.')};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(url).then(done,function(){toast('Press Ctrl+D to bookmark this page.')})}else{toast('Press Ctrl+D to bookmark this page.')}}
/* ---------- scroll: reveal, scrollspy, back-to-top ---------- */
function scrollFx(){var root=document.querySelector('.stm');if(!root||!('IntersectionObserver' in window))return;root.classList.add('stm-js');
  var els=root.querySelectorAll('.stm-h2,.stm-cx,.stm-fc,.stm-ws,.stm-tl,.stm-gauges,.stm-radar,.stm-tides,.stm-check,.stm-nums,.stm-biz,.stm-share,.stm-app,.stm-keep');
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('stm-in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.05});
  for(var i=0;i<els.length;i++){els[i].classList.add('stm-rv');io.observe(els[i])}
  var links={},nav=root.querySelector('.stm-navin');root.querySelectorAll('.stm-navin a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
  var spy=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;var a=links[e.target.id];if(!a)return;for(var k in links)links[k].classList.remove('stm-act');a.classList.add('stm-act');
    if(nav){var l=a.offsetLeft-nav.clientWidth/2+a.clientWidth/2;nav.scrollTo?nav.scrollTo({left:l,behavior:'smooth'}):(nav.scrollLeft=l)}})},{rootMargin:'-35% 0px -60% 0px'});
  root.querySelectorAll('h2[id]').forEach(function(h){spy.observe(h)});
  var top=$('stm-totop'),hero=root.querySelector('.stm-hero');if(top&&hero){new IntersectionObserver(function(es){top.classList.toggle('stm-show',!es[0].isIntersecting)}).observe(hero)}}
/* ---------- run ---------- */
function run(){
if($('stm-ribbon'))$('stm-ribbon').classList.add('stm-loading');
Promise.all([forecast().catch(function(){}),alerts().catch(function(){}).then(function(){return tides().catch(function(){})}),obs().catch(function(){}),qpf().catch(function(){})]).then(function(){if($('stm-ribbon'))$('stm-ribbon').classList.remove('stm-loading')});
}
function go(){
document.addEventListener('change',function(e){if(e.target&&e.target.classList&&e.target.classList.contains('stm-cb'))prog()});
restore();ticks();scrollFx();countdown();setInterval(countdown,1000);
run();setInterval(run,10*60*1000);setInterval(ago,30000);
['stm-save','stm-save2'].forEach(function(id){var b=$(id);if(b)b.addEventListener('click',save)});
var r=$('stm-ref');if(r)r.addEventListener('click',function(){r.classList.add('stm-spin');run();setTimeout(function(){r.classList.remove('stm-spin')},600)});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
