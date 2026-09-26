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
