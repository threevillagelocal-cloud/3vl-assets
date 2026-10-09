<script>(function(){
function go(){var slot=document.getElementById('tvd-form-slot'),f=document.querySelector('form[name^="drone_services"]');
 if(!slot||!f||slot.querySelector('form'))return;slot.appendChild(f);
 [].forEach.call(document.querySelectorAll('#tvd a[href="#tvd-book"]'),function(a){a.addEventListener('click',function(e){e.preventDefault();document.getElementById('tvd-book').scrollIntoView({behavior:'smooth',block:'start'})})});
 f.addEventListener('submit',function(){try{if(window.gtag)gtag('event','drone_booking_submit')}catch(x){}});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();})();</script>
