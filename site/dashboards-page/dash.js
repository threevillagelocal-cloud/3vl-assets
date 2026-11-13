;(function(){var R=document.getElementById('tvs');if(!R||!R.classList.contains('tvd'))return;
var RM=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
function ev(n,p){try{if(window.gtag)gtag('event',n,p||{})}catch(x){}}
function fmt(v,dec){var s=dec?v.toFixed(dec):String(Math.round(v));var pr=s.split('.'),i=pr[0],o='';while(i.length>3){o=','+i.slice(-3)+o;i=i.slice(0,-3)}return i+o+(pr[1]?'.'+pr[1]:'')}
function cnt(el){var to=parseFloat(el.getAttribute('data-c')),dec=+(el.getAttribute('data-d')||0);if(RM){el.textContent=fmt(to,dec);return}
 var t0=null,dur=1300;function st(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/dur),e=1-Math.pow(1-k,3);el.textContent=fmt(to*e,dec);if(k<1)requestAnimationFrame(st)}requestAnimationFrame(st)}
function counts(scope){[].forEach.call(scope.querySelectorAll('[data-c]'),cnt)}
function seen(el,fn,margin){if(!el)return;if(!('IntersectionObserver' in window)){fn(true);return}new IntersectionObserver(function(es){fn(es[0].isIntersecting)},{rootMargin:margin||'0px'}).observe(el)}
var toastT=null;function toast(msg){var t=document.getElementById('tvd-toast');if(!t)return;t.textContent=msg;t.classList.add('on');clearTimeout(toastT);toastT=setTimeout(function(){t.classList.remove('on')},2400)}

/* 1. dashboard showcase: tabs, guided tour while on screen until the visitor clicks */
var app=document.getElementById('tvd-app');
if(app){var tabs=[].slice.call(app.querySelectorAll('.tvd-tab')),panes=[].slice.call(app.querySelectorAll('.tvd-pane'));
 var order=tabs.map(function(t){return t.getAttribute('data-p')}),cur='cc',tour=!RM&&!!(window.matchMedia&&matchMedia('(min-width: 901px)').matches),timer=null,vis=false,first=true;
 function show(k,user){cur=k;tabs.forEach(function(t){var on=t.getAttribute('data-p')===k;t.classList.toggle('on',on);t.setAttribute('aria-selected',on?'true':'false');t.tabIndex=on?0:-1;
   if(on&&user!=='init'){var s=t.parentNode;if(s.scrollWidth>s.clientWidth+4)s.scrollTo({left:t.offsetLeft-s.clientWidth/2+t.clientWidth/2,behavior:RM?'auto':'smooth'})}});
  panes.forEach(function(p){var on=p.getAttribute('data-p')===k;p.hidden=!on;p.classList.toggle('on',on);if(on)counts(p)});
  if(user===true){tour=false;stopT();ev('dash_demo_tab',{tab:k})}}
 function stopT(){if(timer){clearInterval(timer);timer=null}}
 function startT(){if(!tour||timer)return;timer=setInterval(function(){show(order[(order.indexOf(cur)+1)%order.length],false)},7000)}
 tabs.forEach(function(t,i){t.addEventListener('click',function(){show(t.getAttribute('data-p'),true)});
  t.addEventListener('keydown',function(e){var k=e.key,n=-1;if(k==='ArrowDown'||k==='ArrowRight')n=(i+1)%tabs.length;if(k==='ArrowUp'||k==='ArrowLeft')n=(i-1+tabs.length)%tabs.length;if(n>-1){e.preventDefault();tabs[n].focus();show(order[n],true)}})});
 tabs.forEach(function(t){t.tabIndex=t.classList.contains('on')?0:-1});
 app.addEventListener('pointerdown',function(){tour=false;stopT()});
 seen(app,function(on){vis=on;if(on){if(first){first=false;var p=app.querySelector('.tvd-pane.on');p.classList.remove('on');void p.offsetWidth;p.classList.add('on');counts(p)}startT()}else stopT()});
 /* interactive bits inside the screens */
 app.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('button');if(!b||!app.contains(b))return;
  if(b.classList.contains('tvd-approve')){var post=b.closest('.tvd-post');post.classList.remove('wait');post.classList.add('ok');post.querySelector('em').textContent='Approved';b.disabled=true;b.textContent='Scheduled';var ed=post.querySelector('.tvd-edit');if(ed)ed.remove();toast('Approved. It will post Tuesday at 4 PM.');ev('dash_demo_action',{a:'approve'})}
  else if(b.classList.contains('tvd-edit')){toast('Opens the post editor in your dashboard.')}
  else if(b.classList.contains('tvd-post-reply')){b.disabled=true;b.textContent='Reply posted';toast('Reply posted to Google.');ev('dash_demo_action',{a:'reply'})}
  else if(b.classList.contains('tvd-sw')){var on=!b.classList.contains('on');b.classList.toggle('on',on);b.setAttribute('aria-checked',on?'true':'false');var em=b.parentNode.querySelector('em');if(em)em.textContent=on?'On':'Off';toast((on?'Turned on: ':'Turned off: ')+b.getAttribute('aria-label'));ev('dash_demo_action',{a:'toggle'})}});
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

/* 4. live automations feed + hours counter, only while on screen */
var feed=document.getElementById('tvd-feed');
if(feed){var items=[].slice.call(document.querySelectorAll('template.tvd-fe')).map(function(t){return t.innerHTML}),fi=0,ft=null,hrs=41.5,hel=document.getElementById('tvd-hrs');
 function push(){var w=document.createElement('ul');w.innerHTML=items[fi%items.length];fi++;var li=w.firstElementChild;feed.insertBefore(li,feed.firstChild);
  [].forEach.call(feed.querySelectorAll('li'),function(x,i){var em=x.querySelector('em');if(em&&i>0&&em.textContent==='just now')em.textContent=(i*2)+' min ago';else if(em&&i>0)em.textContent=(i*2)+' min ago'});
  while(feed.children.length>7)feed.removeChild(feed.lastChild);
  hrs+=0.1;if(hel)hel.textContent=hrs.toFixed(1)}
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
