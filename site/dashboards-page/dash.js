;(function(){var R=document.getElementById('tvs');if(!R||!R.classList.contains('tvd'))return;
var RM=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
function ev(n,p){try{if(window.gtag)gtag('event',n,p||{})}catch(x){}}
function fmt(v,dec){var s=dec?v.toFixed(dec):String(Math.round(v));var pr=s.split('.'),i=pr[0],o='';while(i.length>3){o=','+i.slice(-3)+o;i=i.slice(0,-3)}return i+o+(pr[1]?'.'+pr[1]:'')}
function cnt(el){var to=parseFloat(el.getAttribute('data-c')),dec=+(el.getAttribute('data-d')||0);if(RM){el.textContent=fmt(to,dec);return}
 var t0=null,dur=1300;function st(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/dur),e=1-Math.pow(1-k,3);el.textContent=fmt(to*e,dec);if(k<1)requestAnimationFrame(st)}requestAnimationFrame(st)}
function counts(scope){[].forEach.call(scope.querySelectorAll('[data-c]'),cnt)}
function seen(el,fn,margin){if(!el)return;if(!('IntersectionObserver' in window)){fn(true);return}new IntersectionObserver(function(es){fn(es[0].isIntersecting)},{rootMargin:margin||'0px'}).observe(el)}
var toastT=null;function toast(msg){var t=document.getElementById('tvd-toast');if(!t)return;t.textContent=msg;t.classList.add('on');clearTimeout(toastT);toastT=setTimeout(function(){t.classList.remove('on')},2400)}

/* 1. live demos: real dashboards in ?embed=1&tour=1 mode inside a laptop frame + a phone frame.
   Posters show first; iframes load only once the page has loaded and the showcase is near the screen,
   one business at a time (phone frame after the laptop one; phones get the phone frame only). */
var L=document.getElementById('tvd-live');
if(L){var lt=[].slice.call(L.querySelectorAll('.tvd-lt')),scr=[].slice.call(L.querySelectorAll('.tvd-scr')),cur=lt[0],go=false,near=false,started=false;
 function small(){return !!(window.matchMedia&&matchMedia('(max-width: 760px)').matches)}
 function fit(){scr.forEach(function(s){var f=s.querySelector('iframe');if(f)f.style.transform='scale('+(s.clientWidth/+s.getAttribute('data-w'))+')'})}
 function put(s,src,title){var f=s.querySelector('iframe');
  if(!f){f=document.createElement('iframe');f.setAttribute('loading','lazy');f.setAttribute('width',s.getAttribute('data-w'));f.setAttribute('height',s.getAttribute('data-h'));
   f.setAttribute('allow','clipboard-write');f.setAttribute('referrerpolicy','no-referrer-when-downgrade');
   f.addEventListener('load',function(){if(f.getAttribute('src')&&f.getAttribute('src')!=='about:blank')setTimeout(function(){s.classList.add('ready')},900)});
   s.addEventListener('mouseleave',function(){try{f.contentWindow.postMessage({tvlTour:'resume'},'*')}catch(x){}});s.appendChild(f)}
  s.classList.remove('ready');f.setAttribute('title',title);f.setAttribute('src',src);fit()}
 function load(){if(started)return;started=true;var src=cur.getAttribute('data-src'),nm=cur.getAttribute('data-name');
  var lap=scr[0],ph=scr[1];
  if(small()){put(ph,src,nm+' live demo on a phone');return}
  put(lap,src,nm+' live demo');
  var f=lap.querySelector('iframe');var once=function(){f.removeEventListener('load',once);setTimeout(function(){if(cur.getAttribute('data-src')===src)put(ph,src,nm+' live demo on a phone')},1800)};f.addEventListener('load',once)}
 function maybe(){if(go&&near)load()}
 function pick(b,user){if(b===cur&&started)return;cur=b;lt.forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-selected',on?'true':'false')});
  var nm=b.getAttribute('data-name');L.querySelector('.tvd-url').textContent=b.getAttribute('data-url');L.querySelector('.tvd-lname').textContent=nm.replace('&#39;',"'");
  L.querySelector('.tvd-lkind').textContent=b.getAttribute('data-kind');L.querySelector('.tvd-full').setAttribute('href',b.getAttribute('data-full'));
  scr[0].querySelector('.tvd-poster').setAttribute('src',b.getAttribute('data-pd'));scr[1].querySelector('.tvd-poster').setAttribute('src',b.getAttribute('data-pp'));
  scr.forEach(function(s){s.classList.remove('ready');var f=s.querySelector('iframe');if(f)f.setAttribute('src','about:blank')});
  started=false;if(go&&near)load();if(user){ev('dash_live_demo',{demo:b.getAttribute('data-k')});var s=b.parentNode;if(s.scrollWidth>s.clientWidth+4)s.scrollTo({left:b.offsetLeft-s.clientWidth/2+b.clientWidth/2,behavior:RM?'auto':'smooth'})}}
 lt.forEach(function(b){b.addEventListener('click',function(){pick(b,true)})});
 var start=function(){setTimeout(function(){go=true;maybe()},RM?0:500)};if(document.readyState==='complete')start();else window.addEventListener('load',start);
 seen(L,function(on){if(on){near=true;maybe()}},'300px 0px');
 window.addEventListener('resize',fit);fit();
 L.querySelector('.tvd-full').addEventListener('click',function(){ev('dash_demo_open',{demo:cur.getAttribute('data-k'),from:'showcase'})});
 [].forEach.call(document.querySelectorAll('[data-watch]'),function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-watch');var t=L.querySelector('.tvd-lt[data-k="'+k+'"]');if(t)pick(t,true);L.scrollIntoView({behavior:RM?'auto':'smooth',block:'center'})})});
 [].forEach.call(document.querySelectorAll('.tvd-open'),function(a){a.addEventListener('click',function(){ev('dash_demo_open',{from:'cards'})})});
}

/* 2. AI assistant chat */
var chat=document.getElementById('tvd-chat');
if(chat){var box=document.getElementById('tvd-chat-b'),busy=false;
 function add(cls,html){var p=document.createElement('p');p.className=cls;p.innerHTML=html;box.appendChild(p);box.scrollTop=box.scrollHeight;return p}
 [].forEach.call(chat.querySelectorAll('.tvd-q'),function(b){b.addEventListener('click',function(){if(busy)return;busy=true;var i=b.getAttribute('data-i');
  var tpl=chat.querySelector('template.tvd-a[data-i="'+i+'"]');var ans=tpl?tpl.innerHTML:'';b.classList.add('used');
  add('tvd-me-b',b.innerHTML);var typing=add('tvd-bot','<span class="tvd-typing"><i></i><i></i><i></i></span>');
  setTimeout(function(){if(RM){typing.innerHTML=ans;busy=false;box.scrollTop=box.scrollHeight;return}
   var tmp=document.createElement('div');tmp.innerHTML=ans;var txt=tmp.textContent,n=0;typing.textContent='';
   var iv=setInterval(function(){n+=3;typing.textContent=txt.slice(0,n);box.scrollTop=box.scrollHeight;if(n>=txt.length){clearInterval(iv);busy=false}},18)},900);
  if(window.__tvdAuto!==1)ev('dash_ai_question',{q:i})})});
 var asked=false;seen(chat,function(on){if(on&&!asked){asked=true;setTimeout(function(){var f=chat.querySelector('.tvd-q');if(f&&!f.classList.contains('used')){window.__tvdAuto=1;f.click();window.__tvdAuto=0}},700)}},'-80px 0px');
}

/* 3. role switcher */
var rb=document.getElementById('tvd-role');
if(rb){var RT={o:['Owner: the whole picture','Every number, every screen, every setting. Plus your weekly owner report each Monday morning.'],
  m:['Manager: run the day','Customers, schedules, marketing and reviews, without bank balances, payroll or profit.'],
  e:['Employee: just their work','Their schedule, jobs, tasks and time clock. Nothing about money or other customers.']};
 var tiles=[].slice.call(rb.querySelectorAll('.tvd-tile'));
 function role(r,user){rb.setAttribute('data-role',r);[].forEach.call(rb.querySelectorAll('.tvd-role-pick button'),function(b){var on=b.getAttribute('data-r')===r;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false')});
  var n=0;tiles.forEach(function(t){var ok=t.getAttribute('data-r').indexOf(r)>-1;t.classList.toggle('lock',!ok);if(ok)n++});
  document.getElementById('tvd-role-t').textContent=RT[r][0];document.getElementById('tvd-role-d').textContent=RT[r][1];document.getElementById('tvd-role-n').textContent=n+' of '+tiles.length+' screens';
  if(user)ev('dash_role',{role:r})}
 [].forEach.call(rb.querySelectorAll('.tvd-role-pick button'),function(b){b.addEventListener('click',function(){role(b.getAttribute('data-r'),true)})});
 role('o',false)}

/* 4. live automations feed + tasks-done counter, only while on screen */
var feed=document.getElementById('tvd-feed');
if(feed){var items=[].slice.call(document.querySelectorAll('template.tvd-fe')).map(function(t){return t.innerHTML}),fi=0,ft=null,hrs=1029,hel=document.getElementById('tvd-hrs');
 function push(){var w=document.createElement('ul');w.innerHTML=items[fi%items.length];fi++;var li=w.firstElementChild;feed.insertBefore(li,feed.firstChild);
  [].forEach.call(feed.querySelectorAll('li'),function(x,i){var em=x.querySelector('em');if(em&&i>0&&em.textContent==='just now')em.textContent=(i*2)+' min ago';else if(em&&i>0)em.textContent=(i*2)+' min ago'});
  while(feed.children.length>7)feed.removeChild(feed.lastChild);
  hrs+=1;if(hel)hel.textContent=fmt(hrs,0)}
 for(var k=0;k<6;k++)push();
 seen(feed,function(on){if(on&&!ft&&!RM){ft=setInterval(push,2600)}else if(!on&&ft){clearInterval(ft);ft=null}})}

/* 5. industry tabs */
var itabs=[].slice.call(document.querySelectorAll('.tvd-itab')),ipanes=[].slice.call(document.querySelectorAll('.tvd-ipane'));
itabs.forEach(function(t){t.addEventListener('click',function(){var k=t.getAttribute('data-i');
 itabs.forEach(function(x){var on=x===t;x.classList.toggle('on',on);x.setAttribute('aria-selected',on?'true':'false')});
 ipanes.forEach(function(p){p.hidden=p.getAttribute('data-i')!==k});
 var s=t.parentNode;if(s.scrollWidth>s.clientWidth+4)s.scrollTo({left:t.offsetLeft-s.clientWidth/2+t.clientWidth/2,behavior:RM?'auto':'smooth'});
 ev('dash_industry',{industry:k})})});

/* 6. sticky button after the hero, hidden at the form; CTA tracking */
var st=document.querySelector('.tvd-sticky'),top=document.getElementById('tvd-top'),bk=document.getElementById('tvs-book');
if(st&&top&&bk&&'IntersectionObserver' in window){var hv=true,bv=false;function upd(){st.classList.toggle('on',!hv&&!bv)}
 new IntersectionObserver(function(es){hv=es[0].isIntersecting;upd()}).observe(top);new IntersectionObserver(function(es){bv=es[0].isIntersecting;upd()}).observe(bk)}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href="#demos"]');if(a){var d=document.getElementById('demos');if(d){e.preventDefault();d.scrollIntoView({behavior:RM?'auto':'smooth',block:'start'})}ev('dash_demos_click')}},true);
})();
