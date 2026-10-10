# Better Cities Original 6.6.0 + Imperial City 호환 패치 6.6.0a — 한국어 번역 검수 완료

**2026-10-10 본편 6.6.0 + IC 6.6.0a 통합 FOMod 로컬 제작 완료 · Nexus/GitHub 릴리스 미게시**

| 항목 | 건수 |
| --- | ---: |
| 총 검수 대상 | 16,182 |
| 승인 | 12,386 |
| 교정 | 3,796 |
| 문맥 보류 / 미검수 | 0 / 0 |
| 원본 텍스트 필드 매칭 | 24,266 |
| 한국어로 변경한 필드 | 24,151 |
| 유지한 영문·식별자 | 115 |
| 번역으로 출력한 ESM/ESP | 78개 |
| 불필요한 변경이 없는 플러그인 | 9개 |

**진행 기록의 단일 기준:** [online-progress.json](reviews/online-progress.json) (마지막 배치 `wave174_context_047`). 총 969건의 문맥 재검토 항목을 모두 판정했습니다.

## 통합 한국어 번역 — Nexus 업로드용 단일 파일

바탕화면의 `Better Cities 6.6.0a 한국어 번역.zip`은 **Better Cities 오리지널 6.6.0 + IC 호환 패치 6.6.0a 번역을 합친 하나의 파일**입니다. ZIP SHA-256: `53181feb05a4947fcb5065aa3d8c2f1f499c47353c4448757c894e4b7ae1cd9c` (약 21.70 MiB).

원본 6.6.0 FOMod 폴더 구조(`00 Core`, `01 Better Cities`, `01 Better Cities Full`, `02 Better Imperial City`, `30 ...`, `31 ...` 등)에 맞췄습니다. 한국어 번역본 **69개**와 6.6.0a 업데이트 번역 ESP **9개**를 알맞은 원본 폴더에 배치해 **총 78개 ESM/ESP**가 들어 있습니다. 구분 폴더나 중복된 플러그인은 없습니다.

번역 파일만 설치하도록 원본 선택 구조를 수정한 `fomod/ModuleConfig.xml`과 `fomod/info.xml`을 포함합니다. 78개 파일이 모두 설치 선택 경로에서 접근 가능하며, 기존 FOMod가 참조하던 원본 리소스 중 번역본에 없는 파일 경로 19개를 제외했습니다. 기존 목록에서 누락됐던 **Werewolf Legends 호환 플러그인**과 번역된 **LINK 설정 CFG**는 별도의 선택 옵션으로 추가했습니다.

**설치:** 원본 Better Cities 6.6.0과 IC 6.6.0a를 먼저 설치한 뒤, MO2에서 이 통합 ZIP을 별도 모드로 설치합니다. 원본 설치 시 사용했던 FOMod 항목과 같은 항목을 선택하고 번역 모드를 파일 덮어쓰기 우선순위가 높도록 원본보다 아래에 둡니다. 호환 플러그인을 모두 활성화하지 마세요.

- [최신 통합 Nexus용 로컬 파일 및 검증 기록](reviews/final-integrated-nexus-package_20261010.json)
- [검수 최종 진행 상태](reviews/online-progress.json)
- [원본 화자 조건 오류 후보](reviews/source-errata-bravil-torro-melyssa_20261010.json)

원본 ESM/ESP는 수정하지 않았으며, 생성한 78개 번역 플러그인은 레코드 및 필드 기준 독립 대조를 통과했습니다. **실제 MO2 설치 화면을 눌러보는 테스트와 게임 내 한국어 출력 테스트는 아직 수행하지 않았습니다.** 기존 `<spit>` 표기는 사용자 지정대로 유지하고 토로/멜리사 원본 조건도 변경하지 않았습니다.

**Nexus 업로드 전 확인:** 번역본은 원본 모드에서 파생한 ESM/ESP 파일을 포함하므로 Better Cities 제작자의 수정·재배포 허용 조건을 확인해야 합니다. 이 대화에서는 실제 Nexus 업로드나 GitHub Release 생성은 하지 않았습니다.

## 검수 저장소 구성

- `active/`: 검수 당시 대기·문맥 항목의 원문 및 번역. 현재 진행 수치의 기준이 아닙니다.
- `snapshot/`, `snapshot-manifest.json`: 106차 작업 시점의 보존 스냅샷. 덮어쓰지 않았습니다.
- `reviews/`: 107~174차의 개별 번역 판정과 원본 증거, 검증 보고서.
- `scripts/`: 스냅샷 복구 스크립트.
- `GLOSSARY.md`: 확정 용어.

로컬 중간 작업물은 별도 보관 위치로 이동하여 원래 `D:\\Codex_Trans\\Better Cities 한국어 번역` 폴더에는 최종 ZIP만 남겼습니다. 번역 검수 데이터와 원본 모드 파일은 보존했습니다.
