# Reference UI Skills 디자인 기준

## Overview

이 레포는 레퍼런스 기반 UI의 분석·구현·검수 스킬을 관리한다. 특정 제품의 색상·폰트·반경을 공통 프리셋으로 배포하지 않는다. Todo는 실사용 실패를 확인한 사례이며 모든 제품의 디자인 정답이 아니다.

사용자의 과제와 요소의 필요성·관계·적용 범위·판단 순서에 따라 배치와 강조를 정한다. [제품 판단 기준](skills/reference-to-ui/references/product-reasoning.md)과 [기본 작업 지침](AGENTS.md)을 적용한다.

현재 패키지 기준의 진입점으로 작성했다. 각 제품 레포는 [design-md](skills/design-md/SKILL.md)로 분석한 별도 DESIGN.md를 유지한다. 이 레포에는 제품 팔레트·글자 체계·반경 스케일이 없으므로 해당 섹션과 YAML 토큰은 생략한다. 실제 제품 UI 검증을 뜻하지 않는다.

## Layout

원본을 확보한 뒤 [reference-decompose](skills/reference-decompose/SKILL.md)로 관찰을 요소·관계·조립 언어로 번역하고 제품에 적용한다. 프롬프트 재현 실험의 사례별 값과 사용자 교정은 [별도 실험 기준](design/reference-language/DESIGN.md)에 둔다.

[요소 구성](skills/reference-to-ui/references/ui-composition.md), [토큰과 패딩 소유권](skills/reference-to-ui/references/design-tokens.md), [레퍼런스 결합](skills/reference-to-ui/references/reference-synthesis.md)을 적용한다. 공통 역할은 일관되게 연결하며 묶기·분리·이동·삭제는 사용자의 과제와 요소 관계로 판단한다.

