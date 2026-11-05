from datetime import date

from database import get_connection


def create_user(username: str, email: str) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (username, email)
            VALUES (?, ?)
            """,
            (username, email)
        )

        conn.commit()
        return cursor.lastrowid


def add_transaction(
        user_id: int,
        amount: float,
        transaction_type: str,
        category: str,
        description: str
) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO transactions
            (amount, transaction_type, category, date, description, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                amount,
                transaction_type,
                category,
                date.today().isoformat(),
                description,
                user_id
            )
        )

        conn.commit()
        return cursor.lastrowid


def get_all_transactions(user_id: int) -> list:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM transactions
            WHERE user_id = ?
            ORDER BY id
            """,
            (user_id,)
        )

        return cursor.fetchall()


def get_balance(user_id: int) -> float:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'income'
                            THEN amount
                            ELSE -amount
                        END
                    ),
                    0
                ) AS balance
            FROM transactions
            WHERE user_id = ?
            """,
            (user_id,)
        )

        return cursor.fetchone()["balance"]


def get_expenses_by_category(user_id: int) -> list:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                category,
                SUM(amount) AS total
            FROM transactions
            WHERE user_id = ?
              AND transaction_type = 'expense'
            GROUP BY category
            ORDER BY total DESC
            """,
            (user_id,)
        )

        return cursor.fetchall()


def set_budget(
        user_id: int,
        category: str,
        monthly_limit: float
) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO budgets
            (category, monthly_limit, user_id)
            VALUES (?, ?, ?)
            """,
            (
                category,
                monthly_limit,
                user_id
            )
        )

        conn.commit()
        return cursor.lastrowid


def delete_transaction(transaction_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )

        conn.commit()

        return cursor.rowcount > 0