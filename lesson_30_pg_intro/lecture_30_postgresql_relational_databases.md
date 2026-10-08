# Заняття 30. Реляційні бази даних і PostgreSQL

**Тривалість:** 2 годин (1 година теорії + 1 година практики)

**Викладач:** Олександр Панченко / QALight  
**Курс:** Програмування Python · Модуль 5. PostgreSQL

## Цілі заняття

1. Розуміти архітектуру реляційних баз даних
2. Навчитися встановлювати та налаштовувати PostgreSQL
3. Опанувати концепції первинних та зовнішних ключів
4. Разобраться з типами даних PostgreSQL
5. Освоїти роботу з послідовностями (`SEQUENCE`, `SERIAL`)
6. Підключатися до PostgreSQL через Python за допомогою `psycopg`
7. Виконувати базові операції з курсорами та параметризованими запитами

## Частина 1. Теорія. Реляційні дані та архітектура

### 1.1. Що таке реляційна база даних?

**Реляційна база даних** — це структурована система зберігання інформації, в якій дані організовані в **таблиці** (відносини), що складаються з **рядків** та **стовпців**.

#### Основні поняття:

| Термін | Пояснення | Аналогія |
|--------|-----------|----------|
| **Таблиця** | Набір однотипних записів | Excel-документ |
| **Рядок** | Один запис | Один рядок таблиці |
| **Стовпець** | Поле з однойменним типом даних | Одна колонка таблиці |
| **Ключ** | Унікальний ідентифікатор рядка | ID користувача |
| **Схема** | Структура таблиць та їхніх зв'язків | План будівлі |

#### Приклад реляційної структури:

```
Таблиця: users
┌──────┬──────────┬────────────────────┐
│ id   │ name     │ email              │
├──────┼──────────┼────────────────────┤
│ 1    │ Іван     │ ivan@example.com   │
│ 2    │ Марія    │ maria@example.com  │
│ 3    │ Петро    │ petro@example.com  │
└──────┴──────────┴────────────────────┘

Таблиця: posts
┌──────┬──────────────┬─────────┐
│ id   │ title        │ user_id │
├──────┼──────────────┼─────────┤
│ 1    │ Привіт світе │ 1       │
│ 2    │ Перший пост  │ 2       │
│ 3    │ Друга стаття │ 1       │
└──────┴──────────────┴─────────┘
```

### 1.2. PostgreSQL як реляційна БД

**PostgreSQL** — це потужна, вільна та open-source реляційна СУБД. Вона надає:

✅ **ACID-гарантії** (атомарність, консистентність, ізоляція, довговічність)  
✅ **Складні типи даних** (JSON, масиви, діапазони, геометричні типи)  
✅ **Розширюваність** (користувацькі типи, функції, індекси)  
✅ **Безпеку** (аутентифікація, ролі, дозволи)  
✅ **Функціональність** (транзакції, представлення, збережені процедури)  

#### Переваги PostgreSQL:

- **Стабільність:** використовується у великих компаніях (Apple, Spotify, Instagram)
- **Сумісність:** працює на Linux, macOS, Windows
- **Сумісність із Python:** чудова бібліотека `psycopg`
- **Масштабованість:** підтримує гігабайти і терабайти даних

### 1.3. Первинні ключі (Primary Key)

**Первинний ключ** — це стовпець (або група стовпців), що унікально ідентифікує кожен рядок у таблиці.

#### Властивості первинного ключа:

| Властивість | Пояснення |
|-------------|-----------|
| **Унікальність** | Два рядки не можуть мати однаковий первинний ключ |
| **Обов'язковість** | Первинний ключ не може бути `NULL` |
| **Простота запитів** | Дозволяє швидко знаходити рядок по його ID |
| **Один на таблицю** | У кожної таблиці не більше одного первинного ключа |

