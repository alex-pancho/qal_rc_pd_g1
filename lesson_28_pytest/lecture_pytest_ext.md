# Практичне застосування pytest

## 1. Мета заняття

Після заняття студент повинен вміти:

* організовувати тести за принципом **Arrange → Act → Assert**;
* використовувати `pytest.fixture`;
* виконувати підготовку та очищення тестового оточення;
* параметризувати тести;
* перевіряти exceptions;
* використовувати `ids` для читабельних тестів;
* працювати з logging;
* запускати окремі тести та групи тестів;
* дебажити pytest-тести у VS Code;
* розуміти, де закінчується тест і починається test infrastructure;
* писати тести, які легко підтримувати.

---

# 2. Тестований код

Для практики використаємо простий `BankAccount`.

```python
class BankAccount:

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError(
                "For deposit amount should be large than zero"
            )

        self.balance += amount


def add(a, b):
    return a + b
```

---

# 3. Базовий тест

Почнемо з найпростішого.

```python
def test_add_plus():
    assert add(2, 3) == 5
```

Тут pytest робить три речі:

1. запускає функцію `test_add_plus`;
2. виконує `add(2, 3)`;
3. перевіряє `assert`.

---

# 4. Arrange → Act → Assert

У реальних проектах тест краще структурувати.

```python
def test_ab_positive():
    # Arrange
    a = 1
    b = 2
    expected = 3

    # Act
    actual_result = add(a, b)

    # Assert
    assert expected == actual_result
```

### Що означають ці етапи?

**Arrange** — підготовка даних:

```python
a = 1
b = 2
expected = 3
```

**Act** — виконання операції:

```python
actual_result = add(a, b)
```

**Assert** — перевірка результату:

```python
assert expected == actual_result
```

Цей підхід особливо важливий, коли тест стає складнішим.

---

# 5. Інформативні повідомлення при падінні

Можна додати власне повідомлення:

```python
def test_ab_positive():
    a = 1
    b = 2
    expected = 3

    actual_result = add(a, b)

    assert expected == actual_result, (
        f"Get wrong data: {a}, {b}, "
        f"result {actual_result}, expected {expected}"
    )
```

Якщо тест впаде, pytest покаже контекст.

Наприклад:

```text
AssertionError:
Get wrong data: 1, 2, result 4, expected 3
```

Це особливо корисно у CI/CD, де тест запускається без debugger.

---

# 6. Fixture

Тепер переходимо до `BankAccount`.

Ми можемо створювати account безпосередньо в кожному тесті:

```python
def test_ba_without_changes():
    account = BankAccount(0)

    assert account.balance == 0
```

Але якщо багато тестів працюють з однаковим account, код починає дублюватися.

Для цього використовуємо fixture.

## `conftest.py`

```python
import pytest

from source import BankAccount


@pytest.fixture
def zero_account():
    acc = BankAccount(0)

    yield acc

    del acc


@pytest.fixture
def one_000_account():
    acc = BankAccount(1000)

    yield acc

    del acc
```

Тепер тест:

```python
def test_ba_without_changes(zero_account):
    assert zero_account.balance == 0
```

pytest сам:

1. знайде fixture;
2. виконає `BankAccount(0)`;
3. передасть результат у тест;
4. після тесту продовжить виконання fixture після `yield`.

---

# 7. `yield` у fixture

Ось це важливий практичний момент:

```python
@pytest.fixture
def zero_account():
    # SETUP
    acc = BankAccount(0)

    yield acc

    # TEARDOWN
    del acc
```

Можна умовно представити так:

```text
        fixture
           │
           ▼
       SETUP
           │
           ▼
       BankAccount
           │
           ▼
         yield
           │
           ▼
          TEST
           │
           ▼
       TEARDOWN
           │
           ▼
         del acc
```

### Навіщо це потрібно?

У реальному проекті замість:

```python
del acc
```

може бути:

```python
delete_test_user()
```

або:

```python
close_database_connection()
```

або:

```python
docker_container.stop()
```

