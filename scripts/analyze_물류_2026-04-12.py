"""
물류 키워드 분석 스크립트 (2026-04-12)
wishket raw.csv → analyzed.csv 생성
"""
import csv
import os

FIELDNAMES = [
    "source_platform", "source_url", "pain_target", "pain_detail",
    "desired_solution", "alternatives_mentioned", "cluster_id",
    "cluster_name", "opportunity_score", "key_quote"
]

# ── 클러스터 정의 ──────────────────────────────────────────────
# 빈도 40% + 예산규모 30% + 구체성 30% 기준
# C1: 물류 자동화 & ERP 연동   (4건, SAP/CJ API 등 고구체성, 고예산) → 82
# C2: 택배/배송 매칭 앱        (5건, Android/iOS/Flutter, 중예산)   → 78
# C3: 물류 통합 관리 시스템    (3건, WMS/POS/구글시트, 중예산)       → 63
# C4: 해외/크로스보더 물류     (1건, 아마존 API, 해외시장, 고구체성)  → 60
# C5: 기업 홈페이지 구축       (1건, 단순홈페이지, 저예산)           → 26

WISHKET_ROWS = [
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/138918/",
        "pain_target": "물류/영업 통합 운영 담당자",
        "pain_detail": "물류센터·구매팀·영업팀 간 데이터 분산으로 동일 시트 접근 불가, 정보 공유 비효율",
        "desired_solution": "구글 스프레드시트 기반 통합 관리 시스템 구축",
        "alternatives_mentioned": "Google Sheets;Google Apps Script",
        "cluster_id": "C3",
        "cluster_name": "물류 통합 관리 시스템",
        "opportunity_score": 63,
        "key_quote": "물류센터, 구매팀, 영업팀이 동일한 시트에서 필요한 정보를 접근할 수 있도록 구성",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/10693/",
        "pain_target": "물류 서비스 이용자 (발송인/수취인)",
        "pain_detail": "물류 서비스의 모바일 채널 부재 — Android/iOS 앱으로 접근 불가",
        "desired_solution": "물류 서비스 Android·iOS 앱 구축",
        "alternatives_mentioned": "",
        "cluster_id": "C2",
        "cluster_name": "택배/배송 매칭 앱",
        "opportunity_score": 78,
        "key_quote": "물류 서비스를 위한 안드로이드 및 iOS 앱 서비스 구축 프로젝트",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/134192/",
        "pain_target": "택배 의뢰인 및 물류 부자재 구매자",
        "pain_detail": "택배 매칭과 물류 부자재 구매를 한 앱에서 처리하는 디지털 채널 부재",
        "desired_solution": "택배 매칭 + 물류 부자재 구매 통합 Android/iOS 앱 (디자인+개발)",
        "alternatives_mentioned": "Android;iOS",
        "cluster_id": "C2",
        "cluster_name": "택배/배송 매칭 앱",
        "opportunity_score": 78,
        "key_quote": "택배(물류) 매칭 및 물류 부자재 구매를 위한 Android, iOS 앱 디자인 및 개발 프로젝트",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/128097/",
        "pain_target": "택배 의뢰인 및 물류 부자재 구매자",
        "pain_detail": "택배 매칭·부자재 구매 통합 앱 구축 필요 (디자인 후속 개발 단계)",
        "desired_solution": "택배 매칭 + 물류 부자재 구매 통합 Android/iOS 앱 구축",
        "alternatives_mentioned": "Android;iOS",
        "cluster_id": "C2",
        "cluster_name": "택배/배송 매칭 앱",
        "opportunity_score": 78,
        "key_quote": "택배(물류) 매칭 및 물류 부자재 구매를 위한 Android, iOS 앱 구축 프로젝트",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/142417/",
        "pain_target": "공장 물류 자동화 시스템 운영팀",
        "pain_detail": "AMR/AGF(자율주행 로봇/무인지게차) 위치관제 대시보드 UI 노후화 — 현장 가시성 저하",
        "desired_solution": "AMR/AGF 위치관제 대시보드 UI 개선",
        "alternatives_mentioned": "AMR;AGF;Dashboard",
        "cluster_id": "C1",
        "cluster_name": "물류 자동화 & ERP 연동",
        "opportunity_score": 82,
        "key_quote": "AMR/AGF(자율주행 물류로봇/무인지게차)를 사용하여 구축된 시스템의 위치관제 대시보드 UI 개선 프로젝트",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/130140/",
        "pain_target": "미국 아마존 셀러 (한국 발송)",
        "pain_detail": "한국→해외 배송 물류 대행 서비스 부재, 아마존 시스템 연동 미비",
        "desired_solution": "물류 대행 시스템 개발 + 아마존 API 연동",
        "alternatives_mentioned": "Amazon API",
        "cluster_id": "C4",
        "cluster_name": "해외/크로스보더 물류",
        "opportunity_score": 60,
        "key_quote": "미국 아마존 셀러들이 한국에서 해외 배송할 때 사용하는 물류 대행 시스템 개발 및 아마존 API 연동",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/119957/",
        "pain_target": "물류 플랫폼 운영사",
        "pain_detail": "배송정보 입력 가능한 웹/모바일 물류 플랫폼 부재, 상주 개발 인력 필요",
        "desired_solution": "배송정보 입력 물류 플랫폼 (웹+모바일) 구축",
        "alternatives_mentioned": "",
        "cluster_id": "C3",
        "cluster_name": "물류 통합 관리 시스템",
        "opportunity_score": 63,
        "key_quote": "배송 정보 입력이 가능한 물류 플랫폼 구축 프로젝트. 웹/모바일 지원 필요. 상주 개발자 필요.",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/123068/",
        "pain_target": "물류사·화주·컨테이너 화물 운전자",
        "pain_detail": "물류사-화주 매칭과 운전자 상하차 관리를 통합한 모바일 솔루션 부재",
        "desired_solution": "Flutter 기반 물류 운전자 및 상차 관리 앱 (매칭+상하차)",
        "alternatives_mentioned": "Flutter;Android;iOS",
        "cluster_id": "C2",
        "cluster_name": "택배/배송 매칭 앱",
        "opportunity_score": 78,
        "key_quote": "물류사와 화주를 연결하고 운전자가 화물 상하차를 관리하는 Flutter 기반 모바일 앱 개발",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/38379/",
        "pain_target": "몽골 유통·물류 기업",
        "pain_detail": "POS·창고관리(WMS)·물류 ERP 등 종합 물류 인프라 부재 (해외 현지)",
        "desired_solution": "POS + WMS + 물류 ERP 종합 시스템 구축",
        "alternatives_mentioned": "POS;ERP;WMS",
        "cluster_id": "C3",
        "cluster_name": "물류 통합 관리 시스템",
        "opportunity_score": 63,
        "key_quote": "몽골에서 사용될 POS 시스템, 창고관리(WMS), 물류 ERP 등 종합 물류 시스템 구축 프로젝트",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/152801/",
        "pain_target": "수출 물류 현장 담당자 (SAP ERP 사용 기업)",
        "pain_detail": "SAP ERP ↔ CJ대한통운 시스템 연동 미비로 수동 수출 검증 작업 반복",
        "desired_solution": "SAP ERP + CJ대한통운 연동 + 바코드 스캔 자동화 Windows 시스템",
        "alternatives_mentioned": "SAP ERP;CJ대한통운;바코드스캔",
        "cluster_id": "C1",
        "cluster_name": "물류 자동화 & ERP 연동",
        "opportunity_score": 82,
        "key_quote": "SAP ERP와 CJ 대한통운 시스템을 연동하고, 물류 현장 PC에 연결된 바코드 스캐너로 자동화된 수출 검증 처리를 구현",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/147499/",
        "pain_target": "택배 접수·물류 담당자",
        "pain_detail": "수동 택배 접수 및 운송장 출력 비효율, CJ대한통운 API 미연동으로 반복 수작업 발생",
        "desired_solution": "CJ대한통운 택배 접수 API 연동 + 바코드 스캔 자동화",
        "alternatives_mentioned": "CJ대한통운 API;바코드",
        "cluster_id": "C1",
        "cluster_name": "물류 자동화 & ERP 연동",
        "opportunity_score": 82,
        "key_quote": "CJ 대한통운 택배 접수 API 연동으로 택배 접수 및 운송장 출력 자동화. 기존 수동 작업을 바코드 스캔 연동으로 자동화",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/1116/",
        "pain_target": "화물 운송 사업자",
        "pain_detail": "화물 배차 관리 디지털 솔루션 부재 — 웹·앱 통합 플랫폼 필요",
        "desired_solution": "화물배차 관리 웹 + 앱 제작",
        "alternatives_mentioned": "",
        "cluster_id": "C2",
        "cluster_name": "택배/배송 매칭 앱",
        "opportunity_score": 78,
        "key_quote": "화물 배차 관리를 위한 웹과 앱 제작 프로젝트",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/152139/",
        "pain_target": "반도체·물류 기업 마케팅/HR 담당자",
        "pain_detail": "기업 공식 홈페이지 및 온라인 채용 시스템 부재",
        "desired_solution": "공식 홈페이지 + 채용 시스템 구축",
        "alternatives_mentioned": "",
        "cluster_id": "C5",
        "cluster_name": "기업 홈페이지 구축",
        "opportunity_score": 26,
        "key_quote": "반도체 및 물류 전문 기업의 공식 홈페이지 및 채용 시스템 구축 프로젝트",
    },
    {
        "source_platform": "wishket",
        "source_url": "https://www.wishket.com/project/64855/",
        "pain_target": "물류 관리 시스템 운영팀",
        "pain_detail": "기존 Spring 기반 물류 관리 시스템의 주문·배송·상품 관리 기능 미흡 — 고도화 필요",
        "desired_solution": "Spring 기반 물류 관리 시스템 고도화 (주문/배송/상품 관리 메뉴)",
        "alternatives_mentioned": "Spring;Java",
        "cluster_id": "C1",
        "cluster_name": "물류 자동화 & ERP 연동",
        "opportunity_score": 82,
        "key_quote": "Spring 기반 내부 물류 관리 앱 시스템의 고도화 기능 개발. 주문 관리, 배송 관리, 상품 관리 메뉴 포함",
    },
]


def write_analyzed_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows → {path}")


# 위시켓
write_analyzed_csv(
    "output/freelance-marketplace/wishket/물류/2026-04-12/analyzed.csv",
    WISHKET_ROWS,
)

# 원티드긱스 (0건)
write_analyzed_csv(
    "output/freelance-marketplace/wanted-gigs/물류/2026-04-12/analyzed.csv",
    [],
)

# 프리모아 (0건 - 네트워크 오류)
write_analyzed_csv(
    "output/freelance-marketplace/freemoa/물류/2026-04-12/analyzed.csv",
    [],
)

print("Done.")
