/* 3VL app popup: "Your only ad today". App users only (html.tvl-inapp, set by widget 13), after ~45s of use
   (counted across pages), at most once per day per person. Shows one VIP (rotates daily) and links to their listing.
   Preview anywhere with ?tvlpop=1 */
(function(){
'use strict';
var me=document.currentScript||document.querySelector('script[src*="apppop.js"]');
var BASE=me?me.src.replace(/site\/p3\/apppop\.js.*$/,''):'';
var FORCE=/[?&]tvlpop=1/.test(location.search),SECS=45;
var SKIP=/\/(account|login|checkout|member-match|join|promotion|getmatched|register|claim|admin)/i;
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function today(){var d=new Date();return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate()}
function track(n,p){try{if(window.gtag)window.gtag('event',n,p)}catch(e){}}
function esc(s){return String(s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}

var CSS='#tvlpop{position:fixed;inset:0;z-index:2147483000;display:flex;align-items:center;justify-content:center;padding:18px;background:rgba(10,18,30,.62);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);opacity:0;transition:opacity .35s}'+
'#tvlpop.on{opacity:1}'+
'#tvlpop .tp-card{position:relative;width:100%;max-width:400px;background:#fff;border-radius:24px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.45);transform:translateY(24px) scale(.96);transition:transform .45s cubic-bezier(.2,.9,.3,1.2);font-family:inherit}'+
'#tvlpop.on .tp-card{transform:none}'+
'#tvlpop .tp-top{padding:16px 64px 12px 18px;background:linear-gradient(135deg,#1b2f45,#205081)}'+
'#tvlpop .tp-pill{display:inline-flex;align-items:center;gap:7px;padding:5px 12px;border-radius:999px;background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#1b2f45;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;box-shadow:0 4px 12px rgba(255,197,61,.35)}'+
'#tvlpop .tp-sub{margin:9px 0 0!important;color:#dfe8f2;font-size:14.5px;line-height:1.4;font-weight:600}'+
'#tvlpop .tp-x{position:absolute;top:12px;right:12px;width:46px;height:46px;border-radius:50%;border:1px solid rgba(255,255,255,.6);background:rgba(255,255,255,.22);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);color:#fff;font-size:28px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;box-shadow:0 6px 16px rgba(0,0,0,.25);z-index:2}'+
'#tvlpop .tp-img{display:block;position:relative;background:#eef3f8}'+
'#tvlpop .tp-img img{display:block;width:100%;height:auto;aspect-ratio:6/5;object-fit:cover}'+
'#tvlpop .tp-body{padding:14px 18px 16px}'+
'#tvlpop .tp-k{margin:0!important;font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#0a6fb5}'+
'#tvlpop .tp-name{margin:3px 0 12px!important;font-size:21px;line-height:1.15;font-weight:800;color:#1b2f45;word-break:normal;overflow-wrap:normal}'+
'#tvlpop .tp-btns{display:flex;gap:8px}'+
'#tvlpop .tp-go,#tvlpop .tp-call{flex:1;display:flex;align-items:center;justify-content:center;gap:6px;height:48px;border-radius:14px;font-size:16px;font-weight:800;text-decoration:none!important}'+
'#tvlpop .tp-go{background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#1b2f45!important;box-shadow:0 8px 18px rgba(255,197,61,.35)}'+
'#tvlpop .tp-call{flex:0 0 36%;background:#eef3f8;color:#1b2f45!important}'+
'#tvlpop .tp-foot{margin:12px 0 0!important;text-align:center;font-size:12.5px;color:#6b7a8b}';

function pick(list){var groups={},keys=[];list.forEach(function(b){var g=b.group||b.id;if(!groups[g]){groups[g]=[];keys.push(g)}groups[g].push(b)});
  var d=new Date(),n=Math.floor(new Date(d.getFullYear(),d.getMonth(),d.getDate())/864e5);
  var g=groups[keys[n%keys.length]];return g[n%g.length]}

function show(b){
  if(document.getElementById('tvlpop'))return;
  var st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st);
  var tel=String(b.phone||'').replace(/\D/g,'');
  var w=document.createElement('div');w.id='tvlpop';w.setAttribute('role','dialog');w.setAttribute('aria-modal','true');w.setAttribute('aria-label','Local business spotlight');
  w.innerHTML='<div class="tp-card"><button type="button" class="tp-x" aria-label="Close">&times;</button>'+
    '<div class="tp-top"><span class="tp-pill">&#9728;&#65039; Your only ad today</span>'+
    '<p class="tp-sub">One great local business, once a day. Close it and you&rsquo;re ad-free until tomorrow. Promise.</p></div>'+
    '<a class="tp-img" href="'+esc(b.url)+'"><img src="'+esc(BASE+'weekender/'+b.img)+'" alt="'+esc(b.name)+'"></a>'+
    '<div class="tp-body"><p class="tp-k">Today&rsquo;s Local Spotlight</p><p class="tp-name">'+esc(b.name)+'</p>'+
    '<div class="tp-btns"><a class="tp-go" href="'+esc(b.url)+'">Check them out &rarr;</a>'+(tel?'<a class="tp-call" href="tel:'+tel+'">&#128222; Call</a>':'')+'</div>'+
    '<p class="tp-foot">Supporting local keeps Three Village thriving &#128153;</p></div></div>';
  document.body.appendChild(w);
  requestAnimationFrame(function(){requestAnimationFrame(function(){w.classList.add('on')})});
  ls('tvl_pop_day',today());
  var p={biz:b.name,biz_id:b.id};track('app_pop_show',p);
  function close(how){if(!w.parentNode)return;track('app_pop_close',{biz:b.name,biz_id:b.id,how:how});w.classList.remove('on');setTimeout(function(){w.remove()},350);document.removeEventListener('keydown',key)}
  function key(e){if(e.key==='Escape')close('esc')}
  w.querySelector('.tp-x').onclick=function(){close('x')};
  w.addEventListener('click',function(e){if(e.target===w)close('backdrop')});
  document.addEventListener('keydown',key);
  [].forEach.call(w.querySelectorAll('.tp-img,.tp-go'),function(a){a.addEventListener('click',function(){track('app_pop_click',{biz:b.name,biz_id:b.id,to:'listing'})})});
  var c=w.querySelector('.tp-call');if(c)c.addEventListener('click',function(){track('app_pop_click',{biz:b.name,biz_id:b.id,to:'call'})});
}

function load(){fetch(BASE+'weekender/banners.json').then(function(r){return r.json()}).then(function(l){if(l&&l.length)show(pick(l))}).catch(function(){})}

function go(){
  if(FORCE){load();return}
  if(!document.documentElement.classList.contains('tvl-inapp'))return;
  if(SKIP.test(location.pathname))return;
  if(ls('tvl_pop_day')===today())return;
  var k='tvl_pop_t_'+today(),t=+(ls(k)||0);
  var iv=setInterval(function(){if(document.hidden)return;t+=5;ls(k,t);if(t>=SECS){clearInterval(iv);if(ls('tvl_pop_day')!==today())load()}},5000);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(go,300)});else setTimeout(go,300);
})();
