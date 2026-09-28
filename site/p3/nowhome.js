/* 3VL /now as homepage (9/28): compact carry-overs from the old homepage.
   1) Featured local businesses (VIP row) right after "Top Things to Do"
   2) Browse by category chips + 3) Latest local stories, near the bottom (before the business CTA).
   Data: search/index.json (nightly member index) + site/p3/vip_meta.json (ratings) + /blog. Runs on /now (or any page with ?nowhome=1). */
(function(){
'use strict';
var p=location.pathname.replace(/\/+$/,'')||'/';
var LIVE=false;  /* PREVIEW MODE: only shows with ?nowhome=1 until the owner approves; then set LIVE=true */
if(!/[?&]nowhome=1/.test(location.search)&&!(LIVE&&p==='/now'))return;
var IDX='https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/search/index.json';
var BASE=(document.currentScript&&document.currentScript.src||'').replace(/nowhome\.js.*$/,'')||'https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@master/site/p3/';
function $(s,r){return (r||document).querySelector(s)}function $$(s,r){return [].slice.call((r||document).querySelectorAll(s))}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function town(t){t=String(t||'').trim();return /^(East\s+)?Setauket/i.test(t)?'Setauket':t}
function track(a,o){try{if(window.gtag)window.gtag('event','now_home_click',Object.assign({action:a},o||{}))}catch(e){}}

var CSS=[
'.nh-sec{margin:34px 0 0}',
'.nh-row{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:4px 2px 12px;scrollbar-width:thin}',
'.nh-row>*{scroll-snap-align:start}',
'a.nh-biz{flex:0 0 250px;display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:18px;background:#fff;border:1px solid #e6ebf1;box-shadow:0 8px 22px rgba(20,38,59,.08);text-decoration:none!important;color:#14263b!important;transition:transform .2s ease,box-shadow .2s ease}',
'a.nh-biz:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(20,38,59,.14)}',
'.nh-logo{flex:0 0 64px;width:64px;height:64px;border-radius:14px;background:#fff center/contain no-repeat;border:1px solid #eef2f6;box-shadow:inset 0 0 0 4px #fff}',
'.nh-t{flex:1;min-width:0}',
'.nh-n{display:block;font-size:16px;font-weight:800;line-height:1.2;word-break:normal;overflow-wrap:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}',
'.nh-m{display:block;margin-top:4px;font-size:13px;color:#5b6978;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
'.nh-m .nh-st{color:#f2a93b;letter-spacing:1px;margin-right:4px}',
'.nh-vip{display:inline-block;margin-top:6px;font-size:10.5px;font-weight:800;letter-spacing:.08em;padding:3px 8px;border-radius:999px;background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#14263b;white-space:nowrap}',
'.nh-cats{display:flex;flex-wrap:wrap;gap:8px}',
'a.nh-cat{display:inline-flex;align-items:center;gap:8px;padding:9px 16px;border-radius:999px;background:#fff;border:1px solid #e3e9f0;color:#14263b!important;font-weight:700;font-size:15px;text-decoration:none!important;white-space:nowrap;word-break:normal;box-shadow:0 3px 10px rgba(20,38,59,.05)}',
'a.nh-cat:hover{border-color:#f2a93b;box-shadow:0 0 0 3px rgba(242,169,59,.2)}',
'a.nh-cat svg{width:18px;height:18px;flex:0 0 18px;stroke:#b7862a;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}',
'a.nh-cat.nh-allc{background:#14263b;color:#fff!important;border-color:#14263b}',
'a.nh-story{flex:0 0 300px;display:flex;gap:12px;align-items:center;padding:10px;border-radius:16px;background:#fff;border:1px solid #e6ebf1;text-decoration:none!important;color:#14263b!important;box-shadow:0 6px 18px rgba(20,38,59,.06)}',
'.nh-sim{flex:0 0 96px;width:96px;height:64px;border-radius:10px;background:#dfe6ee center/cover no-repeat}',
'.nh-sb{min-width:0}',
'.nh-sb i{display:block;font-style:normal;font-size:12px;font-weight:700;color:#b7862a;margin-bottom:3px}',
'.nh-sb b{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:15px;line-height:1.25;word-break:normal;overflow-wrap:normal}',
'.nh-more{font-size:inherit;font-weight:800;color:#0a6fb5!important;text-decoration:none!important;white-space:nowrap}',
'@media(max-width:600px){a.nh-biz{flex-basis:78%}a.nh-story{flex-basis:84%}a.nh-cat{font-size:14px;padding:8px 13px}.nh-cats{flex-wrap:nowrap;overflow-x:auto;padding:2px 2px 10px;scrollbar-width:none}.nh-cats::-webkit-scrollbar{display:none}}'
].join('');

var ICO={utensils:'<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M17 3c-2 0-3 3-3 6s1 4 3 4v8"/>',home:'<path d="M3 10.5L12 3l9 7.5M5 9v12h14V9M10 21v-6h4v6"/>',
 hammer:'<path d="M13 7l-9 9 3 3 9-9M12 4h5l3 3v2l-2 2-5-5z"/>',pulse:'<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21l8.8-8.3a5 5 0 0 0 0-7.1z"/>',
 key:'<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',scale:'<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 6a3 3 0 0 0 6 0L5 7M19 7l-3 6a3 3 0 0 0 6 0l-3-6"/>',
 scissors:'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.1 15.9M14.5 14.5L20 20M8.1 8.1L12 12"/>',dollar:'<circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.5-1-1.6-1.5-3-1.5-1.7 0-3 .8-3 2s1.3 1.8 3 2 3 .9 3 2.1-1.3 2-3 2c-1.5 0-2.6-.6-3-1.6M12 6.5v11"/>'};
var CATS=[['Restaurants','/restaurant','utensils'],['Home Services','/home-services','home'],['Contractors','/contractor','hammer'],['Health & Wellness','/health-wellness','pulse'],
 ['Real Estate','/real-estate-services','key'],['Attorneys','/attorney','scale'],['Beauty','/beauty-personal-care','scissors'],['Financial','/financial-services','dollar']];

function head(t,small,link,lt){var l=link?'<a class="nh-more" href="'+link+'">'+lt+' &rarr;</a>':'';return '<h2 class="wk-h2"><span>'+t+'</span>'+((small||l)?'<small>'+(small?small+(l?' &middot; ':''):'')+l+'</small>':'')+'</h2>'}

function run(){
  var main=$('.wk-main');if(!main||$('#nh-feat'))return !!main;
  var st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st);

  /* 1. Featured local businesses (VIP), after Top Things to Do */
  var feat=document.createElement('section');feat.className='wk-sec nh-sec';feat.id='nh-feat';
  feat.innerHTML=head('Featured Local Businesses','Neighbors who support Three Village Local','/search_results','See all businesses')+'<div class="nh-row" id="nh-frow"></div>';
  var picks=$('#wk-picks');if(picks&&picks.parentNode)picks.parentNode.insertBefore(feat,picks.nextSibling);else main.insertBefore(feat,main.firstChild);

  /* 2+3. categories + stories, before the business sign-up block (or at the end) */
  var ex=document.createElement('section');ex.className='wk-sec nh-sec';ex.id='nh-explore';
  ex.innerHTML=head('Browse Local Businesses','','','')+
    '<div class="nh-cats">'+CATS.map(function(c){return '<a class="nh-cat" href="'+c[1]+'"><svg viewBox="0 0 24 24">'+ICO[c[2]]+'</svg>'+esc(c[0])+'</a>'}).join('')+
    '<a class="nh-cat nh-allc" href="/categories">All categories &rarr;</a></div>'+
    '<div style="height:38px"></div>'+head('Latest Local Stories','','/blog','All stories')+'<div class="nh-row" id="nh-srow"></div>';
  var cta=$('.wk-cta')||$('#wk-next');
  if(cta&&cta.classList.contains('wk-cta'))cta.parentNode.insertBefore(ex,cta);
  else if(cta)cta.parentNode.insertBefore(ex,cta.nextSibling);else main.appendChild(ex);

  /* data */
  Promise.all([fetch(IDX+'?v='+Math.floor(Date.now()/36e5)).then(function(r){return r.json()}),
               fetch(BASE+'vip_meta.json').then(function(r){return r.json()}).catch(function(){return {}})]).then(function(a){
    var meta=a[1]||{},v=(a[0].members||[]).filter(function(m){return m.p==='vip'});
    var day=Math.floor(Date.now()/864e5);v.sort(function(x,y){return ((+x.id*7919+day*104729)%1000)-((+y.id*7919+day*104729)%1000)});  /* fair daily rotation */
    $('#nh-frow').innerHTML=v.map(function(m){var mt=meta[m.id]||{},r=mt.rating,n=mt.reviews;
      var line=(r?'<span class="nh-st">&#9733; '+(+r).toFixed(1)+'</span>'+(n?'('+n+') &middot; ':'&middot; '):'')+esc(town(m.t)||m.c||'');
      return '<a class="nh-biz" href="'+esc(m.u)+'" data-biz="'+esc(m.n)+'"><span class="nh-logo" style="background-image:url(\''+esc(m.l)+'\')"></span><span class="nh-t"><b class="nh-n">'+esc(m.n)+'</b><span class="nh-m">'+line+'</span><span class="nh-vip">&#9733; VIP</span></span></a>'}).join('');
  }).catch(function(){feat.style.display='none'});

  fetch('/blog').then(function(r){return r.text()}).then(function(t){var doc=new DOMParser().parseFromString(t,'text/html'),M=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'];
    var L=$$('.search_result',doc).map(function(it){var a=$('.mid_section a.h3',it),img=$('img.search_result_image',it),d=(($('.posted_meta_data span',it)||{}).textContent||'').match(/(\d+)\/(\d+)\/(\d+)/);
      return a?{h:a.getAttribute('href'),t:a.textContent.trim(),img:img?img.getAttribute('src'):'',d:d?M[+d[1]-1]+' '+(+d[2])+', '+d[3]:'',ts:d?new Date(+d[3],+d[1]-1,+d[2]).getTime():0}:null}).filter(Boolean).sort(function(a,b){return b.ts-a.ts}).slice(0,3);
    if(!L.length){$('#nh-srow').previousSibling.style.display='none';return}
    $('#nh-srow').innerHTML=L.map(function(x){return '<a class="nh-story" href="'+esc(x.h)+'"><span class="nh-sim" style="background-image:url(\''+esc(x.img)+'\')"></span><span class="nh-sb">'+(x.d?'<i>'+esc(x.d)+'</i>':'')+'<b>'+esc(x.t)+'</b></span></a>'}).join('')}).catch(function(){});

  document.addEventListener('click',function(e){var a=e.target.closest('#nh-feat a.nh-biz,#nh-explore a');if(!a)return;
    track(a.classList.contains('nh-biz')?'featured_business':a.classList.contains('nh-cat')?'category':a.classList.contains('nh-story')?'story':'more',{label:a.getAttribute('data-biz')||a.textContent.trim().slice(0,60)})});
  return true}
var n=0,t=setInterval(function(){n++;if(run()||n>60)clearInterval(t)},250);
})();