або:

```python
delete_test_file()
```

або:

```python
rollback_transaction()
```

Наприклад:

```python
@pytest.fixture
def test_user():
    user = create_user()

    yield user

    delete_user(user.id)
```

Тест отримує готового користувача:

```python
def test_user_login(test_user):
    response = login(test_user)

    assert response.status_code == 200
```

А після тесту користувач гарантовано видаляється.

**Це одна з головних практичних задач fixtures — керувати життєвим циклом тестових ресурсів.**

---

# 8. Fixture scope

Fixtures можуть мати різний lifecycle.

```python
@pytest.fixture(scope="function")
def account():
    ...
```

За замовчуванням:

```text
function
```

Тобто fixture створюється для кожного тесту.

Також є:

```text
function
class
module
package
session
```

Наприклад:

```python
@pytest.fixture(scope="session")
def database():
    db = create_database()

    yield db

    db.close()
```

Така fixture буде створена один раз на весь pytest session.

### Практичне правило

Чим ширший `scope`, тим довше живе ресурс.

Наприклад:

```text
function → один тест
class    → один клас тестів
module   → один файл
session  → весь запуск pytest
```

---

# 9. Параметризація

У нас є такі тести:

```python
def test_add_plus():
    assert add(2, 3) == 5


def test_add_zero():
    assert add(10, 0) == 10


def test_add_minus():
    assert add(-1, -2) == -3
```

Тут одна й та сама логіка тесту.

Замість трьох функцій:

```python
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (10, 0, 10),
        (-1, -2, -3),
    ]
)
def test_add(a, b, expected):
    assert add(a, b) == expected
```

Тепер pytest запустить тест тричі.

---

# 10. `ids` для параметризованих тестів

Можна зробити тести зрозумілими у pytest output:

```python
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (10, 0, 10),
        (-1, -2, -3),
    ],
    ids=[
        "positive_numbers",
        "zero",
        "negative_numbers",
    ]
)
def test_add(a, b, expected):
    assert add(a, b) == expected
```

У результаті:

```text
test_add[positive_numbers] PASSED
test_add[zero] PASSED
test_add[negative_numbers] PASSED
```

Це набагато корисніше, ніж:

```text
test_add[2-3-5]
```

особливо коли тестів сотні.

---

# 11. Параметризація BankAccount

Банківський приклад можна привести до такого вигляду:

```python
@pytest.mark.parametrize(
    "init_balance, amount",
    [
        (0, 0.01),
        (100, 0.01),
        (0, 1),
        (100, 1),
        (0, 10.01),
        (100, 10.01),
        (0, 100000.01),
        (100, 10000.01),
    ],
    ids=[
        "zero_balance_small_deposit",
        "100_balance_small_deposit",
        "zero_balance_one",
        "100_balance_one",
        "zero_balance_10",
        "100_balance_10",
        "zero_balance_large_deposit",
        "100_balance_large_deposit",
    ]
)
def test_ba_fill_more_balance(init_balance, amount):

    # Arrange
    account = BankAccount(init_balance)

    # Act
    account.deposit(amount)

    # Assert
    assert account.balance == init_balance + amount
```

Це хороший приклад того, як **один тест перевіряє багато наборів даних**.

---

# 12. Parametrize + fixture

Важливий момент: fixture не можна просто передати сюди:

```python
@pytest.mark.parametrize(
    "account",
    [
        zero_account,
        one_000_account
    ]
)
```

Тому що `zero_account` тут — це не результат fixture, а сама функція.

Якщо дуже потрібно параметризувати fixture, існує `indirect`.

Наприклад:

```python
@pytest.fixture
def account(request):
    return BankAccount(request.param)
```

Тоді:

```python
@pytest.mark.parametrize(
    "account",
    [0, 1000],
    indirect=True
)
def test_account(account):
    assert account.balance >= 0
```

Але для простих випадків краще параметризувати **вхідні дані**, а не fixtures.

---

# 13. Перевірка exceptions

