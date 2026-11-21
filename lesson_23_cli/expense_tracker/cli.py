import argparse
from models import TransactionType


def build_parser(version: str = "0.3.0") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Expense Tracker — консольний менеджер особистих фінансів",
        epilog="Приклад: python main.py add --type expense --amount 250 --category Food",
    )
    parser.add_argument("--version", action="version", version=f"Expense Tracker v{version}")

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # --- команда: add ---
    add_parser = subparsers.add_parser("add", help="Додати дохід або витрату")
    add_parser.add_argument(
        "--type",
        dest="t_type",
        choices=[t.value for t in TransactionType],
        required=True,
        help="Тип транзакції: income або expense",
    )
    add_parser.add_argument("--amount", type=float, required=True, help="Сума транзакції")
    add_parser.add_argument("--category", required=True, help="Категорія (наприклад, Food, Salary)")
    add_parser.add_argument("--description", default="", help="Опис (необов'язково)")

    # --- команда: list ---
    list_parser = subparsers.add_parser("list", help="Показати список транзакцій")
    list_parser.add_argument(
        "--type",
        dest="t_type",
        choices=[t.value for t in TransactionType],
        help="Фільтр за типом (income / expense)",
    )
    list_parser.add_argument("--category", help="Фільтр за категорією")

    # --- команда: balance ---
    subparsers.add_parser("balance", help="Показати поточний баланс")

    # --- команда: report ---
    subparsers.add_parser("report", help="Місячний звіт за поточний місяць")

    # --- команда: delete ---
    delete_parser = subparsers.add_parser("delete", help="Видалити транзакцію за ID")
    delete_parser.add_argument("--id", type=int, required=True, help="ID транзакції")

    # --- команда: export ---
    export_parser = subparsers.add_parser("export", help="Експортувати транзакції у CSV або JSON")
    export_parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Формат файлу (за замовчуванням: csv)",
    )

    return parser
