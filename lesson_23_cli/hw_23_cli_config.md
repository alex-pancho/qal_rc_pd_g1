# Домашнє завдання — Заняття 23
## CLI та конфігурація застосунків

**Олександр Панченко, ТОВ «Тренінг-центр КьюЕйЛайт»**

## Що потрібно зробити

На цьому занятті ви навчились перетворювати звичайний скрипт на повноцінний консольний інструмент. Сьогодні — **тільки доробка проєкту**: замінити інтерактивне меню `while True / input()` на CLI із підкомандами, додати конфігурацію через `.env` і `config.ini`.

## Що змінюється у проєкті

**Було** — інтерактивне меню:

```
1. Add task
2. Show tasks
3. Delete task
4. Exit
```

Користувач запускає програму і "застряє" всередині циклу. Неможливо автоматизувати, неможливо викликати з іншого скрипту.

**Стане** — CLI із підкомандами:

```bash
python main.py add --title "Fix login" --type Bug --priority High
python main.py list --status Open
python main.py delete --id 3
python main.py export --format csv
```

Кожна команда робить одну річ і завершується. Можна викликати з bash-скрипту, з тесту, з планувальника задач.

## Структура файлів після доробки

```
your_project/
├── main.py          ← точка входу, тільки CLI-парсинг
├── cli.py           ← визначення команд та аргументів (argparse)
├── config.py        ← завантаження налаштувань з .env і config.ini
├── models.py        ← @dataclass моделі (з заняття 22)
├── decorators.py    ← декоратори (з заняття 21)
├── storage.py       ← збереження у JSON/CSV (з заняття 17–18)
├── .env             ← секретні налаштування (не комітити в Git!)
├── config.ini       ← публічні налаштування
└── .gitignore       ← обов'язково додати .env
```

## Проєкт 1 — Task & Bug Manager

### Команди CLI

Реалізуйте наступний інтерфейс командного рядка:

```bash
# Додати задачу або баг
python main.py add --title "Fix login bug" --type Bug --priority High
python main.py add --title "Write unit tests" --type Task --priority Medium --deadline 2024-12-31

# Переглянути список
python main.py list
python main.py list --status Open
python main.py list --type Bug
python main.py list --priority High

# Змінити статус
python main.py status --id 3 --status "In Progress"

# Видалити
python main.py delete --id 3

# Експорт
python main.py export --format csv
python main.py export --format json

# Показати інформацію про програму
python main.py --version
python main.py --help
```

### Файл `cli.py`

```python
import argparse
from enum import Enum


class IssueType(Enum):
    TASK = "Task"
    BUG = "Bug"
    TEST_CASE = "TestCase"


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task-manager",
        description="Task & Bug Manager — консольний інструмент керування задачами",
        epilog="Приклад: python main.py add --title 'Fix bug' --type Bug --priority High",
    )
    parser.add_argument(
        "--version", action="version", version="Task Manager v0.3.0"
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # --- команда: add ---
    add_parser = subparsers.add_parser("add", help="Додати нову задачу або баг")
    add_parser.add_argument(
        "--title", required=True, help="Назва задачі"
    )
    add_parser.add_argument(
        "--type",
        dest="issue_type",
        choices=[t.value for t in IssueType],
        default=IssueType.TASK.value,
        help="Тип: Task, Bug, TestCase (за замовчуванням: Task)",
    )
    add_parser.add_argument(
        "--priority",
        choices=[p.value for p in Priority],
        default=Priority.MEDIUM.value,
        help="Пріоритет (за замовчуванням: Medium)",
    )
    add_parser.add_argument(
        "--deadline",
        metavar="YYYY-MM-DD",
        help="Дедлайн у форматі YYYY-MM-DD (необов'язково)",
    )
    # TODO: додати --assignee (ім'я відповідального)
    # TODO: додати --tags (через кому: "backend,auth,critical")

    # --- команда: list ---
    list_parser = subparsers.add_parser("list", help="Переглянути список задач")
    list_parser.add_argument(
        "--status",
        choices=[s.value for s in Status],
        help="Фільтр за статусом",
    )
    list_parser.add_argument(
        "--type",
        dest="issue_type",
        choices=[t.value for t in IssueType],
        help="Фільтр за типом",
    )
    list_parser.add_argument(
        "--priority",
        choices=[p.value for p in Priority],
        help="Фільтр за пріоритетом",
    )
    # TODO: додати --sort (за полем: priority, deadline, title)

    # --- команда: status ---
    status_parser = subparsers.add_parser("status", help="Змінити статус задачі")
    status_parser.add_argument("--id", type=int, required=True, help="ID задачі")
    status_parser.add_argument(
        "--status",
        choices=[s.value for s in Status],
        required=True,
        help="Новий статус",
    )

    # --- команда: delete ---
    delete_parser = subparsers.add_parser("delete", help="Видалити задачу")
    delete_parser.add_argument("--id", type=int, required=True, help="ID задачі")

    # --- команда: export ---
    export_parser = subparsers.add_parser("export", help="Експортувати дані")
    export_parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Формат експорту (за замовчуванням: csv)",
    )
    # TODO: додати --output (шлях до файлу)

    return parser
```

