# Домашнє завдання. Заняття 39. Expense & Budget Tracker

## Мета
Створити веб-інтерфейс для управління доходами та витратами. Практикуватися з шаблонами, статичними файлами, фільтрами для грошей та дат, успадкуванням шаблонів.

## Вимоги до завдання

### Базовий рівень (обов'язково)

#### 1. Створити базовий шаблон `base.html`

**Файл:** `templates/base.html`

Структура:
```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Expense Tracker{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <header>
        <div class="header-content">
            <h1>💰 Expense & Budget Tracker</h1>
            <nav>
                <a href="{% url 'dashboard' %}">Панель керування</a>
                <a href="{% url 'transactions' %}">Транзакції</a>
                <a href="{% url 'budgets' %}">Бюджети</a>
                <a href="{% url 'reports' %}">Звіти</a>
                <a href="{% url 'about' %}">Про застосунок</a>
            </nav>
        </div>
    </header>

    <main class="container">
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2026 Expense Tracker | Керуйте своїми фінансами розумно</p>
    </footer>

    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
```

#### 2. Панель керування (Dashboard) `dashboard.html`

**Файл:** `templates/dashboard.html`

Вимоги:
- Успадковується від `base.html`
- Виводить поточний баланс (сума дохідів мінус витрати)
- Карточки з основними показниками:
  - Сумарний дохід цього місяця
  - Сумарні витрати цього місяця
  - Баланс
- Останні 5 транзакцій у таблиці
- Посилання на детальну сторінку про кожну транзакцію

**Приклад:**
```html
{% extends 'base.html' %}

{% block title %}Панель керування | Expense Tracker{% endblock %}

{% block content %}
<h2>Привіт, {{ user_name }}! Твоя панель керування</h2>

<div class="summary">
    <div class="card income">
        <h3>Дохід цього місяця</h3>
        <p class="amount">{{ total_income|floatformat:2 }} ₴</p>
    </div>
    <div class="card expense">
        <h3>Витрати цього місяця</h3>
        <p class="amount">{{ total_expense|floatformat:2 }} ₴</p>
    </div>
    <div class="card balance">
        <h3>Баланс</h3>
        <p class="amount {% if balance < 0 %}negative{% endif %}">
            {{ balance|floatformat:2 }} ₴
        </p>
    </div>
</div>

<h3>Останні транзакції</h3>
<table class="transactions-table">
    <thead>
        <tr>
            <th>Дата</th>
            <th>Категорія</th>
            <th>Тип</th>
            <th>Сума</th>
            <th>Дія</th>
        </tr>
    </thead>
    <tbody>
    {% for trans in recent_transactions %}
        <tr>
            <td>{{ trans.date|date:"d.m.Y" }}</td>
            <td>{{ trans.category }}</td>
            <td class="type-{{ trans.type|lower }}">{{ trans.type }}</td>
            <td class="{% if trans.type == 'Income' %}income{% else %}expense{% endif %}">
                {{ trans.amount|floatformat:2 }} ₴
            </td>
            <td>
                <a href="{% url 'transaction-detail' trans.id %}">Деталі</a>
            </td>
        </tr>
    {% empty %}
        <tr>
            <td colspan="5">Транзакцій немає. Додайте першу!</td>
        </tr>
    {% endfor %}
    </tbody>
</table>

<a href="{% url 'add-transaction' %}" class="btn btn-primary">+ Додати транзакцію</a>
{% endblock %}
```

#### 3. Сторінка всіх транзакцій `transactions.html`

**Файл:** `templates/transactions.html`

Вимоги:
- Успадковується від `base.html`
- Виводить всі транзакції користувача
- Таблиця з колонками: дата, категорія, тип, сума, дія
- Фільтрування за типом (дохід / витрата)
- Посилання на деталі та редагування кожної транзакції
- Якщо немає транзакцій, показати повідомлення

