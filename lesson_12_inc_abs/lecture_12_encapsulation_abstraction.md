# Заняття 12. Інкапсуляція та абстракція

**Курс:** Програмування Python | QALight  
**Тривалість:** 2 години (0,5 год. теорія + 1,5 год. практика)

## 🎯 Мета заняття

Зрозуміти принципи інкапсуляції та абстракції: навчитися захищати внутрішній стан об'єктів, будувати валідацію даних через властивості, а також проєктувати спільний інтерфейс для ієрархій класів за допомогою абстрактних класів.

## Частина 1. Інкапсуляція

### Що таке інкапсуляція?

**Інкапсуляція** — принцип ООП, за яким внутрішній стан об'єкта прихований від зовнішнього коду. Зовнішній світ взаємодіє з об'єктом лише через чітко визначений інтерфейс (методи), а не напряму через атрибути.

Навіщо це потрібно:
- захист даних від некоректної зміни ззовні;
- можливість змінити внутрішню реалізацію, не зачіпаючи зовнішній код;
- централізована валідація — перевірка даних в одному місці.

### Рівні доступу в Python

Python не має суворих модифікаторів доступу (як `private` у Java чи C++), але існують **угоди про іменування**:

| Іменування | Рівень | Що означає |
|---|---|---|
| `name` | Публічний | Доступний звідусіль |
| `_name` | Захищений | Угода: "не чіпай ззовні" |
| `__name` | Приватний | Name mangling: реально захищений |

### Публічні атрибути (без захисту)

```python
class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.balance = balance  # публічний — нічого не заважає зламати


account = BankAccount("Іван", 1000)
account.balance = -99999  # ніхто не зупинить!
print(account.balance)    # -99999 — катастрофа
```

Проблема очевидна: будь-який код може встановити будь-яке значення. Інкапсуляція вирішує це.

### Захищені атрибути: одне підкреслення `_`

Одне підкреслення — це **угода між розробниками**: "цей атрибут внутрішній, не використовуй його ззовні". Python технічно не забороняє доступ, але добросовісний код його уникає.

```python
class Person:
    def __init__(self, name: str, age: int):
        self._name = name   # захищений
        self._age = age     # захищений

    def introduce(self) -> str:
        return f"Мене звати {self._name}, мені {self._age} років"


p = Person("Марія", 25)
print(p.introduce())     # Мене звати Марія, мені 25 років

# Технічно можна, але не варто:
print(p._name)           # Марія — працює, але порушує угоду
p._age = -5              # Теж працює, але це поганий стиль
```

Захищені атрибути часто використовуються в базових класах, де дочірні класи мають до них доступ, але зовнішній код — ні.

### Приватні атрибути: подвійне підкреслення `__`

Подвійне підкреслення вмикає механізм **name mangling** (спотворення імені): Python автоматично перейменовує `__name` на `_ClassName__name`. Це реальний технічний захист.

```python
class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.__balance = balance  # приватний

    def get_balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сума поповнення має бути позитивною")
        self.__balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сума зняття має бути позитивною")
        if amount > self.__balance:
            raise ValueError("Недостатньо коштів")
        self.__balance -= amount


account = BankAccount("Іван", 1000)
account.deposit(500)
account.withdraw(200)
print(account.get_balance())   # 1300

# Прямий доступ — помилка:
# print(account.__balance)     # AttributeError!

# Але через name mangling — технічно можливо (не робіть так):
print(account._BankAccount__balance)  # 1300
```

> 💡 Name mangling існує не для безпеки від зловмисників, а для захисту від **випадкового** конфлікту імен у підкласах.

## Частина 2. Властивості: `@property`

### Проблема геттерів і сеттерів

