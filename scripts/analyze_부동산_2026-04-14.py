#!/usr/bin/env python3
"""부동산 키워드 분석 스크립트 - 2026-04-14"""

import csv
import os

BASE = "/home/user/researcher-korea/output/freelance-marketplace"
DATE = "2026-04-14"
KEYWORD = "부동산"

# ── 클러스터 정의 ─────────────────────────────────────────────────
CLUSTERS = {
    "C1": "데이터 수집/크롤링",
    "C2": "매물 추천·분석 플랫폼",
    "C3": "중개 플랫폼·서비스",
    "C4": "경매·입찰 서비스",
    "C5": "자동화·마케팅 도구",
    "C6": "정보·홍보 페이지",
    "C7": "현장(임장) 관리 도구",
}

# ── 위시켓 데이터 수동 분석 결과 ─────────────────────────────────
wishket_analyzed = [
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/6824/",
        "pain_target": "부동산 중개업체 / 스타트업",
        "pain_detail": "여러 부동산 플랫폼(네이버, 부동산114 등)에 분산된 매물 정보를 일일이 수작업으로 수집해야 함",
        "desired_solution": "다수 플랫폼 매물 크롤링 후 DB 자동 저장 백엔드",
        "alternatives_mentioned": "네이버 부동산;부동산114;다음 부동산",
        "cluster_id": "C1",
        "cluster_name": "데이터 수집/크롤링",
        "opportunity_score": 55,
        "key_quote": "네이버 부동산, 부동산114, 다음 부동산 등 주요 부동산 플랫폼에서 매물 정보를 크롤링하여 데이터베이스에 저장",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/91924/",
        "pain_target": "부동산 투자자 / 중개사",
        "pain_detail": "KB 부동산 시세 정보를 수동으로 조회하고 관리하는 비효율",
        "desired_solution": "KB 부동산 시세 크롤링 + 관리 페이지",
        "alternatives_mentioned": "KB부동산",
        "cluster_id": "C1",
        "cluster_name": "데이터 수집/크롤링",
        "opportunity_score": 55,
        "key_quote": "KB 부동산 시세 정보를 크롤링하여 수집하고 관리할 수 있는 관리 페이지 개발",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/150806/",
        "pain_target": "부동산 플랫폼 운영사 / 스타트업",
        "pain_detail": "사용자가 방대한 매물 중에서 자신에게 맞는 물건을 찾기 어렵고, 비교 분석 리포트 생성이 수동으로 이루어짐",
        "desired_solution": "AI 기반 매물 추천 + 자동 분석 리포트 생성 플랫폼",
        "alternatives_mentioned": "",
        "cluster_id": "C2",
        "cluster_name": "매물 추천·분석 플랫폼",
        "opportunity_score": 78,
        "key_quote": "AI 기반 부동산 매물 추천 및 비교 분석 리포트 생성 플랫폼 구축. 예산 6,000만원, 기간 150일.",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/100956/",
        "pain_target": "부동산 서비스 개발사",
        "pain_detail": "공적장부(토지대장, 건축물대장 등) 데이터를 수동으로 조회하는 불편함",
        "desired_solution": "부동산 공적장부 공공 API 연동 개발",
        "alternatives_mentioned": "",
        "cluster_id": "C2",
        "cluster_name": "매물 추천·분석 플랫폼",
        "opportunity_score": 62,
        "key_quote": "부동산 관련 공공 API를 연동하여 데이터를 수집 및 활용",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/144819/",
        "pain_target": "부동산 투자자 / 일반 수요자",
        "pain_detail": "데이터 기반 부동산 추천 서비스가 부재하여 감에 의존한 투자 결정",
        "desired_solution": "데이터 분석 + 추천 플랫폼 앱",
        "alternatives_mentioned": "",
        "cluster_id": "C2",
        "cluster_name": "매물 추천·분석 플랫폼",
        "opportunity_score": 65,
        "key_quote": "데이터 기반 부동산 추천 서비스 구현",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/67986/",
        "pain_target": "부동산 중개 스타트업",
        "pain_detail": "웹·앱 통합 매물 중개 서비스 부재로 모바일 사용자 이탈",
        "desired_solution": "웹 + 하이브리드 앱 통합 중개 서비스",
        "alternatives_mentioned": "",
        "cluster_id": "C3",
        "cluster_name": "중개 플랫폼·서비스",
        "opportunity_score": 70,
        "key_quote": "부동산 매물 중개 서비스를 위한 웹 및 하이브리드 앱 제작. 예산 2,000만원, 기간 75일.",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/151568/",
        "pain_target": "발전소(태양광 등) 매도자·매수자",
        "pain_detail": "발전소 매매 전문 중개 플랫폼 부재로 당사자 간 직접 거래의 어려움",
        "desired_solution": "발전소 매매 중개 플랫폼 MVP",
        "alternatives_mentioned": "",
        "cluster_id": "C3",
        "cluster_name": "중개 플랫폼·서비스",
        "opportunity_score": 58,
        "key_quote": "태양광 발전소 등 매도자와 매수자를 연결하는 중개 플랫폼",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/121599/",
        "pain_target": "부동산 플랫폼 운영사",
        "pain_detail": "모바일 환경에 최적화되지 않은 기존 플랫폼으로 인한 UX 저하",
        "desired_solution": "반응형 웹 기반 부동산 플랫폼 구축",
        "alternatives_mentioned": "",
        "cluster_id": "C3",
        "cluster_name": "중개 플랫폼·서비스",
        "opportunity_score": 55,
        "key_quote": "다양한 디바이스에서 최적화된 부동산 플랫폼 웹 서비스 제공",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/104814/",
        "pain_target": "위치 기반 부동산 서비스 스타트업",
        "pain_detail": "GPS·지도 기반 O2O 부동산 연결 서비스 부재",
        "desired_solution": "GPS·Map 기반 부동산 O2O 플랫폼",
        "alternatives_mentioned": "",
        "cluster_id": "C3",
        "cluster_name": "중개 플랫폼·서비스",
        "opportunity_score": 63,
        "key_quote": "GPS 및 Map 기반의 부동산 O2O 플랫폼 구축 프로젝트. 위치 기반 부동산 서비스 연결 플랫폼 개발.",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/36827/",
        "pain_target": "부동산 경매 참여자 / 스타트업",
        "pain_detail": "경매 정보 분산·불투명성으로 실시간 입찰 참여의 어려움",
        "desired_solution": "실제 입찰 가능한 경매 앱 서비스",
        "alternatives_mentioned": "",
        "cluster_id": "C4",
        "cluster_name": "경매·입찰 서비스",
        "opportunity_score": 72,
        "key_quote": "실제 입찰이 가능한 부동산 경매 앱 서비스 구축. 예산 3,800만원, 기간 120일.",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/117687/",
        "pain_target": "경매 참여자 / 대출 필요 투자자",
        "pain_detail": "경매 참여와 대출 중개를 하나의 플랫폼에서 처리할 수 없어 절차가 복잡함",
        "desired_solution": "경매 + 대출 중개 통합 Android/iOS 앱",
        "alternatives_mentioned": "",
        "cluster_id": "C4",
        "cluster_name": "경매·입찰 서비스",
        "opportunity_score": 68,
        "key_quote": "부동산 경매 참여자들의 불편함을 해소하는 토탈 경매 솔루션 플랫폼",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/133703/",
        "pain_target": "부동산 중개업소 / 마케터",
        "pain_detail": "매물 홍보를 위한 블로그 포스팅을 수작업으로 반복 작성하는 비효율",
        "desired_solution": "매물 정보 기반 블로그 포스팅 자동 작성 프로그램",
        "alternatives_mentioned": "",
        "cluster_id": "C5",
        "cluster_name": "자동화·마케팅 도구",
        "opportunity_score": 48,
        "key_quote": "부동산 매물 정보를 기반으로 블로그 포스팅을 자동으로 작성해주는 프로그램 설계 및 개발",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/148145/",
        "pain_target": "부동산 법인",
        "pain_detail": "전문적인 법인 홈페이지 부재로 온라인 신뢰도 및 고객 유입 부족",
        "desired_solution": "종합 부동산 법인 공식 홈페이지 구축",
        "alternatives_mentioned": "",
        "cluster_id": "C6",
        "cluster_name": "정보·홍보 페이지",
        "opportunity_score": 35,
        "key_quote": "부동산 법인의 공식 홈페이지 제작 의뢰",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/139256/",
        "pain_target": "부동산 중개사무소",
        "pain_detail": "사무실 홍보 전용 랜딩페이지 부재로 온라인 마케팅 한계",
        "desired_solution": "사무실 소개용 랜딩페이지 구축",
        "alternatives_mentioned": "",
        "cluster_id": "C6",
        "cluster_name": "정보·홍보 페이지",
        "opportunity_score": 32,
        "key_quote": "부동산 중개 사무소 홍보용 랜딩페이지 제작",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/122094/",
        "pain_target": "부동산 투자자 / 중개사",
        "pain_detail": "임장 시 촬영한 사진·동영상 자료를 체계적으로 관리할 도구 부재",
        "desired_solution": "사진·동영상 정리 및 관리 임장 전용 모바일 앱",
        "alternatives_mentioned": "",
        "cluster_id": "C7",
        "cluster_name": "현장(임장) 관리 도구",
        "opportunity_score": 56,
        "key_quote": "부동산 임장 시 촬영한 사진/동영상을 정리하고 관리하는 모바일 앱 구축. 예산 2,000만원, 기간 60일.",
    },
]

COLUMNS = [
    "source_platform", "source_url", "pain_target", "pain_detail",
    "desired_solution", "alternatives_mentioned", "cluster_id",
    "cluster_name", "opportunity_score", "key_quote",
]


def save_analyzed(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[OK] analyzed.csv saved → {path} ({len(rows)} rows)")


def save_empty_analyzed(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
    print(f"[OK] analyzed.csv (empty) saved → {path}")


# ── 저장 ─────────────────────────────────────────────────────────
save_analyzed(
    f"{BASE}/wishket/{KEYWORD}/{DATE}/analyzed.csv",
    wishket_analyzed,
)
save_empty_analyzed(f"{BASE}/wanted-gigs/{KEYWORD}/{DATE}/analyzed.csv")
save_empty_analyzed(f"{BASE}/freemoa/{KEYWORD}/{DATE}/analyzed.csv")

print("Done.")
