// Renders guide.html to ../downloads/shadowing-a-doctor-guide.pdf and audits each page.
//
// Every page is a fixed Letter sheet whose body shares spare height between its
// blocks. The audit reports, per page, whether content overflows the sheet and how
// large the shared gap is, so a page that is too full or too empty is caught here
// instead of in the PDF.
//
// Playwright lives in the Odyssey repo on this machine:
//   NODE_PATH=/Users/marcgray/odyssey/node_modules node render.mjs
import { createRequire } from 'module';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const D = dirname(fileURLToPath(import.meta.url));
const OUT = join(D, '..', 'downloads', 'shadowing-a-doctor-guide.pdf');

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 816, height: 1056 } });
await page.goto(`file://${join(D, 'guide.html')}`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(400);

const report = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
  const body = p.querySelector('.body');
  if (!body) return { page: i + 1, fixed: true };
  const kids = [...body.children];
  const used = kids.reduce((s, k) => s + k.getBoundingClientRect().height, 0);
  const room = body.getBoundingClientRect().height;
  const gap = kids.length > 1 ? (room - used) / (kids.length - 1) : 0;
  // headings must sit closer to what they introduce than to what came before
  const clipped = [...p.querySelectorAll('*')].some(e => {
    const r = e.getBoundingClientRect(), pr = p.getBoundingClientRect();
    return r.height > 0 && (r.bottom > pr.bottom - 66 + 0.5) && !e.closest('.foot') && !e.closest('.cover') && e.children.length === 0;
  });
  return { page: i + 1, blocks: kids.length, gap: Math.round(gap), overflow: used > room + 0.5, clipped };
}));

let bad = 0;
for (const r of report) {
  if (r.fixed) { console.log(`page ${r.page}: fixed layout`); continue; }
  const flag = r.overflow || r.clipped ? 'OVERFLOW' : r.gap > 30 ? 'LOOSE' : r.gap < 10 ? 'TIGHT' : 'ok';
  if (flag !== 'ok') bad++;
  console.log(`page ${r.page}: ${r.blocks} blocks, shared gap ${r.gap}px  ${flag}`);
}

await page.pdf({ path: OUT, printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log(`wrote ${OUT}${bad ? `, ${bad} page(s) need attention` : ''}`);
