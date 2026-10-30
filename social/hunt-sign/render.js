// node render.js <html> <out.pdf> <out.png>   (4x6 in: vector PDF for printing + 1200x1800 PNG preview)
const p=require('C:/Users/Matt/Documents/3vl-assets/sitecheck/node_modules/puppeteer-core');const fs=require('fs'),os=require('os'),path=require('path');
(async()=>{const [,,file,pdf,png]=process.argv;const dir=fs.mkdtempSync(path.join(os.tmpdir(),'hunt-'));
const b=await p.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:'new',args:['--user-data-dir='+dir,'--allow-file-access-from-files','--no-first-run']});
const pg=await b.newPage();await pg.setViewport({width:384,height:576,deviceScaleFactor:3.125});await pg.goto('file:///'+file,{waitUntil:'networkidle0'});await pg.evaluate(()=>document.fonts.ready);await new Promise(r=>setTimeout(r,600));
await pg.pdf({path:pdf,width:'4in',height:'6in',printBackground:true,pageRanges:'1'});await pg.screenshot({path:png});await b.close();})();
