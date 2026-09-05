# 상세 UI·실패 누적·판독기 검증

검증일: 2026-09-06. 실제 제품의 시각 품질 검증과 스킬/CLI 검증을 구분한다.

## 실행 결과

- 상세 분석의 기존 행동: [component-detail-baseline.md](component-detail-baseline.md). 기존 모델이 이미 잘 구분한 이미지 픽셀·CSS 단위·미확인 정보는 실패로 기록하지 않았다. 새 지침에는 요소/변형별 상세 인계와 토큰 사용 검사를 명시했다.
- 상세 분석과 토큰 적용: [component-tokens-green.md](component-tokens-green.md). 기존 토큰의 배경/전경과 실제 하드코딩 차이, 여백, 검은 채움 아이콘과 흰 윤곽 아이콘의 차이를 찾아 수정 방향을 제시했다. 승인된 1px 광학 보정은 이유 있는 예외로 보존했다.
- CLI RED: 스크립트 구현 전에 테스트를 실행하자 setUpClass에서 누락된 CLI로 실패했다(실행 테스트 0개). 이를 실제 UI 결함이나 17개 동작 실패로 표시하지 않는다.
- CLI GREEN: `python3 -m unittest discover -s evals -p test_design_gate.py -v` — 최종 21개 테스트 통과. PASS/FAIL/UNVERIFIED, 규칙/증거 누락, 중복, 검사 종류 약화, 미선언 예외, catalog/계약/기존·신규 소스 변경, 이력 중복 방지, 실패→해결 이력 보존, 불완전 이력 보호를 검사했다.
- 기본 catalog: 57개 활성 규칙 전체가 계약에 없으면 차단되는 것을 확인했다. ORC-F 16개, ORC-G 24개, ORC-A 10개를 원본 파일과 비교해 50개 원문의 연속 일치 및 SHA-256 일치를 확인했다. 추가 7개는 이 패키지의 작업 기준이며 orc 원본으로 표시하지 않는다.
- 외부 근거: anti-slop README·설치 스킬·일반 규칙 등록 코드와 Douglas persona·관련 지식 5편을 확인했다. Douglas의 6개 고정 revision 링크 경로를 저장소 트리와 대조했다. 전체 지식 폴더나 원문 LinkedIn 링크를 모두 읽었다고 주장하지 않는다.
- 스킬 5개의 YAML/메타데이터, 실제 로컬 문서 링크 33개, 개인 symlink 5개를 확인했다. `반환된 ui_url`처럼 명시된 예시 자리표시는 경로 검사에서 제외했다. [현재 형식 검사](structure-current.json).

## 검증 범위

CLI의 이미지 파일은 합성 바이트다. 이 테스트는 실제 이미지 판독, 판정자의 정직성, 접근성이나 제품 사용성을 검증하지 않는다. 소스와 증거의 해시도 실제 재검사 자체를 증명하지 않는다. 화면 비교와 행동 실행을 별도로 수행해야 한다.

현재 저장소에는 제품 TS/JS 구현이 없으므로 Oxlint/anti-slop을 설치·실행하지 않았다. Python CLI의 테스트 통과는 anti-slop lint 통과가 아니다. 실제 TS/JS 구현 작업에서는 해당 통합과 lint/typecheck를 별도로 수행하도록 스킬에 명시했다.
