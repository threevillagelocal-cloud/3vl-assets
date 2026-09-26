/* MOCKUP: "Happening Today in Three Village" strip for the homepage.
   Data: hourly weather-proof feed weekender/live/events.json (photos, venues, cancellations) + BD /event-calendar-json (links to our own event pages) + NWS for today's weather. */
(function(){
var host=document.querySelector('.homepage-sections');if(!host||document.getElementById('td'))return;
var FEED='https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/weekender/live/events.json';
var DOW=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],MON=['January','February','March','April','May','June','July','August','September','October','November','December'];
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function tm(d){var h=d.getHours(),m=d.getMinutes(),a=h>=12?'PM':'AM';h=h%12||12;return h+(m?':'+(m<10?'0':'')+m:'')+' '+a}
var IMG='https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@efc082d3ec73/events-cal/img/';
function venuePhoto(e){var b=((e.src||'')+' '+(e.venue||'')+' '+(e.addr||'')).toLowerCase();
  if(/emmaclark|emma s|library/.test(b))return IMG+['emma-clark.jpg','emma-clark-2.jpg','emma-clark-3.jpg'][(e.title||'').length%3];
  if(/west meadow/.test(b))return IMG+'west-meadow.jpg';if(/cedar beach|sinai/.test(b))return IMG+'beach-sunset.jpg';return IMG+'port-jeff.jpg'}
function key(t){return String(t||'').toLowerCase().replace(/[^a-z0-9]/g,'').slice(0,40)}
var now=new Date(),t0=new Date(now.getFullYear(),now.getMonth(),now.getDate()),t1=new Date(t0.getTime()+864e5),t2=new Date(t0.getTime()+2*864e5);
var box=document.createElement('section');box.id='td';box.className='td';
box.innerHTML='<div class="td-in"><div class="td-head"><span class="td-live"><i></i>LIVE</span><h2>Happening Today <span>in Three Village</span></h2><span class="td-date">'+DOW[now.getDay()]+', '+MON[now.getMonth()]+' '+now.getDate()+'<b id="td-wx"></b></span><a class="td-all" href="/events-calendar">Full calendar &rarr;</a></div><div class="td-wrap"><button class="td-arrow td-prev" aria-label="Scroll left">&#8249;</button><div class="td-row" id="td-row"><p class="td-load">Loading today&rsquo;s events&hellip;</p></div><button class="td-arrow td-next" aria-label="Scroll right">&#8250;</button></div></div>';
host.parentNode.insertBefore(box,host);
Promise.all([fetch(FEED+'?v='+Math.floor(Date.now()/3e5)).then(function(r){return r.json()}),fetch('/event-calendar-json').then(function(r){return r.json()}).catch(function(){return []})]).then(function(res){
  var feed=res[0].events||[],bd=(res[1].result||res[1]||[]),links={};
  bd.forEach(function(x){var d=new Date(+x.start);links[key(x.title)+'|'+d.toDateString()]=String(x.url).indexOf('//')===0?location.protocol+x.url:x.url});
  var evs=feed.map(function(e){e.s=new Date(e.start);e.e=new Date(e.end||e.start);if(e.e<=e.s)e.e=new Date(e.s.getTime()+(e.allday?864e5:5400e3));return e});
  var today=evs.filter(function(e){return e.s<t1&&e.e>now});
  if(today.filter(function(e){return !e.status}).length<6)today=today.concat(evs.filter(function(e){return e.s>=t1&&e.s<t2}));
  today.sort(function(a,b){return (a.status?1:0)-(b.status?1:0)||a.s-b.s});   /* what's on first, cancellations last */
  var row=document.getElementById('td-row');
  if(!today.length){row.innerHTML='<p class="td-load">Quiet day in Three Village. <a href="/events-calendar">See what&rsquo;s coming up &rarr;</a></p>';return}
  row.innerHTML=today.slice(0,14).map(function(e,i){
    var live=!e.status&&e.s<=now&&e.e>now,tomorrow=e.s>=t1;
    var when=e.status?e.status:live?'Happening now':tomorrow?'Tomorrow '+(e.allday?'':tm(e.s)):(e.allday?'All day':tm(e.s));
    var href=links[key(e.title)+'|'+e.s.toDateString()]||e.url||'/events-calendar';
    return '<a class="td-card'+(e.status?' is-off':'')+(live?' is-live':'')+'" href="'+esc(href)+'" style="--i:'+i+'"><div class="td-pic">'+'<img src="'+esc(e.img||venuePhoto(e))+'" alt="" loading="lazy">'+
      '<span class="td-when">'+(live?'<i></i>':'')+esc(when)+'</span>'+(e.status?'<span class="td-rib">'+esc(e.status)+'</span>':'')+'</div><div class="td-b"><b>'+esc(e.title)+'</b><small>&#128205; '+esc(e.venue||'Three Village')+'</small></div></a>'}).join('');
  var sc=function(d){row.scrollBy({left:d*row.clientWidth*.85,behavior:'smooth'})};
  box.querySelector('.td-prev').onclick=function(){sc(-1)};box.querySelector('.td-next').onclick=function(){sc(1)};
}).catch(function(){box.remove()});
fetch('https://api.weather.gov/gridpoints/OKX/62,57/forecast',{headers:{Accept:'application/geo+json'}}).then(function(r){return r.json()}).then(function(d){var p=(d.properties.periods||[])[0];if(p)document.getElementById('td-wx').textContent=' · '+p.temperature+'° '+p.shortForecast}).catch(function(){});
})();