**Приклад умовного фільтрування:**
```html
{% extends 'base.html' %}

{% block content %}
<h2>Всі транзакції</h2>

<!-- Фільтри -->
<div class="filters">
    <a href="{% url 'transactions' %}" class="filter-btn {% if not filter %}active{% endif %}">
        Всі
    </a>
    <a href="?type=income" class="filter-btn">Дохід</a>
    <a href="?type=expense" class="filter-btn">Витрати</a>
</div>

<table class="transactions-table">
    <!-- Той же код як в dashboard -->
    {% for trans in transactions %}
    <tr>
        <td>{{ trans.date|date:"d.m.Y" }}</td>
        <td>{{ trans.category }}</td>
        <td>{{ trans.type }}</td>
        <td>{{ trans.amount|floatformat:2 }} ₴</td>
        <td>
            <a href="{% url 'transaction-detail' trans.id %}">Деталі</a>
            <a href="{% url 'edit-transaction' trans.id %}">Редагувати</a>
            <a href="{% url 'delete-transaction' trans.id %}">Видалити</a>
        </td>
    </tr>
    {% empty %}
    <tr><td colspan="5">Транзакцій немає</td></tr>
    {% endfor %}
</table>
{% endblock %}
```

#### 4. Детальна сторінка транзакції `transaction_detail.html`

**Файл:** `templates/transaction_detail.html`

Вимоги:
- Успадковується від `base.html`
- Показує повну інформацію про одну транзакцію
- Поля: дата, категорія, тип, сума, опис, дата створення
- Посилання назад та на редагування

#### 5. Сторінка бюджетів `budgets.html`

**Файл:** `templates/budgets.html`

Вимоги:
- Успадковується від `base.html`
- Виводить список бюджетів за категоріями
- Для кожного показати: категорія, ліміт, витрачено, залишок
- Прогрес-бар для наочності витрат
- Посилання на редагування та видалення

**Приклад:**
```html
{% extends 'base.html' %}

{% block content %}
<h2>Мої бюджети</h2>

{% for budget in budgets %}
    <div class="budget-card">
        <h3>{{ budget.category }}</h3>
        <p>Ліміт: {{ budget.limit|floatformat:2 }} ₴</p>
        <p>Витрачено: {{ budget.spent|floatformat:2 }} ₴</p>
        <p>Залишок: {{ budget.remaining|floatformat:2 }} ₴</p>
        
        <!-- Прогрес-бар -->
        <div class="progress-bar">
            <div class="progress-fill" style="width: {{ budget.percentage }}%"></div>
        </div>
        
        <a href="{% url 'edit-budget' budget.id %}">Редагувати</a>
        <a href="{% url 'delete-budget' budget.id %}">Видалити</a>
    </div>
{% empty %}
    <p>Бюджетів немає. Створіть перший бюджет!</p>
{% endfor %}

<a href="{% url 'add-budget' %}" class="btn btn-primary">+ Додати бюджет</a>
{% endblock %}
```

#### 6. Сторінка звітів `reports.html`

**Файл:** `templates/reports.html`

Вимоги:
- Успадковується від `base.html`
- Показує звіт про витрати за категоріями
- Таблиця або список з усіма категоріями та сумами
- Загальні статистики (всього витрачено, всього заробив)

#### 7. Статичні файли

**Файл:** `static/css/style.css`

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #ecf0f1;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

header h1 {
    margin-bottom: 15px;
}

header nav {
    display: flex;
    gap: 20px;
}

header nav a {
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.3s;
}

header nav a:hover {
    opacity: 0.8;
}

.container {
    max-width: 1000px;
    margin: 20px auto;
    padding: 30px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* Summary cards */
.summary {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin: 30px 0;
}

.card {
    padding: 20px;
    border-radius: 8px;
    color: white;
}

.card.income {
    background-color: #27ae60;
}

.card.expense {
    background-color: #e74c3c;
}

.card.balance {
    background-color: #3498db;
}

.card.balance.negative {
    background-color: #c0392b;
}

.amount {
    font-size: 28px;
    font-weight: bold;
    margin-top: 10px;
}

/* Tables */
.transactions-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

.transactions-table th {
    background-color: #34495e;
    color: white;
    padding: 12px;
    text-align: left;
}

.transactions-table td {
    padding: 12px;
    border-bottom: 1px solid #ecf0f1;
}

.transactions-table tr:hover {
    background-color: #f5f5f5;
}

.type-income {
    color: #27ae60;
    font-weight: bold;
}

.type-expense {
    color: #e74c3c;
    font-weight: bold;
}

.income {
    color: #27ae60;
    font-weight: bold;
}

.expense {
    color: #e74c3c;
    font-weight: bold;
}

/* Budget cards */
.budget-card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 15px;
    border-left: 4px solid #667eea;
}

