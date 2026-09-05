# Essence + gate — independent synthetic evaluation

2026-09-06. One synthetic response after reading `reference-to-ui/SKILL.md`, product-reasoning, application-format, design-guardrails, design-tokens, anti-slop-code, dashboard, and `reference-review/SKILL.md`, review-criteria, design-gate and all active catalog rule originals. No product code, reference image, rendered UI, build log, lint result or project failure ledger was supplied or verified. Local skill sources were inspected; upstream revisions were not independently audited in this evaluation.

## Actual response to the scenario

이번 명세의 중심은 **판매자가 배송 지연 주문을 비교하고, 발송할 대상을 확인한 뒤 일괄 발송하는 일**입니다. 운영자가 쓴다는 점은 설계 가정입니다. 성공 상태는 선택한 대상과 실제 처리 결과가 일치하고, 실패한 주문을 구별해 다시 처리할 수 있는 것입니다.

R1/O1은 사용자가 전달한 ‘촘촘한 행’ 관찰입니다. 이미지를 직접 보지 않았으므로 `reference-unverified`이며, 원본의 행 높이·색·폰트·뷰포트는 unknown입니다. 사용자 관찰은 근거로 유지합니다. 아래는 `spec-only` 초안이며 컴포넌트 이름은 예정입니다.

| 결정/요소 | 명세와 배치 이유 | 빠지면 생기는 문제 | 확인할 기준 |
|---|---|---|---|
| D1/E1 지연 필터 | 표 바로 위에 지연 조건과 결과 수를 둡니다. 먼저 처리 범위를 판단해야 합니다. | 전체 주문과 지연 주문을 혼동 | 조건 변경 시 결과·선택 범위가 함께 설명됨 |
| D2/E2 주문 표 | R1/O1의 행 기반 비교를 유지합니다. 주문 식별자, 고객, 예정일·지연 기간, 발송 가능 여부를 정렬된 열에 둡니다. 식별자·고객은 왼쪽, 날짜·상태는 비교 가능한 고정 열입니다. | 카드 사이를 오가며 비교하거나 대상을 오인 | 긴 한국어 식별 정보가 읽히고 같은 열을 비교할 수 있음 |
| D3/E3 선택 대상 요약 | 고객 요청을 반영해 선택 후 표와 인접한 요약 영역을 표시합니다. 선택 수, 발송 가능 수, 제외 대상과 이유를 실행 버튼 앞에 둡니다. | 실행 전에 범위와 제외 조건을 알 수 없음 | 행 선택을 바꾸면 요약과 최종 대상이 일치 |
| D4/E4 일괄 발송 | 요약 안에 주 실행 버튼 하나를 둡니다. 필터 옆에 같은 버튼을 반복하지 않습니다. | 정보 확인과 실행이 분리되거나 중복 실행 유발 | 실행 중 재입력 방지, 부분 실패 시 실패 대상만 재처리 |

레퍼런스의 밀도와 정렬은 비교 비용을 줄이고, 새 요약은 실행 전 대상 확인을 돕습니다. 요약이 표를 지나치게 가리는 비용이 있으므로 선택 전에는 접고 선택 후에도 짧게 유지하는 방안을 채택합니다(`chosen`). 위치 고정은 관찰된 사실이 아니며, 스크롤 중 사용성 확인 전에는 일반 문서 흐름으로 명세합니다. 현재 페이지 선택만 지원하고 필터 변경 시 선택을 해제해 알리는 정책을 초안으로 정합니다. 전체 검색 결과 선택은 별도 요구 확인 전 범위에 넣지 않습니다.

큰 KPI 네 개는 지표의 의미·기간·결정 용도가 없어 이번 초안에서 채택하지 않습니다. 대신 필터 결과 수와 선택 요약을 씁니다. 주문마다 다른 색도 비교 순서를 왜곡하므로 중립 행과 텍스트 상태를 사용합니다. 이 판단은 `PROJECT-ORDER-COMPARE`와 `PROJECT-TARGET-SUMMARY`, ORC-F05/G13, F15/G22, G08/G09에 연결합니다. 시간 부족을 기능·장식의 근거로 삼지 않습니다.

브랜드 보라색은 요구사항으로 유지합니다. `EX-BRAND-PRIMARY`의 범위는 E4 주요 행동과 관련 포커스 표현이며, 모든 행의 상태 배지까지 보라색으로 바꾸는 허가는 아닙니다. ORC-A04의 브랜드 기준을 따르고 ORC-G04 색 수 검사도 유지합니다. 상태 배지의 ORC-F15/G22까지 일괄 해제하지 않습니다. 브랜드라는 이유로 실제 충돌이 없는 규칙을 허위 예외 처리하지 않으며, 값 확정 뒤 충돌하는 ID에만 이 예외를 연결합니다. 대비·disabled·focus 검증은 아직 unknown입니다.

그라디언트는 보라색 요구에 포함되지 않습니다. ORC-G01과 미세 그라디언트를 선택지로 제시하는 ORC-A02를 모두 남기고 이번 표면은 단색과 구분선으로 결정합니다. ‘그냥 결함 아님’으로 검사를 없애지 않습니다. 별도의 명시 요구나 관찰 근거로 채택할 때는 요소·상태를 한정한 예외와 검증 결과를 남깁니다. 동일한 행 표현은 표의 비교 목적에 맞고, 카드 변형 규칙 ORC-A09는 카드 그리드를 사용하지 않는 범위에서 미적용입니다.

명세 토큰은 다음처럼 연결합니다. 기존 프로젝트 값은 제공되지 않아 임의의 보라색 HEX를 공식 토큰으로 선언하지 않습니다.

