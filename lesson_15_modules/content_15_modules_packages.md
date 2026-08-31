# Заняття 15. Модульне програмування та пакети

**Курс:** Програмування Python | QALight  
**Тривалість:** 2 години (1 год. теорія + 1 год. практика)

## 🎯 Мета заняття

Зрозуміти, як Python організовує код у модулі та пакети, навчитися використовувати різні форми імпорту, розібратися з просторами імен, коректно визначати точку входу програми та будувати структуру реального Python-проєкту.

## Частина 1. Простори імен (Namespaces)

### Що таке простір імен?

**Простір імен** — це відображення між іменами (змінних, функцій, класів) та об'єктами, на які вони вказують. Простіше кажучи, це «словник», де ключ — ім'я, значення — об'єкт.

Python підтримує кілька рівнів просторів імен, і при зверненні до будь-якого імені інтерпретатор шукає його у чітко визначеному порядку.

### Правило LEGB

Python шукає ім'я у такій послідовності:

```
L — Local       (локальний: всередині поточної функції)
E — Enclosing   (обгортаючий: у функції, що містить поточну)
G — Global      (глобальний: на рівні модуля)
B — Built-in    (вбудований: print, len, range тощо)
```

```python
x = "global"          # G — глобальний простір імен

def outer():
    x = "enclosing"   # E — простір імен outer

    def inner():
        x = "local"   # L — локальний простір імен inner
        print(x)      # "local" — знайдено на рівні L

    inner()
    print(x)          # "enclosing" — знайдено на рівні E

outer()
print(x)              # "global" — знайдено на рівні G
```

### `global` та `nonlocal`

За замовчуванням Python не дозволяє змінювати змінну з зовнішнього простору імен зсередини функції — він просто створює нову локальну. Щоб явно звернутися до зовнішньої змінної, використовують ключові слова `global` і `nonlocal`.

```python
counter = 0           # глобальна змінна

def increment():
    global counter    # явно вказуємо, що працюємо з глобальною
    counter += 1

increment()
increment()
print(counter)        # 2
```

```python
def outer():
    count = 0         # змінна outer

    def inner():
        nonlocal count  # звертаємось до змінної enclosing-рівня
        count += 1

    inner()
    inner()
    print(count)        # 2

outer()
```

> 💡 **Порада:** зловживати `global` і `nonlocal` не варто — це ускладнює читання коду. Краще передавати значення через аргументи та повертати через `return`.

### Перегляд простору імен

```python
# Вбудовані функції для дослідження просторів імен:
print(dir())          # імена у поточному просторі імен
print(globals())      # глобальний простір імен (dict)
print(locals())       # локальний простір імен (dict)
```

## Частина 2. Модулі

### Що таке модуль?

**Модуль** — це будь-який файл з кодом Python (розширення `.py`). Коли ви пишете `import math` — Python завантажує файл `math.py` зі стандартної бібліотеки і робить його вміст доступним у вашому коді.

Кожен модуль має **власний простір імен**, тому імена в різних модулях не конфліктують між собою.

### Форми імпорту

```python
# 1. Імпорт усього модуля — звертаємось через ім'я модуля
import math
print(math.sqrt(16))        # 4.0
print(math.pi)              # 3.14159...

# 2. Імпорт конкретних імен — потрапляють у поточний простір імен
from math import sqrt, pi
print(sqrt(16))             # 4.0 — без префікса math.
print(pi)                   # 3.14159...

# 3. Псевдонім для модуля
import numpy as np          # стандартна угода у спільноті
print(np.array([1, 2, 3]))

# 4. Псевдонім для імені
from math import factorial as fact
print(fact(5))              # 120

# 5. Імпорт усього (не рекомендується!)
from math import *          # забруднює простір імен
```

> ⚠️ `from module import *` — поганий стиль: незрозуміло, звідки прийшло кожне ім'я, і можливі конфлікти.

### Як Python шукає модуль?

При виклику `import my_module` Python перевіряє у такому порядку:

1. Вже завантажені модулі (`sys.modules` — кеш)
2. Вбудовані модулі (`sys.builtin_module_names`)
3. Шляхи з `sys.path` — список директорій:
   - директорія поточного скрипта
   - директорії зі змінної середовища `PYTHONPATH`
   - директорії стандартної бібліотеки
   - директорія `site-packages` (сторонні пакети)

```python
import sys
print(sys.path)   # переглянути шляхи пошуку
```

### Корисні атрибути модуля

```python
import math

print(math.__name__)    # 'math'       — ім'я модуля
print(math.__file__)    # '/usr/.../math.cpython-312.pyc' — шлях до файлу
print(math.__doc__)     # рядок документації модуля
print(dir(math))        # список усіх імен, визначених у модулі
```

### Власний модуль

Створимо файл `calculator.py`:

```python
# calculator.py
"""Простий калькулятор — демонстраційний модуль."""

PI = 3.14159


def add(a: float, b: float) -> float:
    """Повертає суму двох чисел."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Повертає різницю двох чисел."""
    return a - b


def circle_area(radius: float) -> float:
    """Повертає площу кола."""
    return PI * radius ** 2
```

Використовуємо його в іншому файлі:

```python
# main.py
import calculator

print(calculator.add(3, 5))          # 8
print(calculator.circle_area(7))     # 153.938...
print(calculator.PI)                 # 3.14159
```

## Частина 3. Точка входу `main()`

### Проблема без точки входу

Коли Python імпортує модуль — він **виконує весь його код** на верхньому рівні. Якщо у файлі є виклики функцій або друк поза блоком `if __name__ == "__main__"`, вони спрацюють і при імпорті, що небажано.

```python
# calculator.py — поганий приклад
def add(a, b):
    return a + b

# Цей код виконається навіть при імпорті!
print("Тестую функцію add:")
print(add(2, 3))
```

```python
# main.py
import calculator   # ← у консолі з'явиться "Тестую функцію add: 5"
```

### Змінна `__name__`

Python автоматично встановлює змінну `__name__` для кожного модуля:

- Якщо файл **запускається напряму** — `__name__ == "__main__"`
- Якщо файл **імпортується** — `__name__ == "назва_модуля"`

```python
# Перевіримо:
print(__name__)
# При запуску напряму: __main__
# При імпорті:         calculator
```

### Правильна точка входу

```python
# calculator.py — правильний варіант
"""Модуль калькулятора."""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def main() -> None:
    """Точка входу — виконується тільки при прямому запуску."""
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")


if __name__ == "__main__":
    main()
```

Тепер:
- `python calculator.py` → виконає `main()`
- `import calculator` → тільки завантажить функції, `main()` не запуститься

## Частина 4. Стандартні модулі

Python постачається з великою стандартною бібліотекою — «батарейки включені» (batteries included). Ось найбільш вживані модулі:

| Модуль | Призначення | Приклад |
|---|---|---|
| `os` | Робота з операційною системою | `os.getcwd()`, `os.listdir()` |
| `sys` | Параметри інтерпретатора | `sys.argv`, `sys.path` |
| `math` | Математичні функції | `math.sqrt()`, `math.pi` |
| `random` | Генерація випадкових чисел | `random.randint()`, `random.choice()` |
| `datetime` | Дата і час | `datetime.now()`, `timedelta` |
| `pathlib` | Сучасна робота з шляхами | `Path("dir") / "file.txt"` |
| `json` | Серіалізація JSON | `json.dumps()`, `json.loads()` |
| `re` | Регулярні вирази | `re.findall()`, `re.sub()` |
| `collections` | Розширені структури даних | `defaultdict`, `Counter`, `deque` |
| `itertools` | Інструменти для ітерацій | `chain()`, `product()` |
| `functools` | Інструменти для функцій | `lru_cache`, `partial`, `reduce` |

### Приклади використання

```python
import os
import sys
from pathlib import Path
from datetime import datetime
import random

# os — система
print(os.getcwd())                     # поточна директорія
print(os.path.exists("myfile.txt"))    # чи існує файл
os.makedirs("new_dir", exist_ok=True)  # створити директорію

# sys — інтерпретатор
print(sys.version)       # версія Python
print(sys.argv)          # аргументи командного рядка

# pathlib — сучасні шляхи
base = Path("project")
config_path = base / "config" / "settings.json"  # OS-незалежний шлях
print(config_path)       # project/config/settings.json

# datetime
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M"))  # 2024-01-15 10:30

# random
print(random.randint(1, 100))          # випадкове число 1–100
print(random.choice(["яблуко", "груша", "слива"]))  # випадковий елемент
```

