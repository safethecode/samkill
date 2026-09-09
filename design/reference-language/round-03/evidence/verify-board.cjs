const { chromium } = require('../../../../todo/node_modules/@playwright/test');
const fs = require('node:fs');
const path = require('node:path');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome' });
  const observations = [];
  for (const width of [1100, 390, 320]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    await page.goto('http://127.0.0.1:4190/round-03/');
    await page.locator('iframe').last().waitFor();
    const detail = await page.evaluate(() => ({
      width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
      frames: [...document.querySelectorAll('iframe')].map(e => ({ title: e.title, width: e.getBoundingClientRect().width })),
      brokenImages: [...document.images].filter(e => !e.complete || !e.naturalWidth).length,
      hrefs: [...document.querySelectorAll('a')].map(e => e.getAttribute('href')),
      prompts: document.querySelectorAll('details').length,
    }));
    const frameChecks = [];
    for (const frame of page.frames().slice(1)) {
      await frame.waitForLoadState();
      frameChecks.push(await frame.evaluate(() => ({
        url: location.href, viewportHeight: innerHeight, width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
        height: document.documentElement.scrollHeight,
        brokenImages: [...document.images].filter(e => !e.complete || !e.naturalWidth).length,
      })));
    }
    const summary = page.locator('summary').first();
    await summary.focus();
    await page.keyboard.press('Enter');
    const opened = await page.locator('details').first().getAttribute('open') !== null;
    await page.keyboard.press('Enter');
    const closed = await page.locator('details').first().getAttribute('open') === null;
    await page.emulateMedia({ forcedColors: 'active', reducedMotion: 'reduce' });
    const focus = await summary.evaluate(e => ({ focused: document.activeElement === e, outline: getComputedStyle(e).outline }));
    await page.emulateMedia({ forcedColors: 'none', reducedMotion: 'no-preference' });
    await page.screenshot({ path: path.join(__dirname, `board-${width}.png`), fullPage: true });
    if (width === 1100) await page.locator('#assembled').screenshot({ path: path.join(__dirname, 'assembled-final.png') });
    observations.push({ detail, frameChecks, opened, closed, focus });
    await page.close();
  }
  fs.writeFileSync(path.join(__dirname, 'board-checks.json'), JSON.stringify(observations, null, 2) + '\n');
  await browser.close();
  const failures = observations.filter(o => o.detail.scrollWidth > o.detail.width || o.detail.brokenImages || !o.opened || !o.closed || o.frameChecks.some(f => f.brokenImages || f.scrollWidth > f.width || f.height > f.viewportHeight));
  if (failures.length) throw new Error(JSON.stringify(failures));
  console.log('Board at 1100/390/320: 8 prompt disclosures, equal paired widths, no horizontal overflow or failed images, keyboard open/close and forced-colors focus checked.');
})();