У Java прийнято писати `getName()` / `setName()`. У Python для цього є елегантніший інструмент — декоратор `@property`, який дозволяє звертатися до методу як до атрибута.

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Геттер: читаємо значення"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Сеттер: валідація при записі"""
        if value < -273.15:
            raise ValueError(f"Температура {value}°C нижча за абсолютний нуль")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Обчислювана властивість (лише читання)"""
        return self._celsius * 9 / 5 + 32


t = Temperature(100)
print(t.celsius)      # 100     — виглядає як атрибут, але це метод
print(t.fahrenheit)   # 212.0   — обчислюється динамічно

t.celsius = 0
print(t.fahrenheit)   # 32.0

t.celsius = -300      # ValueError: Температура -300°C нижча за абсолютний нуль
```

### Властивість лише для читання

Якщо визначити лише `@property` без `.setter` — атрибут стане read-only:

```python
class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Радіус має бути позитивним")
        self._radius = value

    @property
    def area(self) -> float:
        import math
        return math.pi * self._radius ** 2   # read-only: немає setter

    @property
    def diameter(self) -> float:
        return self._radius * 2              # read-only: немає setter


c = Circle(5)
print(c.area)        # 78.54
print(c.diameter)    # 10

c.radius = 10
print(c.area)        # 314.16

c.area = 100         # AttributeError: can't set attribute
```

## Частина 3. Валідація даних

### Централізована валідація через `@property`

Одна з головних переваг інкапсуляції — перевірка коректності даних відбувається в одному місці. Якщо правило змінюється, оновлюємо лише клас.

```python
class Employee:
    MIN_SALARY = 7000   # мінімальна зарплата (грн)

    def __init__(self, name: str, salary: float, age: int):
        self.name = name        # публічний (не потребує валідації)
        self.salary = salary    # через setter
        self.age = age          # через setter

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Зарплата має бути числом")
        if value < self.MIN_SALARY:
            raise ValueError(f"Зарплата не може бути меншою за {self.MIN_SALARY} грн")
        self._salary = float(value)

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Вік має бути цілим числом")
        if not (18 <= value <= 65):
            raise ValueError("Вік працівника має бути від 18 до 65 років")
        self._age = value

    def __repr__(self) -> str:
        return f"Employee(name='{self.name}', salary={self._salary}, age={self._age})"


emp = Employee("Олена", 15000, 30)
print(emp)                  # Employee(name='Олена', salary=15000.0, age=30)

emp.salary = 20000          # OK
emp.salary = 5000           # ValueError: Зарплата не може бути меншою за 7000 грн
```

## Частина 4. Приватні методи

Так само, як і атрибути, методи можуть бути приватними — якщо вони є допоміжними і не повинні викликатися ззовні.

```python
class PasswordManager:
    def __init__(self, password: str):
        self.__password_hash = self.__hash(password)

    def __hash(self, password: str) -> int:
        """Приватний метод — внутрішня деталь реалізації"""
        return hash(password + "salt_secret")

    def check_password(self, password: str) -> bool:
        """Публічний метод — єдиний спосіб взаємодії ззовні"""
        return self.__hash(password) == self.__password_hash

    def change_password(self, old_password: str, new_password: str) -> None:
        if not self.check_password(old_password):
            raise PermissionError("Невірний поточний пароль")
        if len(new_password) < 8:
            raise ValueError("Новий пароль занадто короткий")
        self.__password_hash = self.__hash(new_password)
        print("Пароль успішно змінено")


pm = PasswordManager("secret123")
print(pm.check_password("secret123"))   # True
print(pm.check_password("wrong"))       # False

pm.change_password("secret123", "newpass456")  # Пароль успішно змінено

# pm.__hash("test")  # AttributeError — приватний метод недоступний
```

> 💡 Приватні методи — це внутрішні деталі реалізації. Вони можуть змінюватися без попередження, тому зовнішній код не повинен від них залежати.

## Частина 5. Абстракція

### Що таке абстракція?

**Абстракція** — принцип ООП, за яким ми визначаємо **що** об'єкт повинен вміти робити, але не **як** саме. Абстракція задає спільний інтерфейс для групи класів.

Уявіть розетку в стіні: ви знаєте, що в неї можна вставити вилку і отримати електрику. Вам не потрібно знати, як влаштована електромережа. Розетка — це абстракція.

### Проблема без абстракції

```python
class PDFReport:
    def generate(self): ...

class ExcelReport:
    def build(self): ...     # різна назва методу!

class HTMLReport:
    def render(self): ...    # ще одна назва!


def create_report(report):
    # Що викликати? generate? build? render?
    # Немає гарантій, що метод взагалі існує
    pass
```

Без спільного інтерфейсу — хаос. Абстрактний клас вирішує це.

## Частина 6. Модуль `abc`

### Абстрактні класи (`ABC`)

Абстрактний клас — це клас, який:
- **не можна** інстанціювати напряму;
- визначає **обов'язковий інтерфейс** для підкласів;
- підкласи **зобов'язані** реалізувати всі абстрактні методи.

```python
from abc import ABC, abstractmethod


class Report(ABC):
    """Абстрактний базовий клас для всіх звітів"""

    def __init__(self, title: str):
        self.title = title

    @abstractmethod
    def generate(self) -> str:
        """Кожен підклас зобов'язаний реалізувати цей метод"""
        pass

    @abstractmethod
    def save(self, filepath: str) -> None:
        """Зберегти звіт у файл"""
        pass

    def preview(self) -> str:
        """Конкретний метод — спільний для всіх підкласів"""
        return f"[Попередній перегляд: {self.title}]"


