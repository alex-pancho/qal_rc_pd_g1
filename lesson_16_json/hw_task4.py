import json


class FolkloreRecord:
    def __init__(
        self,
        title,
        genre,
        region,
        narrator,
        year,
        content,
        tags,
        verified,
    ):
        self.title = title
        self.genre = genre
        self.region = region
        self.narrator = narrator
        self.year = year
        self.content = content
        self.tags = tags
        self.verified = verified

    def to_dict(self):
        return {
            "title": self.title,
            "genre": self.genre,
            "region": self.region,
            "narrator": self.narrator,
            "year": self.year,
            "content": self.content,
            "tags": self.tags,
            "verified": self.verified,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return (
            f'[{self.genre}] "{self.title}" '
            f'- {self.region}, {self.year}'
        )


class FieldExpedition:
    def __init__(
        self,
        expedition_id,
        researcher,
        location,
        date,
    ):
        self.expedition_id = expedition_id
        self.researcher = researcher
        self.location = location
        self.date = date
        self.records = []

    def add_record(self, record):
        for existing in self.records:
            if existing.title == record.title:
                return (
                    f"Запис '{record.title}' "
                    f"вже є в експедиції"
                )

        self.records.append(record)

    def remove_record(self, title):
        for record in self.records:
            if record.title == title:
                self.records.remove(record)
                return

        return f"Запис '{title}' не знайдено"

    def find_by_genre(self, genre):
        result = []

        for record in self.records:
            if record.genre == genre:
                result.append(record)

        return result

    def to_dict(self):
        return {
            "expedition_id": self.expedition_id,
            "researcher": self.researcher,
            "location": self.location,
            "date": self.date,
            "records": [
                record.to_dict()
                for record in self.records
            ],
        }

    @classmethod
    def from_dict(cls, data):
        expedition = cls(
            data["expedition_id"],
            data["researcher"],
            data["location"],
            data["date"],
        )

        expedition.records = [
            FolkloreRecord.from_dict(record)
            for record in data["records"]
        ]

        return expedition

    def save(self, filepath):
        with open(
            filepath,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.to_dict(),
                file,
                indent=4,
                ensure_ascii=False,
            )

    @classmethod
    def load(cls, filepath):
        try:
            with open(
                filepath,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            return cls.from_dict(data)

        except FileNotFoundError:
            print("Файл не знайдено.")
            return None

        except json.JSONDecodeError:
            print("Файл пошкоджено.")
            return None


expedition = FieldExpedition(
    1,
    "Олена Никітенко",
    "Тернопільщина",
    "2026-10-28",
)

expedition.add_record(
    FolkloreRecord(
        "Ой у лузі червона калина",
        "пісня",
        "Полтавщина",
        "Ганна Остапенко",
        1932,
        "Українська народна пісня",
        ["народна", "історична"],
        True,
    )
)

expedition.add_record(
    FolkloreRecord(
        "Про лисицю та журавля",
        "казка",
        "Поділля",
        "Марія Коваль",
        1950,
        "Народна казка",
        ["казка"],
        True,
    )
)

expedition.add_record(
    FolkloreRecord(
        "Легенда про Довбуша",
        "легенда",
        "Гуцульщина",
        "Іван Мельник",
        1948,
        "Легенда про народного героя",
        ["легенда", "герой"],
        False,
    )
)

expedition.add_record(
    FolkloreRecord(
        "Без труда нема плода",
        "прислів'я",
        "Волинь",
        "Петро Савчук",
        1965,
        "Народна мудрість",
        ["прислів'я"],
        True,
    )
)

expedition.save("expedition_1.json")

loaded = FieldExpedition.load("expedition_1.json")

print("\nПісні:")

for record in loaded.find_by_genre("пісня"):
    print(record)

print("\nВидаляємо запис...")

loaded.remove_record("Без труда нема плода")

loaded.save("expedition_1.json")

print("Файл оновлено.")
