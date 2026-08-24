# Заняття 11. Спадкування та поліморфізм

**Курс:** Програмування Python | QALight  
**Тривалість:** 2 години (0,5 год. теорія + 1,5 год. практика)

## 🎯 Мета заняття

Зрозуміти механізми повторного використання коду через спадкування та композицію, навчитися будувати ієрархії класів, розібратися з поліморфізмом і статичними методами.

## Частина 1. Спадкування

### Що таке спадкування?

Спадкування — це механізм ООП, завдяки якому один клас (дочірній, або підклас) отримує атрибути та методи іншого класу (батьківського, або суперкласу). Це дозволяє повторно використовувати код і будувати логічні ієрархії об'єктів.

**Синтаксис:**

```python
class Батьківський:
    pass

class Дочірній(Батьківський):
    pass
```

### Приклад: ієрархія тварин

```python
class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def speak(self) -> str:
        return f"{self.name} каже щось невизначене"

    def describe(self) -> str:
        return f"Мене звати {self.name}, мені {self.age} років"


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} каже: Гав!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} каже: Няв!"


dog = Dog("Рекс", 3)
cat = Cat("Мурчик", 5)

print(dog.describe())   # Мене звати Рекс, мені 3 років
print(dog.speak())      # Рекс каже: Гав!
print(cat.speak())      # Мурчик каже: Няв!
```

Клас `Dog` не визначає `__init__` і `describe` — він їх **успадковує** від `Animal`. Метод `speak` — **перевизначений** (overridden).

### Функція `super()`

`super()` дозволяє викликати метод батьківського класу з дочірнього. Це особливо корисно, коли потрібно розширити, а не повністю замінити поведінку батька.

```python
class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class Dog(Animal):
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)   # викликаємо __init__ батька
        self.breed = breed            # додаємо власний атрибут

    def describe(self) -> str:
        return f"{self.name} ({self.breed}), вік: {self.age}"


dog = Dog("Рекс", 3, "Лабрадор")
print(dog.describe())  # Рекс (Лабрадор), вік: 3
```

> 💡 **Правило:** якщо дочірній клас визначає `__init__`, завжди викликайте `super().__init__()`, щоб не втратити ініціалізацію батька.

## Частина 2. Композиція

### Спадкування vs Композиція

Крім спадкування, існує ще один спосіб повторного використання коду — **композиція**: один клас містить екземпляр іншого як атрибут.

| Критерій | Спадкування | Композиція |
|---|---|---|
| Відношення | "є" (is-a) | "має" (has-a) |
| Гнучкість | Нижча | Вища |
| Зв'язок | Жорсткий | Слабкий |
| Приклад | `Dog` є `Animal` | `Car` має `Engine` |

### Приклад: автомобіль і двигун

```python
class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower

    def start(self) -> str:
        return f"Двигун {self.horsepower} к.с. запущено"

    def stop(self) -> str:
        return "Двигун зупинено"


class Car:
    def __init__(self, brand: str, horsepower: int):
        self.brand = brand
        self.engine = Engine(horsepower)  # композиція

    def drive(self) -> str:
        engine_status = self.engine.start()
        return f"{self.brand}: {engine_status}"


car = Car("Toyota", 150)
print(car.drive())       # Toyota: Двигун 150 к.с. запущено
print(car.engine.stop()) # Двигун зупинено
```

### Коли що обирати?

- **Спадкування** підходить, коли між класами є чітке відношення «є видом чогось» (Dog is-a Animal).
- **Композиція** підходить, коли об'єкт «складається з» інших об'єктів (Car has-a Engine). Вона гнучкіша: можна замінити двигун без зміни класу `Car`.

> 💡 **Принцип:** "Надавай перевагу композиції над спадкуванням" (Favor Composition over Inheritance) — класична порада з книги Gang of Four.

## Частина 3. Множинне спадкування

Python дозволяє дочірньому класу успадковувати одразу від **кількох** батьківських класів.

```python
class Flyable:
    def fly(self) -> str:
        return f"{self.__class__.__name__} летить"


class Swimmable:
    def swim(self) -> str:
        return f"{self.__class__.__name__} пливе"


class Duck(Flyable, Swimmable):
    def quack(self) -> str:
        return "Кря!"


duck = Duck()
print(duck.fly())    # Duck летить
print(duck.swim())   # Duck пливе
print(duck.quack())  # Кря!
```

### Проблема «ромба» (Diamond Problem)