# Report("Звіт")  # TypeError: Can't instantiate abstract class
```

### Реалізація підкласів

```python
class PDFReport(Report):
    def generate(self) -> str:
        return f"PDF звіт: {self.title}"

    def save(self, filepath: str) -> None:
        print(f"Збереження PDF у {filepath}")


class ExcelReport(Report):
    def generate(self) -> str:
        return f"Excel звіт: {self.title}"

    def save(self, filepath: str) -> None:
        print(f"Збереження Excel у {filepath}")


# Поліморфне використання:
reports: list[Report] = [
    PDFReport("Квартальний звіт"),
    ExcelReport("Фінансовий звіт"),
]

for report in reports:
    print(report.generate())          # кожен по-своєму
    print(report.preview())           # спільний метод з ABC
    report.save("/tmp/report")

# PDF звіт: Квартальний звіт
# [Попередній перегляд: Квартальний звіт]
# Збереження PDF у /tmp/report
# Excel звіт: Фінансовий звіт
# ...
```

### Неповна реалізація — помилка

Python не дасть створити екземпляр підкласу, якщо не реалізовані всі абстрактні методи:

```python
class IncompleteReport(Report):
    def generate(self) -> str:
        return "Щось"
    # save() не реалізовано!


IncompleteReport("Тест")
# TypeError: Can't instantiate abstract class IncompleteReport
# with abstract method save
```

### `@abstractmethod` з реалізацією

Абстрактний метод може мати реалізацію за замовчуванням. Підклас зобов'язаний перевизначити його, але може викликати батьківську версію через `super()`:

```python
from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def speak(self) -> str:
        return f"{self.name} видає звук"   # базова реалізація

    def describe(self) -> str:
        return f"Я {self.name}: {self.speak()}"


class Dog(Animal):
    def speak(self) -> str:
        base = super().speak()             # викликаємо базову
        return f"{base} — Гав!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} каже: Няв!"   # повністю замінюємо


print(Dog("Рекс").describe())   # Я Рекс: Рекс видає звук — Гав!
print(Cat("Мурко").describe())  # Я Мурко: Мурко каже: Няв!
```

### Абстрактні властивості

`@abstractmethod` можна комбінувати з `@property`:

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    @property
    @abstractmethod
    def area(self) -> float:
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self) -> str:
        return (
            f"{self.__class__.__name__}: "
            f"площа={self.area:.2f}, периметр={self.perimeter:.2f}"
        )


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    @property
    def area(self) -> float:
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        return 2 * (self._width + self._height)


class Circle(Shape):
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def area(self) -> float:
        import math
        return math.pi * self._radius ** 2

    @property
    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self._radius


shapes: list[Shape] = [Rectangle(4, 6), Circle(5)]

for s in shapes:
    print(s.describe())

# Rectangle: площа=24.00, периметр=20.00
# Circle: площа=78.54, периметр=31.42
```

## Зведений приклад: усе разом

Продовжуємо проєкт "To-Do" — застосовуємо інкапсуляцію та абстракцію до класів завдань.

