# Заняття 20. Основи функціонального програмування

**Олександр Панченко, ТОВ «Тренінг-центр КьюЕйЛайт»**

## Зв'язок із попередніми темами

На попередніх заняттях ми вивчили:

- **Заняття 13** — ітератори та генератори: `iter()`, `next()`, `yield`, генераторні вирази
- **Заняття 8** — серіалізацію та роботу з файлами
- **Заняття 5** — list comprehensions, цикли `for`/`while`

Функціональне програмування — це **ще один підхід до обробки даних**. Замість циклів — функції. Замість зміни стану — перетворення. Генераторні вирази, які ми вже знаємо, є частиною цієї парадигми.

Сьогодні ми навчимось:
- писати **чисті функції** (pure functions)
- використовувати **lambda** — анонімні функції
- застосовувати вбудовані функції вищого порядку: `filter()`, `map()`, `reduce()`

## 1. Що таке функціональне програмування

Функціональне програмування (ФП) — це **стиль написання коду**, де основним будівельним блоком є функція. Програма описує **що треба отримати**, а не **як це зробити крок за кроком**.

### Порівняння стилів

**Імперативний стиль** (як ми робили раніше):

```python
numbers = [1, 2, 3, 4, 5]
result = []
for n in numbers:
    if n % 2 == 0:
        result.append(n * n)
print(result)  # [4, 16]
```

**Функціональний стиль**:

```python
numbers = [1, 2, 3, 4, 5]
result = list(map(lambda n: n * n, filter(lambda n: n % 2 == 0, numbers)))
print(result)  # [4, 16]
```

**З list comprehension** (гібридний підхід, дуже популярний у Python):

```python
result = [n * n for n in numbers if n % 2 == 0]
print(result)  # [4, 16]
```

Усі три дають однаковий результат. Різниця — у **читабельності та підході**.

### Ключові принципи ФП

| Принцип | Опис |
|---|---|
| Чисті функції | Функція залежить лише від аргументів і не змінює нічого зовні |
| Незмінність даних | Замість зміни — створення нових об'єктів |
| Функції як значення | Функції можна передавати як аргументи, повертати як результат |
| Немає побічних ефектів | Функція не змінює глобальний стан, файли, базу даних тощо |

## 2. Чисті функції (Pure Functions)

### Що таке чиста функція

Чиста функція — це функція, яка:

1. **Завжди повертає однаковий результат** для однакових аргументів
2. **Не має побічних ефектів** — не змінює нічого поза собою

### Чиста vs нечиста функція

**Нечиста функція** (залежить від зовнішнього стану):

```python
discount = 0.1  # глобальна змінна

def calculate_price(price):
    return price * (1 - discount)  # залежить від зовнішньої змінної!

print(calculate_price(100))  # 90.0
discount = 0.2
print(calculate_price(100))  # 80.0 — інший результат для того самого аргументу!
```

**Чиста функція**:

```python
def calculate_price(price, discount):
    return price * (1 - discount)  # залежить лише від аргументів

print(calculate_price(100, 0.1))  # 90.0
print(calculate_price(100, 0.1))  # 90.0 — завжди однаково
```

### Побічні ефекти — що це

```python
# Нечиста — змінює переданий список
def add_tax_impure(prices):
    for i in range(len(prices)):
        prices[i] *= 1.2  # модифікуємо оригінал!
    return prices

original = [100, 200, 300]
result = add_tax_impure(original)
print(result)    # [120.0, 240.0, 360.0]
print(original)  # [120.0, 240.0, 360.0] — оригінал змінився!
```

```python
# Чиста — повертає новий список, оригінал не зачіпає
def add_tax_pure(prices):
    return [price * 1.2 for price in prices]

original = [100, 200, 300]
result = add_tax_pure(original)
print(result)    # [120.0, 240.0, 360.0]
print(original)  # [100, 200, 300] — оригінал збережено
```

### Чому чисті функції важливі

