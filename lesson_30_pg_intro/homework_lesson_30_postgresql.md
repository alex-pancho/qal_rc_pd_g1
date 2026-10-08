# Домашнє завдання. Заняття 30. Реляційні бази даних і PostgreSQL

**Курс:** Програмування Python · Модуль 5  
**Студент:** _______________  
**Дата здачі:** _______________  

## Частина A. Обов'язкові завдання

### Завдання 1. Встановлення PostgreSQL (Базове)

**Мета:** Встановити PostgreSQL на вашу машину та перевірити працездатність.

#### Кроки:

1. **Встановіть PostgreSQL** для вашої ОС:
   - **Windows:** https://www.postgresql.org/download/windows/
   - **macOS:** `brew install postgresql@16`
   - **Linux:** `sudo apt install postgresql postgresql-contrib`

2. **Перевірте версію:**
   ```bash
   psql --version
   ```

3. **Запустіть PostgreSQL**:
   - Windows: PostgreSQL автоматично стартує після інсталяції
   - macOS: `brew services start postgresql@16`
   - Linux: `sudo systemctl start postgresql`

4. **Підключіться до БД:**
   ```bash
   psql -U postgres
   ```

5. **Виконайте команди в psql:**
   ```sql
   \l              -- Список баз даних
   SELECT version();  -- Версія PostgreSQL
   \q              -- Вихід
   ```

6. **Створіть нову БД для тестування:**
   ```bash
   psql -U postgres -c "CREATE DATABASE lesson_30_test;"
   ```

#### Що здавати:
- Скріншот входу в psql та виводу `SELECT version();`
- Скріншот списку БД із командою `\l`
- Файл з назвою `INSTALLED.txt`, що містить текст "PostgreSQL установлена успішно"

### Завдання 2. Встановлення psycopg та перше підключення (Базове)

**Мета:** Підключитися до PostgreSQL з Python.

#### Кроки:

1. **Встановіть psycopg3:**
   ```bash
   pip install psycopg[binary]
   ```

2. **Напишіть скрипт `db_connection.py`:**

```python
# db_connection.py
import psycopg

# Параметри підключення
DSN = "postgresql://postgres:your_password@localhost:5432/lesson_30_test"

try:
    # Підключитися до БД
    with psycopg.connect(DSN) as conn:
        print("✅ Успішно підключені до PostgreSQL!")
        
        # Отримати інформацію про БД
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"\n📊 PostgreSQL версія:\n{version}\n")
            
            # Отримати інформацію про поточної користувача
            cur.execute("SELECT current_user;")
            user = cur.fetchone()[0]
            print(f"👤 Користувач: {user}")
            
            # Отримати поточну БД
            cur.execute("SELECT current_database();")
            database = cur.fetchone()[0]
            print(f"📁 Поточна БД: {database}")

except psycopg.Error as e:
    print(f"❌ Помилка підключення: {e}")
```

3. **Запустіть скрипт:**
   ```bash
   python db_connection.py
   ```

#### Що здавати:
- Файл `db_connection.py`
- Скріншот успішного виконання скрипту

### Завдання 3. Створення таблиць для вашого проєкту (Обов'язкове)

**Мета:** Спроєктувати та створити БД для вашого проєкту з первинними та зовнішніми ключами.

#### Обирайте один із трьох проектів:

#### **Варіант 1: Project 1 — Task & Bug Manager**

**Напишіть скрипт `db_schema_task_manager.py`:**

```python
# db_schema_task_manager.py
import psycopg

DSN = "postgresql://postgres:your_password@localhost:5432/task_manager"

def create_database():
    """Створити БД та таблиці"""
    
    try:
        # Крок 1: Підключитися до PostgreSQL і створити БД
        conn = psycopg.connect("postgresql://postgres:your_password@localhost:5432/template1")
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Видалити БД, якщо вже існує
            cur.execute("DROP DATABASE IF EXISTS task_manager;")
            # Створити нову БД
            cur.execute("CREATE DATABASE task_manager;")
        
        conn.close()
        print("✅ База даних task_manager створена")
        
        # Крок 2: Підключитися до нової БД і створити таблиці
        with psycopg.connect(DSN) as conn:
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
                
                # Таблиця задач/багів
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS issues (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        issue_type VARCHAR(50) NOT NULL,
                        priority VARCHAR(50) DEFAULT 'medium',
                        status VARCHAR(50) DEFAULT 'open',
                        deadline DATE,
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
                        issue_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW(),
                        FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    );
                """)
                
                conn.commit()
                print("✅ Таблиці users, issues, comments створені")
                
                # Крок 3: Вивести інформацію про створені таблиці
                cur.execute("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public';
                """)
                tables = cur.fetchall()
                print(f"\n📊 Таблиці в БД: {', '.join([t[0] for t in tables])}")
    
    except psycopg.Error as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    create_database()
```

