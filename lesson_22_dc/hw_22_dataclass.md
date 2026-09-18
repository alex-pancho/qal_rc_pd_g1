# Домашнє завдання — Заняття 22
## Dataclass + практика функціонального програмування

**Олександр Панченко, ТОВ «Тренінг-центр КьюЕйЛайт»**

## Що потрібно зробити

ДЗ складається з двох частин:

- **Частина 1** — три окремі задачі на функціональне програмування (`filter`, `map`, `reduce`, `lambda`) — відпрацювання навичок із занять 20–22
- **Частина 2** — доробка проєкту: переписати моделі на `@dataclass` і обробити колекцію сутностей у функціональному стилі

## Частина 1. Функціональна практика

### Завдання 1. Охоронці воріт

Запорізька Січ перевіряє паролі воїнів на вході. Пароль вважається надійним, якщо він:

- має довжину від 8 до 20 символів включно
- містить хоча б одну цифру
- містить хоча б одну велику літеру
- не містить пробілів

Дано список паролів:

```python
passwords = [
    "Cossack1",
    "sich",
    "ZAPORIZHZHIA2024",
    "Sich Gate 5",
    "Mazepa99",
    "короткий1",
    "BohunTheBrave",
    "D0br0nich!",
    "аааааааА1",
    "Valid1Pass",
]
```

Використовуючи `filter` і `lambda`:

1. Відфільтруйте **лише надійні паролі**.
2. Виведіть їх у вигляді: `✅ Cossack1 — надійний`.
3. Відфільтруйте **ненадійні** та виведіть: `❌ sich — відхилено`.

> Усю логіку перевірки реалізуйте через одну функцію `is_strong(password)`, а `filter` + `lambda` — для розділення на дві групи.

### Завдання 2. Перепис козацького реєстру

Гетьман отримав список козаків у "брудному" форматі — з помилками, пробілами, змішаним регістром. Потрібно привести реєстр до єдиного стандарту та підрахувати підсумки.

```python
raw_registry = [
    "  іван сірко  | полковник | 150",
    "БОГДАН ХМЕЛЬНИЦЬКИЙ | гетьман | 10000",
    "петро дорошенко|сотник|75",
    "  Іван Мазепа | гетьман | 30000 ",
    "семен палій  |  полковник  | 500",
    "  Григорій Сковорода | філософ | 0",
]
```

Кожен рядок — `ім'я | посада | кількість воїнів`.

Використовуючи `map`:

1. Розпарсіть кожен рядок у словник `{"name": ..., "rank": ..., "warriors": int}` — ім'я та посада з великої літери, числа — цілі.
2. Через `filter` залиште лише тих, у кого воїнів більше 0.
3. Через `reduce` підрахуйте **загальну кількість воїнів** у реєстрі.
4. Через `sorted` + `lambda` відсортуйте за кількістю воїнів (спадання) і виведіть таблицю:

```
Козацький реєстр (4 записи):
────────────────────────────────────────
 №  Ім'я                  Посада      Воїни
────────────────────────────────────────
 1  Богдан Хмельницький   Гетьман     10000
 2  Іван Мазепа           Гетьман     30000
...
────────────────────────────────────────
Разом воїнів: XXXXX
```

### Завдання 3. Пошук козацьких шифрів

Козаки передають таємні послання. Повідомлення вважається **шифром**, якщо рядок є паліндромом (читається однаково зліва направо і справа наліво) — без урахування регістру та пробілів.

```python
messages = [
    "А роза упала на лапу азора",
    "Козак",
    "Зараз",
    "level",
    "Python",
    "А баба",
    "racecar",
    "Запоріжжя",
    "noon",
    "Мазепа",
]
```

1. Напишіть функцію `is_palindrome(s)` — повертає `True`/`False`.
2. Через `filter` + `lambda` знайдіть усі шифри.
3. Через `map` перетворіть кожен шифр у рядок вигляду: `"🔐 {оригінал}" → "{розвернутий нижній регістр без пробілів}"`.
4. Виведіть результат.

**Очікуваний вивід (частково):**

```
🔐 А роза упала на лапу азора → арозаупаланалапуазора
🔐 level → level
🔐 racecar → racecar
```

## Частина 2. Доробка проєкту

Оберіть свій проєкт і виконайте переписування моделей на `@dataclass`.

### Що таке "переписування на dataclass" і навіщо

Зараз ваші моделі — це класи з `__init__`, де ви вручну присвоюєте `self.title = title`, `self.status = status` тощо. `@dataclass` генерує весь цей шаблонний код автоматично, а ще дає `__repr__`, `__eq__` і можливість заморожування — безкоштовно.

**До (звичайний клас):**

```python
class Issue:
    def __init__(self, title, issue_type, priority, status="Open", deadline=None):
        self.title = title
        self.issue_type = issue_type
        self.priority = priority
        self.status = status
        self.deadline = deadline

    def __repr__(self):
        return f"Issue({self.title}, {self.status})"
```

