/* 3VL Guide Kit (Oct 2026): shared interactive layer for premium guide articles.
   Finder (who/budget/distance -> cards reorder), live map, countdowns, "this weekend" strip, foliage-style meter,
   save-to-my-list + share, reading progress, sticky jump nav with scrollspy, scroll reveals.
   Markup contract: root <div class="gk" id="gk-top" data-key="unique-list-key" data-title="List title">.
   Cards: <article class="gk-card" data-id data-who="tod kid teen adult" data-cost="free|$|$$" data-mi="7" data-lat data-lng
          data-start="2026-10-10" data-end="2026-10-11" data-name>. Everything works (static) without JS. */
(function(){
'use strict';
var root=document.getElementById('gk-top');if(!root)return;
root.classList.add('js');
var KEY='gk-'+(root.getAttribute('data-key')||'list');
function $(s,r){return (r||document).querySelector(s)}function $$(s,r){return [].slice.call((r||document).querySelectorAll(s))}
function track(a,o){try{if(window.gtag)window.gtag('event','guide_click',Object.assign({action:a,guide:KEY},o||{}))}catch(e){}}
function day(s){var p=String(s).split('-');return new Date(+p[0],+p[1]-1,+p[2])}
var today=new Date();today.setHours(0,0,0,0);

/* falling leaves in the hero (built here so the post HTML stays clean) */
var lv=$('.gk-leaves',root);
if(lv&&!lv.children.length&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
  for(var li=0;li<16;li++){var e=document.createElement('i');e.style.left=(Math.random()*100)+'%';e.style.animationDuration=(9+Math.random()*9)+'s';e.style.animationDelay=(-Math.random()*14)+'s';lv.appendChild(e)}}

/* lazy photos */
/* phones get the -480 copy of our -640 card photos */
var small=matchMedia('(max-width:560px)').matches&&(window.devicePixelRatio||1)<2.5;
var bgs=$$('[data-bg]',root),setbg=function(e){if(e.hasAttribute('data-bg')){var u=e.getAttribute('data-bg');if(small&&/-640\.webp$/.test(u))u=u.replace(/-640\.webp$/,'-480.webp');e.style.backgroundImage="url('"+u+"')";e.removeAttribute('data-bg')}};
if('IntersectionObserver' in window){var bo=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){setbg(x.target);bo.unobserve(x.target)}})},{rootMargin:'900px 0px'});bgs.forEach(function(e){bo.observe(e)})}
else bgs.forEach(setbg);

/* past events fade + "happening now / this weekend" badges */
var cards=$$('.gk-card',root);
var fri=new Date(today);fri.setDate(today.getDate()+((5-today.getDay()+7)%7));if(today.getDay()===6||today.getDay()===0){fri.setDate(today.getDate()-(today.getDay()===6?1:2))}
var sun=new Date(fri);sun.setDate(fri.getDate()+2);
cards.forEach(function(c){var s=c.getAttribute('data-start'),e=c.getAttribute('data-end')||s;if(!s)return;
  var S=day(s),E=day(e);
  if(E<today){c.classList.add('is-past');var b=document.createElement('span');b.className='gk-badge gk-b-past';b.textContent='Over for 2026';c.appendChild(b);return}
  var lab='';if(S<=today&&E>=today)lab='Happening now';else if(S<=sun&&E>=fri)lab='This weekend';
  if(lab){var b2=document.createElement('span');b2.className='gk-badge'+(lab==='Happening now'?' gk-b-live':'');b2.textContent=lab;c.appendChild(b2);c.setAttribute('data-wk','1')}});

/* this-weekend strip */
var wk=$('#gk-weekend');
if(wk){var hits=cards.filter(function(c){return c.getAttribute('data-wk')});
  if(hits.length){wk.innerHTML='<p class="gk-wk-h">On this weekend</p><div class="gk-wk-row">'+hits.map(function(c){
      return '<a class="gk-wk-chip" href="#'+c.id+'">'+(c.getAttribute('data-name')||'')+'</a>'}).join('')+'</div>'}
  else wk.style.display='none'}

