# Round9 이력서 작업실

`dist/index.html`은 랜딩페이지, `dist/workspace.html`은 이력서 작업실이다. 둘 다 직접 열거나 `dist`에서 로컬 서버로 열 수 있다. 개발 미리보기는 http://127.0.0.1:4199 이다.

- 새 이력서, 기본 정보/소개/복수 경력·학력/스킬 작성, 브라우저 저장
- 제목·직무 검색, 상태 필터, 독립 복제, 보관/꺼내기
- 이름을 붙인 버전 저장, 변경 항목 우선 비교/전체 비교, 복원 전 안전 버전
- 한글 연월 선택/해제, 입력·기간 점검, 공고의 스킬 문자열 대조
- 인쇄/PDF, JSON 백업과 검증 후 불러오기

예시 이력서3개는 편집 가능하다. 서버 동기화나 AI 연결은 없으며 공고 대조는 명시적 문자열 검사다. file/HTTP의 브라우저 저장 영역은 서로 다르다. 채용 서비스보다 우수하다는 실증 판정이나 채용 가능성 점수는 제공하지 않는다.

## 개발

이 폴더에서 `npm install` 후 `npm run build`. dist의 icons/model/view/app.js가 원본이며 classic scope를 결합한 .build/entry.js를 esbuild로 번들한다. Zod는 저장값과 백업파일 경계의 계약을 검증한다. 타입/lint는 결합된 소유 소스에 적용하고 외부 라이브러리는 해당 라이선스로 보존한다. 번들은 직접 편집하지 않는다.

루트의 `todo/node_modules`에 있는 Playwright/Chrome 환경으로 `node design/reference-language/round-09/verify.cjs`, `node design/reference-language/round-09/evidence/verify-extra.cjs`를 실행한다. 실제 검증 결과와 실패/수정 이력은 review.md와 gate-report.json을 참조한다.
