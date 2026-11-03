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
  var b=f.querySelector('[type=submit],button');if(b){if(b.tagName==='INPUT')b.value='Sign me up';else b.textContent='Sign me up'}
  /* arriving from the sign-up card on a post or event page: the email is already typed in */
  var pre='';try{pre=sessionStorage.getItem('tvl_nl_email')||''}catch(e){}
  if(pre&&em&&!em.value){em.value=pre;try{sessionStorage.removeItem('tvl_nl_email')}catch(e){}
    var tip=document.createElement('p');tip.className='nl-almost';tip.textContent='Almost done: add your first name, tick the box and tap Sign me up.';
    box.insertBefore(tip,box.firstChild);setTimeout(function(){slot.scrollIntoView({behavior:'smooth',block:'center'});if(nm)nm.focus({preventScroll:true})},300)}
  var from=(location.search.match(/[?&]from=([a-z]+)/)||[])[1]||'newsletter_page';
  f.addEventListener('submit',function(){try{localStorage.setItem('tvl_nl_done','1')}catch(e){}try{gtag('event','newsletter_signup',{source:from})}catch(e){}});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
window.addEventListener('load',go);
})();
</script>
