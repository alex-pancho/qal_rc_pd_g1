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
            f'- {self.region}'
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
        self.records.append(record)

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

        except FileNotFoundError:
            print(f"Попередження: {filepath} не знайдено")
            return None

        except json.JSONDecodeError:
            print(f"Попередження: {filepath} пошкоджений")
            return None


def merge_archives(filepaths):
    all_records = []

    for filepath in filepaths:
        expedition = FieldExpedition.load(filepath)

        if expedition is not None:
            all_records.extend(expedition.records)

    return all_records


def filter_records(
    records,
    genre=None,
    region=None,
    verified=None,
):
    result = []

    for record in records:

        if genre is not None:
            if record.genre != genre:
                continue

        if region is not None:
            if record.region != region:
                continue

        if verified is not None:
            if record.verified != verified:
                continue

        result.append(record)

    return result


def export_summary(records, filepath):

    summary = []

    for record in records:
        summary.append(
            {
                "title": record.title,
                "genre": record.genre,
                "region": record.region,
                "verified": record.verified,
            }
        )

    with open(
        filepath,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False,
        )


expedition1 = FieldExpedition(
    1,
    "Олена Никітенко",
    "Тернопільщина",
    "2026-10-28",
)

expedition1.add_record(
    FolkloreRecord(
        "Ой у лузі червона калина",
        "пісня",
        "Полтавщина",
        "Ганна Остапенко",
        1932,
        "Пісня",
        ["народна"],
        True,
    )
)

expedition1.add_record(
    FolkloreRecord(
        "Про лисицю та журавля",
        "казка",
        "Поділля",
        "Марія Коваль",
        1950,
        "Казка",
        ["тварини"],
        True,
    )
)

expedition1.save("expedition_1.json")


expedition2 = FieldExpedition(
    2,
    "Іван Петренко",
    "Львівщина",
    "2026-10-29",
)

expedition2.add_record(
    FolkloreRecord(
        "Легенда про Довбуша",
        "легенда",
        "Гуцульщина",
        "Іван Мельник",
        1948,
        "Легенда",
        ["герой"],
        False,
    )
)

expedition2.add_record(
    FolkloreRecord(
        "Козацька дума",
        "пісня",
        "Запоріжжя",
        "Степан Бойко",
        1938,
        "Дума",
        ["козаки"],
        True,
    )
)

expedition2.save("expedition_2.json")


all_records = merge_archives(
    [
        "expedition_1.json",
        "expedition_2.json",
    ]
)

print("\nУсі записи:")
print(len(all_records))


filtered = filter_records(
    all_records,
    genre="пісня",
    verified=True,
)

print("\nПеревірені пісні:")

for record in filtered:
    print(record)

export_summary(
    filtered,
    "summary.json"
)

print("\nФайл summary.json створено.")
