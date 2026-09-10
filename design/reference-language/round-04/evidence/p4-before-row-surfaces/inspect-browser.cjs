const { chromium } = require('../../../../todo/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
/** @param {import('../../../../todo/node_modules/playwright').Page} page */
async function inspect(page) {
  return page.evaluate(() => {
    /** @param {Element} element */
    function box(element) { const r = element.getBoundingClientRect(); return { x:r.x,y:r.y,width:r.width,height:r.height }; }
    const visible = [...document.querySelectorAll('*')].filter(element=> element.getBoundingClientRect().width > 0 && element.getBoundingClientRect().height > 0);
    return {
      width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,
      text: visible.filter(element=>[...element.childNodes].some(node=> node.nodeType===Node.TEXT_NODE && node.textContent?.trim())).map(element=>({tag:element.tagName,class:element.className,text:element.textContent?.trim(),size:getComputedStyle(element).fontSize,color:getComputedStyle(element).color,...box(element)})),
      controls:visible.filter(element=>element.matches('button,a,input,select,[tabindex]')).map(element=>({tag:element.tagName,class:element.className,text:element.textContent?.trim(),label:element.getAttribute('aria-label'),cursor:getComputedStyle(element).cursor,...box(element)})),
      scrollContainers:visible.filter(element=>/(auto|scroll)/.test(getComputedStyle(element).overflowY) && element.scrollHeight>element.clientHeight).map(element=>({tag:element.tagName,class:element.className,...box(element)})),
      badImages:[...document.images].filter(element=>!element.complete||!element.naturalWidth).map(element=>element.src),
      headings:visible.filter(element=>element.matches('h1,h2,h3')).map(element=>({tag:element.tagName,text:element.textContent,...box(element)})),
      divCount:document.querySelectorAll('div').length,elementCount:document.querySelectorAll('*').length
    };
  });
}
async function run() {
  const browser=await chromium.launch({channel:'chrome',headless:true});
  const reports=[];
  const prefix=process.argv[2] || "review-main-initial";
  for(const width of [390,320]) {
    const page=await browser.newPage({viewport:{width,height:844}});
    /** @type {string[]} */
    const errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    await page.goto('http://localhost:4190/round-04/app.html');
    await page.screenshot({path:path.join(__dirname,`${prefix}-${width}.png`),fullPage:true});
    reports.push({width,errors,inspection:await inspect(page)});
    await page.close();
  }
  fs.writeFileSync(path.join(__dirname,`${prefix}.json`),JSON.stringify(reports,null,2));
  await browser.close();
}
module.exports={inspect};
if(require.main===module) run().catch(error=>{ process.stderr.write(String(error));process.exitCode=1; });
