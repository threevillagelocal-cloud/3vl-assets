/* VIP + Featured profile layer (owner 10/7/2026): badges row under the name + scroll reveals for .p3v-reveal blocks. */
(function(){
var CHECK='<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8"/><path d="M4.6 8.3l2.2 2.2 4.6-4.8" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>';
var STAR='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 1.2l2 4.3 4.7.5-3.5 3.2 1 4.6L8 11.5 3.8 13.8l1-4.6L1.3 6l4.7-.5z" fill="#13294b"/></svg>';
function badges(){
  var mp=document.querySelector('.member_profile');if(!mp||mp.classList.contains('p3-hastiers'))return;
  var vip=mp.classList.contains('level_1')||mp.classList.contains('level_8'),feat=mp.classList.contains('level_2');
  var h1=mp.querySelector('.member-profile-header h1');if(!h1||(!vip&&!feat))return;
  var ver=!!document.querySelector('img[alt="Verified Member"]');
  var b=document.createElement('div');b.className='p3-tiers';
  b.innerHTML=(vip?'<span class="p3-tier vip">'+STAR+'VIP Member</span>':'<span class="p3-tier feat">Featured Business</span>')+
    (ver?'<span class="p3-tier ver" title="Three Village Local verified this business">'+CHECK+'Verified</span>':'');
  h1.parentNode.insertBefore(b,h1.nextSibling);mp.classList.add('p3-hastiers');
}
function reveals(){
  var els=document.querySelectorAll('.p3v-reveal:not(.p3v-seen)');if(!els.length)return;
  if(!('IntersectionObserver' in window)){for(var i=0;i<els.length;i++)els[i].classList.add('p3v-on');return}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('p3v-on');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  for(var j=0;j<els.length;j++){els[j].classList.add('p3v-seen');io.observe(els[j])}
}
document.documentElement.classList.add('p3v-js');
function go(){badges();reveals()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();window.addEventListener('load',go);
})();
