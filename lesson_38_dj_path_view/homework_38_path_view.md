# Заняття 38. Домашнє завдання — Маршрутизація та представлення

**Період:** Module 6. Django Basics  
**Теми:** URL-маршрутизація, представлення (views), передача даних у шаблони, структура проєкту

---

## Завдання для всіх студентів

### Обов'язкові завдання

Виберіть один із трьох проєктів і виконайте завдання з відповідною складністю.

---

## Проєкт 1: Task & Bug Manager

### Рівень 1. Обов'язковий — Базова маршрутизація та представлення

**Мета:** Створити мінімальний Django-застосунок із сторінками для перегляду задач, багів та тест-кейсів.

#### Крок 1. Підготовка структури

```bash
# Якщо ще немає Django-проєкту:
django-admin startproject config .
python manage.py startapp issues

# Додайте 'issues' у INSTALLED_APPS
```

#### Крок 2. Створення представлень

Файл `issues/views.py`:

```python
from django.shortcuts import render
from django.http import HttpResponse

# Тимчасові дані (на місці БД)
ISSUES_DATA = [
    {"id": 1, "title": "Помилка входу", "type": "Bug", "status": "Open", "priority": "High"},
    {"id": 2, "title": "Додати функцію пошуку", "type": "Task", "status": "In Progress", "priority": "Medium"},
    {"id": 3, "title": "Тестувати API", "type": "Test Case", "status": "Open", "priority": "Low"},
]

def home(request):
    """Головна сторінка"""
    context = {
        "title": "Task & Bug Manager",
        "message": "Вітаємо в системі управління задачами!",
    }
    return render(request, "issues/home.html", context)

def issues_list(request):
    """Список всіх задач"""
    context = {
        "title": "Список задач",
        "issues": ISSUES_DATA,
    }
    return render(request, "issues/issues_list.html", context)

def issue_detail(request, issue_id):
    """Деталі конкретної задачі"""
    issue = next((i for i in ISSUES_DATA if i["id"] == issue_id), None)
    if issue is None:
        return HttpResponse("Задача не знайдена", status=404)
    
    context = {
        "issue": issue,
    }
    return render(request, "issues/issue_detail.html", context)

def about(request):
    """Про проєкт"""
    context = {
        "title": "Про Task Manager",
        "description": "Це система для управління задачами та багами проєкту.",
    }
    return render(request, "issues/about.html", context)
```

#### Крок 3. Налаштування маршрутів

Файл `issues/urls.py` (новий файл):

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("issues/", views.issues_list, name="issues_list"),
    path("issues/<int:issue_id>/", views.issue_detail, name="issue_detail"),
    path("about/", views.about, name="about"),
]
```

Файл `config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("issues.urls")),
]
```

#### Крок 4. Створення папки для шаблонів

```bash
mkdir -p issues/templates/issues
```

#### Крок 5. Написання шаблонів

Файл `issues/templates/issues/home.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        nav { background-color: #007bff; padding: 10px; margin-bottom: 20px; }
        nav a { color: white; margin: 0 10px; text-decoration: none; }
    </style>
</head>
<body>
    <nav>
        <a href="{% url 'home' %}">Головна</a>
        <a href="{% url 'issues_list' %}">Задачи</a>
        <a href="{% url 'about' %}">Про нас</a>
    </nav>
    
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
</body>
</html>
```

Файл `issues/templates/issues/issues_list.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    
    {% if issues %}
        <table border="1">
            <tr>
                <th>ID</th>
                <th>Назва</th>
                <th>Тип</th>
                <th>Статус</th>
                <th>Пріоритет</th>
                <th>Дія</th>
            </tr>
            {% for issue in issues %}
                <tr>
                    <td>{{ issue.id }}</td>
                    <td>{{ issue.title }}</td>
                    <td>{{ issue.type }}</td>
                    <td>{{ issue.status }}</td>
                    <td>{{ issue.priority }}</td>
                    <td><a href="{% url 'issue_detail' issue.id %}">Переглянути</a></td>
                </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>Немає задач.</p>
    {% endif %}
    
    <a href="{% url 'home' %}">Назад на головну</a>
</body>
</html>
```

Файл `issues/templates/issues/issue_detail.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ issue.title }}</title>
</head>
<body>
    <h1>{{ issue.title }}</h1>
    <p><strong>ID:</strong> {{ issue.id }}</p>
    <p><strong>Тип:</strong> {{ issue.type }}</p>
    <p><strong>Статус:</strong> {{ issue.status }}</p>
    <p><strong>Пріоритет:</strong> {{ issue.priority }}</p>
    
    <a href="{% url 'issues_list' %}">Назад до списку</a>