.budget-card h3 {
    margin-bottom: 10px;
}

/* Progress bar */
.progress-bar {
    width: 100%;
    height: 20px;
    background-color: #ecf0f1;
    border-radius: 10px;
    overflow: hidden;
    margin: 10px 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #27ae60 0%, #f39c12 100%);
    transition: width 0.3s ease;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn-primary {
    background-color: #667eea;
    color: white;
}

.btn-primary:hover {
    background-color: #764ba2;
}

/* Filters */
.filters {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.filter-btn {
    padding: 8px 15px;
    border: 2px solid #bdc3c7;
    background-color: white;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s;
}

.filter-btn.active {
    background-color: #667eea;
    color: white;
    border-color: #667eea;
}

footer {
    background-color: #34495e;
    color: white;
    padding: 20px;
    text-align: center;
    margin-top: 40px;
}

@media (max-width: 768px) {
    .summary {
        grid-template-columns: 1fr;
    }
    
    header nav {
        flex-direction: column;
        gap: 10px;
    }
}
```

**Файл:** `static/js/main.js`

```javascript
document.addEventListener("DOMContentLoaded", function () {
    console.log("Expense Tracker завантажився!");
    
    // Форматування чисел як грошей
    function formatMoney(amount) {
        return amount.toLocaleString('uk-UA', {
            style: 'currency',
            currency: 'UAH'
        });
    }
    
    // Приклад: форматування при наведенні
    const amounts = document.querySelectorAll('.amount');
    amounts.forEach(el => {
        const text = el.textContent;
        if (text.includes('₴')) {
            el.style.cursor = 'pointer';
        }
    });
});
```

#### 8. View функції

**Файл:** `views.py`

```python
from django.shortcuts import render
from datetime import datetime, timedelta

def dashboard(request):
    # Мок-дані
    user_name = "Андрій"
    
    transactions = [
        {"id": 1, "date": datetime.now(), "category": "Зарплата", "type": "Income", "amount": 15000},
        {"id": 2, "date": datetime.now() - timedelta(days=1), "category": "Їжа", "type": "Expense", "amount": 450},
        {"id": 3, "date": datetime.now() - timedelta(days=2), "category": "Транспорт", "type": "Expense", "amount": 150},
        {"id": 4, "date": datetime.now() - timedelta(days=3), "category": "Хобі", "type": "Expense", "amount": 200},
        {"id": 5, "date": datetime.now() - timedelta(days=4), "category": "Фріланс", "type": "Income", "amount": 3000},
    ]
    
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    balance = total_income - total_expense
    
    context = {
        "user_name": user_name,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "recent_transactions": transactions[:5],
        "title": "Панель керування"
    }
    return render(request, "dashboard.html", context)

def transactions_list(request):
    transactions = [
        {"id": 1, "date": datetime.now(), "category": "Зарплата", "type": "Income", "amount": 15000},
        {"id": 2, "date": datetime.now() - timedelta(days=1), "category": "Їжа", "type": "Expense", "amount": 450},
        {"id": 3, "date": datetime.now() - timedelta(days=2), "category": "Транспорт", "type": "Expense", "amount": 150},
    ]
    
    context = {
        "transactions": transactions,
        "title": "Транзакції"
    }
    return render(request, "transactions.html", context)

def transaction_detail(request, transaction_id):
    transaction = {
        "id": transaction_id,
        "date": datetime.now(),
        "category": "Їжа",
        "type": "Expense",
        "amount": 450,
        "description": "Покупка продуктів на ринку",
        "created_at": datetime.now() - timedelta(days=5)
    }
    
    context = {
        "transaction": transaction,
        "title": "Деталі транзакції"
    }
    return render(request, "transaction_detail.html", context)

def budgets_list(request):
    budgets = [
        {"id": 1, "category": "Їжа", "limit": 2000, "spent": 1350, "remaining": 650, "percentage": 67.5},
        {"id": 2, "category": "Транспорт", "limit": 500, "spent": 280, "remaining": 220, "percentage": 56},
        {"id": 3, "category": "Розваги", "limit": 1000, "spent": 450, "remaining": 550, "percentage": 45},
    ]
    
    context = {
        "budgets": budgets,
        "title": "Бюджети"
    }
    return render(request, "budgets.html", context)

def reports(request):
    report_data = [
        {"category": "Їжа", "amount": 1350},
        {"category": "Транспорт", "amount": 280},
        {"category": "Розваги", "amount": 450},
        {"category": "Комунальні послуги", "amount": 800},
    ]
    
    total_spent = sum(r['amount'] for r in report_data)
    
    context = {
        "report_data": report_data,
        "total_spent": total_spent,
        "title": "Звіти"
    }
    return render(request, "reports.html", context)

def about(request):
    context = {"title": "Про застосунок"}
    return render(request, "about.html", context)
```

#### 9. URL маршрути

**Файл:** `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("transactions/", views.transactions_list, name="transactions"),
    path("transactions/<int:transaction_id>/", views.transaction_detail, name="transaction-detail"),
    path("budgets/", views.budgets_list, name="budgets"),
    path("reports/", views.reports, name="reports"),
    path("about/", views.about, name="about"),
]
```

---

### Додатковий рівень (за бажанням)

1. **Фільтрування транзакцій за датою**
   - Додати поле для вибору дати або діапазону дат
   - Фільтрувати список за цим параметром

2. **Графіки витрат**
   - Додати диаграму видатків за категоріями
   - Використовувати CSS для демонстрації прогресу

3. **Категорії**
   - Виводити список категорій
   - Показувати кількість транзакцій та суму для кожної категорії

4. **Прогноз бюджету**
   - Показати, на скільки днів вистачить грошей за поточного темпу видатків
   - Попередження якщо витрати перевищили ліміт

5. **Історія змін баланса**
   - Лінійний графік з показом баланса з часом

---

## Очікуваний результат

**Структура:**
```
expense_tracker/
    templates/
        base.html
        dashboard.html
        transactions.html
        transaction_detail.html
        budgets.html
        reports.html
        about.html
    static/
        css/
            style.css
        js/
            main.js
    views.py
    urls.py
    models.py
    manage.py
```

**Функціональність:**
- ✅ Панель керування з основними показниками
- ✅ Список всіх транзакцій із фільтруванням
- ✅ Детальна сторінка транзакції
- ✅ Управління бюджетами з прогрес-барами
- ✅ Звіти про витрати
- ✅ Стилізований інтерфейс

## Критерії оцінювання

| Критерій | Базовий | Додатковий |
|----------|---------|-----------|
| Панель керування | ✅ | - |
| Список транзакцій | ✅ | - |
| Детальна сторінка | ✅ | - |
| Управління бюджетами | ✅ | - |
| Звіти | ✅ | - |
| Статичні файли | ✅ | - |
| Фільтрування | - | ✅ |
| Графіки / діаграми | - | ✅ |
| Форматування грошей | - | ✅ |
| Прогноз бюджету | - | ✅ |

## Рекомендації

1. **Фільтри для грошей:** використовуйте `{{ amount|floatformat:2 }}` для коректного відображення
2. **Дати:** використовуйте `{{ date|date:"d.m.Y" }}` для українського формату
3. **Умовне форматування:** для від'ємних чисел додавайте клас CSS `negative`
4. **CSS Grid:** використовуйте для розташування карточок на панелі керування
5. **Прогрес-бари:** обчислюйте відсоток витрат в view і передавайте в шаблон

Успіхів у розробці! 💰
