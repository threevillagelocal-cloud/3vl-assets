/* A Three Village Throwback: Crazy Eddie (2026): reading progress, jump-nav scrollspy, scroll reveals,
   click-to-play YouTube (no YouTube download until tapped), lazy images, share. No regex (BD strips backslashes). */
(function(){
  var root=document.querySelector('.ce');if(!root)return;root.classList.add('js');
  var bar=document.createElement('div');bar.className='ce-prog';document.body.appendChild(bar);
  function prog(){var r=root.getBoundingClientRect(),h=r.height-window.innerHeight;var p=h>0?Math.min(1,Math.max(0,-r.top/h)):0;bar.style.width=(p*100)+'%'}
  window.addEventListener('scroll',prog,{passive:true});prog();
  /* lazy images: data-src / data-srcset load near the screen */
  var lazy=[].slice.call(root.querySelectorAll('img[data-src]'));
  function load(img){if(img.getAttribute('data-srcset'))img.srcset=img.getAttribute('data-srcset');img.src=img.getAttribute('data-src');img.removeAttribute('data-src')}
  var rv=[].slice.call(root.querySelectorAll('.ce-rv'));
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    rv.forEach(function(el){io.observe(el)});
    var il=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){load(e.target);il.unobserve(e.target)}})},{rootMargin:'900px 0px'});
    lazy.forEach(function(i){il.observe(i)});
  }else{rv.forEach(function(el){el.classList.add('in')});lazy.forEach(load)}
  /* count-up stats */
  var cnt=[].slice.call(root.querySelectorAll('[data-count]'));
  function run(el){var n=+el.getAttribute('data-count'),pre=el.getAttribute('data-pre')||'',suf=el.getAttribute('data-suf')||'',t0=null;
    function f(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/1400);el.textContent=pre+Math.round(n*(1-Math.pow(1-k,3)))+suf;if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)}
  if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion:reduce)').matches){
    var ic=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){run(e.target);ic.unobserve(e.target)}})},{threshold:.6});
    cnt.forEach(function(c){ic.observe(c)})}
  /* scrollspy */
  var links=[].slice.call(root.querySelectorAll('.ce-nav a'));
  function spy(){var cur=null;links.forEach(function(a){var s=document.getElementById(a.getAttribute('href').slice(1));if(s&&s.getBoundingClientRect().top<140)cur=a});
    links.forEach(function(a){a.classList.toggle('on',a===cur)})}
  window.addEventListener('scroll',spy,{passive:true});spy();
  /* click-to-play video */
  [].forEach.call(root.querySelectorAll('.ce-play'),function(b){b.addEventListener('click',function(){
    var id=b.getAttribute('data-yt'),f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0';f.title=b.getAttribute('aria-label')||'Crazy Eddie commercial';
    f.setAttribute('allow','accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');f.setAttribute('allowfullscreen','');
    b.parentNode.appendChild(f);b.remove();if(window.gtag)gtag('event','video_play',{video:id,page:'crazy-eddie'})})});
  /* share */
  var toast=document.createElement('div');toast.className='ce-toast';document.body.appendChild(toast);
  function say(t){toast.textContent=t;toast.classList.add('on');setTimeout(function(){toast.classList.remove('on')},2200)}
  [].forEach.call(root.querySelectorAll('[data-share]'),function(b){b.addEventListener('click',function(){
    var d={title:document.title,text:'Remember Crazy Eddie on Route 347? His prices were INSANE!',url:location.href.split('#')[0]};
    if(navigator.share){navigator.share(d).catch(function(){})}else if(navigator.clipboard){navigator.clipboard.writeText(d.url).then(function(){say('Link copied')})}else{say(d.url)}
    if(window.gtag)gtag('event','share',{page:'crazy-eddie'})})});
})();
