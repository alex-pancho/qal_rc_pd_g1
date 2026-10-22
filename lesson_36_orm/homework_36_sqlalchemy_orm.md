# Домашнє завдання. Заняття 36. SQLAlchemy ORM — вступ у професійну роботу з даними

**Курс:** Програмування Python · Модуль 5. PostgreSQL · Заняття 36  
**Студент:** _______________  
**Дата здачі:** _______________

---

## Частина A. Обов'язкові завдання

### Завдання 1. Встановлення SQLAlchemy та налаштування (Базове)

**Мета:** Встановити необхідні пакети та налаштувати з'єднання з БД.

#### Кроки:

1. **Встановіть пакети:**
   ```bash
   pip install sqlalchemy psycopg2-binary
   ```

2. **Перевірте встановлення:**
   ```bash
   python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__}')"
   ```

3. **Напишіть файл `requirements.txt`:**
   ```
   sqlalchemy>=1.4.0,<2.0
   psycopg2-binary>=2.9.0
   python-dotenv>=0.19.0
   ```

4. **Встановіть з requirements:**
   ```bash
   pip install -r requirements.txt
   ```

#### Що здавати:
- Файл `requirements.txt`
- Скріншот успішної перевірки версії

---

### Завдання 2. Налаштування database.py (Базове)

**Мета:** Створити основний модуль для з'єднання з БД.

**Напишіть файл `database.py`:**

```python
# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Конфігурація
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/your_database"
)

# Створити Engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Встановити True для дебагу
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Перевіряти з'єднання перед використанням
)

# Declarative Base
Base = declarative_base()

# SessionLocal для створення сесій
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Функція для отримання сесії (для dependency injection)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Функція для ініціалізації БД
def init_db():
    """Створити всі таблиці"""
    Base.metadata.create_all(bind=engine)
    print("✅ БД ініціалізована")

# Функція для очистки БД (для тестування)
def drop_db():
    """Видалити всі таблиці"""
    Base.metadata.drop_all(bind=engine)
    print("✅ БД очищена")
```

**Додатково:** створіть `.env` файл для конфігурації:

```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/your_database
```

#### Що здавати:
- Файл `database.py`
- Файл `.env`
- Перевірка підключення (скріншот)

---

### Завдання 3. Створення моделей (Обов'язкове)

**Мета:** Визначити моделі SQLAlchemy для вашого проекту.

**Обирайте варіант за вашим проектом:**

---

#### **Варіант 1: Project 1 — Task & Bug Manager**

**Напишіть файл `models.py`:**

```python
# models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class IssueType(str, enum.Enum):
    TASK = "task"
    BUG = "bug"
    TEST_CASE = "test_case"

class IssuePriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IssueStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    issues = relationship("Issue", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Issue(Base):
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    issue_type = Column(Enum(IssueType), nullable=False, default=IssueType.TASK)
    priority = Column(Enum(IssuePriority), nullable=False, default=IssuePriority.MEDIUM)
    status = Column(Enum(IssueStatus), nullable=False, default=IssueStatus.OPEN)
    deadline = Column(DateTime)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = relationship("User", back_populates="issues")
    comments = relationship("Comment", back_populates="issue", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Issue(id={self.id}, title='{self.title}', status={self.status})>"

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    issue = relationship("Issue", back_populates="comments")
    author = relationship("User", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment(id={self.id}, author='{self.author.username}')>"
```

---

#### **Варіант 2: Project 2 — Expense & Budget Tracker**

```python
# models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from database import Base
import enum

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    currency = Column(String(3), default="UAH")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="category", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    description = Column(String(500))
    transaction_date = Column(Date, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    monthly_limit = Column(Float, nullable=False)
    month = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")
```

---

#### **Варіант 3: Project 3 — Service Management System**

```python
# models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from database import Base
import enum

class OrderStatus(str, enum.Enum):
    CREATED = "created"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="client", cascade="all, delete-orphan")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    duration_minutes = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="service")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    order_date = Column(DateTime, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.CREATED)
    total_price = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="orders")
    service = relationship("Service", back_populates="orders")

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    unit_price = Column(Float)
    min_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

#### Що здавати:
- Файл `models.py` з усіма моделями
- Скріншот перевірки синтаксису

---

### Завдання 4. Ініціалізація БД та створення таблиць (Базове)

**Мета:** Створити таблиці у БД через SQLAlchemy.

**Напишіть файл `init_db.py`:**

```python
# init_db.py
from database import engine, Base, init_db
from models import *  # Імпортувати всі моделі

