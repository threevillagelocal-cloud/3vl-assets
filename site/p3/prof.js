/* 3VL premium business profile v3 (MOCKUP - not wired into the site yet).
   Hero = the business's OWN uploaded cover photo (never stock), logo card overlapping it,
   then organized sections: About / Specialties / Reviews / Articles, with a Contact & details card on the right. */
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
var locEl=row('location'),addr=locEl?(locEl.innerText||'').split(/\n+/).map(function(x){return x.trim()}).filter(function(x){return x&&!/^united states$/i.test(x)}).join(', ').replace(/Setauket- East Setauket/,'East Setauket').replace(/New York,?\s*(\d{5})/,'NY $1'):txt($('.profile-header-location',hdr));
var web=($('a.weblink')||{}).href||'',msg=($('.btn-send_message_action',hdr)||{}).href||'';
var rating=(txt($('.the-average-rating',hdr)).match(/([\d.]+)\s*\/\s*5/)||[])[1],count=(txt($('.the-review-count',hdr)).match(/\d+/)||[])[0];
var verified=!!$('.member-badges img[alt*="Verified"]'),vip=!!$('.member-badges img[alt*="VIP"]');
var cover=($('.coverPhoto')||{}).src||'';
var town=(addr.split(',').slice(-2).join(',')||'').trim();
var maps='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(name+' '+addr);
function track(act){try{if(window.gtag)window.gtag('event','vip_profile_click',{action:act,business:name,business_id:uid})}catch(e){}}

/* ---------- hero ---------- */
var h='<section id="pf" class="pf'+(cover?'':' pf-nocover')+'">'+
  (cover?'<div class="pf-cover"><img src="'+esc(cover)+'" alt="'+esc(name)+' cover photo"></div>':'<div class="pf-cover pf-cover-empty"></div>')+
  '<div class="pf-card"><div class="pf-idrow"><div class="pf-logo"><img src="'+esc(logo)+'" alt="'+esc(name)+' logo"></div>'+
  '<div class="pf-id">'+(vip?'<span class="pf-vip">&#11088; VIP LOCAL BUSINESS</span>':'')+'<h1 class="pf-name">'+esc(name)+'</h1>'+
  '<p class="pf-meta">'+esc(cat)+(town?' <i>&#9679;</i> '+esc(town):'')+'</p>'+
  '<div class="pf-badges" id="pf-badges">'+(verified?'<span class="pf-b pf-bok">&#10003; Verified</span>':'')+
  (rating?'<a class="pf-b pf-bstar" href="#pf-reviews">&#9733; '+esc((+rating).toFixed(1))+' <small>'+esc(count||0)+' review'+(count==='1'?'':'s')+'</small></a>':'')+'</div></div></div>'+
  '<nav class="pf-bar" aria-label="Contact '+esc(name)+'">'+
  (tel?'<a class="pf-a pf-call" data-act="call" href="tel:'+tel+'">&#128222; <b class="pf-long">'+telF+'</b><span class="pf-short">Call</span></a><a class="pf-a pf-text" data-act="text" href="sms:'+tel+'">&#128172; <span>Text</span></a>':'')+
  '<a class="pf-a" data-act="directions" href="'+esc(maps)+'" target="_blank" rel="noopener">&#128205; <span><b class="pf-long">Directions</b><b class="pf-short">Map</b></span></a>'+
  '<button type="button" class="pf-a" data-act="save_contact">&#128100; <span><b class="pf-long">Save contact</b><b class="pf-short">Save</b></span></button>'+
  (msg?'<a class="pf-a" data-act="message" href="'+esc(msg)+'">&#9993;&#65039; <span>Message</span></a>':'')+
  (web?'<a class="pf-a pf-web" data-act="website" href="'+esc(web)+'" target="_blank" rel="noopener">&#127760; <span>Website</span></a>':'')+
  '<button type="button" class="pf-a" data-act="share">&#128279; <span>Share</span></button></nav></div>'+
  '<nav class="pf-secnav" id="pf-secnav"></nav><div class="pf-toast" id="pf-toast"></div></section>';
hdr.insertAdjacentHTML('beforebegin',h);document.documentElement.classList.add('pf-on');
var pf=document.getElementById('pf');

/* ---------- reorganize BD's tabs into sections ---------- */
var tabs=$('.member-profile-tabs'),panes=tabs?$$('.tab-pane',tabs):[],main=document.createElement('div');main.className='pf-main';
var navItems=[];
function tabLink(p){return $('.profile-tabs-nav a[href="#'+p.id+'"]')}
function label(p){var a=tabLink(p);return a?txt(a).replace(/\s*\(\d+\)$/,''):''}
function num(p){var a=tabLink(p);var m=a&&txt(a).match(/\((\d+)\)$/);return m?m[1]:''}
function section(key,title,count,nodes){if(!nodes.length)return;var s=document.createElement('section');s.className='pf-sec';s.id='pf-'+key;
  s.innerHTML='<h2 class="pf-h2">'+esc(title)+(count?' <span>'+esc(count)+'</span>':'')+'</h2>';nodes.forEach(function(n){s.appendChild(n)});main.appendChild(s);navItems.push([key,title])}
var contactNodes=[];
if(panes[0]){var kids=[].slice.call(panes[0].children),about=[];
  kids.forEach(function(k,i){var n2=kids[i+2];
    if(k.classList.contains('table-view')||k.id==='map-canvas'||(k.classList.contains('alert')&&n2&&n2.id==='map-canvas'))contactNodes.push(k);else about.push(k)});
  section('about','About',0,about)}
