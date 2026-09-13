# Заняття 19. Замикання та зворотний виклик

**Викладач:** Олександр Панченко, ТОВ «Тренінг-центр КьюЕйЛайт»

## Частина 1. Нова тема: Замикання та зворотний виклик (1 година)

### 2.1 Функції як об'єкти першого класу

У Python функції є **об'єктами першого класу** (first-class citizens). Це означає, що функцію можна:

- присвоїти змінній
- передати як аргумент іншій функції
- повернути з функції
- зберегти у списку чи словнику

```python
def greet(name: str) -> str:
    return f"Привіт, {name}!"

# Присвоєння функції змінній
say_hello = greet
print(say_hello("Олена"))  # Привіт, Олена!

# Передача функції як аргументу
def apply(func, value):
    return func(value)

result = apply(greet, "Максим")
print(result)  # Привіт, Максим!
```

Зверніть увагу: `say_hello = greet` — ми передаємо **саму функцію**, а не результат її виклику. Дужки `()` означають виклик.

### 2.2 Внутрішні функції

Функцію можна визначити **всередині іншої функції**. Така функція називається **внутрішньою** (inner function або nested function).

```python
def outer():
    print("Зовнішня функція")

    def inner():
        print("Внутрішня функція")

    inner()  # Виклик зсередини зовнішньої

outer()
# Виведе:
# Зовнішня функція
# Внутрішня функція

# inner()  # NameError — inner недоступна зовні!
```

Внутрішня функція існує лише у просторі імен зовнішньої. Ззовні до неї напряму звернутися неможливо.

### 2.3 Замикання (Closure)

**Замикання** — це внутрішня функція, яка **«запам'ятовує» змінні** з зовнішньої функції, навіть після того, як зовнішня функція завершила виконання.

Простіше кажучи: функція «захоплює» (closes over) змінні оточуючого середовища і зберігає до них доступ.

```python
def make_greeting(greeting: str):
    def greet(name: str) -> str:
        return f"{greeting}, {name}!"  # greeting — захоплена змінна
    return greet  # Повертаємо функцію, а не результат!

hello = make_greeting("Привіт")
hi = make_greeting("Вітаю")

print(hello("Соломія"))  # Привіт, Соломія!
print(hi("Богдан"))      # Вітаю, Богдан!
```

Тут `hello` — це не просто функція `greet`, а **замикання**: функція разом із захопленою змінною `greeting = "Привіт"`.

**Перевірка замикання:**

```python
print(hello.__closure__)               # (<cell at 0x...>,)
print(hello.__closure__[0].cell_contents)  # Привіт
```

### 2.4 Захоплення змінних (Variable Capture)

Замикання захоплює **посилання** на змінну, а не її значення на момент створення. Це важлива деталь, яка може призвести до несподіваних результатів.

**Проблема із циклом:**

```python
functions = []
for i in range(3):
    def f():
        return i  # Захоплює посилання на i, а не поточне значення
    functions.append(f)

print(functions[0]())  # 2 — несподівано!
print(functions[1]())  # 2
print(functions[2]())  # 2
```

Усі функції отримують `2`, бо після завершення циклу `i == 2`, і всі замикання вказують на **одну й ту саму** змінну `i`.

**Рішення — default argument:**

```python
functions = []
for i in range(3):
    def f(x=i):  # Фіксуємо значення i у момент створення
        return x
    functions.append(f)

print(functions[0]())  # 0
print(functions[1]())  # 1
print(functions[2]())  # 2
```

### 2.5 Практичне застосування замикань: фабричні функції

Замикання часто використовують для створення **фабричних функцій** — функцій, що генерують інші функції з різною поведінкою.

```python
def make_multiplier(factor: int):
    def multiply(number: float) -> float:
        return number * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10.0
print(triple(5))   # 15.0
print(double(7))   # 14.0
```

