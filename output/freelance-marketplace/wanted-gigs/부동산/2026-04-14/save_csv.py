import csv
import os

output_path = "/home/user/researcher-korea/output/freelance-marketplace/wanted-gigs/부동산/2026-04-14/raw.csv"

fieldnames = [
    "url", "title", "budget_min", "budget_max", "currency",
    "category", "skills", "region", "duration", "applicants",
    "date", "pain_signals", "content"
]

# 검색 결과에서 추출된 프로젝트 데이터
# 원티드긱스는 SPA로 개별 프로젝트 페이지가 검색 엔진에 인덱싱되지 않아
# "부동산" 키워드 관련 개별 프로젝트 URL이 검색 결과에 나타나지 않았음
rows = []

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"저장 완료: {output_path}")
print(f"수집 건수: {len(rows)}")
