/* Culper Spy Day 2026 Blueprint (Three Village Local): countdown, decoder, flip cards, checklist, share, scrollspy, reveal. */
(function(){
'use strict';
var root=document.getElementById('spy-top');if(!root)return;
root.classList.add('js');
function $(s,r){return (r||document).querySelector(s)}function $$(s,r){return [].slice.call((r||document).querySelectorAll(s))}
function track(a,o){try{if(window.gtag)window.gtag('event','spyday_click',Object.assign({action:a},o||{}))}catch(e){}}

/* countdown to the 10 AM flag raising */
var cd=$('#spy-count');
if(cd){var T=new Date(cd.getAttribute('data-target')).getTime(),end=T+6*36e5;
  var tick=function(){var n=Date.now(),d=T-n;
    if(n>=end){cd.innerHTML='<span class="spy-cl">Mission complete. See you next year.</span>';return}
    if(d<=0){cd.classList.add('is-live');cd.innerHTML='<span class="spy-cl">&#9679; Happening now: 10 AM to 4 PM</span>';return}
    var u={d:Math.floor(d/864e5),h:Math.floor(d/36e5)%24,m:Math.floor(d/6e4)%60,s:Math.floor(d/1e3)%60};
    $$('b[data-u]',cd).forEach(function(b){var v=u[b.getAttribute('data-u')];b.textContent=(v<10&&b.getAttribute('data-u')!=='d'?'0':'')+v});
    setTimeout(tick,1000)};
  tick()}

/* decoder */
$$('#spy-msg button').forEach(function(b){var code=b.textContent;
  b.addEventListener('click',function(){var on=b.classList.toggle('is-on');b.textContent=on?b.getAttribute('data-w'):code;
    if($$('#spy-msg button.is-on').length===$$('#spy-msg button').length)track('decoded_all')})});

/* flip cards */
$$('.spy-flip').forEach(function(f){f.addEventListener('click',function(){f.classList.toggle('is-on');track('fact')})});

/* checklist (saved on this device) */
var KEY='spyday2026-checks',saved={};try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
var items=$$('#spy-checks li'),bar=$('#spy-pbar');
function prog(){var n=items.filter(function(li){return li.classList.contains('is-on')}).length;if(bar)bar.style.width=(items.length?n/items.length*100:0)+'%'}
items.forEach(function(li){var k=li.getAttribute('data-k');if(saved[k])li.classList.add('is-on');li.setAttribute('role','checkbox');li.setAttribute('tabindex','0');
  var flip=function(){var on=li.classList.toggle('is-on');saved[k]=on;li.setAttribute('aria-checked',on?'true':'false');try{localStorage.setItem(KEY,JSON.stringify(saved))}catch(e){}prog()};
  li.addEventListener('click',flip);li.addEventListener('keydown',function(e){if(e.key===' '||e.key==='Enter'){e.preventDefault();flip()}})});
prog();

/* share */
var sb=$('#spy-share');
function toast(t){var el=document.createElement('div');el.className='spy-toast';el.textContent=t;document.body.appendChild(el);setTimeout(function(){el.classList.add('is-on')},10);setTimeout(function(){el.classList.remove('is-on');setTimeout(function(){el.remove()},400)},2200)}
if(sb)sb.addEventListener('click',function(){var data={title:'The Ultimate Culper Spy Day Blueprint',text:'Culper Spy Day is Saturday, Oct. 3 in Setauket. Here is the whole plan:',url:location.href.split('#')[0]};track('share');
  if(navigator.share){navigator.share(data).catch(function(){})}else if(navigator.clipboard){navigator.clipboard.writeText(data.url).then(function(){toast('Link copied. Send it to your crew!')})}else toast(data.url)});

/* scrollspy for the jump nav */
var nav=$('#spy-nav');
if(nav&&'IntersectionObserver' in window){var links=$$('a',nav),map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.remove('is-on')});var a=map[e.target.id];if(a){a.classList.add('is-on');a.scrollIntoView({block:'nearest',inline:'center'})}}})},{rootMargin:'-40% 0px -55% 0px'});
  $$('.spy-sec[id]').forEach(function(s){if(map[s.id])io.observe(s)})}

/* scroll reveal (content is visible without JS) */
var rv=$$('.spy-order,.spy-stop,.spy-card,.spy-b,.spy-ag,.spy-flip,.spy-tl li');
if('IntersectionObserver' in window){rv.forEach(function(el){el.classList.add('spy-rv')});
  var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');ro.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  rv.forEach(function(el){ro.observe(el)})}

/* clicks on business cards */
$$('a.spy-b').forEach(function(a){a.addEventListener('click',function(){track('business',{label:(($('b',a)||{}).textContent||'').trim()})})});
})();