#### Приклад у SQL:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,      -- Первинний ключ
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);
```

#### Типові варіанти первинного ключа:

1. **Автоінкремент** (найпоширеніший):
   ```sql
   id SERIAL PRIMARY KEY
   ```

2. **UUID** (для розподілених систем):
   ```sql
   id UUID PRIMARY KEY DEFAULT gen_random_uuid()
   ```

3. **Складений ключ** (з кількох стовпців):
   ```sql
   PRIMARY KEY (user_id, post_id)
   ```

### 1.4. Зовнішні ключі (Foreign Key)

**Зовнішній ключ** — це стовпець, що посилається на первинний ключ іншої таблиці. Це встановлює **зв'язок один-до-багатьох** між таблицями.

#### Приклад:

```
users (батьківська таблиця)
┌────┬──────────┐
│ id │ name     │
├────┼──────────┤
│ 1  │ Іван     │
│ 2  │ Марія    │
└────┴──────────┘

posts (дочірня таблиця)
┌────┬──────────────┬─────────┐
│ id │ title        │ user_id │  ← Зовнішній ключ
├────┼──────────────┼─────────┤
│ 1  │ Привіт світе │ 1       │  → Посилається на users.id = 1
│ 2  │ Перший пост  │ 2       │  → Посилається на users.id = 2
│ 3  │ Друга стаття │ 1       │  → Посилається на users.id = 1
└────┴──────────────┴─────────┘
```

#### SQL-синтаксис для зовнішнього ключа:

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### Каскадне видалення (CASCADE):

При видаленні користувача всі його пости видаляються автоматично:

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### Переваги зовнішніх ключів:

✅ **Цілісність даних** — унеможливлює видалення користувача з активними постами  
✅ **Консистентність** — гарантує, що пост завжди належить реальному користувачу  
✅ **Простота запитів** — дозволяє легко об'єднувати дані з кількох таблиць (JOIN)

### 1.5. Типи даних PostgreSQL

PostgreSQL підтримує широкий спектр типів даних:

#### Числові типи:

| Тип | Розмір | Діапазон | Приклад |
|-----|--------|----------|---------|
| `SMALLINT` | 2 байта | -32768 до 32767 | `age SMALLINT` |
| `INTEGER` (або `INT`) | 4 байта | -2,147,483,648 до 2,147,483,647 | `user_id INTEGER` |
| `BIGINT` | 8 байт | -9.2×10¹⁸ до 9.2×10¹⁸ | `large_number BIGINT` |
| `DECIMAL` / `NUMERIC` | змінний | До 131,072 цифр | `price DECIMAL(10,2)` |
| `REAL` | 4 байта | 6 десяткових цифр точності | `height REAL` |
| `DOUBLE PRECISION` | 8 байт | 15 десяткових цифр точності | `latitude DOUBLE PRECISION` |

#### Текстові типи:

| Тип | Опис | Приклад |
|-----|------|---------|
| `VARCHAR(n)` | Рядок до n символів | `name VARCHAR(100)` |
| `TEXT` | Рядок необмеженої довжини | `description TEXT` |
| `CHAR(n)` | Рядок фіксованої довжини n | `code CHAR(5)` |

#### Дата та час:

| Тип | Формат | Приклад |
|-----|--------|---------|
| `DATE` | YYYY-MM-DD | `birth_date DATE` |
| `TIME` | HH:MM:SS | `start_time TIME` |
| `TIMESTAMP` | YYYY-MM-DD HH:MM:SS | `created_at TIMESTAMP` |
| `INTERVAL` | Інтервал часу | `duration INTERVAL` |

#### Логічний тип:

| Тип | Значення | Приклад |
|-----|----------|---------|
| `BOOLEAN` | `TRUE`, `FALSE`, `NULL` | `is_active BOOLEAN DEFAULT TRUE` |

#### Спеціальні типи:

| Тип | Опис | Приклад |
|-----|------|---------|
| `JSON` / `JSONB` | JSON-об'єкти | `metadata JSONB` |
| `UUID` | Універсальний унікальний ідентифікатор | `id UUID PRIMARY KEY` |
| `ARRAY` | Масив елементів | `tags TEXT[]` |
| `BYTEA` | Бінарні дані | `image BYTEA` |

### 1.6. SEQUENCE та SERIAL

**SEQUENCE** — це об'єкт БД, що генерує послідовність унікальних чисел.

#### SERIAL (синтаксичний цукор):

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY
);
```

