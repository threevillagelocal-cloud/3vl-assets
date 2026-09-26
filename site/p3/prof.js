/* 3VL premium business profile (MOCKUP - not wired into the site yet). Runs only on member profile pages. */
(function(){
var hdr=document.querySelector('.member_profile .member-profile-header');if(!hdr||document.getElementById('pf'))return;
var me=document.currentScript;var BASE=me?me.src.replace(/prof\.js.*$/,''):'';
function $(s,r){return (r||document).querySelector(s)}function $$(s,r){return [].slice.call((r||document).querySelectorAll(s))}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function txt(e){return e?e.textContent.replace(/\s+/g,' ').trim():''}
function row(label){var r=$$('.table-view-group').filter(function(g){return txt($('.bold',g)).toLowerCase()===label})[0];return r?$('.col-sm-8',r):null}
var name=txt($('h1',hdr)),cat=txt($('.profile-header-top-category',hdr)),uid=($('.userData',hdr)||{getAttribute:function(){return ''}}).getAttribute('data-userid');
var logo=($('.profile-image img',hdr)||{}).src||'',telA=$('a[href^="tel:"]',hdr),tel=telA?telA.getAttribute('href').replace(/[^\d]/g,'').slice(-10):'';
var telF=tel.length===10?tel.slice(0,3)+'-'+tel.slice(3,6)+'-'+tel.slice(6):'';
var locEl=row('location'),addr=locEl?txt(locEl).replace(/United States$/,'').replace(/Setauket- East Setauket/,'East Setauket').replace(/\s*,\s*$/,''):txt($('.profile-header-location',hdr));
var web=($('a.weblink')||{}).href||'',msg=($('.btn-send_message_action',hdr)||{}).href||'',rev=($('.btn-write_a_review_for',hdr)||{}).href||'',revs=($('.the-rating-link',hdr)||{}).href||'';
var ratingTxt=txt($('.the-average-rating',hdr)),countTxt=txt($('.the-review-count',hdr));
var rating=(ratingTxt.match(/([\d.]+)\s*\/\s*5/)||[])[1],count=(countTxt.match(/\d+/)||[])[0];
var verified=!!$('.member-badges img[alt*="Verified"]');
var vipBadge=!!$('.member-badges img[alt*="VIP"]');
var maps='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(name+' '+addr);

function track(act){try{if(window.gtag)window.gtag('event','vip_profile_click',{action:act,business:name,business_id:uid})}catch(e){}}

var h='<section id="pf" class="pf"><header class="pf-hero" style="background-image:url(\''+BASE+'img/village-hero.jpg\')"><div class="pf-hin">'+
  '<div class="pf-logo"><img src="'+esc(logo)+'" alt="'+esc(name)+'"></div>'+
  '<div class="pf-id">'+(vipBadge?'<span class="pf-vip">&#11088; VIP LOCAL BUSINESS</span>':'')+'<h1 class="pf-name">'+esc(name)+'</h1>'+
  '<p class="pf-meta">'+esc(cat)+(addr?' &middot; &#128205; '+esc(addr):'')+'</p><div class="pf-badges" id="pf-badges">'+
  (verified?'<span class="pf-b pf-bok">&#10003; Verified local business</span>':'')+
  (rating?'<a class="pf-b pf-bstar" href="'+esc(revs)+'">&#9733; '+esc(rating)+' &middot; '+esc(count||0)+' neighbor review'+(count==='1'?'':'s')+'</a>':'')+
  '</div></div></div><span class="pf-credit">Photo: Iracaz, CC BY-SA 3.0</span></header>'+
  '<nav class="pf-bar" aria-label="Contact '+esc(name)+'">'+
  (tel?'<a class="pf-a pf-call" data-act="call" href="tel:'+tel+'">&#128222; '+telF+'</a><a class="pf-a pf-text" data-act="text" href="sms:'+tel+'">&#128172; Text</a>':'')+
  '<a class="pf-a" data-act="directions" href="'+esc(maps)+'" target="_blank" rel="noopener">&#128205; Directions</a>'+
  '<button type="button" class="pf-a" data-act="save_contact">&#128100; Save contact</button>'+
  (msg?'<a class="pf-a" data-act="message" href="'+esc(msg)+'">&#9993;&#65039; Message</a>':'')+
  (web?'<a class="pf-a" data-act="website" href="'+esc(web)+'" target="_blank" rel="noopener">&#127760; Website</a>':'')+
  '<button type="button" class="pf-a" data-act="share">&#128279; Share</button>'+
  '</nav><div class="pf-toast" id="pf-toast"></div></section>';
hdr.insertAdjacentHTML('beforebegin',h);document.documentElement.classList.add('pf-on');
var pf=document.getElementById('pf');

/* extra trust from public listing details (years, specialties) */
fetch(BASE+'vip_meta.json').then(function(r){return r.json()}).then(function(M){var m=M[uid];if(!m)return;var b=$('#pf-badges');
  if(m.since){var y=new Date().getFullYear()-(+m.since);if(y>0)b.insertAdjacentHTML('beforeend','<span class="pf-b pf-bcal">Serving since '+esc(m.since)+' &middot; '+y+' yrs</span>')}
  if(m.specs&&m.specs.length)$('.pf-id',pf).insertAdjacentHTML('beforeend','<div class="pf-specs">'+m.specs.map(function(x){return '<span>'+esc(x)+'</span>'}).join('')+'</div>')}).catch(function(){});

function toast(t){var e=$('#pf-toast');e.textContent=t;e.classList.add('is-on');clearTimeout(toast.h);toast.h=setTimeout(function(){e.classList.remove('is-on')},3000)}
pf.addEventListener('click',function(e){var a=e.target.closest('[data-act]');if(!a)return;var act=a.getAttribute('data-act');track(act);
  if(act==='save_contact'){e.preventDefault();var L=['BEGIN:VCARD','VERSION:3.0','FN:'+name,'ORG:'+name];if(tel)L.push('TEL;TYPE=WORK,VOICE:+1'+tel);if(addr)L.push('ADR;TYPE=WORK:;;'+addr+';;;;');if(web)L.push('URL:'+web);L.push('URL;TYPE=3VL:'+location.href.split('#')[0]);L.push('NOTE:Found on Three Village Local - threevillagelocal.com');L.push('END:VCARD');
    var bl=new Blob([L.join('\r\n')],{type:'text/vcard'}),x=document.createElement('a');x.href=URL.createObjectURL(bl);x.download=name.replace(/[^\w ]+/g,'').trim()+'.vcf';document.body.appendChild(x);x.click();setTimeout(function(){x.remove()},1500);toast('Contact card downloaded')}
  if(act==='share'){e.preventDefault();var u=location.href.split('#')[0];if(navigator.share)navigator.share({title:name,text:name+' on Three Village Local',url:u}).catch(function(){});else if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){toast('Link copied')})}});

/* tidy BD's own blocks */
$$('.make-connection').forEach(function(e){e.style.display='none'});
$$('.coverPhoto').forEach(function(e){e.style.display='none'});
$$('.content_w_sidebar > .col-md-3 .module').forEach(function(m){if(!txt(m)&&!m.querySelector('iframe'))m.style.display='none'});
})();