| 토큰 | 역할·값/참조 | 근거·상태 | 예정 사용처·상태 / 검증 |
|---|---|---|---|
| color.brand | 브랜드 기본색, 값 unknown | 사용자 요구 | E4 기본 배경 / 기존 토큰 조회 |
| action.primary.background | 의미색 → color.brand | D4, chosen 관계 | E4 기본 / 실제 대비 미검증 |
| action.primary.foreground | 글자·아이콘 공통색, 값 unknown | D4 | E4 기본 / 배경과 함께 결정 |
| border.subtle | 표 구분선, 값 unknown | D2 | E2 / 실제 렌더 필요 |
| control.padding.block / inline | 컨트롤 사방 여백, 값 unknown CSS-px | E1/E4 | 상하·좌우 각각 같은 참조 / 기존 간격 체계 조회 |
| text.body / control.height | 글자 규격·컨트롤 높이, 값 unknown | E1–E4 | 긴 한국어·클릭 영역 / 뷰포트 확정 후 검증 |

hover/pressed/focus/disabled/loading의 배경·글자·아이콘·테두리 조합, 글자 크기/굵기/줄높이/자간, 반경과 gap은 기존 토큰 확인 후 E-ID에 보완합니다. 아이콘은 필수 정보에 사용하지 않으며 채택 시 패밀리·선/채움·크기·정렬을 함께 정합니다. 이미지 px와 CSS px를 같다고 추정하지 않습니다. 현재 이 값들이 unknown인 만큼 구현 가능한 상세 명세가 확정됐다고 보고하지 않습니다.

과거 실패는 삭제하지 않습니다. 원본 ORC ID와 규칙을 보존하고 실패 → 수정 → 재검증을 새 이벤트로 누적합니다. 재발은 같은 ID로 연결합니다. 이번 입력에 과거 기록 파일이 없으므로 읽거나 해결했다고 주장하지 않습니다. 규칙 자체가 틀렸다고 입증되면 삭제 대신 사유와 대체 ID를 붙여 deprecated 처리합니다.

TS에서 `as unknown as T`를 반복하거나 lint를 꺼서 통과시키는 방식은 채택하지 않습니다. 외부 응답은 경계에서 파싱하고 내부에는 명명된 계약을 전달합니다. 구조화된 객체 매개변수 자체가 금지는 아닙니다. `no-object-parameters`는 느슨한 `object` 타입을 다루며, 원본 타입 가드·cause 등의 허용 조건도 보존합니다. 필요한 단언은 실제 불변 조건과 SAFETY 근거가 있어야 합니다. 구현 시 anti-slop 일반 규칙을 error로 적용한 lint와 typecheck 결과를 확인하고, Effect 규칙은 해당 의존/요구가 있을 때만 적용합니다. 지금은 명세이므로 설치·실행 결과를 주장하지 않습니다.

완료는 두 범위로 나눕니다. 이번 요청은 명세와 검증 계획 전달로 종료할 수 있고 상태는 `spec-only`입니다. 미정 상세값은 위와 같이 명시합니다. 제품 구현 완료에는 필터 → 선택 → 요약 → 실행 → 부분 실패 복구의 실제 동작과, 목표 폭·높이에서 표 밀도·긴 내용·색상 대비·포커스·로딩/빈 결과/오류를 확인한 증거가 모두 필요합니다. 빌드 통과는 시나리오가 전달한 정보일 뿐 제가 실행한 결과가 아니며, 시각·행동 판정은 `not-verified`입니다.

자동 게이트는 모든 active ID의 적용 범위와 PROJECT 규칙, 선언된 예외를 보존하고 실제 판독 증거 및 소스 해시와 함께 검사합니다. 명세 계약은 spec 범위에서 판단하며 이를 구현 게이트 PASS로 바꾸지 않습니다. 구현 계약에 visual/interaction 증거가 없으면 UNVERIFIED로 남깁니다. 도구는 기록과 증거 무결성을 검사할 뿐 미관을 자동 판독하지 않습니다. 여기서는 자동 게이트를 실행하지 않았습니다.

## Assessment

Behavioral result: the response demonstrates the requested reasoning on this single synthetic case. It produces an order-workflow artifact, keeps the reported reference separate from direct observation, joins dense comparison with pre-send summary, bounds brand use, retains original/conflicting IDs and history, rejects lint laundering, and separates spec delivery from verified implementation. This is an evaluator assessment, **not** a design-gate PASS or product verification.

Concrete remaining gaps: no supplied reference identity/image, existing tokens, viewport, actual data/API eligibility contract, past failure ledger or executable product evidence. The response is a useful contract draft; its unresolved element metrics and state token combinations preclude calling it a fully resolved implementation specification. It names scenario-relevant rules but does not serialize applicability for every active ID; no complete gate-contract/report was produced or checked. These omissions are disclosed rather than converted into passes.

One documentation ambiguity to resolve: design-gate.md requires every active rule and forbids reducing catalog `checks`, while also requesting a separate spec-scope contract for spec-only tasks. The instructions do not show a worked contract encoding for applicable mixed spec/visual rules in that mode. A future implementer could wrongly drop visual checks or mark the whole rule inapplicable. This evaluation avoided both by making no automatic gate claim, but an explicit valid spec-only example would improve reproducibility.

## Follow-up assessment — spec-only clarification

Read the added “명세만 요청된 경우” subsection in design-gate.md. It closes the reported documentation loophole: spec-only artifact delivery may end without forcing implementation; a prepared implementation contract preserves every active ID and its checks; the RUI-07 example remains applicable with spec + visual and reports unknown when no render exists. It explicitly forbids removing visual or marking the whole rule not-applicable merely because implementation is absent. The example is correctly identified as partial CLI input. Original finding remains above as history. This follow-up verifies the written instruction only; no CLI execution, rendered evidence, or product/gate PASS is claimed.
