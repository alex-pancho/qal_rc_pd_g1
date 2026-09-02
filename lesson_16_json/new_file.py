import json
from source_json import Issue

with open("lesson_16_json/task2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

issues = [Issue.from_dict(d) for d in data]
print(issues[0].title)

new_issue = Issue("New title", "critical", "hight")
print(new_issue.title)