/* countdowns */
$$('.gk-count',root).forEach(function(cd){var T=new Date(cd.getAttribute('data-target')).getTime(),lab=cd.getAttribute('data-label')||'';
  var tick=function(){var d=T-Date.now();
    if(d<=0){cd.classList.add('is-live');cd.innerHTML='<span class="gk-cl">&#9679; '+(cd.getAttribute('data-live')||'Happening now')+'</span>';return}
    var u={d:Math.floor(d/864e5),h:Math.floor(d/36e5)%24,m:Math.floor(d/6e4)%60,s:Math.floor(d/1e3)%60};
    cd.innerHTML='<span class="gk-cl">'+lab+'</span>'+['d','h','m','s'].map(function(k){return '<b>'+(u[k]<10&&k!=='d'?'0':'')+u[k]+'</b><i>'+{d:'days',h:'hrs',m:'min',s:'sec'}[k]+'</i>'}).join('');
    setTimeout(tick,1000)};tick()});

/* meter: ring fills by date between data-from and data-peak (e.g. foliage) */
$$('.gk-meter',root).forEach(function(m){var a=day(m.getAttribute('data-from')),p=day(m.getAttribute('data-peak')),z=day(m.getAttribute('data-to')||m.getAttribute('data-peak'));
  var v=today<=a?0:today>=p?(today>z?100:100):Math.round((today-a)/(p-a)*100);
  var ring=$('.gk-ring-fg',m),num=$('.gk-mnum',m),txt=$('.gk-mtxt',m),C=2*Math.PI*52;
  if(ring){ring.style.strokeDasharray=C;ring.style.strokeDashoffset=C}
  var go=function(){if(ring)ring.style.strokeDashoffset=C*(1-v/100);var t0=null;
    var step=function(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/1400);if(num)num.textContent=Math.round(v*k)+'%';if(k<1)requestAnimationFrame(step)};requestAnimationFrame(step)};
  if(txt){var msgs=JSON.parse(m.getAttribute('data-msgs')||'[]');for(var i=msgs.length-1;i>=0;i--){if(v>=msgs[i][0]){txt.textContent=msgs[i][1];break}}}
  if('IntersectionObserver' in window){var mo=new IntersectionObserver(function(en){if(en[0].isIntersecting){go();mo.disconnect()}},{threshold:.4});mo.observe(m)}else go()});

/* finder */
var fd=$('#gk-finder'),grid=$$('.gk-grid',root);
if(fd){var sel={who:null,cost:null,mi:null};
  var run=function(){var any=sel.who||sel.cost||sel.mi;
    cards.forEach(function(c){var s=0;
      if(sel.who&&(' '+(c.getAttribute('data-who')||'')+' ').indexOf(' '+sel.who+' ')>=0)s+=3;
      if(sel.cost){var cc=c.getAttribute('data-cost')||'$';if(sel.cost==='free'?cc==='free':sel.cost==='$'?(cc==='free'||cc==='$'):true)s+=2}
      if(sel.mi){var mi=+(c.getAttribute('data-mi')||99);if(mi<=+sel.mi)s+=2}
      if(c.classList.contains('is-past'))s-=10;
      c.style.order=any?String(100-s):'';c.classList.toggle('is-match',!!any&&s>=(sel.who?3:2)+(sel.cost?2:0)+(sel.mi?2:0)-0&&s>0);
      c.classList.toggle('is-dim',!!any&&s<=0)});
    var n=cards.filter(function(c){return c.classList.contains('is-match')}).length,out=$('#gk-fout');
    if(out)out.textContent=any?(n?n+' perfect match'+(n>1?'es':'')+' highlighted below':'No exact match, closest picks are first'):'';
    var first=cards.filter(function(c){return c.classList.contains('is-match')})[0];return first};
  $$('[data-f]',fd).forEach(function(b){b.addEventListener('click',function(){var g=b.getAttribute('data-f'),v=b.getAttribute('data-v');
    sel[g]=sel[g]===v?null:v;$$('[data-f="'+g+'"]',fd).forEach(function(x){x.classList.toggle('is-on',sel[g]===x.getAttribute('data-v'))});run();track('finder',{f:g,v:v})})});
  var go=$('#gk-fgo');if(go)go.addEventListener('click',function(){var f=run();var t=f||grid[0];if(t)t.scrollIntoView({behavior:'smooth',block:'center'})})}