### Файл `config.py`

```python
import os
import configparser
from pathlib import Path


# --- Завантаження .env вручну (без python-dotenv) ---
def load_env(env_path: str = ".env") -> None:
    """
    Зчитує файл .env і додає змінні до os.environ.
    Ігнорує рядки, що починаються з # або порожні.
    """
    path = Path(env_path)
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


# --- Завантаження config.ini ---
def load_config(config_path: str = "config.ini") -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config


# --- Збірні налаштування застосунку ---
def get_settings() -> dict:
    load_env()
    config = load_config()

    return {
        # З .env — секретні або залежні від середовища
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "secret_key": os.getenv("SECRET_KEY", ""),  # TODO: використати у Занятті 44

        # З config.ini — публічні налаштування
        "data_file": config.get("storage", "data_file", fallback="issues.json"),
        "export_dir": config.get("storage", "export_dir", fallback="exports/"),
        "max_issues": config.getint("limits", "max_issues", fallback=1000),
        "app_name": config.get("app", "name", fallback="Task Manager"),
        "app_version": config.get("app", "version", fallback="0.3.0"),
    }
```

### Файл `.env`

```dotenv
# Налаштування середовища (не комітити в Git!)
DEBUG=true
LOG_LEVEL=DEBUG
SECRET_KEY=your-secret-key-here
```

### Файл `config.ini`

```ini
[app]
name = Task & Bug Manager
version = 0.3.0

[storage]
data_file = data/issues.json
export_dir = exports/

[limits]
max_issues = 1000
```

### Файл `main.py`

```python
import sys
import logging
from config import get_settings
from cli import build_parser
# from storage import Storage
# from models import Issue, IssueType, Priority, Status


def main():
    settings = get_settings()

    logging.basicConfig(
        level=settings["log_level"],
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("task_manager.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    parser = build_parser()
    args = parser.parse_args()

    # storage = Storage(settings["data_file"])

    if args.command == "add":
        # TODO: викликати storage.create_issue(...)
        print(f"✅ Додано: [{args.issue_type}] {args.title} | {args.priority}")

    elif args.command == "list":
        # TODO: отримати issues з storage, застосувати фільтри
        print("📋 Список задач (фільтри ще не підключені до storage)")

    elif args.command == "status":
        # TODO: storage.change_status(args.id, args.status)
        print(f"🔄 Статус задачі #{args.id} змінено на: {args.status}")

    elif args.command == "delete":
        # TODO: storage.delete_issue(args.id)
        print(f"🗑️  Задачу #{args.id} видалено")

    elif args.command == "export":
        # TODO: storage.export(args.format, settings["export_dir"])
        print(f"📤 Експорт у форматі {args.format.upper()} (ще не підключено)")


if __name__ == "__main__":
    main()
```

### `.gitignore` — обов'язково додати

```gitignore
.env
__pycache__/
*.pyc
*.log
exports/
data/
```

### Що перевірятиметься

- `python main.py --help` виводить список команд із описами
- `python main.py add --help` виводить аргументи команди `add`
- `python main.py add --title "Test" --type Bug --priority High` — виконується без помилок
- `python main.py list --status Open` — виконується без помилок
- `python main.py add` (без `--title`) — виводить помилку argparse, а не traceback
- Файл `.env` присутній, `.gitignore` містить `.env`
- `config.py` завантажує налаштування з обох джерел
- `config.ini` присутній із заповненими секціями

## Проєкт 2 — Expense & Budget Tracker

### Команди CLI

