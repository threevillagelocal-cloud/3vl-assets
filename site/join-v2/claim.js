(function(){
/* BD claim flow: profile "Claim Listing" -> /join?claim=<hash>. Carry the hash onto every /checkout/ link (also links inside the
   plan pop-ups, which call window.jvClaim after they open) and relabel the free button. Keep this if /join is redesigned. */
function run(root){try{var c=new URLSearchParams(location.search).get('claim');if(!c||c==='hide')return;
[].forEach.call((root||document).querySelectorAll('a[href^="/checkout/"]'),function(a){var h=a.getAttribute('href');
if(h.indexOf('claim=')<0){a.setAttribute('href',h+(h.indexOf('?')<0?'?':'&')+'claim='+encodeURIComponent(c));}
if(h.indexOf('/checkout/6')===0){a.textContent='Claim my free page';}});}catch(e){}}
window.jvClaim=run;run(document);
})();
