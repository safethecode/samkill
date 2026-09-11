# Round10 모바일 청첩장

예시 인물·예식 정보와 생성한 웨딩 사진으로 만든 하객용 모바일 웹입니다.

- 미리보기: http://127.0.0.1:4200/
- dist/index.html을 직접 열어도 본문과 번들 기능을 사용할 수 있습니다. 파일/HTTP는 브라우저에 따라 별도 저장 공간을 씁니다.
- 실행: 저장소 루트에서 `python3 -m http.server 4200 --bind 127.0.0.1 --directory design/reference-language/round-10/dist`
- 빌드: `npm ci --prefix design/reference-language/round-10` 후 `npm run build --prefix design/reference-language/round-10`.
- 통합 확인: 현재 저장소의 todo Playwright 런타임을 사용하는 `node design/reference-language/round-10/verify.cjs`. 타입/lint 명령은 evidence/code-checks.md 참조.

## 사용할 수 있는 흐름
사진확대/이전·다음/방향키·터치,달력과ICS파일다운로드,지도검색·주소복사,연락안내,접힌예시계좌복사,참석인원·식사·불참과응답수정/삭제,축하글작성/수정/삭제,브라우저저장,공유지원시공유창/링크복사와권한거절시직접복사. 새로고침과입력취소·저장실패를구별합니다.

## 예시 범위
연락처는미등록으로실제통화/문자전송을하지않습니다. 계좌는실제송금에쓰지않는예시입니다. 예식장은가상이며지도는공식주소를확인한서울숲으로연결합니다. 일정파일에도예시라고표시했습니다. 응답과축하글은현재브라우저에만저장되어신랑·신부나서버에전송되지않습니다. 현재공유주소는로컬미리보기이며외부공개사이트는아닙니다.

## 에셋과 확인
사진2장은이작업에서생성한가상커플이며dist/assets에포함합니다. 기본생성원본은Codex generated_images의 exec-5392c2d8-0da1-42b8-9835-efeb1f35eefd.png와exec-55dcaecc-cb87-4e7c-a8e2-3c707fb9db83.png입니다. Lucide SVG원본/라이선스와Zod라이선스를함께보존합니다. [제품계약](DESIGN.md), [참조/구조](reference-brief.md), [검토](review.md)를참조하세요.
