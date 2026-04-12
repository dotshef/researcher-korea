# /analyzer - Clustering & Scoring

플랫폼별 raw.csv를 읽어 Pain Point를 클러스터링하고 기회 점수를 매겨 통일된 analyzed.csv를 생성한다.

> 출력 경로는 `.claude/rules/output-path.md`를 따른다.

## 입력
사용자가 경로를 지정하면 해당 경로를 사용한다.
지정하지 않으면 가장 최근 날짜의 output 디렉토리에서 모든 플랫폼을 분석한다.

사용 예:
- `/analyzer` → 최신 날짜의 전체 플랫폼 분석
- `/analyzer output/freelance-marketplace/wishket/crm/2026-03-25/` → 특정 플랫폼의 특정 주제만 분석

## 분석 프로세스

### Step 1: raw.csv 로드
지정된 디렉토리에서 `raw.csv`를 찾는다.
경로가 지정되지 않으면 최신 날짜 디렉토리에서 모든 `raw.csv`를 재귀적으로 탐색한다.
각 플랫폼의 컬럼 구조가 다를 수 있으므로, 컬럼명을 확인하고 내용을 해석한다.

### Step 2: Pain Point 추출
각 행의 **content 필드에 명시적으로 적힌 내용만** 기반으로 다음을 식별한다:
- **요구사항**: 어떤 시스템/서비스를 원하는가
- **구체적 문제**: 무엇을 해결하려 하는가
- **원하는 해결책**: 어떤 결과물을 기대하는가
- **기존 대안**: 이미 사용 중이거나 언급된 기존 도구/서비스

**할루시네이션 방지 규칙:**
- raw.csv의 content에 **명시적으로 적혀있지 않은 내용은 추론하지 않는다**.
- content에서 직접 추출할 수 없는 필드는 `[추정] ...` 접두어를 붙인다.
- content가 스니펫 기반(짧은 텍스트)이면 정보가 부족한 것이므로, 추출 가능한 필드만 채우고 나머지는 빈 값으로 둔다.

### Step 3: 클러스터링
유사한 요구사항을 그룹으로 묶어 각 행에 cluster_id와 cluster_name을 부여한다.

### Step 4: 스코어링
각 클러스터에 기회 점수를 매긴다 (0-100):
- **빈도** (40%): 해당 클러스터의 행 수 / 전체 행 수
- **예산 규모** (30%): 클러스터 내 평균 예산
- **구체성** (30%): 요구사항의 구체성 및 상세도

## 출력
파일: `raw.csv`와 같은 디렉토리에 `analyzed.csv`로 저장한다.

raw.csv의 컬럼은 유지하지 않는다. 분석 결과를 통일된 포맷으로 재구성한다:

CSV 컬럼:
source_platform,source_url,pain_target,pain_detail,desired_solution,alternatives_mentioned,cluster_id,cluster_name,opportunity_score,key_quote

- source_platform: 출처 플랫폼 (wishket, wanted-gigs, freemoa)
- source_url: 원본 URL
- pain_target: 요구 대상 시스템/서비스명 (content에서 직접 추출. 없으면 빈 값)
- pain_detail: 구체적 문제/요구사항 요약 (content에 명시된 내용만. 추론 시 `[추정]` 접두어)
- desired_solution: 원하는 해결책 요약 (content에 명시된 내용만. 추론 시 `[추정]` 접두어)
- alternatives_mentioned: 언급된 기존 도구/서비스 (content/skills에서 직접 추출. 세미콜론 구분)
- cluster_id: 클러스터 번호 (1, 2, 3, ...)
- cluster_name: 클러스터 라벨 (예: "커머스 플랫폼 구축")
- opportunity_score: 해당 클러스터의 기회 점수 (0-100)
- key_quote: content에서 직접 발췌한 원문 (가공하지 않은 원문 그대로)
