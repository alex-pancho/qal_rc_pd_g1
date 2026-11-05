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
        return cls(
            title=data["title"],
            genre=data["genre"],
            region=data["region"],
            narrator=data["narrator"],
            year=data["year"],
            content=data["content"],
            tags=data["tags"],
            verified=data["verified"],
        )

    def __str__(self):
        return (
            f'[{self.genre}] "{self.title}" — '
            f'{self.region}, {self.year} '
            f'(оповідач: {self.narrator})'
        )


records = [
    FolkloreRecord(
        "Ой у лузі червона калина",
        "пісня",
        "Полтавщина",
        "Ганна Остапенко",
        1932,
        "Українська народна пісня",
        ["народна", "історична"],
        True,
    ),
    FolkloreRecord(
        "Про лисицю та журавля",
        "казка",
        "Поділля",
        "Марія Коваль",
        1950,
        "Народна казка",
        ["казка"],
        True,
    ),
    FolkloreRecord(
        "Легенда про Довбуша",
        "легенда",
        "Гуцульщина",
        "Іван Мельник",
        1948,
        "Історія про Довбуша",
        ["легенда"],
        False,
    ),
]


with open(
    "records.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        [record.to_dict() for record in records],
        file,
        indent=4,
        ensure_ascii=False,
    )


with open(
    "records.json",
    "r",
    encoding="utf-8"
) as file:
    loaded_data = json.load(file)


loaded_records = [
    FolkloreRecord.from_dict(item)
    for item in loaded_data
]


print("Відновлені записи:\n")

for record in loaded_records:
    print(record)
