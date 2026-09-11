# Заняття 18. SQLite та локальна база даних

## Зміст

1. Що таке база даних і навіщо вона потрібна
2. Реляційні бази даних і SQL
3. SQLite — вбудована БД у Python
4. Основні типи даних SQLite
5. DDL: створення таблиць і зовнішні ключі
6. DML: INSERT, SELECT, UPDATE, DELETE
7. JOIN: об'єднання таблиць
8. Практичний приклад: навчальний проєкт
9. Типові помилки
10. Підсумкова таблиця

## 1. Що таке база даних і навіщо вона потрібна

До цього моменту ми зберігали дані у файлах — JSON і CSV. Це підходить для невеликих обсягів і простих структур. Але вже при зростанні даних виникають проблеми:

- пошук по JSON-файлу — це читання всього файлу;
- фільтрація, сортування, підрахунок потребують написання власного Python-коду;
- зв'язки між об'єктами (наприклад, транзакція належить користувачу) реалізуються вручну через id у словниках;
- одночасна робота декількох процесів може пошкодити файл.

**База даних** (БД) — це організоване сховище даних, яке забезпечує ефективне зберігання, пошук, оновлення та видалення інформації.

**СУБД (система управління базами даних)** — програмне забезпечення, яке керує базою даних. Вона бере на себе всі операції з даними: зберігання на диску, пошук, транзакції, контроль цілісності.

Популярні СУБД:

| СУБД | Призначення |
|---|---|
| SQLite | локальна, вбудована, без сервера |
| PostgreSQL | потужна серверна СУБД, open source |
| MySQL / MariaDB | популярна у веб-розробці |
| Microsoft SQL Server | корпоративні рішення |

На цьому занятті ми починаємо з SQLite — вона вбудована у Python і не потребує жодних додаткових встановлень.

## 2. Реляційні бази даних і SQL

**Реляційна база даних** зберігає дані у вигляді таблиць. Таблиця — це рядки (записи) та стовпці (поля). Відносини між таблицями описуються через ключі.

Уявіть таблицю `users`:

| id | username | email |
|---|---|---|
| 1 | alice | alice@example.com |
| 2 | bob | bob@example.com |

І таблицю `issues` (задачі), де кожна задача належить певному користувачу:

| id | title | status | user_id |
|---|---|---|---|
| 1 | Fix login bug | Open | 1 |
| 2 | Write tests | Done | 2 |
| 3 | Update docs | Open | 1 |

Поле `user_id` у таблиці `issues` посилається на поле `id` таблиці `users`. Це і є **зв'язок між таблицями**.

**SQL (Structured Query Language)** — мова запитів для роботи з реляційними базами даних. SQL розділяється на кілька підмов:

| Підмова | Розшифрування | Команди |
|---|---|---|
| DDL | Data Definition Language | CREATE, ALTER, DROP |
| DML | Data Manipulation Language | INSERT, SELECT, UPDATE, DELETE |
| DCL | Data Control Language | GRANT, REVOKE |
| TCL | Transaction Control Language | COMMIT, ROLLBACK |

Сьогодні ми зосередимось на DDL і DML.

## 3. SQLite — вбудована БД у Python

