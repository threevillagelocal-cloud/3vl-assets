// node site/member-dashboard/shots.js 115 499  -> _shots/<uid>-<width>.png (full page) + word-split check
const path=require('path'),fs=require('fs');
const puppeteer=require(path.join(__dirname,'..','..','sitecheck','node_modules','puppeteer-core'));
const ids=process.argv.slice(2).length?process.argv.slice(2):['115','499'];
(async()=>{
  const ud=path.join(require('os').tmpdir(),'md-shots-'+Date.now());
  const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:'new',userDataDir:ud,args:['--no-first-run','--allow-file-access-from-files']});
  try{
  for(const id of ids){
    for(const [w,mob] of [[1440,false],[412,true],[360,true],[320,true]]){
      const p=await b.newPage();
      await p.emulate({viewport:{width:w,height:900,deviceScaleFactor:mob?2:1,isMobile:mob,hasTouch:mob},userAgent:mob?'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36':'Mozilla/5.0 Chrome/124'});
      await p.goto('file:///'+path.join(__dirname,'_local',id+'.html').split(path.sep).join('/'),{waitUntil:'networkidle0',timeout:60000});
      await new Promise(r=>setTimeout(r,1600));
      const chk=await p.evaluate(()=>{
        const over=document.documentElement.scrollWidth>window.innerWidth+1;
        // word split check: any text node word whose characters land on two different lines
        const bad=[];const tw=document.createTreeWalker(document.getElementById('md'),NodeFilter.SHOW_TEXT);let n;
        while((n=tw.nextNode())){const t=n.textContent;const re=/\S+/g;let m;while((m=re.exec(t))){if(m[0].length<3)continue;const r=document.createRange();r.setStart(n,m.index);r.setEnd(n,m.index+m[0].length);const rs=[...r.getClientRects()].filter(x=>x.width>0);if(rs.length>1&&Math.abs(rs[0].top-rs[rs.length-1].top)>4)bad.push(m[0])}}
        return {over,bad:[...new Set(bad)].slice(0,10)}});
      const f=path.join(__dirname,'_shots',id+'-'+w+'.png');
      await p.screenshot({path:f,fullPage:true});
      console.log(id,w,JSON.stringify(chk));
      await p.close();
    }
  }}finally{await b.close();}
})();
