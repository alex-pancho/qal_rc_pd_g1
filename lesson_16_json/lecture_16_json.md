# Заняття 16. Робота з JSON та серіалізація даних

## План заняття

| Блок | Час | Зміст |
|---|---|---|
| Теорія | 60 хв | JSON, модуль `json`, серіалізація |
| Практика | 60 хв | Застосування у навчальних проєктах |

# ЧАСТИНА 1. ТЕОРІЯ

## Блок 1. Повторення: словники, списки, умови

Перш ніж переходити до JSON — швидко згадаємо інструменти, без яких JSON не має сенсу. Бо JSON — це, по суті, і є словники та списки, тільки у текстовому форматі.

### Словники

Словник — це структура «ключ → значення». Ключ завжди рядок або число, значення — будь-що.

```python
researcher = {
    "name": "Вернадський",
    "age": 82,
    "fields": ["мінералогія", "геохімія", "біосфера"],
    "alive": False
}
```

Найважливіші операції зі словниками, які знадобляться сьогодні:

```python
# Читання значення
print(researcher["name"])           # Вернадський

# Безпечне читання — якщо ключ відсутній, не падає
print(researcher.get("city", "невідомо"))   # невідомо

# Додавання або зміна
researcher["city"] = "Київ"

# Перевірка наявності ключа
if "age" in researcher:
    print("вік відомий")

# Перебір ключів і значень
for key, value in researcher.items():
    print(f"{key}: {value}")

# Видалення
del researcher["city"]
# або
researcher.pop("city", None)    # None — щоб не падало, якщо ключа немає
```

Вкладені словники — словник всередині словника:

```python
mineral = {
    "name": "Кварц",
    "properties": {
        "hardness": 7,
        "formula": "SiO₂"
    }
}

# Доступ до вкладеного значення
print(mineral["properties"]["hardness"])    # 7
print(mineral.get("properties", {}).get("hardness"))    # безпечно
```

### Списки

Список — впорядкована колекція елементів.

```python
minerals = ["Кварц", "Берил", "Топаз", "Діамант"]
```

Операції, які знадобляться:

```python
# Додавання
minerals.append("Смарагд")

# Видалення за значенням
minerals.remove("Топаз")    # якщо немає — ValueError

# Видалення за індексом
minerals.pop(0)

# Перебір з індексом
for i, mineral in enumerate(minerals):
    print(f"{i + 1}. {mineral}")

# Список словників — дуже часта структура
records = [
    {"name": "Кварц", "hardness": 7},
    {"name": "Берил", "hardness": 8},
]

# Знайти елемент за полем
for record in records:
    if record["name"] == "Берил":
        print(record["hardness"])
```

### Умовні конструкції — коротке нагадування

Під час роботи з JSON часто потрібно перевіряти: чи існує файл, чи є ключ, чи не порожній список. Типові перевірки:

```python
data = []

# Перевірка на порожнечу
if not data:
    print("список порожній")

# Перевірка типу
if isinstance(data, list):
    print("це список")

# Перевірка наявності ключа у словнику
record = {"name": "Кварц"}
if "hardness" not in record:
    print("твердість не вказана")
```

## Блок 2. Що таке JSON і навіщо він потрібен

### Проблема, яку вирішує JSON

Уяви: ти запустив програму, створив 10 задач у Task Manager, і закрив термінал. Наступного разу запускаєш — усі задачі зникли. Тому що вони жили тільки в пам'яті: у списку всередині об'єкта `TaskManager`. Пам'ять очищається — дані зникають.

Щоб дані **жили між запусками** — їх потрібно зберігати. Є багато способів: бази даних, CSV, бінарні файли. Але найпростіший і найчитабельніший для початку — **JSON**.

### Що таке JSON

**JSON** (JavaScript Object Notation) — це текстовий формат для зберігання і передачі структурованих даних. Попри назву, він давно вийшов за межі JavaScript і став універсальним стандартом: його розуміє Python, Java, Go, будь-який браузер, будь-яке API.

Головна ідея: **будь-яка складна структура даних записується як звичайний текст**, який можна зберегти у файл або передати по мережі, а потім відновити назад.

Приклад JSON-файлу `task.json`:

```json
{
    "id": 1,
    "title": "Написати звіт",
    "status": "open",
    "priority": "high",
    "tags": ["робота", "терміново"],
    "assignee": null
}
```

Якщо ти вже знаєш Python-словники — JSON виглядає майже ідентично. Це не випадково.

### Синтаксис JSON

JSON підтримує рівно шість типів даних:

| JSON тип | Python відповідник | Приклад |
|---|---|---|
| `string` | `str` | `"Привіт"` |
| `number` | `int` або `float` | `42`, `3.14` |
| `boolean` | `bool` | `true`, `false` |
| `null` | `None` | `null` |
| `object` | `dict` | `{"key": "value"}` |
| `array` | `list` | `[1, 2, 3]` |

