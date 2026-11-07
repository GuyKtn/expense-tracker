import csv
import random
from datetime import date, timedelta

random.seed(42)  # same data every run

RANGES = {
    "food": (3, 25),
    "transport": (2, 60),
    "leisure": (5, 50),
    "health": (10, 80),
    "shopping": (10, 120),
}

start = date(2026, 4, 1)
rows = []
for offset in range(200):
    day = start + timedelta(days=offset)
    for _ in range(random.randint(0, 3)):
        category = random.choice(list(RANGES))
        low, high = RANGES[category]
        rows.append([round(random.uniform(low, high), 2), category, "", day.isoformat()])

with open("sample_data/expenses_sample.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["amount", "category", "note", "day"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} expenses")