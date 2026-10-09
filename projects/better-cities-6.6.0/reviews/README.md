# Better Cities 온라인 검수 (최신 108차)

- 기준: 106차 16,141건 검수, 41건 미검수
- 107차: g00764, g00808 직접 원문 대조 및 교정
- 108차: g00754, g00758 직접 원문 대조 및 교정
- **온라인 누적: 16,145/16,182건 (99.77%), 미검수 37건, 문맥 보류 969건**
- 교정 본문·원문 문자열 치환 근거: `wave107_book_desc_001.json`, `wave108_book_desc_002.json`
- 다음 작업: `online-progress.json`에서 `reviewed_ids` 4건을 제외하고 `active/pending-*.jsonl`을 검수
- `node scripts/validate-online-reviews.mjs`로 온라인 변경분의 재현 가능성 및 포맷 무결성 확인

**중요:** `active/`, `snapshot/`은 106차 불변 기준 자료입니다. 온라인 검수는 `reviews/`에 누적하며, 전체 16,182건 무결성 검사는 나중에 복구·병합 후 실행합니다.