#### **Варіант 2: Project 2 — Expense & Budget Tracker**

**Напишіть скрипт `db_schema_expense_tracker.py`:**

```python
# db_schema_expense_tracker.py
import psycopg

DSN = "postgresql://postgres:your_password@localhost:5432/expense_tracker"

def create_database():
    """Створити БД для Expense Tracker"""
    
    try:
        # Создать БД
        conn = psycopg.connect("postgresql://postgres:your_password@localhost:5432/template1")
        conn.autocommit = True
        
        with conn.cursor() as cur:
            cur.execute("DROP DATABASE IF EXISTS expense_tracker;")
            cur.execute("CREATE DATABASE expense_tracker;")
        
        conn.close()
        print("✅ База даних expense_tracker створена")
        
        # Таблиці
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                
                # Користувачі
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        currency VARCHAR(3) DEFAULT 'UAH',
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)
                
                # Категорії видатків
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS categories (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    );
                """)
                
                # Транзакції (доходи та видатки)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id SERIAL PRIMARY KEY,
                        amount DECIMAL(10, 2) NOT NULL,
                        transaction_type VARCHAR(20) NOT NULL,
                        category_id INTEGER,
                        description TEXT,
                        user_id INTEGER NOT NULL,
                        transaction_date DATE DEFAULT CURRENT_DATE,
                        created_at TIMESTAMP DEFAULT NOW(),
                        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    );
                """)
                
                # Бюджети
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS budgets (
                        id SERIAL PRIMARY KEY,
                        category_id INTEGER NOT NULL,
                        monthly_limit DECIMAL(10, 2) NOT NULL,
                        month DATE NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    );
                """)
                
                conn.commit()
                print("✅ Таблиці створені: users, categories, transactions, budgets")
    
    except psycopg.Error as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    create_database()
```

#### **Варіант 3: Project 3 — Service Management System**

**Напишіть скрипт `db_schema_service_manager.py`:**

```python
# db_schema_service_manager.py
import psycopg

DSN = "postgresql://postgres:your_password@localhost:5432/service_manager"

def create_database():
    """Створити БД для Service Management System"""
    
    try:
        # Создать БД
        conn = psycopg.connect("postgresql://postgres:your_password@localhost:5432/template1")
        conn.autocommit = True
        
        with conn.cursor() as cur:
            cur.execute("DROP DATABASE IF EXISTS service_manager;")
            cur.execute("CREATE DATABASE service_manager;")
        
        conn.close()
        print("✅ База даних service_manager створена")
        
        # Таблиці
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                
                # Клієнти
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS clients (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) NOT NULL,
                        phone VARCHAR(20),
                        email VARCHAR(100),
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)
                
                # Послуги
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS services (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) NOT NULL,
                        description TEXT,
                        price DECIMAL(10, 2) NOT NULL,
                        duration_minutes INTEGER,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)
                
                # Замовлення / Записи
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        id SERIAL PRIMARY KEY,
                        client_id INTEGER NOT NULL,
                        service_id INTEGER NOT NULL,
                        order_date DATE NOT NULL,
                        status VARCHAR(50) DEFAULT 'created',
                        total_price DECIMAL(10, 2) NOT NULL,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT NOW(),
                        FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
                        FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE RESTRICT
                    );
                """)
                
                # Інвентар (запчастини / матеріали)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS inventory (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) NOT NULL,
                        quantity INTEGER NOT NULL,
                        unit_price DECIMAL(10, 2),
                        min_quantity INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)
                
                conn.commit()
                print("✅ Таблиці створені: clients, services, orders, inventory")
    
    except psycopg.Error as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    create_database()
```

