/* 3VL homepage effects: reveal on scroll + hover lift/tilt for feature cards and the Favorites carousel. */
(function(){
'use strict';
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var fine=window.matchMedia&&matchMedia('(hover: hover) and (pointer: fine)').matches;
function tilt(el,amt){
  el.addEventListener('mouseenter',function(){el.classList.add('tvl-lift')});
  el.addEventListener('mousemove',function(e){var b=el.getBoundingClientRect(),x=(e.clientX-b.left)/b.width,y=(e.clientY-b.top)/b.height;
    el.style.setProperty('--ry',((x-.5)*amt).toFixed(2)+'deg');el.style.setProperty('--rx',((.5-y)*amt*.8).toFixed(2)+'deg');
    el.style.setProperty('--gx',(x*100)+'%');el.style.setProperty('--gy',(y*100)+'%')});
  el.addEventListener('mouseleave',function(){el.classList.remove('tvl-lift');el.style.setProperty('--rx','0deg');el.style.setProperty('--ry','0deg')});
}
function go(){
  var sec=document.querySelector('.homepage_steps');
  if(sec&&!reduce&&'IntersectionObserver' in window&&sec.getBoundingClientRect().top>innerHeight*.85){
    sec.classList.add('tvl-anim');
    var io=new IntersectionObserver(function(en){if(en[0].isIntersecting){sec.classList.add('tvl-in');io.disconnect()}},{threshold:.2});io.observe(sec)}
  if(reduce||!fine)return;
  if(sec)Array.prototype.forEach.call(sec.querySelectorAll('.sm-bmargin > a'),function(a){tilt(a,10)});
  Array.prototype.forEach.call(document.querySelectorAll('.recent-member .well'),function(w){tilt(w,6)});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
