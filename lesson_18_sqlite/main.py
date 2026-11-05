from database import init_db
from models import (
    create_user,
    add_transaction,
    get_all_transactions,
    get_balance,
    get_expenses_by_category,
    set_budget,
)


def main():
    init_db()

    user_id = create_user(
        "olena",
        "olena@example.com"
    )

    add_transaction(
        user_id,
        15000,
        "income",
        "Salary",
        "Monthly salary"
    )

    add_transaction(
        user_id,
        450,
        "expense",
        "Food",
        "Groceries"
    )

    add_transaction(
        user_id,
        120,
        "expense",
        "Transport",
        "Bus tickets"
    )

    add_transaction(
        user_id,
        300,
        "expense",
        "Food",
        "Restaurant"
    )

    add_transaction(
        user_id,
        5000,
        "income",
        "Freelance",
        "Side project"
    )

    set_budget(
        user_id,
        "Food",
        2000
    )

    set_budget(
        user_id,
        "Transport",
        1000
    )

    print("=== Транзакції ===")

    transactions = get_all_transactions(user_id)

    for transaction in transactions:
        amount = transaction["amount"]

        if transaction["transaction_type"] == "income":
            sign = "+"
        else:
            sign = "-"

        print(
            f'[{transaction["id"]}] '
            f'{transaction["date"]} | '
            f'{transaction["transaction_type"]:8} | '
            f'{transaction["category"]:10} | '
            f'{sign}{amount:.2f}'
        )

    balance = get_balance(user_id)

    print()
    print(f"=== Баланс: {balance:.2f} ===")

    print()
    print("=== Витрати за категоріями ===")

    expenses = get_expenses_by_category(user_id)

    for expense in expenses:
        print(
            f'{expense["category"]:10} : '
            f'{expense["total"]:.2f}'
        )


if __name__ == "__main__":
    main()