# UIbowl 실제 연결 확인

확인일: 2026-09-06. `search_components(component_type="바텀시트", pattern="결제", category="커머스", country="한국", platform="MOBILE", limit=3, page=1)` 한 번 호출 성공. 반환 3개, 전체 12개, 대표 이미지 3개 첨부. 추가 페이지는 조회하지 않았다. 아래는 대표 정지 화면을 직접 확인한 관찰이다.

| ID | 출처 | 관찰 | 범위/제약 |
|---|---|---|---|
| R1 | [쿠팡](https://uibowl.io/name/%EC%BF%A0%ED%8C%A1?patterns=%EC%98%88%EC%95%BD%C2%B7%EA%B2%B0%EC%A0%9C&imgId=usu873awuevh9q67ncsnuxbi) | 상품 화면 위 시트. 가격·배송·수량을 압축해서 표시, 장바구니와 바로구매를 병렬 배치 | 원본 정확한 수치·고정 동작·결제 후 전이 미확인 |
| R2 | [IKEA](https://uibowl.io/name/IKEA?patterns=%EC%98%88%EC%95%BD%C2%B7%EA%B2%B0%EC%A0%9C&imgId=clvg6nuqm0018kv081731i5zw) | 주소 저장 질문, 설명, 주소 요약, 검은 pill 버튼, 나중에 텍스트 행동 | 거래 실행 화면이 아닌 주소 저장 결정. 개인 주소 내용은 평가 기록에 복제하지 않음 |
| R3 | [올리브영](https://uibowl.io/name/%EC%98%AC%EB%A6%AC%EB%B8%8C%EC%98%81?patterns=%EC%98%88%EC%95%BD%C2%B7%EA%B2%B0%EC%A0%9C&imgId=cmj8689m0001ejs04ekdnat98) | 배송 방법 변경 제목, 상품 목록, 라디오 선택지, 취소/확인 행동 | 변경 확정 후 동작과 실제 API 정책 미확인 |

공통: 배경이 어두워지고 하단 밝은 시트가 현재 결정을 강조한다. 차이: 구매 옵션/주소 저장/배송 변경으로 과제가 다르므로 태그가 같다는 이유로 같은 UI 명세를 만들면 안 된다.

스킬 규칙 검증: 동일 바텀시트라도 큰 pill 버튼과 작은 사각 버튼이 공존한다. 반경 전면 금지가 아니라 과제·관찰에 따라 채택해야 한다. 정지 화면으로 애니메이션/고정 위치/다음 단계는 검증하지 못했다. 메타데이터의 data_month를 스크린샷 수집일로 단정하지 않았다. 이 테스트는 연결·조회·이미지 관찰 확인이며 코드 구현·브라우저 검증은 아니다.