Наприклад, негативний deposit заборонений.

```python
def test_ba_fill_negative(zero_account):

    with pytest.raises(ValueError):
        zero_account.deposit(-1)
```

А якщо треба перевірити текст exception:

```python
def test_ba_fill_negative(zero_account):

    with pytest.raises(ValueError) as e:
        zero_account.deposit(-1)

    assert str(e.value) == (
        "For deposit amount should be large than zero"
    )
```

Або:

```python
def test_ba_fill_negative(zero_account):

    with pytest.raises(
        ValueError,
        match="For deposit amount should be large than zero"
    ):
        zero_account.deposit(-1)
```

---

# 14. Параметризація негативних сценаріїв

Тут уже можна отримати хороший production-like тест:

```python
@pytest.mark.parametrize(
    "amount",
    [
        -1,
        -0.01,
        -100,
        -100000,
    ],
    ids=[
        "negative_one",
        "negative_fraction",
        "negative_hundred",
        "negative_large_amount",
    ]
)
def test_ba_negative_deposit(zero_account, amount):

    with pytest.raises(
        ValueError,
        match="For deposit amount should be large than zero"
    ):
        zero_account.deposit(amount)
```

Тепер один тест перевіряє цілу групу негативних сценаріїв.

---

# 15. Logging

У тестах іноді потрібно бачити, що саме відбувається.

```python
import logging

logger = logging.getLogger(__name__)
```

Потім:

```python
def test_ab_positive():
    a = 1
    b = 2
    expected = 3

    actual_result = add(a, b)

    logger.debug(
        "Get data: %d, %d result %d, expected %d",
        a,
        b,
        actual_result,
        expected
    )

    assert actual_result == expected
```

Зверни увагу: краще використовувати:

```python
logger.debug("value=%s", value)
```

а не:

```python
logger.debug("value=%s" % value)
```

Logging сам виконає форматування.

---

# 16. Налаштування logging у `conftest.py`

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            "example.log",
            encoding="utf8"
        )
    ]
)
```

Тепер повідомлення можуть одночасно йти:

```text
console
   +
example.log
```

Для реальних automation-проектів це корисно, коли потрібно зрозуміти:

```text
що тест робив
з якими даними
який response отримав
який SQL виконався
який результат очікувався
```

---

# 17. `-s`, `-v`, `-vv`, `-vvv`

Базовий запуск:

```bash
pytest
```

Більше інформації:

```bash
pytest -v
```

Ще більше:

```bash
pytest -vv
```

Виведення `print()`:

```bash
pytest -s
```

Разом:

```bash
pytest -vv -s
```

Наприклад:

```bash
pytest -vv -s test_bank_account.py
```

---

# 18. Запуск конкретного тесту

Можна запускати конкретний тест:

```bash
pytest -k test_ba_fill_balance
```

Або:

```bash
pytest -k "negative"
```

Тоді pytest запустить тести, в назві яких є `negative`.

Наприклад:

```text
test_ba_negative_deposit
test_ba_fill_negative
test_negative_balance
```

---

# 19. Запуск конкретного параметризованого кейса

Якщо є:

```python
ids=[
    "zero_balance",
    "100_balance",
    "large_balance",
]
```

можна знайти конкретний кейс через `-k`:

```bash
pytest -k "zero_balance"
```

Це дуже зручно, коли один параметризований тест має 50–100 наборів даних, а впав лише один.

---

# 20. Debugging у VS Code

Для дебагу pytest можна використовувати `.vscode/launch.json`.

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Pytest Debugger",
            "type": "debugpy",
            "request": "launch",
            "console": "integratedTerminal",
            "justMyCode": true,
            "module": "pytest",
            "args": [
                "-vvv",
                "-s",
                "${file}"
            ],
            "purpose": [
                "debug-test"
            ]
        },
        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}
```

Після цього можна:

1. поставити breakpoint;
2. відкрити тест;
3. вибрати `Pytest Debugger`;
4. запустити Debug;
5. виконання зупиниться на breakpoint.