## Частина 5. Пакети

### Що таке пакет?

**Пакет** — це директорія з файлами Python-модулів. Пакет дозволяє організувати код ієрархічно: замість десятків окремих файлів ви отримуєте логічно структуровану бібліотеку.

### Файл `__init__.py`

Щоб Python розпізнав директорію як пакет, у ній має бути файл `__init__.py`. Він може бути порожнім або містити ініціалізаційний код пакету.

```
my_package/
    __init__.py        ← робить директорію пакетом
    module_a.py
    module_b.py
```

### Імпорт з пакету

```python
# Варіант 1: через крапкову нотацію
import my_package.module_a
my_package.module_a.some_function()

# Варіант 2: імпортувати конкретне ім'я
from my_package.module_a import some_function
some_function()

# Варіант 3: через __init__.py (якщо там прописано)
from my_package import some_function
```

### `__init__.py` — фасад пакету

`__init__.py` часто використовують як «фасад»: імпортують ключові імена з підмодулів, щоб зовнішній код міг робити простий імпорт.

```python
# my_package/__init__.py
from .module_a import ClassA, function_a
from .module_b import ClassB

__all__ = ["ClassA", "ClassB", "function_a"]
```

Тепер замість `from my_package.module_a import ClassA` можна писати просто `from my_package import ClassA`.

### Відносні імпорти

Всередині пакету модулі можуть імпортувати один одного через **відносні імпорти** (з крапкою):

```python
# my_package/module_b.py

from . import module_a          # імпорт з того ж пакету
from .module_a import ClassA    # конкретне ім'я з сусіднього модуля
from ..utils import helper      # на рівень вище (підпакет → пакет)
```

> 💡 Відносні імпорти читаються так: `.` — поточний пакет, `..` — батьківський пакет, `...` — ще на рівень вище.

## Частина 6. Структура реального Python-проєкту

### Рекомендована структура

```
todo_project/                  ← корінь проєкту
│
├── pyproject.toml             ← метадані проєкту (або setup.py)
├── README.md                  ← опис проєкту
├── .gitignore
│
├── src/                       ← весь вихідний код
│   └── todo/                  ← пакет програми
│       ├── __init__.py
│       ├── main.py            ← точка входу
│       ├── models/            ← підпакет: класи даних
│       │   ├── __init__.py
│       │   ├── task.py
│       │   └── user.py
│       ├── storage/           ← підпакет: збереження даних
│       │   ├── __init__.py
│       │   ├── base.py
│       │   └── file_storage.py
│       └── utils/             ← підпакет: допоміжні функції
│           ├── __init__.py
│           └── validators.py
│
└── tests/                     ← тести (поза src)
    ├── __init__.py
    ├── test_task.py
    └── test_storage.py
```

### Приклад реалізації

```python
# src/todo/models/task.py
from datetime import datetime


class Task:
    def __init__(self, title: str):
        self.title = title
        self.is_done = False
        self.created_at = datetime.now()

    def complete(self) -> None:
        self.is_done = True

    def __repr__(self) -> str:
        status = "✅" if self.is_done else "⏳"
        return f"[{status}] {self.title}"
```

```python
# src/todo/utils/validators.py


def validate_title(title: str) -> str:
    """Перевіряє назву завдання та повертає очищений рядок."""
    if not title or not title.strip():
        raise ValueError("Назва не може бути порожньою")
    if len(title) > 100:
        raise ValueError("Назва не може перевищувати 100 символів")
    return title.strip()
```

```python
# src/todo/models/__init__.py
from .task import Task

__all__ = ["Task"]
```