```python
def make_validator(min_val: float, max_val: float):
    def validate(value: float) -> bool:
        return min_val <= value <= max_val
    return validate

is_valid_age = make_validator(0, 150)
is_valid_grade = make_validator(0, 100)

print(is_valid_age(25))    # True
print(is_valid_age(200))   # False
print(is_valid_grade(85))  # True
```

### 2.6 Замикання зі збереженням стану

Замикання можуть зберігати **змінний стан** між викликами. Для зміни захопленої змінної в Python 3 використовується ключове слово `nonlocal`.

```python
def make_counter(start: int = 0):
    count = start

    def increment():
        nonlocal count  # Дозволяємо змінювати count із зовнішнього scope
        count += 1
        return count

    def reset():
        nonlocal count
        count = start
        return count

    def get():
        return count

    return increment, reset, get

inc, rst, get = make_counter()

print(inc())  # 1
print(inc())  # 2
print(inc())  # 3
print(get())  # 3
print(rst())  # 0
print(inc())  # 1
```

Зверніть увагу: `nonlocal` відрізняється від `global`. `global` вказує на глобальний простір імен модуля, `nonlocal` — на найближчий зовнішній scope функції.

### 2.7 Зворотний виклик (Callback)

**Callback** (зворотний виклик) — це функція, яку передають як аргумент і яку буде викликано пізніше, у певний момент або при певній умові.

Концепція: «не викликай мене — я сам тебе викличу» (Inversion of Control).

```python
def process_data(data: list, callback):
    """Обробляє дані та передає результат у callback."""
    result = [item * 2 for item in data]
    callback(result)

def print_result(data: list) -> None:
    print("Результат:", data)

def save_result(data: list) -> None:
    with open("result.txt", "w") as f:
        f.write(str(data))
    print("Збережено у файл")

numbers = [1, 2, 3, 4, 5]

process_data(numbers, print_result)   # Виводить результат
process_data(numbers, save_result)    # Зберігає у файл
```

Callback дозволяє **відокремити алгоритм обробки від того, що робити з результатом**.

### 2.8 Callable та перевірка викличності

Не лише функції є «викличними» (callable) об'єктами в Python. Будь-який об'єкт, у якого визначений метод `__call__`, може бути викликаний як функція.

**Перевірка:** вбудована функція `callable()` повертає `True`, якщо об'єкт можна викликати.

```python
def my_func():
    return 42

print(callable(my_func))   # True
print(callable(42))        # False
print(callable(print))     # True
print(callable(list))      # True — list є класом, його виклик створює екземпляр
```

**Клас із `__call__`:**

```python
class Multiplier:
    def __init__(self, factor: int):
        self.factor = factor

    def __call__(self, value: float) -> float:
        return value * self.factor

double = Multiplier(2)
print(callable(double))  # True
print(double(5))         # 10.0
print(double(7))         # 14.0
```

Такий підхід корисний, коли потрібна функція зі збереженим станом, але у вигляді об'єкта (альтернатива замиканню).

### 2.9 Функція sorted() та параметр key

Вбудована функція `sorted()` приймає callback-функцію через параметр `key`. Ця функція визначає, **за яким значенням** сортувати елементи.

```python
students = [
    {"name": "Оксана", "grade": 85},
    {"name": "Іван", "grade": 92},
    {"name": "Марія", "grade": 78},
]

# Сортування за оцінкою (зростання)
by_grade = sorted(students, key=lambda s: s["grade"])
print(by_grade)

# Сортування за оцінкою (спадання)
by_grade_desc = sorted(students, key=lambda s: s["grade"], reverse=True)
print(by_grade_desc)

# Сортування за довжиною імені
words = ["Python", "Go", "JavaScript", "Rust"]
by_length = sorted(words, key=len)  # len — це callback!
print(by_length)  # ['Go', 'Rust', 'Python', 'JavaScript']
```

`key=len` — передаємо функцію `len` як callback. `sorted` викликає `len(element)` для кожного елемента і сортує за отриманими значеннями.

