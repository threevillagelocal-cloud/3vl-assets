<script>
/* 3VL newsletter page (/newsletter): moves BD's own newsletter sign-up form (newsletter_modal_signup, placed on the page by BD)
   into the designed card, so sign-ups land in the same subscriber list as always. No backslashes (BD strips them). */
(function(){
function go(){
  var slot=document.getElementById('nl-formslot');if(!slot||slot.firstChild)return;
  var fs=[].slice.call(document.querySelectorAll('form[id^=newsletter_modal_signup]')),f=fs.filter(function(x){return !x.closest('.modal')})[0];
  if(!f)return;
  /* BD writes its "thanks" reply into .newsletter_modal_form_container: move that wrapper with the form, or make one */
  var box=f.closest('.newsletter_modal_form_container');
  if(!box){box=document.createElement('div');box.className='newsletter_modal_form_container';f.parentNode.insertBefore(box,f);box.appendChild(f)}
  slot.appendChild(box);
  var nm=f.querySelector('input[name=first_name]');if(nm)nm.setAttribute('placeholder','First name');
  var em=f.querySelector('input[name=email]');if(em)em.setAttribute('placeholder','Email address');
  var b=f.querySelector('[type=submit],button');if(b){if(b.tagName==='INPUT')b.value='Send me the weekly email';else b.textContent='Send me the weekly email'}
  f.addEventListener('submit',function(){try{gtag('event','newsletter_signup',{source:'newsletter_page'})}catch(e){}});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
window.addEventListener('load',go);
})();
</script>
