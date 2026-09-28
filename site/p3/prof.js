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

/* logo: trim baked-in white margins */
(function(img){if(!img)return;function go(){try{var w=img.naturalWidth,h=img.naturalHeight;if(!w||!h)return;var c=document.createElement('canvas'),k=Math.min(1,700/Math.max(w,h));c.width=Math.round(w*k);c.height=Math.round(h*k);
  var x=c.getContext('2d');x.drawImage(img,0,0,c.width,c.height);var d=x.getImageData(0,0,c.width,c.height).data,W=c.width,H=c.height,t=H,l=W,r=0,b=0;
  for(var y=0;y<H;y++)for(var X=0;X<W;X++){var i=(y*W+X)*4;if(d[i+3]>20&&(d[i]<235||d[i+1]<235||d[i+2]<235)){if(y<t)t=y;if(y>b)b=y;if(X<l)l=X;if(X>r)r=X}}
  if(r<=l||b<=t||(r-l)*(b-t)>W*H*.92)return;var p=Math.round(Math.max(r-l,b-t)*.05);l=Math.max(0,l-p);t=Math.max(0,t-p);r=Math.min(W-1,r+p);b=Math.min(H-1,b+p);
  var o=document.createElement('canvas');o.width=r-l+1;o.height=b-t+1;o.getContext('2d').drawImage(c,l,t,o.width,o.height,0,0,o.width,o.height);img.onload=null;img.removeAttribute('width');img.removeAttribute('height');img.src=o.toDataURL('image/png')}catch(e){}}
  if(img.complete&&img.naturalWidth)go();else img.onload=go})($('.profile-image img',hdr));
/* About section first in the overview tab (above Contact Information / Company Details) */
(function(){var ab=$('.overview-tab-about-me');if(!ab)return;var fd=$('.field-about_me',ab);if(!fd||!fd.textContent.trim())return;var pane=ab.closest('.tab-pane');if(pane&&pane.firstElementChild!==ab)pane.insertBefore(ab,pane.firstElementChild);
  /* designed bios carry their own headline: drop BD's plain "About" heading */
  var f1=[].filter.call(fd.children,function(c){return !c.classList.contains('clearfix')})[0],h=$('.about-member-blurb',ab);if(h&&f1&&(f1.tagName==='DIV'||/^H[1-3]$/.test(f1.tagName)))h.style.setProperty('display','none','important')})();
/* Contact Information + Company Details merged into one compact "Business details" card grid */
(function(){var pane=$('.tab-pane.active')||$('.tab-pane');if(!pane||$('.pf-facts',pane))return;
  var tvs=$$('.table-view',pane).filter(function(t){return !t.closest('.overview-tab-about-me')&&$('.table-view-group',t)});if(!tvs.length)return;
  var box=document.createElement('div');box.className='pf-facts';box.innerHTML='<h2>Business details</h2><div class="pf-fgrid"></div>';var grid=$('.pf-fgrid',box);
  tvs.forEach(function(t){$$('.table-view-group',t).forEach(function(g){
    if(g.classList.contains('table-display-company'))return;
    var v=$('.col-sm-8',g);if(!v||!v.textContent.trim()&&!v.querySelector('a,img,i'))return;
    g.classList.add('pf-fact');if(v.textContent.trim().length>90)g.classList.add('pf-wide');grid.appendChild(g)})});
  if(!grid.children.length)return;
  /* raw URLs -> short labels (long links overflowed the tiles) */
  $$('.pf-fact a[href^="http"]',grid).forEach(function(a){var tx=a.textContent.trim();if(!/^(https?:\/\/|www\.)/i.test(tx))return;
    var lab=((($('.bold',a.closest('.pf-fact'))||{}).textContent)||'').toLowerCase(),host='';try{host=new URL(a.href).hostname.replace(/^www\./,'')}catch(e){}
    a.textContent=/appoint|book|schedul/.test(lab)?'Book an appointment':/website|site/.test(lab)?'Visit website':(host||'Open link');a.setAttribute('title',a.href);a.classList.add('pf-link')});
  /* useful facts first, long text blocks last */
  var ord=['phone','website','address','rep_matters','booking','social','experience','affiliation','cv','credentials','awards'];
  function rank(g){if(g.classList.contains('pf-wide'))return 99;var c=g.className;for(var i=0;i<ord.length;i++)if(c.indexOf(ord[i])>-1)return i;return 50}
  [].slice.call(grid.children).map(function(g,i){return [rank(g),i,g]}).sort(function(a,b){return a[0]-b[0]||a[1]-b[1]}).forEach(function(x){grid.appendChild(x[2])});
  var ab=$('.overview-tab-about-me',pane);if(ab&&ab.parentNode===pane)pane.insertBefore(box,ab.nextSibling);else pane.insertBefore(box,tvs[0]);
  tvs.forEach(function(t){t.style.display='none'})})();
/* tidy */
$$('.make-connection').forEach(function(e){e.style.display='none'});
$$('.content_w_sidebar > .col-md-3 .module').forEach(function(m){if(!m.textContent.trim()&&!m.querySelector('iframe,img'))m.style.display='none'});
document.addEventListener('click',function(e){var a=e.target.closest('.member_profile [data-act], .member_profile .btn-send_message_action, .member_profile .btn-write_a_review_for, .member_profile a.weblink');if(!a)return;
  track(a.getAttribute('data-act')||(a.classList.contains('weblink')?'website':a.classList.contains('btn-write_a_review_for')?'review':'message'))});
})();
