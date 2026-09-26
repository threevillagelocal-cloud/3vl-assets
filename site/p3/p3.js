/* 3VL premium page styles (Categories + Blog). Loaded sitewide from widget 13; acts only on its own pages.
   Business search results + Deals are NOT enabled here. */
(function(){
var me=document.currentScript;var BASE=me?me.src.replace(/p3\.js.*$/,''):'';
var path=location.pathname.replace(/\/+$/,'')||'/';
if(path!=='/categories'&&path!=='/blog')return;
function $(s,r){return (r||document).querySelector(s)}function $$(s,r){return [].slice.call((r||document).querySelectorAll(s))}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function mount(html,anchor){var d=document.createElement('div');d.id='p3';d.className='p3';d.innerHTML=html;anchor.parentNode.insertBefore(d,anchor);document.documentElement.classList.add('p3-on');return d}
var ICON={'arts':'&#127912;','attorney':'&#9878;&#65039;','automotive':'&#128663;','beauty':'&#128135;','commercial':'&#127970;','community':'&#129309;','contractor':'&#128296;','doctor':'&#129658;','education':'&#127891;','events':'&#127926;','farm':'&#127806;','financial':'&#128176;','fitness':'&#127947;&#65039;','health':'&#127807;','home':'&#127969;','hotel':'&#127976;','local-gov':'&#127963;&#65039;','marine':'&#9875;','marketing':'&#128227;','nightlife':'&#127864;','non-profit':'&#10084;&#65039;','payroll':'&#129534;','pet':'&#128062;','real':'&#127968;','restaurant':'&#127869;&#65039;','food':'&#127869;&#65039;','shopping':'&#128717;&#65039;','retail':'&#128717;&#65039;','travel':'&#9992;&#65039;','wedding':'&#128141;','insurance':'&#128737;&#65039;','dentist':'&#129463;','landscap':'&#127795;','tech':'&#128187;','child':'&#129490;','religious':'&#9962;','sports':'&#9917;','service':'&#128736;&#65039;'};
function iconFor(slug){for(var k in ICON){if(slug.indexOf(k)>=0)return ICON[k]}return '&#11088;'}
var COLORS=['#006fbb','#d9534f','#0f866c','#f0ad4e','#8e5bd6','#205081','#3aa0e8'];

/* ---------- CATEGORIES ---------- */
if(path==='/categories'){
  var panels=$$('.categories-panel');if(!panels.length)return;
  var cats=panels.map(function(p,i){var a=$('.topClass',p);var subs=$$('.sub-level-link > a.sub-category',p).map(function(x){return {n:x.textContent.trim(),h:x.getAttribute('href')}});
    return {n:a.textContent.trim(),h:a.getAttribute('href'),slug:(a.getAttribute('href')||'').replace('/',''),subs:subs,c:COLORS[i%COLORS.length]}});
  var quick=['Restaurants','Contractor','Home Services','Health & Wellness','Attorney','Real Estate','Beauty & Personal Care','Pet Services'].map(function(n){
    var m=cats.filter(function(c){return c.n.toLowerCase().indexOf(n.toLowerCase().split(' ')[0])===0})[0];return m?{n:n,h:m.h}:null}).filter(Boolean);
  var h='<header class="p3-phero" style="background-image:url(\''+BASE+'img/cafe-hero.jpg\')"><div class="p3-phin"><span class="p3-kick">THREE VILLAGE LOCAL</span><h1 class="p3-h1">Explore <em>Three Village</em></h1>'+
    '<p class="p3-sub">The local businesses your neighbors trust, all in one place.</p>'+
    '<form class="p3-search p3-hsearch" action="/search_results" method="get"><span>&#128269;</span><input id="p3q" name="q" autocomplete="off" placeholder="What are you looking for? Try &quot;pizza&quot;, &quot;plumber&quot;, &quot;dentist&quot;&hellip;"></form></div>'+
    '<span class="p3-credit">Photo: Shixart1985, CC BY 2.0</span></header>'+
    '<div class="p3-chips">'+quick.map(function(q){return '<a class="p3-chip" href="'+esc(q.h)+'">'+esc(q.n)+'</a>'}).join('')+'</div>'+
    '<div class="p3-cgrid">'+cats.map(function(c,i){return '<a class="p3-ctile" href="'+esc(c.h)+'" data-n="'+esc((c.n+' '+c.subs.map(function(s){return s.n}).join(' ')).toLowerCase())+'" style="--c:'+c.c+';--i:'+(i%12)+'"><span class="p3-cic">'+iconFor(c.slug)+'</span><span class="p3-ctx"><b>'+esc(c.n)+'</b><small>'+(c.subs.length?c.subs.length+' specialt'+(c.subs.length===1?'y':'ies'):'Browse all')+'</small></span><em>&rarr;</em></a>'}).join('')+'</div>'+
    '<p class="p3-none" id="p3none"></p>';
  var anchor=$('.category_filter_module')||panels[0];var root=mount(h,anchor);
  $$('.category_filter_module,.categories-panel').forEach(function(e){e.style.display='none'});
  $$('h1,h2').forEach(function(x){if(/Businesses by Category/.test(x.textContent)&&!root.contains(x))x.style.display='none'});
  var none=$('#p3none');
  $('#p3q').addEventListener('input',function(){var q=this.value.toLowerCase().trim(),n=0;$$('.p3-ctile').forEach(function(t){var ok=!q||t.getAttribute('data-n').indexOf(q)>=0;t.style.display=ok?'':'none';if(ok)n++});
    none.innerHTML=q&&!n?'No category matches &ldquo;'+esc(this.value)+'&rdquo;. <a href="/search_results?q='+encodeURIComponent(this.value)+'">Search every business for it &rarr;</a>':''});
}

/* ---------- BLOG ---------- */
if(path==='/blog'){
  var q0=/[?&]q=/.test(location.search);   /* keep BD's own layout for keyword searches */
  if(q0)return;
  var items=$$('.search_result');if(!items.length)return;
  function dfmt(s){var m=s.match(/(\d+)\/(\d+)\/(\d+)/);if(!m)return s;var M=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'];return M[+m[1]-1]+' '+(+m[2])+', '+m[3]}
  function read(it){var a=$('.mid_section a.h3',it)||$('a.h3',it),img=$('img.search_result_image',it),d=$('.posted_meta_data span',it),p=$('.mid_section p',it);
    if(!a)return null;var ex=p?p.textContent.replace(/View More/,'').replace(/\s+/g,' ').trim():'';
    return {t:a.textContent.trim(),h:a.getAttribute('href'),img:img?img.getAttribute('src').replace('news-pictures-thumbnails','news-pictures'):'',thumb:img?img.getAttribute('src'):'',d:d?d.textContent.replace('Posted','').trim():'',ex:ex}}
  function hide(it){it.style.display='none';it.setAttribute('data-p3','1');var n=it.nextElementSibling;while(n&&(n.tagName==='HR'||/^clearfix$/.test(n.className))){n.style.display='none';n=n.nextElementSibling}}
  function card(p,i){return '<a class="p3-bcard" href="'+esc(p.h)+'" style="--i:'+(i%9)+'"><div class="p3-bimg"><img src="'+esc(p.img)+'" alt="'+esc(p.t)+'" loading="lazy" onerror="if(this.src!==this.dataset.t){this.src=this.dataset.t}" data-t="'+esc(p.thumb)+'"></div><div class="p3-bb"><p class="p3-date">'+esc(dfmt(p.d))+'</p><h3>'+esc(p.t)+'</h3><p>'+esc(p.ex.slice(0,120))+(p.ex.length>120?'&hellip;':'')+'</p></div></a>'}
  function ts(p){var m=(p.d||'').match(/(\d+)\/(\d+)\/(\d+)/);return m?new Date(+m[3],+m[1]-1,+m[2]).getTime():0}
  var posts=items.map(read).filter(Boolean).sort(function(a,b){return ts(b)-ts(a)});   /* BD pins featured posts first; lead with the newest */
  var lead=posts[0],rest=posts.slice(1);
  var mos=posts.slice(0,6).map(function(p){return '<span style="background-image:url(\''+esc(p.img)+'\')"></span>'}).join('');
  var h='<header class="p3-hero"><div class="p3-mosaic">'+mos+'</div><div class="p3-hin"><span class="p3-kick">THREE VILLAGE LOCAL</span><h1 class="p3-h1">Local <em>Stories</em></h1><p class="p3-sub">Neighbors, businesses, events and the news that matters in Stony Brook, Setauket and Port Jefferson.</p></div></header>'+
    '<a class="p3-lead" href="'+esc(lead.h)+'"><div class="p3-limg"><img src="'+esc(lead.img)+'" alt="'+esc(lead.t)+'" onerror="if(this.src!==this.dataset.t){this.src=this.dataset.t}" data-t="'+esc(lead.thumb)+'"><span class="p3-new">&#9679; LATEST</span></div><div class="p3-lb"><p class="p3-date">'+esc(dfmt(lead.d))+'</p><h2>'+esc(lead.t)+'</h2><p>'+esc(lead.ex)+'</p><span class="p3-go">Read the story &rarr;</span></div></a>'+
    '<div class="p3-bgrid" id="p3grid">'+rest.map(card).join('')+'</div>';
  var root=mount(h,items[0].closest('[itemprop="mainEntity"]')||items[0]);
  items.forEach(hide);
  $$('.feature_results_header,.post-search-result-count-container,.views').forEach(function(e){if(!root.contains(e))e.style.display='none'});
  /* BD loads more posts as you scroll: turn each new one into a card */
  var grid=$('#p3grid'),seen={},n=rest.length;posts.forEach(function(p){seen[p.h]=1});
  new MutationObserver(function(){$$('.search_result:not([data-p3])').forEach(function(it){var p=read(it);hide(it);if(p&&!seen[p.h]){seen[p.h]=1;grid.insertAdjacentHTML('beforeend',card(p,n++))}})}).observe(document.body,{childList:true,subtree:true});
}
})();