#### Що здавати для Завдання 3:
- Скрипт `db_schema_[project_name].py`
- Скріншот успішного виконання скрипту
- Команда `\d` для кожної таблиці (структура таблиць) — скопіювати до файлу `schema_info.txt`

### Завдання 4. CRUD операції (Обов'язкове)

**Мета:** Реалізувати базові операції: Create, Read, Update, Delete.

**Напишіть скрипт `crud_operations.py` для вашого проєкту:**

```python
# crud_operations.py
import psycopg
from dataclasses import dataclass
from typing import Optional, List

# Виберіть необхідний DSN для вашого проєкту
# DSN = "postgresql://postgres:password@localhost:5432/task_manager"
# DSN = "postgresql://postgres:password@localhost:5432/expense_tracker"
# DSN = "postgresql://postgres:password@localhost:5432/service_manager"

@dataclass
class User:
    id: int
    username: str
    email: str

class UserRepository:
    """Репозиторій для роботи з користувачами"""
    
    def __init__(self, dsn: str):
        self.dsn = dsn
    
    def create(self, username: str, email: str) -> int:
        """Створити користувача, повернути ID"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id;",
                        (username, email)
                    )
                    user_id = cur.fetchone()[0]
                    conn.commit()
                    return user_id
                except psycopg.IntegrityError as e:
                    print(f"❌ Помилка: користувач з таким username або email вже існує")
                    return None
    
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
                else:
                    return False
                
                conn.commit()
                return cur.rowcount > 0
    
    def delete(self, user_id: int) -> bool:
        """Видалити користувача"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
                conn.commit()
                return cur.rowcount > 0

# Тестування CRUD операцій
if __name__ == "__main__":
    DSN = "postgresql://postgres:your_password@localhost:5432/task_manager"
    repo = UserRepository(DSN)
    
    print("=== CRUD ОПЕРАЦІЇ ===\n")
    
    # CREATE
    print("📝 CREATE — додавання користувачів:")
    user_id_1 = repo.create("ivan_petrov", "ivan@example.com")
    user_id_2 = repo.create("maria_sidorenko", "maria@example.com")
    print(f"✅ Користувачі створені: ID {user_id_1}, {user_id_2}\n")
    
    # READ ONE
    print("📖 READ — отримання користувача:")
    user = repo.read(user_id_1)
    if user:
        print(f"✅ {user.username}: {user.email}\n")
    
    # READ ALL
    print("📚 READ ALL — отримання всіх користувачів:")
    users = repo.read_all()
    for u in users:
        print(f"  - {u.username} ({u.email})")
    print()
    
    # UPDATE
    print("✏️  UPDATE — оновлення користувача:")
    success = repo.update(user_id_1, email="newemail@example.com")
    if success:
        print(f"✅ Користувач оновлений\n")
    
    # DELETE
    print("🗑️  DELETE — видалення користувача:")
    success = repo.delete(user_id_2)
    if success:
        print(f"✅ Користувач видалений\n")
    
    # Фінальна перевірка
    print("📊 Фінальний список користувачів:")
    users = repo.read_all()
    for u in users:
        print(f"  - {u.username} ({u.email})")
```

#### Що здавати:
- Файл `crud_operations.py`
- Скріншот успішного виконання скрипту

### Завдання 5. Параметризовані запити (Обов'язкове)

**Мета:** Продемонструвати захист від SQL-ін'єкцій.

**Напишіть скрипт `parameterized_queries.py`:**