</body>
</html>
```

Файл `issues/templates/issues/about.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
    
    <h2>Можливості:</h2>
    <ul>
        <li>Створення та керування задачами</li>
        <li>Відстеження багів</li>
        <li>Управління тест-кейсами</li>
    </ul>
    
    <a href="{% url 'home' %}">Назад на головну</a>
</body>
</html>
```

#### Крок 6. Перевірка

```bash
python manage.py runserver
```

Зайдіть на:
- `http://127.0.0.1:8000/` — головна
- `http://127.0.0.1:8000/issues/` — список задач
- `http://127.0.0.1:8000/issues/1/` — деталі задачі #1
- `http://127.0.0.1:8000/about/` — про проєкт

### Рівень 2. Просунутий — Розширена функціональність

**Додаткові завдання:**

1. **Фільтрування по типу:**
   - Додайте маршрут `issues/type/<str:issue_type>/`
   - View повинен показати лише задачи вибраного типу (Bug, Task, Test Case)

2. **Фільтрування по статусу:**
   - Додайте маршрут `issues/status/<str:status>/`
   - View повинен показати лише задачи вибраного статусу

3. **Пошук по ID:**
   - Додайте `<int:issue_id>` в URL і обробіть помилку 404

4. **Користувачі:**
   - Додайте маршрут `users/<str:username>/`
   - Покажіть профіль користувача з його задачами

### Рівень 3. Бонус — Creative Challenge

**На вибір:**

1. **Додайте CSS-стилізацію**
   - Навіть просту, але красиву
   - Використовуйте `{% static %}` для CSS

2. **Додайте comments:**
   - Маршрут `issues/<int:issue_id>/comments/`
   - Покажіть коментарі до задачі (можуть бути hardcoded)

3. **Додайте dashboard:**
   - Маршрут `/dashboard/`
   - Статистика: кількість задач, багів, тест-кейсів, статусів

---

## Проєкт 2: Expense & Budget Tracker

### Рівень 1. Обов'язковий — Базова маршрутизація та представлення

**Мета:** Створити Django-застосунок для перегляду доходів, витрат та бюджету.

#### Крок 1. Підготовка

```bash
django-admin startproject config .
python manage.py startapp transactions
# Додайте 'transactions' у INSTALLED_APPS
```

#### Крок 2. Представлення

Файл `transactions/views.py`:

