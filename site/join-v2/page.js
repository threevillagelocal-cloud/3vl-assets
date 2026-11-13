(function(){
var root=document.getElementById('jv');if(!root||root.getAttribute('data-on'))return;root.setAttribute('data-on','1');
var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function ga(n,p){try{if(window.gtag)gtag('event',n,p||{});}catch(x){}}
function $$(s,r){return [].slice.call((r||document).querySelectorAll(s));}

/* top offset = bottom of BD's fixed/sticky header (if any) */
function topOff(){var m=0;try{var els=document.elementsFromPoint(Math.round(window.innerWidth/2),2);for(var i=0;i<els.length;i++){var e=els[i];while(e&&e!==document.body&&e!==document.documentElement){var ps=getComputedStyle(e).position;if((ps==='fixed'||ps==='sticky')&&!(root.contains(e))&&e.id!=='jvm'){var b=e.getBoundingClientRect().bottom;if(b>m&&b<window.innerHeight*0.5)m=b;}e=e.parentElement;}}}catch(x){}return m;}

/* count up */
function countUp(el){var n=+el.getAttribute('data-n');if(!n||RM||el.__c)return;el.__c=1;var t0=null,d=n>999?1400:900;
function f(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/d);k=1-Math.pow(1-k,3);el.textContent=Math.round(n*k).toLocaleString('en-US');if(k<1)requestAnimationFrame(f);}
el.textContent='0';requestAnimationFrame(f);}

/* reveal mini dashboard on the page */
var big=root.querySelector('.jv-n-big');
if(big){if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){big.classList.add('jv-run');$$('[data-n]',big).forEach(countUp);io.disconnect();}});},{threshold:.3});io.observe(big);}else big.classList.add('jv-run');}

/* in-page anchors: account for the fixed header */
$$('a[href^="#jv-"]',root).forEach(function(a){a.addEventListener('click',function(ev){var t=document.getElementById(a.getAttribute('href').slice(1));if(!t)return;ev.preventDefault();
var y=t.getBoundingClientRect().top+window.pageYOffset-topOff()-12;window.scrollTo({top:y,behavior:RM?'auto':'smooth'});});});

/* plan clicks */
document.addEventListener('click',function(ev){var a=ev.target.closest&&ev.target.closest('[data-jv-plan]');if(a&&a.tagName==='A')ga('join_plan_click',{plan:a.getAttribute('data-jv-plan'),where:a.closest('#jvm')?'popup':'page'});},true);

/* ---------- comparison: pinned plan header ---------- */
var wrap=document.getElementById('jv-tblwrap'),tbl=document.getElementById('jv-tbl'),pin=document.getElementById('jv-pin');
if(wrap&&tbl&&pin){
 var pinSpans=$$('span',pin),ref=null,ticking=false,off=0,offT=0;
 function refCells(){var r=tbl.querySelector('tbody tr:not(.jv-grp)');return r?$$('td',r):[];}
 function place(){ticking=false;var now=Date.now();if(now-offT>800){off=topOff();offT=now;}
  var tr=tbl.getBoundingClientRect(),h=pin.offsetHeight||58,show=tr.top<off+4&&tr.bottom>off+h+90;
  pin.classList.toggle('on',show);if(!show)return;
  var w=wrap.getBoundingClientRect();pin.style.top=off+'px';pin.style.left=w.left+'px';pin.style.width=w.width+'px';
  var cells=refCells();pinSpans.forEach(function(s,i){var c=cells[i];if(!c)return;var r=c.getBoundingClientRect();s.style.left=(r.left-w.left)+'px';s.style.width=r.width+'px';});}
 function req(){if(!ticking){ticking=true;requestAnimationFrame(place);}}
 window.addEventListener('scroll',req,{passive:true});window.addEventListener('resize',function(){offT=0;req();});req();
}