형식 미지정 UI 디자인은 수정·렌더 가능한 화면을 기본으로 한다. [핵심 화면의 첫 비교](skills/reference-to-ui/references/reference-synthesis.md#핵심-화면의-첫-비교)에서 원본의 구조·위계·밀도를 확인하고 핵심 퇴보를 수정한 뒤 의존 화면으로 확장한다. 명시된 이미지 시안·명세·읽기 전용 범위는 유지한다.

## Components

제품별 관찰과 선택에서 토큰·상태·사용처를 연결한다. [UX 문구](skills/ux-copy/SKILL.md), [모바일](skills/reference-to-ui/references/mobile.md), 토큰 계약의 모션·경계·포커스 기준을 관련 작업에 적용한다. 정지 이미지로 상호작용을 검증하지 않는다. 입력의 실제 초점은 input/textarea에 유지하고 시각적 포커스는 필드 컨테이너의 inset box-shadow로 표현한다. border 변경이나 내부 입력 링으로 대체하지 않으며 고대비 대체 표시는 보존한다.

## Do's and Don'ts

[실패 목록](skills/reference-review/references/failure-catalog.json)과 [리뷰 기준](skills/reference-review/references/review-criteria.md)을 적용한다. [맥락과 교정 이력](docs/session-context.md), [평가 사례](evals/cases.md)는 보존한다. 금지 목록 통과나 외형 일부 복제로 품질을 확정하지 않는다.

읽는 글자 기본14 CSS px와 검증된 보조정보의 제한적12px 예외, 임의 로고/아이콘 제작 방지 등 명시된 사용자 기준을 유지한다. 제품 색·배치·타이포그래피는 해당 제품 근거에서 정한다. 미실행 lint·렌더·행동 검증을 통과했다고 하지 않는다.

영역 구분 바와 탭의 하단 기준선·선택 밑줄/이동 바를 사용하지 않는다. hr뿐 아니라 border·pseudo-element·shadow·gradient·SVG로 구현한 동등한 선도 포함하며, 단일 선이나 탭 관례도 예외가 아니다. 선택 상태와 영역 관계는 선 이외의 위계·간격·표면으로 전달한다. 입력/버튼 경계·키보드 포커스·실제 데이터 표현은 역할을 구별해 보존한다.

## 사용자 교정의 재사용

사용자 교정이 누적된 화면과 관련 패턴 확장에는 [재발 점검](skills/reference-review/references/feedback-regression.md)을 적용한다. 요구→원인→현재 기준→적용처→검증/미완료를 연결하며 사례의 고정값을 공통 프리셋으로 만들지 않는다. Round4부터 P12까지의 [피드백별 대응표](evals/results/round4-feedback-coverage.md)는 누락 점검 근거이며 다른 앱의 구현 계약을 대신하지 않는다.

## Round8 냉장고 재료 앱

[Round8 제품 기준](design/reference-language/round-08/DESIGN.md)은 음식 사진과 어두운 표면을 중심으로 요리 선택·재료 관리·사진 등록·조리 순서를 연결한다. CREME의 사진/제목/행동 대비를 주 시각 기준으로 삼고 재료 관리와 촬영 레퍼런스는 역할을 구분해 조합한다. 산호색과 사진 비율은 이번 제품의 선택이며 공통 스킬 프리셋이 아니다. 자동 사진 인식은 연결하지 않는다. 이전 라운드의 스타일 손실 지적을 Q-ID 비교와 교정 기록에 연결한다. Round9 이력서 웹 서비스 요청과 별개다.

## Round9 이력서 웹과 Round8 교정의 공통 반영

[Round9 제품 기준](design/reference-language/round-09/DESIGN.md)은 점핏의 문서 목록과 원티드의 중앙 문서 편집, 서핏·refresh.cv 공개 자료를 참고한 밝은 로컬 이력서 작업실이다. 지원처별 복제·변경 항목 비교·복원 전 보존을 실제 행동으로 연결하며, 팔레트나 폼 배치를 Round8에 전파하지 않는다. [검토](design/reference-language/round-09/review.md)에 비교 범위와 서버/AI 미연결을 명시한다.

Round8의 반복 교정은 [평가 기록](evals/results/round8-feedback.md)에 연결한다. 아이콘의 역할·관례·명시 요구·보이는 묶음 중심을 먼저 판단하며 특정 방향이나4px를 보편화하지 않는다. 맥락상 분명한 아이콘 단독 조작은 접근 가능한 이름·터치·초점을 유지한다. 표면/고정CTA/직접HTML진입은 기존 기준과 실제 실패에 연결해 적용 조건을 구별한다.

Round9은 사용자 요청에 따라 [랜딩 계약](design/reference-language/round-09/landing-contract.md)을 추가했다. 첫 진입은 서비스 소개와 실제 문서 예시이며 작성 도구는 workspace.html로 분리한다. 기존 밝은 문서 표면과 파랑 행동색을 유지하되 소개 화면의 제목 위계와 여백은 편집 도구와 구별한다.

Round8·9의 [종합 학습](evals/results/round8-9-learning.md)은 아이콘·표면·행동 대상·실제 진입·랜딩 마무리를 함께 다룬다. 랜딩은 [적용 계약](skills/reference-to-ui/references/application-format.md)의 영역·목적지로 전체 구성을 확인하며, 고정 간격이나 다열 푸터를 모든 제품에 전파하지 않는다.

## Round10 모바일 청첩장

[Round10 제품 기준](design/reference-language/round-10/DESIGN.md)은 가상 인물·생성 웨딩 사진·예시 예식 정보로 만든 하객용 모바일 청첩장이다. 사진·초대글에서 일정·교통·참석·마음 전하기·축하글·감사/공유까지 이어진다. 청첩장 특유의 중앙 서체와 여백은 이번 제품의 선택이며 도구형 Round9에 전파하지 않는다. [검토](design/reference-language/round-10/review.md)에 실제 로컬 동작, 예시/서버 범위, 확대·저장 충돌 교정을 남긴다.
