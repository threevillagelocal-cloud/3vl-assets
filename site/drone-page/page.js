<script>(function(){
function go(){var r=document.getElementById('tvd');if(!r||r.getAttribute('data-on'))return;r.setAttribute('data-on','1');r.classList.add('js');
 var slot=document.getElementById('tvd-form-slot'),f=document.querySelector('form[name^="drone_services"]');
 if(slot&&f){var box=f.closest('.form-container')||f.parentNode;slot.appendChild(f);if(box&&box!==document.body&&!box.querySelector('form')&&box.textContent.trim()==='')box.style.display='none'}
 var rv=[].slice.call(r.querySelectorAll('.tvd-rv'));
 if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -40px 0px'});rv.forEach(function(e){io.observe(e)})}else rv.forEach(function(e){e.classList.add('in')});
 var lb=document.getElementById('tvd-lb'),li=lb.querySelector('img');
 [].forEach.call(r.querySelectorAll('.tvd-ph'),function(b){b.addEventListener('click',function(){li.src=b.getAttribute('data-full');li.alt=b.querySelector('img').alt;lb.hidden=false})});
 lb.addEventListener('click',function(){lb.hidden=true;li.src=''});
 document.addEventListener('keydown',function(e){if(e.key==='Escape')lb.hidden=true});
 var fl=r.querySelector('.tvd-float'),bk=document.getElementById('tvd-book'),hero=r.querySelector('.tvd-hero');
 function sc(){var h=hero.getBoundingClientRect().bottom<0,b=bk.getBoundingClientRect();fl.classList.toggle('on',h&&b.top>innerHeight)}
 addEventListener('scroll',sc,{passive:true});sc();
 [].forEach.call(r.querySelectorAll('a[href^="#tvd-"]'),function(a){a.addEventListener('click',function(e){var t=document.getElementById(a.getAttribute('href').slice(1));if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'});try{if(window.gtag)gtag('event','drone_page_click',{target:a.getAttribute('href')})}catch(x){}}})});
 if(f)f.addEventListener('submit',function(){try{if(window.gtag)gtag('event','drone_booking_submit')}catch(x){}});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();})();</script>
