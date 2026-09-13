import sqlite3
from pathlib import Path


def work_with_databese(db_file: Path) -> sqlite3.connect: 
    # Якщо файл не існує — він буде створений автоматично
    conn = sqlite3.connect(db_file)
    # conn.row_factory = sqlite3.Row # Щоб отримувати словники
    # Отримання курсору — об'єкта для виконання запитів
    cursor = conn.cursor()
    yield cursor, conn
    # Закриття з'єднання
    conn.close()


def create_table(cursor, conn):
    """
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL UNIQUE,
            email     TEXT    NOT NULL UNIQUE
        )
    """

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issues (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        title       TEXT    NOT NULL,
        description TEXT,
        issue_type  TEXT    NOT NULL DEFAULT 'Task',
        priority    TEXT    NOT NULL DEFAULT 'Medium',
        status      TEXT    NOT NULL DEFAULT 'Open',
        deadline    TEXT,
        user_id     INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """
    )
    conn.commit()


def insert_data(cursor, conn, username: str, email:str):
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email)
        )
    conn.commit()

def update_data(cursor, conn, _id: int, email:str):
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (email, _id)
        )
    conn.commit()


users_data = [
    ("bob", "bob@example.com"),
    ("carol", "carol@example.com"),
    ("dave", "dave@example.com"),
]

# cursor.executemany(
#     "INSERT INTO users (username, email) VALUES (?, ?)",
#     users_data
# )
# conn.commit()

def select(cursor, query:str):
    cursor.execute(query)
    return cursor.fetchall()

def row_output(results: dict):
    for v in results:
        print(*v)



if __name__ == "__main__":
    db_file = Path(__file__).parent / "my_database.db"
    cursor, conn = next(work_with_databese(db_file))
    create_table(cursor, conn)
    # for username, email in users_data:
    #     insert_data(cursor, conn, username, email)
    users = select(cursor, "SELECT * FROM users")
    print(users)
    issues = select(cursor, "SELECT * FROM issues")
    print(issues)
    users = select(cursor, "SELECT email, username FROM users")
    print(users)
    users = select(cursor, "SELECT * FROM users WHERE username = 'alice' OR id = 4")
    print("WHERE username = 'alice'", users)
    row_output(users)
    update_data(cursor, conn, 4, 'carol4@example.com')
    cursor.execute("DELETE FROM users WHERE id = ?", (3,))
    conn.commit()