Еквівалентно:

```sql
CREATE SEQUENCE users_id_seq;
CREATE TABLE users (
    id INTEGER PRIMARY KEY DEFAULT nextval('users_id_seq')
);
```

#### Використання SEQUENCE напряму:

```sql
-- Створити послідовність
CREATE SEQUENCE product_ids START WITH 1000 INCREMENT BY 1;

-- Одержати наступне значення
SELECT nextval('product_ids');  -- Повертає 1000, 1001, 1002, ...

-- Вибрати поточне значення (без інкременту)
SELECT currval('product_ids');

-- Встановити послідовність на певне значення
SELECT setval('product_ids', 2000);
```

#### Типи SERIAL у PostgreSQL:

| Тип | Базовий тип | Розмір | Діапазон |
|-----|------------|--------|----------|
| `SMALLSERIAL` | `SMALLINT` | 2 байта | 1 до 32,767 |
| `SERIAL` | `INTEGER` | 4 байта | 1 до 2,147,483,647 |
| `BIGSERIAL` | `BIGINT` | 8 байт | 1 до 9,223,372,036,854,775,807 |

#### Приклад зі стартовим значенням:

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Вставляємо дані — id автоматично генерується
INSERT INTO orders DEFAULT VALUES;
INSERT INTO orders DEFAULT VALUES;
INSERT INTO orders DEFAULT VALUES;

-- Результат:
-- id = 1, created_at = 2024-01-15 14:30:00
-- id = 2, created_at = 2024-01-15 14:30:01
-- id = 3, created_at = 2024-01-15 14:30:02
```

### 1.7. Ролі, користувачі та дозволи

PostgreSQL використовує **ролі** для керування доступом.

#### Розрізнення в термінології:

- **Роль** — об'єкт в PostgreSQL, що може мати дозволи і властивості
- **Користувач** — це роль з правом входу (`LOGIN`)

#### Базові команди:

```sql
-- Створити користувача (з правом входу)
CREATE USER username WITH PASSWORD 'password';

-- Створити роль (без права входу)
CREATE ROLE role_name;

-- Надати дозволи
GRANT SELECT, INSERT, UPDATE ON users TO username;

-- Видалити дозволи
REVOKE DELETE ON users FROM username;

-- Список користувачів
\du
```

#### Типові ролі на проєкті:

```sql
-- Адміністратор (повні права)
CREATE USER admin WITH PASSWORD 'admin_password' SUPERUSER;

-- Розробник (читання та запис)
CREATE USER developer WITH PASSWORD 'dev_password';
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO developer;

-- Читач (лише читання)
CREATE USER reader WITH PASSWORD 'reader_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
```

## Частина 2. Практика. Встановлення та налаштування PostgreSQL

### 2.1. Встановлення PostgreSQL

#### На **Windows**:

1. Завантажити інсталер з https://www.postgresql.org/download/windows/
2. Запустити інсталер, обрати параметри:
   - **Port:** 5432 (за замовчуванням)
   - **Username:** postgres
   - **Password:** встановити свій пароль
3. Завершити інсталяцію
4. Перевірити: `psql --version`

#### На **macOS**:

```bash
# Через Homebrew (рекомендовано)
brew install postgresql@16

# Запустити PostgreSQL
brew services start postgresql@16

# Перевірити версію
psql --version
```

#### На **Linux** (Ubuntu/Debian):

```bash
# Оновити пакети
sudo apt update
sudo apt upgrade

# Встановити PostgreSQL
sudo apt install postgresql postgresql-contrib

# Запустити сервіс
sudo systemctl start postgresql

# Перевірити статус
sudo systemctl status postgresql

# Увійти як користувач postgres
sudo -u postgres psql
```

### 2.2. Базова конфігурація PostgreSQL

#### Вхід до інтерпретатора psql:

```bash
# Як користувач системи, підключитися як postgres
psql -U postgres

