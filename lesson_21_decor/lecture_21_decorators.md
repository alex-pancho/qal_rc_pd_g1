# Заняття 21. Декоратори та декорування функцій

## Що таке декоратор

Декоратор — це функція, яка приймає іншу функцію, додає до неї нову поведінку та повертає оновлену функцію.

Простими словами: декоратор дозволяє додати функціональність до існуючого коду без зміни самого коду.

У реальних проєктах декоратори часто використовуються для:

* логування викликів функцій;
* перевірки прав доступу;
* кешування результатів;
* вимірювання часу виконання;
* обробки помилок;
* повторних спроб виконання запиту (retry).

# Композиція функцій

Декоратори базуються на тому, що в Python функції є об'єктами.

Функцію можна:

* передавати як аргумент;
* повертати з іншої функції;
* зберігати у змінній.

Приклад композиції функцій:

```python
def add_prefix(text):
    return f"[INFO] {text}"

def make_upper(text):
    return text.upper()

message = add_prefix(make_upper("server started"))

print(message)
```

Результат:

```text
[INFO] SERVER STARTED
```

Тут результат однієї функції передається в іншу.

Саме на цьому принципі побудовані декоратори.

# Функція як аргумент

```python
def execute(func):
    func()

def say_hello():
    print("Hello")

execute(say_hello)
```

Результат:

```text
Hello
```

Функція `say_hello` передається як звичайний об'єкт.

# Перший декоратор

Припустимо, ми хочемо логувати виклик функцій.

Без декоратора:

```python
def create_user():
    print("Creating user")

print("Function started")
create_user()
print("Function finished")
```

Проблема — код логування доведеться копіювати багато разів.

# Створення декоратора

```python
def logger(func):

    def wrapper():
        print("Function started")
        func()
        print("Function finished")

    return wrapper


@logger
def create_user():
    print("Creating user")


create_user()
```

Результат:

```text
Function started
Creating user
Function finished
```

Синтаксис:

```python
@logger
def create_user():
    ...
```

еквівалентний:

```python
create_user = logger(create_user)
```

# Як працює декоратор

Кроки виконання:

1. Python створює функцію `create_user`.
2. Викликає `logger(create_user)`.
3. Усередині створюється функція `wrapper`.
4. `wrapper` повертається замість оригінальної функції.
5. Під час виклику запускається `wrapper`.

Схема:

```text
create_user
      ↓
   logger
      ↓
   wrapper
      ↓
create_user()
```

# Декоратор для функцій з аргументами

Реальні функції майже завжди приймають параметри.

```python
def logger(func):

    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@logger
def create_user(name):
    print(f"User {name} created")


create_user("Alex")
```

Результат:

```text
Calling create_user
User Alex created
```

# Практичний приклад: логування API-запитів

У бекенд-системах часто потрібно бачити всі виклики сервісів.

```python
def log_request(func):

    def wrapper(*args, **kwargs):
        print(f"API call: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@log_request
def get_user(user_id):
    print(f"Loading user {user_id}")



```

# Практичний приклад: вимірювання часу виконання

```python
import time


def measure_time(func):

    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        finish = time.time()

        print(f"Execution time: {finish - start:.3f}s")

        return result

    return wrapper


@measure_time
def load_data():
    time.sleep(1)


load_data()
```

Такий підхід часто використовується для пошуку повільних операцій.

# functools.wraps

Після декорування інформація про функцію втрачається.

```python
print(load_data.__name__)
```

Результат:

```text
wrapper
```

Для виправлення використовується `functools.wraps`.

```python
from functools import wraps


def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
```

Тепер:

```python
print(load_data.__name__)
```

Результат:

```text
load_data
```

# Декоратори з аргументами

Іноді потрібно передати налаштування в декоратор.

Наприклад, дозволити виконувати функцію лише певній ролі користувача.

```python
def require_role(role):

    def decorator(func):

        def wrapper(user_role):
            if user_role != role:
                raise PermissionError("Access denied")

            return func(user_role)

        return wrapper

    return decorator
```

Використання:

```python
@require_role("admin")
def delete_user(user_role):
    print("User deleted")
```

# Практичний приклад: Retry для API

Мережеві запити можуть випадково падати.

```python
def retry(attempts):

    def decorator(func):

        def wrapper(*args, **kwargs):

            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)

                except Exception:
                    pass

            raise Exception("All attempts failed")

        return wrapper

    return decorator
```

Використання:

```python
@retry(3)
def send_request():
    ...
```

Функція буде автоматично повторюватися до 3 разів.

# Фабрики декораторів

Фабрика декораторів — це функція, яка створює декоратор.

Насправді всі декоратори з параметрами є фабриками.

```python
def logger(level):

    def decorator(func):

        def wrapper(*args, **kwargs):
            print(f"[{level}] {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
```

Використання:

```python
@logger("INFO")
def create_user():
    pass

@logger("ERROR")
def delete_user():
    pass
```

# Мемоізація

Мемоізація — це кешування результатів функції.

Якщо функція вже виконувалась з такими аргументами, результат повертається з кешу.

Без кешу:

```python
def square(number):
    print("Calculating...")
    return number * number
```

Кожен виклик виконує обчислення заново.

# Власна реалізація мемоізації

```python
def memoize(func):

    cache = {}

    def wrapper(number):

        if number not in cache:
            cache[number] = func(number)

        return cache[number]

    return wrapper


@memoize
def square(number):
    print("Calculating...")
    return number * number
```

Перевірка:

```python
print(square(5))
print(square(5))
print(square(5))
```

Результат:

```text
Calculating...
25
25
25
```

Обчислення виконалось лише один раз.

# functools.lru_cache

У Python вже існує готовий декоратор кешування.

```python
from functools import lru_cache


@lru_cache
def fibonacci(number):

    if number < 2:
        return number

    return fibonacci(number - 1) + fibonacci(number - 2)
```

Це один із найпоширеніших прикладів використання мемоізації.

# Декоратори у фреймворках

У професійній розробці декоратори використовуються всюди.

Flask:

```python
@app.route("/users")
def get_users():
    pass
```

Django:

```python
@login_required
def profile(request):
    pass
```

Pytest:

```python
@pytest.fixture
def browser():
    pass
```

Ви вже користувались декораторами, навіть якщо не знали про це.

# Коли варто використовувати декоратори

Використовуйте декоратори коли потрібно:

* логування;
* кешування;
* вимірювання часу;
* перевірка доступу;
* повторні спроби виконання;
* обробка винятків;
* валідація аргументів.

Не варто використовувати декоратори, якщо логіка потрібна лише в одному місці або робить код складнішим для читання.

# Підсумок

Сьогодні ми вивчили:

* композицію функцій;
* передачу функцій як об'єктів;
* створення власних декораторів;
* декоратори з аргументами;
* фабрики декораторів;
* мемоізацію та кешування;
* використання декораторів у реальних проєктах.

Декоратори — один із найважливіших механізмів Python, який активно використовується у Flask, Django, FastAPI, Pytest та багатьох інших бібліотеках.