if __name__ == "__main__":
    print("🔄 Ініціалізація БД...")
    init_db()
    print("✅ Таблиці успішно створені!")
    
    # Перевірити таблиці
    print("\n📊 Створені таблиці:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")
```

**Запустіть:**
```bash
python init_db.py
```

#### Що здавати:
- Файл `init_db.py`
- Скріншот виконання
- Перевірка таблиць в psql (`\dt`)

---

### Завдання 5. CRUD операції (Обов'язкове)

**Мета:** Реалізувати базові операції через ORM.

**Напишіть файл `crud_operations.py`:**

```python
# crud_operations.py
from sqlalchemy.orm import Session
from models import User, Issue, Comment  # Для Task Manager
# ЛІ
# from models import User, Transaction, Category  # Для Expense Tracker
# ЛІ
# from models import Client, Order, Service  # Для Service Management

# ===== USER CRUD (для всіх проектів) =====

class UserCRUD:
    @staticmethod
    def create(session: Session, username: str, email: str, password_hash: str) -> User:
        """Створити користувача"""
        user = User(username=username, email=email, password_hash=password_hash)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    @staticmethod
    def get_by_id(session: Session, user_id: int) -> User | None:
        """Отримати по ID"""
        return session.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_username(session: Session, username: str) -> User | None:
        """Отримати по username"""
        return session.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 10) -> list[User]:
        """Отримати всіх з пагінацією"""
        return session.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(session: Session, user_id: int, **kwargs) -> User | None:
        """Оновити користувача"""
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            session.commit()
            session.refresh(user)
        return user
    
    @staticmethod
    def delete(session: Session, user_id: int) -> bool:
        """Видалити користувача"""
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False

# ===== ISSUE CRUD (для Task Manager) =====

class IssueCRUD:
    @staticmethod
    def create(session: Session, title: str, issue_type: str, author_id: int, description: str = None) -> Issue:
        """Створити завдання"""
        issue = Issue(title=title, issue_type=issue_type, author_id=author_id, description=description)
        session.add(issue)
        session.commit()
        session.refresh(issue)
        return issue
    
    @staticmethod
    def get_by_id(session: Session, issue_id: int) -> Issue | None:
        """Отримати завдання по ID"""
        return session.query(Issue).filter(Issue.id == issue_id).first()
    
    @staticmethod
    def get_by_user(session: Session, user_id: int) -> list[Issue]:
        """Отримати всі завдання користувача"""
        return session.query(Issue).filter(Issue.author_id == user_id).all()
    
    @staticmethod
    def get_by_status(session: Session, status: str) -> list[Issue]:
        """Отримати завдання за статусом"""
        return session.query(Issue).filter(Issue.status == status).all()
    
    @staticmethod
    def update(session: Session, issue_id: int, **kwargs) -> Issue | None:
        """Оновити завдання"""
        issue = session.query(Issue).filter(Issue.id == issue_id).first()
        if issue:
            for key, value in kwargs.items():
                if hasattr(issue, key):
                    setattr(issue, key, value)
            session.commit()
            session.refresh(issue)
        return issue
    
    @staticmethod
    def delete(session: Session, issue_id: int) -> bool:
        """Видалити завдання"""
        issue = session.query(Issue).filter(Issue.id == issue_id).first()
        if issue:
            session.delete(issue)
            session.commit()
            return True
        return False
```

#### Що здавати:
- Файл `crud_operations.py` з класами для вашого проекту
- Перевірка синтаксису

---

### Завдання 6. Тестування CRUD операцій (Обов'язкове)

**Мета:** Протестувати CRUD функції на реальних даних.

**Напишіть файл `test_crud.py`:**

```python
# test_crud.py
from database import SessionLocal
from models import User, Issue, Comment
from crud_operations import UserCRUD, IssueCRUD