# Або в Linux (з правами sudo)
sudo -u postgres psql

# Задати пароль, якщо потрібен
psql -U postgres -W
```

#### Основні команди в psql:

| Команда | Опис |
|---------|------|
| `\l` або `\list` | Список всіх баз даних |
| `\c database_name` | Підключитися до БД |
| `\dt` | Список таблиць у поточній БД |
| `\d table_name` | Структура таблиці |
| `\du` | Список користувачів та ролей |
| `\q` | Вихід з psql |
| `\h` | Довідка по SQL-командам |
| `\timing` | Показати час виконання запитів |

#### Приклад сеансу:

```bash
$ psql -U postgres
psql (16.0)
Type "help" for help.

postgres=# CREATE DATABASE myapp;
CREATE DATABASE

postgres=# \l
                          List of databases
   Name    | Owner    | Encoding | Collate | Ctype | Access privileges
-----------+----------+----------+---------+-------+-------------------
 myapp     | postgres | UTF8     | C       | C     |
 postgres  | postgres | UTF8     | C       | C     |
 template0 | postgres | UTF8     | C       | C     |
 template1 | postgres | UTF8     | C       | C     |
(4 rows)

postgres=# \c myapp
You are now connected to database "myapp" as user "postgres".

myapp=# CREATE TABLE users (
myapp(#     id SERIAL PRIMARY KEY,
myapp(#     name VARCHAR(100) NOT NULL,
myapp(#     email VARCHAR(100) UNIQUE
myapp(# );
CREATE TABLE

myapp=# \dt
         List of relations
 Schema | Name  | Type  | Owner
--------+-------+-------+----------
 public | users | table | postgres
(1 row)

myapp=# \q
$
```

### 2.3. Встановлення psycopg та підключення з Python

#### Встановлення бібліотеки:

```bash
# Активувати віртуальне середовище
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\activate     # Windows

# Встановити psycopg3 (рекомендовано)
pip install psycopg[binary]

# Або psycopg2 (старіша версія, також робить)
pip install psycopg2-binary
```

#### Базове підключення (psycopg3):

```python
import psycopg

# Параметри підключення
connection_params = {
    "host": "localhost",      # IP-адреса серверу БД
    "port": 5432,             # Порт PostgreSQL
    "database": "myapp",      # Назва БД
    "user": "postgres",       # Користувач
    "password": "your_password"  # Пароль
}

# Підключитися до БД
try:
    with psycopg.connect(**connection_params) as conn:
        print("✅ Успішно підключені до PostgreSQL!")
        
        # Одержати курсор для виконання запитів
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"PostgreSQL версія: {version[0]}")
except psycopg.Error as e:
    print(f"❌ Помилка підключення: {e}")
```

#### Альтернативний спосіб з рядком підключення:

```python
import psycopg

# Рядок підключення (DSN — Data Source Name)
dsn = "postgresql://postgres:password@localhost:5432/myapp"

try:
    conn = psycopg.connect(dsn)
    print("✅ Підключені!")
except psycopg.Error as e:
    print(f"❌ Помилка: {e}")
finally:
    if conn:
        conn.close()
```

### 2.4. Курсори та параметризовані запити

#### Що таке курсор?

**Курсор** — це об'єкт, який дозволяє виконувати SQL-запити та отримувати результати.

#### Базова схема роботи з курсором:

```python
import psycopg

conn = psycopg.connect("postgresql://postgres:password@localhost:5432/myapp")

# Варіант 1: Явне управління курсором
cur = conn.cursor()

# Виконати запит
cur.execute("SELECT * FROM users;")

# Одержати результати
rows = cur.fetchall()
for row in rows:
    print(row)

# Закрити курсор та з'єднання
cur.close()
conn.close()
```

#### Варіант 2: Контекстний менеджер (РЕКОМЕНДОВАНО):

```python
import psycopg

# З'єднання автоматично закривається
with psycopg.connect("postgresql://postgres:password@localhost:5432/myapp") as conn:
    # Курсор автоматично закривається
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
```

#### Методи курсора:

| Метод | Опис |
|-------|------|
| `execute(query, params)` | Виконати запит |
| `fetchone()` | Одержати один рядок |
| `fetchall()` | Одержати всі рядки |
| `fetchmany(size)` | Одержати кілька рядків |
| `rowcount` | Кількість рядків, що набули впливу |
| `description` | Інформація про стовпці |

### 2.5. Параметризовані запити (SQL Injection Protection)

**Параметризовані запити** — це безпечний спосіб передачі значень у SQL-запит. Вони захищають від **SQL-ін'єкцій**.

#### ❌ НЕБЕЗПЕЧНО! Рядкова конкатенація:

```python
# НІКОЛИ не робіть так!
username = "admin'; DROP TABLE users; --"
query = f"SELECT * FROM users WHERE name = '{username}';"
cur.execute(query)  # 💥 SQL-ін'єкція!
```

#### ✅ БЕЗПЕЧНО! Параметризовані запити:

```python
import psycopg

conn = psycopg.connect("postgresql://postgres:password@localhost:5432/myapp")

with conn.cursor() as cur:
    # Спосіб 1: Заповнювачі %s
    username = "admin"
    cur.execute(
        "SELECT * FROM users WHERE name = %s;",
        (username,)
    )
    result = cur.fetchone()
    print(result)

    # Спосіб 2: Кілька параметрів
    name = "Іван"
    email = "ivan@example.com"
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s);",
        (name, email)
    )
    conn.commit()  # Зберегти зміни

    # Спосіб 3: Іменовані параметри
    user_id = 1
    cur.execute(
        "DELETE FROM users WHERE id = %(id)s;",
        {"id": user_id}
    )
    conn.commit()
```

#### Як параметризація захищає:

```
Небезпечний запит:
  SELECT * FROM users WHERE name = 'admin'; DROP TABLE users; --';
  ↓
  Видаляє всю таблицю! 💥

Безпечний запит:
  SELECT * FROM users WHERE name = %s;
  Параметр: ("admin'; DROP TABLE users; --",)
  ↓
  Шукає користувача з назвою буквально "admin'; DROP TABLE users; --"
  (не знаходить — і таблиця залишається цілою) ✅
```

### 2.6. Практичний приклад: Створення таблиці та роботи з даними

#### Завдання 1: Створити таблиці для проєкту завтаків

```python
import psycopg
from datetime import datetime

# Параметри підключення
DSN = "postgresql://postgres:password@localhost:5432/lesson_30"

# Крок 1: Створити БД
try:
    conn_template = psycopg.connect(
        "postgresql://postgres:password@localhost:5432/template1"
    )
    conn_template.autocommit = True
    with conn_template.cursor() as cur:
        cur.execute("DROP DATABASE IF EXISTS lesson_30;")
        cur.execute("CREATE DATABASE lesson_30;")
    conn_template.close()
    print("✅ БД створена")
except psycopg.Error as e:
    print(f"❌ Помилка: {e}")

# Крок 2: Підключитися до нової БД та створити таблиці
try:
    conn = psycopg.connect(DSN)
    
    with conn.cursor() as cur:
        # Таблиця користувачів
        cur.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        # Таблиця завтаків
        cur.execute("""
            CREATE TABLE tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        
        # Таблиця коментарів до завтаків
        cur.execute("""
            CREATE TABLE comments (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                task_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        
        conn.commit()
        print("✅ Таблиці створені")
        
except psycopg.Error as e:
    print(f"❌ Помилка при створенні таблиць: {e}")
    conn.rollback()
finally:
    conn.close()
```

#### Завдання 2: Вставити дані

```python
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/lesson_30"

try:
    conn = psycopg.connect(DSN)
    
    with conn.cursor() as cur:
        # Вставити користувачів
        users_data = [
            ("ivan_petrov", "ivan@example.com"),
            ("maria_sidorenko", "maria@example.com"),
            ("petro_shevchenko", "petro@example.com"),
        ]
        
        for username, email in users_data:
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s);",
                (username, email)
            )
        
        conn.commit()
        print("✅ Користувачі додані")
        
        # Вставити завтаки
        tasks_data = [
            ("Написати конспект", "Завершити конспект до заняття 30", 1),
            ("Придумати приклади", "Придумати 5 практичних прикладів", 1),
            ("Прочитати документацію", "Ознайомитися з docs.postgresql.org", 2),
            ("Зробити гарячий чай", "Заварити чай з імбиром", 3),
        ]
        
        for title, description, user_id in tasks_data:
            cur.execute(
                """INSERT INTO tasks (title, description, user_id) 
                   VALUES (%s, %s, %s);""",
                (title, description, user_id)
            )
        
        conn.commit()
        print("✅ Завтаки додані")
        
except psycopg.Error as e:
    print(f"❌ Помилка: {e}")
    conn.rollback()
finally:
    conn.close()
```

#### Завдання 3: Отримати дані з JOIN

```python
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/lesson_30"

try:
    conn = psycopg.connect(DSN)
    
    with conn.cursor() as cur:
        # Запит з JOIN для отримання завтаків з іменами користувачів
        cur.execute("""
            SELECT 
                t.id,
                t.title,
                u.username,
                t.status,
                t.created_at
            FROM tasks t
            JOIN users u ON t.user_id = u.id
            ORDER BY t.created_at DESC;
        """)
        
        rows = cur.fetchall()
        
        print("\n📋 Список завтаків з користувачами:\n")
        for row in rows:
            task_id, title, username, status, created_at = row
            print(f"ID: {task_id}")
            print(f"  Назва: {title}")
            print(f"  Користувач: {username}")
            print(f"  Статус: {status}")
            print(f"  Створено: {created_at}\n")
        
except psycopg.Error as e:
    print(f"❌ Помилка: {e}")
finally:
    conn.close()
```

#### Завдання 4: Оновити та видалити дані

```python
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/lesson_30"

try:
    conn = psycopg.connect(DSN)
    
    with conn.cursor() as cur:
        # Оновити статус завтака
        task_id = 1
        new_status = "completed"
        
        cur.execute(
            "UPDATE tasks SET status = %s WHERE id = %s;",
            (new_status, task_id)
        )
        conn.commit()
        print(f"✅ Завтак ID {task_id} оновлений на статус '{new_status}'")
        
        # Видалити завтак по ID
        task_id_to_delete = 4
        
        cur.execute(
            "DELETE FROM tasks WHERE id = %s;",
            (task_id_to_delete,)
        )
        conn.commit()
        print(f"✅ Завтак ID {task_id_to_delete} видалений")
        
except psycopg.Error as e:
    print(f"❌ Помилка: {e}")
    conn.rollback()
finally:
    conn.close()
```

### 2.7. Обробка помилок та Transactions (Транзакції)

**Транзакція** — це набір SQL-операцій, які виконуються як одне ціле. Або все виконується (`COMMIT`), або нічого не змінюється (`ROLLBACK`).

#### Приклад транзакції:

```python
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/lesson_30"

try:
    conn = psycopg.connect(DSN)
    
    # Автоматичний режим — кожна команда автоматично коммітиться
    # conn.autocommit = True
    
    with conn.cursor() as cur:
        # Мовна перевід грошей від користувача A до користувача B
        try:
            # Крок 1: Зменшити баланс користувача A
            cur.execute(
                "UPDATE users SET balance = balance - 100 WHERE id = %s;",
                (1,)
            )
            
            # Крок 2: Збільшити баланс користувача B
            cur.execute(
                "UPDATE users SET balance = balance + 100 WHERE id = %s;",
                (2,)
            )
            
            # Крок 3: Зафіксувати транзакцію
            conn.commit()
            print("✅ Транзакція успішна")
            
        except psycopg.Error as e:
            # Якщо помилка — відкотити всі зміни
            conn.rollback()
            print(f"❌ Помилка, транзакція скасована: {e}")
        
except psycopg.Error as e:
    print(f"❌ Помилка підключення: {e}")
finally:
    conn.close()
```

#### Робота з точками збереження (Savepoints):

```python
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/lesson_30"

conn = psycopg.connect(DSN)

try:
    with conn.cursor() as cur:
        # Крок 1: Вставити користувача
        cur.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s);",
            ("new_user", "new@example.com")
        )
        
        # Точка збереження
        conn.execute("SAVEPOINT step_1;")
        
        # Крок 2: Спроба додати поштовхнув з дублікатом email
        try:
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s);",
                ("another_user", "new@example.com")  # ← Помилка унікальності!
            )
        except psycopg.IntegrityError:
            # Скасувати тільки крок 2
            conn.execute("ROLLBACK TO SAVEPOINT step_1;")
            print("⚠️ Крок 2 скасований, але крок 1 залишився")
        
        # Крок 3: Вставити коректного користувача
        cur.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s);",
            ("another_user", "another@example.com")
        )
        
        conn.commit()
        print("✅ Транзакція успішна")
        