```bash
# Додати транзакцію
python main.py add income --amount 5000 --category Salary
python main.py add expense --amount 350 --category Food --desc "Обід у кафе"

# Переглянути
python main.py list
python main.py list --type expense
python main.py list --category Food
python main.py list --month 2024-03

# Баланс і звіт
python main.py balance
python main.py report --month 2024-03

# Бюджет
python main.py budget set --category Food --limit 3000
python main.py budget show

# Видалити
python main.py delete --id 5

# Експорт
python main.py export --format csv
python main.py export --format json

python main.py --version
```

### Файл `cli.py`

```python
import argparse
from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class ExportFormat(Enum):
    CSV = "csv"
    JSON = "json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Expense & Budget Tracker — облік доходів і витрат",
        epilog="Приклад: python main.py add expense --amount 350 --category Food",
    )
    parser.add_argument("--version", action="version", version="Expense Tracker v0.3.0")

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # --- команда: add ---
    add_parser = subparsers.add_parser("add", help="Додати транзакцію")
    add_parser.add_argument(
        "transaction_type",
        choices=[t.value for t in TransactionType],
        help="Тип: income або expense",
    )
    add_parser.add_argument("--amount", type=float, required=True, help="Сума")
    add_parser.add_argument("--category", required=True, help="Категорія")
    add_parser.add_argument("--desc", default="", help="Опис (необов'язково)")
    add_parser.add_argument("--date", metavar="YYYY-MM-DD", help="Дата (за замовчуванням: сьогодні)")
    # TODO: додати --currency (USD, EUR, UAH) для майбутнього @currency_aware

    # --- команда: list ---
    list_parser = subparsers.add_parser("list", help="Переглянути транзакції")
    list_parser.add_argument(
        "--type",
        dest="transaction_type",
        choices=[t.value for t in TransactionType],
        help="Фільтр за типом",
    )
    list_parser.add_argument("--category", help="Фільтр за категорією")
    list_parser.add_argument(
        "--month", metavar="YYYY-MM", help="Фільтр за місяцем"
    )
    # TODO: додати --sort (за датою або сумою)
    # TODO: додати --limit (кількість записів)

    # --- команда: balance ---
    subparsers.add_parser("balance", help="Показати поточний баланс")

    # --- команда: report ---
    report_parser = subparsers.add_parser("report", help="Місячний звіт")
    report_parser.add_argument(
        "--month", metavar="YYYY-MM", help="Місяць звіту (за замовчуванням: поточний)"
    )

    # --- команда: delete ---
    delete_parser = subparsers.add_parser("delete", help="Видалити транзакцію")
    delete_parser.add_argument("--id", type=int, required=True, help="ID транзакції")

    # --- команда: budget ---
    budget_parser = subparsers.add_parser("budget", help="Керування бюджетом")
    budget_sub = budget_parser.add_subparsers(dest="budget_command", metavar="SUBCOMMAND")
    budget_sub.required = True

    budget_set = budget_sub.add_parser("set", help="Встановити ліміт")
    budget_set.add_argument("--category", required=True, help="Категорія")
    budget_set.add_argument("--limit", type=float, required=True, help="Місячний ліміт")

    budget_sub.add_parser("show", help="Переглянути бюджети та використання")

    # --- команда: export ---
    export_parser = subparsers.add_parser("export", help="Експортувати дані")
    export_parser.add_argument(
        "--format",
        choices=[f.value for f in ExportFormat],
        default=ExportFormat.CSV.value,
        help="Формат (за замовчуванням: csv)",
    )

    return parser
```

### Файл `config.py`

```python
import os
import configparser
from pathlib import Path


def load_env(env_path: str = ".env") -> None:
    path = Path(env_path)
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def load_config(config_path: str = "config.ini") -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config


def get_settings() -> dict:
    load_env()
    config = load_config()

    return {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "base_currency": os.getenv("BASE_CURRENCY", "UAH"),  # TODO: Заняття 25 — exchange API
        "exchange_api_key": os.getenv("EXCHANGE_API_KEY", ""),  # TODO: Заняття 25

        "data_file": config.get("storage", "data_file", fallback="data/transactions.json"),
        "budget_file": config.get("storage", "budget_file", fallback="data/budgets.json"),
        "export_dir": config.get("storage", "export_dir", fallback="exports/"),
        "app_name": config.get("app", "name", fallback="Expense Tracker"),
        "app_version": config.get("app", "version", fallback="0.3.0"),
        "warn_budget_pct": config.getfloat("limits", "warn_budget_pct", fallback=80.0),
    }
```