---

# 21. Практична задача для студентів

Спробуйте самостійно таку вправу:

## Завдання

Є:

```python
class BankAccount:

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError(
                "For deposit amount should be large than zero"
            )

        self.balance += amount
```

Необхідно написати тести:

### 1. Початковий баланс

Перевірити:

```text
0
100
1000
```

### 2. Deposit

Перевірити:

```text
0 + 1
100 + 1
1000 + 100
```

Використати `parametrize`.

### 3. Negative deposit

Перевірити:

```text
-1
-0.01
-100
```

Очікувати `ValueError`.

### 4. Fixtures

Створити:

```python
zero_account
one_000_account
```

у `conftest.py`.

### 5. Teardown

Додати:

```python
yield acc
del acc
```

і пояснити, що в реальному тестовому середовищі після `yield` може виконуватися cleanup:

```python
delete_test_account(acc.id)
```

### 6. Logging

Додати лог:

```text
initial balance
deposit amount
final balance
expected balance
```

### 7. Debugging

Поставити breakpoint перед:

```python
account.deposit(amount)
```

і подивитися значення:

```text
account.balance
amount
expected
```

---

# 22. Фінальний варіант тестового файлу

У підсумку у вас може прийти приблизно до такого:

```python
import logging

import pytest

from source import add, BankAccount


logger = logging.getLogger(__name__)


def test_add_positive():
    # Arrange
    a = 1
    b = 2
    expected = 3

    # Act
    actual = add(a, b)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (10, 0, 10),
        (-1, -2, -3),
    ],
    ids=[
        "positive",
        "zero",
        "negative",
    ]
)
def test_add(a, b, expected):
    assert add(a, b) == expected


def test_ba_without_changes(zero_account):
    assert zero_account.balance == 0


def test_ba_fill_zero(zero_account):
    zero_account.deposit(0)

    assert zero_account.balance == 0


@pytest.mark.parametrize(
    "init_balance, amount",
    [
        (0, 0.01),
        (100, 0.01),
        (0, 1),
        (100, 1),
        (0, 10.01),
        (100, 10.01),
        (0, 100000.01),
        (100, 10000.01),
    ],
    ids=[
        "zero_small",
        "100_small",
        "zero_one",
        "100_one",
        "zero_10",
        "100_10",
        "zero_large",
        "100_large",
    ]
)
def test_ba_deposit(init_balance, amount):

    # Arrange
    account = BankAccount(init_balance)
    expected = init_balance + amount

    # Act
    account.deposit(amount)

    logger.debug(
        "Initial=%s amount=%s actual=%s expected=%s",
        init_balance,
        amount,
        account.balance,
        expected,
    )

    # Assert
    assert account.balance == expected


@pytest.mark.parametrize(
    "amount",
    [-1, -0.01, -100],
    ids=[
        "negative_one",
        "negative_fraction",
        "negative_hundred",
    ]
)
def test_ba_negative_deposit(zero_account, amount):

    with pytest.raises(
        ValueError,
        match="For deposit amount should be large than zero"
    ):
        zero_account.deposit(amount)


def test_1000_without_changes(one_000_account):
    assert one_000_account.balance == 1000
```

---

## 23. Що студент має винести з практики

зв'язок у одне ціле

```text
pytest
 │
 ├── Test
 │    ├── Arrange
 │    ├── Act
 │    └── Assert
 │
 ├── Fixture
 │    ├── Setup
 │    ├── Test
 │    └── Teardown
 │
 ├── Parametrize
 │    └── багато тестових даних → один тест
 │
 ├── raises
 │    └── перевірка негативних сценаріїв
 │
 ├── logging
 │    └── діагностика
 │
 └── debugger
      └── пошук причини помилки
```

**Головна ідея уроку:** pytest — це не просто `assert`. Це інструмент для побудови керованого **test lifecycle**: підготувати середовище → виконати дію → перевірити результат → гарантовано прибрати створені ресурси → отримати достатньо інформації для діагностики падіння.