panes.slice(1).forEach(function(p){var t=label(p),key=/review/i.test(t)?'reviews':/blog|article/i.test(t)?'articles':/special/i.test(t)?'specialties':t.toLowerCase().replace(/\W+/g,'-');
  var kids=[].slice.call(p.children).filter(function(k,i){return !(k.tagName==='H2'&&i<2)&&!(k.tagName==='HR'&&i<3)});section(key,t,num(p),kids)});
if(tabs){tabs.parentNode.insertBefore(main,tabs);tabs.style.display='none'}
var side=$('.content_w_sidebar > .col-md-3');
if(side){var cc=document.createElement('section');cc.className='pf-contact';cc.id='pf-contact';
  cc.innerHTML='<h2 class="pf-h2">Contact &amp; details</h2>'+(tel?'<a class="pf-cphone" data-act="call" href="tel:'+tel+'">&#128222; '+telF+'</a>':'')+(addr?'<p class="pf-caddr">&#128205; '+esc(addr)+'</p>':'');
  contactNodes.forEach(function(n){cc.appendChild(n)});side.insertBefore(cc,side.firstChild);navItems.push(['contact','Contact'])}
$('#pf-secnav').innerHTML=navItems.map(function(n,i){return '<a href="#pf-'+n[0]+'"'+(i?'':' class="is-on"')+'>'+esc(n[1])+'</a>'}).join('');

fetch(BASE+'vip_meta.json').then(function(r){return r.json()}).then(function(M){var m=M[uid];if(!m)return;var b=$('#pf-badges');
  if(m.since){var y=new Date().getFullYear()-(+m.since);if(y>0)b.insertAdjacentHTML('beforeend','<span class="pf-b pf-bcal">Since '+esc(m.since)+' <small>'+y+' yrs</small></span>')}}).catch(function(){});

(function(img){if(!img)return;function go(){try{var w=img.naturalWidth,h=img.naturalHeight;if(!w||!h)return;var c=document.createElement('canvas'),k=Math.min(1,700/Math.max(w,h));c.width=Math.round(w*k);c.height=Math.round(h*k);
  var x=c.getContext('2d');x.drawImage(img,0,0,c.width,c.height);var d=x.getImageData(0,0,c.width,c.height).data,W=c.width,H=c.height,t=H,l=W,r=0,b=0;
  for(var y=0;y<H;y++)for(var X=0;X<W;X++){var i=(y*W+X)*4;if(d[i+3]>20&&(d[i]<235||d[i+1]<235||d[i+2]<235)){if(y<t)t=y;if(y>b)b=y;if(X<l)l=X;if(X>r)r=X}}
  if(r<=l||b<=t||(r-l)*(b-t)>W*H*.92)return;var p=Math.round(Math.max(r-l,b-t)*.04);l=Math.max(0,l-p);t=Math.max(0,t-p);r=Math.min(W-1,r+p);b=Math.min(H-1,b+p);
  var o=document.createElement('canvas');o.width=r-l+1;o.height=b-t+1;o.getContext('2d').drawImage(c,l,t,o.width,o.height,0,0,o.width,o.height);img.onload=null;img.src=o.toDataURL('image/png')}catch(e){}}
  if(img.complete&&img.naturalWidth)go();else img.onload=go})($('.pf-logo img',pf));

function toast(t){var e=$('#pf-toast');e.textContent=t;e.classList.add('is-on');clearTimeout(toast.h);toast.h=setTimeout(function(){e.classList.remove('is-on')},3000)}
document.addEventListener('click',function(e){var a=e.target.closest('#pf [data-act], #pf-contact [data-act]');if(!a)return;var act=a.getAttribute('data-act');track(act);
  if(act==='save_contact'){e.preventDefault();var L=['BEGIN:VCARD','VERSION:3.0','FN:'+name,'ORG:'+name];if(tel)L.push('TEL;TYPE=WORK,VOICE:+1'+tel);if(addr)L.push('ADR;TYPE=WORK:;;'+addr+';;;;');if(web)L.push('URL:'+web);L.push('URL;TYPE=3VL:'+location.href.split('#')[0]);L.push('NOTE:Found on Three Village Local - threevillagelocal.com');L.push('END:VCARD');
    var bl=new Blob([L.join('\r\n')],{type:'text/vcard'}),x=document.createElement('a');x.href=URL.createObjectURL(bl);x.download=name.replace(/[^\w ]+/g,'').trim()+'.vcf';document.body.appendChild(x);x.click();setTimeout(function(){x.remove()},1500);toast('Contact card downloaded')}
  if(act==='share'){e.preventDefault();var u=location.href.split('#')[0];if(navigator.share)navigator.share({title:name,text:name+' on Three Village Local',url:u}).catch(function(){});else if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){toast('Link copied')})}});
if('IntersectionObserver' in window){var links={};$$('#pf-secnav a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
  var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting&&links[en.target.id]){for(var k in links)links[k].classList.remove('is-on');links[en.target.id].classList.add('is-on')}})},{rootMargin:'-30% 0px -60% 0px'});
  $$('.pf-sec, .pf-contact').forEach(function(s){io.observe(s)})}
$$('.make-connection, .coverPhoto, ol.breadcrumb').forEach(function(e){e.style.display='none'});
$$('.content_w_sidebar > .col-md-3 .social_share_buttons').forEach(function(e){e.style.display='none'});
})();
