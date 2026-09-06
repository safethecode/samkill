# Reference UI Skills

![Made with AI: 100%](https://img.shields.io/badge/Made_with_AI-100%25-blue)

사용자 문제 → UIbowl 레퍼런스 상세 분석 → 아이디어와 배치 결정 → 토큰 기반 구현 → 판독과 실패 누적으로 연결하는 개인 스킬 패키지예요. orc의 reference-first와 컴포넌트별 DO NOT을 분석해, 과제와 무관한 장식·레이아웃을 줄이는 방향으로 구성했어요.

| 스킬 | 호출 예시 | 결과 |
|---|---|---|
| `uibowl-research` | `$uibowl-research 한국 커머스 결제 바텀시트 레퍼런스를 분석해줘` | 출처, 실제 관찰, 후보별 채택·배제, 미확인 사항 |
| `reference-to-ui` | `$reference-to-ui 이 레퍼런스로 주문 관리 화면을 구현해줘. 우리 보라색 브랜드는 유지해` | 적용 계약, 코드, 검증 결과 |
| `reference-review` | `$reference-review 구현 화면을 레퍼런스와 비교하고 중요한 차이를 고쳐줘` | 근거별 차이, 수정 우선순위, 재검증 |
| `ux-copy` | `$ux-copy 이 결제 실패 화면의 문구와 노출 조건을 정리해줘` | 문자열 ID, 문구, 사실·행동 계약, 검증 |
| `onboarding-flow` | `$onboarding-flow 이 레퍼런스로 이메일 가입 흐름과 실패 복구를 설계해줘` | 관찰/제안 구분, 상태·전이 표, 검증 경로 |

## 작업 연결

이 저장소의 기본 작업 지침은 [AGENTS.md](AGENTS.md)에 있어요. 스킬을 만든 배경과 이번 대화의 요청·결정·교정은 [대화 맥락 기록](docs/session-context.md)에 남겼어요. 이후 중요한 기준 변경도 함께 기록해요.

구현 요청은 `reference-to-ui`에서 시작하면 돼요. 필요한 리서치와 리뷰를 연결하고, 이미 충분한 자료가 있으면 재검색하지 않아요. 문구·온보딩 스킬은 해당 과제가 있을 때만 사용해요. 모든 작업에 5개를 한꺼번에 로드하지 않아요.

프로젝트에 기존 문서 위치가 있으면 그 위치를 써요. 없으면 아래 결과물을 필요한 것만 만들어요.

```text
design/
  reference-brief.md      # R-ID 출처, O-ID 관찰
  design-contract.md      # D-ID 채택·배제·구현·검증 기준
  review.md               # V-ID 차이·심각도·재검증
  copy.md                 # C-ID 문자열·조건·동작
  flow.md                 # S-ID 상태, T-ID 전이
  gate-contract.json      # 적용 규칙·제외 항목·예외·소스 범위
  gate-report.json        # 실제 판독과 증거
  failure-events.jsonl    # 실패·수정·재발 이력
```

출처를 적었다는 것만으로 충분하지 않아요. 실제 이미지 확인 상태와 관찰 범위를 남기고, 중요한 구현 결정이 어느 관찰 또는 사용자 요구에서 나왔는지 추적할 수 있어야 해요.

## 디자인 기준

- 필요 없는 그라디언트·glow·glass·대형 카드·무지개 배지·장식 애니메이션을 자동으로 추가하지 않아요.
- “AI스럽지 않게”를 모든 화면의 회색 미니멀화로 해석하지 않아요. 명시된 브랜드와 콘텐츠 개성을 유지해요.
- 정지 화면에서 hover, fixed, 스와이프, 다음 단계를 확인했다고 하지 않아요.
- 관찰값과 추정값, 새로 정한 구현값을 구분해요.
- 실제 렌더와 동작을 확인해요. 빌드 통과를 시각 검증 통과로 쓰지 않아요.
- 한국어 문구는 사용자가 제공한 토스의 8가지 원칙을 적용해요. 번역투·중복 설명을 줄이고, 누른 직후의 행동·비용·선택권을 명확하게 써요. [한국어 글쓰기 기준](skills/ux-copy/references/korean-writing.md)에 전후 예시가 있어요.
- 세부 UI 분석에서는 [컴포넌트 상세 분석](skills/uibowl-research/references/component-anatomy.md)으로 상하좌우 여백·간격·글자·버튼 배경/글자/아이콘 색·아이콘 선과 채움까지 기록해요. 이미지 픽셀과 CSS 단위, 관찰과 추정은 구분해요.
- 디자인과 구현에 [토큰 계약](skills/reference-to-ui/references/design-tokens.md)을 적용해요. 기존 토큰을 재사용하고 기본값·역할·필요한 컴포넌트 변형을 연결해요. 실제 사용처와 상태별 색 조합까지 확인하며, 직접값 예외는 이유를 남겨요.

- [제품의 본질에서 배치하기](skills/reference-to-ui/references/product-reasoning.md)를 먼저 적용해요. Douglas 자료의 고객 문제·가치 관점을 사용자 행동과 각 요소의 배치 이유로 연결해요.
- 생성 코드에는 [anti-slop 기준](skills/reference-to-ui/references/anti-slop-code.md)을 적용해요. TS/JS 검사와 다른 언어의 검증을 구분해요.
- [디자인 게이트](skills/reference-review/references/design-gate.md)는 orc 원본 50개와 추가 기준 25개, 프로젝트별 제외 항목을 검사해요. 실패를 일반론으로 해제하지 않고 예외와 과거 결과를 보존해요. 스크립트는 판독 기록과 증거를 검사하므로 실제 화면 비교도 필요해요.

- [UI 구성 기준](skills/reference-to-ui/references/ui-composition.md)은 Todo 실사용 피드백을 반영해요. 임의 로고 금지, 글자 14px 하한, CTA/필터 구분, 불필요한 문구·구분선·스크롤 제거, 목록과 대화의 화면 분리를 다뤄요.

- [레퍼런스 결합 품질](skills/reference-to-ui/references/reference-synthesis.md)은 채택한 장점이 실제 구현에 남았는지 나란히 비교해요. 제외 항목을 지킨 것과 원본에 견줄 만한 품질을 별도로 판단해요.

- [여러 검색의 누적](skills/uibowl-research/references/research-plan.md): Todo와 채팅처럼 다른 과제는 각각 조사하고, 추가 페이지·후보·구현 적용을 누적해요. 모바일 탭도 별도 레퍼런스로 검토해요.

## 위치와 사용

이 폴더의 `skills/`가 관리 원본이에요. 개인 사용을 위해 `~/.codex/skills/`에 각 폴더를 연결하는 구성이에요. 기존에 같은 이름이 있으면 덮어쓰지 않고 먼저 비교해요. 이 저장소를 이동하면 연결 경로도 갱신해야 해요. 현재 대화의 스킬 목록이 갱신되지 않았다면 새 대화에서 호출하거나 해당 SKILL.md 경로를 직접 지정해 읽도록 할 수 있어요.

UIbowl MCP 인증과 연결은 실행 환경에서 제공해야 해요. 이 패키지는 인증 설정을 변경하거나 토큰을 보관하지 않아요. 다른 스킬은 사용자 이미지/관찰 자료로도 사용할 수 있어요.

## 확장과 검증

[orc 분석](docs/orc-analysis.md), [회귀 사례](evals/cases.md), [평가 기록](evals/results/baseline.md)을 함께 제공해요. `templates/`에는 다음 스킬을 만들 때 사용할 작성 틀이 있어요. 실제 역할이 달라지면 별도 스킬을, 같은 작업의 플랫폼·업종별 기준은 필요한 참고 문서로 추가해요.

스킬 형식은 YAML·메타데이터·문서 링크를 확인하고, 실행 도구는 `python3 -m unittest discover -s evals -p test_design_gate.py -v`로 검사해요. 형식 검증과 합성 행동 평가는 실제 제품에서의 디자인 품질 보장을 의미하지 않아요. 수행한 범위와 미검증 항목은 [검증 결과](evals/results/summary.md)에 기록해요.