```python
from django.shortcuts import render
from django.http import HttpResponse

# Тимчасові дані
TRANSACTIONS = [
    {"id": 1, "amount": 30000, "type": "income", "category": "Salary", "date": "2024-01-15", "description": "Зарплата за січень"},
    {"id": 2, "amount": 5000, "type": "expense", "category": "Food", "date": "2024-01-16", "description": "Продукти"},
    {"id": 3, "amount": 3000, "type": "expense", "category": "Transport", "date": "2024-01-17", "description": "Бензин"},
    {"id": 4, "amount": 15000, "type": "income", "category": "Freelance", "date": "2024-01-18", "description": "Проєкт для клієнта"},
]

BUDGETS = [
    {"category": "Food", "monthly_limit": 10000},
    {"category": "Transport", "monthly_limit": 5000},
    {"category": "Entertainment", "monthly_limit": 3000},
]

def home(request):
    """Головна"""
    total_income = sum(t["amount"] for t in TRANSACTIONS if t["type"] == "income")
    total_expense = sum(t["amount"] for t in TRANSACTIONS if t["type"] == "expense")
    balance = total_income - total_expense
    
    context = {
        "title": "Expense Tracker",
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
    }
    return render(request, "transactions/home.html", context)

def transactions_list(request):
    """Список всіх транзакцій"""
    context = {
        "title": "Мої транзакції",
        "transactions": TRANSACTIONS,
    }
    return render(request, "transactions/transactions_list.html", context)

def transaction_detail(request, transaction_id):
    """Деталі транзакції"""
    transaction = next((t for t in TRANSACTIONS if t["id"] == transaction_id), None)
    if transaction is None:
        return HttpResponse("Транзакція не знайдена", status=404)
    
    context = {"transaction": transaction}
    return render(request, "transactions/transaction_detail.html", context)

def budgets_list(request):
    """Список бюджетів"""
    context = {
        "title": "Бюджети",
        "budgets": BUDGETS,
    }
    return render(request, "transactions/budgets_list.html", context)

def income_list(request):
    """Тільки доходи"""
    income_transactions = [t for t in TRANSACTIONS if t["type"] == "income"]
    total = sum(t["amount"] for t in income_transactions)
    
    context = {
        "title": "Доходи",
        "transactions": income_transactions,
        "total": total,
    }
    return render(request, "transactions/transactions_list.html", context)

def expense_list(request):
    """Тільки витрати"""
    expense_transactions = [t for t in TRANSACTIONS if t["type"] == "expense"]
    total = sum(t["amount"] for t in expense_transactions)
    
    context = {
        "title": "Витрати",
        "transactions": expense_transactions,
        "total": total,
    }
    return render(request, "transactions/transactions_list.html", context)
```

#### Крок 3. Маршрути

Файл `transactions/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("transactions/", views.transactions_list, name="transactions_list"),
    path("transactions/<int:transaction_id>/", views.transaction_detail, name="transaction_detail"),
    path("income/", views.income_list, name="income_list"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("budgets/", views.budgets_list, name="budgets_list"),
]
```

Додайте в `config/urls.py`:

```python
path("", include("transactions.urls")),
```

#### Крок 4. Папка шаблонів

```bash
mkdir -p transactions/templates/transactions
```

#### Крок 5. Шаблони

Файл `transactions/templates/transactions/home.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .balance { font-size: 24px; color: green; }
        .expense { color: red; }
        .income { color: green; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    
    <h2>Ваш баланс</h2>
    <p class="income">Доходи: {{ total_income }} грн</p>
    <p class="expense">Витрати: {{ total_expense }} грн</p>
    <p class="balance">Баланс: {{ balance }} грн</p>
    
    <nav>
        <a href="{% url 'transactions_list' %}">Усі транзакції</a> |
        <a href="{% url 'income_list' %}">Доходи</a> |
        <a href="{% url 'expense_list' %}">Витрати</a> |
        <a href="{% url 'budgets_list' %}">Бюджети</a>
    </nav>
</body>
</html>
```

Файл `transactions/templates/transactions/transactions_list.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    
    {% if transactions %}
        <table border="1">
            <tr>
                <th>Дата</th>
                <th>Категорія</th>
                <th>Тип</th>
                <th>Сума</th>
                <th>Опис</th>
            </tr>
            {% for t in transactions %}
                <tr>
                    <td>{{ t.date }}</td>
                    <td>{{ t.category }}</td>
                    <td>{{ t.type }}</td>
                    <td>{{ t.amount }} грн</td>
                    <td>{{ t.description }}</td>
                </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>Немає транзакцій.</p>
    {% endif %}
    
    <a href="{% url 'home' %}">Назад на головну</a>
</body>
</html>
```

Файл `transactions/templates/transactions/budgets_list.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    
    {% if budgets %}
        <ul>
            {% for budget in budgets %}
                <li>{{ budget.category }}: {{ budget.monthly_limit }} грн/місяць</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>Немає бюджетів.</p>
    {% endif %}
    
    <a href="{% url 'home' %}">Назад на головну</a>
</body>
</html>
```

### Рівень 2. Просунутий

**Додаткові завдання:**

1. **Фільтрування по категорії:**
   - Маршрут `transactions/category/<str:category>/`
   - Покажіть лише транзакції вибраної категорії