Важливі відмінності від Python:

```json
// JSON                        # Python
true                           True
false                          False
null                           None
"рядки лише в подвійних"      'можна одинарні'
```

```json
// У JSON немає:
// - коментарів
// - кортежів
// - множин
// - об'єктів із ключами-числами (лише рядки)
```

Типова помилка початківців — написати `True` з великої літери або `None` у JSON-файлі вручну. JSON цього не розуміє — тільки `true` і `null`.

### Структура JSON на практиці

JSON-файл може бути або об'єктом (словником) на верхньому рівні:

```json
{
    "title": "Fix login bug",
    "status": "open"
}
```

Або масивом (списком):

```json
[
    {"title": "Fix login bug", "status": "open"},
    {"title": "Write tests", "status": "done"}
]
```

Для зберігання колекцій записів (задачі, транзакції, клієнти) зазвичай використовують **список словників** — це найзручніша структура, яка легко перебирається і фільтрується.

## Блок 3. Модуль `json`

Модуль вбудований — нічого встановлювати не потрібно:

```python
import json
```

Він надає чотири основні функції. Запам'ятай їх парами:

| Функція | Що робить | Аналогія |
|---|---|---|
| `json.dumps()` | Python → рядок JSON | «dump to string» |
| `json.loads()` | рядок JSON → Python | «load from string» |
| `json.dump()` | Python → файл JSON | «dump to file» |
| `json.load()` | файл JSON → Python | «load from file» |

### `json.dumps()` — об'єкт у рядок

```python
import json

task = {
    "title": "Fix login bug",
    "status": "open",
    "priority": "high",
    "tags": ["backend", "auth"]
}

# Перетворити словник на рядок JSON
json_string = json.dumps(task)
print(json_string)
# {"title": "Fix login bug", "status": "open", "priority": "high", "tags": ["backend", "auth"]}

print(type(json_string))    # <class 'str'>
```

Результат — звичайний рядок. Його можна передати по мережі, записати у файл, вставити у базу даних.

Параметр `indent` робить рядок читабельним:

```python
json_string = json.dumps(task, indent=4)
print(json_string)
```

```json
{
    "title": "Fix login bug",
    "status": "open",
    "priority": "high",
    "tags": [
        "backend",
        "auth"
    ]
}
```

Параметр `ensure_ascii=False` — важливий для кирилиці:

```python
task = {"title": "Виправити баг входу"}

# Без параметра — кирилиця екранується
print(json.dumps(task))
# {"title": "\u0412\u0438\u043f\u0440\u0430\u0432\u0438\u0442\u0438 ..."}

# З параметром — читабельно
print(json.dumps(task, ensure_ascii=False))
# {"title": "Виправити баг входу"}
```

### `json.loads()` — рядок у об'єкт

```python
json_string = '{"title": "Fix login bug", "status": "open"}'

task = json.loads(json_string)
print(task)         # {'title': 'Fix login bug', 'status': 'open'}
print(type(task))   # <class 'dict'>

print(task["title"])    # Fix login bug
```

Типова помилка — передати у `loads()` не рядок, а байти або вже розпарсений словник:

```python
json.loads({"key": "value"})    # TypeError — це вже dict, не рядок
```

### `json.dump()` — об'єкт у файл

```python
tasks = [
    {"id": 1, "title": "Fix login bug", "status": "open"},
    {"id": 2, "title": "Write tests", "status": "done"},
]

with open("tasks.json", "w", encoding="utf-8") as file:
    json.dump(tasks, file, indent=4, ensure_ascii=False)
```

Після виконання у поточній директорії з'явиться файл `tasks.json` із таким вмістом:

```json
[
    {
        "id": 1,
        "title": "Fix login bug",
        "status": "open"
    },
    {
        "id": 2,
        "title": "Write tests",
        "status": "done"
    }
]
```

Зверни увагу: `json.dump()` приймає **два обов'язкові аргументи** — об'єкт і файловий об'єкт. Порядок важливий: спочатку дані, потім файл.

### `json.load()` — файл у об'єкт

```python
with open("tasks.json", "r", encoding="utf-8") as file:
    tasks = json.load(file)

print(type(tasks))      # <class 'list'>
print(len(tasks))       # 2
print(tasks[0]["title"])    # Fix login bug
```

Після `json.load()` ти отримуєш звичайний Python-об'єкт — список, словник, або що там було у файлі. Далі працюєш з ним як завжди.

## Блок 4. Серіалізація та десеріалізація

### Терміни

**Серіалізація** — перетворення об'єкта з пам'яті у формат, придатний для збереження або передачі. У нашому випадку: Python-об'єкт → JSON-рядок або JSON-файл.

