import json


folklore_records = [
    {
        "title": "Ой у лузі червона калина",
        "genre": "пісня",
        "region": "Полтавщина",
        "narrator": "Ганна Остапенко",
        "year": 1932,
        "content": "Українська народна пісня",
        "tags": ["народна", "історична"],
        "verified": True,
    },
    {
        "title": "Про лисицю та журавля",
        "genre": "казка",
        "region": "Поділля",
        "narrator": "Марія Коваль",
        "year": 1950,
        "content": "Народна казка про хитрість.",
        "tags": ["казка", "тварини"],
        "verified": True,
    },
    {
        "title": "Легенда про Довбуша",
        "genre": "легенда",
        "region": "Гуцульщина",
        "narrator": "Іван Мельник",
        "year": 1948,
        "content": "Історія про Олексу Довбуша.",
        "tags": ["легенда", "герой"],
        "verified": False,
    },
    {
        "title": "Без труда нема плода",
        "genre": "прислів'я",
        "region": "Волинь",
        "narrator": "Петро Савчук",
        "year": 1965,
        "content": "Народна мудрість.",
        "tags": ["прислів'я"],
        "verified": True,
    },
    {
        "title": "Козацька дума",
        "genre": "пісня",
        "region": "Запоріжжя",
        "narrator": "Степан Бойко",
        "year": 1938,
        "content": "Козацька народна дума.",
        "tags": ["пісня", "козаки"],
        "verified": True,
    },
]

# Зберігаємо у файл
with open(
    "folklore_archive.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        folklore_records,
        file,
        indent=4,
        ensure_ascii=False,
    )

print("Архів збережено.")

# Читаємо назад
with open(
    "folklore_archive.json",
    "r",
    encoding="utf-8"
) as file:
    loaded_records = json.load(file)

print(f"Кількість записів: {len(loaded_records)}")

print("\nСписок записів:")

for index, record in enumerate(loaded_records, start=1):
    print(
        f'{index}. "{record["title"]}" '
        f'({record["genre"]}, {record["region"]})'
    )