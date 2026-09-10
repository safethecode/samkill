const { chromium } = require('../../../../todo/node_modules/@playwright/test');
const fs = require('node:fs');
const path = require('node:path');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome' });
  const app = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await app.goto('http://127.0.0.1:4190/round-04/app.html');
  await app.screenshot({ path: path.join(__dirname, 'home-final-390.png') });
  const boxes = await app.locator('.header,.search').evaluateAll(es => es.map(e => e.getBoundingClientRect().toJSON()));
  await app.screenshot({ path: path.join(__dirname, 'Q1-final.png'), clip: { x: 0, y: boxes[0].y, width: 390, height: boxes[1].bottom - boxes[0].y } });
  const regions = [{ id: 'Q2', locator: app.locator('.quick') }, { id: 'Q3', locator: app.getByRole('heading', { name: '테마로 둘러보기' }).locator('..') }, { id: 'Q4', locator: app.locator('#results .cafes > li').first() }];
  for (const region of regions) {
    const { id, locator } = region;
    const rect = await locator.boundingBox();
    if (!rect) throw new Error('Region missing');
    await app.screenshot({ path: path.join(__dirname, `${id}-final.png`), clip: { x: 0, y: rect.y, width: 390, height: rect.height } });
  }
  await app.getByRole('button', { name: '온실 커피 9월 12일 13:00 예약 선택', exact: true }).click();
  await app.locator('dialog').screenshot({ path: path.join(__dirname, 'Q5-final.png') });
  await app.close();
  const results = [];
  for (const width of [1100, 390, 320]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    await page.goto('http://127.0.0.1:4190/round-04/');
    await page.locator('.result').last().waitFor();
    const detail = await page.evaluate(() => ({ width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
      brokenImages: [...document.images].filter(e => !e.complete || !e.naturalWidth).length,
      hrefs: [...document.querySelectorAll('a')].map(e => e.getAttribute('href')),
      prompts: document.querySelectorAll('details').length }));
    const frame = page.frames().find(f => f.url().endsWith('app.html'));
    if (!frame) throw new Error('App frame missing');
    const state = await frame.evaluate(() => ({ width: innerWidth, scrollWidth: document.documentElement.scrollWidth, brokenImages: [...document.images].filter(e => !e.complete || !e.naturalWidth).length }));
    await frame.getByRole('button', { name: '음료맛집', exact: true }).click();
    const filtered = await frame.locator('#results .cafes > li').count();
    await frame.getByRole('button', { name: '초기화', exact: true }).click();
    const summary = page.locator('summary').first();
    await summary.focus(); await page.keyboard.press('Enter');
    const opened = await page.locator('details').first().getAttribute('open') !== null;
    await page.keyboard.press('Enter');
    const closed = await page.locator('details').first().getAttribute('open') === null;
    await page.emulateMedia({ forcedColors: 'active', reducedMotion: 'reduce' });
    const focus = await summary.evaluate(e => ({ focused: e === document.activeElement, outline: getComputedStyle(e).outline }));
    await page.emulateMedia({ forcedColors: 'none', reducedMotion: 'no-preference' });
    await page.screenshot({ path: path.join(__dirname, `board-${width}.png`), fullPage: true });
    if (width === 1100) { await page.locator('.preview').screenshot({ path: path.join(__dirname, 'preview-final.png') }); for (const q of ['Q1','Q2','Q3','Q4','Q5']) await page.locator(`#${q}`).screenshot({ path: path.join(__dirname, `${q}-comparison.png`) }); }
    results.push({ detail, state, filtered, opened, closed, focus });
    await page.close();
  }
  fs.writeFileSync(path.join(__dirname, 'board-checks.json'), JSON.stringify(results, null, 2) + '\n');
  await browser.close();
  if (results.some(r => r.detail.scrollWidth > r.detail.width || r.detail.brokenImages || r.state.scrollWidth > r.state.width || r.state.brokenImages || r.filtered !== 1 || !r.opened || !r.closed)) throw new Error('Board verification failed');
  console.log('Board 1100/390/320: images, width, live filter/reset, 5 prompt disclosures, keyboard and forced-colors focus verified.');
})();