/* my list (saved on this device) + share */
var saved={};try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
var bar=$('#gk-mylist');
var paint=function(){var ids=Object.keys(saved).filter(function(k){return saved[k]});
  cards.forEach(function(c){var h=$('.gk-heart',c);if(h){var on=!!saved[c.getAttribute('data-id')];h.classList.toggle('is-on',on);h.setAttribute('aria-pressed',on)}});
  if(bar){bar.classList.toggle('is-show',ids.length>0);var n=$('.gk-mln',bar);if(n)n.textContent=ids.length}};
cards.forEach(function(c){var h=$('.gk-heart',c);if(!h)return;h.addEventListener('click',function(ev){ev.preventDefault();var id=c.getAttribute('data-id');saved[id]=!saved[id];
  try{localStorage.setItem(KEY,JSON.stringify(saved))}catch(e){}h.classList.add('pop');setTimeout(function(){h.classList.remove('pop')},400);paint();track('save',{id:id})})});
var toast=function(t){var x=$('#gk-toast');if(!x){x=document.createElement('div');x.id='gk-toast';root.appendChild(x)}x.textContent=t;x.classList.add('is-on');setTimeout(function(){x.classList.remove('is-on')},2200)};
var share=function(list){var url=location.href.split('#')[0],title=root.getAttribute('data-title')||document.title;
  var txt=list&&list.length?title+':\n'+list.map(function(s){return '• '+s}).join('\n'):title;
  if(navigator.share){navigator.share({title:title,text:txt,url:url}).catch(function(){})}
  else{try{navigator.clipboard.writeText(txt+'\n'+url);toast('Copied! Paste it in a text to your crew.')}catch(e){toast(url)}}};
if(bar){var sb=$('.gk-mlshare',bar);if(sb)sb.addEventListener('click',function(){share(cards.filter(function(c){return saved[c.getAttribute('data-id')]}).map(function(c){return c.getAttribute('data-name')}));track('share_list')});
  var vb=$('.gk-mlview',bar);if(vb)vb.addEventListener('click',function(){var f=cards.filter(function(c){return saved[c.getAttribute('data-id')]})[0];if(f)f.scrollIntoView({behavior:'smooth',block:'center'})})}
$$('.gk-share',root).forEach(function(b){b.addEventListener('click',function(){share();track('share_page')})});
paint();

/* map (Leaflet loaded only when the map nears the screen) */
var mp=$('#gk-map');
if(mp&&'IntersectionObserver' in window){var loaded=false;
  var load=function(){if(loaded)return;loaded=true;
    var css=document.createElement('link');css.rel='stylesheet';css.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css';document.head.appendChild(css);
    var s=document.createElement('script');s.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js';s.onload=function(){
      var L=window.L,m=L.map(mp,{scrollWheelZoom:false,zoomControl:true,attributionControl:true});
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(m);
      var pts=[],near=[];cards.forEach(function(c,i){var la=+c.getAttribute('data-lat'),lo=+c.getAttribute('data-lng');if(!la||!lo)return;pts.push([la,lo]);if(+(c.getAttribute('data-mi')||0)<=15)near.push([la,lo]);
        var ic=L.divIcon({className:'gk-pin'+(c.classList.contains('is-past')?' is-past':''),html:'<span style="animation-delay:'+(i*60)+'ms"><b>'+(c.getAttribute('data-pin')||'&#9679;')+'</b></span>',iconSize:[34,34],iconAnchor:[17,30]});
        L.marker([la,lo],{icon:ic}).addTo(m).bindPopup('<b>'+(c.getAttribute('data-name')||'')+'</b><br><a href="#'+c.id+'">See details &rarr;</a>')});
      var fb=near.length>2?near:pts;if(fb.length)m.fitBounds(fb,{padding:[30,30],maxZoom:13});else m.setView([40.93,-73.12],11);
      mp.classList.add('is-ready')};document.head.appendChild(s)};
  var mo2=new IntersectionObserver(function(en){if(en[0].isIntersecting){load();mo2.disconnect()}},{rootMargin:'600px 0px'});mo2.observe(mp)}
