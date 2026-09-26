/* 3VL business profile: light premium polish on BD's own layout (MOCKUP - not wired yet).
   Keeps the cover, header, tabs and sidebar where BD puts them; only tidies and restyles. */
(function(){
var hdr=document.querySelector('.member_profile .member-profile-header');if(!hdr||document.documentElement.classList.contains('pf-on'))return;
document.documentElement.classList.add('pf-on');
function $(s,r){return (r||document).querySelector(s)}function $$(s,r){return [].slice.call((r||document).querySelectorAll(s))}
var name=(($('h1',hdr)||{}).textContent||'').trim(),uid=($('.userData',hdr)||{getAttribute:function(){return ''}}).getAttribute('data-userid');
function track(act){try{if(window.gtag)window.gtag('event','vip_profile_click',{action:act,business:name,business_id:uid})}catch(e){}}

/* show the phone number right away (no "See Phone Number" step) */
var telA=$('a[href^="tel:"]',hdr);
if(telA){var t=telA.getAttribute('href').replace(/[^\d]/g,'').slice(-10),f=t.slice(0,3)+'-'+t.slice(3,6)+'-'+t.slice(6);
  var box=$('.profile-header-phone-number',hdr);if(box)box.innerHTML='<a class="btn btn-lg btn-block pf-call" data-act="call" href="tel:'+t+'">&#128222; '+f+'</a>';
  $$('.table-display-phone, .myphoneHide').forEach(function(e){var g=e.closest('.table-view-group');if(g&&!g.closest('.member-profile-header')){var c=$('.col-sm-8',g);if(c)c.innerHTML='<a data-act="call" href="tel:'+t+'">'+f+'</a>'}})}

/* the cover already shows the business name/logo: keep it, just make it part of the header card */
var cover=$('.coverPhoto');if(cover){cover.classList.add('pf-coverimg')}

/* tidy */
$$('.make-connection').forEach(function(e){e.style.display='none'});
$$('.content_w_sidebar > .col-md-3 .module').forEach(function(m){if(!m.textContent.trim()&&!m.querySelector('iframe,img'))m.style.display='none'});
document.addEventListener('click',function(e){var a=e.target.closest('.member_profile [data-act], .member_profile .btn-send_message_action, .member_profile .btn-write_a_review_for, .member_profile a.weblink');if(!a)return;
  track(a.getAttribute('data-act')||(a.classList.contains('weblink')?'website':a.classList.contains('btn-write_a_review_for')?'review':'message'))});
})();
