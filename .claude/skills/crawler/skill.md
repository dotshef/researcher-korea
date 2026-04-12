# /crawler - Web Crawling

국내 IT 외주 플랫폼에서 데이터를 수집하여 raw.csv로 저장한다.
각 플랫폼별 서브에이전트는 `.claude/agents/{platform}.md`에 정의되어 있다.

> 출력 경로는 `.claude/rules/output-path.md`를 따른다.

**중요: 사용자 입력이 필요한 단계에서는 반드시 AskUserQuestion 도구를 사용하라. 텍스트로 질문을 출력하지 마라.**

## 크롤링 프로세스

### Step 1: 모드 선택

AskUserQuestion 도구로 질문한다:
- question: "모드를 선택하세요"
- options:
  - 키워드 모드 — "특정 키워드로 타겟 검색 (예: 쇼핑몰, CRM, 앱)"
  - 탐색 모드 — "키워드 없이 최신 프로젝트를 전체 탐색"

키워드 모드 선택 시, AskUserQuestion으로 "검색 키워드를 입력하세요"를 질문한다.

### Step 2: 서브에이전트 병렬 생성
모든 입력을 수집한 후, 3개 플랫폼에 대해 `.claude/agents/{platform}.md`를 읽어 서브에이전트를 병렬 생성한다.
- 각 에이전트에 모드, 키워드, 날짜를 전달한다.

### Step 3: 수집 결과 확인
모든 서브에이전트 완료 후, 각 플랫폼별 수집 건수를 보고한다.

## 출력
- 파일: 각 플랫폼 디렉토리에 `raw.csv`로 저장
- 플랫폼당 최대 20건 수집

## 플랫폼별 서브에이전트
- `.claude/agents/wishket.md` — 위시켓 (WebSearch)
- `.claude/agents/wanted-gigs.md` — 원티드긱스 (WebSearch)
- `.claude/agents/freemoa.md` — 프리모아 (Python 크롤러)

새 플랫폼 추가 시 `.claude/agents/`에 `{platform}.md` 파일을 추가하면 된다.