except psycopg.Error as e:
    conn.rollback()
    print(f"❌ Помилка: {e}")
finally:
    conn.close()
```

### 2.8. Інформаційна схема (Information Schema)

PostgreSQL зберігає інформацію про свою структуру у спеціальній таблиці `information_schema`.

#### Запити до інформаційної схеми:

```python
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/lesson_30"

conn = psycopg.connect(DSN)

with conn.cursor() as cur:
    # 1. Список всіх таблиць
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    tables = cur.fetchall()
    print("📊 Таблиці в БД:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # 2. Структура таблиці users
    cur.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'users';
    """)
    columns = cur.fetchall()
    print("\n🔍 Структура таблиці 'users':")
    for col_name, data_type, is_nullable in columns:
        nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
        print(f"  - {col_name}: {data_type} [{nullable}]")
    
    # 3. Зовнішні ключі
    cur.execute("""
        SELECT constraint_name, table_name, column_name
        FROM information_schema.key_column_usage
        WHERE table_schema = 'public' AND column_name LIKE '%_id';
    """)
    fks = cur.fetchall()
    print("\n🔗 Зовнішні ключі:")
    for constraint, table, column in fks:
        print(f"  - {table}.{column}")

conn.close()
```

## Частина 3. Домашнє завдання

### Завдання 1: Встановлення та налаштування (Обов'язкове)

1. **Встановіть PostgreSQL** на вашу машину (якщо ще не встановлено)
2. **Перевірте версію:**
   ```bash
   psql --version
   ```
3. **Запустіть psql та виконайте базові команди:**
   ```bash
   psql -U postgres
   postgres=# \l
   postgres=# SELECT version();
   postgres=# \q
   ```
4. **Встановіть psycopg:**
   ```bash
   pip install psycopg[binary]
   ```

### Завдання 2: Створення БД та таблиць (Обов'язкове)

Для вашого проєкту (Task Manager, Expense Tracker або Service Management) **створіть базу даних** та **мінімум 3 таблиці** з первинними та зовнішніми ключами.

#### Приклад для Project 1 (Task Manager):

```python
# db_setup.py
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/task_manager"

conn = psycopg.connect(DSN)

with conn.cursor() as cur:
    # Таблиця користувачів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    
    # Таблиця задач
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(50) DEFAULT 'open',
            priority VARCHAR(20) DEFAULT 'medium',
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    
    # Таблиця коментарів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            task_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    print("✅ Таблиці створені")

conn.close()
```

### Завдання 3: CRUD операції (Обов'язкове)

Напишіть функції для **CREATE, READ, UPDATE, DELETE** у вашому проєкті:

```python
# models.py
import psycopg
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    id: int
    username: str
    email: str

class UserRepository:
    def __init__(self, dsn: str):
        self.dsn = dsn
    
    def create(self, username: str, email: str) -> int:
        """Створити користувача, повернути ID"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id;",
                    (username, email)
                )
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id
    
    def read(self, user_id: int) -> Optional[User]:
        """Отримати користувача по ID"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, username, email FROM users WHERE id = %s;",
                    (user_id,)
                )
                row = cur.fetchone()
                if row:
                    return User(*row)
                return None
    
    def read_all(self) -> List[User]:
        """Отримати всіх користувачів"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, email FROM users;")
                return [User(*row) for row in cur.fetchall()]
    
    def update(self, user_id: int, username: str = None, email: str = None) -> bool:
        """Оновити користувача"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                if username and email:
                    cur.execute(
                        "UPDATE users SET username = %s, email = %s WHERE id = %s;",
                        (username, email, user_id)
                    )
                elif username:
                    cur.execute(
                        "UPDATE users SET username = %s WHERE id = %s;",
                        (username, user_id)
                    )
                elif email:
                    cur.execute(
                        "UPDATE users SET email = %s WHERE id = %s;",
                        (email, user_id)
                    )
                conn.commit()
                return cur.rowcount > 0
    
    def delete(self, user_id: int) -> bool:
        """Видалити користувача"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
                conn.commit()
                return cur.rowcount > 0