```python
# src/todo/main.py
from todo.models import Task
from todo.utils.validators import validate_title


def main() -> None:
    tasks: list[Task] = []

    while True:
        raw = input("Введіть назву завдання (або 'q' для виходу): ")
        if raw.lower() == "q":
            break
        try:
            title = validate_title(raw)
            task = Task(title)
            tasks.append(task)
            print(f"Додано: {task}")
        except ValueError as e:
            print(f"Помилка: {e}")

    print("\nВаші завдання:")
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()
```

## Частина 7. `__all__` — публічний інтерфейс модуля

`__all__` — це список імен, які будуть імпортовані при `from module import *`. Також слугує документацією публічного API модуля.

```python
# geometry.py
__all__ = ["Circle", "Rectangle"]   # тільки ці імена є публічними


class Circle:
    def __init__(self, radius: float):
        self.radius = radius


class Rectangle:
    def __init__(self, w: float, h: float):
        self.w, self.h = w, h


class _InternalHelper:      # приватний: починається з _
    pass
```

```python
from geometry import *
# Імпортовано: Circle, Rectangle
# НЕ імпортовано: _InternalHelper (навіть без __all__)
```

## Зведений приклад: модуль зі стандартними модулями

```python
# report_generator.py
"""Генератор звітів — демонстрація роботи з модулями."""

import os
import json
from datetime import datetime
from pathlib import Path
from collections import Counter


def analyze_tasks(tasks: list[dict]) -> dict:
    """Аналізує список завдань та повертає статистику."""
    statuses = Counter(t["status"] for t in tasks)
    return {
        "total": len(tasks),
        "done": statuses.get("done", 0),
        "pending": statuses.get("pending", 0),
        "generated_at": datetime.now().isoformat(),
    }


def save_report(report: dict, output_dir: str = "reports") -> Path:
    """Зберігає звіт у JSON-файл."""
    path = Path(output_dir)
    path.mkdir(exist_ok=True)

    filename = path / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return filename


def main() -> None:
    tasks = [
        {"title": "Написати тести", "status": "done"},
        {"title": "Оновити документацію", "status": "pending"},
        {"title": "Зробити рефакторинг", "status": "done"},
        {"title": "Задеплоїти на сервер", "status": "pending"},
    ]

    report = analyze_tasks(tasks)
    saved_path = save_report(report)

    print(f"Звіт збережено: {saved_path}")
    print(f"Всього завдань: {report['total']}")
    print(f"Виконано: {report['done']}, В роботі: {report['pending']}")


if __name__ == "__main__":
    main()
```

## 📋 Підсумок заняття

| Концепція | Ключова ідея | Синтаксис |
|---|---|---|
| **Простір імен** | Словник ім'я → об'єкт | `globals()`, `locals()` |
| **LEGB** | Порядок пошуку: Local → Enclosing → Global → Built-in | — |
| **`global`** | Змінити глобальну змінну зсередини функції | `global x` |
| **`nonlocal`** | Змінити змінну enclosing-рівня | `nonlocal x` |
| **Модуль** | Файл `.py` з власним простором імен | `import module` |
| **`from ... import`** | Імпорт конкретних імен | `from math import sqrt` |
| **`__name__`** | `"__main__"` при прямому запуску | `if __name__ == "__main__":` |
| **Точка входу** | Код, що виконується лише при прямому запуску | `def main(): ...` |
| **Пакет** | Директорія з `__init__.py` | `import my_package.module` |
| **Відносний імпорт** | Імпорт між модулями одного пакету | `from . import module` |
| **`__all__`** | Публічний інтерфейс модуля | `__all__ = ["ClassA"]` |

## 🏠 Домашнє завдання

Перетворіть проєкт "To-Do" на повноцінний Python-пакет:

1. Створіть структуру директорій: `todo/models/`, `todo/storage/`, `todo/utils/`.
2. Перенесіть класи `Task`, `UrgentTask`, `RecurringTask` у `todo/models/task.py`.
3. Створіть `todo/utils/validators.py` з функцією `validate_title(title)`.
4. Налаштуйте `todo/models/__init__.py` — зробіть `Task` доступним через `from todo.models import Task`.
5. Напишіть `todo/main.py` з функцією `main()` та блоком `if __name__ == "__main__"`.
6. Перевірте, що `python todo/main.py` запускає програму, а `import todo` не виводить нічого зайвого.