2. **Місячний звіт:**
   - Маршрут `reports/<int:month>/`
   - Статистика по місяцю

3. **Рейтинг витрат:**
   - Сторінка `top-expenses/`
   - Топ-5 найбільших витрат

### Рівень 3. Бонус

1. **Додайте валюти:**
   - Маршрут `convert/`
   - Конвертер грн ↔ USD ↔ EUR (з hardcoded курсами)

2. **Графіки витрат:**
   - ASCII-арт графік видатків по категоріям

---

## Проєкт 3: Service Management System

### Рівень 1. Обов'язковий — Базова маршрутизація та представлення

**Мета:** Створити Django-застосунок для управління клієнтами, замовленнями та послугами.

Виберіть домен: **Auto Service** або **Beauty Clinic**

#### Приклад для Auto Service:

Файл `services/views.py`:

```python
from django.shortcuts import render
from django.http import HttpResponse

CLIENTS = [
    {"id": 1, "name": "Іван Петренко", "phone": "+380501234567", "email": "ivan@example.com"},
    {"id": 2, "name": "Марія Сидоренко", "phone": "+380502345678", "email": "maria@example.com"},
]

VEHICLES = [
    {"id": 1, "client_id": 1, "brand": "Toyota", "model": "Camry", "year": 2020},
    {"id": 2, "client_id": 2, "brand": "BMW", "model": "X5", "year": 2022},
]

ORDERS = [
    {"id": 1, "client_id": 1, "vehicle_id": 1, "service": "Діагностика", "status": "Completed", "price": 500},
    {"id": 2, "client_id": 2, "vehicle_id": 2, "service": "Заміна масла", "status": "In Progress", "price": 800},
]

def home(request):
    """Головна"""
    context = {
        "title": "Auto Service Management",
        "message": "Вітаємо в системі управління автосервісом!",
    }
    return render(request, "services/home.html", context)

def clients_list(request):
    """Список клієнтів"""
    context = {
        "title": "Клієнти",
        "clients": CLIENTS,
    }
    return render(request, "services/clients_list.html", context)

def client_detail(request, client_id):
    """Деталі клієнта"""
    client = next((c for c in CLIENTS if c["id"] == client_id), None)
    if client is None:
        return HttpResponse("Клієнт не знайдений", status=404)
    
    vehicles = [v for v in VEHICLES if v["client_id"] == client_id]
    
    context = {
        "client": client,
        "vehicles": vehicles,
    }
    return render(request, "services/client_detail.html", context)

def orders_list(request):
    """Список замовлень"""
    context = {
        "title": "Замовлення",
        "orders": ORDERS,
    }
    return render(request, "services/orders_list.html", context)

def order_detail(request, order_id):
    """Деталі замовлення"""
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if order is None:
        return HttpResponse("Замовлення не знайдено", status=404)
    
    context = {"order": order}
    return render(request, "services/order_detail.html", context)

def vehicles_list(request):
    """Список автомобілів"""
    context = {
        "title": "Автомобілі",
        "vehicles": VEHICLES,
    }
    return render(request, "services/vehicles_list.html", context)
```

Файл `services/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("clients/", views.clients_list, name="clients_list"),
    path("clients/<int:client_id>/", views.client_detail, name="client_detail"),
    path("orders/", views.orders_list, name="orders_list"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("vehicles/", views.vehicles_list, name="vehicles_list"),
]
```

Шаблони (аналогічно попередніх проєктів):
- `home.html` — головна
- `clients_list.html` — таблиця клієнтів
- `client_detail.html` — профіль клієнта з його авто
- `orders_list.html` — таблиця замовлень
- `vehicles_list.html` — список автомобілів

### Рівень 2. Просунутий

1. **Замовлення клієнта:**
   - Маршрут `clients/<int:client_id>/orders/`
   - Усі замовлення конкретного клієнта

2. **Замовлення по статусу:**
   - Маршрут `orders/status/<str:status>/`
   - Фільтрація по статусу (Completed, In Progress, Pending)

3. **Пошук по послузі:**
   - Маршрут `services/search/<str:service_name>/`

### Рівень 3. Бонус