def test_user_crud():
    """Тестування User CRUD"""
    print("=== TEST USER CRUD ===\n")
    
    session = SessionLocal()
    
    # CREATE
    print("1️⃣ CREATE — додавання користувача")
    user = UserCRUD.create(session, "ivan_test", "ivan@test.com", "hash123")
    print(f"✅ Користувач створений: ID {user.id}, {user.username}\n")
    
    # READ
    print("2️⃣ READ — отримання користувача")
    fetched = UserCRUD.get_by_username(session, "ivan_test")
    print(f"✅ Знайдено: {fetched.username} ({fetched.email})\n")
    
    # UPDATE
    print("3️⃣ UPDATE — оновлення користувача")
    updated = UserCRUD.update(session, user.id, email="ivan.new@test.com")
    print(f"✅ Email оновлений: {updated.email}\n")
    
    # DELETE
    print("4️⃣ DELETE — видалення користувача")
    deleted = UserCRUD.delete(session, user.id)
    print(f"✅ Користувач видалений: {deleted}\n")
    
    session.close()

def test_issue_crud():
    """Тестування Issue CRUD (для Task Manager)"""
    print("=== TEST ISSUE CRUD ===\n")
    
    session = SessionLocal()
    
    # Створити користувача для тесту
    user = UserCRUD.create(session, "test_author", "author@test.com", "hash")
    
    # CREATE
    print("1️⃣ CREATE — додавання завдання")
    issue = IssueCRUD.create(session, "Test Issue", "bug", user.id, "Test description")
    print(f"✅ Завдання створено: ID {issue.id}, {issue.title}\n")
    
    # READ
    print("2️⃣ READ — отримання завдання")
    fetched = IssueCRUD.get_by_id(session, issue.id)
    print(f"✅ Знайдено: {fetched.title} (статус: {fetched.status})\n")
    
    # UPDATE
    print("3️⃣ UPDATE — оновлення статусу")
    updated = IssueCRUD.update(session, issue.id, status="in_progress")
    print(f"✅ Статус оновлений: {updated.status}\n")
    
    # Очистка
    IssueCRUD.delete(session, issue.id)
    UserCRUD.delete(session, user.id)
    
    session.close()

if __name__ == "__main__":
    test_user_crud()
    test_issue_crud()
    print("\n✅ Все тести пройшли успішно!")
```

**Запустіть:**
```bash
python test_crud.py
```

#### Що здавати:
- Файл `test_crud.py`
- Скріншот успішного виконання тестів

---

## Частина B. Розширені завдання

### Завдання 7. Складні запити (Середня складність)

**Мета:** Написати запити з фільтруванням, JOIN, агрегуванням.

**Напишіть файл `advanced_queries.py`:**

```python
# advanced_queries.py
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session, joinedload
from models import User, Issue, Comment  # Для Task Manager
# ЛІ інші для інших проектів

def get_user_with_issues(session: Session, user_id: int):
    """Отримати користувача з усіма завданнями (eager loading)"""
    user = session.query(User).options(
        joinedload(User.issues)
    ).filter(User.id == user_id).first()
    return user

def get_open_issues_by_priority(session: Session, priority: str):
    """Отримати відкриті завдання певного пріоритету"""
    return session.query(Issue).filter(
        and_(
            Issue.status == "open",
            Issue.priority == priority
        )
    ).order_by(Issue.created_at.desc()).all()

def get_issues_by_author_and_status(session: Session, user_id: int, status: str):
    """Отримати завдання користувача зі статусом"""
    return session.query(Issue).filter(
        and_(
            Issue.author_id == user_id,
            Issue.status == status
        )
    ).all()

def search_issues(session: Session, search_term: str):
    """Пошук завдань по назві (LIKE)"""
    return session.query(Issue).filter(
        Issue.title.ilike(f"%{search_term}%")
    ).all()

def get_issue_count_by_status(session: Session):
    """Підрахувати кількість завдань по статусам"""
    return session.query(
        Issue.status,
        func.count(Issue.id).label("count")
    ).group_by(Issue.status).all()

def get_user_issue_counts(session: Session):
    """Отримати кількість завдань кожного користувача"""
    return session.query(
        User.username,
        func.count(Issue.id).label("issue_count")
    ).join(Issue).group_by(User.id).all()

def get_paged_issues(session: Session, page: int = 1, per_page: int = 10):
    """Отримати завдання з пагінацією"""
    offset = (page - 1) * per_page
    
    total = session.query(Issue).count()
    issues = session.query(Issue).offset(offset).limit(per_page).all()
    total_pages = (total + per_page - 1) // per_page
    
    return {
        "issues": issues,
        "total": total,
        "page": page,
        "total_pages": total_pages
    }
