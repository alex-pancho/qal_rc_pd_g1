# Заняття 28. Тестування

## Мета заняття

Після заняття ви зможете:

* пояснити навіщо потрібне тестування;
* розрізняти основні типи тестів;
* встановлювати та використовувати pytest;
* створювати тестові функції;
* використовувати assert;
* запускати тести;
* працювати з фікстурами;
* використовувати файл conftest.py;
* писати тести для власних проєктів.

# Що таке тестування

Тестування — це процес перевірки правильності роботи програми.

Мета тестування:

* знайти помилки;
* перевірити бізнес-логіку;
* захиститися від регресії;
* підтвердити коректність змін.

Наприклад, ми написали функцію:

```python
def add(a, b):
    return a + b
```

Звідки ми знаємо, що вона працює правильно?

Можна перевірити вручну:

```python
print(add(2, 3))
```

але для великого проєкту це незручно.

Краще написати автоматичний тест.

# Навіщо потрібні автоматичні тести

Уявіть проєкт із 500 функцій.

Після кожної зміни потрібно перевіряти:

* чи працює авторизація;
* чи працюють розрахунки;
* чи працює API;
* чи працюють класи.

Робити це вручну дуже дорого.

Автоматичні тести виконують перевірки за секунди.

# Типи тестування

Існує багато видів тестування:

* Unit Testing
* Integration Testing
* System Testing
* UI Testing
* Performance Testing

Ми зосередимося на Unit Testing.

# Що таке Unit Test

Unit Test перевіряє окрему частину програми.

Зазвичай це:

* функція;
* метод;
* клас.

Наприклад:

```python
def multiply(a, b):
    return a * b
```

Ми перевіряємо тільки цю функцію.

Без бази даних.

Без мережі.

Без браузера.

# Що таке pytest

Pytest — найпопулярніший фреймворк тестування Python.

Переваги:

* простий синтаксис;
* мінімум коду;
* потужні фікстури;
* автоматичний пошук тестів;
* зрозумілі повідомлення про помилки.

# Встановлення pytest

```bash
pip install pytest
```

Перевірка:

```bash
pytest --version
```

# Структура проєкту

```text
project/

├── calculator.py
└── test_calculator.py
```

# Перша функція

Файл:

```python
# calculator.py

def add(a, b):
    return a + b
```

# Перший тест

```python
# test_calculator.py

from calculator import add

def test_add():

    result = add(2, 3)

    assert result == 5
```

# Assert

Основний інструмент pytest:

```python
assert
```

Приклад:

```python
assert 10 == 10
```

Тест проходить.

# Невдалий тест

```python
assert 10 == 5
```

Pytest покаже:

```text
E assert 10 == 5
```

# Запуск тестів

```bash
pytest
```

або

```bash
pytest -v
```

# Правила пошуку тестів

Pytest автоматично знаходить:

Файли:

```text
test_*.py
```

або

```text
*_test.py
```

Функції:

```python
def test_something():
```

# Кілька тестів

```python
from calculator import add

def test_add_positive():

    assert add(2, 3) == 5


def test_add_zero():

    assert add(10, 0) == 10


def test_add_negative():

    assert add(-1, -2) == -3
```

# Перевірка рядків

```python
def upper_text(text):
    return text.upper()
```

Тест:

```python
def test_upper_text():

    assert upper_text("python") == "PYTHON"
```

# Перевірка списків

```python
def get_numbers():
    return [1, 2, 3]
```

Тест:

```python
def test_get_numbers():

    assert get_numbers() == [1, 2, 3]
```

# Тестування класів

Клас:

```python
class User:

    def __init__(self, name):
        self.name = name
```

# Тест класу

```python
def test_user_name():

    user = User("Alex")

    assert user.name == "Alex"
```

# Приклад проєкту

Створимо клас банківського рахунку.

```python
class BankAccount:

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
```

# Тест поповнення рахунку

```python
def test_deposit():

    account = BankAccount()

    account.deposit(100)

    assert account.balance == 100
```

# Тестування винятків

Іноді ми очікуємо помилку.

Функція:

```python
def divide(a, b):
    return a / b
```

# Перевірка Exception

```python
import pytest

def test_divide_by_zero():

    with pytest.raises(
        ZeroDivisionError
    ):
        divide(10, 0)
```

# Повторення коду

Подивимось на приклад:

```python
def test_deposit():

    account = BankAccount()

    ...
```

```python
def test_withdraw():

    account = BankAccount()

    ...
```

Створення об'єкта повторюється.

# Що таке Fixture

Fixture — підготовка тестових даних.

Замість створення об'єкта в кожному тесті ми створюємо його один раз.

# Перша Fixture

```python
import pytest

@pytest.fixture
def account():

    return BankAccount()
```

# Використання Fixture

```python
def test_deposit(account):

    account.deposit(100)

    assert account.balance == 100
```

Pytest автоматично передасть об'єкт.

# Переваги Fixture

* менше дублювання;
* чистіший код;
* простіше підтримувати;
* перевикористання між тестами.

# Що таке conftest.py

Файл:

```text
conftest.py
```

зберігає спільні фікстури.

# Структура проєкту

```text
project/

├── app.py
├── conftest.py
├── test_user.py
└── test_account.py
```

# Приклад conftest.py

```python
import pytest

from account import BankAccount

@pytest.fixture
def account():

    return BankAccount()
```

# Тест використовує fixture

```python
def test_balance(account):

    assert account.balance == 0
```

Фікстура автоматично доступна.

# Практика №1

Напишіть тести для функцій:

```python
add()
subtract()
multiply()
divide()
```

Перевірте:

* позитивні числа;
* від'ємні числа;
* нуль.

# Практика №2

Напишіть тести для класу:

```python
BankAccount
```

Перевірте:

* створення рахунку;
* поповнення;
* списання;
* баланс після операцій.

# Практика №3

Створіть fixture:

```python
account()
```

та використайте її у всіх тестах.

# Типові помилки

Неправильно:

```python
assert add(2, 2) == 5
```

Неправильно:

```python
def add_test():
```

Pytest не знайде тест.

Правильно:

```python
def test_add():
```

# Хороші практики

Кожен тест повинен:

* перевіряти одну поведінку;
* бути незалежним;
* мати зрозумілу назву;
* швидко виконуватися.

Приклад:

```python
test_withdraw_reduces_balance()
```

краще ніж:

```python
test_1()
```

# Підсумок

На цьому занятті ми:

* розглянули основи тестування;
* познайомилися з Unit Testing;
* встановили pytest;
* створювали тести;
* використовували assert;
* перевіряли винятки;
* працювали з fixture;
* використовували conftest.py;
* тестували функції та класи.

Unit-тести є фундаментом автоматизованого тестування та одним із найважливіших інструментів Python-розробника і QA Automation Engineer.