**Десеріалізація** — зворотній процес: JSON-рядок або файл → Python-об'єкт.

```
Python об'єкт  →  серіалізація  →  JSON (рядок або файл)
JSON           →  десеріалізація →  Python об'єкт
```

Простіше запам'ятати так: **серіалізація — пакуємо, десеріалізація — розпаковуємо**.

### Проблема: клас не серіалізується напряму

Модуль `json` вміє серіалізувати лише вбудовані типи Python: `dict`, `list`, `str`, `int`, `float`, `bool`, `None`. Якщо спробувати передати об'єкт власного класу напряму — отримаємо помилку:

```python
class Issue:
    def __init__(self, title, status):
        self.title = title
        self.status = status

issue = Issue("Fix bug", "open")
json.dumps(issue)   # TypeError: Object of type Issue is not JSON serializable
```

Це логічно: `json` не знає, які саме атрибути твого класу потрібно зберегти і в якому вигляді.

### Рішення 1: метод `to_dict()`

Найпростіший і найпрозоріший підхід — додати у клас метод, який перетворює об'єкт на словник:

```python
class Issue:
    def __init__(self, title, status, priority):
        self.title = title
        self.status = status
        self.priority = priority

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "priority": self.priority
        }
```

Тепер серіалізація виглядає так:

```python
issue = Issue("Fix login bug", "open", "high")

# Один об'єкт
json_string = json.dumps(issue.to_dict(), ensure_ascii=False, indent=4)

# Список об'єктів
issues = [Issue("Fix bug", "open", "high"), Issue("Write tests", "done", "low")]
data = [i.to_dict() for i in issues]
json.dump(data, file, ensure_ascii=False, indent=4)
```

### Рішення 2: метод `from_dict()` — фабричний метод

Щоб відновити об'єкт зі словника після завантаження з файлу — додаємо **класовий метод** `from_dict()`:

```python
class Issue:
    def __init__(self, title, status, priority):
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
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            status=data["status"],
            priority=data["priority"]
        )
```

Повний цикл збереження і завантаження:

```python
# Зберегти
issues = [Issue("Fix bug", "open", "high"), Issue("Write tests", "done", "low")]

with open("issues.json", "w", encoding="utf-8") as f:
    json.dump([i.to_dict() for i in issues], f, ensure_ascii=False, indent=4)

# Завантажити
with open("issues.json", "r", encoding="utf-8") as f:
    data = json.load(f)

issues = [Issue.from_dict(d) for d in data]
print(issues[0].title)  # Fix bug
```

Цей патерн — `to_dict()` / `from_dict()` — є стандартним підходом для роботи з JSON у Python-проєктах без зовнішніх бібліотек. Запам'ятай його: він буде використовуватись в усіх наступних модулях аж до Django.

### Обробка помилок при роботі з JSON

Два типових сценарії, які потрібно передбачати:

**Файл не існує** — перший запуск програми, файл ще не створено:

```python
import os

def load_issues():
    if not os.path.exists("issues.json"):
        return []

    with open("issues.json", "r", encoding="utf-8") as f:
        return json.load(f)
```

**Файл пошкоджений або містить некоректний JSON:**

```python
def load_issues():
    try:
        with open("issues.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Файл пошкоджений. Починаємо з порожнього списку.")
        return []
```

## Блок 5. Типові патерни роботи з JSON-файлами

### Патерн «Завантажити або створити»

```python
def load_data(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
```

### Патерн «Оновити один запис у файлі»

```python
def update_status(filepath, issue_id, new_status):
    data = load_data(filepath)

    for record in data:
        if record["id"] == issue_id:
            record["status"] = new_status
            break

    save_data(filepath, data)
```

Зверни увагу на підхід: **завантажив → змінив у пам'яті → перезаписав файл повністю**. Для невеликих обсягів даних це стандартна практика.

### Патерн «Видалити запис»

```python
def delete_issue(filepath, issue_id):
    data = load_data(filepath)
    data = [record for record in data if record["id"] != issue_id]
    save_data(filepath, data)
```

# Підсумок заняття

| Концепція | Суть |
|---|---|
| JSON | Текстовий формат для зберігання структурованих даних |
| `json.dumps()` | Об'єкт → рядок |
| `json.loads()` | Рядок → об'єкт |
| `json.dump()` | Об'єкт → файл |
| `json.load()` | Файл → об'єкт |
| Серіалізація | Пакуємо об'єкт для збереження |
| Десеріалізація | Розпаковуємо назад |
| `to_dict()` / `from_dict()` | Стандартний патерн для власних класів |

На наступному занятті — CSV: ще один формат зберігання даних, зручний для таблиць і звітів.