Складнощі виникають, коли два батьки мають спільного предка і обидва перевизначають один і той самий метод.

```python
class A:
    def hello(self):
        return "Привіт від A"

class B(A):
    def hello(self):
        return "Привіт від B"

class C(A):
    def hello(self):
        return "Привіт від C"

class D(B, C):
    pass

d = D()
print(d.hello())  # Привіт від B — але чому саме B?
```

Яке `hello()` викличеться? Відповідає на це **MRO**.

## Частина 4. MRO — Method Resolution Order

**MRO** (порядок розв'язання методів) — це алгоритм, за яким Python шукає метод у ланцюжку спадкування. Використовується **алгоритм C3-лінеаризації**.

```python
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# Або у зручнішому форматі:
print([cls.__name__ for cls in D.__mro__])
# ['D', 'B', 'C', 'A', 'object']
```

**Правило пошуку:** Python іде зліва направо по списку `__mro__` і викликає перший знайдений метод.

Тому `d.hello()` → шукаємо в `D` (немає) → шукаємо в `B` (є!) → повертаємо `"Привіт від B"`.

### `super()` у множинному спадкуванні

`super()` теж дотримується MRO і викликає наступний клас у ланцюжку, а не обов'язково прямого батька:

```python
class A:
    def hello(self):
        return "A"

class B(A):
    def hello(self):
        return "B -> " + super().hello()

class C(A):
    def hello(self):
        return "C -> " + super().hello()

class D(B, C):
    def hello(self):
        return "D -> " + super().hello()

print(D().hello())  # D -> B -> C -> A
```

MRO для `D`: `[D, B, C, A, object]` — `super()` в кожному класі викликає наступний у цьому списку.

## Частина 5. Поліморфізм

### Що таке поліморфізм?

**Поліморфізм** (від грец. "багато форм") — здатність об'єктів різних класів відповідати на однаковий інтерфейс (виклик однакового методу), але по-різному.

```python
class Shape:
    def area(self) -> float:
        raise NotImplementedError("Підклас має реалізувати area()")


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height


# Поліморфний код: не знає конкретний тип, але викликає area()
shapes: list[Shape] = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 8),
]

for shape in shapes:
    print(f"{shape.__class__.__name__}: площа = {shape.area():.2f}")

# Circle: площа = 78.54
# Rectangle: площа = 24.00
# Triangle: площа = 12.00
```

### Duck Typing

Python реалізує поліморфізм через **duck typing**: "якщо об'єкт ходить як качка і крякає як качка — він і є качкою". Не потрібна явна ієрархія спадкування:

```python
class Dog:
    def speak(self) -> str:
        return "Гав!"

class Cat:
    def speak(self) -> str:
        return "Няв!"

class Robot:
    def speak(self) -> str:
        return "Біп-буп!"


def make_noise(entity) -> None:  # не вимагає конкретного типу
    print(entity.speak())


for creature in [Dog(), Cat(), Robot()]:
    make_noise(creature)

# Гав!
# Няв!
# Біп-буп!
```

> 💡 `Dog`, `Cat` і `Robot` не пов'язані спадкуванням, але всі мають метод `speak()` — цього достатньо для поліморфного використання.

## Частина 6. Статичні методи

### Три типи методів у класі

| Тип | Декоратор | Перший аргумент | Доступ до |
|---|---|---|---|
| Метод екземпляра | *(немає)* | `self` | атрибутів екземпляра та класу |
| Метод класу | `@classmethod` | `cls` | атрибутів класу, не екземпляра |
| Статичний метод | `@staticmethod` | *(немає)* | нічого, це звичайна функція в класі |

### Приклад: `@staticmethod`

Статичний метод не отримує ні `self`, ні `cls`. Це звичайна функція, розміщена всередині класу для логічного групування.

```python
class MathHelper:
    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def is_even(n: int) -> bool:
        return n % 2 == 0


# Можна викликати і через клас, і через екземпляр
print(MathHelper.add(3, 5))       # 8
print(MathHelper.is_even(4))      # True

helper = MathHelper()
print(helper.is_even(7))          # False
```

### Приклад: `@classmethod`

Метод класу отримує `cls` — посилання на сам клас. Часто використовується як **альтернативний конструктор**:

```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, data: str) -> "Person":
        """Альтернативний конструктор: 'Іван:30' → Person"""
        name, age = data.split(":")
        return cls(name, int(age))

    @classmethod
    def from_birth_year(cls, name: str, birth_year: int) -> "Person":
        """Альтернативний конструктор через рік народження"""
        from datetime import datetime
        age = datetime.now().year - birth_year
        return cls(name, age)

    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age})"


p1 = Person("Іван", 30)
p2 = Person.from_string("Марія:25")
p3 = Person.from_birth_year("Олег", 1995)

print(p1)  # Person(name='Іван', age=30)
print(p2)  # Person(name='Марія', age=25)
print(p3)  # Person(name='Олег', age=~30)
```

## Зведений приклад: усе разом

Проєкт «To-Do» — розширення структури класів із попереднього заняття.

```python
from datetime import datetime


class Task:
    """Базовий клас завдання"""

    task_count = 0  # атрибут класу

    def __init__(self, title: str, description: str = ""):
        Task.task_count += 1
        self.id = Task.task_count
        self.title = title
        self.description = description
        self.created_at = datetime.now()
        self.is_done = False

    def complete(self) -> None:
        self.is_done = True

    def status(self) -> str:
        return "✅" if self.is_done else "⏳"

    def __repr__(self) -> str:
        return f"[{self.status()}] #{self.id} {self.title}"

    @classmethod
    def get_count(cls) -> int:
        return cls.task_count

    @staticmethod
    def validate_title(title: str) -> bool:
        return bool(title) and len(title) <= 100


class UrgentTask(Task):
    """Термінове завдання з дедлайном"""

    def __init__(self, title: str, deadline: datetime, description: str = ""):
        super().__init__(title, description)
        self.deadline = deadline

    def is_overdue(self) -> bool:
        return datetime.now() > self.deadline and not self.is_done

    def status(self) -> str:  # поліморфізм
        if self.is_overdue():
            return "🔥"
        return super().status()


class RecurringTask(Task):
    """Завдання, що повторюється"""

    def __init__(self, title: str, interval_days: int, description: str = ""):
        super().__init__(title, description)
        self.interval_days = interval_days

    def status(self) -> str:  # поліморфізм
        return f"🔄({self.interval_days}д)"


# --- Використання ---
tasks: list[Task] = [
    Task("Прочитати документацію"),
    UrgentTask("Здати звіт", datetime(2024, 1, 1)),  # минулий дедлайн
    RecurringTask("Щоденний стендап", 1),
]

for task in tasks:
    print(task)  # поліморфний виклик __repr__ і status()

print(f"\nВсього завдань створено: {Task.get_count()}")
print(f"Валідна назва 'Test': {Task.validate_title('Test')}")
print(f"Валідна назва '': {Task.validate_title('')}")
```

**Вивід:**
```
[⏳] #1 Прочитати документацію
[🔥] #2 Здати звіт
[🔄(1д)] #3 Щоденний стендап

Всього завдань створено: 3
Валідна назва 'Test': True
Валідна назва '': False
```

## 📋 Підсумок заняття

| Концепція | Ключова ідея | Синтаксис |
|---|---|---|
| **Спадкування** | Дочірній клас отримує код батька | `class Child(Parent):` |
| **`super()`** | Виклик методу батьківського класу | `super().__init__(...)` |
| **Перевизначення** | Дочірній клас замінює метод батька | Визначити метод з тим самим ім'ям |
| **Композиція** | Клас містить екземпляр іншого класу | `self.engine = Engine()` |
| **Множинне спадкування** | Успадкування від кількох батьків | `class D(B, C):` |
| **MRO** | Порядок пошуку методів | `ClassName.__mro__` |
| **Поліморфізм** | Різні класи — однаковий інтерфейс | Перевизначення методу |
| **`@staticmethod`** | Функція в класі без `self`/`cls` | `@staticmethod` |
| **`@classmethod`** | Метод, що отримує `cls` | `@classmethod` |

## 🏠 Домашнє завдання

Розширте проєкт "To-Do" з попереднього заняття:

1. Створіть ще один підклас `Task`, наприклад `TeamTask` (завдання з відповідальним виконавцем — `assignee: str`).
2. Перевизначте метод `__repr__` у новому підкласі, щоб він виводив ім'я виконавця.
3. Додайте `@staticmethod` метод `create_sample()` у клас `Task`, який повертає екземпляр з демонстраційними даними.
4. Перевірте `Task.__mro__` і поясніть отриманий результат у коментарі до коду.
5. Створіть список із завданнями різних типів і виведіть їх у циклі — переконайтеся, що поліморфізм працює.
