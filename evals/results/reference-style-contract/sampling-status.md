# 독립 행동 평가 실행 상태

- 계획: 변경 전 새 컨텍스트 5회, 변경 후 새 컨텍스트 5회, exact-copy 및 무채색 반례.
- 변경 전 3개 파일은 /tmp/reference-style-contract-eval/control 에 복사했고 SHA-256은 eval-manifest.json에 있다.
- 첫 fork_turns=none spawn은 `agent thread limit reached`로 거절됐다. 평가 응답은 하나도 생성되지 않았다.
- 슬롯 확인 list_agents가 완료된 리뷰 에이전트의 답 전체를 자동 노출했다. 평가 담당에게 거절 UI 차이와 커스텀 한 안이 노출되었으므로 직접 답변을 독립 control로 대체하지 않는다.
- 부모 지시에 따라 추가 spawn 반복이나 CLI 우회를 하지 않는다.
- control 1–5: NOT RUN. updated 1–5: NOT RUN. 독립 표본 0/10.
- diagnostic-before.md는 리뷰 텍스트 노출 후 동결 스킬을 적용한 비독립 진단이다. 통계적 효과·분산·5회 기준 PASS를 주장하지 않는다.
- 변경 후 적용과 반례는 동일 평가 담당의 후속 진단으로만 보고한다. 구현 품질의 증명과 별개다.
