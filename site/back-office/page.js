<script>(function(){
var root=document.getElementById('bo');if(!root)return;
var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var q=root.querySelector('.bo-q'),tiles=root.querySelectorAll('.bo-tile'),none=root.querySelector('.bo-none');
var dr=root.querySelector('.bo-drawer'),scrim=root.querySelector('.bo-scrim'),last=null;
function track(n,p){try{gtag('event',n,p||{})}catch(x){}}
function open(k,from){var p=root.querySelector('.bo-panel[data-k="'+k+'"]');if(!p)return;
 root.querySelectorAll('.bo-panel').forEach(function(x){x.classList.toggle('on',x===p);});
 p.querySelectorAll('.bo-pro').forEach(function(c){c.style.animation='none';void c.offsetWidth;c.style.animation='';});
 last=document.activeElement;dr.hidden=false;scrim.hidden=false;dr.scrollTop=0;
 requestAnimationFrame(function(){requestAnimationFrame(function(){dr.classList.add('on');scrim.classList.add('on');});});
 document.documentElement.style.overflow='hidden';
 try{history.replaceState(null,'','#'+k)}catch(x){}
 dr.querySelector('.bo-x').focus({preventScroll:true});track('back_office_open',{service:k,from:from||'tile'});}
function close(){dr.classList.remove('on');scrim.classList.remove('on');document.documentElement.style.overflow='';
 setTimeout(function(){dr.hidden=true;scrim.hidden=true;},still?0:450);
 try{history.replaceState(null,'',location.pathname+location.search)}catch(x){}
 if(last&&last.focus)last.focus({preventScroll:true});}
tiles.forEach(function(t){t.addEventListener('click',function(){open(t.getAttribute('data-k'));});});
dr.querySelector('.bo-x').addEventListener('click',close);scrim.addEventListener('click',close);
document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&!dr.hidden)close();});
var sy=null;dr.addEventListener('touchstart',function(ev){sy=dr.scrollTop<=0?ev.touches[0].clientY:null;},{passive:true});
dr.addEventListener('touchend',function(ev){if(sy!==null&&ev.changedTouches[0].clientY-sy>90)close();sy=null;},{passive:true});
function words(t){return t.toLowerCase().split(' ').filter(function(w){return w.length>1;});}
function run(){var ws=words(q.value||''),any=false,best=null,bs=0;
 tiles.forEach(function(t){var s=t.getAttribute('data-s'),sc=0;ws.forEach(function(w){if(s.indexOf(w)>-1)sc++;});
  var ok=!ws.length||sc>0;t.classList.toggle('dim',!!ws.length&&!ok);t.classList.toggle('hit',!!ws.length&&ok);if(ok)any=true;if(sc>bs){bs=sc;best=t;}});
 none.hidden=any;return best;}
q.addEventListener('input',run);
q.addEventListener('keydown',function(ev){if(ev.key==='Enter'){var b=run();if(b){open(b.getAttribute('data-k'),'search');track('back_office_search',{q:q.value});}}});
if(!still&&'IntersectionObserver' in window){root.classList.add('anim');
 var rv=root.querySelectorAll('.bo-tile,.bo-ask,.bo-print,.bo-end');
 rv.forEach(function(el){el.classList.add('bo-rv');var i=+(el.style.getPropertyValue('--i')||0);el.style.setProperty('--d',(i%4)*0.08+'s');});
 var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{rootMargin:'0px 0px -6% 0px'});
 rv.forEach(function(el){io.observe(el);});
 root.querySelectorAll('.bo-stats b').forEach(function(b){var n=+b.getAttribute('data-n'),t0=0,done=false;b.textContent='0';
  function step(){if(done)return;var now=Date.now();if(!t0)t0=now;var p=Math.min(1,(now-t0)/1400);b.textContent=Math.round(n*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(step);else done=true;}
  setTimeout(function(){requestAnimationFrame(step);},500);setTimeout(function(){done=true;b.textContent=n;},2600);});
 var ws=root.querySelectorAll('.bo-words b'),wi=0;
 if(ws.length)setInterval(function(){if(document.hidden)return;var cur=ws[wi];cur.classList.remove('on');cur.classList.add('out');wi=(wi+1)%ws.length;var nx=ws[wi];nx.classList.remove('out');void nx.offsetWidth;nx.classList.add('on');setTimeout(function(){cur.classList.remove('out');},520);},2200);
}
root.querySelectorAll('.bo-dl').forEach(function(a){a.addEventListener('click',function(){track('back_office_pdf',{from:a.closest('.bo-hero')?'hero':'page'});});});
var h=(location.hash||'').slice(1);if(h&&root.querySelector('.bo-panel[data-k="'+h+'"]'))setTimeout(function(){open(h,'link');},400);
})();
</script>