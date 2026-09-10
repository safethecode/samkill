const {chromium,expect}=require('../../../../todo/node_modules/@playwright/test');
const fs=require('node:fs');
const outputRoot=__dirname+'/review-p4';
fs.mkdirSync(outputRoot,{recursive:true});
const {inspect}=require('./inspect-browser.cjs');
/** @type {Array<{width:number,states:Array<{name:string,inspection:Awaited<ReturnType<typeof inspect>>}>,checks:string[],errors:string[]}>} */
const reports=[];
async function run(){
 const browser=await chromium.launch({channel:'chrome',headless:true});
 for(const width of [390,320]){
  const page=await browser.newPage({viewport:{width,height:844}});
  /** @type {string[]} */const errors=[];
  /** @type {Array<{name:string,inspection:Awaited<ReturnType<typeof inspect>>}>} */const states=[];
  /** @type {string[]} */const checks=[];
  page.on('pageerror',error=>errors.push(error.message));
  /** @param {string} name */async function capture(name){await page.waitForLoadState('networkidle');await page.screenshot({path:`${outputRoot}/review-${name}-${width}.png`,fullPage:true});const inspection=await inspect(page);expect(inspection.scrollWidth).toBe(width);expect(inspection.badImages).toEqual([]);for(const text of inspection.text)expect(parseFloat(text.size)).toBeGreaterThanOrEqual(14);states.push({name,inspection});}
  await page.goto('http://localhost:4190/round-04/app.html');
  await capture('home');
  await page.getByRole('button',{name:'저장',exact:true}).click();await capture('saved-empty');
  await page.getByRole('button',{name:'예약',exact:true}).click();await capture('bookings-empty');
  await page.getByRole('button',{name:'둘러보기',exact:true}).click();
  const search=page.getByRole('searchbox');await search.fill('없는 이름 <img>');await expect(search).toBeFocused();await expect(page.locator('article')).toHaveCount(0);await capture('search-empty');await page.getByRole('button',{name:'검색어 지우기'}).click();await expect(search).toBeFocused();
  await page.getByLabel('지역 선택').selectOption('연남');await expect(page.locator('article')).toHaveCount(1);await expect(page.locator('article')).toContainText('커피와 산책');
  await page.getByLabel('지역 선택').selectOption('전체');
  for(const [name,count] of [['동반입장',2],['음료맛집',2],['맹견전용',1],['넓은마당',2]]){const control=page.getByRole('button',{name:String(name),exact:true});await control.click();await expect(page.locator('article')).toHaveCount(Number(count));await expect(control).toBeFocused();await control.click();await expect(page.locator('article')).toHaveCount(4);}
  await page.getByRole('button',{name:'온실 커피 저장',exact:true}).click();
  await page.getByRole('button',{name:'산책 뒤, 느긋하게',exact:true}).click();await expect(page.locator('article')).toHaveCount(2);await page.getByRole('button',{name:'저장',exact:true}).click();await expect(page.locator('article')).toHaveCount(1);await expect(page.locator('.filter-summary')).toHaveCount(0);await capture('saved');await page.getByRole('button',{name:'둘러보기',exact:true}).click();await expect(page.getByRole('button',{name:'넓은마당',exact:true})).toHaveAttribute('aria-pressed','true');await page.getByRole('button',{name:'초기화',exact:true}).click();
  await page.getByRole('button',{name:'초록빛 실내에서',exact:true}).click();await expect(page.locator('article')).toHaveCount(1);await page.getByRole('button',{name:'초기화',exact:true}).click();checks.push('검색 입력초점·HTML문자 빈결과·지우기·지역·4조건 선택해제·2테마·저장범위 분리·탭상태 복귀');
  await page.getByRole('link',{name:'온실 커피',exact:true}).click();await capture('detail');await expect(page.getByText('이동가방 필수',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:'예약 일시 선택',exact:true}).click();await capture('booking');
  await expect(page.getByRole('button',{name:'13일 (일) 예약 마감',exact:true})).toBeDisabled();
  await page.getByRole('button',{name:'18일 (금)',exact:true}).click();await page.getByRole('button',{name:'15:00',exact:true}).click();await page.getByLabel('인원',{exact:true}).selectOption('4');await page.getByLabel('반려동물',{exact:true}).selectOption('2');
  await page.getByRole('button',{name:'예약 내용 확인',exact:true}).click();await expect(page.getByRole('checkbox')).toBeFocused();await expect(page.getByRole('checkbox')).toHaveAttribute('aria-invalid','true');await capture('validation');await page.getByRole('checkbox').check();
  await page.getByRole('button',{name:'예약 내용 확인',exact:true}).click();await capture('summary');await expect(page.getByText('2026년 9월 18일 15:00',{exact:true})).toBeVisible();await expect(page.getByText('4명 · 반려동물 2마리',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:'이전',exact:true}).click();await expect(page.getByLabel('인원',{exact:true})).toHaveValue('4');await expect(page.getByRole('button',{name:'18일 (금)',exact:true})).toHaveAttribute('aria-pressed','true');await page.keyboard.press('Escape');await expect(page.getByRole('button',{name:'예약 일시 선택',exact:true})).toBeFocused();
  await page.getByRole('button',{name:'예약 일시 선택',exact:true}).click();await expect(page.getByRole('button',{name:'18일 (금)',exact:true})).toHaveAttribute('aria-pressed','true');await page.getByRole('button',{name:'예약 내용 확인',exact:true}).click();await page.getByRole('button',{name:'예약 화면 닫기',exact:true}).click();await page.getByRole('button',{name:'카페 목록으로 돌아가기',exact:true}).click();
  await page.getByRole('button',{name:'예약',exact:true}).click();await expect(page.locator('.reservation')).toHaveCount(0);await page.getByRole('button',{name:'둘러보기',exact:true}).click();
  await page.getByRole('button',{name:'온실 커피 9월 12일 14:00 예약 선택',exact:true}).click();await expect(page.getByRole('button',{name:'12일 (토)',exact:true})).toHaveAttribute('aria-pressed','true');await expect(page.getByRole('button',{name:'14:00',exact:true})).toHaveAttribute('aria-pressed','true');await page.getByRole('button',{name:'예약 내용 확인',exact:true}).click();await page.getByRole('button',{name:'예약 체험 완료',exact:true}).click();await capture('done');await expect(page.getByText('실제 예약은 접수되지 않았어요',{exact:true})).toBeVisible();await page.getByRole('button',{name:'예약 내역 보기',exact:true}).click();await capture('bookings');await page.getByRole('button',{name:'예약 취소 체험',exact:true}).click();await capture('cancelled');await page.reload();await page.getByRole('button',{name:'예약',exact:true}).click();await expect(page.getByText('취소 체험 완료',{exact:true})).toBeVisible();checks.push('마감비활성·날짜/시간/4인2마리·필수조건오류/초점·요약보존·이전/Escape/닫기 취소0건·상세초안재진입·목록12일시간맥락·완료/취소/persistence');
  await page.getByRole('button',{name:'둘러보기',exact:true}).click();await page.getByRole('button',{name:'맹견전용',exact:true}).click();await page.getByRole('link',{name:'단독 마당',exact:true}).click();await capture('danger-detail');await page.getByRole('button',{name:'예약 요청 체험',exact:true}).click();await page.getByRole('checkbox').check();await page.getByRole('button',{name:'요청 내용 확인',exact:true}).click();await capture('danger-summary');await expect(page.getByText('대관비는 매장 확인이 필요해요.',{exact:true})).toBeVisible();await page.getByRole('button',{name:'요청 체험 완료',exact:true}).click();await page.getByRole('button',{name:'예약 내역 보기',exact:true}).click();await expect(page.getByText('요청 체험 완료',{exact:true})).toBeVisible();checks.push('맹견전용 단독대관·미정금액·별도요청CTA·로컬요청완료');
  expect(errors).toEqual([]);reports.push({width,states,checks,errors});await page.close();
 }
 await browser.close();fs.writeFileSync(`${outputRoot}/review-browser.json`,JSON.stringify(reports,null,2));
}
run().catch(error=>{fs.writeFileSync(`${outputRoot}/review-browser-partial.json`,JSON.stringify(reports,null,2));process.stderr.write(String(error));process.exitCode=1;});
