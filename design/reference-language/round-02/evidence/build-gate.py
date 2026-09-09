#!/usr/bin/env python3
"""Serialize frozen human review decisions; not an automated visual judge.
Run from repository root after reading gate-review.md and current screenshot artifacts:
python3 design/reference-language/round-02/evidence/build-gate.py
Then run design_gate.py check with --root design/reference-language/round-02.
Do not rerun on changed UI to renew old visual decisions. Re-capture and manually
review affected states, update this frozen mapping and gate-review first.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
CATALOG = REPO / 'skills/reference-review/references/failure-catalog.json'
GATE = REPO / 'skills/reference-review/scripts/design_gate.py'
catalog = json.loads(CATALOG.read_text())
# These are explicit reviewer applicability decisions for this single static experiment.
NA = {
'ORC-F01':'단일 모바일 멘토 목록이며 사이드바가 없다.',
'ORC-F02':'사이드바/본문 간 강조색 배분 과제가 없다.',
'ORC-F04':'실행 CTA나 중복 실행 진입점이 없다. 입력 하나만 편집 가능하다.',
'ORC-F08':'항목 하트는 상태 이미지이며 반복 실행 버튼이 아니다.',
'ORC-F09':'복수 열 대시보드가 아닌 단일 열 목록이다.',
'ORC-F13':'클릭 이벤트나 커스텀 클릭 요소가 없다. 네이티브 텍스트 입력은 text 커서다.',
'ORC-G10':'사이드바/본문 모드 비교 대상이 없다.',
'ORC-G12':'중복 CTA가 없다.',
'ORC-G13':'20개 이상 데이터 그리드가 아닌 관찰된 두 멘토의 정적 카드다.',
'ORC-G16':'하트는 비상호작용 상태 이미지, 반복 액션이 없다.',
'ORC-G17':'복수 열 레이아웃이 없다.',
'ORC-G21':'onclick이나 커스텀 클릭 요소가 없다.',
'ORC-A09':'카드 그리드가 아닌 동일 역할 두 멘토의 단일 열 목록이다.',
'ORC-A10':'API/비동기 요청/서비스 상태가 없는 정적 재현. 입력 편집만 있으므로 로딩·빈 결과·오류를 생성하지 않는다.',
'RUI-05':'사용자 범위는 언어 재현 실험이며 새 제품 아이디어 결합이 아니다.',
'RUI-15':'대화 UI나 전송·결과·복구 흐름이 없다.',
'RUI-18':'단일 화면 분해 실험으로 복합 제품 조사 분기가 없다.',
'RUI-19':'필터는 분야 상태이며 목적지 모바일 탭 내비게이션이 없다.',
'RUI-20':'생성/수정 폼이 없다. 화면 제목 위계는 ORC-F07/G15에서 확인한다.',
'RUI-21':'날짜·시간 선택 입력이 없다.',
}
EX = {
'ORC-G02':('검색 hover/focus 경계','hover의 inset shadow는 장식 깊이가 아닌 레이아웃을 바꾸지 않는 입력 경계다. 사용자 경계 전환/포커스 보존 기준에 따른 한정 예외.'),
'ORC-G05':('검색 hover 경계','bg-only 일반 기준 대신 사용자 경계 모션 지침에 따라 inset 경계가150ms로 전환된다. 확대/이동/불투명도 장식은 없다.'),
'ORC-F03':('E3 전체 필터','흰 글자 대비는 확보하되 P1은400을 선택했다. 사용자 재현 요청과 원본의 작은 필터 위계를 따른 분석자 선택이며 사용자가400을 지정한 것은 아니다.'),
'ORC-F05':('E4 멘토 카드','3개 이상 속성에도 원본은 아바타·설명 중심 카드다. 표로 변경하면 재현 과제를 바꾸므로 관찰된 두 카드에 한해 유지한다.'),
'ORC-F06':('E4 찜한 멘토 하트','원본에서 붉은 채움이 찜 상태를 식별한다. 오류색으로 재해석하지 않는 재현 범위 예외.'),
'ORC-F07':('E1 제목','18px/700은 원본의 작은 강한 제목을 옮긴 분석자 선택.20–24px/600 일반 기준과 차이를 공개한다.'),
'ORC-F10':('E4 자격 아이콘','P1의14px 자격 아이콘은14px 텍스트와 같은 크기다. 원본의 작은 배지 관계를 옮긴 선택으로 +2–4px 공식 예외. 실제 중심정렬은 별도 확인.'),
'ORC-F12':('E1/E4/E5 간격','헤더 끝20px,본문16px 및 메타/배지2·6px,설명-footer14px는 서로 다른 역할의 분석자 수치.4px 강제보다 관찰 관계 보존. 행내 형제간격은 일정하게 검사.'),
'ORC-F15':('E4 현직/인증 배지','원본의 파랑/보라 자격 구분은 회색+2강조 이내. 무채색 강제는 재현 손실이므로 두 자격 상태에만 예외.'),
'ORC-G01':('화면 배경','원본의 연보라 배경 밝기 변화를 옮긴 미세 그라디언트다. P1 색상은 분석자 선택이고 장식 강조 그라디언트는 없다.'),
'ORC-G03':('E2/E4 반경','검색12px/카드14px는 원본의 둥근 흰 표면 관계를 옮긴 분석자 선택. pill·avatar 외8px 한도 예외를 해당 두 역할에 한정.'),
'ORC-G04':('화면 상태색','배경 연보라·자격 파랑/보라·찜 빨강은 원본의 서로 다른 의미다.2색 한도 때문에 상태를 지우지 않는 재현 예외.'),
'ORC-G07':('배지/설명 간격','2px/6px/14px는 배지 밀도와 설명-footer 관계를 유지하는 P1 분석자 선택. 모든 간격4px 배수 규칙의 국소 예외.'),
'ORC-G11':('전체 선택 필터','흰 글자400은 원본 관계를 옮긴 P1 선택. 일반500 하한 예외이며 실제14px 하한은 유지한다.'),
'ORC-G14':('E4 붉은 찜 하트','원본의 저장된 찜 상태를 보존하는 범위에만 비-danger 빨강을 허용한다.'),
'ORC-G18':('E4 자격 아이콘','14px 글자+14px SVG는 원본의 작은 자격 배지 관계를 옮긴 선택. +2–4px 공식만 예외이며 중심정렬은 유지한다.'),
'ORC-G20':('헤더 마지막 도구 inset','원본 오른쪽 도구 여유를 옮긴20px와 화면16px의4px 차이는 역할 예외. 세 아이콘의20px 동등 gap과 내용16px 양끝은 유지한다.'),
'ORC-G22':('자격 배지','현직 파랑/인증 보라와 중립 면접은3색 이내지만 gray/traffic-light 강제와 다르다. 원본 자격표현 재현 범위 예외.'),
'ORC-A03':('검색 키보드 포커스','inset shadow는 장식 깊이가 아닌 크기를 바꾸지 않는 초점 경계. AGENTS의 명시 포커스 보존 기준에 따라 예외; 카드 그림자는 없다.'),
'ORC-A06':('정적 멘토 정보','원본에서 확인하지 못한 가격/별점/판매자를 추가하지 않는다. 정보 밀도는 관찰된 카드 설명과 자격에 한해 판독한다.'),
'ORC-A07':('전역 도구/찜 상태','원본처럼 아이콘만 보이고 role=img/aria-label로 의미를 제공한다. 재현 요청 범위이며 실제 이동 버튼이라는 약속은 없다.'),
'RUI-13':('390 비교 프레임','원본 키보드 앞 관찰영역만 단일 crop으로 표시한다. 분석자 선택390×460.33은 원본 앱 스크롤 복원이 아니다.320 문서는 자연 높이로 모든 생성내용을 읽게 한다.'),
}
PASS = {
'ORC-F11':'현직/인증의 qualification 컨테이너가 SVG와 글자에 같은 상태색을 전달한다.',
'ORC-F14':'main/header/article/ul/li/footer/input을 역할에 맞게 사용하며 div는 inset·flex·표본 역할이다.',
'ORC-F16':'카드 자체 스크롤바가 없고320은 자연 문서.390 프레임 crop은 관찰영역 비교이며 중첩 스크롤을 만들지 않는다.',
'ORC-G02':'큰 그림자나 hover 상승 그림자가 없다. 입력 inset 경계는 초점 표시다.',
'ORC-G05':'검색 hover는 inset 경계 색만 변한다. transform/scale/translate/opacity 장식이 없다.',
'ORC-G06':'읽는 글자14px/18px 두 단계이며 폰트 크기를 늘어놓지 않는다.',
'ORC-G08':'제목→검색→작은 필터→멘토 정보로 단일 과제 밀도를 유지한다.',
'ORC-G09':'새 장식/로고/CTA/별점은 없다. 아바타와 상태아이콘은 식별 정보다.',
'ORC-G15':'멘토링 제목18px로24px 최대 이하이다.',
'ORC-G19':'배지 icon/text가 같은 currentColor 상태색을 공유한다.',
'ORC-G23':'내부 overflow-auto/scroll 컨테이너가 없다.320 문서 스크롤만 사용한다.',
'ORC-G24':'목록/카드/머리말/하단정보 의미 태그와 실제 입력을 사용한다. 단순 div는 표본/inset/flex 역할이다.',
'ORC-A01':'avatar 원형,필터 pill,검색12px,카드14px,배지6px로 역할별 반경을 구별한다.',
'ORC-A02':'흰 카드와 매우 옅은 연보라 배경의 표면 단계를 유지한다.',
'ORC-A04':'기본 blue500가 아닌 원본 자격/찜의 파랑·보라·빨강 선택이다.',
'ORC-A05':'카드 왼쪽 아바타·이름과 우측 하트,하단 좌우 정보로 정보 역할에 맞는 비대칭을 유지한다.',
'ORC-A08':'제공된 원본 새 아바타2개를 실제 이미지로 표시하고 placeholder가 없다.',
'RUI-01':'P1은1170×2532 image-px와390 CSS px 선택을 구별하고 DPR/서체/실제 기능을 unknown으로 둔다.',
'RUI-02':'CSS 의미 변수에서 배경/글자/상태/간격/반경/크기를 정의하고 실제 컴포넌트가 참조한다. 구조 reset·0·100%는 레이아웃 값이다.',
'RUI-03':'catalog v4 활성75개 모두 원래 checks를 보존하며 예외와 미적용을 개별 명시한다.',
'RUI-04':'정적 E1–E5와 조립 화면,네이티브 입력 편집 범위를 실제 실행한다. 서비스 기능 완료로 확대하지 않는다.',
'RUI-06':'제품은HTML/CSS로 렌더/DOM 검증하며 검증용JS는기존 anti-slop lint/typecheck를 실행한다.',
'RUI-07':'필터는검색조건,카드는멘토식별/설명,찜은항목상태로원본의판단순서와소속을보존한다.',
'RUI-08':'멘토링은화면제목이고새로고/슬로건을생성하지않는다.',
'RUI-09':'390/320및독립표본의읽는글자와placeholder는computed14px이상이다.',
'RUI-10':'작은내용폭필터는정적선택군으로표시하며큰CTA나가짜실행버튼이없다.',
'RUI-11':'원본에없는안내를화면안에추가하지않고정적범위는독립표본바깥에서설명한다.',
'RUI-12':'제공공식Lucide path를사용하며알림/찜/인물/검색/자격의의미와채움/윤곽상태를보존한다.',
'RUI-14':'hr/탭밑줄/영역바가없다. 검색focus경계는단일입력역할이고장식선이아니다.',
'RUI-16':'V1–V6의원본영역을P1/E1–E5와같은폭렌더에직접대조한다.',
'RUI-17':'배경/흰표면/작은필터/아바타-이름-별도하트/본문왼쪽복귀/footer양끝/둘째상태의핵심관계를직접판독한다.',
'RUI-22':'화면16px부모inset과카드16px내부여백을분리하고독립표본에서도동일관계를유지한다.',
'RUI-23':'조립과E1–E5를390/320같은폭으로비교하고동일클래스/토큰의입력·카드·글자·상태톤을확인한다.',
'RUI-24':'횟수9회는한번만표시하고현직/인증·소속·면접은다른정보역할이다.',
'RUI-25':'검색/필터와멘토목록은간격,카드표면과내부여백으로구분한다.선을삭제한뒤에도소속이보인다.',
}

def evidence(kind, relative):
    return {'kind':kind,'path':relative,'sha256':hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()}

rules=[]
results=[]
for rule in catalog['rules']:
    if rule['status'] != 'active':
        continue
    rid=rule['id']
    assert rid in NA or rid in EX or rid in PASS, rid
    scope,reason=EX.get(rid,('screen.html/components.html/ui.css 및 P1', NA.get(rid,PASS.get(rid))))
    exceptions=[{'id':'R2-'+rid,'scope':scope,'reason':reason,'basis':'사용자 재현 실험 요청; source.png 직접 관찰; P1 분석자 선택. 사용자 직접 수치 지정으로 주장하지 않음.'}] if rid in EX else []
    rules.append({'id':rid,'applicable':rid not in NA,'scope':scope,'reason':reason,'checks':rule['checks'],'exceptions':exceptions})
    status='not-applicable' if rid in NA else 'exception' if rid in EX else 'pass'
    files={'spec':'gate-review.md','code':'ui.css','visual':'evidence/gate-screen-390.png','interaction':'evidence/gate-browser.json'}
    ev=[] if rid in NA else [evidence(kind,files[kind]) for kind in rule['checks']]
    if rid not in NA:
        ev.append(evidence('spec','gate-review.md'))
        if 'visual' in rule['checks']:
            ev.extend(evidence('visual',f'evidence/gate-{page}-{width}.png') for page,width in [('screen',320),('components',390),('components',320)])
        if rid=='RUI-06':
            ev.append(evidence('code','evidence/code-checks.txt'))
    result={'id':rid,'status':status,'reason':reason,'evidence':ev}
    if rid in EX:
        result['exception_id']='R2-'+rid
    results.append(result)
project={'id':'PROJECT-R2-RECONSTRUCTION','applicable':True,'scope':'E1–E5 및 조립','reason':'원본의관계·두상태·가시영역을보존하고320에서생성내용잘림없이읽으며입력편집가능.숨은서비스기능생성금지.','checks':['spec','code','visual','interaction'],'exceptions':[]}
rules.append(project)
for pid, reason in [('PROJECT-BOX-SUM','P1 내부48px 계약과 자식56px 합계 충돌. P2는24+2+22=48로 수정하여390 첫 카드180/둘째y372를 재검증.'),('PROJECT-SPECIMEN-WIDTH','P2 독립390 표본은342px로 줄어듦. P3는표본390/320폭을조립과같게하고설명padding을분리하여재검증.')]:
    rules.append({**project,'id':pid,'reason':reason,'checks':['spec','code','visual']})
    results.append({'id':pid,'status':'pass','reason':reason,'evidence':[evidence('spec','gate-review.md'),evidence('code','ui.css'),evidence('visual','evidence/gate-components-390.png'),evidence('interaction','evidence/gate-browser.json')]})
results.append({'id':project['id'],'status':'pass','reason':'V1–V6와390/320조립·독립표본,입력행동을직접확인했다.','evidence':[evidence(k,{'spec':'gate-review.md','code':'ui.css','visual':'evidence/gate-screen-390.png','interaction':'evidence/gate-browser.json'}[k]) for k in project['checks']]})
contract={'schema_version':1,'catalog_version':catalog['version'],'targets':['screen.html','components.html','ui.css','prompt-v1.md'],'rules':rules}
for prompt in ['prompt-v2.md','prompt-v3.md']:
    if (ROOT/prompt).exists():
        contract['targets'].append(prompt)
contract_path=ROOT/'gate-contract.json'
contract_path.write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('design_gate',GATE)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
report={'schema_version':1,**module.fingerprints(ROOT,CATALOG,contract_path,contract),'results':results}
(ROOT/'gate-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Wrote frozen human decisions. Run CLI integrity check separately.')
