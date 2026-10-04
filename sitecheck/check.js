// 3VL nightly site check. Loads every important page like a visitor (scrolls, waits), and checks that the content really
// appears: category lists load ALL their businesses, homepage sections are filled, events/blog render, no script errors,
// no broken images, no sideways scrolling on phones. Writes out/report.json; never changes the site.
// Usage: node check.js [--quick]
const puppeteer = require('puppeteer-core');
const fs = require('fs'), path = require('path'), os = require('os'), https = require('https');
const SITE = 'https://www.threevillagelocal.com';
const CHROME = process.env.CHROME || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : '/usr/bin/google-chrome');
const OUT = path.join(__dirname, 'out');
const QUICK = process.argv.includes('--quick');

function getJSON(u) { return new Promise((res) => https.get(u, { headers: { 'User-Agent': 'Mozilla/5.0' } }, r => { let b = ''; r.on('data', c => b += c); r.on('end', () => { try { res(JSON.parse(b)) } catch (e) { res(null) } }) }).on('error', () => res(null))) }
const sleep = ms => new Promise(r => setTimeout(r, ms));
// third-party noise that is not ours to fix
const IGNORE = /facebook|fbevents|doubleclick|googletagmanager|google-analytics|gtag|googlesyndication|hotjar|clarity\.ms|sweetalert|ResizeObserver loop|Failed to load resource: net::ERR_BLOCKED|chrome-extension/i;
const OURS = /threevillagelocal\.com|3vl-share|3vl-assets|optimizecdn\.com/i;

async function buildList() {
  const sub = await getJSON('https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/search/subcats.json');
  const idx = await getJSON('https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/search/index.json');
  const ev = await getJSON('https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/weekender/live/events.json');
  const L = [];
  L.push({ u: '/', kind: 'home' }, { u: '/', kind: 'home', phone: true });
  L.push({ u: '/categories', kind: 'categories' }, { u: '/events', kind: 'events' }, { u: '/events-calendar', kind: 'events' }, { u: '/blog', kind: 'blog' });
  for (const p of ['/join', '/newsletter', '/locallistings', '/app', '/promotion', '/smart-publisher', '/three-village-farmers-market', '/login', '/about/contact'])
    L.push({ u: p, kind: 'page' });
  L.push({ u: '/search_results?q=pizza', kind: 'search' }, { u: '/search_results?q=plumber', kind: 'search' });
  const cats = sub && sub.cats ? Object.keys(sub.cats) : [];
  for (const c of cats) L.push({ u: '/' + c, kind: 'category' });
  if (cats.length) L.push({ u: '/' + cats[0], kind: 'category', phone: true });
  // specialty pages: a different slice every night so all ~260 get covered over the week
  const specs = sub && sub.cats ? Object.values(sub.cats).flatMap(c => c.s.map(x => x[0])) : [];
  const day = Math.floor(Date.now() / 864e5), n = QUICK ? 5 : 40;
  for (let i = 0; i < Math.min(n, specs.length); i++) L.push({ u: '/' + specs[(day * n + i) % specs.length], kind: 'category' });
  // every VIP profile + a few others
  const mem = idx && idx.members ? idx.members : [];
  for (const m of mem.filter(m => m.p === 'vip')) L.push({ u: m.u.replace(SITE, ''), kind: 'profile' });
  const others = mem.filter(m => m.p !== 'vip');
  for (let i = 0; i < Math.min(QUICK ? 2 : 6, others.length); i++) L.push({ u: others[(day * 7 + i * 13) % others.length].u.replace(SITE, ''), kind: 'profile' });
  // upcoming event pages + newest blog posts
  const evs = ev && ev.events ? ev.events.filter(e => e.page && e.page.indexOf(SITE + '/events/') === 0).slice(0, QUICK ? 1 : 4) : [];
  for (const e of evs) L.push({ u: e.page.replace(SITE, ''), kind: 'event' });
  L.push({ u: '/blog/the-ultimate-culper-spy-day-blueprint-setaukets-spy-ring-weekend-oct-3', kind: 'post' });
  return QUICK ? L.filter((x, i) => i < 40) : L;
}