```python
# parameterized_queries.py
import psycopg

DSN = "postgresql://postgres:your_password@localhost:5432/task_manager"

def demonstrate_sql_injection():
    """Показати різницю між небезпечним та безпечним кодом"""
    
    print("=== ПАРАМЕТРИЗОВАНІ ЗАПИТИ ===\n")
    
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            
            # Тестові дані
            print("1️⃣  Вставляємо тестові дані:\n")
            
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s);",
                ("alice_wonderland", "alice@example.com")
            )
            conn.commit()
            print("✅ Вставлено: alice_wonderland\n")
            
            # Безпечний пошук (параметризований запит)
            print("2️⃣  БЕЗПЕЧНИЙ пошук за username:\n")
            search_username = "alice_wonderland"
            
            cur.execute(
                "SELECT id, username, email FROM users WHERE username = %s;",
                (search_username,)
            )
            result = cur.fetchone()
            if result:
                print(f"✅ Знайдено: {result}\n")
            
            # Небезпечна спроба (мовна ілюстрація — НЕ виконуємо!)
            print("3️⃣  НЕБЕЗПЕЧНИЙ код (для демонстрації):\n")
            print("❌ НІКОЛИ не робіть так:")
            dangerous_username = "admin'; DROP TABLE users; --"
            dangerous_query = f"SELECT * FROM users WHERE username = '{dangerous_username}';"
            print(f"   {dangerous_query}")
            print("   ^ Це видалить всю таблицю користувачів!\n")
            
            # Правильний способ з параметрами
            print("✅ ПРАВИЛЬНО з параметрами:")
            print("   cur.execute(")
            print("       \"SELECT * FROM users WHERE username = %s;\",")
            print(f"       ('{dangerous_username}',)")
            print("   )")
            print("   ^ Шукає користувача з буквальною назвою, тому безпечно\n")
            
            # Приклад з кількома параметрами
            print("4️⃣  Приклад з кількома параметрами:\n")
            
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s);",
                ("bob_builder", "bob@example.com")
            )
            conn.commit()
            
            # Оновлення з кількома параметрами
            cur.execute(
                "UPDATE users SET email = %s WHERE username = %s;",
                ("bob.new@example.com", "bob_builder")
            )
            conn.commit()
            print("✅ Оновлено: bob_builder → bob.new@example.com\n")
            
            # Видалення з параметром
            cur.execute(
                "DELETE FROM users WHERE username = %s;",
                ("bob_builder",)
            )
            conn.commit()
            print("✅ Видалено: bob_builder\n")

if __name__ == "__main__":
    try:
        demonstrate_sql_injection()
    except psycopg.Error as e:
        print(f"❌ Помилка: {e}")
```

#### Що здавати:
- Файл `parameterized_queries.py`
- Скріншот виконання

## Частина B. Розширені завдання

### Завдання 6. JOIN запити (Середня складність)

**Мета:** Написати запити з об'єднанням таблиць.

**Додайте до вашого проєкту скрипт `join_queries.py`:**

```python
# join_queries.py
import psycopg

DSN = "postgresql://postgres:your_password@localhost:5432/task_manager"

def demonstrate_joins():
    """Показати різні типи JOIN запитів"""
    
    print("=== JOIN ЗАПИТИ ===\n")
    
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            
            # Крок 1: Вставити тестові дані
            print("1️⃣  Вставляємо тестові дані:\n")
            
            # Користувачі
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s);",
                ("alice", "alice@example.com")
            )
            user_id_1 = cur.lastrowid if hasattr(cur, 'lastrowid') else 1
            
            # Отримати ID останнього користувача
            cur.execute("SELECT id FROM users WHERE username = %s;", ("alice",))
            user_id_1 = cur.fetchone()[0]
            
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s);",
                ("bob", "bob@example.com")
            )
            cur.execute("SELECT id FROM users WHERE username = %s;", ("bob",))
            user_id_2 = cur.fetchone()[0]
            
            # Завдання для alice
            cur.execute(
                "INSERT INTO issues (title, issue_type, user_id) VALUES (%s, %s, %s);",
                ("Задача 1", "Task", user_id_1)
            )
            
            cur.execute(
                "INSERT INTO issues (title, issue_type, user_id) VALUES (%s, %s, %s);",
                ("Баг 1", "Bug", user_id_1)
            )
            
            # Завдання для bob
            cur.execute(
                "INSERT INTO issues (title, issue_type, user_id) VALUES (%s, %s, %s);",
                ("Задача 2", "Task", user_id_2)
            )
            
            conn.commit()
            print("✅ Дані додані\n")
            
            # Крок 2: INNER JOIN
            print("2️⃣  INNER JOIN — користувачі з їхніми завданнями:\n")
            
            cur.execute("""
                SELECT u.username, i.title, i.issue_type
                FROM users u
                INNER JOIN issues i ON u.id = i.user_id
                ORDER BY u.username;
            """)
            
            for username, title, issue_type in cur.fetchall():
                print(f"  {username}: {title} [{issue_type}]")
            print()
            
            # Крок 3: LEFT JOIN
            print("3️⃣  LEFT JOIN — користувачі та їхні завдання (включно без завдань):\n")
            
            cur.execute("""
                SELECT u.username, COUNT(i.id) as task_count
                FROM users u
                LEFT JOIN issues i ON u.id = i.user_id
                GROUP BY u.id, u.username;
            """)
            
            for username, count in cur.fetchall():
                print(f"  {username}: {count} завдань")
            print()
            
            # Крок 4: Агрегування
            print("4️⃣  Агрегування — статистика по користувачам:\n")
            
            cur.execute("""
                SELECT 
                    u.username,
                    COUNT(i.id) as total_issues,
                    SUM(CASE WHEN i.status = 'open' THEN 1 ELSE 0 END) as open_issues
                FROM users u
                LEFT JOIN issues i ON u.id = i.user_id
                GROUP BY u.id, u.username
                ORDER BY total_issues DESC;
            """)
            
            for username, total, open_count in cur.fetchall():
                print(f"  {username}: всього {total}, відкритих {open_count}")

if __name__ == "__main__":
    try:
        demonstrate_joins()
    except psycopg.Error as e:
        print(f"❌ Помилка: {e}")
```