```

#### Що здавати:
- Файл `advanced_queries.py`
- Тест запитів з результатами

---

### Завдання 8. Міграція з SQL на ORM (Середня складність)

**Мета:** Переписати старий SQL код на SQLAlchemy ORM.

**Напишіть файл `migration_example.py`:**

```python
# migration_example.py
"""
Порівняння: "сирий" SQL vs SQLAlchemy ORM
"""

from database import SessionLocal, engine
import psycopg
from models import User, Issue

# ❌ СТАРИЙ СПОСІБ — "сирий" SQL через psycopg
def old_add_user_sql(username: str, email: str, password_hash: str):
    """SQL версія"""
    conn = psycopg.connect("postgresql://...")
    cur = conn.cursor()
    
    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )
        conn.commit()
        print(f"✅ SQL: користувач {username} додан")
    finally:
        cur.close()
        conn.close()

def old_get_users_sql():
    """SQL версія"""
    conn = psycopg.connect("postgresql://...")
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id, username, email FROM users")
        rows = cur.fetchall()
        users = [{"id": row[0], "username": row[1], "email": row[2]} for row in rows]
        return users
    finally:
        cur.close()
        conn.close()

def old_update_user_sql(user_id: int, email: str):
    """SQL версія"""
    conn = psycopg.connect("postgresql://...")
    cur = conn.cursor()
    
    try:
        cur.execute(
            "UPDATE users SET email = %s WHERE id = %s",
            (email, user_id)
        )
        conn.commit()
        print(f"✅ SQL: користувач {user_id} оновлений")
    finally:
        cur.close()
        conn.close()

