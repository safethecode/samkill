# Round8 냉장고로 한 끼

`dist/index.html`을 브라우저로 직접 열거나, `dist`에서 로컬 HTTP 서버를 실행해 사용한다. 파일 미리보기에서도 실행되도록 일반 스크립트 번들을 제공한다.

원본은 `dist/data.js`, `dist/icons.js`, `dist/app.js`다. 원본 수정 후 저장소 루트에서 `python3 design/reference-language/round-08/build.py`를 실행한다. 생성된 `dist/app.bundle.js`는 직접 편집하지 않는다.

파일과 HTTP 주소는 브라우저 저장 공간이 서로 다르다. 실제 카메라는 브라우저 권한과 실행 환경의 지원이 필요하다. 사진 속 재료는 사용자가 선택하며 자동 인식 서버는 연결하지 않았다. 음식 사진은 reference-brief.md에 출처를 기록한 로컬 실험 자료다.

## 사용자 교정 검증

- index.html 직접 열기에서 모듈 CORS 차단으로 빈 화면이 재현됐다. 일반 스크립트 번들로 수정했다.
- 파일/HTTP 각각 320·390 폭에서 첫 화면과 냉장고·사진 등록 이동을 확인했다. `evidence/entry-results.json`과 해당 스크린샷 참조.
- 버튼 간격 4px, 선행 동작 아이콘과 텍스트 묶음의 중앙 정렬, 외부 SVG 요청이 막혀도 아이콘 표시, 필요한 재료의 옅은 표면은 `evidence/feedback-results.json` 참조.
- 이 기록은 해당 교정의 검증이다. 전체 디자인 게이트와 Round9 구현의 완료 판정은 아니다.
