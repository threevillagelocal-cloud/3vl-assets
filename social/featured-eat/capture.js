// node capture.js <page.html> <width> <height> <out.mp4>  - renders the page's render(t) at 30 fps into an MP4
const puppeteer = require('puppeteer-core');
const ffmpeg = require('ffmpeg-static');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
const [page_, W, H, OUT] = process.argv.slice(2);
const FPS = 30;
const CHROME = process.env.CHROME || (process.platform === 'win32' ? 'C:/Program Files/Google/Chrome/Application/chrome.exe' : '/usr/bin/google-chrome');
(async () => {
  const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'feat-anim-'));
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', userDataDir: prof,
    args: ['--no-sandbox', '--hide-scrollbars', '--force-color-profile=srgb'], defaultViewport: { width: +W, height: +H, deviceScaleFactor: 1 } });
  const page = await browser.newPage();
  await page.goto('file:///' + path.resolve(page_).split(String.fromCharCode(92)).join('/') + '?capture', { waitUntil: 'networkidle0' });
  await page.evaluate(async () => { await document.fonts.ready; });
  const dur = await page.evaluate(() => DURATION);
  const fr = fs.mkdtempSync(path.join(os.tmpdir(), 'feat-frames-'));
  for (let i = 0; i < Math.round(dur * FPS); i++) {
    await page.evaluate(t => render(t), i / FPS);
    await page.screenshot({ path: path.join(fr, `f${String(i + 1).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 95 });
  }
  await browser.close();
  execFileSync(ffmpeg, ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(fr, 'f%05d.jpg'),
    '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-movflags', '+faststart', OUT]);
  fs.rmSync(fr, { recursive: true, force: true }); fs.rmSync(prof, { recursive: true, force: true });
  console.log('wrote', OUT);
})();
