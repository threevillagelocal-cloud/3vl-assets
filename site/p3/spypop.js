/* 3VL Culper Spy Day popup (event promo, 2026). Every visitor, website + app, after a few seconds, at most once per day.
   Links to the Spy Day guide. Turns itself OFF after Saturday 10/3/2026 11:59 PM ET, even if the script tag is still in widget 13.
   Preview anywhere with ?spypop=1 (ignores the date, the once-a-day limit and the skipped pages). */
(function(){
'use strict';
var me=document.currentScript||document.querySelector('script[src*="spypop.js"]');
var BASE=me?me.src.replace(/site\/p3\/spypop\.js.*$/,''):'';
var FORCE=/[?&]spypop=1/.test(location.search);
var END=Date.UTC(2026,9,4,4,0,0); /* Sun 10/4/2026 12:00 AM ET (EDT = UTC-4) */
var URL='/blog/the-ultimate-culper-spy-day-blueprint-setaukets-spy-ring-weekend-oct-3';
var IMG=BASE+'posts/spyday-2026/spyday-share-v2-1200.jpg';
var DELAY=4000;
var SKIP=/\/(account|login|checkout|member-match|join|promotion|getmatched|register|claim|admin)|culper-spy-day/i;
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function today(){var d=new Date();return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate()}
function track(n,p){try{if(window.gtag)window.gtag('event',n,p||{})}catch(e){}}

var CSS='#tvlspy{position:fixed;inset:0;z-index:2147483001;display:flex;align-items:center;justify-content:center;padding:18px;background:rgba(10,18,30,.66);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);opacity:0;transition:opacity .35s}'+
'#tvlspy.on{opacity:1}'+
'#tvlspy *{box-sizing:border-box;word-break:normal!important;overflow-wrap:normal!important;-webkit-hyphens:none!important;hyphens:none!important}'+
'#tvlspy .sp-card{position:relative;width:100%;max-width:440px;max-height:calc(100vh - 36px);overflow:auto;background:#12202f;border-radius:24px;box-shadow:0 30px 70px rgba(0,0,0,.5);transform:translateY(24px) scale(.96);transition:transform .45s cubic-bezier(.2,.9,.3,1.2);font-family:inherit}'+
'#tvlspy.on .sp-card{transform:none}'+
'#tvlspy .sp-x{position:absolute;top:10px;right:10px;width:46px;height:46px;border-radius:50%;border:1px solid rgba(255,255,255,.65);background:rgba(10,18,30,.45);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);color:#fff;font-size:28px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;box-shadow:0 6px 16px rgba(0,0,0,.3);z-index:2}'+
'#tvlspy .sp-img{display:block}'+
'#tvlspy .sp-img img{display:block;width:100%;height:auto;aspect-ratio:1200/630;object-fit:cover}'+
'#tvlspy .sp-body{padding:16px 20px 18px}'+
'#tvlspy .sp-pill{display:inline-block;padding:6px 13px;border-radius:999px;background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#1b2f45;font-size:13px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}'+
'#tvlspy .sp-h{margin:10px 0 4px!important;color:#fff;font-size:26px;line-height:1.12;font-weight:800}'+
'#tvlspy .sp-sub{margin:0 0 14px!important;color:#dfe8f2;font-size:16px;line-height:1.4;font-weight:600}'+
'#tvlspy .sp-go{display:flex;align-items:center;justify-content:center;height:52px;border-radius:14px;background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#1b2f45!important;font-size:17px;font-weight:800;text-decoration:none!important;box-shadow:0 8px 18px rgba(255,197,61,.3)}'+
'#tvlspy .sp-later{display:block;width:100%;margin:8px 0 0;padding:10px;border:0;background:none;color:#aebdcc;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit}';

function show(){
  if(document.getElementById('tvlspy'))return;
  var st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st);
  var w=document.createElement('div');w.id='tvlspy';w.setAttribute('role','dialog');w.setAttribute('aria-modal','true');w.setAttribute('aria-label','Culper Spy Day guide');
  w.innerHTML='<div class="sp-card"><button type="button" class="sp-x" aria-label="Close">&times;</button>'+
    '<a class="sp-img" href="'+URL+'"><img src="'+IMG+'" alt="Culper Spy Day, Saturday October 3"></a>'+
    '<div class="sp-body"><span class="sp-pill">&#128373;&#65039; This Saturday &middot; Oct 3</span>'+
    '<p class="sp-h">Culper Spy Day is here!</p>'+
    '<p class="sp-sub">Setauket&rsquo;s biggest day of the year. Our guide has the schedule, trolley, food and spy secrets.</p>'+
    '<a class="sp-go" href="'+URL+'">Read the Spy Day Guide &rarr;</a>'+
    '<button type="button" class="sp-later">Maybe later</button></div></div>';
  document.body.appendChild(w);
  requestAnimationFrame(function(){requestAnimationFrame(function(){w.classList.add('on')})});
  if(!FORCE)ls('tvl_spy_day',today());
  var app=document.documentElement.classList.contains('tvl-inapp')?'app':'web';
  track('spy_pop_show',{src:app});
  function close(how){if(!w.parentNode)return;track('spy_pop_close',{how:how,src:app});w.classList.remove('on');setTimeout(function(){w.remove()},350);document.removeEventListener('keydown',key)}
  function key(e){if(e.key==='Escape')close('esc')}
  w.querySelector('.sp-x').onclick=function(){close('x')};
  w.querySelector('.sp-later').onclick=function(){close('later')};
  w.addEventListener('click',function(e){if(e.target===w)close('backdrop')});
  document.addEventListener('keydown',key);
  [].forEach.call(w.querySelectorAll('.sp-img,.sp-go'),function(a){a.addEventListener('click',function(){track('spy_pop_click',{src:app})})});
}

function go(){
  if(!FORCE){
    if(Date.now()>=END)return;
    if(SKIP.test(location.pathname))return;
    if(ls('tvl_spy_day')===today())return;
  }
  setTimeout(show,FORCE?300:DELAY);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