1. **Інвентар:**
   - Маршрут `inventory/`
   - Список запчастин/матеріалів

2. **Графік запису:**
   - Маршрут `schedule/`
   - Розклад замовлень

---

## Критерії оцінювання

### Рівень 1 (Обов'язковий) — 10 балів

- ✅ Структура Django-проєкту правильна
- ✅ Створено 4+ маршрути
- ✅ Створено 4+ view-функції
- ✅ Створено 4+ HTML-шаблони
- ✅ Дані передаються в шаблони через контекст
- ✅ Код без помилок, сервер запускається

### Рівень 2 (Просунутий) — додатково 5 балів

- ✅ Додані фільтрування по параметрам
- ✅ Маршрути з динамічними параметрами (`<int:id>`, `<str:name>`)
- ✅ Обробка помилки 404

### Рівень 3 (Бонус) — додатково 5 балів

- ✅ CSS-стилізація або додаткові функції
- ✅ Нестандартна функціональність
- ✅ Творчий підхід

---

## Вимоги до сабміту

1. **GitHub репозиторій**
   - Гарна структура проєкту
   - Гарна назва репозиторію (наприклад, `django-task-manager`, `expense-tracker-app`)
   - README.md з інструкціями запуску

2. **Коміти**
   - Мінімум 5 логічних комітів
   - Гарні повідомлення: `feat: add client list view`, `refactor: organize templates`

3. **Структура папок**
   ```
   project/
   ├── manage.py
   ├── config/
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   ├── app_name/
   │   ├── templates/app_name/
   │   │   ├── home.html
   │   │   ├── list.html
   │   │   └── detail.html
   │   ├── views.py
   │   ├── urls.py
   │   └── models.py
   ├── requirements.txt
   └── README.md
   ```

4. **README.md**
   ```markdown
   # Project Name
   
   ## Installation
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py runserver
   ```
   
   ## Features
   - ...
   - ...
   
   ## Views
   - GET / — главная страница
   - GET /list/ — список элементов
   - GET /detail/<id>/ — деталі елемента
   ```

---

## Додаткові матеріали та поради

### Типові помилки студентів

1. ❌ Забули додати застосунок у `INSTALLED_APPS`
   - ✅ Завжди додавайте новий застосунок!

2. ❌ Параметр URL не типізований: `<id>` замість `<int:id>`
   - ✅ Завжди вказуйте тип: `<int:>`, `<str:>`, `<slug:>`

3. ❌ Шаблон лежить у неправильній папці
   - ✅ Структура: `app/templates/app/template.html`

4. ❌ Забули `{% url %}` для посилань у шаблонах
   - ✅ Використовуйте: `<a href="{% url 'name' %}">Link</a>`

### Корисні команди

```bash
# Запуск сервера
python manage.py runserver

# Запуск на іншому порту
python manage.py runserver 8001

# Отримати інформацію про проєкт
python manage.py check

# Перегляд всіх доступних маршрутів
python manage.py show_urls  # (якщо встановлено django-extensions)
```

### Найкраще для розуміння

1. Кожен маршрут → свій view
2. Кожен view → свій шаблон
3. Кожен шаблон → свій контекст
4. Контекст передається через `render(request, 'template.html', context)`

---

## Дедлайн

**Завдання здавати до передостанньої дати перед** **Заняттям 39 (Шаблони та статичні файли)**

Це дозволить вам мати готову базу для наступного заняття.

---

## Контрольні запитання

Перш ніж здавати, перевірте себе:

1. ✅ Чи я розумію, що таке маршрут?
2. ✅ Чи я знаю різницю між `path()` та `include()`?
3. ✅ Чи я можу написати view з параметром URL?
4. ✅ Чи я знаю, як передавати дані в шаблон через контекст?
5. ✅ Чи я можу обробити помилку 404?
6. ✅ Чи я знаю, як генерувати посилання в шаблонах через `{% url %}`?
7. ✅ Чи структура мого проєкту правильна?

Якщо на якесь запитання "ні", перечитайте лекцію 38 перш ніж здавати.

---

## Успіху! 🚀

Запитання — в Discord чи на консультаціях.

Happy coding! 💻