- **Передбачуваність** — легше зрозуміти, що робить функція
- **Тестованість** — не потрібно готувати зовнішній стан перед тестом
- **Паралельність** — чисті функції безпечні для багатопотокового виконання
- **Відлагоджування** — якщо результат неправильний, проблема точно у функції, а не "десь зовні"

> **Зв'язок із тестуванням (заняття 28):** чисті функції значно простіше покривати `pytest`-тестами. Тест для `calculate_price(100, 0.1)` виглядає як `assert calculate_price(100, 0.1) == 90.0` — і нічого більше не потрібно.

## 3. Lambda — анонімні функції

### Синтаксис

```python
lambda параметри: вираз
```

Lambda — це **функція без імені**, яка записується в один рядок. Вона може мати будь-яку кількість параметрів, але лише **один вираз** (не блок коду).

### Порівняння з def

```python
# Звичайна функція
def square(x):
    return x ** 2

# Те саме, але lambda
square_lambda = lambda x: x ** 2

print(square(5))        # 25
print(square_lambda(5)) # 25
```

```python
# Функція з двома параметрами
def add(a, b):
    return a + b

add_lambda = lambda a, b: a + b

print(add(3, 4))        # 7
print(add_lambda(3, 4)) # 7
```

### Коли використовувати lambda

Lambda корисна там, де функція потрібна **один раз** і коротка — зазвичай як аргумент до іншої функції:

```python
students = [
    {"name": "Олена", "grade": 92},
    {"name": "Богдан", "grade": 78},
    {"name": "Марина", "grade": 85},
]

# Сортування за оцінкою
sorted_students = sorted(students, key=lambda s: s["grade"])
for s in sorted_students:
    print(f"{s['name']}: {s['grade']}")
# Богдан: 78
# Марина: 85
# Олена: 92
```

> **Зв'язок із заняттям 5:** `sorted()` ми вже використовували. Параметр `key` — це функція, яка приймає елемент і повертає значення для порівняння. Раніше ми писали окрему `def`, тепер можемо обійтись lambda.

### Обмеження lambda

Lambda **не підходить**, якщо логіка складніша за один вираз:

```python
# Так не можна — lambda не підтримує if/else-блоки, цикли, return
# bad_lambda = lambda x: if x > 0: return x else: return -x  # SyntaxError

# Правильно — тернарний оператор (один вираз)
abs_value = lambda x: x if x >= 0 else -x
print(abs_value(-5))  # 5
print(abs_value(3))   # 3

# Або просто def, якщо логіка складніша
def absolute(x):
    if x >= 0:
        return x
    else:
        return -x
```

**Правило:** якщо lambda не поміщається в один рядок або потребує пояснення — краще написати `def`.

## 4. Функції вищого порядку

Функція вищого порядку — це функція, яка:
- **приймає іншу функцію як аргумент**, або
- **повертає функцію як результат**

Ми вже зустрічали це: `sorted(..., key=func)`, декоратори (заняття 22). Сьогодні — вбудовані: `filter()`, `map()`, `reduce()`.

## 5. filter() — фільтрація

### Синтаксис

```python
filter(функція, ітерований_об'єкт)
```

`filter()` повертає ітератор із тих елементів, для яких функція повернула `True`.

> **Зв'язок із заняттям 13:** `filter()` повертає **ітератор** (як генератор). Щоб отримати список — загортаємо в `list()`.

### Приклади

**Базовий приклад:**

```python
numbers = [1, -3, 5, -2, 8, -6, 4]

# Тільки додатні числа
positive = list(filter(lambda x: x > 0, numbers))
print(positive)  # [1, 5, 8, 4]

# Тільки парні
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)  # [-2, 8, -6, 4]
```

**Без lambda — із named функцією:**

```python
def is_adult(age):
    return age >= 18

ages = [12, 25, 16, 30, 17, 21]
adults = list(filter(is_adult, ages))
print(adults)  # [25, 30, 21]
```

**Фільтрація рядків:**