SQLite — це легка реляційна БД, яка зберігає всі дані в одному файлі на диску (або цілком у пам'яті). Вона не потребує окремого сервера і вбудована у стандартну бібліотеку Python через модуль `sqlite3`.

**Коли використовувати SQLite:**
- прототипування та навчання;
- мобільні застосунки та desktop-програми;
- невеликі проєкти з помірним навантаженням;
- тестові середовища.

**Коли краще перейти на PostgreSQL/MySQL:**
- висока конкурентність (багато одночасних клієнтів);
- великі обсяги даних;
- складні транзакції та вимоги до надійності.

### Підключення до SQLite

```python
import sqlite3

# Підключення до файлу бази даних
# Якщо файл не існує — він буде створений автоматично
conn = sqlite3.connect("my_database.db")

# Отримання курсору — об'єкта для виконання запитів
cursor = conn.cursor()

# ... виконання запитів ...

# Закриття з'єднання
conn.close()
```

Краща практика — використовувати контекстний менеджер `with`. Він автоматично виконує `commit()` при успішному завершенні або `rollback()` при помилці:

```python
import sqlite3

with sqlite3.connect("my_database.db") as conn:
    cursor = conn.cursor()
    # ... виконання запитів ...
# conn.close() викликається автоматично
```

**База даних у пам'яті** — корисна для тестів, не зберігається після завершення програми:

```python
conn = sqlite3.connect(":memory:")
```

## 4. Основні типи даних SQLite

SQLite має спрощену систему типів порівняно з іншими СУБД:

| Тип SQLite | Відповідність Python | Опис |
|---|---|---|
| `INTEGER` | `int` | Ціле число |
| `REAL` | `float` | Число з плаваючою комою |
| `TEXT` | `str` | Рядок тексту |
| `BLOB` | `bytes` | Бінарні дані |
| `NULL` | `None` | Відсутність значення |

Важливо: SQLite використовує **динамічну типізацію** — тип прив'язаний до значення, а не до стовпця. На практиці це зазвичай не створює проблем, але потрібно мати на увазі.

## 5. DDL: створення таблиць і зовнішні ключі

### Первинний ключ (PRIMARY KEY)

Первинний ключ — це унікальний ідентифікатор кожного рядка таблиці. У SQLite найпоширеніший варіант — `INTEGER PRIMARY KEY AUTOINCREMENT`, який автоматично генерує числовий id для кожного нового запису.

### Створення таблиці

```python
import sqlite3

with sqlite3.connect("task_manager.db") as conn:
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL UNIQUE,
            email     TEXT    NOT NULL UNIQUE
        )
    """)

    conn.commit()
    print("Таблиця users створена")
```

Пояснення ключових слів:
- `CREATE TABLE IF NOT EXISTS` — створити таблицю, якщо вона ще не існує (захист від помилки при повторному запуску);
- `NOT NULL` — поле не може бути порожнім;
- `UNIQUE` — значення в стовпці мають бути унікальними.

### Зовнішні ключі (FOREIGN KEY)

Зовнішній ключ — це поле в одній таблиці, яке посилається на первинний ключ іншої таблиці. Він забезпечує **цілісність даних**: не можна додати задачу для неіснуючого користувача.

```python
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
""")
```

**Важливо:** SQLite за замовчуванням не виконує перевірку зовнішніх ключів. Щоб увімкнути її, потрібно виконати:

```python
cursor.execute("PRAGMA foreign_keys = ON")
```

Це потрібно робити **при кожному новому з'єднанні** з базою даних.

### Видалення таблиці

```python
cursor.execute("DROP TABLE IF EXISTS issues")
```

## 6. DML: INSERT, SELECT, UPDATE, DELETE

### INSERT — додавання записів

```python
# Додавання одного запису
cursor.execute(
    "INSERT INTO users (username, email) VALUES (?, ?)",
    ("alice", "alice@example.com")
)
conn.commit()

# Отримання id щойно доданого запису
print(cursor.lastrowid)  # наприклад, 1
```

**Параметризовані запити** (символ `?`) — це обов'язкова практика. Вони захищають від **SQL-ін'єкцій** — атаки, при якій зловмисник вставляє шкідливий SQL-код у рядок запиту.

Ніколи не робіть так:
```python
# НЕБЕЗПЕЧНО — SQL-ін'єкція
username = input("Введіть ім'я: ")
cursor.execute(f"INSERT INTO users (username) VALUES ('{username}')")
```

Завжди так:
```python
# БЕЗПЕЧНО — параметризований запит
cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
```

**Масове додавання** через `executemany`:

```python
users_data = [
    ("bob", "bob@example.com"),
    ("carol", "carol@example.com"),
    ("dave", "dave@example.com"),
]

cursor.executemany(
    "INSERT INTO users (username, email) VALUES (?, ?)",
    users_data
)
conn.commit()
```

### SELECT — читання записів

```python
# Отримати всі рядки
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)  # кожен рядок — це кортеж: (1, 'alice', 'alice@example.com')
```

**Методи отримання результатів:**

| Метод | Повертає |
|---|---|
| `fetchone()` | один рядок або `None` |
| `fetchmany(n)` | список із n рядків |
| `fetchall()` | список усіх рядків |

```python
# Отримати конкретні стовпці
cursor.execute("SELECT id, username FROM users")

# Отримати один запис
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
user = cursor.fetchone()
print(user)  # (1, 'alice', 'alice@example.com')

# Фільтрація
cursor.execute("SELECT * FROM issues WHERE status = ?", ("Open",))
open_issues = cursor.fetchall()

# Сортування
cursor.execute("SELECT * FROM issues ORDER BY deadline ASC")

# Обмеження кількості результатів
cursor.execute("SELECT * FROM issues LIMIT 10")

# Підрахунок
cursor.execute("SELECT COUNT(*) FROM issues WHERE status = 'Open'")
count = cursor.fetchone()[0]
print(f"Відкритих задач: {count}")
```

### Отримання результатів як словників

За замовчуванням SQLite повертає кортежі. Щоб отримувати словники, потрібно встановити `row_factory`:

```python
conn.row_factory = sqlite3.Row

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row["username"], row["email"])  # доступ за іменем стовпця
```

### UPDATE — оновлення записів

```python
cursor.execute(
    "UPDATE issues SET status = ? WHERE id = ?",
    ("Done", 1)
)
conn.commit()

# Перевірка кількості оновлених рядків
print(cursor.rowcount)  # 1
```

### DELETE — видалення записів

```python
cursor.execute("DELETE FROM issues WHERE id = ?", (3,))
conn.commit()

# Видалення всіх записів (але таблиця залишається)
cursor.execute("DELETE FROM issues")
conn.commit()
```

## 7. JOIN: об'єднання таблиць

JOIN — це операція, яка поєднує рядки з двох або більше таблиць на основі умови.

### Ситуація без JOIN

Щоб дізнатися, які задачі належать користувачу "alice", без JOIN довелося б:
1. Отримати id alice з таблиці users.
2. Виконати окремий запит до таблиці issues за цим id.

З JOIN це робиться одним запитом.

### INNER JOIN

Повертає тільки ті рядки, для яких умова об'єднання виконується в **обох** таблицях.

```python
cursor.execute("""
    SELECT
        issues.id,
        issues.title,
        issues.status,
        users.username
    FROM issues
    INNER JOIN users ON issues.user_id = users.id
""")

rows = cursor.fetchall()
for row in rows:
    print(row)
```

Результат: задачі разом з іменами їх авторів. Задачі без призначеного користувача (`user_id = NULL`) у результат **не потраплять**.

### LEFT JOIN

Повертає всі рядки з **лівої** таблиці, навіть якщо для них немає відповідності у правій.

```python
cursor.execute("""
    SELECT
        issues.id,
        issues.title,
        users.username
    FROM issues
    LEFT JOIN users ON issues.user_id = users.id
""")
```

Задачі без призначеного користувача будуть включені, але поле `username` буде `NULL`.

### Типи JOIN у SQL

| Тип | Що повертає |
|---|---|
| `INNER JOIN` | тільки збіги в обох таблицях |
| `LEFT JOIN` | усі з лівої + збіги з правої |
| `RIGHT JOIN` | усі з правої + збіги з лівої (у SQLite не підтримується) |
| `FULL OUTER JOIN` | усі рядки з обох таблиць (у SQLite не підтримується) |

На практиці `INNER JOIN` і `LEFT JOIN` покривають більшість потреб.

### Псевдоніми таблиць (аліаси)

Для скорочення запитів зручно використовувати аліаси:

```python
cursor.execute("""
    SELECT
        i.id,
        i.title,
        i.status,
        u.username
    FROM issues AS i
    INNER JOIN users AS u ON i.user_id = u.id
    WHERE i.status = 'Open'
    ORDER BY i.id
""")
```

## 8. Практичний приклад: навчальний проєкт

Зведемо все разом у повноцінний модуль роботи з базою даних для проєктних задач.

### Структура файлів

```
task_manager/
├── database.py      ← ініціалізація та підключення до БД
├── models.py        ← функції для роботи з даними
└── main.py          ← точка входу
```

### database.py — ініціалізація

```python
import sqlite3
from pathlib import Path

DB_PATH = Path("data") / "task_manager.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    NOT NULL UNIQUE,
                email    TEXT    NOT NULL UNIQUE
            )
        """)

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
        """)

        conn.commit()
        print("База даних ініціалізована")
```

### models.py — операції з даними

```python
import sqlite3
from database import get_connection


def create_user(username: str, email: str) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )
        conn.commit()
        return cursor.lastrowid


def get_all_users() -> list[sqlite3.Row]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY username")
        return cursor.fetchall()


def create_issue(
    title: str,
    issue_type: str = "Task",
    priority: str = "Medium",
    user_id: int | None = None
) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO issues (title, issue_type, priority, user_id)
            VALUES (?, ?, ?, ?)
            """,
            (title, issue_type, priority, user_id)
        )
        conn.commit()
        return cursor.lastrowid


def get_issues_with_users() -> list[sqlite3.Row]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                i.id,
                i.title,
                i.issue_type,
                i.priority,
                i.status,
                u.username AS assigned_to
            FROM issues AS i
            LEFT JOIN users AS u ON i.user_id = u.id
            ORDER BY i.id
        """)
        return cursor.fetchall()


def update_issue_status(issue_id: int, new_status: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE issues SET status = ? WHERE id = ?",
            (new_status, issue_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_issue(issue_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
        conn.commit()
        return cursor.rowcount > 0
```

### main.py — демонстрація

```python
from database import init_db
from models import (
    create_user,
    get_all_users,
    create_issue,
    get_issues_with_users,
    update_issue_status,
)


def main() -> None:
    init_db()

    # Створення користувачів
    alice_id = create_user("alice", "alice@example.com")
    bob_id = create_user("bob", "bob@example.com")

    # Створення задач
    create_issue("Fix login bug", issue_type="Bug", priority="High", user_id=alice_id)
    create_issue("Write unit tests", issue_type="Task", user_id=bob_id)
    create_issue("Update README", issue_type="Task", user_id=alice_id)

    # Виведення задач з іменами
    print("\n=== Задачі ===")
    issues = get_issues_with_users()
    for issue in issues:
        print(f"[{issue['id']}] {issue['title']} | {issue['issue_type']} | "
              f"{issue['status']} | {issue['assigned_to']}")

    # Зміна статусу
    update_issue_status(1, "Done")
    print("\nСтатус задачі #1 змінено на Done")

    # Повторний вивід
    print("\n=== Оновлені задачі ===")
    for issue in get_issues_with_users():
        print(f"[{issue['id']}] {issue['title']} | {issue['status']}")


if __name__ == "__main__":
    main()
```

## 9. Типові помилки

### 1. Забули викликати `commit()`

```python
# Неправильно
cursor.execute("INSERT INTO users (username) VALUES (?)", ("alice",))
# Дані не збережуться!

# Правильно
cursor.execute("INSERT INTO users (username) VALUES (?)", ("alice",))
conn.commit()
```

При використанні `with sqlite3.connect(...) as conn` commit відбувається автоматично, але тільки якщо блок завершився без винятку.

### 2. Конкатенація рядків замість параметрів

```python
# НЕБЕЗПЕЧНО
name = "alice'; DROP TABLE users; --"
cursor.execute(f"SELECT * FROM users WHERE username = '{name}'")

# БЕЗПЕЧНО
cursor.execute("SELECT * FROM users WHERE username = ?", (name,))
```

### 3. Передача одного значення без коми

```python
# Помилка — передається рядок, а не кортеж
cursor.execute("INSERT INTO users (username) VALUES (?)", ("alice"))

# Правильно — кортеж з одним елементом потребує коми
cursor.execute("INSERT INTO users (username) VALUES (?)", ("alice",))
```

### 4. Зовнішні ключі не перевіряються без PRAGMA

```python
# Перевірка вимкнена за замовчуванням!
# Можна вставити user_id = 9999, якого не існує

# Вмикаємо перевірку
conn.execute("PRAGMA foreign_keys = ON")
```

### 5. Не закрили з'єднання

```python
# Проблема: якщо виникне помилка між connect і close — з'єднання залишиться відкритим
conn = sqlite3.connect("db.sqlite3")
# ... щось пішло не так ...
conn.close()  # може не виконатись

# Правильно: використовуйте with
with sqlite3.connect("db.sqlite3") as conn:
    ...  # з'єднання закриється автоматично
```

## 10. Підсумкова таблиця

| Концепція | Команда / синтаксис | Призначення |
|---|---|---|
| Підключення | `sqlite3.connect("db.sqlite3")` | відкрити або створити БД |
| Курсор | `conn.cursor()` | об'єкт для виконання запитів |
| Створення таблиці | `CREATE TABLE IF NOT EXISTS` | DDL: структура таблиці |
| Зовнішній ключ | `FOREIGN KEY (col) REFERENCES table(id)` | зв'язок між таблицями |
| Увімкнення FK | `PRAGMA foreign_keys = ON` | активація перевірки зовнішніх ключів |
| Додавання | `INSERT INTO ... VALUES (?, ?)` | DML: новий запис |
| Читання | `SELECT ... FROM ... WHERE` | DML: вибірка даних |
| Оновлення | `UPDATE ... SET ... WHERE` | DML: зміна запису |
| Видалення | `DELETE FROM ... WHERE` | DML: видалення запису |
| Об'єднання | `INNER JOIN ... ON ...` | об'єднання таблиць за умовою |
| Ліве об'єднання | `LEFT JOIN ... ON ...` | всі з лівої + збіги з правої |
| Параметри | `(?, ?)` + `(val1, val2)` | захист від SQL-ін'єкцій |
| Фіксація | `conn.commit()` | зберегти зміни |
| Словники | `conn.row_factory = sqlite3.Row` | доступ до полів за іменем |
| Збереження змін | `cursor.rowcount` | кількість змінених рядків |