async function checkPage(browser, item) {
  const page = await browser.newPage();
  const W = item.phone ? 390 : 1366;
  await page.setViewport(item.phone ? { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true } : { width: 1366, height: 900 });
  await page.setCacheEnabled(false);
  await page.setUserAgent(item.phone ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36');
  const res = { url: SITE + item.u, kind: item.kind, phone: !!item.phone, problems: [], notes: [] };
  const errs = [], bad = [];
  page.on('pageerror', e => { if (!IGNORE.test(e.message + (e.stack || ''))) errs.push(e.message.slice(0, 160)) });
  page.on('response', r => { const u = r.url(); if (r.status() >= 400 && OURS.test(u) && !/favicon|\.map$|\/wapi\/stats|apple-touch/i.test(u)) bad.push(r.status() + ' ' + u.slice(0, 140)) });
  const t0 = Date.now();
  let status = 0;
  try {
    const resp = await page.goto(SITE + item.u + (item.u.includes('?') ? '&' : '?') + 'sitecheck=' + Date.now(), { waitUntil: 'networkidle2', timeout: 60000 });
    status = resp ? resp.status() : 0;
  } catch (e) { res.problems.push('page did not finish loading in 60s (' + e.message.slice(0, 60) + ')') }
  res.status = status; res.ms = Date.now() - t0;
  if (status >= 400) res.problems.push('HTTP ' + status);
  await sleep(2500);
  try {
    // scroll like a visitor (gradually), so lazy content and load-more fire
    for (let i = 0; i < 12; i++) { const done = await page.evaluate(() => { window.scrollBy(0, innerHeight * 0.9); return innerHeight + scrollY >= document.body.scrollHeight - 5 }); await sleep(450); if (done) break }
    if (item.kind === 'category') {
      // keep scrolling until BD says everything is loaded (or 40s)
      for (let i = 0; i < 40; i++) {
        const s = await page.evaluate(() => ({ cur: +((document.querySelector('.current__amount__js') || {}).textContent || 0), tot: +((document.querySelector('.total__js') || {}).textContent || 0) }));
        if (!s.tot || s.cur >= s.tot) break;
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await sleep(1000);
      }
    }
    await sleep(1200);
    const d = await page.evaluate((kind) => {
      const q = s => document.querySelectorAll(s).length;
      const imgs = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.src && !/^data:/.test(i.src) && i.offsetParent !== null).map(i => i.src.slice(0, 120));
      const o = { title: document.title, textLen: (document.body.innerText || '').length, brokenImgs: imgs, overflow: document.documentElement.scrollWidth - innerWidth,
        htmlCls: document.documentElement.className.slice(0, 200) };
      if (kind === 'category' || kind === 'search') {
        o.vip = q('.p3-vwrap'); o.reg = q('.p3-rcard'); o.cur = +((document.querySelector('.current__amount__js') || {}).textContent || 0);
        o.tot = +((document.querySelector('.total__js') || {}).textContent || 0); o.p3 = !!document.getElementById('p3vl'); o.none = !!document.getElementById('p3none');
      }
      if (kind === 'home') { o.eat = q('#wk-eat .wk-sp'); o.picks = q('#wk-top .wk-pick, #wk-top article, #wk-top .wk-card'); o.top = !!document.getElementById('wk-top'); o.secs = q('.wk-sec') }
      if (kind === 'events') { o.cards = q('.tvc-cards > *, .tvc-card, .tvc-ev'); o.tvc = /tvc-(on|done)/.test(document.documentElement.className + ' ' + document.body.className) }
      if (kind === 'blog') o.cards = q('.p3-bcard, .p3-bgrid > *');
      if (kind === 'categories') o.tiles = q('#p3grid > *, .p3-cat, .p3-tile');
      if (kind === 'event') o.ev = !!document.getElementById('ev') || q('.ev-on, #ev-next') > 0;
      if (kind === 'profile') o.h1 = (document.querySelector('h1') || {}).textContent || '';
      return o;
    }, item.kind);
    res.data = d;
    if (d.textLen < 400) res.problems.push('page is almost empty (' + d.textLen + ' characters of text)');
    if (d.brokenImgs.length) res.problems.push(d.brokenImgs.length + ' broken image(s): ' + d.brokenImgs.slice(0, 3).join(' , '));
    if (d.overflow > 2) res.problems.push('sideways scrolling: page is ' + d.overflow + 'px wider than the screen');
    if (item.kind === 'category') {
      if (!d.p3) res.problems.push('our page design did not load (BD default layout showing)');
      else if (d.tot && d.vip + d.reg < d.tot) res.problems.push('only ' + (d.vip + d.reg) + ' of ' + d.tot + ' businesses loaded (load-more stalled)');
      else if (!d.tot && d.vip + d.reg === 0 && !d.none) res.notes.push('no businesses listed');
    }
    if (item.kind === 'search' && d.vip + d.reg === 0) res.problems.push('search returned no results');
    if (item.kind === 'home') { if (!d.top) res.problems.push('homepage content (Things to Do) missing'); if (d.eat < 4) res.problems.push('Eat & Drink shows ' + d.eat + ' cards (expected 6)') }
    if (item.kind === 'events' && !d.cards) res.problems.push('no events showing on the calendar');
    if (item.kind === 'blog' && d.cards < 3) res.problems.push('blog shows ' + d.cards + ' posts');
    if (item.kind === 'categories' && d.tiles < 5) res.problems.push('category tiles missing');
    if (item.kind === 'event' && !d.ev) res.problems.push('event page design did not load');
    if (item.kind === 'profile' && !d.h1.trim()) res.problems.push('profile has no business name heading');
  } catch (e) { res.problems.push('check failed: ' + e.message.slice(0, 100)) }
  if (errs.length) res.problems.push('script error: ' + [...new Set(errs)].slice(0, 2).join(' | '));
  if (bad.length) res.problems.push('failed files: ' + [...new Set(bad)].slice(0, 3).join(' , '));
  if (res.ms > 20000) res.notes.push('slow: ' + (res.ms / 1000).toFixed(1) + 's to load');
  await page.close();
  return res;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const list = await buildList();
  const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'sitecheck-'));
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: prof, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const results = [];
  for (const item of list) {
    let r = await checkPage(browser, item);
    if (r.problems.length) { await sleep(3000); const r2 = await checkPage(browser, item); r2.retried = true; if (!r2.problems.length) r2.notes.push('passed on 2nd try (first try: ' + r.problems.join('; ') + ')'); r = r2 }
    results.push(r);
    console.log((r.problems.length ? 'FAIL ' : 'ok   ') + (r.phone ? '[phone] ' : '') + item.u + (r.problems.length ? '  -> ' + r.problems.join(' | ') : '') + (r.notes.length ? '  (' + r.notes.join('; ') + ')' : ''));
  }
  await browser.close(); fs.rmSync(prof, { recursive: true, force: true });
  const failed = results.filter(r => r.problems.length);
  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify({ when: new Date().toISOString(), checked: results.length, failed: failed.length, results }, null, 1));
  console.log('\nchecked', results.length, 'pages,', failed.length, 'with problems');
})();
