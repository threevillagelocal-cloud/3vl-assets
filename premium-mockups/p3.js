/* MOCKUP ONLY: premium "Now/Events" look for Categories, Blog, Business search results and Deals. Injected in a private preview browser. */
(function(){
var VIP=["112", "115", "122", "137", "138", "142", "151", "217", "228", "240", "299", "364", "474", "484", "499", "71", "78"];
var path=location.pathname.replace(/\/+$/,'')||'/';
function $(s,r){return (r||document).querySelector(s)}function $$(s,r){return [].slice.call((r||document).querySelectorAll(s))}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function hero(kick,title,accent,sub,stats,mosaic,btn){
  return '<header class="p3-hero"><div class="p3-mosaic">'+(mosaic||[]).slice(0,6).map(function(u){return '<span style="background-image:url(\''+esc(u)+'\')"></span>'}).join('')+'</div>'+
  '<div class="p3-hin"><span class="p3-kick">'+kick+'</span><h1 class="p3-h1">'+title+' <em>'+accent+'</em></h1><p class="p3-sub">'+sub+'</p>'+
  (stats&&stats.length?'<div class="p3-stats">'+stats.map(function(s){return '<div><b>'+s[0]+'</b><span>'+s[1]+'</span></div>'}).join('')+'</div>':'')+(btn||'')+'</div></header>'}
function mount(html,anchor){var d=document.createElement('div');d.id='p3';d.className='p3';d.innerHTML=html;anchor.parentNode.insertBefore(d,anchor);document.documentElement.classList.add('p3-on');return d}
var ICON={'arts':'&#127912;','attorney':'&#9878;&#65039;','automotive':'&#128663;','beauty':'&#128135;','commercial':'&#127970;','community':'&#129309;','contractor':'&#128296;','doctor':'&#129658;','education':'&#127891;','events':'&#127926;','farm':'&#127806;','financial':'&#128176;','fitness':'&#127947;&#65039;','health':'&#127807;','home':'&#127969;','hotel':'&#127976;','local-gov':'&#127963;&#65039;','marine':'&#9875;','marketing':'&#128227;','nightlife':'&#127864;','non-profit':'&#10084;&#65039;','payroll':'&#129534;','pet':'&#128062;','real':'&#127968;','restaurant':'&#127869;&#65039;','food':'&#127869;&#65039;','shopping':'&#128717;&#65039;','retail':'&#128717;&#65039;','travel':'&#9992;&#65039;','wedding':'&#128141;','insurance':'&#128737;&#65039;','dentist':'&#129463;','landscap':'&#127795;','tech':'&#128187;','child':'&#129490;','religious':'&#9962;','sports':'&#9917;','service':'&#128736;&#65039;'};
function iconFor(slug){for(var k in ICON){if(slug.indexOf(k)>=0)return ICON[k]}return '&#11088;'}
var COLORS=['#006fbb','#d9534f','#0f866c','#f0ad4e','#8e5bd6','#205081','#3aa0e8'];

/* ---------- CATEGORIES ---------- */
if(path==='/categories'){
  var panels=$$('.categories-panel');if(!panels.length)return;
  var cats=panels.map(function(p,i){var a=$('.topClass',p);var subs=$$('.sub-level-link > a.sub-category',p).map(function(x){return {n:x.textContent.trim(),h:x.getAttribute('href')}});
    return {n:a.textContent.trim(),h:a.getAttribute('href'),slug:(a.getAttribute('href')||'').replace('/',''),subs:subs,c:COLORS[i%COLORS.length]}});
  var total=cats.reduce(function(s,c){return s+c.subs.length},0);
  var h=hero('THREE VILLAGE LOCAL','Explore','Three Village','Every local business in Stony Brook, Setauket, Port Jefferson and nearby, sorted so you can find the right one fast.',[[cats.length,'categories'],[total,'specialties'],['100%','local']])+
    '<div class="p3-search"><span>&#128269;</span><input id="p3q" placeholder="What are you looking for? Try &quot;pizza&quot;, &quot;plumber&quot;, &quot;dentist&quot;&hellip;"></div>'+
    '<div class="p3-chips">'+['Restaurants','Contractor','Home Services','Health & Wellness','Attorney','Real Estate','Beauty & Personal Care','Pet Services'].map(function(n){return '<span class="p3-chip">'+esc(n)+'</span>'}).join('')+'</div>'+
    '<div class="p3-cgrid">'+cats.map(function(c,i){return '<a class="p3-ctile" href="'+esc(c.h)+'" data-n="'+esc((c.n+' '+c.subs.map(function(s){return s.n}).join(' ')).toLowerCase())+'" style="--c:'+c.c+';--i:'+(i%12)+'"><span class="p3-cic">'+iconFor(c.slug)+'</span><b>'+esc(c.n)+'</b><small>'+(c.subs.length?c.subs.slice(0,3).map(function(s){return esc(s.n)}).join(' &middot; ')+(c.subs.length>3?' &middot; +'+(c.subs.length-3)+' more':''):'Browse all')+'</small><em>&rarr;</em></a>'}).join('')+'</div>';
  var anchor=$('.category_filter_module')||panels[0];var root=mount(h,anchor);
  $$('.category_filter_module,.categories-panel').forEach(function(e){e.style.display='none'});
  $$('h1,h2').forEach(function(x){if(/Businesses by Category/.test(x.textContent)&&!root.contains(x))x.style.display='none'});
  $('#p3q').addEventListener('input',function(){var q=this.value.toLowerCase().trim();$$('.p3-ctile').forEach(function(t){t.style.display=!q||t.getAttribute('data-n').indexOf(q)>=0?'':'none'})});
}

/* ---------- BLOG ---------- */
if(path==='/blog'){
  var items=$$('.search_result.featured-post-blog');if(!items.length)return;
  var posts=items.map(function(it){var a=$('.mid_section a.h3',it),img=$('img.search_result_image',it),d=$('.posted_meta_data span',it),p=$('.mid_section p',it);
    var ex=p?p.textContent.replace(/View More/,'').trim():'';return {t:a.textContent.trim(),h:a.getAttribute('href'),img:img?img.getAttribute('src').replace('news-pictures-thumbnails','news-pictures'):'',d:d?d.textContent.replace('Posted','').trim():'',ex:ex}});
  function dfmt(s){var m=s.match(/(\d+)\/(\d+)\/(\d+)/);if(!m)return s;var M=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'];return M[+m[1]-1]+' '+(+m[2])+', '+m[3]}
  var lead=posts[0],rest=posts.slice(1);
  var h=hero('THREE VILLAGE LOCAL','Local','Stories','Neighbors, businesses, events and the news that matters in Stony Brook, Setauket and Port Jefferson.',[],posts.map(function(p){return p.img}))+
    '<div class="p3-chips">'+['All stories','Events','Business Spotlights','Community','Storm & Weather','Food & Drink'].map(function(n,i){return '<span class="p3-chip'+(i?'':' is-on')+'">'+n+'</span>'}).join('')+'</div>'+
    '<a class="p3-lead" href="'+esc(lead.h)+'"><div class="p3-limg" style="background-image:url(\''+esc(lead.img)+'\')"><span class="p3-new">&#9679; LATEST</span></div><div class="p3-lb"><p class="p3-date">'+esc(dfmt(lead.d))+'</p><h2>'+esc(lead.t)+'</h2><p>'+esc(lead.ex)+'</p><span class="p3-go">Read the story &rarr;</span></div></a>'+
    '<div class="p3-bgrid">'+rest.map(function(p,i){return '<a class="p3-bcard" href="'+esc(p.h)+'" style="--i:'+i+'"><div class="p3-bimg" style="background-image:url(\''+esc(p.img)+'\')"></div><div class="p3-bb"><p class="p3-date">'+esc(dfmt(p.d))+'</p><h3>'+esc(p.t)+'</h3><p>'+esc(p.ex.slice(0,120))+(p.ex.length>120?'&hellip;':'')+'</p></div></a>'}).join('')+'</div>';
  var first=items[0];var root=mount(h,first.closest('[itemprop="mainEntity"]')||first);
  items.forEach(function(e){e.style.display='none';var n=e.nextElementSibling;while(n&&(n.tagName==='HR'||n.className==='clearfix')){n.style.display='none';n=n.nextElementSibling}});
  $$('.feature_results_header,.post-search-result-count-container,.views').forEach(function(e){if(!root.contains(e))e.style.display='none'});
}

/* ---------- BUSINESS RESULTS (search + category pages) ---------- */
var mem=$$('.member_results.search_result');
if(mem.length){
  var biz=mem.map(function(it){var g=function(p){var m=it.querySelector('[itemprop="'+p+'"]');return m?(m.getAttribute('content')||m.getAttribute('href')||''):''};
    var uid=(it.querySelector('.postItem')||{getAttribute:function(){return ''}}).getAttribute('data-userid');
    return {n:g('name'),u:(it.querySelector('link[itemprop="url"][href*="#"]')||it.querySelector('[itemtype$="LocalBusiness"] link[itemprop="url"]')||{}).href||'',img:g('image'),tel:g('telephone'),d:g('description'),st:g('streetAddress'),town:g('addressLocality'),vip:VIP.indexOf(uid)>=0}});
  var q=(location.search.match(/q=([^&]*)/)||[])[1];q=q?decodeURIComponent(q.replace(/\+/g,' ')):'';
  var h=hero('THREE VILLAGE LOCAL',q?'Results for':'Local','&ldquo;'+esc(q||'Businesses')+'&rdquo;','Neighbor-rated local businesses. Call, get directions or see the full listing.',[[biz.length,'local matches'],[biz.filter(function(b){return b.vip}).length,'VIP members']])+
    '<div class="p3-rgrid">'+biz.map(function(b,i){var town=(b.town||'').replace('Setauket- East Setauket','East Setauket');var tel=(b.tel||'').replace(/[^\d]/g,'').slice(-10);
      return '<div class="p3-rcard'+(b.vip?' is-vip':'')+'" style="--i:'+i+'"><a class="p3-rtop" href="'+esc(b.u.replace(/#.*$/,''))+'"><img src="'+esc(b.img)+'" alt="" loading="lazy"><div><b>'+esc(b.n)+'</b><small>&#128205; '+esc(town||'Three Village')+'</small>'+(b.vip?'<span class="p3-vip">&#11088; VIP local business</span>':'')+'</div></a>'+
      '<p class="p3-rd">'+esc(b.d.slice(0,140))+(b.d.length>140?'&hellip;':'')+'</p><div class="p3-racts">'+(tel?'<a class="p3-call" href="tel:'+tel+'">&#128222; Call</a>':'')+
      '<a href="https://www.google.com/maps/search/?api=1&amp;query='+encodeURIComponent(b.n+' '+(b.st||'')+' '+town)+'" target="_blank">&#128205; Map</a><a class="p3-view" href="'+esc(b.u.replace(/#.*$/,''))+'">View &rarr;</a></div></div>'}).join('')+'</div>';
  var first=mem[0];var root=mount(h,first.closest('[itemprop="mainEntity"]')||first.parentNode.firstElementChild||first);
  mem.forEach(function(e){e.style.display='none'});
  $$('.feature_results_header,.post-search-result-count-container,.views,.member_results_header,.member-search-result-count-container,.member-search-result-filters,.sort-members-select').forEach(function(e){if(!root.contains(e))e.style.display='none'});
  $$('h1').forEach(function(x){if(!root.contains(x)&&/Business Directory/.test(x.textContent))x.style.display='none'});
}

/* ---------- DEALS ---------- */
if(path==='/coupons'){
  var cs=$$('.search_result');if(!cs.length)return;
  var deals=cs.map(function(it){var a=$('.mid_section a.h3, a.h3',it),img=$('img',it),p=$('.mid_section p, p',it),by=$('.posted_meta_data a',it),off=it.textContent.match(/(\d+%\s*OFF|\$\d+\s*OFF|FREE [A-Z ]+)/i);
    return {t:a?a.textContent.trim():'',h:a?a.getAttribute('href'):'#',img:img?img.getAttribute('src'):'',ex:p?p.textContent.replace(/View More/,'').trim():'',by:by?by.textContent.trim():'',off:off?off[1].toUpperCase():'SPECIAL'}});
  var h=hero('THREE VILLAGE LOCAL','Local','Deals','Specials and offers from Three Village businesses. Show the deal at the counter or tap to claim.',[[deals.length,'live deal'+(deals.length===1?'':'s')],['Free','for businesses to post']])+
    '<div class="p3-dgrid">'+deals.map(function(d,i){return '<a class="p3-ticket" href="'+esc(d.h)+'" style="--i:'+i+'"><div class="p3-timg" style="background-image:url(\''+esc(d.img)+'\')"></div><div class="p3-tb"><span class="p3-off">'+esc(d.off)+'</span><h3>'+esc(d.t)+'</h3><p class="p3-by">'+esc(d.by)+'</p><p>'+esc(d.ex.slice(0,150))+'&hellip;</p><span class="p3-claim">Get this deal &rarr;</span></div></a>'}).join('')+
    '<a class="p3-ticket p3-post" href="/promotion"><div class="p3-tb"><span class="p3-off">YOUR BUSINESS HERE</span><h3>Got a special this week?</h3><p>Send it to us and we&rsquo;ll feature it free here and on Three Village Now.</p><span class="p3-claim">Submit a deal &rarr;</span></div></a></div>';
  var root=mount(h,cs[0].closest('[itemprop="mainEntity"]')||cs[0]);
  cs.forEach(function(e){e.style.display='none'});
  $$('.feature_results_header,.post-search-result-count-container,.views').forEach(function(e){if(!root.contains(e))e.style.display='none'});
}
})();
