/* 3VL smart search: instant, relevance-ranked business results under the homepage search box.
   Index = search/index.json (built nightly from BD members + Member Match + AI neighbor words by 3vl-site-guard member-db).
   Ranking: best match first; paid plans only break ties (and get a badge). Enter / "See all" still runs BD's normal search. */
(function(){
'use strict';
var IDX='https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/search/index.json';
var FORCE=/[?&]tvlsearch=1/.test(location.search);
var p=location.pathname.replace(/\/+$/,'')||'/';
if(!FORCE&&p!=='/'&&p!=='/home')return;
var STOP={the:1,a:1,an:1,and:1,of:1,'for':1,near:1,me:1,'in':1,best:1,local:1,good:1,my:1,to:1,at:1,on:1,with:1,service:1,services:1,company:1,ny:1};
var TIER={vip:3,noticed:2,house:1,basic:0,claim:0};
var data=null,loading=null;
function track(n,o){try{if(window.gtag)window.gtag('event',n,o)}catch(e){}}
function esc(s){return String(s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function norm(s){return String(s||'').toLowerCase().replace(/&amp;/g,'&').replace(/[’']/g,'').replace(/[^a-z0-9&]+/g,' ').trim()}
function stem(w){return w.length>4?w.replace(/(ies)$/,'y').replace(/(es|s)$/,''):w}
function load(){if(data||loading)return loading;loading=fetch(IDX+'?v='+Math.floor(Date.now()/36e5)).then(function(r){return r.json()}).then(function(j){
  data=(j.members||[]).map(function(m){return {m:m,name:norm(m.n),cat:norm(m.c+' '+(m.s||[]).join(' ')),terms:(m.k||[]).map(norm),desc:norm(m.d),town:norm(m.t)}});return data}).catch(function(){loading=null});return loading}
function lev1(a,b){if(Math.abs(a.length-b.length)>1)return false;var i=0,j=0,e=0;while(i<a.length&&j<b.length){if(a[i]===b[j]){i++;j++;continue}if(++e>1)return false;if(a.length>b.length)i++;else if(b.length>a.length)j++;else{i++;j++}}return e+(a.length-i)+(b.length-j)<=1}
function wordHit(w,text){if(!text)return 0;if((' '+text+' ').indexOf(' '+w)>-1)return 2;if(text.indexOf(w)>-1)return 1;
  if(w.length>=5){var ws=text.split(' ');for(var i=0;i<ws.length;i++)if(ws[i].length>=4&&lev1(stem(w),stem(ws[i])))return 1}return 0}
function score(r,q,words){var s=0;
  if(r.name===q)s+=400;else if(r.name.indexOf(q)===0)s+=220;else if((' '+r.name).indexOf(' '+q)>-1)s+=150;
  if(q.length>2){for(var i=0;i<r.terms.length;i++){if(r.terms[i]===q){s+=160;break}if(r.terms[i].indexOf(q)>-1){s+=90;break}}
    if(r.cat.indexOf(q)>-1)s+=110}
  var all=true;words.forEach(function(w){var ws=stem(w),best=0;
    best=Math.max(best,wordHit(ws,r.name)*45,wordHit(ws,r.cat)*35);
    for(var i=0;i<r.terms.length&&best<60;i++)best=Math.max(best,wordHit(ws,r.terms[i])*30);
    if(!best)best=wordHit(ws,r.desc)*8+wordHit(ws,r.town)*10;
    if(!best)all=false;s+=best});
  if(words.length>1&&all)s+=40;if(!all&&words.length>1)s*=.55;
  return s}
function search(qraw){var q=norm(qraw);if(q.length<2||!data)return [];
  var words=q.split(' ').filter(function(w){return w&&!STOP[w]});if(!words.length)words=[q];
  var out=[];data.forEach(function(r){var s=score(r,q,words);if(s>=28)out.push({r:r,s:s})});
  out.sort(function(a,b){return b.s-a.s||(TIER[b.r.m.p]||0)-(TIER[a.r.m.p]||0)||(b.r.m.l?1:0)-(a.r.m.l?1:0)||a.r.m.n.localeCompare(b.r.m.n)});
  return out.slice(0,7)}
function hl(text,q){var t=esc(text),ws=norm(q).split(' ').filter(function(w){return w.length>1&&!STOP[w]});
  ws.forEach(function(w){t=t.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'),'<b>$1</b>')});return t}
var CSS='#tvlss{position:absolute;left:0;right:0;top:calc(100% + 8px);z-index:9999;background:#fff;border:1px solid #e3e9f0;border-radius:18px;box-shadow:0 24px 60px rgba(15,26,40,.25);overflow:hidden;text-align:left;font-family:inherit}'+
'#tvlss[hidden]{display:none}'+
'#tvlss .ss-h{margin:0;padding:10px 16px 6px;font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#0a6fb5}'+
'#tvlss a.ss-r{display:flex;align-items:center;gap:12px;padding:10px 16px;text-decoration:none!important;color:#1b2f45;border-top:1px solid #f0f3f7}'+
'#tvlss a.ss-r:hover,#tvlss a.ss-r.on{background:#f3f8fd}'+
'#tvlss .ss-l{flex:0 0 44px;width:44px;height:44px;border-radius:12px;background:#eef3f8 center/cover no-repeat;border:1px solid #e3e9f0}'+
'#tvlss .ss-l.ss-ini{display:flex;align-items:center;justify-content:center;font-weight:800;color:#205081;font-size:17px;background:linear-gradient(145deg,#fff,#e8f1fa)}'+
'#tvlss .ss-t{flex:1;min-width:0}'+
'#tvlss .ss-n{display:block;font-size:16px;font-weight:700;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'+
'#tvlss .ss-n b{color:#0a6fb5}'+
'#tvlss .ss-m{display:block;font-size:13px;color:#5b6b7d;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:2px}'+
'#tvlss .ss-b{flex:0 0 auto;font-size:10.5px;font-weight:800;letter-spacing:.08em;padding:4px 8px;border-radius:999px;text-transform:uppercase}'+
'#tvlss .ss-vip{background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#1b2f45}'+
'#tvlss .ss-gn{background:#e3f4ef;color:#0f866c}'+
'#tvlss .ss-all{display:block;padding:12px 16px;border-top:1px solid #e3e9f0;background:#f7f9fc;font-size:14px;font-weight:800;color:#0a6fb5;text-decoration:none!important}'+
'#tvlss .ss-none{margin:0;padding:14px 16px;font-size:14px;color:#5b6b7d}'+
'@media (max-width:600px){#tvlss a.ss-r{padding:9px 12px}#tvlss .ss-n{font-size:15px}#tvlss .ss-b{display:none}}';
function init(){
  var inp=document.querySelector('.search_box input[name=q]')||document.querySelector('form[action*="search_results"] input[name=q]');
  if(!inp||inp.getAttribute('data-ss'))return false;
  /* retire BD's alphabetical 3-per-group suggest dropdown on this box */
  var fresh=inp.cloneNode(true);fresh.classList.remove('large-autosuggest-input');fresh.setAttribute('autocomplete','off');fresh.setAttribute('data-ss','1');inp.parentNode.replaceChild(fresh,inp);inp=fresh;
  var form=inp.form,host=inp.parentNode;if(getComputedStyle(host).position==='static')host.style.position='relative';
  var st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st);
  var box=document.createElement('div');box.id='tvlss';box.hidden=true;box.setAttribute('role','listbox');host.appendChild(box);
  var sel=-1,items=[],tmr;
  function render(){var q=inp.value.trim();if(q.length<2){box.hidden=true;return}
    load().then(function(){var res=search(q);items=res;sel=-1;
      var h='<p class="ss-h">Best matches in Three Village</p>';
      if(!res.length)h+='<p class="ss-none">No quick match. Press Enter to search everything.</p>';
      res.forEach(function(x,i){var m=x.r.m,ini=(m.n||'?').replace(/^the\s+/i,'').charAt(0).toUpperCase(),meta=[m.c,m.t].filter(Boolean).join(' \u00b7 ');
        h+='<a class="ss-r" role="option" href="'+esc(m.u)+'" data-i="'+i+'">'+(m.l?'<span class="ss-l" style="background-image:url(\''+esc(m.l)+'\')"></span>':'<span class="ss-l ss-ini">'+esc(ini)+'</span>')+
          '<span class="ss-t"><span class="ss-n">'+hl(m.n,q)+'</span><span class="ss-m">'+esc(meta)+'</span></span>'+(m.p==='vip'?'<span class="ss-b ss-vip">&#11088; VIP</span>':m.p==='noticed'?'<span class="ss-b ss-gn">Featured</span>':'')+'</a>'});
      h+='<a class="ss-all" href="/search_results?q='+encodeURIComponent(q)+'">See all results for &ldquo;'+esc(q)+'&rdquo; &rarr;</a>';
      box.innerHTML=h;box.hidden=false})}
  inp.addEventListener('focus',load);
  inp.addEventListener('input',function(){clearTimeout(tmr);tmr=setTimeout(render,90)});
  inp.addEventListener('keydown',function(e){var rows=box.querySelectorAll('a.ss-r');if(box.hidden||!rows.length)return;
    if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();sel=(sel+(e.key==='ArrowDown'?1:-1)+rows.length)%rows.length;[].forEach.call(rows,function(r,i){r.classList.toggle('on',i===sel)})}
    else if(e.key==='Enter'&&sel>-1){e.preventDefault();rows[sel].click();location.href=rows[sel].href}
    else if(e.key==='Escape'){box.hidden=true}});
  box.addEventListener('click',function(e){var a=e.target.closest('a.ss-r');if(a){var x=items[+a.getAttribute('data-i')];if(x)track('smart_search_click',{search_term:inp.value.trim(),biz:x.r.m.n,rank:+a.getAttribute('data-i')+1})}
    else if(e.target.closest('.ss-all'))track('smart_search_all',{search_term:inp.value.trim()})});
  document.addEventListener('click',function(e){if(!host.contains(e.target))box.hidden=true});
  if(form)form.addEventListener('submit',function(){track('smart_search_submit',{search_term:inp.value.trim()})});
  return true}
var n=0,t=setInterval(function(){n++;if(init()||n>40)clearInterval(t)},250);
})();