### Файл `.env`

```dotenv
DEBUG=false
LOG_LEVEL=INFO
BASE_CURRENCY=UAH

# Буде використано у Занятті 25 (HTTP + API курсів валют)
EXCHANGE_API_KEY=
```

### Файл `config.ini`

```ini
[app]
name = Expense & Budget Tracker
version = 0.3.0

[storage]
data_file = data/transactions.json
budget_file = data/budgets.json
export_dir = exports/

[limits]
; Попередження при використанні X% від ліміту бюджету
warn_budget_pct = 80.0
```

### Файл `main.py`

```python
import logging
from config import get_settings
from cli import build_parser


def main():
    settings = get_settings()

    logging.basicConfig(
        level=settings["log_level"],
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("expense_tracker.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        # TODO: storage.add_transaction(...)
        sign = "+" if args.transaction_type == "income" else "-"
        print(f"✅ {sign}{args.amount} {settings['base_currency']} [{args.category}] додано")

    elif args.command == "list":
        # TODO: storage.list_transactions(type=..., category=..., month=...)
        print("📋 Транзакції (фільтри ще не підключені до storage)")

    elif args.command == "balance":
        # TODO: підрахувати баланс через storage
        print("💰 Баланс: (підключіть storage)")

    elif args.command == "report":
        # TODO: місячний звіт
        month = getattr(args, "month", None) or "поточний місяць"
        print(f"📊 Звіт за {month}: (підключіть storage)")

    elif args.command == "delete":
        # TODO: storage.delete_transaction(args.id)
        print(f"🗑️  Транзакцію #{args.id} видалено")

    elif args.command == "budget":
        if args.budget_command == "set":
            # TODO: storage.set_budget(args.category, args.limit)
            print(f"📌 Ліміт для '{args.category}': {args.limit} {settings['base_currency']}")
        elif args.budget_command == "show":
            # TODO: storage.list_budgets()
            print("📊 Бюджети: (підключіть storage)")

    elif args.command == "export":
        # TODO: storage.export(args.format, settings["export_dir"])
        print(f"📤 Експорт у форматі {args.format.upper()}")


if __name__ == "__main__":
    main()
```

### Що перевірятиметься

- `python main.py --help` і `python main.py add --help` — виводять підказки
- `python main.py add income --amount 5000 --category Salary` — виконується
- `python main.py add expense --amount abc --category Food` — argparse сам повідомляє про помилку типу
- `python main.py budget set --category Food --limit 3000` — виконується
- `python main.py add expense` (без `--amount`) — помилка argparse
- Налаштування `base_currency` та `warn_budget_pct` зчитуються з `.env` / `config.ini`

## Проєкт 3 — Service Management System

### Команди CLI

```bash
# Клієнти
python main.py client add --name "Іваненко Петро" --phone "+380991234567"
python main.py client list
python main.py client show --id 2

# Послуги
python main.py service add --name "Заміна масла" --price 800 --duration 30
python main.py service list

# Замовлення / записи
python main.py order create --client-id 1 --service-id 2
python main.py order list
python main.py order list --status "In Progress"
python main.py order status --id 3 --status Completed
python main.py order delete --id 3

# Звіт
python main.py report --period today
python main.py report --period month

# Експорт
python main.py export --format csv

python main.py --version
```

### Файл `cli.py`

