import csv
import os

output_path = "/home/user/researcher-korea/output/freelance-marketplace/wanted-gigs/물류/2026-04-12/raw.csv"
fieldnames = [
    "url", "title", "budget_min", "budget_max", "currency",
    "category", "skills", "region", "duration", "applicants",
    "date", "pain_signals", "content"
]

rows = []
# No projects were found via WebSearch for keyword "물류" on wanted.co.kr/gigs/projects.
# The platform is SPA-based and project pages are not indexed by search engines.

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV saved: {output_path} ({len(rows)} rows)")
