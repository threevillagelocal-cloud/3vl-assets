/* 3VL homepage refresh (MOCKUP): category tiles, Featured businesses row, one business band, bold headings, clean story cards. */
(function(){
var p=location.pathname.replace(/\/+$/,'')||'/';if(p!=='/'&&p!=='/home')return;
var hs=document.querySelector('.homepage-sections');if(!hs||document.getElementById('h2-tiles'))return;
function $(s,r){return (r||document).querySelector(s)}function $$(s,r){return [].slice.call((r||document).querySelectorAll(s))}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
document.documentElement.classList.add('h2-on');
var SVG={utensils:'<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M17 3c-2 0-3 3-3 6s1 4 3 4v8"/>',home:'<path d="M3 10.5L12 3l9 7.5M5 9v12h14V9M10 21v-6h4v6"/>',
 hammer:'<path d="M13 7l-9 9 3 3 9-9M12 4h5l3 3v2l-2 2-5-5z"/>',pulse:'<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21l8.8-8.3a5 5 0 0 0 0-7.1zM4 12h3.5l1.5-2.5 2.5 5 1.5-2.5H20"/>',
 key:'<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',scale:'<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 6a3 3 0 0 0 6 0L5 7M19 7l-3 6a3 3 0 0 0 6 0l-3-6"/>',
 scissors:'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.1 15.9M14.5 14.5L20 20M8.1 8.1L12 12"/>',dollar:'<circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.5-1-1.6-1.5-3-1.5-1.7 0-3 .8-3 2s1.3 1.8 3 2 3 .9 3 2.1-1.3 2-3 2c-1.5 0-2.6-.6-3-1.6M12 6.5v11"/>',
 grid:'<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>'};
var CATS=[['Restaurants','/restaurant','utensils'],['Home Services','/home-services','home'],['Contractors','/contractor','hammer'],['Health & Wellness','/health-wellness','pulse'],
 ['Real Estate','/real-estate-services','key'],['Attorneys','/attorney','scale'],['Beauty & Personal Care','/beauty-personal-care','scissors'],['Financial Services','/financial-services','dollar']];
function ico(k){return '<svg viewBox="0 0 24 24" aria-hidden="true">'+SVG[k]+'</svg>'}
function head(t,sub,link,lt){return '<div class="h2-head"><div><h2 class="h2-title">'+t+'</h2>'+(sub?'<p class="h2-sub">'+sub+'</p>':'')+'</div>'+(link?'<a class="h2-all" href="'+link+'">'+lt+' &rarr;</a>':'')+'</div>'}

/* 1. category tiles replace the stock-photo cards */
var s1=$('.homepage-section-1',hs);
var tiles=document.createElement('section');tiles.id='h2-tiles';tiles.className='h2-sec';
tiles.innerHTML='<div class="h2-in">'+head('Find a local business','Browse by what you need.','/categories','All categories')+'<div class="h2-tgrid">'+
  CATS.map(function(c){return '<a class="h2-tile" href="'+c[1]+'"><span class="h2-ic">'+ico(c[2])+'</span><b>'+esc(c[0])+'</b></a>'}).join('')+'</div></div>';
hs.insertBefore(tiles,hs.firstChild);if(s1)s1.style.display='none';

/* 2. Three Village Favorites -> Featured Local Businesses (same members, new card) */
var s2=$('.homepage-section-2',hs),mem=s2?$$('.slick-slide:not(.slick-cloned) .member',s2):[];
if(mem.length){var seen={},cards=mem.map(function(m){var a=$('a.h4',m);if(!a)return '';var href=a.getAttribute('href');if(seen[href])return '';seen[href]=1;
    var nm=(a.getAttribute('title')||a.textContent).replace(/\s*-\s*View Listing$/,'').trim(),img=$('img',m),src=img?(img.getAttribute('data-src')||img.getAttribute('src')):'';
    var info=$('.recent-member-info',m),town=info?(info.textContent.split('Located in')[1]||'').replace(/\s+/g,' ').trim().replace(/View Listing/g,'').replace('Setauket- East Setauket','East Setauket').replace(/,?\s*$/,'').trim():'';
    var rt=($('.the-average-rating',m)||{}).textContent||'',r=(rt.match(/([\d.]+)\s*\/\s*5/)||[])[1],n=((($('.the-review-count',m)||{}).textContent||'').match(/\d+/)||[])[0];
    var ver=!!$('.member-search-verified',m);
    return '<a class="h2-fcard" href="'+esc(href)+'"><span class="h2-ftag">&#9733; FEATURED</span><span class="h2-flogo"><img src="'+esc(src)+'" alt="" loading="lazy"></span>'+
      '<b class="h2-fname">'+esc(nm)+'</b><span class="h2-ftown">&#128205; '+esc(town||'Three Village')+'</span><span class="h2-fbadges">'+(ver?'<i class="h2-ok">&#10003; Verified</i>':'')+(r?'<i class="h2-star">&#9733; '+(+r).toFixed(1)+(n?' ('+n+')':'')+'</i>':'')+'</span>'+
      '<span class="h2-fgo">View profile &rarr;</span></a>'}).join('');
  var fs=document.createElement('section');fs.id='h2-feat';fs.className='h2-sec h2-alt';
  fs.innerHTML='<div class="h2-in">'+head('Featured local businesses','Trusted Three Village businesses that support this site.','/search_results','See all businesses')+
    '<div class="h2-rowwrap"><button class="h2-arr h2-prev" aria-label="Scroll left">&#8249;</button><div class="h2-frow">'+cards+'</div><button class="h2-arr h2-next" aria-label="Scroll right">&#8250;</button></div></div>';
  s2.parentNode.insertBefore(fs,s2);s2.style.display='none';
  var row=$('.h2-frow',fs);$('.h2-prev',fs).onclick=function(){row.scrollBy({left:-row.clientWidth*.9,behavior:'smooth'})};$('.h2-next',fs).onclick=function(){row.scrollBy({left:row.clientWidth*.9,behavior:'smooth'})};
  $$('.h2-flogo img',fs).forEach(function(img){function go(){try{var w=img.naturalWidth,h=img.naturalHeight;if(!w)return;var c=document.createElement('canvas'),k=Math.min(1,500/Math.max(w,h));c.width=Math.round(w*k);c.height=Math.round(h*k);var x=c.getContext('2d');x.drawImage(img,0,0,c.width,c.height);var d=x.getImageData(0,0,c.width,c.height).data,W=c.width,H=c.height,t=H,l=W,r=0,b=0;
    for(var y=0;y<H;y++)for(var X=0;X<W;X++){var i=(y*W+X)*4;if(d[i+3]>20&&(d[i]<235||d[i+1]<235||d[i+2]<235)){if(y<t)t=y;if(y>b)b=y;if(X<l)l=X;if(X>r)r=X}}
    if(r<=l||b<=t||(r-l)*(b-t)>W*H*.92)return;var p=Math.round(Math.max(r-l,b-t)*.05);l=Math.max(0,l-p);t=Math.max(0,t-p);r=Math.min(W-1,r+p);b=Math.min(H-1,b+p);var o=document.createElement('canvas');o.width=r-l+1;o.height=b-t+1;o.getContext('2d').drawImage(c,l,t,o.width,o.height,0,0,o.width,o.height);img.onload=null;img.src=o.toDataURL('image/png')}catch(e){}}
    if(img.complete&&img.naturalWidth)go();else img.onload=go})}

/* 3+4. one business band replaces the black band + mission/list cards */
var s3=$('.homepage-section-3',hs),s4=$('.homepage-section-4',hs),s5=$('.homepage-section-5',hs);
var band=document.createElement('section');band.id='h2-biz';band.className='h2-sec';
band.innerHTML='<div class="h2-in"><div class="h2-band"><div><p class="h2-bk">FOR LOCAL BUSINESSES</p><h2 class="h2-bt">Get found by your Three Village neighbors.</h2>'+
  '<p class="h2-bs">Free listing on the website and the Three Village Local app. Upgrade anytime to be featured.</p></div>'+
  '<div class="h2-bbtns"><a class="h2-bbtn" href="/join">Get listed free</a><a class="h2-blink" href="/join">See featured options &rarr;</a></div></div></div>';
if(s3)s3.style.display='none';if(s4)s4.style.display='none';

/* 5. stories: same card style as the blog page, full titles + dates from /blog */
if(s5){var st=document.createElement('section');st.id='h2-stories';st.className='h2-sec';
  st.innerHTML='<div class="h2-in">'+head('Latest local stories','','/blog','All stories')+'<div class="h2-sgrid" id="h2-sgrid"></div></div>';
  var fallback=$$('.slickBlogArticles > div',s5).slice(0,3).map(function(d){var a=$('a.homepage-link-element',d)||$('a',d),pic=$('.pic',d);return {h:a?a.getAttribute('href'):'#',t:(($('.pic-title',d)||{}).textContent||'').trim(),img:pic?pic.getAttribute('data-src'):'',d:''}});
  function draw(L){$('.h2-sgrid',st).innerHTML=L.slice(0,3).map(function(x){return '<a class="h2-scard" href="'+esc(x.h)+'"><span class="h2-simg"><img src="'+esc(x.img)+'" alt="" loading="lazy"></span><span class="h2-sb">'+(x.d?'<i>'+esc(x.d)+'</i>':'')+'<b>'+esc(x.t)+'</b></span></a>'}).join('')}
  draw(fallback);
  fetch('/blog').then(function(r){return r.text()}).then(function(t){var doc=new DOMParser().parseFromString(t,'text/html'),M=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'];
    var L=$$('.search_result',doc).map(function(it){var a=$('.mid_section a.h3',it),img=$('img.search_result_image',it),d=(($('.posted_meta_data span',it)||{}).textContent||'').match(/(\d+)\/(\d+)\/(\d+)/);
      return a?{h:a.getAttribute('href'),t:a.textContent.trim(),img:img?img.getAttribute('src').replace('news-pictures-thumbnails','news-pictures'):'',d:d?M[+d[1]-1]+' '+(+d[2])+', '+d[3]:'',ts:d?new Date(+d[3],+d[1]-1,+d[2]).getTime():0}:null}).filter(Boolean).sort(function(a,b){return b.ts-a.ts});
    if(L.length>=3)draw(L)}).catch(function(){});
  s5.parentNode.insertBefore(st,s5);s5.style.display='none';st.parentNode.insertBefore(band,st.nextSibling)}
else hs.appendChild(band);
})();
/* Three Village Now portal banner (9/27): sits right above Happening Today (#td). */
(function(){
var p=location.pathname.replace(/\/+$/,'')||'/';if(p!=='/'&&p!=='/home')return;
var css='#tvn{max-width:1140px;margin:30px auto 6px;padding:0 15px;font-family:"Radio Canada",sans-serif}'
+'#tvn a.tvn-card{position:relative;overflow:hidden;display:grid;grid-template-columns:1.1fr 1fr;gap:26px;align-items:center;padding:28px 30px;border-radius:26px;text-decoration:none!important;color:#fff!important;'
+'background:radial-gradient(circle at 92% 0%,rgba(143,208,255,.22),transparent 45%),radial-gradient(circle at 0% 100%,rgba(58,160,232,.32),transparent 50%),linear-gradient(150deg,#1f3a5c,#13233a 60%,#0f1a28);'
+'border:1.5px solid rgba(255,197,61,.45);box-shadow:0 20px 50px rgba(15,26,40,.25);transition:transform .2s,box-shadow .2s}'
+'#tvn a.tvn-card:hover{transform:translateY(-3px);box-shadow:0 26px 60px rgba(15,26,40,.32)}'
+'#tvn .tvn-live{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:700;letter-spacing:.16em;padding:6px 12px;border-radius:999px;background:#e5322d;color:#fff}'
+'#tvn .tvn-live i{width:9px;height:9px;border-radius:50%;background:#fff;animation:tvnPulse 1.6s infinite}'
+'@keyframes tvnPulse{0%{box-shadow:0 0 0 0 rgba(255,255,255,.8)}70%{box-shadow:0 0 0 8px rgba(255,255,255,0)}100%{box-shadow:0 0 0 0 rgba(255,255,255,0)}}'
+'#tvn .tvn-h{display:block;font-size:40px;font-weight:700;line-height:1.05;letter-spacing:-.02em;margin:12px 0 8px;color:#fff;word-break:normal}'
+'#tvn .tvn-h em{font-style:normal;color:#ffc53d}'
+'#tvn .tvn-d{display:block;font-size:17px;line-height:1.45;color:#c9d6e4;margin:0 0 16px;word-break:normal}'
+'#tvn .tvn-btn{position:relative;overflow:hidden;display:inline-flex;align-items:center;gap:8px;font-size:17px;font-weight:700;padding:13px 22px;border-radius:14px;background:#ffc53d;color:#13233a;box-shadow:0 10px 24px rgba(255,197,61,.3)}'
+'#tvn .tvn-btn:after{content:"";position:absolute;inset:0;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.6) 48%,transparent 62%);transform:translateX(-130%);animation:tvnShine 4.5s ease-in-out 1.2s infinite}'
+'@keyframes tvnShine{0%,70%{transform:translateX(-130%)}90%,100%{transform:translateX(130%)}}'
+'#tvn .tvn-g{display:grid;grid-template-columns:1fr 1fr;gap:12px}'
+'#tvn .tvn-t{display:flex;align-items:center;gap:12px;padding:14px;border-radius:18px;background:linear-gradient(155deg,rgba(255,255,255,.14),rgba(255,255,255,.04));border:1px solid rgba(255,255,255,.18);box-shadow:inset 0 1px 0 rgba(255,255,255,.2)}'
+'#tvn .tvn-ic{position:relative;flex:0 0 46px;width:46px;height:46px;border-radius:14px;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,var(--a),var(--b));border:1px solid rgba(255,255,255,.45);box-shadow:inset 0 2px 0 rgba(255,255,255,.5),0 8px 18px rgba(0,0,0,.25)}'
+'#tvn .tvn-ic svg{width:24px;height:24px}'
+'#tvn .tvn-t b{display:block;font-size:17px;color:#fff;line-height:1.15;white-space:nowrap}'
+'#tvn .tvn-t small{display:block;font-size:13px;color:#c9d6e4;line-height:1.3}'
+'@media(max-width:860px){#tvn a.tvn-card{grid-template-columns:1fr;gap:18px;padding:22px 18px}#tvn .tvn-h{font-size:32px}#tvn .tvn-btn{display:flex;justify-content:center}#tvn .tvn-t{padding:11px}#tvn .tvn-ic{flex-basis:40px;width:40px;height:40px}#tvn .tvn-t b{font-size:15.5px}#tvn .tvn-t small{display:none}#tvn .tvn-d{font-size:16px}#tvn .tvn-h{margin:10px 0 6px}}'
+'@media(prefers-reduced-motion:reduce){#tvn .tvn-live i,#tvn .tvn-btn:after{animation:none}}';
function ic(a,b,path){return '<span class="tvn-ic" style="--a:'+a+';--b:'+b+'"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'+path+'</svg></span>'}
var html='<a class="tvn-card" href="/now"><div>'
+'<span class="tvn-live"><i></i>LIVE</span>'
+'<span class="tvn-h">Three Village <em>Now</em></span>'
+'<span class="tvn-d">Your live local community dashboard: events, restaurant specials, weather and alerts for Setauket, Stony Brook and Port Jefferson, today and all week.</span>'
+'<span class="tvn-btn">Enter Three Village Now &rarr;</span></div>'
+'<div class="tvn-g">'
+'<span class="tvn-t">'+ic('#5cb8f2','#1f6fb0','<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>')+'<span><b>Events</b><small>Today and this week</small></span></span>'
+'<span class="tvn-t">'+ic('#ffd76a','#f5a800','<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M17 3c-2 0-3 3-3 6s1 4 3 4v8"/>')+'<span><b>Eat &amp; Drink</b><small>Local specials</small></span></span>'
+'<span class="tvn-t">'+ic('#6fd6b8','#0f866c','<circle cx="9" cy="9" r="3.5"/><path d="M9 2.5v1.5M2.5 9H4M4.4 4.4l1 1M13.6 4.4l-1 1"/><path d="M9 19h9a3.5 3.5 0 0 0 0-7 5 5 0 0 0-9.6 1.4A3 3 0 0 0 9 19z"/>')+'<span><b>Weather</b><small>Live forecast</small></span></span>'
+'<span class="tvn-t">'+ic('#ff7a70','#d9362f','<path d="M12 3L2 20h20L12 3z"/><path d="M12 10v4.5"/><circle cx="12" cy="17.3" r=".6" fill="#fff"/>')+'<span><b>Alerts</b><small>Closings and warnings</small></span></span>'
+'</div></a>';
function put(){
  if(document.getElementById('tvn'))return true;
  var td=document.getElementById('td'),hs=document.querySelector('.homepage-sections');if(!td&&!hs)return false;
  var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
  var box=document.createElement('div');box.id='tvn';box.innerHTML=html;
  if(td)td.parentNode.insertBefore(box,td);else hs.insertBefore(box,hs.firstChild);
  box.querySelector('a').addEventListener('click',function(){try{gtag('event','now_banner_click')}catch(e){}});
  return true;
}
var n=0,t=setInterval(function(){n++;if((document.getElementById('td')&&put())||n>30){clearInterval(t);put()}},200);
})();
/* Homepage search box tidy-up (9/27, until the smart-search overhaul): drop the "What do you need:" label, friendlier placeholder. */
(function(){
var p=location.pathname.replace(/\/+$/,'')||'/';if(p!=='/'&&p!=='/home')return;
var st=document.createElement('style');st.textContent='.search_box > .form-group.col-md-5{display:none!important}';document.head.appendChild(st);
function ph(){var i=document.querySelector('.search_box input[name=q]');if(!i)return;
  i.setAttribute('placeholder','Search businesses & services');i.setAttribute('aria-label','Search local businesses')}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ph);else ph();
})();
