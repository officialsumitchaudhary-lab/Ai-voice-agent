// Renders the ad frame by frame with headless Chromium.
// node render.mjs <fmt v|s> <outDir> [--cut ad|full] [--times 1,2,3] [--workers 4]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const fmt = args[0] === 's' ? 's' : 'v';
const outDir = path.resolve(args[1] || 'frames');
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const workers = Number(opt('--workers', 4));
const times = opt('--times', null);
const cut = opt('--cut', 'ad');
const W = 1080, H = fmt === 's' ? 1080 : 1920, FPS = 30;
fs.mkdirSync(outDir, { recursive: true });
const url = 'file://' + path.join(here, 'meera-ad.html') + '?render=1&fmt=' + fmt + '&cut=' + cut;

// read the timeline once: the video's length follows the call recording
const probe = await chromium.launch();
const pp = await probe.newPage({ viewport: { width: W, height: H } });
await pp.goto(url);
await pp.evaluate(() => window.__ready);
const timeline = await pp.evaluate(() => window.__timeline);
await probe.close();
fs.writeFileSync(path.join(outDir, `timeline_${fmt}.json`), JSON.stringify(timeline, null, 1));
const DUR = timeline.dur;

const jobs = times ? times.split(',').map((t, i) => ({ t: Number(t), name: `still_${fmt}_${String(i).padStart(2, '0')}_${t}s.png` }))
  : Array.from({ length: Math.round(FPS * DUR) }, (_, f) => ({ t: f / FPS, name: `f${String(f).padStart(5, '0')}.jpg` }));

const n = Math.min(workers, jobs.length);
const started = Date.now();
await Promise.all(Array.from({ length: n }, async (_, wi) => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto(url);
  await page.evaluate(() => window.__ready);
  for (let j = wi; j < jobs.length; j += n) {
    await page.evaluate((t) => window.__renderAt(t), jobs[j].t);
    const file = path.join(outDir, jobs[j].name);
    await page.screenshot(file.endsWith('.png') ? { path: file, type: 'png' } : { path: file, type: 'jpeg', quality: 95 });
    if (wi === 0 && j % 200 === 0) console.log(`${fmt}: frame ${j}/${jobs.length} · ${((Date.now() - started) / 1000).toFixed(0)}s`);
  }
  await browser.close();
}));
console.log(`${fmt}: ${jobs.length} images in ${((Date.now() - started) / 1000).toFixed(0)}s`);