**Складне сортування — сортування за кількома ключами:**

```python
students = [
    {"name": "Оксана", "grade": 85, "age": 20},
    {"name": "Іван", "grade": 85, "age": 18},
    {"name": "Марія", "grade": 92, "age": 20},
]

# Спочатку за оцінкою (спадання), потім за іменем (зростання)
result = sorted(students, key=lambda s: (-s["grade"], s["name"]))
for s in result:
    print(s)
```

### 2.10 Порівняння: замикання vs клас

| Характеристика | Замикання | Клас із `__call__` |
|---|---|---|
| Простота синтаксису | Компактніше | Більше коду |
| Збереження стану | Через `nonlocal` | Через атрибути `self` |
| Читабельність | Може бути складніше | Більш явне |
| Розширюваність | Обмежена | Простіше додавати методи |
| Коли використовувати | Проста логіка, фабрики | Складний стан, багато методів |

### 2.11 Підсумок

**Замикання** дозволяють:
- Створювати фабричні функції з налаштовуваною поведінкою
- Зберігати стан без глобальних змінних
- Інкапсулювати логіку в компактному вигляді

**Callbacks** дозволяють:
- Передавати поведінку як аргумент
- Відокремити алгоритм від дії з результатом
- Налаштовувати поведінку функцій (`sorted`, `filter`, `map`)

**`callable()`** дозволяє:
- Перевірити, чи є об'єкт викличним
- Безпечно передавати об'єкти як callbacks


# Повторення 1: логування 

[content_14_log.md] Зміст лекції

**Ключові концепції:**

- Модуль `logging`: рівні `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

```python
import logging

logging.basicConfig(level=logging.INFO)

def divide(a: float, b: float) -> float:
    if b == 0:
        logging.error("Ділення на нуль!")
        raise ValueError("Дільник не може бути нулем")
    return a / b

try:
    result = divide(10, 0)
except ValueError as e:
    logging.warning(f"Виняток: {e}")
finally:
    logging.info("Операцію завершено")
```

### 1.1 SQLite та локальні бази даних (Заняття 18)

На минулому занятті ми навчились працювати з SQLite — вбудованою реляційною базою даних Python.

**Ключові концепції:**

- `sqlite3` — стандартна бібліотека Python, не потребує встановлення
- Підключення відбувається через `sqlite3.connect("назва.db")`
- Для виконання запитів потрібен **курсор**: `conn.cursor()`
- Зміни фіксуються через `conn.commit()`, з'єднання закривається через `conn.close()`
- Контекстний менеджер `with` автоматично виконує commit при виході без помилок

**Типовий патерн роботи:**

```python
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade INTEGER
    )
