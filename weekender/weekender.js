/* The Weekender: live behavior. Everything degrades gracefully: the static HTML is complete without this file. */
(function(){
'use strict';
var root=document.getElementById('wk-top');if(!root)return;
var $=function(id){return document.getElementById(id)};
var $$=function(sel,el){return Array.prototype.slice.call((el||root).querySelectorAll(sel))};
var LAT=40.9387,LON=-73.1182;
/* a photo that fails to load (e.g. the CDN is still fetching a just-published file) gets one more try */
root.addEventListener('error',function(e){var t=e.target;if(!t||t.tagName!=='IMG'||t.getAttribute('data-rt')||t.hasAttribute('onerror')||!t.getAttribute('src'))return;t.setAttribute('data-rt','1');setTimeout(function(){var s=t.getAttribute('src');t.src=s+(s.indexOf('?')<0?'?':'&')+'r=1'},1500)},true);
var START=new Date(root.getAttribute('data-start')),END=new Date(root.getAttribute('data-end'));
var DAYS={fri:null,sat:null,sun:null};
var DAYC={fri:'#ff8a3d',sat:'#ffc145',sun:'#4dd6c1'};
var DAYN={fri:'Friday',sat:'Saturday',sun:'Sunday'};
function DAYN2(d){return ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getDay()]+' '+tm(d)}
var TAGI={free:'&#127903;&#65039;',kids:'&#129490;',outdoor:'&#127795;',music:'&#127928;',history:'&#128373;&#65039;',food:'&#127822;',arts:'&#127912;',stage:'&#127917;'};
function now(){var q=location.search.match(/wknow=([^&]+)/);return q?new Date(decodeURIComponent(q[1])):new Date()}
function ds(d){return ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getDay()]+', '+['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getMonth()]+' '+d.getDate()}
function tm(d){var h=d.getHours(),m=d.getMinutes(),ap=h>=12?'PM':'AM';h=h%12||12;return h+(m?':'+(m<10?'0':'')+m:'')+' '+ap}
function pad(n){return(n<10?'0':'')+n}
function toast(msg){var t=$('wk-toast');if(!t)return;t.textContent=msg;t.classList.add('is-on');clearTimeout(t._t);t._t=setTimeout(function(){t.classList.remove('is-on')},2200)}
function track(name,params){try{if(window.gtag)window.gtag('event',name,params||{})}catch(e){}}
var store={get:function(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}},set:function(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};

/* ---------- events index ---------- */
var EV={},LIST=[];
function indexEvents(){EV={};
  $$('[data-id][data-start]').forEach(function(el){var id=el.getAttribute('data-id');if(EV[id])return;
    EV[id]={id:id,el:el,day:el.getAttribute('data-day'),start:new Date(el.getAttribute('data-start')),end:new Date(el.getAttribute('data-end')),
    tags:(el.getAttribute('data-tags')||'').split(' '),img:el.getAttribute('data-img')||'',lat:+el.getAttribute('data-lat'),lon:+el.getAttribute('data-lon'),
    title:el.getAttribute('data-title'),venue:el.getAttribute('data-venue'),addr:el.getAttribute('data-addr')}});
  LIST=Object.keys(EV).map(function(k){return EV[k]}).filter(function(e){return !e.el.getAttribute('data-off')}).sort(function(a,b){return a.start-b.start})}

/* ---------- LIVE DATA: rebuild schedule, picks and closings from the hourly events.json ---------- */
var LIVEURL=root.getAttribute('data-live')||'https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/weekender/live/events.json';
var CALP='https://www.threevillagelocal.com/events-calendar';  /* where a Things to Do card goes when its event has no page of its own */
var TAGL={free:'Free',kids:'Kids',outdoor:'Outdoor',music:'Music',history:'History',food:'Food',arts:'Arts',stage:'On Stage'};
function fnv(s){s=unescape(encodeURIComponent(s));for(var h=0x811c9dc5,i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),0x01000193)>>>0;return ('0000000'+h.toString(16)).slice(-8)}
function sm(u,w){u=String(u||'');if(!u||/\.svg(\?|$)|^data:|wsrv\.nl|google\.com\/s2\/favicons|threevillagelocal-cloud\.github\.io|cdn\.jsdelivr\.net\/gh\/threevillagelocal-cloud\/.*\.webp$/i.test(u))return u;if(u.charAt(0)==='/'&&u.charAt(1)!=='/')u=location.origin+u;
  return /^https?:/i.test(u)?'https://threevillagelocal-cloud.github.io/3vl-share/t/'+fnv(u)+'-'+(w>400?800:360)+'.webp':u}  /* our small WebP copy (3vl-share/t/gen.py makes them every 30 min); some originals are 6 MB */
function bgfix(root){[].forEach.call((root||document).querySelectorAll('[data-bgo]'),function(el){var m=(el.getAttribute('style')||'').match(/url\('([^']+)'\)/);if(!m||m[1]===el.getAttribute('data-bgo'))return;
  var i=new Image();i.onerror=function(){el.style.backgroundImage="url('"+el.getAttribute('data-bgo')+"')"};i.src=m[1]})}  /* background photo whose copy isn't made yet: use the original */
function smi(u,w,sz){var s=sm(u,w),q=function(x){return String(x).replace(/&/g,'&amp;').replace(/"/g,'&quot;')};if(sz&&s===u&&/cdn[.]jsdelivr[.]net.*-720[.]webp$/.test(u)){var b=u.slice(0,-9);return 'src="'+q(u)+'" srcset="'+q(b+'-360.webp')+' 360w, '+q(b+'-540.webp')+' 540w, '+q(u)+' 720w" sizes="'+sz+'" onerror="if(this.srcset)this.removeAttribute(&quot;srcset&quot;)"'}return s===u?'src="'+q(u)+'"':'src="'+q(s)+'" data-o="'+q(u)+'" onerror="if(this.dataset.o){this.src=this.dataset.o;this.dataset.o=\'\'}"'}  /* <img> attrs; falls back to the original if the copy is missing */
function esc2(x){return String(x||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function dkey(d){return 'd'+d.getFullYear()+('0'+(d.getMonth()+1)).slice(-2)+('0'+d.getDate()).slice(-2)}
function renderLive(data){
  var t=now(),t0=new Date(t.getFullYear(),t.getMonth(),t.getDate()),end=new Date(t0.getTime()+(9-((t0.getDay()+6)%7>4?0:0))*864e5),IC=data.icons||{};
  var AB=root.getAttribute('data-assets')||'',MB='https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@master/weekender/';
  var evs=(data.events||[]).map(function(e){if(AB&&e.img&&e.img.indexOf(MB)===0)e.img=AB+e.img.slice(MB.length);e.s=new Date(e.start);e.e=new Date(e.end||e.start);if(e.e<=e.s)e.e=new Date(e.s.getTime()+(e.allday?864e5:5400e3));return e})
    .filter(function(e){return e.e>t&&e.s<end}).sort(function(a,b){return a.s-b.s});
  if(!evs.length)return false;
  var gm=function(e){return 'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent((e.venue||'')+', '+(e.addr||''))};
  var acts=function(e){return '<div class="wk-acts"><button type="button" class="wk-save" data-save="'+e.id+'" aria-pressed="false"><span class="wk-star">&#9734;</span><span class="wk-savet">Save</span></button><button type="button" class="wk-cal" data-cal="'+e.id+'">&#128197; Add</button><a class="wk-dir" href="'+gm(e)+'" target="_blank" rel="noopener">&#128205; Map</a></div>'};
  var chips=function(tg){return tg.map(function(x){return '<span class="wk-tag" data-t="'+x+'">'+(TAGL[x]||x)+'</span>'}).join('')};
  var attrs=function(e){var d=e.s,wk=(d.getDay()===0||d.getDay()===6||(d.getDay()===5&&d.getHours()>=15));
    return 'data-id="'+esc2(e.id)+'" data-day="'+dkey(d)+'" data-wknd="'+(wk?1:0)+'" data-start="'+e.s.toISOString()+'" data-end="'+e.e.toISOString()+'" data-tags="'+esc2(e.tags.join(' '))+'" data-title="'+esc2(e.title)+'" data-venue="'+esc2(e.venue)+'" data-addr="'+esc2(e.addr)+'" data-img="'+esc2(e.img)+'"'+(e.status?' data-off="'+esc2(e.status)+'"':'')};
  var md=function(e){return e.e-e.s>864e5*1.1},thru=function(e){return 'thru '+['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][e.e.getMonth()]+' '+e.e.getDate()};
  var when=function(e){return e.s<t0?'Ongoing':e.allday?'All day':tm(e.s)};
  /* schedule: tabs + one block per day */
  var sec=$('wk-sched');if(sec){
    var days={};evs.forEach(function(e){if(e.ongoing)return;var sd=e.s<t0?t0:e.s,k=dkey(sd);(days[k]=days[k]||{d:new Date(sd.getFullYear(),sd.getMonth(),sd.getDate()),l:[]}).l.push(e)});  /* ongoing events roll forward into Today */
    var tabs=root.querySelector('.wk-tabs');
    if(tabs)tabs.innerHTML='<button type="button" role="tab" class="wk-tab is-on" data-day="all">This Week</button><button type="button" role="tab" class="wk-tab" data-day="'+dkey(t0)+'">Today</button><button type="button" role="tab" class="wk-tab" data-day="'+dkey(new Date(t0.getTime()+864e5))+'">Tomorrow</button><button type="button" role="tab" class="wk-tab" data-day="wknd">Weekend</button><span class="wk-tabink" aria-hidden="true"></span>';
    $$('.wk-dayblk',sec).forEach(function(b){b.remove()});
    var anchor=root.querySelector('#wk-sched .wk-allwk')||$('wk-nomatch');
    Object.keys(days).sort().forEach(function(k,di){var D=days[k],isT=k===dkey(t0),isTm=k===dkey(new Date(t0.getTime()+864e5));
      var h=(di?'':'<p class="wk-daytip">&#128073; Tap a day to see what&rsquo;s up</p>')+'<div class="wk-dayblk is-collapsed" data-day="'+k+'"><p class="wk-dayh" role="button" tabindex="0" aria-expanded="false"><b>'+(isT?'Today':isTm?'Tomorrow':DAYN2x(D.d))+'</b><span>'+ds(D.d)+'</span><i class="wk-dcount">'+D.l.length+' event'+(D.l.length===1?'':'s')+'</i><em class="wk-chev" aria-hidden="true"></em></p><ol class="wk-tl">';
      D.l.forEach(function(e){var th=e.img?'<img '+smi(e.img,360)+' alt="" loading="lazy" width="120" height="120">':'<span class="wk-ticon">'+(IC[(e.tags.filter(function(x){return x!=='free'})[0])||'arts']||'&#9733;')+'</span>';
        h+='<li class="wk-ev" '+attrs(e)+'><div class="wk-evt"><b>'+when(e)+'</b><span>'+(md(e)?thru(e):e.allday?'':'to '+tm(e.e))+'</span></div><div class="wk-evc"><div class="wk-evthumb">'+th+'</div><div class="wk-evbody">'+
          '<p class="wk-evtitle">'+(e.url?'<a href="'+esc2(e.url)+'" target="_blank" rel="noopener">'+esc2(e.title)+'</a>':esc2(e.title))+' <span class="wk-pstat" data-status></span></p><p class="wk-evwhere">'+esc2(e.venue)+'</p>'+
          (e.desc?'<p class="wk-evdesc" tabindex="0">'+esc2(e.desc)+'</p>':'')+'<div class="wk-tags">'+chips(e.tags)+'<span class="wk-wxchip"></span></div></div>'+acts(e)+'</div></li>'});
      h+='</ol></div>';anchor.insertAdjacentHTML('beforebegin',h)});
    var sm=root.querySelector('#wk-sched .wk-h2 small');if(sm)sm.innerHTML='Updated '+tm(new Date(data.updated))+' &middot; tap &#9734; to save';
    var sp=root.querySelector('#wk-sched .wk-h2 span');if(sp)sp.textContent='What\u2019s Happening This Week';
    var aw=root.querySelector('#wk-sched .wk-allwk p.wk-dayh b');if(aw)aw.textContent='Ongoing';
  }
  /* top things to do: soonest upcoming events that have photos (curated picks first); the build's "Coming up" radar cards stay at the end */
  var RAD=(function(){var b=document.querySelector('#wk-picks .wk-picks');return b?[].slice.call(b.querySelectorAll('.wk-radar')):[]})();
  var pk=$('wk-picks'),box=pk&&pk.querySelector('.wk-picks');
  if(box){var cand=evs.filter(function(e){return e.img&&!e.fb&&!e.status&&(e.pu?new Date(e.pu):e.e)>t}).sort(function(a,b){return (b.pick?1:0)-(a.pick?1:0)||(a.rank||9)-(b.rank||9)||a.s-b.s});
    var cur=cand.filter(function(e){return e.pick}),soon=cand.filter(function(e){return !e.pick&&e.s<new Date(t0.getTime()+3*864e5)}),pick=cur.concat(soon,cand.filter(function(e){return cur.indexOf(e)<0&&soon.indexOf(e)<0})).slice(0,6);
    if(pick.length>=3)box.innerHTML=pick.map(function(e,i){return '<article class="wk-pick wk-rv is-in" data-href="'+esc2(e.page||CALP)+'" '+attrs(e).replace('data-id="','data-id="pk-')+'><div class="wk-pimg"><img '+smi(e.img,900,'280px')+' alt="'+esc2(e.title)+'" loading="lazy"><span class="wk-pnum">0'+(i+1)+'</span>'+(e.ongoing?'':'<span class="wk-pstat" data-status></span>')+'</div>'+
      '<div class="wk-pbody"><p class="wk-pwhen">'+(e.ongoing?esc2(e.whenText):ds(e.s)+' &middot; '+when(e))+'</p><h3 class="wk-ptitle"><a href="'+esc2(e.page||CALP)+'">'+esc2(e.title)+'</a></h3><p class="wk-pwhere">&#128205; '+esc2(e.venue)+'</p><p class="wk-pdesc">'+esc2(e.desc)+'</p><div class="wk-tags">'+chips(e.tags)+'</div>'+(e.ongoing?acts(e).replace(/<button type="button" class="wk-cal"[^<]*<\/button>/,'<a class="wk-dir" href="'+esc2(e.url)+'" target="_blank" rel="noopener">&#128279; Details</a>'):acts(e))+'</div></article>'}).join('')}
  if(box)RAD.forEach(function(r){if(!box.contains(r)){r.classList.add('is-in');box.appendChild(r)}});
  /* 3VL guide articles (weekend.json guides via #wk-top data-guides): link matching Top Things to Do cards (9/28) */
  (function(){var G=[];try{G=JSON.parse((document.getElementById('wk-top')||{getAttribute:function(){return '[]'}}).getAttribute('data-guides')||'[]')}catch(e){}
    if(!G.length||!box)return;[].forEach.call(box.querySelectorAll('.wk-pick'),function(c){var h=c.querySelector('.wk-ptitle');if(!h||c.querySelector('.wk-guide'))return;var tt=h.textContent.toLowerCase();
      G.forEach(function(g){if(tt.indexOf(g[0])<0)return;c.setAttribute('data-href',g[1]);h.innerHTML='<a href="'+g[1]+'">'+esc2(h.textContent)+'</a>';var a=c.querySelector('.wk-acts');
        var l=document.createElement('a');l.className='wk-guide';l.href=g[1];l.innerHTML='&#128373;&#65039; '+esc2(g[2]);if(a)a.insertBefore(l,a.firstChild);else c.querySelector('.wk-pbody').appendChild(l)})})})();
  /* closings strip: only show items that are today or later */
  var cx=$('wk-cx');if(cx){var items=(data.closings||[]).filter(function(c){return new Date(c.date+'T23:59:00')>=t0});
    if(!items.length)cx.remove();else{var row=cx.querySelector('.wk-cxrow');if(row)row.innerHTML=items.map(function(c){return '<div class="wk-cxi" data-off="'+esc2(c.status)+'"><p class="wk-cxn">'+esc2(c.title)+'</p><p class="wk-cxd">'+esc2(c.note)+'</p></div>'}).join('')}}
  /* Port Jefferson Ferry strip (live/ferry.py): same look as the storm closings strip, only when the ferry posts a SERVICE alert
     (cancellations, delays, weather, schedule changes) or the schedule marks cancelled trips. Nothing shows on a normal day. */
  (function(){var f=data.ferry,old=$('wk-ferry');if(old)old.remove();if(!f||!((f.alerts||[]).length||f.cancellations))return;
    var items=(f.alerts||[]).map(function(a){return [/cancel|suspend|not running|no service/i.test(a.title+' '+a.text)?'Cancelled':'Alert',a.title,a.text,a.link||f.url]});
    if(f.cancellations&&!items.some(function(x){return x[0]==='Cancelled'}))items.unshift(['Cancelled','Some ferry trips are cancelled today','Check the schedule before you head to the dock.',f.url]);
    var s=document.createElement('section');s.className='wk-sec wk-cxsec';s.id='wk-ferry';
    s.innerHTML='<div class="wk-cxhead"><span class="wk-live wk-ferryp"><i></i>FERRY</span><p><b>Port Jefferson Ferry</b> service update</p><a class="wk-cxall" href="'+esc2(f.url)+'" target="_blank" rel="noopener">Ferry schedule &rarr;</a></div>'+
      '<div class="wk-cxrow wk-swipe">'+items.map(function(x){return '<a class="wk-cxi" data-off="'+esc2(x[0])+'" href="'+esc2(x[3])+'" target="_blank" rel="noopener"><p class="wk-cxn">'+esc2(x[1])+'</p>'+(x[2]?'<p class="wk-cxd">'+esc2(x[2])+'</p>':'')+'</a>'}).join('')+'</div>';
    var main=document.querySelector('#wk-top .wk-main'),first=$('wk-cx')||$('wk-picks');if(main){if(first&&first.parentNode===main)main.insertBefore(s,first);else main.insertBefore(s,main.firstChild)}})();
  /* Eat & Drink: walk the owner's ranked list (data.eatOrder). Each place shows its Instagram special if it has one,
     else this week's hand-picked card, else it is skipped. Hand-picked places not on the list go last. Max data.eatCap. */
  var eat=document.querySelector('#wk-eat .wk-eat'),order=data.eatOrder||[];
  if(eat&&order.length){var nm=function(x){return String(x||'').toLowerCase().replace(/&[a-z#0-9]+;/g,'').replace(/\(.*?\)/g,'').replace(/[^a-z0-9]/g,'').replace(/^the/,'')};
    var cur={},ig={},out=[],used={};
    [].forEach.call(eat.querySelectorAll('.wk-sp'),function(a){var b=a.querySelector('.wk-spbiz');if(b)cur[nm(b.textContent)]=a});
    (data.specials||[]).forEach(function(x){if(!ig[nm(x.biz)])ig[nm(x.biz)]=x});
    var card=function(x,old){var big=x.img||x.inset,small=x.img?x.inset:'',ob=old&&old.querySelector('.wk-spbiz');
      var map='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(x.biz.replace(/\s*\(.*?\)/,'')+', '+(x.town||'Three Village')+', NY');
      var t=document.createElement('div');
      t.innerHTML='<article class="wk-sp wk-rv is-in"'+(x.page?' data-href="'+esc2(x.page)+'"':'')+'>'+(big?'<div class="wk-eimg"><img '+smi(big,800,'(max-width:760px) 280px, 470px')+' alt="'+esc2(x.biz)+'" loading="lazy">'+(small?'<span class="wk-dish"><img '+smi(small,300,'96px')+' alt="Food at '+esc2(x.biz)+'" loading="lazy"></span>':'')+'</div>':'')+
       '<div class="wk-spb"><p class="wk-spbiz">'+(ob?ob.innerHTML:x.page?'<a class="wk-biz" href="'+esc2(x.page)+'">'+esc2(x.biz.replace(/\s*\(.*?\)/,''))+'</a>':esc2(x.biz.replace(/\s*\(.*?\)/,'')))+'</p><p class="wk-spt">'+esc2(x.title)+'</p>'+(x.when?'<p class="wk-spw">'+esc2(x.when)+'</p>':'')+'<p class="wk-spd">'+esc2(x.desc)+'</p>'+
       '<p class="wk-spf"><span class="wk-src wk-igb">&#9711;</span><span>via <a class="wk-biz" href="'+esc2(x.url)+'" target="_blank" rel="noopener">Instagram</a></span><a class="wk-dir" href="'+esc2(map)+'" target="_blank" rel="noopener">&#128205; Map</a></p></div></article>';
      return t.firstChild};
    /* owner 10/10/2026 "refresh the 6": places with a current special come first (ranked order); last week's hand-picked
       cards only fill slots that are left */
    order.forEach(function(n){var k=nm(n);if(used[k]||!ig[k])return;used[k]=1;out.push(card(ig[k],cur[k]))});
    order.forEach(function(n){var k=nm(n);if(used[k]||!cur[k])return;used[k]=1;out.push(cur[k])});
    Object.keys(cur).forEach(function(k){if(!used[k])out.push(cur[k])});
    out=out.slice(0,data.eatCap||9);eat.innerHTML='';out.forEach(function(a){eat.appendChild(a)})}
  return true}
function DAYN2x(d){return ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][d.getDay()]}

/* ---------- hero: leaves + countdown ---------- */
function leaves(){var box=root.querySelector('.wk-leaves');if(!box||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  var set=['&#127810;','&#127809;','&#127810;','&#127811;'];
  for(var i=0;i<14;i++){var s=document.createElement('span');s.className='wk-leaf';s.innerHTML=set[i%set.length];
    s.style.left=(Math.random()*100)+'%';s.style.animationDuration=(9+Math.random()*9)+'s';s.style.animationDelay=(-Math.random()*16)+'s';
    s.style.fontSize=(14+Math.random()*16)+'px';s.style.setProperty('--dx',(Math.random()*160-80)+'px');s.style.setProperty('--r',(Math.random()*720-360)+'deg');box.appendChild(s)}}
function countdown(){var c=$('wk-count'),l=$('wk-cl'),t=now(),target,label;if(!c||!l)return;
  if(t<START){target=START;label='The weekend starts in'}else if(t<END){target=END;label='&#9679; Live now. Weekend ends in';c.classList.add('is-live')}else{l.innerHTML='That’s a wrap. See you next weekend';$('wk-cv').style.display='none';return}
  l.innerHTML=label;var s=Math.max(0,Math.floor((target-t)/1000));
  var v={d:Math.floor(s/86400),h:pad(Math.floor(s%86400/3600)),m:pad(Math.floor(s%3600/60)),s:pad(s%60)};
  $$('#wk-cv i').forEach(function(i){var u=i.getAttribute('data-u');if(i.textContent!=String(v[u]))i.textContent=v[u]})}


/* ---------- compact live hero ---------- */
function heroLive(){var t=now(),d=$('wk-hdate'),c=$('wk-hclock');
  if(d)d.textContent=t.toLocaleDateString('en-US',{weekday:'long',month:'short',day:'numeric'});
  if(c)c.textContent=tm(t);
  var live=LIST.filter(function(e){return isLive(e,t)}),next=LIST.filter(function(e){return e.start>t})[0],n=$('wk-hnow'),x=$('wk-hnext');
  if(n)n.textContent=live.length?live.length+(live.length===1?' event':' events'):'Quiet now';
  if(x)x.textContent=next?'Next: '+next.title.slice(0,34)+(next.title.length>34?'...':'')+(next.start.toDateString()===t.toDateString()?' at '+tm(next.start):', '+ds(next.start)):'See the full schedule';}
function heroWx(){fetch('https://api.weather.gov/points/'+LAT+','+LON).then(function(r){return r.json()}).then(function(p){return fetch(p.properties.forecastHourly)}).then(function(r){return r.json()}).then(function(d){
  var p=(d.properties.periods||[])[0];if(!p)return;var te=$('wk-htemp'),sk=$('wk-hsky'),ic=$('wk-hwi2');
  if(te)te.textContent=p.temperature;if(sk)sk.textContent=p.shortForecast+(p.windSpeed?', wind '+p.windSpeed:'');if(ic)ic.innerHTML=wxSvg(p.shortForecast)}).catch(function(){})}

/* ---------- count-up stats ---------- */
function countUp(el){var n=+el.getAttribute('data-n'),t0=null;function f(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/1200);el.textContent=Math.round(n*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)}requestAnimationFrame(f)}

/* ---------- sunset (NOAA approximation) ---------- */
function sunset(date){var rad=Math.PI/180,day=Math.floor((Date.UTC(date.getFullYear(),date.getMonth(),date.getDate())-Date.UTC(date.getFullYear(),0,0))/864e5);
  var g=2*Math.PI/365*(day-1+.5),eq=229.18*(.000075+.001868*Math.cos(g)-.032077*Math.sin(g)-.014615*Math.cos(2*g)-.040849*Math.sin(2*g)),
  dec=.006918-.399912*Math.cos(g)+.070257*Math.sin(g)-.006758*Math.cos(2*g)+.000907*Math.sin(2*g)-.002697*Math.cos(3*g)+.00148*Math.sin(3*g),
  ha=Math.acos(Math.cos(90.833*rad)/(Math.cos(LAT*rad)*Math.cos(dec))-Math.tan(LAT*rad)*Math.tan(dec))/rad,
  mins=720-4*(LON-ha)-eq;var d=new Date(Date.UTC(date.getFullYear(),date.getMonth(),date.getDate())+mins*60000);return d}

/* "happening now": one-day events use their real start/end. Events that run for days or weeks are only live during
   their daily hours (the start/end clock times when given, else 10 AM to 6 PM), never overnight (owner 9/28/2026). */
function isLive(e,t){if(!(t>=e.start&&t<e.end))return false;if(e.end-e.start<=864e5*1.1)return true;
  var m=t.getHours()*60+t.getMinutes(),a=e.start.getHours()*60+e.start.getMinutes(),b=e.end.getHours()*60+e.end.getMinutes();
  if(a===0||b<=a){a=600;b=1080}return m>=a&&m<b}
/* ---------- status chips: live / soon / done ---------- */
function statuses(){var t=now();
  LIST.forEach(function(e){var txt='',cls='';
    if(isLive(e,t)){txt='Happening now';cls='is-now'}
    else if(e.start>t&&e.start-t<3*3600e3){var m=Math.round((e.start-t)/60000);txt='Starts in '+(m>=60?Math.floor(m/60)+'h '+(m%60)+'m':m+' min');cls='is-soon'}
    else if(t>=e.end&&t-e.end<12*3600e3){txt='Wrapped';cls='is-done'}
    $$('[data-id="'+e.id+'"] [data-status]').forEach(function(s){s.textContent=txt;s.className='wk-pstat '+cls});
    $$('.wk-ev[data-id="'+e.id+'"]').forEach(function(li){li.classList.toggle('is-now',cls==='is-now')})})}

/* ---------- happening now panel ---------- */
function nowPanel(){var b=$('wk-nowb'),c=$('wk-clock');if(!b)return;var t=now();
  c.textContent=tm(t).replace(' ',' ');
  var live=LIST.filter(function(e){return isLive(e,t)}),next=LIST.filter(function(e){return e.start>t}).slice(0,live.length?2:4);
  var h='';
  function row(e,isLive){var p=isLive?Math.round((t-e.start)/(e.end-e.start)*100):0,lbl;
    if(isLive){var left=Math.round((e.end-t)/60000);lbl=(left>=60?Math.floor(left/60)+'h':left+'m')+'<br><small style="font-size:8px">left</small>'}
    else{var d=Math.round((e.start-t)/60000);lbl=d<60?d+'m':d<1440?Math.floor(d/60)+'h':ds(e.start).split(', ')[1]}
    var pic=e.img?'<img '+smi(e.img,240)+' alt="" loading="lazy">':'<span class="wk-nowico">'+(TAGI[e.tags.filter(function(t){return t!=="free"&&t!=="outdoor"})[0]||e.tags[0]]||'&#9733;')+'</span>';
    return '<a class="wk-nowi" href="#'+e.el.id+'" data-jump="'+e.id+'"><span class="wk-nowpic">'+pic+'</span><span class="wk-nowtx"><b>'+e.title+'</b><small>'+e.venue+' &middot; '+(isLive?'until '+tm(e.end):ds(e.start)+', '+tm(e.start))+'</small></span><span class="wk-nowbar" style="--p:'+p+'"><span>'+lbl+'</span></span></a>'}
  if(live.length){h+='<p class="wk-nowsub">&#9679; On right now &middot; '+live.length+'</p>';live.slice(0,4).forEach(function(e){h+=row(e,true)});if(live.length>4)h+='<a class="wk-nowmore" href="#wk-sched">+ '+(live.length-4)+' more happening now &rarr;</a>'}
  if(next.length){h+='<p class="wk-nowsub">'+(t<START?'Coming up':'Up next')+'</p>';next.forEach(function(e){h+=row(e,false)})}
  if(!h)h='<p class="wk-nowempty">That’s a wrap on this weekend. The next Weekender drops Thursday.</p>';
  b.innerHTML=h}

/* ---------- live feed ---------- */
var seen=store.get('wkFeedSeen',{}),firstLoad=true;
function ago(s){var d=/T/.test(s)?new Date(s):null,t=now();
  if(!d){var day=new Date(s+'T12:00:00'),diff=Math.round((new Date(t.getFullYear(),t.getMonth(),t.getDate())-new Date(day.getFullYear(),day.getMonth(),day.getDate()))/864e5);return diff<=0?'Today':diff===1?'Yesterday':diff+' days ago'}
  var m=Math.round((t-d)/60000);if(m<1)return'Just now';if(m<60)return m+' min ago';if(m<1440)return Math.floor(m/60)+' hr ago';var dd=Math.floor(m/1440);return dd===1?'Yesterday':dd+' days ago'}
var ICONS={joke:'&#128679;',facebook:'f',instagram:'&#9711;',tiktok:'&#9834;',alert:'!',news:'N',web:'&#8599;',nws:'&#9888;'};
function drawFeed(items){var ol=$('wk-flist'),tk=$('wk-tkt');if(!ol&&!tk)return;
  items.sort(function(a,b){return(b.t>a.t)?1:-1});
  if(ol)ol.innerHTML=items.slice(0,14).map(function(it,i){var key=it.who+it.text,isNew=!firstLoad&&!seen[key];seen[key]=1;
    var host='';try{host=it.url?new URL(it.url).hostname:''}catch(e){}var logo=it.logo||(host&&!/facebook\.com$/.test(host)&&it.src!=='nws'?'https://www.google.com/s2/favicons?sz=64&domain='+host:'');
    return '<li class="wk-fi'+(isNew?' is-new':'')+'" style="animation-delay:'+(i*60)+'ms"><span class="wk-fic s-'+it.src+(logo?' has-logo':'')+'">'+(logo?'<img '+smi(logo,120)+' alt="" loading="lazy">':(ICONS[it.src]||'&#8226;'))+'</span><div><p class="wk-fw"><b>'+it.who+'</b> &middot; <span data-ago="'+it.t+'">'+ago(it.t)+'</span></p><p class="wk-ft">'+(it.url?'<a href="'+it.url+'" target="_blank" rel="noopener">'+it.text+'</a>':it.text)+'</p></div></li>'}).join('');
  store.set('wkFeedSeen',seen);firstLoad=false;
  /* ticker only runs for big news: breaking items in feed.json or an active NWS warning */
  var big=items.filter(function(it){return it.breaking||(it.src==='nws'&&/Warning|Emergency/i.test(it.text))});
  var bar=$('wk-ticker');if(tk&&bar){if(big.length){var s=big.slice(0,6).map(function(it){return '<span><b>'+it.who+'</b>'+it.text+'</span>'}).join('');if(RM){tk.innerHTML=s;bar.classList.add('is-rot');tkI=0;tkRot();if(!tkT)tkT=setInterval(tkRot,5000)}else{tk.innerHTML=s+s+s}bar.hidden=false}else{bar.hidden=true}}}
var RM=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches),tkI=0,tkT=null;
function tkRot(){var sp=$$('#wk-tkt span');if(!sp.length)return;tkI=tkI%sp.length;sp.forEach(function(x,i){x.classList.toggle('on',i===tkI)});tkI++}
var JOKES=[];
var feedItems=[],nwsItems=[];
function loadFeed(){var url=root.getAttribute('data-feed');if(!url)return;
  fetch(url+(url.indexOf('?')<0?'?':'&')+'v='+Math.floor(Date.now()/60000),{cache:'no-store'}).then(function(r){return r.json()}).then(function(d){feedItems=d.items||[];JOKES=d.jokes||[];if(JOKES.length&&!feedItems.some(function(x){return x.src==='joke'})){feedItems.push({t:new Date().toISOString(),src:'joke',who:'347 Traffic Desk',text:JOKES[Math.floor(Math.random()*JOKES.length)]})}drawFeed(feedItems.concat(nwsItems));
    var u=$('wk-fupd');if(u)u.textContent='synced '+tm(new Date())}).catch(function(){var u=$('wk-fupd');if(u)u.textContent='offline'})}
function loadAlerts(){fetch('https://api.weather.gov/alerts/active?point='+LAT+','+LON).then(function(r){return r.json()}).then(function(d){
  nwsItems=(d.features||[]).slice(0,3).map(function(f){var p=f.properties;return{t:p.sent,src:'nws',who:'National Weather Service',text:p.event+(p.ends||p.expires?' in effect until '+DAYN2(new Date(p.ends||p.expires))+'.':'.'),url:'https://forecast.weather.gov/MapClick.php?lat='+LAT+'&lon='+LON}});
  drawFeed(feedItems.concat(nwsItems))}).catch(function(){})}


/* ---------- animated weather icons (inline SVG, CSS-animated) ---------- */
function wxSvg(short){var s=(short||'').toLowerCase(),sun='<g class="wi-sun"><circle cx="32" cy="30" r="11" fill="#FFC845"/><g class="wi-rays" stroke="#FFC845" stroke-width="3" stroke-linecap="round"><path d="M32 10v5M32 45v5M12 30h5M47 30h5M18 16l3.5 3.5M42.5 40.5L46 44M18 44l3.5-3.5M42.5 19.5L46 16"/></g></g>',
  cloud=function(x,y,c){return '<g class="wi-cloud" transform="translate('+x+' '+y+')"><path d="M14 36h30a10 10 0 0 0 0-20 14 14 0 0 0-27-3A10 10 0 0 0 14 36z" fill="'+(c||'#E8EEF6')+'"/></g>'},
  drops='<g class="wi-rain" stroke="#7CC4FF" stroke-width="3" stroke-linecap="round"><path class="d1" d="M24 46l-3 7"/><path class="d2" d="M34 46l-3 7"/><path class="d3" d="M44 46l-3 7"/></g>',
  bolt='<path class="wi-bolt" d="M34 40l-7 12h7l-4 10 12-15h-7l4-7z" fill="#FFD23F"/>',
  snow='<g class="wi-snow" fill="#fff"><circle class="d1" cx="24" cy="50" r="2.2"/><circle class="d2" cx="34" cy="52" r="2.2"/><circle class="d3" cx="44" cy="50" r="2.2"/></g>',
  body;
  if(/thunder/.test(s))body=cloud(2,2,'#C9D5E3')+bolt;
  else if(/snow|flurr/.test(s))body=cloud(2,2)+snow;
  else if(/rain|shower|drizzle/.test(s))body=cloud(2,0,'#D5DEEA')+drops;
  else if(/fog|haze|mist/.test(s))body='<g class="wi-fog" stroke="#E8EEF6" stroke-width="4" stroke-linecap="round"><path d="M12 26h40"/><path class="d2" d="M16 36h36"/><path d="M12 46h32"/></g>';
  else if(/partly|mostly sunny|mostly clear/.test(s))body=sun.replace('cx="32" cy="30"','cx="24" cy="24"').replace('<path d="M32','<path transform="translate(-8 -6)" d="M32')+cloud(8,10);
  else if(/cloud|overcast/.test(s))body=cloud(-4,-6,'#B8C6D8')+cloud(6,6);
  else body=sun;
  return '<svg class="wi" viewBox="0 0 64 64" aria-hidden="true">'+body+'</svg>'}

/* ---------- weather ---------- */
var WX={};
function icon(s){s=s.toLowerCase();if(/thunder/.test(s))return'&#9928;&#65039;';if(/rain|shower/.test(s))return'&#127783;&#65039;';if(/snow/.test(s))return'&#10052;&#65039;';if(/fog/.test(s))return'&#127787;&#65039;';if(/partly|mostly sunny/.test(s))return'&#9925;';if(/cloud/.test(s))return'&#9729;&#65039;';return'&#9728;&#65039;'}
function score(w){var s=100;s-=Math.max(0,w.pop-10)*.9;s-=Math.max(0,w.wind-12)*2.2;if(w.hi<55)s-=(55-w.hi)*1.6;if(w.hi>86)s-=(w.hi-86)*2;return Math.max(5,Math.min(99,Math.round(s)))}
function paintWx(){var best=null;
  ['fri','sat','sun'].forEach(function(k){var w=WX[k],c=root.querySelector('.wk-wd[data-day='+k+']'),hw=root.querySelector('.wk-hwd[data-day='+k+']');
    var ss=DAYS[k]?sunset(DAYS[k]):null;if(c&&ss)c.querySelector('.wk-set').textContent=tm(ss);
    if(k==='sat'&&ss&&$('wk-sunset'))$('wk-sunset').textContent=tm(ss).replace(' PM','');
    if(!w||!c)return;var sc=score(w);w.score=sc;if(!best||sc>WX[best].score)best=k;
    c.querySelector('.wk-score').textContent=sc;c.querySelector('.wk-rfil').style.strokeDashoffset=314.16*(1-sc/100);
    c.querySelector('.wk-wicon').innerHTML=wxSvg(w.short);c.querySelector('.wk-hi').textContent=w.hi;c.querySelector('.wk-lo').textContent=w.lo==null?'':' / '+w.lo;
    c.querySelector('.wk-ws').textContent=w.short;c.querySelector('.wk-pop').textContent=w.pop+'%';
    c.querySelector('.wk-wind').textContent=w.wind+' mph';
    wxFx(k,w);
    if(hw){hw.querySelector('.wk-hwi').innerHTML=wxSvg(w.short);hw.querySelector('.wk-hwt').innerHTML=w.hi+'&deg;'}
    $$('.wk-ev[data-day='+k+']').forEach(function(li){var e=EV[li.getAttribute('data-id')],ch=li.querySelector('.wk-wxchip');if(!ch||!e||e.tags.indexOf('outdoor')<0)return;
      if(w.pop>=50){ch.innerHTML='&#9748; '+w.pop+'% rain, check plans';ch.className='wk-wxchip is-rain'}else if(sc>=75){ch.innerHTML='&#9728;&#65039; Great day for it';ch.className='wk-wxchip is-great'}})});
  $$('.wk-wd').forEach(function(c){c.classList.toggle('is-best',c.getAttribute('data-day')===best)});
  var v=$('wk-verdict');if(v&&best){var w=WX[best],bi=['fri','sat','sun'].indexOf(best),dn=bi===0?'Today':bi===1?'Tomorrow':['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][DAYS[best].getDay()];
    v.innerHTML=icon(w.short)+(w.pop>=60?' Wet few days ahead. <b>'+dn+'</b> is the best of the three: ':' <b>'+dn+'</b> looks like the best day to be outside: ')+w.short.toLowerCase()+', '+w.hi+'&deg;, '+w.pop+'% chance of rain.'}}
function loadWx(){fetch('https://api.weather.gov/points/'+LAT+','+LON).then(function(r){return r.json()}).then(function(p){return fetch(p.properties.forecast)}).then(function(r){return r.json()}).then(function(d){
  var per=d.properties.periods||[];
  ['fri','sat','sun'].forEach(function(k){if(!DAYS[k])return;var ds=DAYS[k].toDateString();
    var day=per.filter(function(p){return new Date(p.startTime).toDateString()===ds&&p.isDaytime})[0],night=per.filter(function(p){return new Date(p.startTime).toDateString()===ds&&!p.isDaytime})[0];
    if(!day&&!night)return;var b=day||night;
    WX[k]={short:b.shortForecast,hi:(day||b).temperature,lo:night?night.temperature:null,pop:(b.probabilityOfPrecipitation&&b.probabilityOfPrecipitation.value)||0,wind:parseInt(((b.windSpeed||'0').match(/(\d+)(?!.*\d)/)||[0,0])[1],10)}});
  if(!Object.keys(WX).length){var v=$('wk-verdict');if(v)v.innerHTML='&#128197; The National Weather Service forecast reaches this weekend by Tuesday. Scores fill in automatically.'}
  paintWx()}).catch(function(){paintWx()})}


/* ---------- weather tile backgrounds: live cams by day, animated photos otherwise, weather FX on top ---------- */
function wxScenes(){var real=new Date(),ss=sunset(real),dayLight=/wkcam=1/.test(location.search)||(real.getHours()>=7&&real<new Date(ss.getTime()-20*60000));
  $$('.wk-wd').forEach(function(c){var bg=c.querySelector('.wk-wbg'),cam=bg&&bg.getAttribute('data-cam'),live=c.querySelector('.wk-wlive');
    if(cam&&dayLight&&!bg.querySelector('iframe')&&!(navigator.connection&&navigator.connection.saveData)){
      var f=document.createElement('iframe');f.src=cam;f.title='Live camera';f.setAttribute('tabindex','-1');f.setAttribute('aria-hidden','true');f.setAttribute('allow','autoplay');
      f.onload=function(){setTimeout(function(){bg.classList.add('is-cam');if(live)live.hidden=false},2500)};bg.appendChild(f)}
    if(!dayLight&&bg&&bg.classList.contains('is-cam')){bg.classList.remove('is-cam');if(live)live.hidden=true;var fr=bg.querySelector('iframe');if(fr)fr.remove()}
    var clk=c.querySelector('.wk-wclk');if(clk)clk.textContent=tm(real)})}
function wxFx(k,w){var c=root.querySelector('.wk-wd[data-day='+k+'] .wk-wfx');if(!c||c.getAttribute('data-fx'))return;var s=(w.short||'').toLowerCase();
  if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  if(/rain|shower|storm|drizzle/.test(s)||w.pop>=50){c.setAttribute('data-fx','rain');var cv=document.createElement('canvas');c.appendChild(cv);var x=cv.getContext('2d'),drops=[];
    var size=function(){cv.width=c.offsetWidth;cv.height=c.offsetHeight};size();window.addEventListener('resize',size);
    for(var i=0;i<110;i++)drops.push({x:Math.random(),y:Math.random(),v:.012+Math.random()*.018,l:10+Math.random()*16});
    var rOn=true,rRun=true;onScreen(c,function(v){rOn=v;if(v&&!rRun){rRun=true;requestAnimationFrame(draw)}});
     function draw(){if(!rOn||document.hidden){rRun=false;return}x.clearRect(0,0,cv.width,cv.height);x.strokeStyle='rgba(200,220,255,.45)';x.lineWidth=1.2;x.beginPath();
      drops.forEach(function(d){var px=d.x*cv.width,py=d.y*cv.height;x.moveTo(px,py);x.lineTo(px-d.l*.25,py+d.l);d.y+=d.v;d.x-=d.v*.25;if(d.y>1.05){d.y=-.05;d.x=Math.random()*1.1}});x.stroke();requestAnimationFrame(draw)}draw();
     document.addEventListener('visibilitychange',function(){if(!document.hidden&&rOn&&!rRun){rRun=true;requestAnimationFrame(draw)}})}
  else if(/cloud|overcast|fog/.test(s)){c.setAttribute('data-fx','cloud');for(var i=0;i<4;i++){var d=document.createElement('div');d.className='wk-cloud';d.style.top=(5+i*14)+'%';d.style.animationDuration=(40+i*12)+'s';d.style.animationDelay=(-i*11)+'s';c.appendChild(d)}
    if(/partly|mostly sunny/.test(s))c.classList.add('wk-fx-sun')}
  else{c.setAttribute('data-fx','sun');c.classList.add('wk-fx-sun')}}

/* ---------- filters ---------- */
var fDay='all',fTag='all',lastDay='all';
function setOpen(b,open){b.classList.toggle('is-collapsed',!open);var h=b.querySelector('.wk-dayh');if(h)h.setAttribute('aria-expanded',open?'true':'false')}
root.addEventListener('click',function(e){var h=e.target.closest('.wk-dayblk .wk-dayh');if(!h)return;var b=h.parentNode,open=b.classList.contains('is-collapsed');setOpen(b,open);
  if(open)track('weekender_day_open',{day:b.getAttribute('data-day')})});
root.addEventListener('keydown',function(e){if((e.key==='Enter'||e.key===' ')&&e.target.classList&&e.target.classList.contains('wk-dayh')&&e.target.closest('.wk-dayblk')){e.preventDefault();e.target.click()}});
function applyFilter(){var shown=0;
  $$('.wk-ev').forEach(function(li){var ok=(fDay==='all'||li.getAttribute('data-day')===fDay||(fDay==='wknd'&&li.getAttribute('data-wknd')==='1'))&&(fTag==='all'||(' '+li.getAttribute('data-tags')+' ').indexOf(' '+fTag+' ')>=0);li.classList.toggle('is-hidden',!ok);if(ok)shown++});
  $$('.wk-dayblk').forEach(function(b){var any=b.querySelectorAll('.wk-ev:not(.is-hidden)').length;b.classList.toggle('is-hidden',!any);
    var c=b.querySelector('.wk-dcount');if(c)c.textContent=any+' event'+(any===1?'':'s')});
  if(fDay!==lastDay){lastDay=fDay;var vis=$$('.wk-dayblk').filter(function(b){return !b.classList.contains('is-hidden')});
    vis.forEach(function(b){setOpen(b,fDay!=='all')})}
  $$('.wk-aw').forEach(function(a){a.classList.toggle('is-hidden',fTag!=='all'&&(' '+a.getAttribute('data-tags')+' ').indexOf(' '+fTag+' ')<0)});
  var c=$('wk-shown');if(c)c.textContent='Showing '+shown+' event'+(shown===1?'':'s')+(fDay==='wknd'?' this weekend':fDay!=='all'?' '+((root.querySelector('.wk-tab.is-on')||{}).textContent||'').toLowerCase():' this week')+(fTag!=='all'?' tagged '+fTag:'');
  var nm=$('wk-nomatch');if(nm)nm.hidden=shown>0;
  reveal()}
function ink(){var on=root.querySelector('.wk-tab.is-on'),i=root.querySelector('.wk-tabink');if(!on||!i)return;i.style.width=on.offsetWidth+'px';i.style.transform='translateX('+(on.offsetLeft-5)+'px)'}

/* ---------- save / my weekend ---------- */
var saved=store.get('wkSaved_'+root.getAttribute('data-edition'),[]);
function syncSaved(){$$('[data-save]').forEach(function(b){var on=saved.indexOf(b.getAttribute('data-save'))>=0;b.setAttribute('aria-pressed',on);var t=b.querySelector('.wk-savet');if(t&&!/Spy/.test(t.textContent))t.textContent=on?'Saved':'Save';var s=b.querySelector('.wk-star');if(s)s.innerHTML=on?'&#9733;':'&#9734;'});
  var n=$('wk-fabn');if(n)n.textContent=saved.length;var f=$('wk-fab');if(f)f.classList.toggle('is-up',saved.length>0||window.scrollY>900);drawDrawer()}
function toggleSave(id){var i=saved.indexOf(id);if(i>=0)saved.splice(i,1);else{saved.push(id);toast('Added to My Weekend');track('weekender_save',{event_id:id})}
  store.set('wkSaved_'+root.getAttribute('data-edition'),saved);syncSaved();var f=$('wk-fab');if(f){f.classList.remove('is-bump');void f.offsetWidth;f.classList.add('is-bump')}}
function drawDrawer(){var l=$('wk-drlist');if(!l)return;var items=saved.map(function(id){return EV[id]}).filter(Boolean).sort(function(a,b){return a.start-b.start});
  if(!items.length){l.innerHTML='<p class="wk-drempty">Tap &#9734; Save on anything that looks good. Your plan shows up here, and it stays on this device.</p>';return}
  l.innerHTML=items.map(function(e,i){var clash=items.some(function(o,j){return j!==i&&o.start<e.end&&e.start<o.end});
    return '<div class="wk-dri'+(clash?' is-clash':'')+'"><span class="wk-drday" style="background:'+DAYC[e.day]+'">'+DAYN[e.day].slice(0,3).toUpperCase()+'</span><div><b>'+e.title+'</b><small>'+tm(e.start)+' &middot; '+e.venue+'</small>'+(clash?'<div class="wk-clash">Overlaps another pick</div>':'')+'</div><button type="button" class="wk-drrm" data-rm="'+e.id+'" aria-label="Remove">&times;</button></div>'}).join('')}
function openDrawer(on){var d=$('wk-drawer'),f=$('wk-fab');if(!d)return;d.classList.toggle('is-open',on);d.setAttribute('aria-hidden',!on);d.inert=!on;if(f)f.setAttribute('aria-expanded',on)}

/* ---------- calendar (.ics) ---------- */
function icsDate(d){return d.toISOString().replace(/[-:]/g,'').split('.')[0]+'Z'}
function ics(list){var L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Three Village Local//The Weekender//EN'];
  list.forEach(function(e){L.push('BEGIN:VEVENT','UID:'+e.id+'-'+root.getAttribute('data-edition')+'@threevillagelocal.com','DTSTAMP:'+icsDate(new Date()),'DTSTART:'+icsDate(e.start),'DTEND:'+icsDate(e.end),
    'SUMMARY:'+e.title,'LOCATION:'+e.venue+', '+e.addr,'DESCRIPTION:From The Weekender on Three Village Local. '+location.href.split('#')[0],'END:VEVENT')});L.push('END:VCALENDAR');
  var blob=new Blob([L.join('\r\n')],{type:'text/calendar'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=(list.length>1?'my-weekend':list[0].id)+'.ics';document.body.appendChild(a);a.click();setTimeout(function(){a.remove()},100);
  toast('Calendar file downloaded');track('weekender_calendar',{count:list.length})}

/* ---------- share ---------- */
function share(text){var url=location.href.split('#')[0];if(navigator.share){navigator.share({title:'The Weekender',text:text,url:url}).catch(function(){})}
  else if(navigator.clipboard){navigator.clipboard.writeText(text+' '+url).then(function(){toast('Link copied')})}track('weekender_share',{})}
function planText(){var items=saved.map(function(id){return EV[id]}).filter(Boolean).sort(function(a,b){return a.start-b.start});
  if(!items.length)return 'Here’s everything happening in Three Village this weekend:';
  return 'My Three Village plans: '+items.map(function(e){return ds(e.start)+' '+tm(e.start)+' '+e.title}).join(', ')+'. Plan yours:'}

/* ---------- VIP ads ---------- */
/* Shuffle so the same business or competitors (same "group") are at least GAP+1 slots apart, including when the loop wraps. */
function spread(arr,key,gap){var best=arr.slice();
  for(var tries=0;tries<200;tries++){var pool=arr.slice(),out=[];
    for(var i=pool.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=pool[i];pool[i]=pool[j];pool[j]=t}
    while(pool.length){var pick=-1;for(var k=0;k<pool.length;k++){var ok=true;for(var b=1;b<=gap&&b<=out.length;b++){if(key(out[out.length-b])===key(pool[k])){ok=false;break}}if(ok){pick=k;break}}
      if(pick<0)break;out.push(pool.splice(pick,1)[0])}
    if(out.length===arr.length){var wrapOk=true,n=out.length;for(var a=0;a<n&&wrapOk;a++)for(var d=1;d<=gap;d++){if(n>gap*2&&key(out[a])===key(out[(a+d)%n])){wrapOk=false;break}}if(wrapOk)return out;best=out}}
  return best}

function vip(){var rot=$('wk-adrot');if(!rot)return;var ads=$$('.wk-ad',rot);if(!ads.length)return;
  /* competitors never share a page (owner 10/2/2026: e.g. the two orthopedic practices): one business per group per page view,
     picked at random so each gets its share across visitors; a business with two designs keeps both */
  var pickG={};ads.forEach(function(a){var g=a.getAttribute('data-group'),v=a.getAttribute('data-vip');if(!g)return;(pickG[g]=pickG[g]||[]);if(pickG[g].indexOf(v)<0)pickG[g].push(v)});
  Object.keys(pickG).forEach(function(g){pickG[g]=pickG[g][Math.floor(Math.random()*pickG[g].length)]});
  ads=ads.filter(function(a){var g=a.getAttribute('data-group');if(!g||pickG[g]===a.getAttribute('data-vip'))return true;a.parentNode.removeChild(a);return false});
  ads=spread(ads,function(a){return a.getAttribute('data-group')||a.getAttribute('data-vip')},3);
  ads.forEach(function(a){rot.appendChild(a)});
  var idx=0,dur=6500,t0=0,paused=false,bar=$('wk-adbar'),dots=$('wk-addots'),seenV={};
  var slots=$$('.wk-adslot');var r2=$('wk-adrot2');if(r2&&innerWidth>1060)slots.unshift(r2);var clones=slots.map(function(s,n){var w=document.createElement('div');w.className='wk-adrot';s.appendChild(w);
    ads.forEach(function(a){var c=a.cloneNode(true);c.classList.remove('is-on');var lb=document.createElement('span');lb.className='wk-adlabel';lb.textContent='3VL VIP';c.appendChild(lb);w.appendChild(c)});return $$('.wk-ad',w)});
  /* lower rail pair: no banner downloads until the reader scrolls close to it (it starts just below the first screen) */
  $$('.wk-rslot').forEach(function(s){if(!('IntersectionObserver' in window))return;s.setAttribute('data-far','1');
    var io=new IntersectionObserver(function(en){if(!en[0].isIntersecting)return;io.disconnect();s.removeAttribute('data-far');
      var on=s.querySelector('.wk-ad.is-on');if(on){ld(on);ld(on.nextElementSibling&&on.nextElementSibling.classList.contains('wk-ad')?on.nextElementSibling:s.querySelector('.wk-ad'))}},{rootMargin:'100px 0px'});io.observe(s)});
  if(dots)dots.innerHTML=ads.map(function(a,i){return '<button type="button" aria-label="Show ad '+(i+1)+'"></button>'}).join('');
  function ld(a){if(!a)return;var im=a.querySelector('img[data-src]');if(!im)return;var u=im.getAttribute('data-src');im.removeAttribute('data-src');im.src=u;var pc=a.querySelector('.wk-adpic');if(pc)pc.style.setProperty('--bgimg','url('+u+')')}
  function show(n){idx=(n+ads.length)%ads.length;if(rot.offsetParent!==null){ld(ads[idx]);ld(ads[(idx+1)%ads.length])}ads.forEach(function(a,i){a.classList.toggle('is-on',i===idx);a.setAttribute('aria-hidden',i!==idx);a.inert=i!==idx});
    var usedG=[(ads[idx].getAttribute('data-group')||ads[idx].getAttribute('data-vip'))];
    clones.forEach(function(cs,k){var m=(idx+k*4+3)%cs.length,guard=0;
      while(guard<cs.length&&usedG.indexOf(cs[m].getAttribute('data-group')||cs[m].getAttribute('data-vip'))>=0){m=(m+1)%cs.length;guard++}
      usedG.push(cs[m].getAttribute('data-group')||cs[m].getAttribute('data-vip'));
      var vis=cs[m].parentNode.offsetParent!==null&&!cs[m].parentNode.parentNode.hasAttribute('data-far');if(vis){ld(cs[m]);ld(cs[(m+1)%cs.length])}
      cs.forEach(function(a,i){a.classList.toggle('is-on',i===m);a.setAttribute('aria-hidden',i!==m);a.inert=i!==m})});
    if(dots)$$('button',dots).forEach(function(b,i){b.classList.toggle('is-on',i===idx)});t0=performance.now();
    var name=ads[idx].getAttribute('data-vip');if(!seenV[name]&&rot.offsetParent){seenV[name]=1;track('vip_ad_view',{vip:name,placement:'weekender_rail'})}}
  var bp=0;function loop(ts){if(document.hidden){requestAnimationFrame(loop);return}if(!paused){var p=(ts-t0)/dur;bp=Math.min(1,p);if(bar)bar.style.transform='scaleX('+bp+')';if(p>=1)show(idx+1)}else{t0=ts-bp*dur}requestAnimationFrame(loop)}
  rot.addEventListener('mouseenter',function(){paused=true});rot.addEventListener('mouseleave',function(){paused=false});
  var gl=document.createElement('div');gl.className='wk-adglare';rot.appendChild(gl);
  rot.insertAdjacentHTML('beforeend','<button type="button" class="wk-adnav wk-adprev" aria-label="Previous ad">&#8249;</button><button type="button" class="wk-adnav wk-adnext" aria-label="Next ad">&#8250;</button>');
  rot.querySelector('.wk-adprev').addEventListener('click',function(e){e.preventDefault();show(idx-1)});
  rot.querySelector('.wk-adnext').addEventListener('click',function(e){e.preventDefault();show(idx+1)});
  if(matchMedia('(hover:hover) and (pointer:fine)').matches&&!matchMedia('(prefers-reduced-motion:reduce)').matches){
    rot.addEventListener('mouseenter',function(){rot.classList.add('lift')});
    rot.addEventListener('mousemove',function(e){var r=rot.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;
      rot.style.setProperty('--ry',((x-.5)*10).toFixed(2)+'deg');rot.style.setProperty('--rx',((.5-y)*8).toFixed(2)+'deg');rot.style.setProperty('--gx',(x*100)+'%');rot.style.setProperty('--gy',(y*100)+'%')});
    rot.addEventListener('mouseleave',function(){rot.classList.remove('lift');rot.style.setProperty('--rx','0deg');rot.style.setProperty('--ry','0deg')})}
  if(dots)dots.addEventListener('click',function(e){var b=e.target.closest('button');if(b)show($$('button',dots).indexOf(b))});
  root.addEventListener('click',function(e){var a=e.target.closest('[data-vip]');if(a&&a.tagName==='A')track('vip_ad_click',{vip:a.getAttribute('data-vip'),link:a.className})});
  requestAnimationFrame(function(){show(0);requestAnimationFrame(loop)})}

/* ---------- map ---------- */
function map(){var box=$('wk-lmap');if(!box)return;var started=false;
  function start(){if(started)return;started=true;var go=function(){
    var m=L.map(box,{scrollWheelZoom:false,zoomControl:true,attributionControl:true}).setView([40.93,-73.105],13);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',{maxZoom:18,attribution:'Tiles &copy; Esri'}).addTo(m);
    var groups={fri:L.layerGroup().addTo(m),sat:L.layerGroup().addTo(m),sun:L.layerGroup().addTo(m)},pts=[],byLoc={};
    LIST.forEach(function(e,i){var key=e.lat.toFixed(4)+','+e.lon.toFixed(4);byLoc[key]=(byLoc[key]||0)+1;var off=(byLoc[key]-1)*.0006;
      var ic=L.divIcon({className:'',html:'<div class="wk-pin" style="--pc:'+DAYC[e.day]+';animation-delay:'+(i*70)+'ms">'+(TAGI[e.tags.filter(function(t){return t!=='free'&&t!=='outdoor'})[0]||e.tags[0]]||'&#9733;')+'</div>',iconSize:[34,34],iconAnchor:[17,17],popupAnchor:[0,-16]});
      var mk=L.marker([e.lat+off,e.lon+off],{icon:ic}).bindPopup('<b>'+e.title+'</b><br>'+DAYN[e.day]+', '+tm(e.start)+'<br>'+e.venue+'<br><a href="#" data-jump="'+e.id+'">See details &rarr;</a>');
      groups[e.day].addLayer(mk);pts.push([e.lat,e.lon])});
    m.fitBounds(pts,{padding:[40,40]});
    box.parentNode.addEventListener('click',function(){box.parentNode.classList.add('is-live');m.scrollWheelZoom.enable()},{once:true});
    $$('.wk-mapleg button').forEach(function(b){b.addEventListener('click',function(ev){ev.stopPropagation();var d=b.getAttribute('data-day'),g=groups[d];if(m.hasLayer(g)){m.removeLayer(g);b.classList.add('is-off')}else{m.addLayer(g);b.classList.remove('is-off')}})})};
    if(window.L)return go();var l=document.createElement('link');l.rel='stylesheet';l.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';document.head.appendChild(l);
    var s=document.createElement('script');s.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';s.onload=go;document.head.appendChild(s)}
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(en){if(en[0].isIntersecting){start();io.disconnect()}},{rootMargin:'400px'});io.observe(box)}else start()}

/* ---------- spy day: cipher + trolley ---------- */
function cipher(){var b=root.querySelector('#wk-cipher b');if(!b)return;var plain=b.getAttribute('data-plain'),A='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',done=false;
  function run(){if(done)return;done=true;var f=0,total=plain.length*3+12;(function tick(){f++;var out='';for(var i=0;i<plain.length;i++){var c=plain[i];out+=c===' '?' ':(f>i*3+12?c:A[Math.floor(Math.random()*A.length)])}b.textContent=out;if(f<total)setTimeout(tick,38)})()}
  b.textContent=plain.replace(/[A-Z]/g,'#');
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(en){if(en[0].isIntersecting){run();io.disconnect()}},{threshold:.6});io.observe(b)}else run()}
function onScreen(el,cb){if(!el||!('IntersectionObserver' in window)){cb(true);return}new IntersectionObserver(function(en){cb(en[0].isIntersecting)},{rootMargin:'120px 0px'}).observe(el)}
function trolley(){var path=$('wk-rpath'),bus=$('wk-bus'),svg=path&&path.ownerSVGElement,stops=$$('.wk-stops li');if(!path||!bus||!svg||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  var len=path.getTotalLength(),t0=null,D=16000,G=null,on=false,run=false,vb=svg.viewBox.baseVal;
  function geo(){var bb=svg.getBoundingClientRect(),box=bus.parentNode.getBoundingClientRect();G={dx:bb.left-box.left,dy:bb.top-box.top,w:bb.width,h:bb.height}}
  window.addEventListener('resize',function(){G=null});onScreen(svg,function(v){on=v;if(v&&!run){run=true;requestAnimationFrame(f)}});
  function f(ts){if(!on||document.hidden){run=false;return}if(!t0)t0=ts;if(!G)geo();var p=((ts-t0)%D)/D,pt=path.getPointAtLength(p*len);
    var x=G.dx+pt.x*G.w/vb.width-14,y=G.dy+pt.y*G.h/vb.height-22;bus.style.transform='translate('+x+'px,'+y+'px)';
    var n=Math.min(stops.length-1,Math.floor(p*stops.length));stops.forEach(function(s,i){s.classList.toggle('is-on',i===n)});requestAnimationFrame(f)}
  document.addEventListener('visibilitychange',function(){if(!document.hidden&&on&&!run){run=true;requestAnimationFrame(f)}})}

/* ---------- video facade ---------- */
function video(){$$('.wk-vid').forEach(function(v){v.addEventListener('click',function(){if(v.querySelector('iframe'))return;var id=v.getAttribute('data-yt');
  v.insertAdjacentHTML('beforeend','<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0" title="Trailer" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>');track('weekender_video',{id:id})})})}

/* ---------- reveal + scrollspy ---------- */
var io2=null;
function reveal(){if(!('IntersectionObserver' in window)){$$('.wk-rv').forEach(function(e){e.classList.add('is-in')});return}
  if(!io2)io2=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('is-in');io2.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});
  $$('.wk-rv:not(.is-in)').forEach(function(e){io2.observe(e)})}
function spy(){var links=$$('.wk-navin a'),secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))});
  function on(){var y=window.scrollY+140,cur=0;secs.forEach(function(s,i){if(s&&s.getBoundingClientRect().top+window.scrollY<=y)cur=i});links.forEach(function(a,i){a.classList.toggle('is-on',i===cur)});
    var tt=$('wk-totop');if(tt)tt.classList.toggle('is-up',window.scrollY>1200);var f=$('wk-fab');if(f)f.classList.toggle('is-up',saved.length>0||window.scrollY>900)}
  window.addEventListener('scroll',on,{passive:true});on()}


/* ---------- compact mode (phones): cap long lists, toggles ---------- */
function compact(){
  var small=matchMedia('(max-width:760px)').matches;
  $$('.wk-more[data-more]').forEach(function(btn){btn.addEventListener('click',function(){var t=$(btn.getAttribute('data-more'));if(!t)return;var open=t.classList.toggle('is-open');btn.innerHTML=open?'Close the field guide &#9652;':'Open the full field guide &#9662;'})});
  if(!small)return;
  $$('.wk-dayblk').forEach(function(blk){var items=$$('.wk-ev',blk);if(items.length<=4)return;
    items.slice(4).forEach(function(li){li.classList.add('wk-capped')});
    var b=document.createElement('button');b.type='button';b.className='wk-more';b.textContent='Show all '+items.length+' events';
    b.addEventListener('click',function(){items.forEach(function(li){li.classList.remove('wk-capped')});b.remove()});blk.appendChild(b)});
  var fl=$('wk-flist');if(fl){fl.classList.add('wk-fcap');var fb=document.createElement('button');fb.type='button';fb.className='wk-more wk-more-dark';fb.textContent='More from around town';
    fb.addEventListener('click',function(){fl.classList.remove('wk-fcap');fb.remove()});fl.parentNode.insertBefore(fb,fl.nextSibling)}
}

/* ---------- boot ---------- */
function hdr(){var n=document.querySelector('.navbar-fixed-top');var h=n?n.offsetHeight:0;root.style.setProperty('--hdr',h+'px')}
function go(){hdr();window.addEventListener('scroll',hdr,{passive:true});
  var tn=now(),b0=new Date(tn.getFullYear(),tn.getMonth(),tn.getDate(),12);DAYS.fri=b0;DAYS.sat=new Date(b0.getTime()+864e5);DAYS.sun=new Date(b0.getTime()+1728e5);
  ['fri','sat','sun'].forEach(function(k,i){var w=root.querySelector('.wk-wd[data-day='+k+'] .wk-wdn');if(w)w.textContent=i===0?'Today':i===1?'Tmrw':['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][DAYS[k].getDay()]});
  indexEvents();
  $$('.wk-ev').forEach(function(li){li.id='wk-ev-'+li.getAttribute('data-id')});$$('.wk-pick').forEach(function(p){EV[p.getAttribute('data-id')]&&!EV[p.getAttribute('data-id')].el.id&&(EV[p.getAttribute('data-id')].el.id='wk-pk-'+p.getAttribute('data-id'))});
  LIST.forEach(function(e){var li=root.querySelector('#wk-ev-'+e.id);if(li)e.el=li});
  countdown();heroLive();setInterval(heroLive,1000);heroWx();setInterval(heroWx,15*60000);
  var st=$$('.wk-num');if('IntersectionObserver' in window){var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){countUp(x.target);io.unobserve(x.target)}})});st.forEach(function(e){io.observe(e)})}else st.forEach(countUp);
  statuses();nowPanel();setInterval(function(){statuses();nowPanel()},30000);
  loadFeed();loadAlerts();setInterval(loadFeed,60000);setInterval(loadAlerts,300000);setInterval(function(){$$('[data-ago]').forEach(function(s){s.textContent=ago(s.getAttribute('data-ago'))})},30000);
  loadWx();paintWx();setInterval(loadWx,20*60000);
  (function(){var wx=$('wk-wx');if(!wx)return;var go2=function(){wxScenes();setInterval(wxScenes,30000)};if('IntersectionObserver' in window){var io3=new IntersectionObserver(function(en){if(en[0].isIntersecting){go2();io3.disconnect()}},{rootMargin:'300px'});io3.observe(wx)}else go2()})();
  $$('.wk-tab').forEach(function(b){b.addEventListener('click',function(){$$('.wk-tab').forEach(function(x){x.classList.toggle('is-on',x===b)});fDay=b.getAttribute('data-day');ink();applyFilter();track('weekender_filter',{day:fDay})})});
  $$('.wk-chip').forEach(function(b){b.addEventListener('click',function(){$$('.wk-chip').forEach(function(x){x.classList.toggle('is-on',x===b)});fTag=b.getAttribute('data-tag');applyFilter();track('weekender_filter',{tag:fTag})})});
  root.addEventListener('click',function(e){var d=e.target.closest('.wk-evdesc');if(d)d.classList.toggle('is-open')});
  requestAnimationFrame(ink);window.addEventListener('resize',ink);applyFilter();
  root.addEventListener('click',function(e){var s=e.target.closest('[data-save]');if(s){toggleSave(s.getAttribute('data-save'));return}
    var c=e.target.closest('[data-cal]');if(c){var ev=EV[c.getAttribute('data-cal')];if(ev)ics([ev]);return}
    var r=e.target.closest('[data-rm]');if(r){toggleSave(r.getAttribute('data-rm'));return}
    var j=e.target.closest('[data-jump]');if(j){e.preventDefault();openDrawer(false);var el=$('wk-ev-'+j.getAttribute('data-jump'));if(el){el.scrollIntoView({behavior:'smooth',block:'center'});var cc=el.querySelector('.wk-evc');cc.animate&&cc.animate([{boxShadow:'0 0 0 4px #ffc145'},{boxShadow:'0 0 0 0 transparent'}],{duration:1600})}}});
  document.addEventListener('click',function(e){var j=e.target.closest&&e.target.closest('.leaflet-popup [data-jump]');if(j){e.preventDefault();var el=$('wk-ev-'+j.getAttribute('data-jump'));if(el)el.scrollIntoView({behavior:'smooth',block:'center'})}});
  var fab=$('wk-fab');if(fab)fab.addEventListener('click',function(){openDrawer(true)});
  var dx=$('wk-drx');if(dx)dx.addEventListener('click',function(){openDrawer(false)});
  var dr=$('wk-drawer');if(dr)dr.addEventListener('click',function(e){if(e.target===dr)openDrawer(false)});
  var ca=$('wk-calall');if(ca)ca.addEventListener('click',function(){var l=saved.map(function(id){return EV[id]}).filter(Boolean);if(l.length)ics(l);else toast('Save a few events first')});
  ['wk-share'].forEach(function(id){var b=$(id);if(b)b.addEventListener('click',function(){share('Everything happening in Three Village this weekend:')})});
  ['wk-share2','wk-share3'].forEach(function(id){var b=$(id);if(b)b.addEventListener('click',function(){share(planText())})});
  syncSaved();vip();cipher();compact();trolley();video();reveal();spy();swipeHints();
}
function swipeHints(){$$('.wk-swipe,.wk-wx').forEach(function(row){if(row.nextElementSibling&&row.nextElementSibling.classList.contains('wk-swh'))return;
  var kids=[].filter.call(row.children,function(c){return c.offsetWidth>0});if(kids.length<2)return;
  var h=document.createElement('div');h.className='wk-swh';h.setAttribute('aria-hidden','true');
  h.innerHTML='<span class="wk-swd">'+kids.map(function(_,i){return '<i'+(i?'':' class="on"')+'></i>'}).join('')+'</span><span class="wk-swt">Swipe <b>&#8594;</b></span>';
  row.parentNode.insertBefore(h,row.nextSibling);var dots=$$('i',h),t=h.querySelector('.wk-swt');
  function upd(){var over=row.scrollWidth>row.clientWidth+8;h.hidden=!over;if(!over)return;var w=kids[0].offsetWidth+12,i=Math.round(row.scrollLeft/w);
    if(row.scrollLeft+row.clientWidth>=row.scrollWidth-4)i=kids.length-1;dots.forEach(function(d,j){d.classList.toggle('on',j===i)});t.classList.toggle('is-end',i===kids.length-1)}
  row.addEventListener('scroll',function(){requestAnimationFrame(upd)},{passive:true});window.addEventListener('resize',upd);upd()})}
function pickArrows(){var sec=$('wk-picks'),row=sec&&sec.querySelector('.wk-picks');if(!row||sec.querySelector('.wk-parr'))return;
  var wrap=document.createElement('div');wrap.className='wk-pwrap';row.parentNode.insertBefore(wrap,row);wrap.appendChild(row);
  var mk=function(cls,lab,ch){var b=document.createElement('button');b.type='button';b.className='wk-parr '+cls;b.setAttribute('aria-label',lab);b.innerHTML='<span>'+ch+'</span>';wrap.appendChild(b);return b};
  var L=mk('wk-parr-l','Previous picks','&#8249;'),R=mk('wk-parr-r','More picks','&#8250;');
  var step=function(d){var c=row.querySelector('.wk-pick');row.scrollBy({left:d*((c?c.offsetWidth:300)+18),behavior:'smooth'})};
  L.onclick=function(){step(-1)};R.onclick=function(){step(1)};
  function upd(){var over=row.scrollWidth>row.clientWidth+8,im=row.querySelector('.wk-pimg');
    if(im){var y=im.offsetTop+im.offsetHeight/2;L.style.top=R.style.top=y+'px'}
    L.classList.toggle('is-off',!over||row.scrollLeft<8);R.classList.toggle('is-off',!over||row.scrollLeft+row.clientWidth>=row.scrollWidth-8)}
  row.addEventListener('scroll',function(){requestAnimationFrame(upd)},{passive:true});window.addEventListener('resize',upd);setTimeout(upd,300);upd()}
function railStick(){var r=root.querySelector('.wk-railin');if(!r)return;
  function f(){if(innerWidth<1061){r.style.top='';return}var hdr=parseFloat(getComputedStyle(root).getPropertyValue('--hdr'))||0,want=hdr+80,h=r.offsetHeight;
    r.style.top=Math.min(want,innerHeight-h-16)+'px'}   /* tall rail: stick by its bottom edge so both ads stay fully visible */
  f();addEventListener('resize',f);setTimeout(f,1500);setTimeout(f,5000);if(window.ResizeObserver)new ResizeObserver(f).observe(r)}
/* ---------- 10/1: the whole card is a link, and cut-off text gets a "More" button ---------- */
function cardLinks(){root.addEventListener('click',function(e){if(e.target.closest('a,button,input,label'))return;var c=e.target.closest('.wk-pick,.wk-sp');if(!c)return;
  if(window.getSelection&&String(window.getSelection()).length)return;
  var a=c.querySelector('.wk-ptitle a,.wk-spbiz a')||c.querySelector('.wk-spf a.wk-biz'),u=c.getAttribute('data-href')||(a&&a.href);if(!u)return;
  var ours=u.charAt(0)==='/'||u.indexOf('threevillagelocal.com')>-1;
  track('card_click',{card:c.classList.contains('wk-sp')?'eat':'todo',link:u});
  if(ours)location.href=u;else window.open(u,'_blank','noopener')})}
function moreBtns(){$$('.wk-pdesc,.wk-spd').forEach(function(p){if(p.classList.contains('is-open'))return;var b=p.nextElementSibling;b=b&&b.classList.contains('wk-mo')?b:null;
  var cut=p.scrollHeight>p.clientHeight+3;
  if(cut&&!b){b=document.createElement('button');b.type='button';b.className='wk-mo';b.textContent='More';b.setAttribute('aria-expanded','false');
    b.addEventListener('click',function(){var o=p.classList.toggle('is-open');b.textContent=o?'Less':'More';b.setAttribute('aria-expanded',o?'true':'false')});p.parentNode.insertBefore(b,p.nextSibling)}
  else if(!cut&&b)b.remove()})}
function boot(){railStick();cardLinks();setTimeout(moreBtns,1500);setTimeout(moreBtns,4700);addEventListener('resize',function(){clearTimeout(moreBtns.t);moreBtns.t=setTimeout(moreBtns,200)});
  var done=false,fin=function(){if(done)return;done=true;go();setTimeout(moreBtns,80)};
  setTimeout(fin,4000);setTimeout(pickArrows,4200);
  fetch(LIVEURL+'?v='+Math.floor(Date.now()/300000),{cache:'no-store'}).then(function(r){return r.json()}).then(function(d){if(!done){try{renderLive(d)}catch(e){}fin()}}).catch(fin)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
