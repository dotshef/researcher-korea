출력 경로는 다음 규칙을 따른다. 모든 skill과 agent는 이 규칙을 참조한다.

## 그룹 폴더 매핑
- 프리랜서 마켓플레이스 → `output/freelance-marketplace/`

## 플랫폼
- 위시켓: `wishket`
- 원티드긱스: `wanted-gigs`
- 프리모아: `freemoa`
- 크로스 플랫폼: `total`

## 하위 디렉토리 구조

```
output/freelance-marketplace/{platform}/{topic}/{date}/
```

- **키워드 모드**: 입력된 키워드를 topic으로 사용 (예: "crm" → "crm", "쇼핑몰" → "쇼핑몰").
- **탐색 모드**: 키워드 없음 → topic을 `any`로 사용.

## 경로 예시

| 모드 | 경로 |
|------|------|
| 키워드 | `output/freelance-marketplace/wishket/crm/2026-03-25/raw.csv` |
| 키워드 | `output/freelance-marketplace/wanted-gigs/crm/2026-03-25/raw.csv` |
| 키워드 | `output/freelance-marketplace/freemoa/crm/2026-03-25/raw.csv` |
| 탐색 | `output/freelance-marketplace/wishket/any/2026-03-25/raw.csv` |
| 탐색 | `output/freelance-marketplace/wanted-gigs/any/2026-03-25/raw.csv` |
| 탐색 | `output/freelance-marketplace/freemoa/any/2026-03-25/raw.csv` |
| 크로스 플랫폼 | `output/freelance-marketplace/total/crm/2026-03-25/cross-platform-report.md` |

## 파일 종류
- `raw.csv` — 크롤링 원본 데이터
- `analyzed.csv` — 분석 결과
- `report.md` — 플랫폼별 리포트
- `cross-platform-report.md` — 크로스 플랫폼 리포트 (`output/freelance-marketplace/total/{topic}/{date}/`에 저장)