```python
import argparse
from enum import Enum


class OrderStatus(Enum):
    CREATED = "Created"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class ReportPeriod(Enum):
    TODAY = "today"
    WEEK = "week"
    MONTH = "month"
    ALL = "all"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="service-manager",
        description="Service Management System — CRM для сервісу або клініки",
        epilog="Приклад: python main.py order create --client-id 1 --service-id 2",
    )
    parser.add_argument("--version", action="version", version="Service Manager v0.3.0")

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # ======= COMMAND: client =======
    client_parser = subparsers.add_parser("client", help="Керування клієнтами")
    client_sub = client_parser.add_subparsers(dest="client_command", metavar="SUBCOMMAND")
    client_sub.required = True

    client_add = client_sub.add_parser("add", help="Додати клієнта")
    client_add.add_argument("--name", required=True, help="Повне ім'я")
    client_add.add_argument("--phone", required=True, help="Номер телефону")
    client_add.add_argument("--email", default="", help="Email (необов'язково)")
    # TODO: додати --notes

    client_sub.add_parser("list", help="Список клієнтів")

    client_show = client_sub.add_parser("show", help="Деталі клієнта")
    client_show.add_argument("--id", type=int, required=True, help="ID клієнта")

    # ======= COMMAND: service =======
    service_parser = subparsers.add_parser("service", help="Каталог послуг")
    service_sub = service_parser.add_subparsers(dest="service_command", metavar="SUBCOMMAND")
    service_sub.required = True

    service_add = service_sub.add_parser("add", help="Додати послугу")
    service_add.add_argument("--name", required=True, help="Назва послуги")
    service_add.add_argument("--price", type=float, required=True, help="Вартість (грн)")
    service_add.add_argument("--duration", type=int, default=60, help="Тривалість (хв)")

    service_sub.add_parser("list", help="Список послуг")

    # ======= COMMAND: order =======
    order_parser = subparsers.add_parser("order", help="Замовлення / записи")
    order_sub = order_parser.add_subparsers(dest="order_command", metavar="SUBCOMMAND")
    order_sub.required = True

    order_create = order_sub.add_parser("create", help="Створити замовлення")
    order_create.add_argument("--client-id", type=int, required=True, help="ID клієнта")
    order_create.add_argument("--service-id", type=int, required=True, help="ID послуги")
    order_create.add_argument("--notes", default="", help="Нотатки")
    # TODO: додати --scheduled-at (дата і час запису)

    order_list = order_sub.add_parser("list", help="Список замовлень")
    order_list.add_argument(
        "--status",
        choices=[s.value for s in OrderStatus],
        help="Фільтр за статусом",
    )
    order_list.add_argument("--client-id", type=int, help="Фільтр за клієнтом")

    order_status = order_sub.add_parser("status", help="Змінити статус")
    order_status.add_argument("--id", type=int, required=True, help="ID замовлення")
    order_status.add_argument(
        "--status",
        choices=[s.value for s in OrderStatus],
        required=True,
        help="Новий статус",
    )

    order_delete = order_sub.add_parser("delete", help="Видалити замовлення")
    order_delete.add_argument("--id", type=int, required=True)

    # ======= COMMAND: report =======
    report_parser = subparsers.add_parser("report", help="Звіт по замовленнях")
    report_parser.add_argument(
        "--period",
        choices=[p.value for p in ReportPeriod],
        default=ReportPeriod.MONTH.value,
        help="Період (за замовчуванням: month)",
    )

    # ======= COMMAND: export =======
    export_parser = subparsers.add_parser("export", help="Експорт даних")
    export_parser.add_argument(
        "--format", choices=["csv", "json"], default="csv"
    )

    return parser
```

### Файл `config.py`

```python
import os
import configparser
from pathlib import Path


def load_env(env_path: str = ".env") -> None:
    path = Path(env_path)
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def load_config(config_path: str = "config.ini") -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config


def get_settings() -> dict:
    load_env()
    config = load_config()

    return {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "telegram_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),  # TODO: Заняття 25

        "clients_file": config.get("storage", "clients_file", fallback="data/clients.json"),
        "services_file": config.get("storage", "services_file", fallback="data/services.json"),
        "orders_file": config.get("storage", "orders_file", fallback="data/orders.json"),
        "export_dir": config.get("storage", "export_dir", fallback="exports/"),
        "currency": config.get("app", "currency", fallback="UAH"),
        "app_name": config.get("app", "name", fallback="Service Manager"),
        "app_version": config.get("app", "version", fallback="0.3.0"),
        "low_stock_threshold": config.getint("inventory", "low_stock_threshold", fallback=5),
    }
```

### Файл `.env`

```dotenv
DEBUG=false
LOG_LEVEL=INFO

# Буде використано у Занятті 25 (Telegram Bot — сповіщення клієнтів)
TELEGRAM_BOT_TOKEN=
```

### Файл `config.ini`

```ini
[app]
name = Service Management System
version = 0.3.0
currency = UAH

[storage]
clients_file = data/clients.json
services_file = data/services.json
orders_file = data/orders.json
export_dir = exports/

[inventory]
; Попередження при залишку менше X одиниць
low_stock_threshold = 5
```

