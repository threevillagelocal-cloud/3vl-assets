/* 3VL login page top: replaces BD's storefront hero with the premium village photo banner (same look as Categories/Search).
   Runs only on /login. The login box itself is untouched. Loaded sitewide from widget 13. */
(function(){
'use strict';
if(!/^\/login\/?$/.test(location.pathname))return;
var me=document.currentScript||document.querySelector('script[src*="p3/login.js"]');
var BASE=me?me.src.replace(/login\.js.*$/,''):'';
var CSS='html.tvl-login .hero_section_container{display:none!important}'+
'#tvllogin{max-width:1170px;margin:18px auto 22px;padding:0 15px;box-sizing:border-box}'+
'#tvllogin *{box-sizing:border-box;word-break:normal!important;overflow-wrap:normal!important;-webkit-hyphens:none!important;hyphens:none!important}'+
'#tvllogin .lg-hero{position:relative;border-radius:22px;overflow:hidden;background:#132338 center 45%/cover no-repeat;color:#fff;box-shadow:0 16px 36px rgba(27,47,69,.22);isolation:isolate}'+
'#tvllogin .lg-hero:before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(12,22,36,.86) 0%,rgba(12,22,36,.62) 45%,rgba(12,22,36,.14) 100%)}'+
'#tvllogin .lg-in{padding:30px 34px 28px;max-width:660px}'+
'#tvllogin .lg-kick{display:inline-block;padding:6px 13px;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.3);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);font-size:13px;font-weight:800;letter-spacing:.14em;color:#fff}'+
'#tvllogin .lg-h{margin:12px 0 6px!important;padding:0!important;font-size:46px!important;line-height:1.04!important;font-weight:800!important;color:#fff!important;text-shadow:none!important}'+
'#tvllogin .lg-h em{font-style:normal;color:#ffc53d}'+
'#tvllogin .lg-sub{margin:0!important;font-size:18px;line-height:1.45;font-weight:600;color:rgba(255,255,255,.9)}'+
'#tvllogin .lg-credit{position:absolute;right:12px;bottom:8px;font-size:10px;color:rgba(255,255,255,.55)}'+
'@media (max-width:767px){#tvllogin{margin:12px auto 16px}'+
' #tvllogin .lg-hero:before{background:linear-gradient(0deg,rgba(12,22,36,.88),rgba(12,22,36,.5))}'+
' #tvllogin .lg-in{padding:24px 20px 26px}#tvllogin .lg-h{font-size:34px!important}#tvllogin .lg-sub{font-size:16px}}';
function go(){
  var hero=document.querySelector('.hero_section_container');
  if(!hero||document.getElementById('tvllogin'))return;
  var st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st);
  var w=document.createElement('div');w.id='tvllogin';
  w.innerHTML='<header class="lg-hero" style="background-image:url(\''+BASE+'img/village-hero.jpg\')"><div class="lg-in">'+
    '<span class="lg-kick">&#128272; MEMBER LOGIN</span>'+
    '<h1 class="lg-h">Welcome <em>back, neighbor</em></h1>'+
    '<p class="lg-sub">Log in to manage your business listing on Three Village Local.</p></div>'+
    '<span class="lg-credit">Photo: Iracaz, CC BY-SA 3.0</span></header>';
  hero.parentNode.insertBefore(w,hero);
  document.documentElement.classList.add('tvl-login');
  var gap=hero.nextElementSibling;if(gap&&/clearfix-lg/.test(gap.className))gap.style.display='none';
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
