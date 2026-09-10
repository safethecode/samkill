"""Serialize P4 human review decisions; this does not judge images automatically."""
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
CAT=REPO/'skills/reference-review/references/failure-catalog.json'
spec=importlib.util.spec_from_file_location('gate',REPO/'skills/reference-review/scripts/design_gate.py')
gate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
catalog=json.loads(CAT.read_text())
NA={
'ORC-F01':'사이드바가 없는 단일 모바일 앱이며 별도 어두운 사이드바/밝은 본문 조합이 없다.',
'ORC-F02':'사이드바가 없으므로 사이드바에만 강조색을 고립시키는 구성이 없다.',
'ORC-F09':'독립 대시보드 다열이 없다. 동일 역할 테마2열은 동일사진높이이며 본문은 단일 목록이다.',
'ORC-G10':'사이드바와 본문 모드 분리 없음. 동일 모바일 화면 간 톤은 RUI-23으로 실제 검사한다.',
'ORC-G17':'독립 높이를 가진 다열 위젯 없음. 2개 테마는 동일 정보역할/사진높이로 유지한다.',
'RUI-15':'채팅이 없는 카페 탐색/예약 체험이다. 목록과 대화의 경쟁이나 메시지 전송 흐름을 만들지 않는다.'}
EX={
'ORC-F07':('앱 상단 22px/700 제목과44px행','R1/R4의 짙고 굵은 제목을 14px 조건과 구별하는 모바일 관계를 유지한다. 원문 20–24px 크기상한은 준수하며 weight600/행48–56 대신700/44는 모바일 제목·터치행에만 한정한다. 390/320 제목과검색 간격 및200% 자연높이를 직접 확인했다.'),
'ORC-F08':('카페별 가능시간3개와저장44px','R2의 매장소속 시간과 모바일 터치 발견성을 보존한다. hover-only는 사용하지 않는다. 시간은 해당매장 예약시트로, 저장은 독립토글로 작동하며 카드가반복되어도 다른영역에동일주CTA를복제하지 않는다.'),
'ORC-G16':('카페별 가능시간/저장 조작','상시시간은 R2의 핵심 실행관계이며 모바일에서 hover 없이 접근해야 한다. 두폭·터치·키보드로 실제 실행했다. 일반 행관리버튼의무제한반복에예외를확대하지 않는다.'),
'ORC-F10':('카테고리그림36–40,하단아이콘22,CTA아이콘24','R1의그림과라벨은수직스택이며대상별실루엣/채움이유지대상이다. 일반14px글자+2–4px규격으로그림을축소하지않는다. CTA/탭의크기도공식glyph와44px터치영역에서직접정렬판독했다. 수평CTA는flex중앙정렬,검색20px,아이콘24viewBox내glyph를실제로비교했다.'),
'ORC-G18':('카테고리그림/수직탭/CTA의아이콘박스','그림36–40px는라벨14px와기능이달라동일크기공식으로평탄화하지않는다. 상단검색/뒤로/CTA는실제박스와시각중앙을비교했고문자+기호로만든아이콘이없다.'),
'ORC-F11':('4개카테고리그림의대상색과먹색라벨','P4에고정한R1의표현있는그림역할이다. 살구발/크림커피/청색방패/녹색나무는상태색이아니라그림내용이다. 나머지nav/CTA/저장아이콘은currentColor로글자와같은색·hover를공유한다.'),
'ORC-G19':('카테고리그림색에만한정','그림과라벨을동일색으로만드는것이이전평탄화실패를반복하므로카테고리작품만색차이를유지한다. 인터페이스아이콘은공식SVG currentColor이며고대비도직접확인했다.'),
'ORC-F12':('수직하단nav의3px아이콘라벨gap','원문4px배수기준의국소예외다. nav64px안에서22px아이콘+8pxmark패딩+20px라벨+3pxgap의61px내용을중앙정렬한다. 200%에는73px로늘어나고가림방지패딩도같은토큰을따른다. 나머지공유inset20/내부12/섹션36/매장32는4px배수다.'),
'ORC-G07':('하단nav 3px gap','수직아이콘/라벨의광학적간격과64px탭바계산에한정한다. 일반헤더/섹션/카드간격은공유토큰의4px배수이며사방대칭을측정했다.'),
'ORC-G20':('하단nav 수직3px 간격','헤더/툴바간격과좌우20px정렬은일치한다. 수직탭만공유3px간격을써64px기본바와확대73px를검산했고가림이나중복safe-area가없다.'),
'ORC-F15':('퀵메뉴4개공식그림의개별색','사용자교정은색을일괄중립화해원본그림표현을지우지말라는맥락이다. P4/R1의대상구별을위해그림자체색을보존한다. 반복상태badge와일반entity아이콘에는확대하지않는다. 예약/취소상태chip은후속중립수정후두폭재검증했다.'),
'ORC-G04':('카테고리그림과사진콘텐츠의색','2개비회색상한을그림내용전체에적용하면관찰한풍부함을없앤다. P4에서명시한카테고리4종의fill/stroke와사진에한정한다. 조작은청색,오류는빨강,나머지는중립으로구별한다.'),
'ORC-A04':('브랜드없는제품의3개방향제안절차','사용자는현재참조결합의선택관점과관계를교정했다. 세팔레트투표를추가하지않고원본관찰→사진과행동의색온도대비가설→청색#245eea 실제비교로진행한다. 기본Tailwindblue500복제가아니며이청색을보편값으로승격하지않는다.'),
'ORC-A05':('동일역할퀵메뉴4열/테마2열','R1/R3에서가져온그림과라벨의스캔리듬을위한대칭이다. 억지비대칭을추가하지않는다. 매장목록은왼쪽사진/오른쪽정보의비대칭구조이고200%퀵은2열로적응한다.'),
'ORC-A07':('저장/뒤로/닫기/검색어삭제44px아이콘조작','R2저장/R4뒤로/R5닫기의관례와좁은모바일맥락에한정한다. 모든조작은구체aria-label/키보드/터치44px를가지며날짜·시간·nav·주CTA에는보이는라벨이있다. 저장은aria-pressed와선택면으로상태를표현한다.'),
'ORC-A09':('테마2개 동일사진격자와카페비교목록','R3의사진2열과R2의동일매장비교문법이채택관계다. 첫항목을근거없이크게만들거나CTA카드를끼워넣지않는다. 대신퀵그림/테마사진/정보목록/예약폼을역할별로다르게조합했다.'),
'ORC-A10':('서버없는동기식로컬체험에서loading/skeleton/삽화요구','검색0건·저장0건·예약0건·마감날짜·조건validation·취소/완료상태를직접실행했다. 실제데이터요청이없으므로가짜loading/네트워크retry를만들지않으며빈상태에불필요한장식삽화를넣지않는다. 실제API오류복구검증으로확대하지않는다.')}
PASS={
'ORC-F03':'짙은청색의흰14px시간/CTA는600이상,선택은700. 계산대비5.43:1/hover7.37:1이며밝은면의조건글자는5.35:1 이상이다.',
'ORC-F04':'독립영역에같은주CTA를복제하지않는다. 빈조건의상단초기화를제거하고empty에한개만유지함을390/320에서실행했다. 매장사진과이름은한매장탐색핫스폿이다.',
'ORC-F05':'카페는사진·분위기가핵심인4개시각목록이며열정렬이필요한청구서/유저표가아니다. 사진과조건/시간의소속을R2와대조했다.',
'ORC-F06':'빨강은조건오류에만쓰고청색은실행/선택,중립은예약상태다. 녹색나무는그림내용이며진행상태표시가아니다.',
'ORC-F13':'모든행동은button/a/input/select이고버튼pointer,disabled날짜not-allowed를실측했다. hover/터치/Tab도실행했다.',
'ORC-F14':'main/nav/header/section/ul/li/article/dl/dt/dd/fieldset/legend/dialog가역할을소유한다. div는사진정보grid/제목flex/선택grid/입력묶음이며무의미클릭div없다.',
'ORC-F16':'스크롤컨테이너는페이지와내용이긴dialog뿐이다. 빈/1개화면은전체높이844이며내부카드스크롤없다. 200%긴폼은시트에서스크롤해확인/완료까지실행했다.',
'ORC-G01':'app.css에linear/radial gradient없다. 사진자체명암을CSS그라디언트로오인하지않는다.',
'ORC-G02':'최종UI의그림자는없고hover도색변경뿐이다. 기존선택inset선언은최종P4 box-shadow:none으로해소되어장식깊이없다.',
'ORC-G03':'사진/입력/버튼/시트반경8px,nav표시와chip의pill만999px다. 마지막시트16px는P3에서8px로정리했다.',
'ORC-G05':'실hover0/40/100/200ms와해제에서색보간만발생하고width/height불변. transform/scale/shadow/opacity동작없다.',
'ORC-G06':'기본14/18/22의3개읽기크기,200%28/36/44의3개다. 실제DOM과각뷰스크린샷을대조했다.',
'ORC-G08':'소개hero/KPI없이검색→4조건→2테마→카페/시간을배치했다. 사진을확대해도첫시간bottom728/nav780으로실행진입이보인다.',
'ORC-G09':'요청없는로고/슬로건/장식선/장식배너없다. 사진과카테고리그림은실제필터탐색으로연결된다.',
'ORC-G11':'청색행동면흰글자는600/700이고대비5.43:1 이상. 최종안정선택면에서도흰글자유지확인.',
'ORC-G12':'동일초기화중복을제거하고선택조건0건에서정확히한reset을실행했다. 단계별확인/완료는서로다른행동이다.',
'ORC-G13':'20개이상표형데이터가없고4개가상카페의사진/조건비교에R2목록관계를사용한다.',
'ORC-G14':'오류는빨강,행동은청색,상태는중립. 그림대상색을진행/성공의의미색으로쓰지않는다.',
'ORC-G15':'기본page/sheet제목22px로24상한아래다. 200%사용자텍스트확대44px는설계의과대한기본제목으로계산하지않는다.',
'ORC-G21':'실행조작pointer,마감날짜disabled/not-allowed. 키보드/포인터/터치모두실제실행했다.',
'ORC-G22':'예약/요청/취소상태chip은같은중립면하나로후속수정했다. 청색선택필터와카테고리작품은상태badge가아니다.',
'ORC-G23':'빈/1개목록은중첩스크롤0. 긴페이지와모달폼외스크롤컨테이너없고200%시트하단CTA도실행가능하다.',
'ORC-G24':'카페ul/li/article,예약ul/li,조건/요약dl,날짜fieldset/legend/dialog를확인했다. 의미없는wrapper가주데이터구조를대신하지않는다.',
'ORC-A01':'사진/선택/버튼8px,작은nav표시와chip pill,카페article무테두리와개별그림실루엣으로역할이구별된다.',
'ORC-A02':'흰바탕하나로모든표면을합치지않는다. 검색/미선택/조건은중립면,사진은탐색중심,선택/주CTA는청색,시트는backdrop으로층을구별한다.',
'ORC-A03':'P4최종box-shadow없음. 초점은outline이며시트깊이는backdrop으로표현한다.',
'ORC-A06':'매장이름/음료가격/입장공간/크기/준비조건/시간이hover없이표시된다. 첫매장전체가390/320첫뷰에서보이고허위별점은추가하지않는다.',
'ORC-A08':'4개실제분위기사진과공식Lucide경로를사용한다. 전체이미지대체나Imageplaceholder없고이미지오류0. 가상매장사진이라는고지를확인단계에보존한다.',
'RUI-01':'원본image-px와CSS/DPR미상을구별하고P4값을chosen/가설로명시한다. 원본제작자의실제의도나애니메이션을단정하지않는다.',
'RUI-02':'최종CSS역할토큰정의→참조→사용을검산했다. 미정의/미사용0. 일반SVG색은currentColor,카테고리fill/stroke/크기는별도역할토큰이다.',
'RUI-03':'catalog v4 활성75와각원래checks를유지하고프로젝트7개를추가했다. 예외는대상과실제근거를명시하고거절판정을보존한다.',
'RUI-04':'지역/이름/4조건/2테마/저장/상세/날짜/시간/인원/반려동물/동의/요약/취소/예약·요청체험을390/320실제실행했다. 외부예약은범위밖이다.',
'RUI-05':'가격/입장공간/크기/이동가방/전용대관조건을목록·상세·확인에연결한다. 단순원본외형복제나사진시안으로대체하지않는다.',
'RUI-06':'앱JS와독립검증JS에기존anti-slop규칙전체Oxlint와checkJs를실행했다. 기록한범위에서오류경고0이며실행스크립트와증거를연결한다.',
'RUI-07':'중립검색/그림조건/사진테마/명확한매장시간의순서와면적을사용자의탐색→조건판단→예약에연결한다. 색면적/시선순서를원본과대조했다.',
'RUI-08':'새브랜드마크/슬로건없다. 페이지제목은카페찾기,기능그림은조건필터이고브랜드로전용하지않는다.',
'RUI-09':'일반28상태와확대/고대비16상태의읽는글자14px하한/가로넘침0을실측했다. 시간숫자와확대퀵라벨의음절분리를후속수정했다.',
'RUI-10':'회색검색/필터,작은nav표시와청색시간/확인CTA의강도가구별된다. 보조행동도44px면을가지며숨은텍스트실행이없다.',
'RUI-11':'실제예약아님안내는확인행동전후에필요한사실로위치한다. 사진/조건은판단정보이며슬로건/중복보조설명없다.',
'RUI-12':'공식Lucide경로템플릿clone을검산했다. 카테고리의fill/stroke만각색하고새경로를만들지않았다. 저장/닫기/뒤로명칭과고대비표시를실행했다.',
'RUI-13':'빈/한매장/긴목록과200%에서내용가림없이실행했다. main/nav같은가림방지토큰,내부카드스크롤0,긴모달만overflow를쓴다.',
'RUI-14':'앱에hr/영역bar/탭기준선/밑줄없다. 실제렌더에서간격과사진/표면으로그룹이구별된다. 입력윤곽/포커스는조작역할로보존한다.',
'RUI-16':'이전부분adapted판정을철회하고사용자FAIL을보존했다. P4 Q1–Q5 원본/결과비교에서중립면/강조/그림/사진/그룹쉼을새로판독했다. 고유일러스트의완전동급주장은하지않는다.',
'RUI-17':'P4전체는그림/사진탐색과작은고채도실행을구별하며매장간쉼이내부간격보다크다. 베이지평탄화실패를청색치환만으로닫지않고전체시선/밀도/관련화면을직접대조했다. 내부확인범위이며사용자승인은대기다.',
'RUI-18':'reference-brief의B1탐색/B2테마/B3예약선택을R1–R5와Q1–Q5에누적연결한다. 단일마지막출처만구현하지않는다.',
'RUI-19':'nav3목적지는아이콘22+라벨14+작은선택면으로64px이며주CTA의전체청색채움과구별된다. 탭복귀/초점/200%73px/safe-area한번을검증했다.',
'RUI-20':'상세h1/예약시트surface-title22px가18px섹션과14px라벨보다강하다. 본문스타일로폼목적제목을내리지않는다.',
'RUI-21':'날짜/시간선택면과인원/동물select를같은입력체계로구현했다. 마감/선택/요약/초안/명시날짜재진입/취소를실행하고안정색상일치를검산했다.',
'RUI-22':'main좌우20과dialog좌우20,헤더/사진/CTA정렬을같은폭에서비교했다. nav높이와main가림방지는동일토큰이고검색focus전후박스불변이다.',
'RUI-23':'탐색/저장/예약/상세/예약폼/요약/완료를390/320동일폭묶음으로직접대조했다. 흰면/먹색정보/청색실행/중립보조역할이이어진다.',
'RUI-24':'목록날짜는매장별시간의공유맥락한번,요약일시는선택확인역할한번이다. 예약상태와실제미접수고지는서로다른사실이고초기화중복은제거했다.',
'RUI-25':'퀵/테마/목록은36px쉼과각자의그림/사진/정보구성,매장내12와사이32로구별된다. 선제거가경계제거로이어지지않는지전체화면에서판독했다.'}
PROJECT={
'PROJECT-REFERENCE-SYNTHESIS':'P4 Q1–Q5의색면적/명도/그림/사진/그룹리듬을원본과직접비교했다. 원본HEX복사나기능통과를품질승인으로확대하지않으며고유일러스트풍부함차이를남긴다.',
'PROJECT-LOCAL-FLOW':'검색→조건/테마→저장/상세→날짜시간인원동물→필수조건→요약→완료/내역/취소를두폭과터치/키보드로실행했다.',
'PROJECT-DATE-DRAFT':'상세18일초안은보존하고닫기후목록9월12일14시클릭은명시12일로새로선택됨을독립실행했다. 취소/닫기중예약0건과summary이전초안보존도확인했다.',
'PROJECT-PROTOTYPE-TRUTH':'가상매장/사진/메뉴가격역할과실제미전송·미예약을확인전후에표시한다. 맹견은전용단독대관/사전확인/별도요청체험/미정대관비로구별한다.',
'PROJECT-ACCESSIBLE-STATES':'390/320/200%/forced-colors/reduced-motion/Tab/Escape/터치를실행했다. 시간숫자한줄/퀵확대2열/공식SVG고대비/실초점/가림방지를확인했다.',
'PROJECT-HISTORY':'사용자거절P3앱/문서/증거의sha256스냅샷을보존했고이전adapted전체판정을철회했다. P4이후국소교정도사전고정입력으로꾸미지않고후속기록했다.',
'PROJECT-BOARD':'부모검증1100/390/320의liveiframe필터/5개details키보드/이미지/가로넘침결과와P4 Q비교보드를직접열람했다. 보드원본상대링크아카이브는독립실행판정밖이다.'}
def evidence(kind,relative):
 return {'kind':kind,'path':relative,'sha256':hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()}