#### Що здавати:
- Файл `join_queries.py`
- Скріншот виконання

### Завдання 7. Транзакції та обробка помилок (Середня складність)

**Мета:** Продемонструвати транзакції та ROLLBACK.

**Напишіть скрипт `transactions.py`:**

```python
# transactions.py
import psycopg

DSN = "postgresql://postgres:your_password@localhost:5432/task_manager"

def demonstrate_transactions():
    """Показати як працюють транзакції"""
    
    print("=== ТРАНЗАКЦІЇ ===\n")
    
    # Приклад 1: Успішна транзакція
    print("1️⃣  Успішна транзакція:\n")
    
    try:
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                # Крок 1: Вставити користувача
                cur.execute(
                    "INSERT INTO users (username, email) VALUES (%s, %s);",
                    ("charlie", "charlie@example.com")
                )
                print("  ✓ Крок 1: користувач додан")
                
                # Крок 2: Отримати ID користувача
                cur.execute("SELECT id FROM users WHERE username = %s;", ("charlie",))
                user_id = cur.fetchone()[0]
                
                # Крок 3: Додати завдання користувачу
                cur.execute(
                    "INSERT INTO issues (title, issue_type, user_id) VALUES (%s, %s, %s);",
                    ("Перше завдання", "Task", user_id)
                )
                print("  ✓ Крок 2: завдання додане")
                
                # Коміт — зберегти обидві операції
                conn.commit()
                print("  ✓ Крок 3: COMMIT — обидві операції збережені\n")
    
    except psycopg.Error as e:
        print(f"  ❌ Помилка: {e}\n")
    
    # Приклад 2: Транзакція з помилкою та ROLLBACK
    print("2️⃣  Транзакція з помилкою (ROLLBACK):\n")
    
    try:
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                try:
                    # Крок 1: Вставити користувача
                    cur.execute(
                        "INSERT INTO users (username, email) VALUES (%s, %s);",
                        ("david", "david@example.com")
                    )
                    print("  ✓ Крок 1: користувач додан (david)")
                    
                    # Крок 2: Спроба додати користувача з дублікатом email
                    cur.execute(
                        "INSERT INTO users (username, email) VALUES (%s, %s);",
                        ("eve", "david@example.com")  # ← Email конфлікт!
                    )
                    print("  ✓ Крок 2: це не виконається...")
                    
                    conn.commit()
                
                except psycopg.IntegrityError as e:
                    # Помилка унікальності — ROLLBACK
                    conn.rollback()
                    print(f"  ❌ Помилка унікальності: {e}")
                    print("  ↻  ROLLBACK — обидві операції скасовані\n")
    
    except psycopg.Error as e:
        print(f"❌ Помилка підключення: {e}\n")
    
    # Приклад 3: Перевірка результатів
    print("3️⃣  Перевірка результатів:\n")
    
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT username, email FROM users 
                WHERE username IN ('charlie', 'david', 'eve')
                ORDER BY username;
            """)
            
            users = cur.fetchall()
            if users:
                print("  Користувачі в БД:")
                for username, email in users:
                    print(f"    - {username}: {email}")
                print("\n  ✅ charlie додан успішно")
                print("  ❌ david і eve НЕ додані (ROLLBACK вступив у силу)")
            else:
                print("  ❌ Немає користувачів")

if __name__ == "__main__":
    demonstrate_transactions()
```

