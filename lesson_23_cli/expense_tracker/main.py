import sys
import logging
from config import get_settings
from cli import build_parser
from models import User, Transaction, InvalidAmountError, TransactionNotFoundError
from storage import Budget


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

    parser = build_parser(version=settings["app_version"])
    args = parser.parse_args()

    user = User(settings["user_name"])
    budget = Budget(settings["data_file"])
    currency = settings["currency"]

    try:
        if args.command == "add":
            tx = Transaction(args.amount, args.t_type, args.category, args.description)
            saved = budget.add_transaction(tx)
            logging.info(f"[{user.username}] Додано #{saved.id}: {saved.transaction_type} {saved.amount} {currency}")
            print(f"✅ Додано транзакцію #{saved.id}: [{saved.transaction_type.upper()}] {saved.category} — {saved.amount:.2f} {currency}")

        elif args.command == "list":
            items = budget.list_transactions(t_type=args.t_type, category=args.category)
            if not items:
                print("Список транзакцій порожній.")
                return
            print(f"\n--- Транзакції ({user.username}) ---")
            for t in items:
                desc = f" ({t.description})" if t.description else ""
                print(f"#{t.id} | {t.date} | [{t.transaction_type.upper()}] {t.category}: {t.amount:.2f} {currency}{desc}")

        elif args.command == "balance":
            bal = budget.calculate_balance()
            print(f"💰 Поточний баланс ({user.username}): {bal:.2f} {currency}")

        elif args.command == "report":
            inc, exp = budget.monthly_report()
            print("\n--- Звіт за поточний місяць ---")
            print(f"📈 Доходи:  {inc:.2f} {currency}")
            print(f"📉 Витрати: {exp:.2f} {currency}")
            print(f"⚖️ Різниця: {inc - exp:.2f} {currency}")

        elif args.command == "delete":
            removed = budget.delete_transaction(args.id)
            logging.info(f"[{user.username}] Видалено транзакцію #{removed.id}")
            print(f"❌ Транзакцію #{removed.id} ({removed.category}, {removed.amount} {currency}) видалено.")

        elif args.command == "export":
            out_path = budget.export_data(args.format, settings["export_dir"])
            logging.info(f"Експортовано у {out_path}")
            print(f"📁 Дані успішно експортовано у файл: {out_path}")

    except (InvalidAmountError, TransactionNotFoundError) as e:
        logging.error(str(e))
        print(f"⚠️ Помилка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
