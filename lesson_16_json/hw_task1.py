import json


folklore_record = {
    "title": "Ой у лузі червона калина",
    "genre": "пісня",
    "region": "Полтавщина",
    "narrator": "Ганна Остапенко",
    "year": 1932,
    "content": "Українська народна пісня",
    "tags": ["народна", "історична", "козацька"],
    "verified": True,
}


json_string = json.dumps(folklore_record)

print(json_string)
print(type(json_string))

pretty_json = json.dumps(
    folklore_record,
    indent=4,
    ensure_ascii=False,
)

print(pretty_json)

restored = json.loads(json_string)

print(type(restored))
print(restored["title"])
print(restored["genre"])
print(restored["region"])