#### Що здавати:
- Файл `transactions.py`
- Скріншот виконання

## Частина C. Бонус завдання

### Завдання 8* (Бонус). Контекстний менеджер для БД

**Мета:** Напишіть власний контекстний менеджер для безпечної роботи з БД.

```python
# db_context_manager.py
from contextlib import contextmanager
import psycopg
from typing import Generator

@contextmanager
def get_db_connection(dsn: str) -> Generator:
    """
    Контекстний менеджер для безпечної роботи з БД.
    
    Використання:
        with get_db_connection(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users;")
    """
    conn = psycopg.connect(dsn)
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_db_cursor(dsn: str) -> Generator:
    """
    Контекстний менеджер для отримання курсора прямо.
    
    Використання:
        with get_db_cursor(DSN) as cur:
            cur.execute("SELECT * FROM users;")
    """
    conn = psycopg.connect(dsn)
    try:
        cur = conn.cursor()
        yield cur
    finally:
        cur.close()
        conn.close()

# Тестування
if __name__ == "__main__":
    DSN = "postgresql://postgres:password@localhost:5432/task_manager"
    
    print("=== КОНТЕКСТНИЙ МЕНЕДЖЕР ===\n")
    
    # Варіант 1
    print("1️⃣  Використання get_db_connection:\n")
    with get_db_connection(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users;")
            count = cur.fetchone()[0]
            print(f"  Всього користувачів: {count}\n")
    
    # Варіант 2
    print("2️⃣  Використання get_db_cursor:\n")
    with get_db_cursor(DSN) as cur:
        cur.execute("SELECT username FROM users LIMIT 3;")
        for row in cur.fetchall():
            print(f"  - {row[0]}")
```

#### Що здавати:
- Файл `db_context_manager.py`

### Завдання 9* (Бонус). Information Schema

**Мета:** Написати скрипт, що аналізує структуру БД.

```python
# information_schema.py
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/task_manager"

def analyze_database():
    """Аналізувати структуру БД через information_schema"""
    
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            
            print("=== АНАЛІЗ СТРУКТУРИ БД ===\n")
            
            # Таблиці
            print("📊 Таблиці:\n")
            cur.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            
            tables = cur.fetchall()
            for table in tables:
                table_name = table[0]
                print(f"  📋 {table_name}")
                
                # Стовпці кожної таблиці
                cur.execute("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                """, (table_name,))
                
                for col_name, data_type, is_nullable in cur.fetchall():
                    nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                    print(f"      • {col_name}: {data_type} [{nullable}]")
                print()

if __name__ == "__main__":
    analyze_database()
```

#### Що здавати:
- Файл `information_schema.py`

## Частина D. Підсумкова перевірка

### Чек-лист перед здачею:

- [ ] Встановлена PostgreSQL
- [ ] Встановлений psycopg
- [ ] Створена БД для вашого проєкту
- [ ] Створені таблиці з FK та PK
- [ ] Реалізовані CRUD операції
- [ ] Написані параметризовані запити
- [ ] Протестовані транзакції
- [ ] Всі файли скопійовані в папку `outputs/`
- [ ] Написана стаття у файлі `REFLECTION.md` про ваші навчання

### Файли для здачі:

```
lesson_30_homework/
├── db_connection.py
├── db_schema_[project_name].py
├── crud_operations.py
├── parameterized_queries.py
├── join_queries.py
├── transactions.py
├── db_context_manager.py (бонус)
├── information_schema.py (бонус)
├── schema_info.txt
└── REFLECTION.md
```

## Усім студентам!

Заповніть файл `REFLECTION.md`:

```markdown
# Рефлексія. Заняття 30

## Що я навчився?

- Як встановити й налаштувати PostgreSQL
- Як працюють первинні та зовнішні ключи
- ...

## Найскладніший момент

Який момент викликав найбільше труднощів?

## Цікаве відкриття

Що стало для мене неочікуваним?

## План на наступне завдання

Що я хочу поліпшити?
```

**Готово до здачі!** 🎉

Якщо маєте питання — звертайтеся до мене.

**Удачі! 🚀**
