# /reporter - Report Generation

analyzed.csv를 기반으로 플랫폼별 report.md와 크로스 플랫폼 리포트를 생성한다.

> 출력 경로는 `.claude/rules/output-path.md`를 따른다.

## 입력
사용자가 경로를 지정하면 해당 경로를 사용한다.
지정하지 않으면 가장 최근 날짜의 output 디렉토리를 사용한다.

사용 예:
- `/reporter` → 최신 날짜 전체 리포트 생성
- `/reporter output/freelance-marketplace/wishket/crm/2026-03-25/` → 특정 경로 리포트 생성

## 프로세스

### Step 1: analyzed.csv 수집
지정된 날짜 디렉토리에서 모든 `analyzed.csv` 파일을 재귀적으로 탐색한다.

### Step 2: 플랫폼별 report.md 생성

출력 파일: `analyzed.csv`와 같은 디렉토리에 `report.md`로 저장한다.

```markdown
---
platform: {platform}
mode: {keyword 또는 explore}
keyword: {키워드, keyword 모드일 때}
date: {날짜}
total_items: {수집된 행 수}
total_clusters: {클러스터 수}
---

## Top Pain Points

| Rank | Pain Point | Score | Items |
|------|-----------|-------|-------|
| 1 | {cluster_name} | {opportunity_score} | {해당 클러스터 행 수}건 |
| 2 | {cluster_name} | {opportunity_score} | {해당 클러스터 행 수}건 |
| ... | ... | ... | ... |

## Pain Point Clusters (by opportunity score)

### 1. {cluster_name} (Score: {opportunity_score})
{2~3문장으로 이 클러스터가 왜 중요한지 해석. 어떤 패턴이 반복되는지, 왜 기존 도구로 해결이 안 되는지 설명한다.}
- 예산 범위: {analyzed.csv 데이터에서 추출 가능 시}
- 제품 기회: {이 클러스터에서 발견되는 제품화 가능성 1줄 요약}
- 대표 인용:
  > "{key_quote}" — {source_url}
- 언급된 기존 도구: {alternatives_mentioned 통합}
- 관련 소스:
  - [{title 또는 pain_target}]({source_url})
  - ...

### 2. {cluster_name} (Score: {opportunity_score})
...
```

### Step 3: 크로스 플랫폼 리포트 생성 (플랫폼이 2개 이상일 때)

여러 플랫폼의 analyzed.csv가 존재하면, `output/freelance-marketplace/total/{topic}/{date}/cross-platform-report.md`를 생성한다.

```markdown
---
platforms: {platform1}, {platform2}, {platform3}
mode: {keyword 또는 explore}
date: {날짜}
total_items: {전체 행 수}
total_clusters: {클러스터 수}
---

## Cross-Platform Summary
{1~2문장으로 전체 요약}

## Top Pain Points (Cross-Platform)

| Rank | Pain Point | Score | Items | Platforms |
|------|-----------|-------|-------|-----------|
| 1 | {cluster_name} | {opportunity_score} | {건수} | {플랫폼별 분포} |
| ... | ... | ... | ... | ... |

## Key Insights

### 1. {cluster_name} (Score: {opportunity_score})
{3~5문장으로 심층 분석. 3개 플랫폼에서 공통으로 발견되는 패턴, 예산 범위, 기술 스택 경향 등을 포함한다.}
- 예산 범위: {데이터에서 추출}
- 제품 기회: {구체적 제품 아이디어 제안}
- 관련 소스:
  - [{title}]({url}) — {platform}
  - ...

### 2. {cluster_name} (Score: {opportunity_score})
...

## Platform Comparison

| 특성 | 위시켓 | 원티드긱스 | 프리모아 |
|------|--------|-----------|---------|
| 주요 수요 | ... | ... | ... |
| 평균 예산 | ... | ... | ... |
| 프로젝트 유형 | ... | ... | ... |
| 기술 스택 | ... | ... | ... |

## Action Items
1. **즉시 검증 가능**: {가장 빠르게 검증할 수 있는 기회}
2. **높은 ROI**: {투자 대비 수익이 높은 기회}
3. **장기 성장**: {장기적 성장 잠재력이 높은 기회}
```

## 작성 원칙
- 건조한 통계 나열 금지. 각 클러스터마다 **왜 이것이 기회인지** 해석을 포함한다.
- 모든 클러스터에 **관련 소스 링크**를 빠짐없이 표시한다.
- 크로스 플랫폼 리포트에서는 플랫폼 간 **공통점과 차이점**을 분석한다.
