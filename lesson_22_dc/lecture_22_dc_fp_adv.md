# Заняття 22. Dataclass + практика функціонального програмування

## Мета заняття

На цьому занятті ми познайомимось із модулем `dataclasses`, який дозволяє значно скоротити кількість шаблонного коду під час створення класів, а також закріпимо навички функціонального програмування на реальних задачах обробки даних.

Після заняття ви зможете:

* створювати класи за допомогою `@dataclass`;
* використовувати автоматично згенеровані конструктори та методи;
* обробляти колекції даних у функціональному стилі;
* знаходити прості числа та паліндроми;
* видаляти викиди з наборів даних;
* перевіряти коректність ідентифікаторів;
* реалізовувати власні функціональні інструменти.

# Частина 1. Dataclass

## Проблема звичайних класів

Припустимо, нам потрібно створити клас для опису студента.

```python
class Student:

    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score
```

Навіть для простого класу доводиться писати конструктор вручну.

Якщо потрібно красиво друкувати об'єкти або порівнювати їх між собою, коду стає ще більше.

## Dataclass

Починаючи з Python 3.7 з'явився модуль `dataclasses`.

Він автоматично створює:

* `__init__()`
* `__repr__()`
* `__eq__()`

та інші методи.

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    score: float
```

Тепер можна створювати об'єкти:

```python
student = Student("Alex", 25, 95.5)

print(student)
```

Результат:

```python
Student(name='Alex', age=25, score=95.5)
```

## Порівняння об'єктів

Без dataclass:

```python
s1 == s2
```

порівнює адреси в пам'яті.

З dataclass:

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int

s1 = Student("Alex", 25)
s2 = Student("Alex", 25)

print(s1 == s2)
```

Результат:

```python
True
```

## Значення за замовчуванням

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    active: bool = True
```

```python
user = User("John")

print(user)
```

Результат:

```python
User(name='John', active=True)
```

## Метод `__post_init__`

Іноді потрібно виконати додаткову логіку після створення об'єкта.

```python
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    salary: int

    def __post_init__(self):
        if self.salary < 0:
            raise ValueError("Salary cannot be negative")
```

```python
employee = Employee("Bob", 1000)
```

## Dataclass у реальному житті

Часто використовується для:

* конфігурацій;
* DTO (Data Transfer Objects);
* API-відповідей;
* записів із БД;
* структур даних для обробки CSV та JSON.

Приклад:

```python
from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float
```

```python
products = [
    Product(1, "Laptop", 1200),
    Product(2, "Mouse", 25),
    Product(3, "Keyboard", 50)
]
```

# Частина 2. Функціональна обробка даних

На попередніх заняттях ми розглядали:

* `lambda`
* `filter`
* `map`
* `reduce`

Сьогодні використаємо їх для розв'язання типових задач.

# Практика 1. Пошук простих чисел

## Що таке просте число

Просте число ділиться лише на:

* 1
* саме на себе

Наприклад:

```python
2, 3, 5, 7, 11, 13
```

## Функція перевірки

```python
def is_prime(number):

    if number < 2:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True
```

## Використання filter

```python
numbers = range(1, 51)

primes = list(filter(is_prime, numbers))

print(primes)
```

Результат:

```python
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

## Варіант із lambda

```python
numbers = range(1, 51)

primes = list(
    filter(
        lambda n: n > 1 and all(
            n % d != 0
            for d in range(2, int(n ** 0.5) + 1)
        ),
        numbers
    )
)

print(primes)
```

# Практика 2. Пошук паліндромів

## Що таке паліндром

Паліндром читається однаково зліва направо і справа наліво.

Приклади:

```python
level
radar
madam
anna
```

## Функція перевірки

```python
def is_palindrome(word):
    return word == word[::-1]
```

## Використання filter

```python
words = [
    "radar",
    "python",
    "anna",
    "car",
    "level",
    "hello"
]

result = list(filter(is_palindrome, words))

print(result)
```

Результат:

```python
['radar', 'anna', 'level']
```

## Паліндроми серед чисел

