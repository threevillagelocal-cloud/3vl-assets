<script>(function(){
/* Agents who got the first realtor email (utm_campaign=drone-realtors, $120 offer) keep that price, remembered for 60 days.
   Later emails use utm_campaign=drone-realtors-149 and see the regular $149. Form option listing120 exists only for them. */
function early(){var c='';try{c=new URLSearchParams(location.search).get('utm_campaign')||''}catch(x){}
 if(c==='drone-realtors'){try{localStorage.setItem('tvd120',String(Date.now()))}catch(x){}return true}
 try{var t=+localStorage.getItem('tvd120');return !!t&&Date.now()-t<5184e6}catch(x){return false}}
function price(on){var sel=document.querySelector('#tvd-form-slot select[name="package"],form[name^="drone_services"] select[name="package"]');
 if(sel){[].slice.call(sel.options).forEach(function(o){if(o.value===(on?'listing':'listing120'))o.parentNode.removeChild(o)});if(on)sel.value='listing120'}
 if(!on)return;var p=document.querySelector('#tvd .tvd-price');if(p)p.innerHTML='<sup>$</sup>120';
 var k=document.querySelector('#tvd .tvd-cardk');if(k&&k.textContent.indexOf('email price')<0)k.textContent='The Listing Package - your email price'}
function go(){var slot=document.getElementById('tvd-form-slot'),f=document.querySelector('form[name^="drone_services"]');
 if(!slot||!f||slot.querySelector('form'))return;slot.appendChild(f);
 price(early());
 [].forEach.call(document.querySelectorAll('#tvd a[href="#tvd-book"]'),function(a){a.addEventListener('click',function(e){e.preventDefault();document.getElementById('tvd-book').scrollIntoView({behavior:'smooth',block:'start'})})});
 f.addEventListener('submit',function(){try{if(window.gtag)gtag('event','drone_booking_submit')}catch(x){}});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();})();</script>
