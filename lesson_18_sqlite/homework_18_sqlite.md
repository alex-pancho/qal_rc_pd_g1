# Домашнє завдання — Заняття 18. SQLite та локальна база даних

**Курс:** Програмування Python  
**Автор:** Олександр Панченко, ТОВ «Тренінг-центр КьюЕйЛайт»

## Загальні вимоги до всіх варіантів

Перед виконанням завдання переконайтесь:

- У проєкті є окремий файл `database.py` із функціями `get_connection()` та `init_db()`.
- `get_connection()` встановлює `conn.row_factory = sqlite3.Row` та вмикає `PRAGMA foreign_keys = ON`.
- Всі SQL-запити використовують параметри `?` — жодної конкатенації рядків.
- `commit()` викликається після кожного INSERT / UPDATE / DELETE.
- Файл бази даних зберігається у папці `data/` (вона створюється автоматично через `pathlib`).

## 🗂 Проєкт 1 — Task & Bug Manager

### Контекст

Поки що проєкт зберігав задачі у `issues.json`. Тепер замінюємо JSON на SQLite.

### Що зробити

Створіть файл `database.py` з функцією `init_db()`, яка створює три таблиці:

**users** — `id`, `username`, `email`

**issues** — `id`, `title`, `description`, `issue_type`, `priority`, `status`, `deadline`, `user_id` (зовнішній ключ на `users.id`)

**comments** — `id`, `text`, `author_id` (зовнішній ключ на `users.id`), `issue_id` (зовнішній ключ на `issues.id`)

Після цього реалізуйте у `models.py` такі функції:

- `create_user(username, email) → int` — додати користувача, повернути його `id`
- `create_issue(title, issue_type, priority, user_id) → int` — створити задачу
- `get_all_issues() → list` — отримати всі задачі
- `get_issues_with_usernames() → list` — отримати задачі разом із іменем автора (використати JOIN)
- `update_issue_status(issue_id, new_status) → bool` — змінити статус задачі
- `delete_issue(issue_id) → bool` — видалити задачу
- `add_comment(issue_id, author_id, text) → int` — додати коментар до задачі

### Перевірка роботи

У `main.py` (або окремому скрипті `seed.py`) додайте тестові дані:

- двох користувачів;
- три задачі різних типів (Task, Bug, Test Case) з різними пріоритетами;
- по одному коментарю до двох будь-яких задач.

Виведіть усі задачі з іменами авторів у форматі:

```
[1] Fix login bug | Bug | High | Open | alice
[2] Write unit tests | Task | Medium | Open | bob
[3] Update README | Task | Low | Done | alice
```

### Бонус

Реалізуйте функцію `get_issue_with_comments(issue_id)`, яка повертає задачу разом із усіма її коментарями (використати JOIN між `issues`, `comments` та `users`). Виведіть результат у зручному форматі.

## 💰 Проєкт 2 — Expense & Budget Tracker

### Контекст

Проєкт зберігав транзакції у `transactions.json`. Переходимо на SQLite.

### Що зробити

Створіть файл `database.py` з функцією `init_db()`, яка створює три таблиці:

**users** — `id`, `username`, `email`

**transactions** — `id`, `amount`, `transaction_type` (`'income'` або `'expense'`), `category`, `date`, `description`, `user_id` (зовнішній ключ на `users.id`)

**budgets** — `id`, `category`, `monthly_limit`, `user_id` (зовнішній ключ на `users.id`)

Реалізуйте у `models.py`:

- `create_user(username, email) → int`
- `add_transaction(user_id, amount, transaction_type, category, description) → int`
- `get_all_transactions(user_id) → list` — всі транзакції конкретного користувача
- `get_balance(user_id) → float` — різниця між доходами та витратами (використати `SELECT SUM`)
- `get_expenses_by_category(user_id) → list` — витрати, згруповані за категорією (використати `GROUP BY` та `SUM`)
- `set_budget(user_id, category, monthly_limit) → int`
- `delete_transaction(transaction_id) → bool`