```python
numbers = range(100, 200)

palindromes = list(
    filter(
        lambda x: str(x) == str(x)[::-1],
        numbers
    )
)

print(palindromes)
```

# Практика 3. Видалення викидів

## Що таке викид

Викид (outlier) — значення, яке сильно відрізняється від інших.

Наприклад:

```python
[10, 12, 13, 11, 15, 14, 300]
```

Число 300 виглядає підозріло.

## Простий спосіб

Обчислимо середнє значення.

```python
numbers = [10, 12, 13, 11, 15, 14, 300]

average = sum(numbers) / len(numbers)

print(average)
```

## Видалення підозрілих значень

```python
numbers = [10, 12, 13, 11, 15, 14, 300]

average = sum(numbers) / len(numbers)

filtered = list(
    filter(
        lambda x: x < average * 2,
        numbers
    )
)

print(filtered)
```

Результат:

```python
[10, 12, 13, 11, 15, 14]
```

## Більш реалістичний приклад

```python
temperatures = [
    22, 23, 21, 24,
    25, 23, 22, 120
]

clean_data = list(
    filter(
        lambda t: 0 <= t <= 50,
        temperatures
    )
)

print(clean_data)
```

Результат:

```python
[22, 23, 21, 24, 25, 23, 22]
```

# Практика 4. Перевірка ідентифікаторів

У системах часто потрібно перевіряти:

* ID користувачів;
* номери замовлень;
* артикул товару;
* коди доступу.

## Завдання

Залишити лише числові ID.

```python
ids = [
    "12345",
    "ABC12",
    "99999",
    "TEST",
    "54321"
]
```

## Використання filter

```python
valid_ids = list(
    filter(
        lambda x: x.isdigit(),
        ids
    )
)

print(valid_ids)
```

Результат:

```python
['12345', '99999', '54321']
```

## Перевірка довжини

```python
ids = [
    "12345",
    "123",
    "ABCDE",
    "99999"
]

valid_ids = list(
    filter(
        lambda x: x.isdigit() and len(x) == 5,
        ids
    )
)

print(valid_ids)
```

Результат:

```python
['12345', '99999']
```

# Практика 5. Реалізація map через reduce

## Як працює map

```python
numbers = [1, 2, 3, 4]

result = list(
    map(
        lambda x: x * 2,
        numbers
    )
)

print(result)
```

Результат:

```python
[2, 4, 6, 8]
```

## Реалізація через reduce

```python
from functools import reduce

numbers = [1, 2, 3, 4]

result = reduce(
    lambda acc, x: acc + [x * 2],
    numbers,
    []
)

print(result)
```

Результат:

```python
[2, 4, 6, 8]
```

## Створимо власний map

```python
from functools import reduce


def my_map(func, iterable):

    return reduce(
        lambda acc, x: acc + [func(x)],
        iterable,
        []
    )
```

## Використання

```python
numbers = [1, 2, 3, 4]

result = my_map(
    lambda x: x ** 2,
    numbers
)

print(result)
```

Результат:

```python
[1, 4, 9, 16]
```

# Комплексний приклад

Нехай ми отримали список студентів.

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    score: int
```

```python
students = [
    Student("Alex", 90),
    Student("John", 75),
    Student("Kate", 95),
    Student("Bob", 60)
]
```

Отримаємо список оцінок:

```python
scores = list(
    map(
        lambda student: student.score,
        students
    )
)

print(scores)
```

Результат:

```python
[90, 75, 95, 60]
```

Знайдемо студентів із балом понад 80:

```python
best_students = list(
    filter(
        lambda student: student.score > 80,
        students
    )
)

print(best_students)
```

# Підсумок

На цьому занятті ми:

* познайомилися з `@dataclass`;
* навчилися створювати класи без зайвого шаблонного коду;
* використовували `filter`, `map` та `reduce` для обробки даних;
* знаходили прості числа;
* шукали паліндроми;
* видаляли викиди з наборів даних;
* перевіряли коректність ідентифікаторів;
* реалізували власний аналог `map()` через `reduce()`.

`dataclass` сьогодні активно використовується в сучасних Python-проєктах, а функціональний підхід дозволяє писати короткий, читабельний та легко тестований код.
