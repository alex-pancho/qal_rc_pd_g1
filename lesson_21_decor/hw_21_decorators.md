# Домашнє завдання — Заняття 21
## Декоратори та декорування функцій

**Олександр Панченко, ТОВ «Тренінг-центр КьюЕйЛайт»**

## Що потрібно зробити

На цьому занятті ви навчились писати власні декоратори. Сьогоднішнє ДЗ складається з двох частин:

- **Частина 1** — три окремі завдання для відпрацювання механіки декораторів
- **Частина 2** — доробка навчального проєкту: додати до вже написаного коду декоратори, які **залишаться і використовуватимуться в наступних заняттях**

## Частина 1. Завдання на декоратори

### Завдання 1. Козацька хроніка

Кошовий отаман Іван Сірко ведуть журнал усіх рішень: хто, коли, що вирішив. Напишіть декоратор `@chronicle`, який логує кожен виклик функції: її назву, аргументи та результат.

**Вимоги:**

- Декоратор `@chronicle` приймає необов'язковий аргумент — ім'я "літописця" (рядок). Якщо не передано — використовувати `"Анонімний"`.
- Перед виконанням функції виводити: `[Літописець: {ім'я}] Викликано: {назва_функції}({аргументи})`
- Після виконання виводити: `[Результат]: {результат}`
- Логувати через стандартний модуль `logging` з рівнем `INFO`.

**Приклад використання:**

```python
@chronicle("Самійло Величко")
def make_decision(action, target):
    return f"Рішення: {action} → {target}"

@chronicle()
def count_warriors(regiment):
    return 500

make_decision("Атакувати", "Перекоп")
count_warriors("Полтавський")
```

**Очікуваний вивід у лозі:**

```
INFO [Літописець: Самійло Величко] Викликано: make_decision('Атакувати', 'Перекоп')
INFO [Результат]: Рішення: Атакувати → Перекоп
INFO [Літописець: Анонімний] Викликано: count_warriors('Полтавський')
INFO [Результат]: 500
```

### Завдання 2. Хранитель фортеці

Запорізька Січ охороняється. Щоб увійти до фортеці — потрібен пароль. Напишіть декоратор `@guard`, який перевіряє доступ перед викликом функції.

**Вимоги:**

- Декоратор `@guard(secret)` приймає секретне слово.
- Перед кожним викликом захищеної функції він питає: `Назви пароль: `
- Якщо введено правильний пароль — функція виконується.
- Якщо неправильний — виводити `"Стій! Доступ заборонено."` і функція **не** виконується (повертає `None`).
- Спроба перевірки паролю логується на рівні `WARNING` якщо пароль неправильний, і `INFO` якщо правильний.

**Приклад використання:**

```python
@guard(secret="Мамай")
def open_treasury():
    print("Скарбниця відчинена!")
    return "золото, срібло, зброя"

result = open_treasury()
```

**При правильному паролі:**

```
Назви пароль: Мамай
INFO Доступ надано: open_treasury
Скарбниця відчинена!
```

**При неправильному:**

```
Назви пароль: Морозенко
WARNING Невдала спроба доступу до: open_treasury
Стій! Доступ заборонено.
```

### Завдання 3. Залізний характер

Козак Байда відомий своєю витривалістю — якщо щось пішло не так, він спробує ще раз. Напишіть декоратор `@retry`, який повторює виклик функції при виникненні помилки.

**Вимоги:**

- `@retry(times=3, delay=1.0)` — кількість повторних спроб і затримка між ними (секунди, використати `time.sleep`).
- При кожній невдалій спробі — логувати `WARNING` з номером спроби та текстом помилки.
- Якщо всі спроби вичерпано — логувати `ERROR` і повторно підняти виняток.
- Якщо функція виконалась успішно — логувати `INFO` з номером успішної спроби.

**Приклад використання:**

```python
import random

@retry(times=4, delay=0.5)
def unreliable_scout():
    if random.random() < 0.7:  # 70% шанс провалу
        raise ConnectionError("Розвідник не повернувся")
    return "Ворог за річкою!"

result = unreliable_scout()
print(result)
```