**Після (dataclass):**

```python
from dataclasses import dataclass, field
from datetime import date

@dataclass
class Issue:
    title: str
    issue_type: str
    priority: str
    status: str = "Open"
    deadline: date | None = None
    tags: list[str] = field(default_factory=list)

    def is_overdue(self) -> bool:
        if self.deadline is None:
            return False
        return date.today() > self.deadline
```

Це **той самий клас**, але без зайвого шаблонного коду. І він вже готовий до Django ORM (заняття 40) — поля `@dataclass` прямо відповідають полям Django-моделі.

### Проєкт 1 — Task & Bug Manager

#### Що переписати

Перепишіть моделі `Issue` (і підкласи `Task`, `Bug`, `TestCase` якщо є) та `User` на `@dataclass`.

#### Модель `User`

```python
from dataclasses import dataclass

@dataclass
class User:
    username: str
    email: str
    # TODO: додати поле role: str = "developer"
    # TODO: додати метод display() -> str, який повертає "username <email>"
```

#### Модель `Issue`

```python
from dataclasses import dataclass, field
from datetime import date
from enum import Enum

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class Status(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

@dataclass
class Issue:
    title: str
    issue_type: str                         # "Task", "Bug", "TestCase"
    priority: Priority = Priority.MEDIUM
    status: Status = Status.OPEN
    assignee: User | None = None
    deadline: date | None = None
    tags: list[str] = field(default_factory=list)

    # TODO: додати метод is_overdue() -> bool
    # TODO: додати метод summary() -> str:
    #        повертає "[Bug][High] Fix login — Open (до 2024-12-31)"
```

#### Що зробити з колекцією через функціональний підхід

Після переписування моделей створіть список із 6–8 тестових `Issue` і виконайте обробку:

```python
issues: list[Issue] = [...]  # ваші тестові дані

# 1. filter: лише відкриті (status == Status.OPEN)
open_issues = list(filter(lambda i: ..., issues))

# 2. filter: прострочені (is_overdue() == True)
overdue = list(filter(lambda i: ..., issues))

# 3. map: список рядків summary() для всіх issues
summaries = list(map(lambda i: ..., issues))

# 4. sorted: за пріоритетом (Critical → High → Medium → Low)
#    Підказка: визначте порядок через словник або list.index()
priority_order = {Priority.CRITICAL: 0, Priority.HIGH: 1, ...}
sorted_issues = sorted(issues, key=lambda i: ...)

# 5. Виведіть кожен summary зі sorted_issues
```

### Проєкт 2 — Expense & Budget Tracker

#### Що переписати

Перепишіть моделі `Transaction`, `Budget` та `User` на `@dataclass`.

#### Модель `User`

```python
from dataclasses import dataclass

@dataclass
class User:
    username: str
    email: str
    # TODO: додати поле currency: str = "UAH"
    # TODO: додати метод display() -> str
```

#### Модель `Transaction`

```python
from dataclasses import dataclass, field
from datetime import date
from enum import Enum

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

@dataclass
class Transaction:
    amount: float
    transaction_type: TransactionType
    category: str
    date: date = field(default_factory=date.today)
    description: str = ""

    # TODO: додати метод is_expense() -> bool
    # TODO: додати метод formatted() -> str:
    #        повертає "+ 5000.00 UAH [Salary] 2024-03-15"
    #        або     "- 350.00 UAH [Food] 2024-03-15"
```

#### Модель `Budget`

```python
from dataclasses import dataclass

@dataclass
class Budget:
    category: str
    monthly_limit: float
    spent: float = 0.0

    # TODO: додати метод remaining() -> float
    # TODO: додати метод is_exceeded() -> bool
    # TODO: додати метод utilization_pct() -> float
    #        повертає відсоток використання ліміту (0.0 – 100.0+)
```

#### Що зробити з колекцією через функціональний підхід

```python
from functools import reduce

transactions: list[Transaction] = [...]  # 8–10 тестових транзакцій

# 1. filter: лише витрати
expenses = list(filter(lambda t: ..., transactions))

# 2. filter: лише доходи
incomes = list(filter(lambda t: ..., transactions))

# 3. map + reduce: загальна сума витрат
total_expenses = reduce(lambda acc, t: ..., expenses, 0.0)

# 4. map + reduce: загальна сума доходів
total_incomes = reduce(lambda acc, t: ..., incomes, 0.0)

# 5. filter + map: витрати по категорії "food" — список formatted()
food_expenses = list(map(
    lambda t: t.formatted(),
    filter(lambda t: t.category.lower() == "food", expenses)
))

# 6. sorted: транзакції від найбільшої суми до найменшої
sorted_by_amount = sorted(transactions, key=lambda t: ..., reverse=True)

# Вивід звіту:
# Доходи:  +XXXXX.XX UAH
# Витрати: -XXXXX.XX UAH
# Баланс:   XXXXX.XX UAH
```

