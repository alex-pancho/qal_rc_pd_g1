import csv
from pathlib import Path

fieldnames = ["name", "age", "city"]
rows = [
    {"name": "Олена", "age": 25, "city": "Київ, Хрещатик 26; івіві, \" от така біда, малята\""},
    {"name": "Максим", "age": 30, "city": "Харків"},
]

prj_folder = Path(__file__).parents[1]
filepath = prj_folder / "lesson_17_csv" / "output.csv"

with open(
        filepath,
        "w", 
        newline="",
        encoding="utf-8"
    ) as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

csv.register_dialect(
    "semicolon",
    delimiter=";",
    quotechar='"',
    quoting=csv.QUOTE_MINIMAL,
)

with open(
        filepath,
        "w", 
        newline="",
        encoding="utf-8"
    ) as file:
    writer = csv.writer(file, dialect="semicolon")
    writer.writerows([fieldnames, rows[0].values()])
