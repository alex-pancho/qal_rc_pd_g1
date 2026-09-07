import json
from pathlib import Path

researcher = {
    "name": "Вернадський",
    "age": 82,
    "fields": ["мінералогія", "геохімія", "біосфера"],
    "alive": False
}

print(researcher["name"])
print(researcher.get("city", "невідомо"))

researcher["city"] = "Київ"

print(researcher.get("city", "невідомо"))

print(researcher.items())
for key, value in researcher.items():
    print(f"{key}: {value}")

mineral = {
    "name": "Кварц",
    "properties": {
        "hardness": 7,
        "formula": "SiO₂"
    }
}
print("hardness", mineral["properties"]["hardness"])
print(mineral.get("properties", {}).get("hardness"))    # безпечно

minerals = ["Кварц", "Берил", "Топаз", "Діамант"]
print(minerals[2])
minerals.append("Смарагд")

records = [
    {"name": "Кварц", "hardness": 7},
    {"name": "Берил", "hardness": 8},
]

for record in records:
    if record["name"] == "Берил":
        print(record["hardness"])

data = []

# Перевірка на порожнечу
if not data:
    print("список порожній")
else:
    print("else")

# Перевірка типу
if isinstance(data, list):
    print("це список")

# Перевірка наявності ключа у словнику
record = {"name": "Кварц",  } # "hardness": 1
if "hardness" not in record:
    print("твердість не вказана")

"""
# JSON                        # Python
true                           True
false                          False
null                           None
"рядки лише в подвійних"      'можна одинарні'
 У JSON немає:
 - коментарів
 - кортежів
 - множин
 - об'єктів із ключами-числами (лише рядки)
"""


task = {
    "title": "Fix login bug",
    "status": True,
    "priority": 'high',
    "tags": ["backend", "auth"],
    1: "lets go"
}
json_string = json.dumps(task, indent=2)
print(json_string)

task = {"title": "Виправити баг входу"}

# Без параметра — кирилиця екранується
print(json.dumps(task, ensure_ascii=False))

json_string = '{"title": "Fix login bug", "status": "open"}'

task = json.loads(json_string)
print(task)
print(type(task))
print(task["title"])

# json.loads({"key": "value"})
tasks = [
    {"id": 1, "title": "Fix login bug", "status": "відкрито"},
    {"id": 2, "title": "Write tests", "status": "done"},
]

with open("lesson_16_json/tasks.json", "w", encoding="utf-8") as file:
    json.dump(tasks, file, indent=4, ensure_ascii=False)

with open("lesson_16_json/task.json", "r", encoding="utf-8") as file:
    new_tasks = json.load(file)

new_tasks["20years"] = "JustMarried"

with open("lesson_16_json/task.json", "w", encoding="utf-8") as file:
    json.dump(new_tasks, file, indent=4, ensure_ascii=False)


class Issue:
    def __init__(self, title, status, priority=1):
        self.title = title
        self.status = status
        self.priority = priority

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "priority": self.priority
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            title=data["title"],
            status=data["status"],
            priority=data["priority"]
        )

issue = Issue("Fix bug", "open")
# json.dumps(issue)
json_string = json.dumps(issue.to_dict(), ensure_ascii=False, indent=4)
print(json_string)

issues = [Issue("Fix bug", "open", "high"), Issue("Write tests", "done", "low")]
data = [i.to_dict() for i in issues]
# with open("lesson_16_json/task2.json", "w", encoding="utf-8") as file:
#     json.dump(data, file, ensure_ascii=False, indent=4)

# with open("lesson_16_json/task2.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# issues = [Issue.from_dict(d) for d in data]
# print(issues[0].title)

file_path = Path("lesson_16_json") / "task2.json"
print(file_path.exists())
print(file_path)


def load_issues(file_path: Path):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

#print(load_issues(file_path))

def load_data(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as err:
        print(err)
        return []
print(load_data(file_path))
