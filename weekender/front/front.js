/* Front layout (10/24/2026): extras on top of weekender.js. Only runs when #wk-top has .wk-y.
   1) Top Things to Do tabs: Top Picks / Today (from the live schedule) / Coming Up (the "Coming up" cards)
   2) Local Business Spotlight: random start each visit, arrows, 7 s auto-advance (pauses on hover, focus or touch; off for reduced motion) */
(function(){
'use strict';
var root=document.getElementById('wk-top');if(!root||!root.classList.contains('wk-y'))return;
function $$(s,el){return Array.prototype.slice.call((el||root).querySelectorAll(s))}
function track(n,p){try{if(window.gtag)window.gtag('event',n,p||{})}catch(e){}}
function esc(x){return String(x||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches;

/* ---------- 1) Top Things to Do tabs ---------- */
(function(){
  var sec=document.getElementById('wk-picks');if(!sec)return;var h2=sec.querySelector('.wk-h2');if(!h2)return;
  var bar=document.createElement('div');bar.className='y-tabs';bar.setAttribute('role','tablist');
  bar.innerHTML='<button type="button" role="tab" class="on" aria-selected="true" data-y="tp">Top Picks</button><button type="button" role="tab" aria-selected="false" data-y="td">Today <b class="y-tdn"></b></button><button type="button" role="tab" aria-selected="false" data-y="cu">Coming Up</button>';
  h2.parentNode.insertBefore(bar,h2.nextSibling);
  var pane=document.createElement('div');pane.className='y-today';sec.appendChild(pane);
  function todayBlk(){var b=null;$$('#wk-sched .wk-dayblk').forEach(function(x){var t=x.querySelector('.wk-dayh b');if(!b&&t&&/^today$/i.test(t.textContent.trim()))b=x});return b}
  function rows(){var b=todayBlk(),li=b?$$('.wk-ev',b):[];
    pane.innerHTML=li.length?li.map(function(e){var a=e.querySelector('.wk-evtitle a'),t=e.querySelector('.wk-evt b'),w=e.querySelector('.wk-evwhere'),s=e.querySelector('.wk-pstat');
      var title=a?'<a href="'+esc(a.getAttribute('href'))+'"'+(a.target?' target="_blank" rel="noopener"':'')+'>'+esc(a.textContent)+'</a>':'<b>'+esc((e.querySelector('.wk-evtitle')||{}).textContent)+'</b>';
      return '<div class="y-trow"><span class="t">'+esc(t?t.textContent:'')+'</span><div>'+title+'<small>'+esc(w?w.textContent:'')+'</small></div>'+(s&&s.textContent?'<span class="wk-pstat '+esc(s.className.replace('wk-pstat',''))+'">'+esc(s.textContent)+'</span>':'<span></span>')+'</div>'}).join('')+
      '<a class="y-tmore" href="#wk-sched">See the full schedule for this week &rarr;</a>':'<p class="y-trow">Nothing else on the calendar today. <a href="#wk-sched">See this week &rarr;</a></p>';
    var n=bar.querySelector('.y-tdn');if(n)n.textContent=li.length||''}
  function hasRadar(){return !!sec.querySelector('.wk-radar')}
  function upd(){var cu=bar.querySelector('[data-y=cu]');cu.hidden=!hasRadar();var b=todayBlk(),n=bar.querySelector('.y-tdn');if(n)n.textContent=b?$$('.wk-ev',b).length||'':''}
  bar.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var k=b.getAttribute('data-y');
    $$('button',bar).forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-selected',on)});
    sec.classList.toggle('y-td',k==='td');sec.classList.toggle('y-cu',k==='cu');if(k==='td')rows();track('front_tab',{tab:k})});
  /* the live schedule opens on Today (the classic page starts with every day folded) */
  var opened=false;function openToday(){if(opened)return;var b=todayBlk();if(!b)return;opened=true;if(b.classList.contains('is-collapsed')){b.classList.remove('is-collapsed');var h=b.querySelector('.wk-dayh');if(h)h.setAttribute('aria-expanded','true')}}
  upd();var n=0,t=setInterval(function(){upd();if(n>2)openToday();if(++n>12)clearInterval(t)},1500);
})();

/* ---------- 2) Local Business Spotlight ---------- */
(function(){
  var main=document.getElementById('y-spmain'),list=document.getElementById('y-list'),wrap=document.getElementById('y-spw');if(!main||!list)return;
  var cards=$$('.y-mc',list),n=cards.length;if(!n)return;
  var i=Math.floor(Math.random()*n),tm=0,hold=false,wide=window.matchMedia&&matchMedia('(min-width:1201px)');
  var CH='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',PH='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>';
  function card(c){var g=function(k){return c.getAttribute('data-'+k)||''},name=(c.querySelector('.y-mct b')||{}).textContent||'',href=c.getAttribute('href');
    var vis=g('img')?'<img src="'+esc(g('img'))+'" alt="'+esc(g('alt'))+'" style="object-position:'+esc(g('pos'))+'" width="900" height="560">':'<span class="y-panel" style="--c:'+esc(g('color'))+'"><span class="y-plogo" style="background-image:url(\''+esc(g('logo'))+'\')"></span></span>';
    return '<article class="y-spc"><a class="y-spimg" href="'+esc(href)+'" tabindex="-1" aria-hidden="true" data-y="photo">'+vis+'<span class="y-vipb">VIP</span></a><div class="y-spb"><div class="y-sptop"><span class="y-splogo" style="background-image:url(\''+esc(g('logo'))+'\')"></span>'+
      '<p class="y-spcat">'+esc(g('cat'))+(g('town')?' <span>&middot; '+esc(g('town'))+'</span>':'')+'</p></div><h3 class="y-spn2"><a href="'+esc(href)+'" data-y="name">'+esc(name)+'</a></h3>'+(g('desc')?'<p class="y-spd">'+esc(g('desc'))+'</p>':'')+
      '<div class="y-spbtns"><a class="y-btn" href="'+esc(href)+'" data-y="profile">View profile '+CH+'</a>'+(g('tel')?'<a class="y-btn o" href="tel:'+esc(g('tel'))+'" data-y="call">'+PH+'Call</a>':'')+'</div></div></article>'}
  function show(k){i=(k+n)%n;main.innerHTML=card(cards[i]);main.setAttribute('data-vip',(cards[i].querySelector('.y-mct b')||{}).textContent||'');
    cards.forEach(function(c,j){var d=(j-i+n)%n;c.style.order=d;c.classList.toggle('y-on',d>0&&d<=3);c.hidden=d===0});list.scrollLeft=0;
    var nx=cards[(i+1)%n].getAttribute('data-img');if(nx){var p=new Image();p.src=nx}}
  function go(){clearInterval(tm);if(RM)return;tm=setInterval(function(){if(!hold&&!document.hidden)show(i+1)},7000)}
  var sec=document.getElementById('nh-feat')||wrap;
  ['mouseenter','focusin','touchstart'].forEach(function(ev){sec.addEventListener(ev,function(){hold=true},{passive:true})});
  ['mouseleave','focusout'].forEach(function(ev){sec.addEventListener(ev,function(){hold=false})});
  $$('.y-spn',sec).forEach(function(b){b.addEventListener('click',function(){show(i+(+b.getAttribute('data-sp')));go();track('spotlight_nav',{dir:b.getAttribute('data-sp')})})});
  sec.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;
    if(a.closest('#y-spmain'))track('spotlight_click',{vip:main.getAttribute('data-vip'),link:a.getAttribute('data-y')||'card'});
    else if(a.classList.contains('y-mc'))track('spotlight_click',{vip:(a.querySelector('.y-mct b')||{}).textContent||'',link:'also'});
    else if(a.classList.contains('y-lg'))track('spotlight_click',{vip:a.getAttribute('title')||'',link:'logo'});});
  show(i);
  /* start rotating once the section is near the screen (no work while it is far away) */
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(en){if(en[0].isIntersecting){go();io.disconnect()}},{rootMargin:'200px 0px'});io.observe(sec)}else go();
})();
})();
