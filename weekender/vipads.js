/* 3VL VIP sidebar rotator. Drop <script src=".../weekender/vipads.js" defer></script> into any BD blog post.
   It finds the post sidebar (.post-detail-sidebar) and inserts a rotating VIP banner above Related Posts. */
(function(){
'use strict';
var me=document.currentScript||document.querySelector('script[src*="vipads.js"]');
var BASE=me?me.src.replace(/vipads\.js.*$/,''):'';
var PLACE=(me&&me.getAttribute('data-placement'))||'blog_sidebar';
function track(n,p){try{if(window.gtag)window.gtag('event',n,p)}catch(e){}}
var css='#vipx{background:#fff;border:1px solid #ebeef0;border-radius:12px;padding:14px;margin:0 0 20px;box-shadow:0 1px 3px rgba(0,0,0,.04)}'+
'#vipx .vipx-h{display:flex;align-items:center;gap:8px;margin:0 0 12px;font-size:18px;font-weight:700;color:#1b2f45}'+
'#vipx .vipx-h span{font-size:11px;font-weight:700;letter-spacing:.1em;background:#f0ad4e;color:#1b2f45;padding:3px 7px;border-radius:6px}'+
'#vipx .vipx-rot{position:relative;border-radius:12px;overflow:hidden;background:#1b2f45}'+
'#vipx .vipx-rot:before{content:"";display:block;padding-top:83.333%}'+
'#vipx .vipx-ad{position:absolute;inset:0;opacity:0;transition:opacity .9s ease;pointer-events:none}'+
'#vipx .vipx-ad.on{opacity:1;pointer-events:auto}'+
'#vipx .vipx-ad a{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;overflow:hidden}'+
'#vipx .vipx-ad a:before{content:"";position:absolute;inset:-20px;background:var(--b) center/cover;filter:blur(16px);opacity:.55}'+
'#vipx .vipx-ad img{position:relative!important;width:100%!important;height:auto!important;max-height:100%;object-fit:contain;transform:scale(1.01);transition:transform 6.5s ease-out!important;border-radius:0!important}'+
'#vipx .vipx-ad.on img{transform:scale(1.06)}'+
'#vipx .vipx-bar{position:absolute;left:0;right:0;bottom:0;height:3px;background:rgba(255,255,255,.2);z-index:2}#vipx .vipx-bar i{display:block;height:100%;width:0;background:#f0ad4e}'+
'#vipx .vipx-btns{display:flex;gap:8px;margin-top:10px}'+
'#vipx .vipx-btns a{flex:1;display:inline-flex;align-items:center;justify-content:center;height:40px;border-radius:10px;font-weight:700;font-size:14px;text-decoration:none!important;white-space:nowrap}'+
'#vipx .vipx-call{background:#006fbb;color:#fff!important}#vipx .vipx-view{background:#eef4fa;color:#1b2f45!important;border:1px solid #d6e3f0}'+
'#vipx .vipx-dots{display:flex;justify-content:center;gap:4px;margin-top:10px}#vipx .vipx-dots b{width:6px;height:6px;border-radius:6px;background:#cfd8e3;transition:width .3s,background .3s}#vipx .vipx-dots b.on{width:16px;background:#006fbb}'+
'#vipx .vipx-foot{display:block;text-align:center;margin-top:8px;font-size:12px;font-weight:700;color:#006fbb}';
/* Shuffle so the same business or competitors (same "group") are at least GAP+1 slots apart, including when the loop wraps. */
function spread(arr,key,gap){var best=arr.slice();
  for(var tries=0;tries<200;tries++){var pool=arr.slice(),out=[];
    for(var i=pool.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=pool[i];pool[i]=pool[j];pool[j]=t}
    while(pool.length){var pick=-1;for(var k=0;k<pool.length;k++){var ok=true;for(var b=1;b<=gap&&b<=out.length;b++){if(key(out[out.length-b])===key(pool[k])){ok=false;break}}if(ok){pick=k;break}}
      if(pick<0)break;out.push(pool.splice(pick,1)[0])}
    if(out.length===arr.length){var wrapOk=true,n=out.length;for(var a=0;a<n&&wrapOk;a++)for(var d=1;d<=gap;d++){if(n>gap*2&&key(out[a])===key(out[(a+d)%n])){wrapOk=false;break}}if(wrapOk)return out;best=out}}
  return best}
function build(list,side){
  list=spread(list,function(v){return v.group||v.id},3);
  var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
  var box=document.createElement('div');box.id='vipx';box.className='module';
  var h='<p class="vipx-h"><span>VIP</span>Local businesses we love</p><div class="vipx-rot">';
  list.forEach(function(v,i){h+='<div class="vipx-ad'+(i?'':' on')+'" data-vip="'+v.name+'"><a href="'+v.url+'" data-vip="'+v.name+'" style="--b:url('+BASE+v.img+')"><img src="'+BASE+v.img+'" alt="'+v.name+' ad" width="'+v.w+'" height="'+v.h+'" loading="'+(i?'lazy':'eager')+'"></a></div>'});
  h+='<div class="vipx-bar"><i></i></div></div><div class="vipx-btns"><a class="vipx-call" href="#">&#128222; Call</a><a class="vipx-view" href="#">View on 3VL &rarr;</a></div><div class="vipx-dots">';
  list.forEach(function(v,i){h+='<b'+(i?'':' class="on"')+'></b>'});
  h+='</div><a class="vipx-foot" href="https://www.threevillagelocal.com/join">Advertise here &rarr;</a>';
  box.innerHTML=h;side.insertBefore(box,side.firstChild);
  var ads=box.querySelectorAll('.vipx-ad'),dots=box.querySelectorAll('.vipx-dots b'),bar=box.querySelector('.vipx-bar i'),call=box.querySelector('.vipx-call'),view=box.querySelector('.vipx-view');
  var idx=0,dur=6500,t0=0,paused=false,seen={};
  function show(n){idx=(n+list.length)%list.length;for(var k=0;k<ads.length;k++){ads[k].className='vipx-ad'+(k===idx?' on':'');dots[k].className=k===idx?'on':''}
    var v=list[idx];call.href='tel:'+v.phone;call.setAttribute('data-vip',v.name);view.href=v.url;view.setAttribute('data-vip',v.name);t0=performance.now();
    if(!seen[v.name]){var r=box.getBoundingClientRect();if(r.top<innerHeight&&r.bottom>0){seen[v.name]=1;track('vip_ad_view',{vip:v.name,placement:PLACE})}}}
  function loop(ts){if(!paused){var p=(ts-t0)/dur;bar.style.width=Math.min(100,p*100)+'%';if(p>=1)show(idx+1)}else t0=ts-(parseFloat(bar.style.width)||0)/100*dur;requestAnimationFrame(loop)}
  box.addEventListener('mouseenter',function(){paused=true});box.addEventListener('mouseleave',function(){paused=false});
  box.addEventListener('click',function(e){var a=e.target.closest('a[data-vip]');if(a)track('vip_ad_click',{vip:a.getAttribute('data-vip'),placement:PLACE,link:a.className||'banner'})});
  show(0);requestAnimationFrame(loop)}
function go(){var side=document.querySelector('.post-detail-sidebar');if(!side||document.getElementById('vipx'))return;
  fetch(BASE+'banners.json').then(function(r){return r.json()}).then(function(list){if(list&&list.length)build(list,side)}).catch(function(){})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