/* ---------- modal ---------- */
var M=null,opener=null,cur=null,spy=null,chatT=[];
function build(){
 M=document.createElement('div');M.id='jvm';M.setAttribute('role','dialog');M.setAttribute('aria-modal','true');M.setAttribute('aria-labelledby','jvm-t');
 M.innerHTML='<div class="jvm-back" data-x></div><div class="jvm-panel"><header class="jvm-top"><span class="jvm-grab" aria-hidden="true"></span><div><p class="jvm-tag"></p><h2 id="jvm-t"></h2></div><span class="jvm-pr"></span><button type="button" class="jvm-x" data-x aria-label="Close">'+
 '<svg class="jv-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg></button></header><div class="jvm-slot"></div></div>';
 document.body.appendChild(M);
 M.addEventListener('click',function(ev){var t=ev.target;
  if(t.closest('[data-x]')){close();return;}
  var tab=t.closest('.jvm-tab');if(tab){go(tab.getAttribute('data-go'),true);return;}
  var o=t.closest('[data-jv-open]');if(o){var k=o.getAttribute('data-jv-open');ga('join_popup_upgrade',{from:cur,to:k});open(k,null,opener);return;}
  var chip=t.closest('.jvd-chips button');if(chip){var f=chip.getAttribute('data-f'),box=chip.closest('.jvd');$$('.jvd-chips button',box).forEach(function(b){var on=b===chip;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false');});
   $$('.jvd-list li',box).forEach(function(li){li.classList.toggle('jvd-hide',f!=='all'&&li.getAttribute('data-f')!==f);});return;}
  if(t.closest('.jv-chat-re')){runChat(true);}
 });
 M.addEventListener('keydown',function(ev){
  if(ev.key==='Escape'){ev.preventDefault();close();return;}
  if(ev.key!=='Tab')return;var f=$$('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"]),video[controls],summary',M).filter(function(e){return e.offsetParent!==null||e===document.activeElement;});
  if(!f.length)return;var a=f[0],z=f[f.length-1];
  if(ev.shiftKey&&document.activeElement===a){ev.preventDefault();z.focus();}else if(!ev.shiftKey&&document.activeElement===z){ev.preventDefault();a.focus();}
 });
 /* swipe the header down to close (phones) */
 var top=M.querySelector('.jvm-top'),panel=M.querySelector('.jvm-panel'),y0=null,dy=0;
 top.addEventListener('touchstart',function(e){if(e.target.closest('button'))return;y0=e.touches[0].clientY;dy=0;panel.style.transition='none';},{passive:true});
 top.addEventListener('touchmove',function(e){if(y0===null)return;dy=Math.max(0,e.touches[0].clientY-y0);panel.style.transform='translateY('+dy+'px)';},{passive:true});
 top.addEventListener('touchend',function(){if(y0===null)return;panel.style.transition='';panel.style.transform='';y0=null;if(dy>90)close();});
}
function setTab(id){$$('.jvm-tab',M).forEach(function(b){var on=b.getAttribute('data-go')===id;b.classList.toggle('on',on);if(on){b.setAttribute('aria-current','true');var n=b.parentNode;var l=b.offsetLeft-n.clientWidth/2+b.offsetWidth/2;n.scrollTo({left:l,behavior:RM?'auto':'smooth'});}else b.removeAttribute('aria-current');});}
function go(id,user){var body=M.querySelector('.jvm-body'),s=M.querySelector('#jvm-'+id);if(!body||!s)return;
 body.scrollTo({top:s.offsetTop-body.offsetTop-4,behavior:(RM||!user)?'auto':'smooth'});setTab(id);if(user)ga('join_popup_tab',{plan:cur,tab:id});}
function activate(sec){
 if(sec.__a)return;sec.__a=1;
 var d=sec.querySelector('.jvd');if(d){d.classList.add('jvd-run');$$('[data-n]',d).forEach(countUp);}
 var v=sec.querySelector('video[data-src]');if(v){v.src=v.getAttribute('data-src');v.removeAttribute('data-src');if(!RM){var p=v.play();if(p&&p.catch)p.catch(function(){});}}
 if(sec.querySelector('[data-chat]'))runChat(false);
}
function runChat(again){var b=M.querySelector('[data-chat]');if(!b)return;chatT.forEach(clearTimeout);chatT=[];
 var ps=$$('p',b);$$('.typing',b).forEach(function(t){t.remove();});
 if(RM){ps.forEach(function(p){p.classList.add('in');});return;}
 ps.forEach(function(p){p.classList.remove('in');});var t=again?200:500;
 ps.forEach(function(p){var bot=p.classList.contains('bot');
  if(bot){chatT.push(setTimeout(function(){var ty=document.createElement('span');ty.className='typing';ty.innerHTML='<u></u><u></u><u></u>';b.insertBefore(ty,p);},t));t+=1100;
   chatT.push(setTimeout(function(){var ty=b.querySelector('.typing');if(ty)ty.remove();p.classList.add('in');},t));}
  else chatT.push(setTimeout(function(){p.classList.add('in');},t));
  t+=bot?900:1000;});
}
function open(k,sec,from){
 var tpl=document.getElementById('jvt-'+k);if(!tpl)return;if(!M)build();
 if(spy){spy.disconnect();spy=null;}chatT.forEach(clearTimeout);chatT=[];
 var first=!M.classList.contains('on');if(first)opener=from||document.activeElement;
 cur=k;M.setAttribute('data-plan',k);
 M.querySelector('#jvm-t').textContent=tpl.getAttribute('data-title');
 M.querySelector('.jvm-tag').textContent=tpl.getAttribute('data-tag');
 M.querySelector('.jvm-pr').textContent=tpl.getAttribute('data-price');
 var slot=M.querySelector('.jvm-slot');slot.innerHTML='';slot.appendChild(document.importNode(tpl.content,true));
 slot.style.display='contents';
 if(window.jvClaim)window.jvClaim(M);
 var body=M.querySelector('.jvm-body'),secs=$$('.jvm-sec',body);
 if('IntersectionObserver' in window){spy=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){activate(e.target);var id=e.target.getAttribute('data-sec');if(id&&id!=='go'&&e.intersectionRatio>0)setTab(id);}});},{root:body,rootMargin:'-20% 0px -55% 0px',threshold:[0,.01]});secs.forEach(function(s){spy.observe(s);});
  var io2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)activate(e.target);});},{root:body,threshold:.05});secs.forEach(function(s){io2.observe(s);});}
 else secs.forEach(activate);
 if(first){document.documentElement.classList.add('jvm-lock');M.classList.add('on');requestAnimationFrame(function(){requestAnimationFrame(function(){M.classList.add('show');});});}
 var tabs=$$('.jvm-tab',M);setTab(sec||(tabs[0]&&tabs[0].getAttribute('data-go')));
 if(sec)setTimeout(function(){go(sec,false);},first?60:0);else body.scrollTop=0;
 setTimeout(function(){var x=M.querySelector('.jvm-x');if(x)x.focus({preventScroll:true});},first?80:0);
 ga('join_popup_open',{plan:k,section:sec||'top'});
 try{history.pushState({jvm:1},'',location.href.split('#')[0]+'#plan-'+k);}catch(x){}
}
function close(fromPop){if(!M||!M.classList.contains('on'))return;M.classList.remove('show');chatT.forEach(clearTimeout);chatT=[];
 var v=M.querySelector('video');if(v)try{v.pause();}catch(x){}
 setTimeout(function(){M.classList.remove('on');M.querySelector('.jvm-slot').innerHTML='';document.documentElement.classList.remove('jvm-lock');if(spy){spy.disconnect();spy=null;}
  if(opener&&opener.focus)try{opener.focus({preventScroll:true});}catch(x){}},RM?0:260);
 if(!fromPop)try{if(history.state&&history.state.jvm)history.back();}catch(x){}}
window.addEventListener('popstate',function(){if(M&&M.classList.contains('on'))close(true);});
root.addEventListener('click',function(ev){var b=ev.target.closest('[data-jv-open]');if(!b||!root.contains(b))return;ev.preventDefault();open(b.getAttribute('data-jv-open'),b.getAttribute('data-jv-go'),b);});
/* deep link: /preview-join#plan-vip */
var h=location.hash;if(h.indexOf('#plan-')===0){var k=h.slice(6);if(document.getElementById('jvt-'+k))setTimeout(function(){try{history.replaceState(null,'',location.href.split('#')[0]);}catch(x){}open(k,null,null);},300);}
window.jvOpen=open;window.jvClose=close;
})();
