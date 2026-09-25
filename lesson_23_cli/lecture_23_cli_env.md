# Заняття 23. CLI та конфігурація застосунків

## Мета заняття

Після цього заняття ви зможете:

* створювати консольні утиліти;
* отримувати параметри командного рядка;
* використовувати модуль `argparse`;
* працювати зі змінними середовища;
* зберігати налаштування у конфігураційних файлах;
* використовувати переліки (`Enum`);
* розуміти призначення бібліотеки Typer.

# Що таке CLI

CLI (Command Line Interface) — це інтерфейс командного рядка.

Більшість професійних інструментів мають CLI:

* git
* docker
* pytest
* django-admin
* pip

Наприклад:

```bash
git status

pytest tests/

python app.py --debug
```

Програма отримує параметри та виконує відповідну дію.

# Аргументи командного рядка

Під час запуску програми можна передавати додаткові дані.

Приклад:

```bash
python hello.py Alex
```

Усередині програми аргументи доступні через модуль `sys`.

```python
import sys

print(sys.argv)
```

Результат:

```python
['hello.py', 'Alex']
```

Перший елемент завжди містить ім'я файлу.

# Простий приклад

```python
import sys

name = sys.argv[1]

print(f"Hello, {name}")
```

Запуск:

```bash
python hello.py John
```

Результат:

```text
Hello, John
```

# Недоліки sys.argv

При збільшенні кількості параметрів код стає незручним.

```python
import sys

username = sys.argv[1]
password = sys.argv[2]
host = sys.argv[3]
port = sys.argv[4]
```

Легко помилитися.

Для цього існує `argparse`.

# Модуль argparse

`argparse` входить до стандартної бібліотеки Python.

Дозволяє:

* описувати параметри;
* перевіряти введення;
* автоматично генерувати довідку;
* задавати значення за замовчуванням.

# Перший приклад argparse

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("name")

args = parser.parse_args()

print(f"Hello, {args.name}")
```

Запуск:

```bash
python app.py Alex
```

# Автоматична довідка

Будь-яка програма на argparse підтримує:

```bash
python app.py --help
```

Результат:

```text
usage: app.py [-h] name

positional arguments:
  name

options:
  -h, --help
```

Довідка створюється автоматично.

# Іменовані параметри

Зазвичай використовуються параметри виду:

```bash
python app.py --name Alex
```

Код:

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--name")

args = parser.parse_args()

print(args.name)
```

# Значення за замовчуванням

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--host",
    default="localhost"
)

args = parser.parse_args()

print(args.host)
```

# Обов'язкові параметри

```python
parser.add_argument(
    "--username",
    required=True
)
```

Запуск без параметра:

```bash
python app.py
```

Викличе помилку.

# Перетворення типів

```python
parser.add_argument(
    "--age",
    type=int
)
```

Тепер argparse автоматично перетворить рядок у число.

```bash
python app.py --age 25
```

# Практичний приклад: калькулятор

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--a", type=float)
parser.add_argument("--b", type=float)

args = parser.parse_args()

print(args.a + args.b)
```

Запуск:

```bash
python calc.py --a 10 --b 20
```

Результат:

```text
30
```

# Перелік Enum

У багатьох програмах існує обмежений набір значень.

Наприклад:

* dev
* test
* prod

Для цього використовується Enum.

# Створення Enum

```python
from enum import Enum

class Environment(Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"
```

# Використання Enum

```python
env = Environment.DEV

print(env.value)
```

Результат:

```text
dev
```

# Enum + argparse

```python
from enum import Enum
import argparse

class Environment(Enum):
    DEV = "dev"
    PROD = "prod"

parser = argparse.ArgumentParser()

parser.add_argument(
    "--env",
    choices=[e.value for e in Environment]
)

args = parser.parse_args()
```

Тепер користувач не зможе ввести неправильне значення.

# Змінні середовища

Environment Variables або env variables використовуються для:

* паролів;
* токенів;
* адрес серверів;
* конфігурації застосунку.

# Читання env змінної

```python
import os

host = os.getenv("DB_HOST")

print(host)
```

# Значення за замовчуванням

```python
import os

host = os.getenv(
    "DB_HOST",
    "localhost"
)

print(host)
```

# Встановлення змінної

Linux/macOS:

```bash
export DB_HOST=localhost
```

Windows:

```cmd
set DB_HOST=localhost
```

Запуск програми:

```bash
python app.py
```

# Навіщо потрібні env

Поганий варіант:

```python
DB_PASSWORD = "admin123"
```

Хороший варіант:

```python
DB_PASSWORD = os.getenv(
    "DB_PASSWORD"
)
```

Секрети не потрапляють у Git.

# Конфігураційні файли

Не всі параметри зручно зберігати в env.

Для цього використовують:

* ini
* yaml
* json
* toml

Почнемо з ini.

# Файл config.ini

```ini
[database]
host=localhost
port=5432

[application]
debug=true
```

# Модуль configparser

```python
import configparser

config = configparser.ConfigParser()

config.read("config.ini")

host = config["database"]["host"]

print(host)
```

# Читання чисел

```python
port = config.getint(
    "database",
    "port"
)

print(port)
```

# Читання булевих значень

```python
debug = config.getboolean(
    "application",
    "debug"
)

print(debug)
```

# Реальний сценарій

Типовий порядок завантаження конфігурації:

1. Значення за замовчуванням
2. config.ini
3. env variables
4. параметри командного рядка

Кожен наступний рівень має вищий пріоритет.

# Міні-проєкт

Створимо утиліту запуску застосунку.

Файл:

```ini
[app]
env=dev
host=localhost
port=8000
```

# Завантаження конфігурації

```python
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

host = config["app"]["host"]
port = config.getint("app", "port")

print(host)
print(port)
```

# Перевизначення через env

```python
import os

host = os.getenv(
    "APP_HOST",
    host
)
```

Тепер env має вищий пріоритет.

# Перевизначення через CLI

```python
parser.add_argument("--host")

args = parser.parse_args()

if args.host:
    host = args.host
```

CLI має найвищий пріоритет.

# Що таке Typer

Typer — сучасна бібліотека для створення CLI.

Побудована поверх Click.

Використовується у:

* FastAPI ecosystem
* внутрішніх інструментах
* DevOps утилітах

# Найпростіший приклад Typer

```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"Hello {name}")

app()
```

Запуск:

```bash
python app.py hello Alex
```

# Коли використовувати Typer

Для навчання:

* argparse

Для невеликих скриптів:

* argparse

Для великих CLI проєктів:

* Typer

Саме тому сьогодні основний акцент зроблено на стандартній бібліотеці Python.

# Підсумок

На цьому занятті ми:

* створювали CLI-застосунки;
* працювали з `argparse`;
* використовували `Enum`;
* читали env variables;
* працювали з `configparser`;
* будували багаторівневу систему конфігурації;
* ознайомилися з бібліотекою Typer.

Ці інструменти широко використовуються в Django, FastAPI, Docker, CI/CD та production-системах.