### Перевірка роботи

У `main.py` або `seed.py` додайте тестові дані:

- одного користувача;
- щонайменше 5 транзакцій (доходи та витрати, різні категорії);
- бюджет для двох категорій.

Виведіть:

```
=== Транзакції ===
[1] 2024-01-15 | income  | Salary     | +15000.00
[2] 2024-01-16 | expense | Food       |  -450.00
[3] 2024-01-17 | expense | Transport  |  -120.00

=== Баланс: 14430.00 ===

=== Витрати за категоріями ===
Food       : 450.00
Transport  : 120.00
```

### Бонус

Реалізуйте функцію `check_budget_status(user_id) → list`, яка порівнює фактичні витрати поточного місяця за кожною категорією з встановленим бюджетом і виводить попередження, якщо витрати перевищують ліміт. Використати JOIN між `transactions` та `budgets`.

## 🔧 Проєкт 3 — Service Management System

### Контекст

Проєкт зберігав клієнтів та замовлення у JSON-файлах. Переходимо на SQLite.

### Що зробити

Створіть файл `database.py` з функцією `init_db()`, яка створює чотири таблиці:

**clients** — `id`, `name`, `phone`, `email`

**services** — `id`, `name`, `price`, `duration` (тривалість у хвилинах)

**orders** — `id`, `client_id` (FK → `clients.id`), `service_id` (FK → `services.id`), `status`, `total_price`, `created_at`

**inventory** — `id`, `name`, `quantity`, `price`

Реалізуйте у `models.py`:

- `add_client(name, phone, email) → int`
- `add_service(name, price, duration) → int`
- `create_order(client_id, service_id) → int` — статус за замовчуванням `'Created'`, `total_price` береться з таблиці `services`
- `get_all_orders() → list` — всі замовлення
- `get_orders_with_details() → list` — замовлення з іменами клієнтів та назвами послуг (JOIN між трьома таблицями)
- `update_order_status(order_id, new_status) → bool`
- `add_inventory_item(name, quantity, price) → int`
- `get_low_stock_items(threshold) → list` — товари, кількість яких менша за `threshold`

### Перевірка роботи

У `main.py` або `seed.py` додайте тестові дані:

- трьох клієнтів;
- чотири послуги з різними цінами;
- п'ять замовлень у різних статусах;
- кілька позицій складу, деякі з малою кількістю.

Виведіть замовлення з деталями:

```
=== Замовлення ===
[1] Іваненко Олег   | Oil Change    | 850.00 | Done
[2] Петренко Марія  | Tire Rotation | 400.00 | In Progress
[3] Коваль Андрій   | Brake Check   | 600.00 | Created

=== Мало на складі (< 3 шт.) ===
Моторна олива 5W-30 : 2 шт.
Гальмівні колодки   : 1 шт.
```

### Бонус

Реалізуйте функцію `get_client_history(client_id) → list`, яка повертає всі замовлення конкретного клієнта разом із назвою послуги, ціною та статусом, відсортовані за датою створення від найновіших до найстаріших.

## Що здати

- Файли `database.py`, `models.py` та `main.py` (або `seed.py`).
- Git-коміт із повідомленням у форматі: `lesson 18 — sqlite database`.
- Скриншот або копія виводу програми у термінал.

## Таблиця вимог

| Вимога | Обов'язково |
|---|---|
| Окремий `database.py` з `init_db()` та `get_connection()` | ✅ |
| `PRAGMA foreign_keys = ON` | ✅ |
| `row_factory = sqlite3.Row` | ✅ |
| Параметризовані запити `?` | ✅ |
| `commit()` після змін | ✅ |
| JOIN у щонайменше одній функції | ✅ |
| Тестові дані та вивід у термінал | ✅ |
| Git-коміт | ✅ |
| Бонусна функція | ⭐ за бажанням |
