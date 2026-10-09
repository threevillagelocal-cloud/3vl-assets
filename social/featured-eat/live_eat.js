// node live_eat.js  -> prints JSON: the business names in the live homepage's Eat & Drink section, in order.
// The kit must show exactly what the live homepage shows; build.py stops if it can't.
const puppeteer = require('puppeteer-core');
const fs = require('fs'), path = require('path'), os = require('os');
const CHROME = process.env.CHROME || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : '/usr/bin/google-chrome');
(async () => {
  const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'feat-live-'));
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: prof, args: ['--no-sandbox'],
    defaultViewport: { width: 1366, height: 900 } });
  try {
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36');
    await page.goto('https://www.threevillagelocal.com/?kit=' + Date.now(), { waitUntil: 'networkidle2', timeout: 90000 });
    // weekender.js redraws the section from the live feed; wait until it has cards and has settled
    let last = '', same = 0;
    for (let i = 0; i < 40 && same < 4; i++) {
      await new Promise(r => setTimeout(r, 500));
      const cur = await page.evaluate(() => [...document.querySelectorAll('#wk-eat .wk-sp .wk-spbiz')].map(b => b.textContent.trim()).join('|'));
      same = cur && cur === last ? same + 1 : 0; last = cur;
    }
    process.stdout.write(JSON.stringify(last ? last.split('|') : []));
  } finally {
    await browser.close(); fs.rmSync(prof, { recursive: true, force: true });
  }
})().catch(e => { console.error(e.message); process.exit(1); });