```python
words = ["Python", "", "клас", "   ", "функція", ""]

# Відфільтрувати порожні рядки та рядки з пробілів
non_empty = list(filter(lambda w: w.strip(), words))
print(non_empty)  # ['Python', 'клас', 'функція']
```

**Фільтрація словників:**

```python
products = [
    {"name": "Ноутбук", "price": 35000, "in_stock": True},
    {"name": "Миша", "price": 500, "in_stock": False},
    {"name": "Клавіатура", "price": 1200, "in_stock": True},
    {"name": "Монітор", "price": 12000, "in_stock": False},
]

# Тільки товари в наявності
available = list(filter(lambda p: p["in_stock"], products))
for p in available:
    print(f"{p['name']}: {p['price']} грн")
# Ноутбук: 35000 грн
# Клавіатура: 1200 грн

# Товари дешевше 2000 грн
affordable = list(filter(lambda p: p["price"] < 2000, products))
for p in affordable:
    print(p["name"])
# Миша
# Клавіатура
```

### filter() vs list comprehension

```python
numbers = range(1, 11)

# filter + lambda
squares_filter = list(filter(lambda x: x % 3 == 0, numbers))

# list comprehension
squares_lc = [x for x in numbers if x % 3 == 0]

print(squares_filter)  # [3, 6, 9]
print(squares_lc)      # [3, 6, 9]
```

**Обидва підходи рівнозначні.** У Python-спільноті list comprehension вважається більш "пітонічним" для простих випадків. `filter()` зручніша, коли функція вже є і її треба просто передати.

## 6. map() — перетворення

### Синтаксис

```python
map(функція, ітерований_об'єкт)
map(функція, ітерований_об'єкт_1, ітерований_об'єкт_2)
```

`map()` застосовує функцію до **кожного елемента** і повертає ітератор із результатів.

### Приклади

**Базовий приклад:**

```python
numbers = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x ** 2, numbers))
print(squares)  # [1, 4, 9, 16, 25]

doubled = list(map(lambda x: x * 2, numbers))
print(doubled)  # [2, 4, 6, 8, 10]
```

**Перетворення типів:**

```python
# Рядки → числа (типова задача при читанні CSV або введенні користувача)

numbers = list(map(int, raw_input))
print(numbers)       # [10, 25, 3, 17]
print(sum(numbers))  # 55

# Числа → рядки
prices = [100, 250, 75]
formatted = list(map(lambda p: f"{p} грн", prices))
print(formatted)  # ['100 грн', '250 грн', '75 грн']
```

> **Зв'язок із заняттям 17 (CSV):** при читанні CSV усі значення приходять рядками. `map(int, row)` або `map(float, row)` — типовий прийом для конвертації.

**map() з двома ітерабельними:**

```python
prices = [100, 200, 300]
quantities = [2, 5, 1]

totals = list(map(lambda p, q: p * q, prices, quantities))
print(totals)  # [200, 1000, 300]
```

**Обробка рядків:**

```python
names = ["  олена  ", "БОГДАН", "марина"]

# Нормалізація: обрізати пробіли + заголовна літера
normalized = list(map(lambda n: n.strip().capitalize(), names))
print(normalized)  # ['Олена', 'Богдан', 'Марина']
```

**map() з named функцією:**

```python
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

temperatures_c = [0, 20, 37, 100]
temperatures_f = list(map(celsius_to_fahrenheit, temperatures_c))
print(temperatures_f)  # [32.0, 68.0, 98.6, 212.0]
```

### Ланцюжок map + filter

```python
transactions = [-500, 200, -100, 800, -50, 1000]

# Тільки доходи (позитивні), конвертовані у долари (курс 40 грн/$)
usd_incomes = list(map(
    lambda t: t / 40,
    filter(lambda t: t > 0, transactions)
))
print(usd_incomes)  # [5.0, 20.0, 25.0]
```

## 7. reduce() — згортка

### Синтаксис

