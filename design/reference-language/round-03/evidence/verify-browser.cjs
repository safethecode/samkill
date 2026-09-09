const { chromium } = require('../../../../todo/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
/** @param {import('../../../../todo/node_modules/playwright').Page} page */
async function inspect(page) {
  return page.evaluate(() => {
    /** @param {Element} element */
    const rect = (element) => { const box = element.getBoundingClientRect(); return { x: box.x, y: box.y, width: box.width, height: box.height }; };
    const text = [...document.querySelectorAll('*')].filter((element) => [...element.childNodes].some((node) => node.nodeType === Node.TEXT_NODE && (node.textContent || "").trim()));
    return {
      width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
      text: text.map((element) => ({ text: element.textContent, size: getComputedStyle(element).fontSize, class: element.className })),
      boxes: [...document.querySelectorAll('.app,.top,.banner,.summary,.shortcuts,.shortcut,.challenge,.challenge-top,.challenge-title,.challenge-badge,.challenge-subtitle,.flag,.records,.date-row,.date,.record,.record-value,.fab,.bottom-nav,.destination,.sample')].map((element) => ({ class: element.className, ...rect(element) })),
      badImages: [...document.images].filter((element) => !element.complete || !element.naturalWidth).map((element) => element.src),
      actions: document.querySelectorAll('button,a,[onclick]').length,
      scrollContainers: [...document.querySelectorAll('*')].filter((element) => /(auto|scroll)/.test(getComputedStyle(element).overflowY) && element.scrollHeight > element.clientHeight).map((element) => element.className),
      divCount: document.querySelectorAll('div').length, elementCount: document.querySelectorAll('*').length,
      headings: [...document.querySelectorAll('.component')].map((element) => ({ id: element.id, heading: element.querySelector('h2')?.textContent, promptStart: element.querySelector('.prompt')?.textContent?.slice(0, 55) }))
    };
  });
}
async function run() {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const report = [];
  for (const width of [390, 320]) {
    const page = await browser.newPage({ viewport: { width, height: 844 } });
    await page.goto('http://localhost:4190/round-03/screen.html');
    await page.screenshot({ path: path.join(__dirname, `gate-screen-${width}.png`), fullPage: true });
    const screen = await inspect(page);
    const selectors = ['.top','.banner','.summary','.shortcuts','.challenge','.records','.fab','.bottom-nav'];
    const assembly = new Map();
    for (const selector of selectors) assembly.set(selector, await page.locator(selector).first().boundingBox());
    await page.mouse.wheel(0, 600);
    const scrollAfterWheel = await page.evaluate(() => scrollY);
    await page.keyboard.press('Tab');
    const focusAfterTab = await page.evaluate(() => document.activeElement?.tagName);
    await page.goto('http://localhost:4190/round-03/components.html');
    const components = await inspect(page);
    const comparisons = [];
    for (const [index, selector] of selectors.entries()) {
      const sample = page.locator(`#E${index + 1} .w${width}`);
      await sample.screenshot({ path: path.join(__dirname, `gate-E${index + 1}-${width}.png`) });
      const box = await sample.locator(selector).first().boundingBox();
      comparisons.push({ element: index + 1, selector, assembly: assembly.get(selector), sample: box });
    }
    await page.setViewportSize({ width: 1100, height: 844 });
    const wideComparisons = [];
    for (const [index, selector] of selectors.entries()) {
      const sample = page.locator(`#E${index + 1} .w${width}`);
      const box = await sample.locator(selector).first().boundingBox();
      const details = await sample.locator('.date,.record,.shortcut-label,.destination').evaluateAll((elements) => elements.map((element) => ({ text: element.textContent, width: element.getBoundingClientRect().width, height: element.getBoundingClientRect().height })));
      wideComparisons.push({ element: index + 1, box, details });
    }
    const details = page.locator('details').first();
    await details.locator('summary').click();
    const opened = await details.evaluate((element) => element.hasAttribute('open'));
    await details.locator('summary').press('Enter');
    const closedWithKeyboard = await details.evaluate((element) => !element.hasAttribute('open'));
    report.push({ width, screen, scrollAfterWheel, focusAfterTab, components, comparisons, wideComparisons, opened, closedWithKeyboard });
    await page.close();
  }
  fs.writeFileSync(path.join(__dirname, 'gate-browser.json'), JSON.stringify(report, null, 2));
  await browser.close();
}
run().catch((error) => { console.error(error); process.exitCode = 1; });
