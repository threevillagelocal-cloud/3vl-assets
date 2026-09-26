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

/* Favorites logos: trim empty white/transparent margins so the real logo fills its frame. Photos (headshots) are left as-is. */
function trimLogo(img){
  if(img.getAttribute('data-trimmed')||!img.naturalWidth||/^data:/.test(img.src))return;
  img.setAttribute('data-trimmed','1');
  try{
    var w=img.naturalWidth,h=img.naturalHeight,s=Math.min(1,400/Math.max(w,h)),cw=Math.round(w*s),ch=Math.round(h*s);
    var c=document.createElement('canvas');c.width=cw;c.height=ch;var x=c.getContext('2d');x.drawImage(img,0,0,cw,ch);
    var d=x.getImageData(0,0,cw,ch).data,minX=cw,minY=ch,maxX=-1,maxY=-1,edge=0,edgeN=0;
    for(var yy=0;yy<ch;yy++)for(var xx=0;xx<cw;xx++){var i=(yy*cw+xx)*4,a=d[i+3],r=d[i],g=d[i+1],b=d[i+2];
      var blank=a<16||(r>238&&g>238&&b>238);
      if(xx===0||yy===0||xx===cw-1||yy===ch-1){edgeN++;if(blank)edge++}
      if(!blank){if(xx<minX)minX=xx;if(xx>maxX)maxX=xx;if(yy<minY)minY=yy;if(yy>maxY)maxY=yy}}
    if(maxX<0)return;
    if(edge/edgeN<0.6){img.classList.add('tvl-photo');return}   /* edges mostly non-white: it's a photo, not a logo on white */
    var bw=maxX-minX+1,bh=maxY-minY+1;if(bw>cw*0.92&&bh>ch*0.92){if(cw/ch>1.35)img.classList.add('tvl-wide');return}
    var pad=Math.round(Math.max(bw,bh)*0.05),ow=bw+pad*2,oh=bh+pad*2;
    var o=document.createElement('canvas');o.width=ow;o.height=oh;var ox=o.getContext('2d');ox.fillStyle='#fff';ox.fillRect(0,0,ow,oh);
    ox.drawImage(c,minX,minY,bw,bh,pad,pad,bw,bh);
    if(ow/oh>1.35)img.classList.add('tvl-wide');
    img.src=o.toDataURL('image/png');
  }catch(e){}
}
function watchLogos(){
  Array.prototype.forEach.call(document.querySelectorAll('.recent-member .recent-member-image img'),function(img){
    if(img.complete)trimLogo(img);img.addEventListener('load',function(){trimLogo(img)});
  });
}
function go(){
  watchLogos();
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
