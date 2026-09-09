"""Serialize individual human review decisions after frozen-source visual inspection."""
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
CAT = REPO / 'skills/reference-review/references/failure-catalog.json'
spec = importlib.util.spec_from_file_location('gate', REPO/'skills/reference-review/scripts/design_gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
catalog = json.loads(CAT.read_text())
preflight = json.loads((ROOT/'evidence/rule-preflight.json').read_text())
NA = preflight['not_applicable']
EX = preflight['exception_candidates']
PASS = {
'ORC-F14':'main/header/section/ul/li/time을 역할별 사용하고 나머지 div는 grid/flex/position 배치를 소유한다. 무의미한 깊은 래퍼나 클릭div가 없다.',
'ORC-G01':'HTML 표면에 linear/radial gradient가 없으며 광고/고유삽화의 원본 픽셀은 별도다.',
'ORC-G08':'E1→광고→두 수치→8메뉴→챌린지→기록의 조밀한 홈 정보 순서를 유지한다. 추가 hero나 빈 소개가 없다.',
'ORC-G15':'상단22px와 챌린지18px는24px 이하이며 독립보드 설명 제목은 제품제목과 별도다.',
'ORC-G22':'참가자 badge는 하나의 옅은 무채색이며 반복 rainbow 상태배지가 없다.',
'ORC-G24':'기록 ul/li와 날짜 time,주영역 main,영역 section을 확인한다. 레이아웃 역할있는 나머지 div는 유지한다.',
'ORC-A04':'강조파랑 #2967ff는 관찰 P1 선택이며 기본 Tailwind blue500을 가져온 것이 아니다.',
'ORC-A06':'8개 한국어 메뉴와 당일 기록/보상 정보가 원본 순서로 촘촘하게 보인다. hover로 내용을 숨기지 않는다.',
'ORC-A08':'광고와7개메뉴/동전/신발/깃발은 실제출처crop. 이미지누락0이며 임시 placeholder가 없다.',
'RUI-01':'1125×2436 image-px와 선택390CSSpx 배율을 구별한다. DPR/폰트/실제fixed동작을 추정확정하지 않는다.',
'RUI-02':'역할별 CSS변수 정의→참조→사용과 직접값 예외를 code-checks에서 대조한다. 미사용값을 제거하며 P1 직접값 실패는 이력에 보존한다.',
'RUI-03':'catalog v4 active75개를 개별 판독하고 원래 checks를 보존한다. 프로젝트 원본재현/가용폭/가림/프롬프트 연결도 추가한다.',
'RUI-04':'원본·언어·HTML/CSS 정적표본을 비교하는 실험범위이다. 390/320 표본렌더와 details click/Enter를 실행하며 앱서비스동작으로 확대하지 않는다.',
'RUI-06':'제품HTML/CSS는 DOM/실제렌더로 검사. 검증JS는 기존 anti-slop oxlint와 checkJs를 실제통과한다. Python serialization은 JSON/게이트실행으로 검사한다.',
'RUI-07':'보상요약·바로가기·챌린지·기록과 기록위FAB의 소속 및 판단순서를 원본과 대조했다.',
'RUI-08':'새 로고·슬로건이 없다. welcome의 원본그림 글자를 새 브랜드제작으로 주장하지 않는다.',
'RUI-10':'상단보기/하단목적지는 정적선택상태이고 FAB는 원형표면+plus로 구별한다. 가짜 텍스트 실행링크가 없다.',
'RUI-11':'제품안에 실험설명·힌트·중복안내를 추가하지 않는다. 표본설명은 제품바깥 형제영역에 둔다.',
'RUI-14':'요약중앙세로선을 생략하고 탭밑줄/영역바/hr가 없다. nav capsule 외곽은 표면경계이며 가로영역바가 아니다.',
'RUI-16':'source-app 직접판독 후 Q1–Q8을 P1/P2와 실제 E1–E8에 연결해비교했다. 자산재사용을 UI전체재현능력으로 부풀리지 않는다.',
'RUI-17':'4×2메뉴·흰표면·제목위계·챌린지·첫5/FAB·옅은세번째/nav 관계가 보존된다. 최초E6 아래밀림과숫자가림은 수정후검증했다.',
'RUI-22':'기본17px와 카드내부 여백소유를 분리한다. 날짜행22+gap10의박스합, 조립/독립 실제가용폭을390/320에서대조했다.',
'RUI-23':'E1–E8 독립표본과조립은동일폭/클래스로같은위계·표면·글자를보인다. E6독립전체높이와조립가림프레임은다른역할이다.',
'RUI-24':'5,000원은포인트,12,000원은챌린지보상으로다른정보다. 날짜는한번만표시하고새중복배지가없다.',
'RUI-25':'흰표면과외부간격으로요약/8메뉴/챌린지/기록의소속이구별된다. 구분선삭제로경계가사라지지않는다.'
}
PROJECT = {
'PROJECT-R3-RECONSTRUCTION':'E1–E8 원본 구조/위계/밀도를390과320에서직접대조. E6첫행600.625와 첫5노출, E7/E8원본가림을확인한다.',
'PROJECT-SPECIMEN-WIDTH':'390/320 조립과독립E1–E8의내부폭및자식위치를대조. 외부보드가넓어도320컨테이너규칙이적용된다.',
'PROJECT-OVERLAP':'날짜·기록·FAB·nav의앵커를같은박스로검산. 첫5일부노출과둘째50.5/옅은셋째49의원본가림을보존한다.',
'PROJECT-PROMPT-MAPPING':'components E-ID/제목/P1본문이일치하고 P2교정을연결한다. 공유계약을요소로세어밀린최초실패를보존한다.'
}
def evidence(kind, relative):
    return {'kind':kind,'path':relative,'sha256':hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()}
rules=[]; results=[]
files={'spec':'gate-review.md','code':'ui.css','visual':'evidence/gate-screen-390.png','interaction':'evidence/gate-browser.json'}
for item in catalog['rules'] + [{'id':key,'status':'active','checks':['spec','code','visual','interaction']} for key in PROJECT]:
    if item['status']!='active': continue
    rid=item['id']; assert rid in NA or rid in EX or rid in PASS or rid in PROJECT, rid
    reason=NA.get(rid,EX.get(rid,PASS.get(rid,PROJECT.get(rid))))
    scope='E1–E8 정적표본/조립 및 해당 설명'; exception_id='R3-'+rid
    rules.append({'id':rid,'applicable':rid not in NA,'scope':scope,'reason':reason,'checks':item['checks'],'exceptions':[{'id':exception_id,'scope':scope,'reason':reason,'basis':'사용자 원본 재현 범위와 원본 직접 관찰. 수치 선택은 분석자 결정이며 사용자 직접 수치 지시로 주장하지 않는다.'}] if rid in EX else []})
    ev=[] if rid in NA else [evidence(k,files[k]) for k in item['checks']]
    if rid not in NA:
        ev.append(evidence('spec','gate-review.md'))
        if 'visual' in item['checks']:
            ev.append(evidence('visual','evidence/gate-screen-320.png'))
            ev.extend(evidence('visual',f'evidence/gate-E{n}-{w}.png') for n in range(1,9) for w in [390,320])
        if rid=='RUI-06': ev.append(evidence('code','evidence/code-checks.txt'))
    result={'id':rid,'status':'not-applicable' if rid in NA else 'exception' if rid in EX else 'pass','reason':reason,'evidence':ev}
    if rid in EX: result['exception_id']=exception_id
    results.append(result)
contract={'schema_version':1,'catalog_version':catalog['version'],'targets':['screen.html','components.html','ui.css','prompt-v1.md','prompt-v2.md','prompt-v3.md','prompt-v4.md','DESIGN.md','assets'],'rules':rules}
contract_path=ROOT/'gate-contract.json'; contract_path.write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
report={'schema_version':1,**gate.fingerprints(ROOT,CAT,contract_path,contract),'results':results}
(ROOT/'gate-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