### Проєкт 3 — Service Management System

#### Що переписати

Перепишіть моделі `Client`, `Service` та `Order` / `Appointment` на `@dataclass`.

#### Модель `Client`

```python
from dataclasses import dataclass

@dataclass
class Client:
    name: str
    phone: str
    email: str = ""
    # TODO: додати поле notes: str = ""
    # TODO: додати метод display() -> str:
    #        повертає "Іваненко Петро | +380991234567"
```

#### Модель `Service`

```python
from dataclasses import dataclass

@dataclass
class Service:
    name: str
    price: float
    duration_minutes: int
    # TODO: додати метод price_per_hour() -> float
    # TODO: додати метод formatted() -> str:
    #        повертає "Заміна масла — 800 грн (30 хв)"
```

#### Модель `Order` / `Appointment`

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    CREATED = "Created"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

@dataclass
class Order:
    client: Client
    service: Service
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    notes: str = ""

    # TODO: додати метод total_price() -> float
    #        (поки що = service.price; пізніше враховуватиме знижки)
    # TODO: додати метод summary() -> str:
    #        "[Created] Іваненко — Заміна масла — 800 грн | 2024-03-15 10:30"
    # TODO: додати метод is_active() -> bool
    #        True якщо статус CREATED або IN_PROGRESS
```

#### Що зробити з колекцією через функціональний підхід

```python
from functools import reduce

orders: list[Order] = [...]  # 6–8 тестових замовлень

# 1. filter: лише активні замовлення (is_active() == True)
active = list(filter(lambda o: ..., orders))

# 2. filter: лише завершені
completed = list(filter(lambda o: ..., orders))

# 3. map + reduce: загальна виручка по завершених
total_revenue = reduce(lambda acc, o: ..., completed, 0.0)

# 4. map: список summary() для всіх активних
active_summaries = list(map(lambda o: ..., active))

# 5. sorted: завершені за датою (найновіші першими)
sorted_completed = sorted(completed, key=lambda o: ..., reverse=True)

# 6. filter: замовлення конкретного клієнта (за ім'ям)
client_name = "Іваненко"
client_orders = list(filter(lambda o: ..., orders))

# Вивід підсумку:
# Активних замовлень:    X
# Завершених замовлень:  X
# Загальна виручка:      XXXX.XX грн
```

## Що здати

**Структура файлів:**

```
your_project/
├── models.py        ← переписані @dataclass моделі
└── main.py          ← демонстрація: створення об'єктів + функціональна обробка
```

**Що перевірятиметься:**

- `@dataclass` застосовано до всіх моделей проєкту
- `Enum` використано для статусів і пріоритетів
- `field(default_factory=...)` використано для мутабельних значень за замовчуванням (`list`, `datetime.now`)
- Всі методи (`summary`, `formatted`, `is_overdue` тощо) реалізовані та повертають рядки / числа / bool
- Колекція сутностей оброблена через `filter`, `map`, `reduce`, `sorted`
- Виводиться читабельний підсумок

## Бонус (необов'язково)

Козацька рада обговорила план: потрібен **незмінний реєстр рішень**, куди не можна вносити правки після прийняття. Реалізуйте заморожений (`frozen=True`) dataclass `Decision`:

```python
@dataclass(frozen=True)
class Decision:
    title: str
    author: str
    date: date
    description: str

    def summary(self) -> str:
        return f"[{self.date}] {self.author}: «{self.title}»"
```

1. Переконайтесь, що після створення об'єкт не можна змінити — отримаєте `FrozenInstanceError`.
2. Збережіть кілька `Decision` у `frozenset` — переконайтесь, що дублікати не додаються.
3. Поясніть у коментарі: **чому `frozen=True` dataclass підходить для журналу дій** і як це пов'язано з концепцією чистих функцій із заняття 20.

## Карта моделей: що стане Django-моделлю

Поле `@dataclass` сьогодні → поле Django Model (заняття 40):

| dataclass | Django ORM |
|---|---|
| `title: str` | `title = models.CharField(max_length=255)` |
| `status: Status = Status.OPEN` | `status = models.CharField(choices=Status.choices)` |
| `deadline: date \| None = None` | `deadline = models.DateField(null=True, blank=True)` |
| `assignee: User \| None = None` | `assignee = models.ForeignKey(User, null=True)` |
| `tags: list[str] = field(...)` | `tags = models.ManyToManyField(Tag)` |
| `created_at: datetime = field(default_factory=datetime.now)` | `created_at = models.DateTimeField(auto_now_add=True)` |

Чим акуратніше ви опишете `@dataclass` зараз — тим простіше буде переписати на Django ORM у занятті 40.
