<script>(function(){
var P={found:{all:[499,0],free:[449,0],featured:[399,0],vip:[349,0]},
 grow:{all:[999,99],free:[899,99],featured:[849,89],vip:[749,79]},
 town:{all:[1999,199],free:[1799,189],featured:[1699,179],vip:[1499,149]}};
function money(n){return n.toLocaleString('en-US')}
function ev(n,p){try{if(window.gtag)gtag('event',n,p||{})}catch(x){}}
function tier(t,root){
 [].forEach.call(root.querySelectorAll('.tvs-tiers button'),function(b){var on=b.getAttribute('data-t')===t;b.classList.toggle('on',on);b.setAttribute('aria-selected',on?'true':'false')});
 [].forEach.call(root.querySelectorAll('.tvs-card'),function(c){var p=P[c.getAttribute('data-b')];if(!p)return;var cur=p[t],base=p.all;
  var b=c.querySelector('.tvs-price b');b.style.opacity='0';setTimeout(function(){b.textContent=money(cur[0]);b.style.opacity='1'},160);
  var mo=c.querySelector('.tvs-mo');if(mo)mo.innerHTML=cur[1]?'+ <b>$'+cur[1]+'</b>/mo':'one time';
  var was=c.querySelector('.tvs-was');if(was)was.textContent=cur[0]<base[0]?'$'+money(base[0]):'';
  var sv=c.querySelector('.tvs-save'),d=base[0]-cur[0],dm=base[1]-cur[1];
  if(sv)sv.textContent=d>0?('You save $'+money(d)+(dm>0?' + $'+dm+'/mo':'')):'';});
}
function count(el){var n=+el.getAttribute('data-n');if(!n)return;var t0=null,dur=1400;
 function step(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/dur),e=1-Math.pow(1-k,3);el.textContent=money(Math.round(n*e));if(k<1)requestAnimationFrame(step)}
 requestAnimationFrame(step)}
function go(){var root=document.getElementById('tvs');if(!root||root.getAttribute('data-on'))return;root.setAttribute('data-on','1');
 var slot=document.getElementById('tvs-form-slot'),f=document.querySelector('form[name^="services_inquiry"]');
 if(slot&&f&&!slot.querySelector('form'))slot.appendChild(f);
 tier('vip',root);
 [].forEach.call(root.querySelectorAll('.tvs-tiers button'),function(b){b.addEventListener('click',function(){var t=b.getAttribute('data-t');tier(t,root);ev('services_tier',{tier:t})})});
 [].forEach.call(root.querySelectorAll('a[href^="#tvs-"]'),function(a){a.addEventListener('click',function(e){var id=a.getAttribute('href').slice(1),tg=document.getElementById(id);if(!tg)return;e.preventDefault();
  tg.scrollIntoView({behavior:'smooth',block:'start'});var pick=a.getAttribute('data-pick');
  if(id==='tvs-book'){var s=document.querySelector('#tvs-form-slot select[name="bundle"]');if(s&&pick)s.value=pick;
   var on=root.querySelector('.tvs-tiers button.on'),m=document.querySelector('#tvs-form-slot select[name="member_tier"]');
   if(m&&on){var map={vip:'vip',featured:'featured',free:'free',all:'no'};if(!m.value||m.selectedIndex<1)m.value=map[on.getAttribute('data-t')]||''}
   var box=document.getElementById('tvs-form-slot');box.classList.remove('tvs-glow');setTimeout(function(){box.classList.add('tvs-glow')},500);
   ev('services_cta',{pick:pick||'book'})}})});
 if(f)f.addEventListener('submit',function(){ev('services_inquiry_submit')});
 root.classList.add('tvs-ready');
 /* reveal: anything at or above 92% of the screen shows; checked on scroll/resize and on a timer, so nothing can stay hidden */
 var ups=[].slice.call(root.querySelectorAll('.tvs-up')),busy=false;
 function show(u){u.classList.add('tvs-in');[].forEach.call(u.querySelectorAll('[data-n]'),count)}
 function check(){busy=false;var lim=window.innerHeight*0.92;ups=ups.filter(function(u){if(u.getBoundingClientRect().top<lim){show(u);return false}return true});
  if(!ups.length){window.removeEventListener('scroll',tick);window.removeEventListener('resize',tick);clearInterval(iv)}}
 function tick(){if(!busy){busy=true;requestAnimationFrame(check)}}
 window.addEventListener('scroll',tick,{passive:true});window.addEventListener('resize',tick);
 var iv=setInterval(check,700);check();
 var st=root.querySelector('.tvs-sticky'),hero=root.querySelector('.tvs-hero'),bk=document.getElementById('tvs-book');
 if(st&&hero&&'IntersectionObserver' in window){var hv=true,bv=false;function upd(){st.classList.toggle('on',!hv&&!bv)}
  new IntersectionObserver(function(es){hv=es[0].isIntersecting;upd()}).observe(hero);
  new IntersectionObserver(function(es){bv=es[0].isIntersecting;upd()}).observe(bk)}
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();})();</script>