base={'spec':['gate-review.md','prompt-v4.md','style-analysis.md'],'code':['app.html','app.css','app.js','evidence/review-p4/code-checks.txt'],'visual':['evidence/review-p4/final-home-390.png','evidence/review-p4/final-home-320.png','evidence/review-p4/final-validation-390.png','evidence/review-p4/final-validation-320.png','evidence/review-p4/final-bookings-390.png','evidence/review-p4/final-bookings-320.png'],'interaction':['evidence/review-p4/review-browser.json','evidence/review-p4/review-accessibility.json','evidence/review-p4/final-checks.json']}
rules=[];results=[]
items=catalog['rules']+[{'id':key,'status':'active','checks':['spec','code','visual','interaction']}for key in PROJECT]
for item in items:
 if item['status']!='active':continue
 rid=item['id'];assert rid in NA or rid in EX or rid in PASS or rid in PROJECT,rid
 scope=EX[rid][0] if rid in EX else 'P4 모바일카페탐색/상세/로컬예약과해당상태'
 reason=NA.get(rid,EX[rid][1]if rid in EX else PASS.get(rid,PROJECT.get(rid)))
 exc=f'R4-P4-{rid}'
 rules.append({'id':rid,'applicable':rid not in NA,'scope':scope,'reason':reason,'checks':item['checks'],'exceptions':[{'id':exc,'scope':scope,'reason':reason,'basis':'사용자 색역할/관계 교정, P4 고정계약, 원본 R1–R5 직접관찰 및두폭/상태실행. 원본미공개복제의일괄예외가아님.'}]if rid in EX else []})
 ev=[]if rid in NA else[evidence(kind,file)for kind in item['checks']for file in base[kind]]
 if rid in ['RUI-16','RUI-17','PROJECT-REFERENCE-SYNTHESIS','PROJECT-BOARD']:
  ev.extend(evidence('visual',f'evidence/p4-Q{q}-comparison.png')for q in range(1,6))
 if rid=='PROJECT-BOARD':ev.append(evidence('interaction','evidence/p4-board-checks.json'))
 if rid in ['PROJECT-ACCESSIBLE-STATES','RUI-09','RUI-13','RUI-19','RUI-21','RUI-23']:
  ev.extend(evidence('visual',f'evidence/review-p4/review-{name}-{w}.png')for name in ['large-home','large-booking','forced-focus']for w in [390,320])
 result={'id':rid,'status':'not-applicable'if rid in NA else'exception'if rid in EX else'pass','reason':reason,'evidence':ev}
 if rid in EX:result['exception_id']=exc
 results.append(result)
contract={'schema_version':1,'catalog_version':catalog['version'],'targets':['app.html','app.css','app.js','assets','references','sources.json','reference-brief.md','style-analysis.md','DESIGN.md','prompt-v1.md','prompt-v2.md','prompt-v3.md','prompt-v4.md','index.html','board.css'],'rules':rules}
p=ROOT/'gate-contract.json';p.write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
report={'schema_version':1,**gate.fingerprints(ROOT,CAT,p,contract),'results':results}
(ROOT/'gate-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
