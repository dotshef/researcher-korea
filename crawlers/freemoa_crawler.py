"""
프리모아(Freemoa) Crawler - JSON API를 사용한 IT 외주 프로젝트 데이터 수집기

사용법:
  # 키워드 모드
  python crawlers/freemoa_crawler.py --mode keyword --keyword "쇼핑몰"

  # 탐색 모드
  python crawlers/freemoa_crawler.py --mode explore

  # 출력 디렉토리 변경
  python crawlers/freemoa_crawler.py --mode keyword --keyword "앱" --output output/freelance-marketplace/freemoa/앱/2026-03-25
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib3
from datetime import datetime

import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MAX_PROJECTS = 20
MIN_BUDGET = 100  # 만원
BASE_URL = "https://www.freemoa.net"
LIST_API = f"{BASE_URL}/m4a/s41a"
PAGE_URL = f"{BASE_URL}/m4/s41"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": PAGE_URL,
}

PAIN_KEYWORDS = {
    "자동화": ["자동화", "자동", "배치", "스케줄", "반복"],
    "연동": ["연동", "api", "연결", "동기화", "webhook"],
    "마이그레이션": ["마이그레이션", "이관", "전환", "이전", "데이터 이전"],
    "커스텀": ["맞춤", "커스텀", "맞춤형", "커스터마이징", "custom"],
    "플랫폼": ["플랫폼", "마켓플레이스", "중개", "매칭"],
    "AI": ["ai", "인공지능", "머신러닝", "딥러닝", "챗봇", "gpt"],
    "커머스": ["쇼핑몰", "이커머스", "커머스", "결제", "주문"],
    "관리시스템": ["erp", "crm", "관리 시스템", "대시보드", "관리자", "백오피스"],
    "앱개발": ["앱", "모바일", "ios", "android", "하이브리드", "react native", "flutter"],
    "리뉴얼": ["리뉴얼", "리디자인", "개편", "고도화", "업그레이드"],
}

CSV_COLUMNS = [
    "url", "title", "budget_min", "budget_max", "currency",
    "category", "skills", "region", "duration", "applicants",
    "date", "pain_signals", "content",
]


def detect_pain_signals(text: str) -> list[str]:
    text_lower = text.lower()
    signals = []
    for signal, keywords in PAIN_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            signals.append(signal)
    return signals


def get_session() -> requests.Session:
    session = requests.Session()
    session.verify = False
    session.headers.update(HEADERS)
    resp = session.get(PAGE_URL, timeout=15)
    resp.raise_for_status()
    return session


def fetch_projects(session: requests.Session, page: int = 1) -> dict:
    data = {"page": page, "sm": 1}
    resp = session.post(LIST_API, data=data, timeout=15)
    resp.raise_for_status()
    return resp.json()


def matches_keyword(project: dict, keyword: str) -> bool:
    keyword_lower = keyword.lower()
    searchable = " ".join([
        project.get("title", ""),
        project.get("txt", ""),
        project.get("proj_language", ""),
        project.get("fld_nm_2nd", ""),
    ]).lower()
    return keyword_lower in searchable


def filter_project(project: dict) -> bool:
    if project.get("isNowApply") != "1":
        return False
    cost_max = int(project.get("cost_max", 0) or 0)
    if cost_max < MIN_BUDGET:
        return False
    return True


def project_to_row(project: dict) -> dict:
    proj_idx = project.get("proj_idx", "")
    title = project.get("title", "")
    cost_min = project.get("cost_min", "0")
    cost_max = project.get("cost_max", "0")
    category = project.get("fld_nm_2nd", "")
    skills = project.get("proj_language", "").replace(",", ";").strip()
    region = project.get("pv_smallnm", "")
    duration = project.get("during", "")
    applicants = project.get("ALL_APPLY_COUNT", "0")
    ins_time = project.get("INS_TIME", "")
    date_str = ins_time[:10] if ins_time else ""

    txt = project.get("txt", "")
    content = txt[:2000].replace("\r\n", " ").replace("\n", " ").strip()

    full_text = f"{title}. {txt}"
    signals = detect_pain_signals(full_text)

    url = f"https://www.freemoa.net/m4/s41?pno={proj_idx}"

    return {
        "url": url,
        "title": title,
        "budget_min": cost_min,
        "budget_max": cost_max,
        "currency": "KRW",
        "category": category,
        "skills": skills,
        "region": region,
        "duration": duration,
        "applicants": applicants,
        "date": date_str,
        "pain_signals": ";".join(signals) if signals else "general",
        "content": content,
    }


def crawl(mode: str, keyword: str | None, max_projects: int) -> list[dict]:
    print("세션 획득 중...")
    session = get_session()

    results: list[dict] = []
    page = 1
    max_pages = 10

    while len(results) < max_projects and page <= max_pages:
        print(f"\n페이지 {page} 수집 중...")
        try:
            response = fetch_projects(session, page)
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"  [WARN] 페이지 {page} 실패: {e}", file=sys.stderr)
            break

        project_list = response.get("DATA", {}).get("PROJECT", {}).get("LIST", [])
        if not project_list:
            print("  → 더 이상 프로젝트 없음")
            break

        valid = [p for p in project_list if filter_project(p)]
        print(f"  → {len(project_list)}건 로드, {len(valid)}건 필터 통과")

        for project in valid:
            if len(results) >= max_projects:
                break

            if mode == "keyword" and keyword:
                if not matches_keyword(project, keyword):
                    continue

            row = project_to_row(project)
            results.append(row)

        page += 1
        time.sleep(1.0)

    results.sort(key=lambda x: int(x["applicants"] or 0), reverse=True)
    return results[:max_projects]


def save_csv(rows: list[dict], output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n저장 완료: {output_path} ({len(rows)}건)")


def main():
    parser = argparse.ArgumentParser(description="프리모아 IT 외주 프로젝트 크롤러")
    parser.add_argument("--mode", choices=["keyword", "explore"], required=True,
                        help="keyword: 키워드 검색, explore: 전체 탐색")
    parser.add_argument("--keyword", type=str, help="검색 키워드 (keyword 모드 필수)")
    parser.add_argument("--max", type=int, default=MAX_PROJECTS,
                        help=f"최대 수집 건수 (기본: {MAX_PROJECTS})")
    parser.add_argument("--output", type=str, help="출력 디렉토리")

    args = parser.parse_args()

    if args.mode == "keyword" and not args.keyword:
        parser.error("keyword 모드에서는 --keyword가 필수입니다")

    today = datetime.now().strftime("%Y-%m-%d")
    topic = args.keyword if args.keyword else "any"
    output_dir = args.output or f"output/freelance-marketplace/freemoa/{topic}/{today}"
    output_path = os.path.join(output_dir, "raw.csv")

    print("=" * 50)
    print("프리모아(Freemoa) Crawler")
    print(f"모드: {'keyword (키워드 검색)' if args.mode == 'keyword' else 'explore (전체 탐색)'}")
    if args.mode == "keyword":
        print(f"키워드: {args.keyword}")
    print(f"최대 수집: {args.max}건")
    print(f"출력: {output_path}")
    print("=" * 50)

    rows = crawl(mode=args.mode, keyword=args.keyword, max_projects=args.max)

    if not rows:
        print("\n수집된 데이터가 없습니다.", file=sys.stderr)
        sys.exit(1)

    save_csv(rows, output_path)

    print("\n--- 수집 요약 ---")
    all_signals = {}
    for r in rows:
        for sig in r["pain_signals"].split(";"):
            if sig:
                all_signals[sig] = all_signals.get(sig, 0) + 1
    print("\n주요 Pain Signals:")
    for sig, c in sorted(all_signals.items(), key=lambda x: -x[1])[:10]:
        print(f"  {sig}: {c}건")

    budgets = [int(r["budget_max"]) for r in rows if r["budget_max"] and int(r["budget_max"]) > 0]
    if budgets:
        avg = sum(budgets) / len(budgets)
        print(f"\n평균 최대 예산: {avg:.0f}만원")
    print(f"총 지원자 수: {sum(int(r['applicants'] or 0) for r in rows)}명")


if __name__ == "__main__":
    main()