/* pin popups link to cards: highlight the card on arrival */
root.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#gk-"]');if(!a)return;var t=document.getElementById(a.getAttribute('href').slice(1));
  if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'center'});t.classList.add('is-flash');setTimeout(function(){t.classList.remove('is-flash')},1800)}});

/* reading progress + jump nav scrollspy + reveal */
var pb=document.createElement('div');pb.className='gk-prog';pb.innerHTML='<span></span>';document.body.appendChild(pb);
var nav=$('#gk-nav'),links=nav?$$('a',nav):[],secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))});
var onScroll=function(){var r=root.getBoundingClientRect(),h=r.height-innerHeight,p=Math.max(0,Math.min(1,-r.top/(h>0?h:1)));pb.firstChild.style.width=(p*100)+'%';
  pb.classList.toggle('is-on',r.top<0&&r.bottom>innerHeight*.5);
  var cur=-1;secs.forEach(function(s,i){if(s&&s.getBoundingClientRect().top<innerHeight*.35)cur=i});
  links.forEach(function(a,i){a.classList.toggle('is-on',i===cur)});
  if(cur>=0&&nav&&links[cur]){var a=links[cur];if(a.offsetLeft<nav.scrollLeft||a.offsetLeft+a.offsetWidth>nav.scrollLeft+nav.clientWidth)nav.scrollLeft=a.offsetLeft-20}};
addEventListener('scroll',onScroll,{passive:true});onScroll();
var rv=$$('.gk-rv',root);
if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
  var ro=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('is-in');ro.unobserve(x.target)}})},{threshold:.12,rootMargin:'0px 0px -8% 0px'});
  rv.forEach(function(e){e.classList.add('gk-pre');ro.observe(e)})}
/* owner 10/6/2026: cards slide in one after another; whole card opens its own page (data-go = url, or "date|url;date|url" for
   multi-date events -> the next date still ahead); heart pops */
$$('.gk-grid',root).forEach(function(g){$$('.gk-card.gk-pre',g).forEach(function(c,i){c.style.transitionDelay=(i%3)*110+'ms';
  c.addEventListener('transitionend',function f(){c.style.transitionDelay='';c.removeEventListener('transitionend',f)})})});
var today=new Date();today.setHours(0,0,0,0);
$$('.gk-card[data-go]',root).forEach(function(c){var g=c.getAttribute('data-go'),u=g;
  if(g.indexOf('|')>-1){var ps=g.split(';').map(function(x){return x.split('|')});u=ps[ps.length-1][1];
    for(var j=0;j<ps.length;j++){if(new Date(ps[j][0]+'T23:59:00')>=today){u=ps[j][1];break}}}
  var ext=/^https?:/.test(u)&&u.indexOf('threevillagelocal.com')<0;
  c.classList.add('gk-link');c.setAttribute('tabindex','0');c.setAttribute('role','link');
  var a=c.querySelector('.gk-go');if(a)a.setAttribute('href',u);
  function go(e){if(e.target.closest('a,button,input,label,select'))return;
    try{if(window.gtag)window.gtag('event','guide_card_click',{card:c.id})}catch(_){}
    if(ext)window.open(u,'_blank','noopener');else location.href=u}
  c.addEventListener('click',go);c.addEventListener('keydown',function(e){if(e.key==='Enter')go(e)})});
root.addEventListener('click',function(e){var h=e.target.closest&&e.target.closest('.gk-heart');if(h){h.classList.remove('gk-pop');void h.offsetWidth;h.classList.add('gk-pop')}});
/* "next up" teasers */
$$('.gk-next',root).forEach(function(n){n.addEventListener('click',function(){var t=document.getElementById(n.getAttribute('data-to'));if(t){t.scrollIntoView({behavior:'smooth'});track('next',{to:n.getAttribute('data-to')})}})});
})();
