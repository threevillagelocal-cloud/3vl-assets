<script>
/* 3VL Smart Publisher page (/smart-publisher). Members-only page; this script picks the view:
   paid plan (VIP 1/8, Getting Noticed 2) -> the form; other plans -> locked card; ?ref=...&do=approve|changes -> review form.
   The real plan + monthly-limit check happens server side (3vl-site-guard smart_publisher.py). */
(function(){
function go(){
  var root=document.getElementById('sp3');if(!root)return;
  var fNew=null,fRev=null;
  [].forEach.call(document.querySelectorAll('form'),function(f){if(f.querySelector('[name=sp_type]'))fNew=f;if(f.querySelector('[name=sp_ref]'))fRev=f});
  var bc=document.body.className,m=bc.match(/session-plan-level-(\d+)/),plan=m?m[1]:'';
  var vip=plan==='1'||plan==='8',gn=plan==='2';
  var q=new URLSearchParams(location.search),ref=q.get('ref'),act=q.get('do');
  function show(id){['sp-new','sp-review','sp-lock'].forEach(function(x){var e=document.getElementById(x);if(e)e.hidden=(x!==id)})}
  if(fRev){document.getElementById('sp-reviewslot').appendChild(fRev)}
  if(fNew){document.getElementById('sp-formslot').appendChild(fNew)}
  if(ref&&fRev){
    show('sp-review');
    fRev.querySelector('[name=sp_ref]').value=ref;
    fRev.querySelector('[name=sp_decision]').value=act==='changes'?'changes':'approve';
    var ta=fRev.querySelector('[name=comments]'),grp=ta&&(ta.closest('.form-group')||ta.parentNode),btn=fRev.querySelector('[type=submit],button');
    if(act==='changes'){document.getElementById('sp-rh').textContent='What should we change?';document.getElementById('sp-rs').textContent='Tell us what to fix and we will send you a new preview, usually within 30 minutes.';if(ta)ta.required=true;if(btn){btn.textContent='Send my changes';btn.value='Send my changes'}}
    else{document.getElementById('sp-rh').textContent='Publish your page?';document.getElementById('sp-rs').textContent='Tap the button and we will publish it on the date you chose. You will get an email when it is live.';if(grp)grp.classList.add('sp-hide');if(btn){btn.textContent='Yes, publish it';btn.value='Yes, publish it'}}
    if(fNew)fNew.classList.add('sp-hide');
    return}
  if(!vip&&!gn){show('sp-lock');if(fNew)fNew.classList.add('sp-hide');return}
  show('sp-new');
  var u=document.getElementById('sp-usage');if(u)u.innerHTML='<span><b>'+(vip?'VIP':'Getting Noticed')+'</b> member</span><span>'+(vip?'2 pages a month (one every two weeks), plus social media':'1 page a month')+'</span>';
  /* social promotion is a VIP extra */
  var soc=fNew.querySelector('[name=sp_social]');if(soc&&!vip){var g=soc.closest('.form-group');if(g)g.classList.add('sp-hide')}
  /* go-live date only when "On a date I pick" */
  var pd=fNew.querySelector('[name=sp_publish_date]'),pdg=pd&&(pd.closest('.form-group')||pd.parentNode);
  function syncPub(){var c=fNew.querySelector('[name=sp_publish]:checked');if(pdg)pdg.classList.toggle('sp-hide',!(c&&c.value==='date'))}
  /* highlight the chosen option chips */
  function chips(){[].forEach.call(fNew.querySelectorAll('input[type=radio]'),function(r){var l=r.closest('label');if(l)l.classList.toggle('sp-on',r.checked)})}
  fNew.addEventListener('change',function(){syncPub();chips()});
  var first=fNew.querySelector('[name=sp_publish][value=asap]');if(first&&!fNew.querySelector('[name=sp_publish]:checked'))first.checked=true;
  var s1=fNew.querySelector('[name=sp_social][value=yes]');if(s1&&vip&&!fNew.querySelector('[name=sp_social]:checked'))s1.checked=true;
  syncPub();chips();
  try{fNew.addEventListener('submit',function(){gtag('event','smart_publisher_submit',{plan:vip?'vip':'gn'})})}catch(e){}
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
</script>