""")

cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", ("Оксана", 90))
conn.commit()

cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
```

**Основні SQL-команди:**

| Команда | Дія |
|---|---|
| `CREATE TABLE IF NOT EXISTS` | Створення таблиці (якщо ще не існує) |
| `INSERT INTO ... VALUES (?, ?)` | Додавання рядка (параметризовані запити) |
| `SELECT * FROM ...` | Вибірка всіх записів |
| `WHERE` | Фільтрація рядків |
| `JOIN` | Об'єднання таблиць |
| `fetchall()` | Отримання всіх рядків результату |
| `fetchone()` | Отримання одного рядка |

**Зовнішні ключі (Foreign Keys):**

Зв'язок між таблицями встановлюється через зовнішній ключ. SQLite за замовчуванням не перевіряє їх — потрібно явно увімкнути:

```python
cursor.execute("PRAGMA foreign_keys = ON")
```

### 1.2 CSV-файли (Заняття 17)

**Ключові концепції:**

- Модуль `csv` — стандартна бібліотека Python
- Читання: `csv.reader()` або `csv.DictReader()`
- Запис: `csv.writer()` або `csv.DictWriter()`
- При відкритті CSV-файлу в Python 3 потрібно вказувати `newline=""` для коректної обробки рядків

```python
import csv

# Читання
with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["grade"])

# Запис
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "grade"])
    writer.writeheader()
    writer.writerow({"name": "Іван", "grade": 85})
```

### 1.3 JSON-серіалізація (Заняття 16)

**Ключові концепції:**

- Модуль `json` — стандартна бібліотека Python
- `json.dumps()` — серіалізація об'єкта в рядок
- `json.dump()` — серіалізація у файл
- `json.loads()` — десеріалізація з рядка
- `json.load()` — десеріалізація з файлу
- Параметр `ensure_ascii=False` — підтримка кирилиці
- Параметр `indent=2` — форматований вивід

```python
import json

data = {"name": "Марія", "scores": [85, 90, 78]}

# Серіалізація у файл
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Десеріалізація з файлу
with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded["name"])
```

### 1.4 Модульне програмування та пакети (Заняття 15)

**Ключові концепції:**

- Модуль — будь-який `.py`-файл
- Пакет — директорія з файлом `__init__.py`
- Імпорт: `import module`, `from module import func`, `from module import *`
- Точка входу: `if __name__ == "__main__":` — код виконується лише при прямому запуску файлу
- Стандартні модулі: `os`, `sys`, `pathlib`, `datetime`, `random`, `math`

```python
# utils/math_ops.py
def add(a: float, b: float) -> float:
    return a + b

# main.py
from utils.math_ops import add

if __name__ == "__main__":
    result = add(3, 5)
    print(result)
```

### Домашнє завдання

#### Завдання 1. Козацька фабрика вітань

Запорізькі козаки мають різні звання: «Гетьман», «Кошовий отаман», «Сотник», «Козак». Кожне звання вітається по-різному.

Напиши функцію `make_greeter(rank: str)`, яка повертає функцію-вітальник. Кожна повернена функція при виклику з іменем козака повертає рядок:
`"<звання> <ім'я>, слава Україні!"`

```text
Приклад:
greet_hetman = make_greeter("Гетьман")
print(greet_hetman("Іван Мазепа"))
# Гетьман Іван Мазепа, слава Україні!
```

#### Завдання 2. Лічильник козацьких перемог

Напиши функцію `make_battle_counter(warrior_name: str)`, яка повертає три функції:
- `add_victory()` — додає перемогу та повертає кількість перемог
- `add_defeat()` — додає поразку та повертає кількість поразок
- `get_stats()` — повертає рядок виду: `"Козак <ім'я>: перемог — X, поразок — Y"`

Усі три функції мають спільний стан через замикання.

#### Завдання 3. Сортування дружини

Є список козаків із полку:

```python
warriors = [
    {"name": "Тарас", "rank": "Сотник", "battles": 15},
    {"name": "Остап", "rank": "Козак", "battles": 8},
    {"name": "Богдан", "rank": "Сотник", "battles": 22},
    {"name": "Микола", "rank": "Кошовий", "battles": 30},
]
```

Напиши функцію `make_sorter(field: str, reverse: bool = False)`, яка повертає функцію сортування. Повернена функція приймає список козаків і повертає відсортований список за вказаним полем.

```text
Приклад:
sort_by_battles = make_sorter("battles", reverse=True)
result = sort_by_battles(warriors)
```

#### Бонус. Перевірник даних

Напиши функцію `make_validator(field: str, min_val, max_val)`, яка повертає функцію-валідатор. Повернена функція приймає словник і повертає `True`, якщо значення поля знаходиться у допустимому діапазоні.

Використай її для перевірки: чи є в козака від 1 до 50 битв і чи не від'ємна кількість перемог.

```text
Приклад:
validate_battles = make_validator("battles", 1, 50)
print(validate_battles({"name": "Тарас", "battles": 15}))  # True
print(validate_battles({"name": "Дід", "battles": 99}))    # False
```
