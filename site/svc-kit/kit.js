;(function(){
var root=document.getElementById('tvs');if(!root||root.getAttribute('data-tvx'))return;root.setAttribute('data-tvx','1');
var SVC=root.getAttribute('data-svc')||'';
var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
window.tvxRM=RM;
function ga(n,p){try{if(window.gtag){p=p||{};p.service=SVC;gtag('event',n,p);}}catch(x){}}
window.tvxGA=ga;
if(RM){[].forEach.call(root.querySelectorAll('[data-n]'),function(el){el.removeAttribute('data-n');});}
/* infinite animations run only while their block is on screen */
var runs=[].slice.call(root.querySelectorAll('[data-run]'));
if('IntersectionObserver' in window){var ro=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('tvx-run',e.isIntersecting);var f=e.target.__tvxRun;if(f)f(e.isIntersecting);});},{rootMargin:'80px 0px'});runs.forEach(function(r){ro.observe(r);});}
else runs.forEach(function(r){r.classList.add('tvx-run');});
window.tvxOnRun=function(el,f){el.__tvxRun=f;if(el.classList.contains('tvx-run'))f(true);};
/* tabs: [data-tabs] > .tvx-tab[data-tab] + [data-panel]; optional data-auto="ms" rotates until the visitor picks one */
[].forEach.call(root.querySelectorAll('[data-tabs]'),function(box){
 var tabs=[].slice.call(box.querySelectorAll('.tvx-tab[data-tab]')),panels=[].slice.call(box.querySelectorAll('[data-panel]'));
 if(!tabs.length)return;var auto=+box.getAttribute('data-auto')||0,user=false,vis=false,iv=null;
 var list=tabs[0].parentNode;list.setAttribute('role','tablist');
 tabs.forEach(function(t,i){t.setAttribute('role','tab');t.setAttribute('type','button');t.id=t.id||('tvx-t-'+Math.random().toString(36).slice(2,8));});
 function set(k,why){tabs.forEach(function(t){var on=t.getAttribute('data-tab')===k;t.classList.toggle('on',on);t.setAttribute('aria-selected',on?'true':'false');t.tabIndex=on?0:-1;});
  panels.forEach(function(p){var on=p.getAttribute('data-panel')===k;if(on)p.removeAttribute('hidden');else p.setAttribute('hidden','');});
  box.setAttribute('data-cur',k);var ev;try{ev=new CustomEvent('tvxtab',{detail:{key:k,why:why}});}catch(x){ev=document.createEvent('CustomEvent');ev.initCustomEvent('tvxtab',false,false,{key:k,why:why});}box.dispatchEvent(ev);}
 tabs.forEach(function(t,i){t.addEventListener('click',function(){user=true;stop();set(t.getAttribute('data-tab'),'click');ga('svc_page_tab',{tab:t.getAttribute('data-tab')});});
  t.addEventListener('keydown',function(e){var k=e.key,j=-1;if(k==='ArrowRight')j=(i+1)%tabs.length;else if(k==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;if(j>-1){e.preventDefault();tabs[j].focus();tabs[j].click();}});});
 var cur=(box.querySelector('.tvx-tab.on')||tabs[0]).getAttribute('data-tab');set(cur,'init');
 function next(){var i=0;tabs.forEach(function(t,n){if(t.classList.contains('on'))i=n;});set(tabs[(i+1)%tabs.length].getAttribute('data-tab'),'auto');}
 function stop(){if(iv){clearInterval(iv);iv=null;}}
 function start(){if(!auto||user||RM||iv||!vis)return;iv=setInterval(next,auto);}
 if(auto&&'IntersectionObserver' in window){new IntersectionObserver(function(es){vis=es[0].isIntersecting;if(vis)start();else stop();},{threshold:.25}).observe(box);
  box.addEventListener('pointerenter',function(){stop();});box.addEventListener('pointerleave',function(){start();});}
});
/* floating "Get my free plan" button: hidden over the hero and the form */
var st=root.querySelector('.tvs-sticky'),hero=document.getElementById('tvx-hero'),bk=document.getElementById('tvs-book');
if(st&&hero&&'IntersectionObserver' in window){var hv=true,bv=false;function upd(){st.classList.toggle('on',!hv&&!bv);st.style.opacity=(!hv&&!bv)?'':'0';st.style.pointerEvents=(!hv&&!bv)?'':'none';}
 new IntersectionObserver(function(es){hv=es[0].isIntersecting;upd();}).observe(hero);if(bk)new IntersectionObserver(function(es){bv=es[0].isIntersecting;upd();}).observe(bk);upd();}
/* section links: smooth scroll under the pinned bar */
root.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#tvp-"]');if(!a)return;var t=document.getElementById(a.getAttribute('href').slice(1));if(!t)return;e.preventDefault();t.scrollIntoView({behavior:RM?'auto':'smooth',block:'start'});ga('svc_page_nav',{to:t.id});});
/* track across-links to other services */
root.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.tvx-rel-c,.tvx-crumbs a');if(a)ga('svc_page_related',{to:a.getAttribute('href')});},true);
})();
