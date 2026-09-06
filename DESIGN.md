# Reference UI Skills 디자인 기준

## Overview

이 레포는 레퍼런스 기반 UI의 분석·구현·검수 스킬을 관리한다. 특정 제품의 색상·폰트·반경을 공통 프리셋으로 배포하지 않는다. Todo는 실사용 실패를 확인한 사례이며 모든 제품의 디자인 정답이 아니다.

사용자의 과제와 요소의 필요성·관계·적용 범위·판단 순서에 따라 배치와 강조를 정한다. [제품 판단 기준](skills/reference-to-ui/references/product-reasoning.md)과 [기본 작업 지침](AGENTS.md)을 적용한다.

현재 패키지 기준의 진입점으로 작성했다. 각 제품 레포는 [design-md](skills/design-md/SKILL.md)로 분석한 별도 DESIGN.md를 유지한다. 이 레포에는 제품 팔레트·글자 체계·반경 스케일이 없으므로 해당 섹션과 YAML 토큰은 생략한다. 실제 제품 UI 검증을 뜻하지 않는다.

## Layout

[요소 구성](skills/reference-to-ui/references/ui-composition.md), [토큰과 패딩 소유권](skills/reference-to-ui/references/design-tokens.md), [레퍼런스 결합](skills/reference-to-ui/references/reference-synthesis.md)을 적용한다. 공통 역할은 일관되게 연결하며 묶기·분리·이동·삭제는 사용자의 과제와 요소 관계로 판단한다.

## Components

제품별 관찰과 선택에서 토큰·상태·사용처를 연결한다. [UX 문구](skills/ux-copy/SKILL.md), [모바일](skills/reference-to-ui/references/mobile.md), 토큰 계약의 모션·경계·포커스 기준을 관련 작업에 적용한다. 정지 이미지로 상호작용을 검증하지 않는다.

## Do's and Don'ts

[실패 목록](skills/reference-review/references/failure-catalog.json)과 [리뷰 기준](skills/reference-review/references/review-criteria.md)을 적용한다. [맥락과 교정 이력](docs/session-context.md), [평가 사례](evals/cases.md)는 보존한다. 금지 목록 통과나 외형 일부 복제로 품질을 확정하지 않는다.

읽는 글자 14 CSS px 하한, 임의 로고/아이콘 제작 방지 등 명시된 사용자 기준을 유지한다. 제품 색·배치·타이포그래피는 해당 제품 근거에서 정한다. 미실행 lint·렌더·행동 검증을 통과했다고 하지 않는다.