**Приклад виводу в лозі:**

```
WARNING Спроба 1/4 не вдалася: Розвідник не повернувся
WARNING Спроба 2/4 не вдалася: Розвідник не повернувся
INFO Успіх на спробі 3/4
```

> **Підказка:** декоратор `@retry` знадобиться у **Занятті 25** (HTTP-запити) — нестабільні мережеві з'єднання та тайм-аути саме та ситуація, де він рятує.

## Частина 2. Доробка проєкту

Оберіть **свій проєкт** і виконайте завдання для нього.

### Проєкт 1 — Task & Bug Manager

#### Що додати

Додайте до проєкту файл `decorators.py` з трьома декораторами. Потім застосуйте їх до методів класу `TaskManager` (або функцій, якщо у вас процедурний стиль).

#### Декоратор 1: `@log_action`

Логує кожну дію з задачами/багами — хто що зробив і коли.

```python
import logging
import functools
from datetime import datetime

def log_action(func):
    """
    Логує виклик методу: назву, аргументи, час виконання та результат.
    Рівень логування — INFO.
    Використовується на: create_issue, update_issue, delete_issue, change_status
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: зафіксувати час початку
        # TODO: викликати func та отримати результат
        # TODO: зафіксувати час завершення
        # TODO: логувати: назва функції, аргументи, час виконання (мс)
        # TODO: повернути результат
        pass
    return wrapper
```

**Застосувати до:**

```python
class TaskManager:
    @log_action
    def create_issue(self, title, issue_type, priority):
        ...

    @log_action
    def delete_issue(self, issue_id):
        ...

    @log_action
    def change_status(self, issue_id, new_status):
        ...
```

#### Декоратор 2: `@validate_input`

Перевіряє, що аргументи функції не є порожніми рядками або `None`. Якщо перевірка не пройшла — логує `WARNING` і повертає `None` без виклику функції.

```python
def validate_input(*required_args):
    """
    Перевіряє, що вказані позиційні аргументи не є None або порожнім рядком.
    required_args — імена параметрів, які треба перевірити (рядки).
    Використовується на: create_issue, update_issue

    Приклад: @validate_input("title", "issue_type")
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: отримати імена параметрів функції через inspect.signature
            # TODO: зіставити імена з переданими значеннями
            # TODO: для кожного з required_args перевірити, що значення не None і не ""
            # TODO: якщо перевірка провалена — logging.warning(...) і return None
            # TODO: інакше — викликати func і повернути результат
            pass
        return wrapper
    return decorator
```

#### Декоратор 3: `@timer` (заглушка для майбутнього)

Вимірює час виконання функції. Поки що лише логує результат. У майбутньому (тестування, оптимізація) знадобиться для профілювання повільних запитів до БД.

```python
def timer(func):
    """
    Вимірює і логує час виконання функції в мілісекундах.
    Рівень логування — DEBUG (не засмічує лог у звичайному режимі).
    Заглушка: реалізуйте вимірювання, але поки що просто логуйте результат.
    Знадобиться у Занятті 36 (PostgreSQL) для виявлення повільних запитів.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: реалізувати вимірювання часу
        pass
    return wrapper
```

#### Налаштування логування