def old_get_user_issues_sql(user_id: int):
    """SQL версія з JOIN"""
    conn = psycopg.connect("postgresql://...")
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT u.username, i.title, i.status
            FROM users u
            LEFT JOIN issues i ON u.id = i.author_id
            WHERE u.id = %s
        """, (user_id,))
        
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

# ✅ НОВИЙ СПОСІБ — SQLAlchemy ORM
def new_add_user_orm(username: str, email: str, password_hash: str):
    """ORM версія"""
    session = SessionLocal()
    try:
        user = User(username=username, email=email, password_hash=password_hash)
        session.add(user)
        session.commit()
        print(f"✅ ORM: користувач {username} додан")
    finally:
        session.close()

def new_get_users_orm():
    """ORM версія"""
    session = SessionLocal()
    try:
        users = session.query(User).all()
        return [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    finally:
        session.close()

def new_update_user_orm(user_id: int, email: str):
    """ORM версія"""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.email = email
            session.commit()
            print(f"✅ ORM: користувач {user_id} оновлений")
    finally:
        session.close()

def new_get_user_issues_orm(user_id: int):
    """ORM версія (автоматично через relationship)"""
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            # Прямий доступ до завдань через relationship!
            return [(user.username, issue.title, issue.status) for issue in user.issues]
        return []
    finally:
        session.close()

# ===== ПОРІВНЯННЯ =====
if __name__ == "__main__":
    print("=== ПОРІВНЯННЯ: SQL vs ORM ===\n")
    
    # ADD
    print("1. ADD USER")
    print(f"   SQL: {len(inspect.getsource(old_add_user_sql).split(chr(10)))} рядків")
    print(f"   ORM: {len(inspect.getsource(new_add_user_orm).split(chr(10)))} рядків")
    print(f"   Економія: 60% коду!\n")
    
    # GET
    print("2. GET USERS")
    print(f"   SQL: 10+ рядків (з управлінням з'єднанням)")
    print(f"   ORM: 3 рядків\n")
    
    # UPDATE
    print("3. UPDATE USER")
    print(f"   SQL: 10+ рядків")
    print(f"   ORM: 3 рядків\n")
    
    # JOIN
    print("4. GET USER WITH ISSUES (JOIN)")
    print(f"   SQL: вручну писати JOIN")
    print(f"   ORM: user.issues (автоматичне завантаження!)\n")
    
    print("✨ Висновок: ORM дозволяє писати 5–10 разів менше коду!")
```

#### Що здавати:
- Файл `migration_example.py`
- Аналіз економії коду

---

## Частина C. Бонус завдання

### Завдання 9* (Бонус). Продвинуті зв'язки та запити

**Мета:** Працювати з複знача relationship та складними запитами.

**Напишіть `complex_relationships.py` (залежно від проекту):**

```python
# complex_relationships.py
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload
from models import User, Issue, Comment

# Eager loading з joinedload
def get_user_with_all_data(session: Session, user_id: int):
    """Завантажити користувача з усіма даними (один запит)"""
    user = session.query(User).options(
        joinedload(User.issues).joinedload(Issue.comments)
    ).filter(User.id == user_id).first()
    return user

# Selectin для більш складних сценаріїв
def get_all_users_with_issues(session: Session):
    """Завантажити всіх користувачів з їхніми завданнями"""
    users = session.query(User).options(
        selectinload(User.issues)
    ).all()
    return users

# Аналітика
def get_issue_statistics(session: Session):
    """Статистика по завданнях"""
    stats = session.query(
        func.count(Issue.id).label("total_issues"),
        func.count(func.distinct(Issue.author_id)).label("authors"),
        func.count(func.distinct(Issue.status)).label("statuses")
    ).first()
    
    return {
        "total_issues": stats[0],
        "total_authors": stats[1],
        "unique_statuses": stats[2]
    }
```

#### Що здавати:
- Файл `complex_relationships.py`

---

### Завдання 10* (Бонус). Тестування CRUD операцій

**Мета:** Написати unit-тести для CRUD функцій.

**Напишіть `test_models.py`:**

```python
# test_models.py
import pytest
from database import SessionLocal
from models import User, Issue
from crud_operations import UserCRUD, IssueCRUD

@pytest.fixture
def session():
    """Fixture для сесії (in-memory SQLite для тестування)"""
    from sqlalchemy import create_engine
    from database import Base
    
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session
    session.close()

class TestUserCRUD:
    def test_create_user(self, session):
        user = UserCRUD.create(session, "test", "test@example.com", "hash")
        assert user.id is not None
        assert user.username == "test"
    
    def test_get_user_by_username(self, session):
        created = UserCRUD.create(session, "alice", "alice@example.com", "hash")
        fetched = UserCRUD.get_by_username(session, "alice")
        assert fetched.id == created.id
    
    def test_update_user(self, session):
        user = UserCRUD.create(session, "bob", "bob@example.com", "hash")
        updated = UserCRUD.update(session, user.id, email="bob.new@example.com")
        assert updated.email == "bob.new@example.com"
    
    def test_delete_user(self, session):
        user = UserCRUD.create(session, "charlie", "charlie@example.com", "hash")
        deleted = UserCRUD.delete(session, user.id)
        assert deleted == True
        fetched = UserCRUD.get_by_id(session, user.id)
        assert fetched is None
```

**Запустіть:**
```bash
pytest test_models.py -v
```

#### Що здавати:
- Файл `test_models.py`
- Скріншот результатів тестування

---

## Частина D. Підсумкова перевірка

### Чек-лист перед здачею:

- [ ] Встановлені SQLAlchemy та psycopg
- [ ] Створені файли database.py, models.py
- [ ] Таблиці створені у БД
- [ ] Реалізовані CRUD операції
- [ ] Протестовані CRUD функції
- [ ] Написані складні запити
- [ ] Створена міграція з SQL на ORM
- [ ] Усі файли в `/mnt/user-data/outputs/`

### Структура файлів для здачі:

```
lesson_36_homework/
├── requirements.txt
├── .env
├── database.py
├── models.py
├── crud_operations.py
├── init_db.py
├── test_crud.py
├── advanced_queries.py
├── migration_example.py
├── complex_relationships.py (бонус)
├── test_models.py (бонус)
└── REFLECTION.md
```

---

## Заповніть файл `REFLECTION.md`:

```markdown
# Рефлексія. Заняття 36. SQLAlchemy ORM

## Що я навчився?

- Навіщо потрібен ORM
- Як використовувати SQLAlchemy
- Моделювання даних через Declarative
- CRUD операції без сирого SQL
- ...

## Найскладніший момент

Який момент викликав найбільше труднощів?

## Еврика-момент!

Що стало для мене неочікуваним або цікавим?

## Порівняння SQL vs ORM

Як вам подобається — SQL чи ORM?
Чому?

## План на Django

Як ви думаєте, Django ORM буде легше/складніше?
```

---

**Готово до здачі!** 🎉

Якщо маєте питання — звертайтеся.

**Удачі! 🚀**