```

### Завдання 4: JOIN запити та агрегація (Обов'язкове)

Напишіть запити, що використовують **JOIN** та **агрегування**:

```python
def get_user_tasks_with_count(dsn: str):
    """Отримати користувачів та кількість їхніх завтаків"""
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    u.id,
                    u.username,
                    COUNT(t.id) as task_count,
                    COUNT(CASE WHEN t.status = 'open' THEN 1 END) as open_tasks
                FROM users u
                LEFT JOIN tasks t ON u.id = t.user_id
                GROUP BY u.id, u.username
                ORDER BY task_count DESC;
            """)
            
            for row in cur.fetchall():
                user_id, username, task_count, open_tasks = row
                print(f"{username}: {task_count} завтаків ({open_tasks} відкритих)")
```

### Завдання 5* (Бонус): Контекстний менеджер для БД

Напишіть власний контекстний менеджер для роботи з БД:

```python
from contextlib import contextmanager
import psycopg

@contextmanager
def get_db_connection(dsn: str):
    """Контекстний менеджер для безпечної роботи з БД"""
    conn = psycopg.connect(dsn)
    try:
        yield conn
    finally:
        conn.close()

# Використання:
with get_db_connection("postgresql://postgres:password@localhost:5432/myapp") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users;")
        for row in cur.fetchall():
            print(row)
```

## Підсумок

На цьому занятті ми:

✅ Розібралися з архітектурою реляційних БД  
✅ Встановили та налаштували PostgreSQL  
✅ Навчилися працювати з первинними та зовнішніми ключами  
✅ Вивчили типи даних PostgreSQL  
✅ Освоїли SEQUENCE та SERIAL  
✅ Підключилися до БД через Python (psycopg)  
✅ Виконали базові CRUD операції  
✅ Запустили параметризовані запити для захисту від SQL-ін'єкцій  
✅ Розібралися з транзакціями та обробкою помилок  

## Корисні посилання

- **PostgreSQL Документація:** https://www.postgresql.org/docs/current/
- **psycopg Документація:** https://www.psycopg.org/psycopg3/docs/
- **SQL Tutorial:** https://www.w3schools.com/sql/
- **PostgreSQL vs SQLite:** https://www.postgresql.org/about/featurematrix/

## Питання для самоперевірки

1. Що таке реляційна база даних? Дайте 3 приклади реальних систем, що використовують реляційні БД.
2. Чим відрізняється первинний ключ від зовнішнього ключа?
3. Що таке CASCADE в контексті зовнішнього ключа?
4. Навіщо потрібні параметризовані запити?
5. Що таке транзакція? Наведіть приклад, коли она необхідна.
6. Які переваги PostgreSQL над SQLite?
7. Як встановити PostgreSQL на ваш ОС?
8. Що таке SEQUENCE і коли його використовувати?
9. Як створити користувача та надати йому дозволи?
10. Що таке `SAVEPOINT` в PostgreSQL?

**Підготовано:** Олександр Панченко  
**Дата:** 2024  
**QALight Training Center**  
**Сертифікований курс Python**
