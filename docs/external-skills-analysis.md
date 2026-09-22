# 외부 스킬 분석과 samkill 반영

2026-09-14 사용자 요청: Jakub Krehel의 스킬을 주로 분석하고 Yetone의 kill-ai-slop도 참고해 현재 `skills/`를 보완한다. 제품 샘플이나 개인 설치 설정을 바꾸는 요청은 아니다.

## 확인한 원본

- 주 자료: [jakubkrehel/skills](https://github.com/jakubkrehel/skills/tree/267330e1adfc66a718fb65fa6918c1f06d0a689e/skills), revision `267330e1adfc66a718fb65fa6918c1f06d0a689e`. 11개 SKILL.md를 비교했다. MIT License 확인.
- 보조 자료: [yetone/kill-ai-slop](https://github.com/yetone/kill-ai-slop/tree/96d1ca568a1db7e1ef9a381644c744440f816ee4/skill), revision `96d1ca568a1db7e1ef9a381644c744440f816ee4`. SKILL.md, taxonomy/detection/fixes와 scanner의 입력·필터·억제 인터페이스를 확인했다. Apache-2.0 License 확인. 스캐너 전체 구현의 정확성·테스트는 감사하지 않았다.
- [파일 목록과 SHA-256](../evals/results/external-skills-2026-09-14/source-inventory.json)은 재조회 기준이다. 목록에 있다는 사실과 본문을 분석했다는 사실은 다르다.

Jakub의 상세 확인 범위는 `break/scenarios.md`, `interface-review/removed-signals.md`, `better-typography/{wrapping-and-punctuation,details-and-accessibility,variable-fonts-and-opentype}.md`, `better-accessibility/{forms,screen-readers,focus-and-keyboard,motion-and-zoom}.md`, `better-colors/contrast.md`다. 나머지 보조 파일·실제 데모·외부 연결 글의 전체 검증은 포함하지 않는다. 외부 스킬은 분석 자료이며 그 안의 설치·승인·작업 중단 지시를 이번 작업의 실행 지침으로 채택하지 않았다.

## Jakub: 담당 역할과 보완 위치

| 원본 스킬 | 기존 samkill과의 비교 | 반영 결정 |
|---|---|---|
| better-interface | samkill도 실제 증거와 사용자 영향을 보지만 공통 원인의 보고 단위가 덜 구체적 | [변경 리뷰](../skills/reference-review/references/change-review.md)에 원인 하나와 전체 사용처를 묶고 변경 귀속·제품 게이트를 구별 |
| interface-review | 삭제된 접근성·상태 신호를 diff 양쪽에서 추적하는 절차가 유용 | 위 문서에 기준 ref, 변경 전후, 동등한 대체, 공유 토큰 영향 범위 추가 |
| better-layout | 관계별 간격·패딩 소유권은 이미 강함 | 고정 배수 추가 없이 [상태 검증](../skills/reference-review/references/state-stress.md)에 형제 압축과 컨테이너/실제 viewport 차이 보완 |
| better-typography | 글자 하한은 있으나 실제 폰트와 대체 폰트·변수 길이 검토가 분산됨 | [타이포그래피](../skills/reference-to-ui/references/typography.md)에 로딩·혼합문자·전체 값 접근·숫자 정렬 통합 |
| better-colors | 토큰 정의→참조→사용처는 있음 | [토큰 계약](../skills/reference-to-ui/references/design-tokens.md)에 역할 오용, 합성 배경, 테마·사진별 대비 기록 추가 |
| better-accessibility | 키보드·포커스·동작 줄이기는 있음 | 상태 검증에 오류 연결·알림의 수명·초점 복귀·입력 도구 호환을 구체화 |
| better-ui | 모션 중단·광학 정렬 기준은 있음 | 토큰 계약에 반경 소유권과 스피너 중심·전환 중단 판독 보완. 고정 모션 프리셋은 채택하지 않음 |
| better-writing | 토스 8원칙과 사실 보존은 유지할 강점 | [한국어 문구](../skills/ux-copy/references/korean-writing.md)에 켠 상태의 토글 문구, 완전한 번역 문자열, 반복 오류의 흐름 문제 구별 추가 |
| explain-interface | 관찰/추정 구별은 있음 | [분해 스킬](../skills/reference-decompose/SKILL.md)에 실측/계산/가설과 겹친 레이어의 작동 설명 추가 |
| variant | Q-ID 비교는 원본과 결과에 집중 | [결합 기준](../skills/reference-to-ui/references/reference-synthesis.md)에 필요할 때 한 판단 축으로 대안을 실맥락에서 비교 |
| break | 실제 사용자 실패 평가가 풍부하지만 재사용할 입력 축이 분산됨 | 상태 검증에 실제 컴포넌트·제품 데이터 경계에 따른 표본과 연속 전이 추가 |

## Yetone: 35개 신호를 적용하는 방법

35개 항목을 새로운 필수 금지 목록으로 복제하지 않았다. 색/타이포/문구/컴포넌트/모션/구조/새 유행이라는 관찰 묶음으로 읽고 [장식·문구 탐지의 판독](../skills/reference-review/references/deslop-triage.md)에 적용 조건과 반례를 연결했다.

- 01–06 색·그라디언트: 기존 색 역할·실패 목록과 대조. 단색·중립색으로 일괄 변경하지 않는다.
- 07–12 글자·강조: 정보 위계와 의미 없는 kicker/강조를 확인. 14px 하한을 어기는 예시값은 가져오지 않는다.
- 13–15 문구: 근거 없는 수사만 다듬고 검증된 수치·조건·가능성은 보존한다.
- 16–25 컴포넌트: 실제 상태 없는 점/배지, 무의미한 아이콘 타일, 겹친 표면을 확인. 독립 객체·실제 상태의 경계는 남긴다.
- 26–27 모션: 기존 상태 전환 기준에 연결하고 스피너 회전을 실제로 관찰한다.
- 28–32 구조: 장식 숫자와 실제 순서, 같은 모양의 반복과 의미 있는 목록, 중첩 패딩을 구별한다.
- 33–35 새 기본형: 검정 모노스페이스·크림 세리프도 제품 과제 없이 적용하면 관성이다. 특정 서체를 금지하지 않는다.

scanner는 문자열 위치를 찾는 도구다. CSS 토큰·런타임·이미지·한국어 의미·Q-ID의 긍정 품질을 검사하지 않는다. `--only/--skip/--exclude`와 `deslop-ignore`로 결과가 줄 수 있으므로 숫자 감소는 품질 향상의 증거가 아니다. 러시아어 추가 규칙의 존재를 한국어 지원으로 해석하지 않는다. 이번에는 scanner를 복사·설치·실행하지 않았고, 기존 dmmulroy/anti-slop 코드 검사와도 구별한다.

## 그대로 채택하지 않은 처방

| 외부 처방 | samkill 결정과 이유 |
|---|---|
| 구분선·hairline으로 구조 대체, 탭 underline | RUI-14의 사용자 금지는 유지. 간격·위계·표면으로 전달하고 입력/포커스 경계는 역할 구별 |
| 모션의 정확한 0.96/0.25/4px, 이미지 전체 outline | 기존 제품 토큰과 관찰 효과를 우선. 필요 없는 효과·경계를 만들지 않음 |
| 모든 반경을 하나로, 모든 색을 중립+단일 강조로 | 제품의 역할 차이·상태 의미·원본 핵심 관계를 보존. 기존 catalog의 예외 절차도 유지 |
| 작은 글자를 16px 선언 뒤 transform으로 축소 | 실제 표시 크기 기준을 우회하므로 채택하지 않음 |
| 모든 제목의 음수 자간, 영문 60–75자를 한글에 적용 | 실제 글꼴·언어·내용으로 결정. `ch`는 한글 글자 수가 아님 |
| APCA를 새 기본 합격 기준으로 사용 | 기존 프로젝트 대비 기준 유지. WCAG 판정과 별도 지표를 혼합하지 않음 |
| 오류에 네트워크 원인·재시도 자동 권고 | 확인된 원인만 표시. 결과 미상은 실패와 구별하고 실제 복구 가능성 확인 |
| 최대 15개 지적·5개 사용처, 한 번만 렌더, 시간이 들면 생략 | 보고 요약과 검사 범위는 구별. 필수 검사를 줄이지 않고 실제 실패 수정·재검증 지속 |
| 과거 결함은 변경 승인에서 제외 | 귀속은 구별하되 현재 제품 게이트에서 기존 실패를 해제하지 않음 |
| 작은 수정도 매번 대안 선택·적용 승인 요구 | 사용자 요청으로 승인된 수정은 진행. 필요 없는 재승인 절차를 추가하지 않음 |
| 브랜드 아이콘을 생성 모델로 대체 | 기능 아이콘은 기존 Lucide 기준. 요청 없는 로고 제작은 금지 |

외부 원문이나 구현 코드를 통째로 이식하지 않고 samkill의 기존 계약에 맞춰 새 한국어 지침으로 작성했다. 원본 링크·revision과 채택/배제 이유를 남긴다. 실제 upstream 파일을 향후 복사하면 해당 라이선스·저작권 고지를 함께 보존한다.

## 검증의 범위

### 후속: 아이콘·클릭 영역·레이아웃 상세

사용자가 아이콘/레이아웃 반영 여부를 확인한 뒤 추가 보완을 요청했다. 앞선 분석 범위에서 빠졌던 동일 revision의 `better-ui/icons.md`, `better-ui/icon-transitions.md`, `better-accessibility/hit-areas.md`, `better-layout/grouping-and-alignment.md`, `better-layout/spacing-and-adaptivity.md`를 전문 대조했다.

[아이콘 영역 계약](../skills/reference-to-ui/references/icon-controls.md)을 추가해 실제 그림·슬롯·유효 클릭 영역·초점, 이웃 충돌/가림, stroke/상태/방향을 연결했다. [요소 구성](../skills/reference-to-ui/references/ui-composition.md#레이아웃의-전환-조건과-읽기-순서)에 컨테이너 전환·시각/DOM 순서·숨은 내용 단서를 보완했다. 기존 토큰 문서에 남아 있던 label→icon 기본 규칙은 최신 사용자 기준과 모순이므로 역할·관례 중심 기준을 참조하도록 수정했다. 앞선 독립 리뷰가 이 모순을 발견하지 못한 사실을 후속 평가에 보존한다.

그대로 채택하지 않은 상세 처방: 고정 stroke값/모든 상태의 fill, 모든 교체의 scale·blur, 세트의 grid와 다른 크기는 무조건 흐리다는 주장, 클릭 영역 충돌 시 무조건 축소, 그룹 간격2배·조작 간격12/24px, 무조건 늦게 접기·행동 개수로 메뉴화. 대신 실제 사용 크기·제품 데이터·이벤트 대상·읽기 순서로 검증한다. WCAG 최소 클릭 기준은 [W3C 원문](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)에서 예외를 포함해 확인했다. 이 다섯 문서의 추가 분석을 upstream의 모든 보조 문서 분석 완료로 확대하지 않는다.

[평가 기록](../evals/results/external-skills-2026-09-14/results.md)에 수정 전 독립 판단, 수정 후 적용, 문서 검증과 미실행 범위를 구분한다. 원본 분석은 제품 화면의 시각 검증이나 스킬의 범용 효과 입증이 아니다. 이번에는 catalog 규칙·버전과 Python 판독기를 변경하지 않는다.