Додайте у `main.py` або окремий `logger.py`:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("task_manager.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
```

#### Очікуваний результат у лозі

```
2024-03-15 10:23:01 [INFO] create_issue викликано з args=('Fix login', 'Bug', 'High') — 2.3 мс
2024-03-15 10:23:05 [WARNING] validate_input: поле 'title' не може бути порожнім
2024-03-15 10:23:10 [INFO] change_status викликано з args=(3, 'Closed') — 1.1 мс
```

### Проєкт 2 — Expense & Budget Tracker

#### Що додати

Додайте файл `decorators.py`. Застосуйте декоратори до методів `ExpenseTracker`.

#### Декоратор 1: `@log_transaction`

Логує кожну фінансову операцію — тип, суму, категорію, час.

```python
import logging
import functools
from datetime import datetime

def log_transaction(func):
    """
    Логує фінансові операції: тип операції, суму, категорію, час.
    Рівень логування — INFO.
    Використовується на: add_income, add_expense, delete_transaction
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: зафіксувати час виклику
        # TODO: викликати func та отримати результат
        # TODO: логувати: назва функції, kwargs або args, час
        # TODO: повернути результат
        pass
    return wrapper
```

**Застосувати до:**

```python
class ExpenseTracker:
    @log_transaction
    def add_income(self, amount, category, description=""):
        ...

    @log_transaction
    def add_expense(self, amount, category, description=""):
        ...

    @log_transaction
    def delete_transaction(self, transaction_id):
        ...
```

#### Декоратор 2: `@validate_amount`

Перевіряє, що сума транзакції є числом більшим за нуль.

```python
def validate_amount(func):
    """
    Перевіряє перший числовий аргумент (amount):
    — має бути int або float
    — має бути > 0
    Якщо ні — логує WARNING і повертає None.
    Використовується на: add_income, add_expense
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: знайти значення аргументу amount (з args або kwargs)
        # TODO: перевірити тип: isinstance(amount, (int, float))
        # TODO: перевірити значення: amount > 0
        # TODO: якщо перевірка провалена — logging.warning(...) і return None
        # TODO: інакше — викликати func і повернути результат
        pass
    return wrapper
```

#### Декоратор 3: `@currency_aware` (заглушка для майбутнього)

Майбутній декоратор для автоматичної конвертації валюти. Поки що лише заглушка — конвертацію ще не реалізовано (вона з'явиться у Занятті 25, коли підключимо API курсів валют).

```python
def currency_aware(base_currency="UAH"):
    """
    ЗАГЛУШКА — буде реалізовано у Занятті 25 (HTTP + requests).
    Майбутня логіка:
    — отримати поточний курс валюти через API
    — якщо транзакція в іноземній валюті — конвертувати в base_currency
    — зберегти обидва значення (оригінальне і конвертоване)
    Зараз: просто викликає функцію без змін і логує DEBUG повідомлення.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.debug(
                f"[currency_aware] Конвертація ще не реалізована. "
                f"Базова валюта: {base_currency}"
            )
            # TODO (Заняття 25): отримати курс через requests.get(EXCHANGE_API_URL)
            # TODO (Заняття 25): конвертувати суму якщо currency != base_currency
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

#### Налаштування логування

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("expense_tracker.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
```

#### Очікуваний результат у лозі

```
2024-03-15 11:00:01 [INFO] add_expense: сума=350, категорія='food', час=11:00:01
2024-03-15 11:00:03 [WARNING] validate_amount: сума має бути > 0, отримано: -100
2024-03-15 11:00:10 [INFO] delete_transaction: id=5, час=11:00:10
```

### Проєкт 3 — Service Management System

#### Що додати

Додайте файл `decorators.py`. Застосуйте декоратори до методів `ServiceManager`.

#### Декоратор 1: `@log_action`

Логує дії над клієнтами, замовленнями, послугами.

```python
import logging
import functools
from datetime import datetime

def log_action(func):
    """
    Логує операції над сутностями системи: замовлення, клієнти, послуги.
    Рівень логування — INFO.
    Формат: [ДІЯ] назва_функції | аргументи | час виконання мс
    Використовується на: create_order, update_status, delete_order, add_client
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: зафіксувати час початку
        # TODO: викликати func та отримати результат
        # TODO: зафіксувати час завершення
        # TODO: логувати у форматі вище
        # TODO: повернути результат
        pass
    return wrapper
```

**Застосувати до:**

```python
class ServiceManager:
    @log_action
    def create_order(self, client_name, service_name, price):
        ...

    @log_action
    def update_status(self, order_id, new_status):
        ...

    @log_action
    def delete_order(self, order_id):
        ...
```

#### Декоратор 2: `@validate_price`

Перевіряє коректність ціни послуги або запчастини.

```python
def validate_price(func):
    """
    Перевіряє аргумент price:
    — має бути int або float
    — має бути >= 0 (безкоштовні послуги дозволені)
    Якщо ні — логує WARNING і повертає None.
    Використовується на: create_order, add_service, add_part
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: знайти значення аргументу price (з args або kwargs)
        # TODO: isinstance(price, (int, float)) та price >= 0
        # TODO: якщо перевірка провалена — logging.warning(...) і return None
        # TODO: інакше — викликати func і повернути результат
        pass
    return wrapper
```

#### Декоратор 3: `@notify_client` (заглушка для майбутнього)

Надсилає сповіщення клієнту після зміни статусу замовлення. Поки що — заглушка. Реальне надсилання через Telegram Bot API з'явиться у Занятті 25.

```python
def notify_client(func):
    """
    ЗАГЛУШКА — буде реалізовано у Занятті 25 (HTTP + Telegram Bot API).
    Майбутня логіка:
    — після зміни статусу замовлення — надіслати клієнту повідомлення
    — через requests.post до Telegram Bot API
    Зараз: логує DEBUG "Сповіщення ще не налаштовано" і виконує функцію.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.debug(
            f"[notify_client] Сповіщення клієнта після {func.__name__}: "
            f"ще не реалізовано (Заняття 25)"
        )
        # TODO (Заняття 25): знайти клієнта за order_id
        # TODO (Заняття 25): надіслати повідомлення через Telegram Bot API
        # TODO (Заняття 25): requests.post(TELEGRAM_API_URL, json={...})
        return result
    return wrapper
```

#### Налаштування логування

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("service_manager.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
```

#### Очікуваний результат у лозі

```
2024-03-15 12:00:01 [INFO] [ДІЯ] create_order | ('Іваненко', 'Заміна масла', 800) | 1.8 мс
2024-03-15 12:00:03 [WARNING] validate_price: ціна має бути >= 0, отримано: -50
2024-03-15 12:00:10 [INFO] [ДІЯ] update_status | (3, 'Completed') | 0.9 мс
2024-03-15 12:00:10 [DEBUG] [notify_client] Сповіщення клієнта після update_status: ще не реалізовано (Заняття 25)
```

## Що здати

**Файли для кожного проєкту:**

```
your_project/
├── decorators.py        ← всі декоратори проєкту
├── main.py              ← головний файл із застосованими декораторами
└── *.log                ← файл логів після запуску програми
```

**Що перевірятиметься:**

- `decorators.py` містить усі три декоратори (два реалізовані, один — заглушка з `TODO`)
- Декоратори застосовані на методах через `@` — не викликаються вручну всередині функцій
- `@functools.wraps` використано у кожному декораторі
- Логування налаштоване через `logging.basicConfig`, а не через `print()`
- Лог-файл присутній і містить записи після запуску

## Бонус (необов'язково)

Козацький гетьман Богдан Хмельницький мав особливу здібність: одним поглядом запам'ятовував будь-яку інформацію, з якою зустрічався — і ніколи не витрачав час двічі на одне й те саме.

Напишіть декоратор `@memoize`, який кешує результати функції: якщо функція вже викликалась із такими самими аргументами — повертає збережений результат без повторного обчислення. Продемонструйте на функції, яка рахує число Фібоначчі рекурсивно — порівняйте час виконання з кешем і без.

```python
# Підказка: зберігайте результати у словнику виду {args: result}
# Логуйте DEBUG-повідомлення: "Кеш: повертаю збережений результат для fib(35)"
```

## Карта декораторів: що де знадобиться

| Декоратор | Зараз (Зан. 21) | Далі |
|---|---|---|
| `@log_action` / `@log_transaction` | Логування операцій | Зан. 28: тести перевіряють лог |
| `@validate_input` / `@validate_amount` / `@validate_price` | Валідація аргументів | Зан. 41: Django Forms — аналогічна логіка |
| `@timer` | Вимірювання часу | Зан. 36: профілювання SQL-запитів |
| `@retry` | Повторні спроби | Зан. 25: HTTP-запити, нестабільний API |
| `@currency_aware` | Заглушка | Зан. 25: API курсів валют |
| `@notify_client` | Заглушка | Зан. 25: Telegram Bot API |
| `@memoize` (бонус) | Кешування | Зан. 27: асинхронне програмування |