```python
from functools import reduce

reduce(функція, ітерований_об'єкт)
reduce(функція, ітерований_об'єкт, початкове_значення)
```

`reduce()` **згортає** послідовність до одного значення, послідовно застосовуючи функцію до двох аргументів.

> На відміну від `filter()` і `map()`, `reduce()` не є вбудованою — вона в модулі `functools`.

### Як працює reduce

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, numbers)
# Крок 1: acc=1, x=2 → 3
# Крок 2: acc=3, x=3 → 6
# Крок 3: acc=6, x=4 → 10
# Крок 4: acc=10, x=5 → 15
print(total)  # 15
```

Візуалізація:
```
[1, 2, 3, 4, 5]
 └─ acc=1
    acc = f(1, 2) = 3
    acc = f(3, 3) = 6
    acc = f(6, 4) = 10
    acc = f(10, 5) = 15
```

### Приклади

**Добуток:**

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
product = reduce(lambda acc, x: acc * x, numbers)
print(product)  # 120  (1 × 2 × 3 × 4 × 5)
```

**Максимальне значення без max():**

```python
from functools import reduce

numbers = [3, 7, 1, 9, 4, 6]
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)  # 9
```

**З початковим значенням:**

```python
from functools import reduce

# Початкове значення — важливо при роботі з порожніми списками
numbers = [10, 20, 30]
total_with_bonus = reduce(lambda acc, x: acc + x, numbers, 100)
# acc починається з 100
# 100 + 10 = 110
# 110 + 20 = 130
# 130 + 30 = 160
print(total_with_bonus)  # 160

# Без початкового значення — порожній список дасть помилку
empty = []
# reduce(lambda a, b: a + b, empty)  # TypeError!
safe_total = reduce(lambda a, b: a + b, empty, 0)
print(safe_total)  # 0
```

**Практична задача — підрахунок суми замовлення:**

```python
from functools import reduce

order_items = [
    {"name": "Піца", "price": 250, "qty": 2},
    {"name": "Кола", "price": 50, "qty": 3},
    {"name": "Салат", "price": 120, "qty": 1},
]

total = reduce(
    lambda acc, item: acc + item["price"] * item["qty"],
    order_items,
    0
)
print(f"Сума замовлення: {total} грн")  # Сума замовлення: 820 грн
```

**Об'єднання рядків:**

```python
from functools import reduce

words = ["Python", "це", "круто"]
sentence = reduce(lambda acc, w: acc + " " + w, words)
print(sentence)  # Python це круто

# Або простіше:
print(" ".join(words))  # Python це круто
# Тут join() — краще рішення, reduce() — навчальна демонстрація
```

## 8. Комбінування filter, map, reduce

Реальна сила ФП — у поєднанні цих функцій у **конвеєр обробки даних**:

### Приклад 1 — аналіз транзакцій

```python
from functools import reduce

transactions = [
    {"type": "income", "amount": 5000, "category": "salary"},
    {"type": "expense", "amount": 1200, "category": "rent"},
    {"type": "income", "amount": 800, "category": "freelance"},
    {"type": "expense", "amount": 350, "category": "food"},
    {"type": "expense", "amount": 200, "category": "transport"},
    {"type": "income", "amount": 1500, "category": "bonus"},
]

# Загальний дохід
total_income = reduce(
    lambda acc, t: acc + t["amount"],
    filter(lambda t: t["type"] == "income", transactions),
    0
)
print(f"Доходи: {total_income} грн")  # Доходи: 7300 грн

# Загальні витрати
total_expenses = reduce(
    lambda acc, t: acc + t["amount"],
    filter(lambda t: t["type"] == "expense", transactions),
    0
)
print(f"Витрати: {total_expenses} грн")  # Витрати: 1750 грн

# Баланс
balance = total_income - total_expenses
print(f"Баланс: {balance} грн")  # Баланс: 5550 грн
```

### Приклад 2 — обробка оцінок студентів

