# 최종 코드·실행 검증

2026-09-11. npm run build(exit0), TypeScript checkJs(target es2022/module esnext/moduleResolution bundler/dom)로 .build/entry.js 전체 소유 소스 검사(exit0). 동일entry와build.mjs를 기존todo/.oxlintrc.json의모든anti-slop일반규칙/deny-warnings로검사(exit0). 규칙을완화하거나타입단언으로우회하지않았다. 외부입력은Zod계약에서파싱한다. 아이콘·Zod라이선스는dist에보존한다.

verify.cjs: 1440/1024/390/320 각각목록/검색/상태필터/복제독립/편집/새문서/재로드저장/보관/복원/버전저장/변경섹션비교/복원전안전버전/경력·학력추가/기간점검/공고대조/미리보기/백업·불러오기를실행했다. 대화상자Escape, 200%문자, reduced-motion, forced-colors 포함. file진입320/1440, 저장Quota실패도검사. 최종exit0와interaction-results.json 확인.

verify-extra.cjs: 필터키보드초점, 연월취소·선택해제·초점복원, 잘못된백업거절, 손상된원본저장값보존, 텍스트하한/gradient/div비중/gap/icon치수 검사. 실제수치는extra-results.json.

지속로그: 월 선택 해제를 눌렀는데 기본submit으로원래값이재적용되는버그가추가검사에서발견됐다. 공통button helper에type=button을명시해수정하고추가검사통과했다. 초기반복형식의 전체버전비교는 실제대조에서수정항목을찾기어려워변경섹션우선으로개선했다.

범위: 실제OS스크린리더음성, 실물모바일IME, 프린터하드웨어, 로그인/서버동기화/AI는검증범위가아니다. 사용자문서나실제채용지원은전송하지않았다.

## 랜딩 추가 검증

- landing.js와 기존 통합 entry.js에 checkJs 및 oxlint를 실행해 오류 0건을 확인했다.
- verify-landing.cjs: 1440/1024/390/320 폭, 예시 전환, FAQ, 신규 작성, 기존 문서 보존, 200% 글자 확대, 강제 색상과 동작 줄이기, file 직접 열기 통과.
- 기존 verify.cjs와 verify-extra.cjs를 workspace.html에서 다시 실행해 통과했다.
- landing-comparison.png와 landing-mobile-top.png를 실제 판독했다. 문서 중심 위계와 단일 주요 행동을 유지하고, 공개 레퍼런스의 AI·로그인·사회적 증명은 구현 범위에 맞지 않아 가져오지 않았다.

## 푸터 후속 검증
HTML/CSS만 수정했다. 1440/390/320에서 푸터 링크 5개의 실제 이동·새 문서 생성 및 200% 확대 가로 넘침 없음 확인. footer-results.json과 footer-{폭}.png, footer-large-{폭}.png에 증거를 남겼다. 1440/390 및 확대390 이미지를 직접 판독했다. 기존 JS는 변경하지 않았다.