```python
from abc import ABC, abstractmethod
from datetime import datetime


class BaseTask(ABC):
    """Абстрактний базовий клас для всіх типів завдань"""

    _id_counter = 0

    def __init__(self, title: str):
        BaseTask._id_counter += 1
        self.__id = BaseTask._id_counter
        self.title = title           # публічний (через setter)
        self.__is_done = False
        self.__created_at = datetime.now()

    @property
    def id(self) -> int:
        return self.__id             # read-only

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Назва завдання не може бути порожньою")
        if len(value) > 100:
            raise ValueError("Назва завдання не може перевищувати 100 символів")
        self._title = value.strip()

    @property
    def is_done(self) -> bool:
        return self.__is_done

    @property
    def created_at(self) -> datetime:
        return self.__created_at    # read-only

    def complete(self) -> None:
        self.__is_done = True

    @abstractmethod
    def status_icon(self) -> str:
        """Кожен підклас визначає власну іконку статусу"""
        pass

    @abstractmethod
    def summary(self) -> str:
        """Короткий опис завдання"""
        pass

    def __repr__(self) -> str:
        return f"[{self.status_icon()}] #{self.id}: {self.title}"


class SimpleTask(BaseTask):
    def status_icon(self) -> str:
        return "✅" if self.is_done else "⏳"

    def summary(self) -> str:
        state = "виконано" if self.is_done else "в роботі"
        return f"Просте завдання «{self.title}» — {state}"


class UrgentTask(BaseTask):
    def __init__(self, title: str, deadline: datetime):
        super().__init__(title)
        self.deadline = deadline

    @property
    def deadline(self) -> datetime:
        return self.__deadline

    @deadline.setter
    def deadline(self, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise TypeError("Дедлайн має бути об'єктом datetime")
        self.__deadline = value

    def __is_overdue(self) -> bool:
        """Приватний допоміжний метод"""
        return datetime.now() > self.__deadline and not self.is_done

    def status_icon(self) -> str:
        if self.__is_overdue():
            return "🔥"
        return "✅" if self.is_done else "⚠️"

    def summary(self) -> str:
        overdue = " [ПРОСТРОЧЕНО]" if self.__is_overdue() else ""
        return f"Термінове завдання «{self.title}» до {self.__deadline.date()}{overdue}"


# --- Використання ---
tasks: list[BaseTask] = [
    SimpleTask("Прочитати документацію"),
    UrgentTask("Підготувати презентацію", datetime(2024, 1, 1)),
    SimpleTask("Написати тести"),
]

tasks[0].complete()

for task in tasks:
    print(task)
    print(f"    {task.summary()}")

print(f"\nВсього завдань: {BaseTask._id_counter}")
```

**Вивід:**
```
[✅] #1: Прочитати документацію
    Просте завдання «Прочитати документацію» — виконано
[🔥] #2: Підготувати презентацію
    Термінове завдання «Підготувати презентацію» до 2024-01-01 [ПРОСТРОЧЕНО]
[⏳] #3: Написати тести
    Просте завдання «Написати тести» — в роботі

Всього завдань: 3
```

## 📋 Підсумок заняття

| Концепція | Ключова ідея | Синтаксис |
|---|---|---|
| **Публічний атрибут** | Доступний звідусіль | `self.name` |
| **Захищений атрибут** | Угода "не чіпай ззовні" | `self._name` |
| **Приватний атрибут** | Name mangling, реальний захист | `self.__name` |
| **`@property`** | Геттер — доступ як до атрибута | `@property` |
| **`.setter`** | Сеттер з валідацією | `@name.setter` |
| **Read-only** | Лише геттер, без сеттера | Тільки `@property` |
| **Приватний метод** | Внутрішня деталь реалізації | `def __method(self)` |
| **`ABC`** | Абстрактний базовий клас | `class A(ABC):` |
| **`@abstractmethod`** | Обов'язковий метод для підкласів | `@abstractmethod` |

## 🏠 Домашнє завдання

Застосуйте інкапсуляцію та валідацію в проєкті "To-Do":

1. Додайте валідацію через `@property` до класу `SimpleTask` — атрибут `priority` (значення: `"low"`, `"medium"`, `"high"`), який перевіряє коректність значення при присвоєнні.
2. Виробіть абстрактний клас `BaseStorage(ABC)` з абстрактними методами `save(task)`, `load_all()`, `delete(task_id)`. Це буде інтерфейс для зберігання завдань.
3. Реалізуйте `InMemoryStorage(BaseStorage)` — зберігає завдання у словнику `dict`.
4. Переконайтеся, що `BaseStorage` не можна інстанціювати напряму — перевірте, що виникає `TypeError`.
5. *(Додатково)* Спробуйте реалізувати `FileStorage(BaseStorage)` — зберігає завдання у текстовий файл.
