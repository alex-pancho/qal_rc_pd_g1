from collections import defaultdict
import json
import os


# =========================================================
# Завдання 3: Клас FolkloreRecord
# =========================================================
class FolkloreRecord:

    def __init__(self, title: str, genre: str, region: str, narrator: str,
                 year: int, content: str, tags: list, verified: bool):
        self.title = title
        self.genre = genre
        self.region = region
        self.narrator = narrator
        self.year = year
        self.content = content
        self.tags = tags
        self.verified = verified

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "genre": self.genre,
            "region": self.region,
            "narrator": self.narrator,
            "year": self.year,
            "content": self.content,
            "tags": self.tags,
            "verified": self.verified
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data.get("title", ""),
            genre=data.get("genre", ""),
            region=data.get("region", ""),
            narrator=data.get("narrator", ""),
            year=data.get("year", 0),
            content=data.get("content", ""),
            tags=data.get("tags", []),
            verified=data.get("verified", False)
        )

    def __str__(self) -> str:
        return f'[{self.genre}] "{self.title}" — {self.region}, {self.year} (оповідач: {self.narrator})'


# =========================================================
# Завдання 4: Клас FieldExpedition
# =========================================================
class FieldExpedition:

    def __init__(self, expedition_id: str, researcher: str, location: str, date: str, records: list = None):
        self.expedition_id = expedition_id
        self.researcher = researcher
        self.location = location
        self.date = date
        self.records = records if records is not None else []

    def add_record(self, record: FolkloreRecord):
        for rec in self.records:
            if rec.title.lower() == record.title.lower():
                return f"Запис '{record.title}' вже є в експедиції"
        self.records.append(record)

    def remove_record(self, title: str):
        for rec in self.records:
            if rec.title.lower() == title.lower():
                self.records.remove(rec)
                return
        return f"Запис '{title}' не знайдено"

    def find_by_genre(self, genre: str) -> list:
        return [rec for rec in self.records if rec.genre.lower() == genre.lower()]

    def to_dict(self) -> dict:
        return {
            "expedition_id": self.expedition_id,
            "researcher": self.researcher,
            "location": self.location,
            "date": self.date,
            "records": [rec.to_dict() for rec in self.records]
        }

    @classmethod
    def from_dict(cls, data: dict):
        records = [FolkloreRecord.from_dict(rec) for rec in data.get("records", [])]
        return cls(
            expedition_id=data.get("expedition_id", ""),
            researcher=data.get("researcher", ""),
            location=data.get("location", ""),
            date=data.get("date", ""),
            records=records
        )

    def save(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return cls.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Помилка при завантаженні {filepath}: {e}")
            return None


# =========================================================
# Завдання 5: Центральний архів
# =========================================================
def merge_archives(filepaths: list) -> list:
    all_records = []
    for path in filepaths:
        try:
            expedition = FieldExpedition.load(path)
            if expedition:
                all_records.extend(expedition.records)
        except Exception as e:
            print(f"Попередження: Не вдалося обробити файл {path}. Причина: {e}")
    return all_records


def filter_records(records: list, genre: str = None, region: str = None, verified: bool = None) -> list:
    filtered = []
    for rec in records:
        if genre is not None and rec.genre.lower() != genre.lower():
            continue
        if region is not None and rec.region.lower() != region.lower():
            continue
        if verified is not None and rec.verified != verified:
            continue
        filtered.append(rec)
    return filtered


def export_summary(records: list, filepath: str):
    summary_data = [
        {
            "title": rec.title,
            "genre": rec.genre,
            "region": rec.region,
            "verified": rec.verified
        }
        for rec in records
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=4)


# =========================================================
# Бонус 🏆: Знаходження дублікатів
# =========================================================
def find_duplicates(filepaths: list) -> dict:
    title_to_regions = defaultdict(list)
    
    for path in filepaths:
        expedition = FieldExpedition.load(path)
        if expedition:
            for rec in expedition.records:
                title_to_regions[rec.title].append(rec.region)

    duplicates = {
        title: regions
        for title, regions in title_to_regions.items()
        if len(regions) > 1
    }
    return duplicates


# =========================================================
# Демонстрація виконання всіх завдань
# =========================================================
if __name__ == "__main__":
    print("=== Завдання 1: Серіалізація вручну ===")
    sample_dict = {
        "title": "Ой у лузі червона калина",
        "genre": "пісня",
        "region": "Полтавщина",
        "narrator": "Ганна Остапенко",
        "year": 1932,
        "content": "Ой у лузі червона калина похилилася...",
        "tags": ["козацька", "народна"],
        "verified": True
    }

    json_str = json.dumps(sample_dict)
    print("Простий JSON-рядок:", json_str)
    print("Тип:", type(json_str))

    json_str_formatted = json.dumps(sample_dict, indent=4, ensure_ascii=False)
    print("\nФорматований JSON-рядок:\n", json_str_formatted)

    restored_dict = json.loads(json_str_formatted)
    print("\nТип після loads:", type(restored_dict))
    print(f"Поля: Назва={restored_dict['title']}, Регіон={restored_dict['region']}")

    print("\n=== Завдання 2: Архів експедиції (файл) ===")
    archive_list = [
        sample_dict,
        {
            "title": "Про лисицю та журавля",
            "genre": "казка",
            "region": "Поділля",
            "narrator": "Іван Коваль",
            "year": 1954,
            "content": "Лисиця запросила журавля на обід...",
            "tags": ["казка про тварин"],
            "verified": True
        },
        {
            "title": "Легенда про Дніпро",
            "genre": "легенда",
            "region": "Київщина",
            "narrator": "Марія Шевчук",
            "year": 1961,
            "content": "Жив колись могутній богатир Дніпро...",
            "tags": ["міфологія"],
            "verified": False
        },
        {
            "title": "Сім п'ятниць на тиждень",
            "genre": "прислів'я",
            "region": "Слобожанщина",
            "narrator": "Василь Бойко",
            "year": 1978,
            "content": "Про непостійну людину...",
            "tags": ["прислів'я"],
            "verified": True
        },
        {
            "title": "Засвіт встали козаченьки",
            "genre": "пісня",
            "region": "Полтавщина",
            "narrator": "Олена Петренко",
            "year": 1928,
            "content": "Засвіт встали козаченьки в похід з полуночі...",
            "tags": ["Маруся Чурай"],
            "verified": True
        }
    ]

    with open("folklore_archive.json", "w", encoding="utf-8") as f:
        json.dump(archive_list, f, ensure_ascii=False, indent=4)

    with open("folklore_archive.json", "r", encoding="utf-8") as f:
        loaded_archive = json.load(f)

    for idx, item in enumerate(loaded_archive, 1):
        print(f'{idx}. "{item["title"]}" ({item["genre"]}, {item["region"]})')

    print("\n=== Завдання 3: Клас FolkloreRecord ===")
    r1 = FolkloreRecord.from_dict(archive_list[0])
    r2 = FolkloreRecord.from_dict(archive_list[1])
    r3 = FolkloreRecord.from_dict(archive_list[2])

    records_to_save = [r1.to_dict(), r2.to_dict(), r3.to_dict()]
    with open("records.json", "w", encoding="utf-8") as f:
        json.dump(records_to_save, f, ensure_ascii=False, indent=4)

    with open("records.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        restored_records = [FolkloreRecord.from_dict(d) for d in data]

    for rec in restored_records:
        print(rec)

    print("\n=== Завдання 4: Клас FieldExpedition ===")
    exp1 = FieldExpedition("EXP-01", "Дмитро Яворницький", "Запоріжжя", "1905-05-12")
    exp1.add_record(r1)
    exp1.add_record(r2)
    exp1.add_record(r3)
    exp1.add_record(FolkloreRecord.from_dict(archive_list[4]))

    exp1.save("expedition_1.json")

    loaded_exp1 = FieldExpedition.load("expedition_1.json")
    print("Завантажена експедиція:", loaded_exp1.expedition_id, loaded_exp1.researcher)

    songs = loaded_exp1.find_by_genre("пісня")
    print("Знайдені пісні:")
    for song in songs:
        print("  -", song)

    loaded_exp1.remove_record("Легенда про Дніпро")
    loaded_exp1.save("expedition_1.json")

    print("\n=== Завдання 5 та Бонус ===")
    exp2 = FieldExpedition("EXP-02", "Филарет Колесса", "Харків", "1912-08-20")
    exp2.add_record(FolkloreRecord("Ой у лузі червона калина", "пісня", "Харківщина", "Панас", 1912, "...", ["пісня"], True))
    exp2.save("expedition_2.json")

    all_found = merge_archives(["expedition_1.json", "expedition_2.json"])
    print(f"Усього об'єднано записів: {len(all_found)}")

    filtered = filter_records(all_found, genre="пісня", verified=True)
    print(f"Знайдено перевірених пісень: {len(filtered)}")

    export_summary(filtered, "summary.json")
    print("Зведення експортовано у 'summary.json'")

    duplicates = find_duplicates(["expedition_1.json", "expedition_2.json"])
    print("Знайдені дублікати (варіанти в інших регіонах):", duplicates)