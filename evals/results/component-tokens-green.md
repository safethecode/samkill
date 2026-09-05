# CTA 상세 인계 및 CSS 리뷰

상태는 `spec-only / reference-unverified`예요. A는 사용자 관찰이며 이미지·DOM을 직접 확인하지 않았어요. B의 기존 토큰과 CSS는 제공된 검증 자료를 근거로 검토했어요. 아래 수정은 제안이며 실행하지 않았어요.

## A. 관찰과 미확인 값

R1/O1/E1: 주요 CTA 한 개, `user-reported`. 보이는 장면을 기본 상태 후보로 다루지만 실제 default 여부는 unknown이에요. 미리보기는 600×1200 image-px이며 원본 크기·CSS viewport·DPR·미리보기 배율은 모두 unknown이에요.

| 속성 | 관찰값·종류 | 인계 |
|---|---|---|
| 표면·전경 | 파란 배경, 흰 라벨과 흰 화살표, estimated | 정확한 HEX·불투명도·대비 unknown |
| 사방 거리 | 좌우 경계–내용 약 24 preview image-px, estimated; 상하 unknown | 실제 padding/margin·아이콘 내부 여백 분리 불가 |
| 아이콘–라벨 | 약 8 preview image-px, estimated | CSS gap unknown |
| 글자 | 잉크 높이 약 14 preview image-px, estimated | font-size·line-height로 변환 불가 |
| 아이콘 | outline, 둥근 선 끝, estimated | stroke 두께·join·패밀리·viewBox·박스 크기 unknown |

버튼 폭·높이·반경·테두리·그림자·외부 간격·부모 정렬·크기 규칙, 라벨 내용·서체·굵기·자간·줄 수, 아이콘 앞뒤 위치·수직 정렬은 unknown이에요. hover/pressed/focus/disabled/loading, 터치 영역과 키보드 행동도 unknown이에요. 관찰의 빈칸을 라이브러리 기본값으로 확정하지 않아요.

## B. 토큰 연결과 수정 제안

D1: 프로젝트의 기존 CSS 변수 체계를 유지해요. 기본 색/크기는 기존 토큰이고, 아래 역할 연결은 제안이에요. 파일 경로와 실제 선택자 이름은 제공되지 않았으므로 꾸며내지 않았어요. ‘사용 경로’는 제공된 primary button/SVG의 CSS 속성까지 나타내요.

| 토큰 | 계층·역할 | 값/참조·단위 | 근거·분류 | 사용 경로·상태 | 검증 |
|---|---|---|---|---|---|
| `--brand` | 기존 브랜드 색 | `#245EDB` | B, existing-token | primary button → background → var(--brand), 현재 | 제공 CSS에서 연결 확인 |
| `--on-brand` | 기존 브랜드 위 전경 | `#fff` | B, existing-token | primary button → color → var(--on-brand), 제안 default | 현재 color는 #111 |
| `--space-control` | 기존 간격; 세로 패딩 역할 제안 | 12 CSS-px | B, existing-token; 역할 chosen | primary button → padding-top/bottom → var(--space-control), 제안 default | 렌더 미검증 |
| `--space-inline` | 기존 간격; 가로 패딩 역할 제안 | 20 CSS-px | B, existing-token; 역할 chosen | primary button → padding-left/right → var(--space-inline), 제안 default | 렌더 미검증 |
| `--icon-control` | 기존 아이콘 크기 | 20 CSS-px | B, existing-token | primary button svg → width → var(--icon-control), 현재 | 제공 CSS 연결 확인 |
| `--icon-control-stroke` | 신규 제안, 컨트롤 아이콘 선 두께 | unknown | O1/D1, proposed·값 미결정 | primary button svg → stroke-width, 결정 후 적용 | 에셋 확인 필요 |

기존 전경을 아이콘에도 공유해요: `--on-brand → button color → SVG stroke: currentColor`. `fill: none`, `stroke-linecap: round`는 에셋/컴포넌트 규칙이에요. 기존 검은 fill은 제거하며, 실제 화살표가 채움 전용 경로라면 outline에 적합한 에셋으로 수정해야 해요. join/viewBox/선 두께는 에셋 확인 후 결정하고 미정 토큰 참조를 실행 코드에 넣지 않아요. 별칭 3단계나 라이브러리 교체는 필요하지 않아요.

제안 패딩은 `var(--space-control) var(--space-inline)`이에요. 이는 기존 시스템을 활용한 12/20 CSS-px 선택이며 24 image-px의 환산 결과가 아니에요. gap·글자·반경·테두리의 실제 기존 규칙은 추가 확인 대상으로 남겨요. 다크 모드는 추가하지 않아요. 다른 상태는 기존 정의를 먼저 확인한 뒤 필요한 전경·아이콘·배경·포커스 동작을 함께 정해야 해요.

## 리뷰와 완료 조건

| 항목 | 판정·영향 | 수정 및 재검증 |
|---|---|---|
| V1/E1/D1 라벨 | P1, 제공 CSS의 #111은 흰 라벨 요구와 명확히 불일치 | color를 --on-brand에 연결; 렌더에서 적용·대비 확인 |
| V2/E1/D1 아이콘 | P1, 검은 fill/no stroke는 흰 outline 요구와 불일치 | 위 SVG 규칙·에셋 적용 후 윤곽·끝·색 확인 |
| V3/D1 패딩 | P2, 14px 22px는 기존 간격 토큰을 우회함; 시각적 오차 크기는 판단 불가 | 12/20 역할 매핑 채택 후 사방 거리·내용 적합성 검증 |

승인된 직접값 예외: `해당 아이콘만 → transform: translateY(1px)`. 목적은 광학 정렬이며 전역 토큰으로 승격하거나 하드코딩 결함으로 거부하지 않아요. 실제 라벨과 나란히 렌더해 정렬·잘림을 검증해야 해요.

정적 검토는 제공된 선언의 요구 불일치와 참조 연결까지예요. 파일 전체의 덮어쓰기·미정의/순환 참조, 실제 에셋, 렌더·대비·뷰포트·상태 동작은 `not-verified`예요. 수정 실행이나 시각 검증 완료를 주장하지 않아요.