### Файл `main.py`

```python
import logging
from config import get_settings
from cli import build_parser


def main():
    settings = get_settings()

    logging.basicConfig(
        level=settings["log_level"],
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("service_manager.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "client":
        if args.client_command == "add":
            # TODO: storage.add_client(args.name, args.phone, args.email)
            print(f"✅ Клієнта додано: {args.name} | {args.phone}")
        elif args.client_command == "list":
            # TODO: storage.list_clients()
            print("👥 Список клієнтів (підключіть storage)")
        elif args.client_command == "show":
            # TODO: storage.get_client(args.id)
            print(f"👤 Клієнт #{args.id} (підключіть storage)")

    elif args.command == "service":
        if args.service_command == "add":
            # TODO: storage.add_service(...)
            print(f"✅ Послугу додано: {args.name} — {args.price} {settings['currency']}")
        elif args.service_command == "list":
            print("🛠️  Список послуг (підключіть storage)")

    elif args.command == "order":
        if args.order_command == "create":
            # TODO: storage.create_order(args.client_id, args.service_id)
            print(f"✅ Замовлення створено: клієнт #{args.client_id}, послуга #{args.service_id}")
        elif args.order_command == "list":
            print("📋 Замовлення (підключіть storage)")
        elif args.order_command == "status":
            # TODO: storage.update_order_status(args.id, args.status)
            print(f"🔄 Статус замовлення #{args.id} → {args.status}")
        elif args.order_command == "delete":
            print(f"🗑️  Замовлення #{args.id} видалено")

    elif args.command == "report":
        print(f"📊 Звіт за період: {args.period} (підключіть storage)")

    elif args.command == "export":
        print(f"📤 Експорт у {args.format.upper()} (підключіть storage)")


if __name__ == "__main__":
    main()
```

### Що перевірятиметься

- `python main.py --help`, `python main.py client --help`, `python main.py order --help` — виводять підказки
- `python main.py client add --name "Іваненко" --phone "+380991234567"` — виконується
- `python main.py order create --client-id 1 --service-id 2` — виконується
- `python main.py order status --id 1 --status "Completed"` — виконується
- Вкладені підкоманди (`client add`, `order create`, `budget set`) — всі прописані
- `low_stock_threshold` зчитується з `config.ini`
- `TELEGRAM_BOT_TOKEN` присутній у `.env` (порожній — це нормально)

## Що здати (для всіх проєктів)

**Файли:**

```
your_project/
├── main.py
├── cli.py
├── config.py
├── config.ini
├── .env             ← з реальними (або порожніми) значеннями
└── .gitignore       ← .env обов'язково в списку
```

**Обов'язкові перевірки перед здачею:**

```bash
# 1. Загальна довідка
python main.py --help

# 2. Довідка по команді
python main.py add --help          # або client --help / order --help

# 3. Версія
python main.py --version

# 4. Виклик із правильними аргументами
python main.py add ...             # власний приклад

# 5. Виклик без обов'язкового аргументу — має дати помилку argparse, не traceback
python main.py add                 # або аналог для вашого проєкту
```

## Бонус (необов'язково)

Козацька рада вирішила: якщо скрипт запускається з прапором `--dry-run`, усі операції лише **виводяться на екран**, але не записуються у файл. Зручно для перевірки команд без змін у даних.

Додайте глобальний аргумент `--dry-run` до парсера і передайте його у `settings`. Усі команди, що модифікують дані, перевіряють `settings["dry_run"]` і або зберігають зміни, або виводять `[DRY RUN] Зміни не збережено`.

```bash
python main.py --dry-run add --title "Test" --type Bug --priority High
# [DRY RUN] Додано б: [Bug] Test | High — зміни не збережено
```

## Карта конфігурації: що звідки береться

| Налаштування | Де зберігати | Чому |
|---|---|---|
| `DEBUG`, `LOG_LEVEL` | `.env` | Залежить від середовища (dev/prod) |
| `SECRET_KEY`, `API_KEY`, токени | `.env` | Секрети не комітяться в Git |
| `data_file`, `export_dir` | `config.ini` | Публічні, можна комітити |
| `max_issues`, `warn_budget_pct` | `config.ini` | Публічна конфігурація |
| Назва і версія застосунку | `config.ini` | Публічна мета-інформація |