```python
from functools import reduce

students = [
    {"name": "Олена", "grades": [90, 85, 92, 88]},
    {"name": "Богдан", "grades": [70, 65, 80, 75]},
    {"name": "Марина", "grades": [95, 98, 92, 97]},
    {"name": "Тарас", "grades": [50, 55, 60, 45]},
]

# Додати середній бал кожному студенту
def add_average(student):
    avg = sum(student["grades"]) / len(student["grades"])
    return {**student, "average": round(avg, 1)}

students_with_avg = list(map(add_average, students))

# Відфільтрувати студентів, що склали (середній > 60)
passed = list(filter(lambda s: s["average"] > 60, students_with_avg))

# Вивести результати
for s in passed:
    print(f"{s['name']}: середній бал {s['average']}")
# Олена: середній бал 88.8
# Богдан: середній бал 72.5
# Марина: середній бал 95.5
```

### Приклад 3 — обробка CSV-даних

```python
from functools import reduce

# Типова ситуація: дані прийшли з CSV як список рядків
raw_data = [
    "Олена,developer,85000",
    "Богдан,designer,60000",
    "Марина,developer,92000",
    "Тарас,manager,75000",
    "Ірина,developer,78000",
]

# Розпарсити
employees = list(map(
    lambda row: dict(zip(["name", "role", "salary"], row.split(","))),
    raw_data
))

# Зарплату в числа
employees = list(map(
    lambda e: {**e, "salary": int(e["salary"])},
    employees
))

# Тільки розробники
developers = list(filter(lambda e: e["role"] == "developer", employees))

# Середня зарплата розробників
avg_salary = reduce(
    lambda acc, e: acc + e["salary"],
    developers,
    0
) / len(developers)

print(f"Середня зарплата розробника: {avg_salary:.0f} грн")
# Середня зарплата розробника: 85000 грн
```

## 9. Порівняння підходів

| Задача | Цикл for | List comprehension | map/filter/reduce |
|---|---|---|---|
| Перетворити елементи | `for x in lst: result.append(f(x))` | `[f(x) for x in lst]` | `list(map(f, lst))` |
| Відфільтрувати | `for x in lst: if cond: result.append(x)` | `[x for x in lst if cond]` | `list(filter(cond, lst))` |
| Підсумувати | `total = 0; for x in lst: total += x` | `sum(lst)` | `reduce(lambda a,b: a+b, lst)` |

**Що краще?**

- **List comprehension** — найчастіше найкращий вибір у Python (читабельно + "пітонічно")
- **map/filter** — зручні, коли функція вже є і її треба передати
- **reduce** — корисна для нестандартних операцій "згортки" (не sum, не max)
- **for** — коли логіка складна і не вкладається в один вираз

## Підсумок заняття

| Концепція | Суть | Коли використовувати |
|---|---|---|
| **Чиста функція** | Результат залежить лише від аргументів, без побічних ефектів | Завжди, коли можливо |
| **lambda** | Анонімна функція в один рядок | Короткі функції як аргументи |
| **filter()** | Залишає елементи, де функція → True | Вибірка з колекції |
| **map()** | Перетворює кожен елемент | Обробка/конвертація колекції |
| **reduce()** | Згортає колекцію в одне значення | Нестандартна агрегація |

### Ключові висновки

- Функціональний підхід робить код **коротшим і передбачуванішим**
- Python підтримує ФП, але не є чисто функціональною мовою — використовуйте там, де це покращує читабельність
- `filter()` і `map()` повертають **ітератори** — якщо потрібен список, загортайте в `list()`
- `reduce()` потребує `from functools import reduce`
- List comprehensions часто читабельніші за `map` + `filter` для простих випадків

### Зв'язок із наступними темами

- **Заняття 21** — практика ФП: пошук простих чисел, паліндромів, видалення викидів
- **Заняття 22** — декоратори: функції, що приймають і повертають функції (функції вищого порядку в дії)
- **Заняття 28** — тестування: чисті функції легко тестувати через `pytest`
