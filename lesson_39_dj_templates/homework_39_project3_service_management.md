# Домашнє завдання. Заняття 39. Service Management System

## Мета
Створити веб-інтерфейс для управління послугами (автомобільні ремонти або салон краси). Практикуватися з шаблонами, статичними файлами, динамічним рендерингом даних, успадкуванням шаблонів.

## Вимоги до завдання

### Базовий рівень (обов'язково)

#### 1. Створити базовий шаблон `base.html`

**Файл:** `templates/base.html`

Структура для **Auto Service**:
```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Auto Service Center{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <header>
        <div class="header-content">
            <h1>🔧 Auto Service Center</h1>
            <p class="tagline">Якісний ремонт вашого автомобіля</p>
            <nav>
                <a href="{% url 'home' %}">Головна</a>
                <a href="{% url 'clients' %}">Клієнти</a>
                <a href="{% url 'orders' %}">Замовлення</a>
                <a href="{% url 'services' %}">Послуги</a>
                <a href="{% url 'inventory' %}">Запчастини</a>
                <a href="{% url 'about' %}">Про нас</a>
            </nav>
        </div>
    </header>

    <main class="container">
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2026 Auto Service Center | Надійна сервісна служба</p>
    </footer>

    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
```

Для **Beauty Clinic**, змініть назву та айконку:
```html
<h1>💅 Beauty Clinic & Aesthetic Medicine</h1>
<p class="tagline">Краса та здоров'я вашої шкіри</p>
```

#### 2. Головна сторінка `home.html`

**Файл:** `templates/home.html`

Вимоги:
- Успадковується від `base.html`
- Коротка інформація про сервіс
- Статистика: кількість клієнтів, замовлень, послуг
- Останні замовлення
- Посилання на основні функції

**Приклад для Auto Service:**
```html
{% extends 'base.html' %}

{% block title %}Головна | Auto Service Center{% endblock %}

{% block content %}
<section class="hero">
    <h2>Ласкаво просимо до нашого сервісу!</h2>
    <p>Ми надаємо високоякісні послуги з ремонту та обслуговування автомобілів.</p>
    <a href="{% url 'orders' %}" class="btn btn-primary">Переглянути замовлення</a>
</section>

<section class="statistics">
    <div class="stat-card">
        <h3>{{ total_clients }}</h3>
        <p>Клієнтів</p>
    </div>
    <div class="stat-card">
        <h3>{{ total_orders }}</h3>
        <p>Замовлень</p>
    </div>
    <div class="stat-card">
        <h3>{{ total_services }}</h3>
        <p>Послуг</p>
    </div>
</section>

<h2>Останні замовлення</h2>
<table class="orders-table">
    <thead>
        <tr>
            <th>Клієнт</th>
            <th>Автомобіль</th>
            <th>Статус</th>
            <th>Дата</th>
            <th>Дія</th>
        </tr>
    </thead>
    <tbody>
    {% for order in recent_orders %}
        <tr>
            <td>{{ order.client_name }}</td>
            <td>{{ order.vehicle }}</td>
            <td class="status-{{ order.status|lower }}">{{ order.status }}</td>
            <td>{{ order.date|date:"d.m.Y" }}</td>
            <td><a href="{% url 'order-detail' order.id %}">Деталі</a></td>
        </tr>
    {% empty %}
        <tr><td colspan="5">Замовлень немає</td></tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}
```

#### 3. Сторінка клієнтів `clients.html`

**Файл:** `templates/clients.html`

Вимоги:
- Успадковується від `base.html`
- Виводить список всіх клієнтів
- Таблиця з колонками: ім'я, контакт, кількість замовлень, дія
- Посилання на профіль клієнта
- Кнопка додавання нового клієнта

**Приклад для Auto Service:**
```html
{% extends 'base.html' %}

{% block content %}
<h2>Наші клієнти</h2>

<a href="{% url 'add-client' %}" class="btn btn-primary">+ Додати клієнта</a>

<table class="clients-table">
    <thead>
        <tr>
            <th>Ім'я</th>
            <th>Телефон</th>
            <th>Email</th>
            <th>Замовлень</th>
            <th>Дія</th>
        </tr>
    </thead>
    <tbody>
    {% for client in clients %}
        <tr>
            <td>{{ client.name }}</td>
            <td>{{ client.phone }}</td>
            <td>{{ client.email }}</td>
            <td>{{ client.order_count }}</td>
            <td>
                <a href="{% url 'client-detail' client.id %}">Профіль</a>
            </td>
        </tr>
    {% empty %}
        <tr><td colspan="5">Клієнтів немає</td></tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}
```

#### 4. Профіль клієнта `client_detail.html`

**Файл:** `templates/client_detail.html`

Вимоги:
- Успадковується від `base.html`
- Показує повну інформацію про клієнта
- Список замовлень цього клієнта
- Контактна інформація
- Кнопки редагування та видалення

#### 5. Сторінка замовлень `orders.html`

**Файл:** `templates/orders.html`

Вимоги:
- Успадковується від `base.html`
- Виводить всі замовлення
- Таблиця з колонками: клієнт, статус, дата, сума, дія
- Фільтрування за статусом (новий, у процесі, готово)
- Посилання на деталі замовлення

**Приклад з фільтруванням:**
```html
{% extends 'base.html' %}

{% block content %}
<h2>Замовлення</h2>

<!-- Фільтри по статусу -->
<div class="filters">
    <a href="{% url 'orders' %}" class="filter-btn {% if not status %}active{% endif %}">
        Всі
    </a>
    <a href="?status=new" class="filter-btn">Нові</a>
    <a href="?status=in_progress" class="filter-btn">У процесі</a>
    <a href="?status=completed" class="filter-btn">Готові</a>
</div>

<a href="{% url 'add-order' %}" class="btn btn-primary">+ Нове замовлення</a>

<table class="orders-table">
    <thead>
        <tr>
            <th>Клієнт</th>
            <th>Послуга</th>
            <th>Статус</th>
            <th>Дата</th>
            <th>Сума</th>
            <th>Дія</th>
        </tr>
    </thead>
    <tbody>
    {% for order in orders %}
        <tr>
            <td>{{ order.client_name }}</td>
            <td>{{ order.service_name }}</td>
            <td class="status-{{ order.status|lower }}">{{ order.get_status_display }}</td>
            <td>{{ order.date|date:"d.m.Y" }}</td>
            <td>{{ order.amount|floatformat:2 }} ₴</td>
            <td>
                <a href="{% url 'order-detail' order.id %}">Деталі</a>
                <a href="{% url 'edit-order' order.id %}">Редагувати</a>
            </td>
        </tr>
    {% empty %}
        <tr><td colspan="6">Замовлень немає</td></tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}
```

#### 6. Детальна сторінка замовлення `order_detail.html`

**Файл:** `templates/order_detail.html`

Вимоги:
- Успадковується від `base.html`
- Показує повну інформацію про замовлення
- Клієнт, послуга, статус, сума, дата створення
- Посилання на редагування та видалення
- Можливість змінити статус

#### 7. Сторінка послуг `services.html`

**Файл:** `templates/services.html`

Вимоги:
- Успадковується від `base.html`
- Виводить список послуг, які пропонує сервіс
- Кожна послуга: назва, опис, цена, дія

#### 8. Сторінка інвентарю `inventory.html`

**Файл:** `templates/inventory.html`

Вимоги:
- Успадковується від `base.html`
- Список запчастин / матеріалів зі складу
- Таблиця: назва, кількість, ціна, дія
- Посилання на редагування та видалення
- Попередження якщо кількість низька

#### 9. Статичні файли

**Файл:** `static/css/style.css`

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f2f5;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.15);
}

header h1 {
    font-size: 32px;
    margin-bottom: 5px;
}

.tagline {
    font-size: 16px;
    opacity: 0.9;
    margin-bottom: 20px;
}

header nav {
    display: flex;
    gap: 30px;
    flex-wrap: wrap;
}

header nav a {
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.3s;
}

header nav a:hover {
    opacity: 0.7;
}

.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 30px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.1);
}

/* Hero section */
.hero {
    text-align: center;
    padding: 40px 0;
    border-bottom: 2px solid #ecf0f1;
    margin-bottom: 40px;
}

.hero h2 {
    font-size: 28px;
    margin-bottom: 15px;
    color: #2c3e50;
}

.hero p {
    font-size: 16px;
    color: #7f8c8d;
    margin-bottom: 20px;
}

/* Statistics */
.statistics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin: 30px 0;
}

.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.stat-card h3 {
    font-size: 36px;
    margin-bottom: 10px;
}

.stat-card p {
    font-size: 14px;
    opacity: 0.9;
}

/* Tables */
.orders-table,
.clients-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

.orders-table th,
.clients-table th {
    background-color: #34495e;
    color: white;
    padding: 15px;
    text-align: left;
}

.orders-table td,
.clients-table td {
    padding: 15px;
    border-bottom: 1px solid #ecf0f1;
}

.orders-table tr:hover {
    background-color: #f8f9fa;
}

.status-new {
    background-color: #fff3cd;
    color: #856404;
    padding: 5px 10px;
    border-radius: 4px;
    font-weight: bold;
}

.status-in_progress {
    background-color: #cce5ff;
    color: #004085;
    padding: 5px 10px;
    border-radius: 4px;
    font-weight: bold;
}

.status-completed {
    background-color: #d4edda;
    color: #155724;
    padding: 5px 10px;
    border-radius: 4px;
    font-weight: bold;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 12px 25px;
    background-color: #667eea;
    color: white;
    text-decoration: none;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    font-weight: 500;
}

.btn:hover {
    background-color: #764ba2;
}

.btn-primary {
    background-color: #667eea;
    margin-bottom: 20px;
}

.btn-danger {
    background-color: #e74c3c;
}

.btn-danger:hover {
    background-color: #c0392b;
}

/* Filters */
.filters {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.filter-btn {
    padding: 8px 16px;
    background-color: white;
    color: #34495e;
    border: 2px solid #bdc3c7;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s;
}

.filter-btn.active,
.filter-btn:hover {
    background-color: #667eea;
    color: white;
    border-color: #667eea;
}

footer {
    background-color: #34495e;
    color: white;
    padding: 30px;
    text-align: center;
    margin-top: 50px;
}

@media (max-width: 768px) {
    .statistics {
        grid-template-columns: 1fr;
    }
    
    header nav {
        flex-direction: column;
        gap: 10px;
    }
    
    .orders-table,
    .clients-table {
        font-size: 14px;
    }
    
    .orders-table th,
    .clients-table th {
        padding: 10px;
    }
    
    .orders-table td,
    .clients-table td {
        padding: 10px;
    }
}
```

**Файл:** `static/js/main.js`

```javascript
document.addEventListener("DOMContentLoaded", function () {
    console.log("Service Management System завантажився!");
    
    // Підсвічування активного меню
    const links = document.querySelectorAll("header nav a");
    const currentPage = window.location.pathname;
    
    links.forEach(link => {
        if (link.href.includes(currentPage)) {
            link.style.opacity = "0.5";
            link.style.textDecoration = "underline";
        }
    });
    
    // Подтвердження видалення
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Ви впевнені що хочете видалити?')) {
                e.preventDefault();
            }
        });
    });
});
```

#### 10. View функції

**Файл:** `views.py`

```python
from django.shortcuts import render
from datetime import datetime, timedelta

def home(request):
    clients = [
        {"id": 1, "name": "Іван Петренко", "phone": "+380671234567", "email": "ivan@example.com"},
        {"id": 2, "name": "Марія Сидоренко", "phone": "+380501234567", "email": "maria@example.com"},
    ]
    
    orders = [
        {"id": 1, "client_name": "Іван Петренко", "vehicle": "Toyota Camry", "status": "Completed", "date": datetime.now() - timedelta(days=2), "amount": 3500},
        {"id": 2, "client_name": "Марія Сидоренко", "vehicle": "Honda CR-V", "status": "In Progress", "date": datetime.now() - timedelta(days=1), "amount": 2500},
        {"id": 3, "client_name": "Іван Петренко", "vehicle": "Toyota Camry", "status": "New", "date": datetime.now(), "amount": 1500},
    ]
    
    context = {
        "total_clients": len(clients),
        "total_orders": len(orders),
        "total_services": 12,
        "recent_orders": orders[:3],
        "title": "Головна"
    }
    return render(request, "home.html", context)

def clients_list(request):
    clients = [
        {"id": 1, "name": "Іван Петренко", "phone": "+380671234567", "email": "ivan@example.com", "order_count": 5},
        {"id": 2, "name": "Марія Сидоренко", "phone": "+380501234567", "email": "maria@example.com", "order_count": 3},
        {"id": 3, "name": "Петро Іванов", "phone": "+380951234567", "email": "petro@example.com", "order_count": 8},
    ]
    
    context = {
        "clients": clients,
        "title": "Клієнти"
    }
    return render(request, "clients.html", context)

def client_detail(request, client_id):
    client = {"id": client_id, "name": "Іван Петренко", "phone": "+380671234567", "email": "ivan@example.com"}
    
    context = {
        "client": client,
        "title": f"Профіль {client['name']}"
    }
    return render(request, "client_detail.html", context)

def orders_list(request):
    orders = [
        {"id": 1, "client_name": "Іван Петренко", "service_name": "Ремонт двигуна", "status": "completed", "get_status_display": "Готово", "date": datetime.now() - timedelta(days=2), "amount": 3500},
        {"id": 2, "client_name": "Марія Сидоренко", "service_name": "Заміна масла", "status": "in_progress", "get_status_display": "У процесі", "date": datetime.now() - timedelta(days=1), "amount": 2500},
        {"id": 3, "client_name": "Іван Петренко", "service_name": "Діагностика", "status": "new", "get_status_display": "Нове", "date": datetime.now(), "amount": 1500},
    ]
    
    context = {
        "orders": orders,
        "title": "Замовлення"
    }
    return render(request, "orders.html", context)

def order_detail(request, order_id):
    order = {"id": order_id, "client_name": "Іван Петренко", "service_name": "Ремонт двигуна", "status": "Готово", "amount": 3500, "date": datetime.now() - timedelta(days=2)}
    
    context = {
        "order": order,
        "title": "Деталі замовлення"
    }
    return render(request, "order_detail.html", context)

def services_list(request):
    services = [
        {"id": 1, "name": "Ремонт двигуна", "description": "Капітальний ремонт двигуна", "price": 3500},
        {"id": 2, "name": "Заміна масла", "description": "Заміна масла та фільтра", "price": 500},
        {"id": 3, "name": "Діагностика", "description": "Повна комп'ютерна діагностика", "price": 800},
    ]
    
    context = {
        "services": services,
        "title": "Послуги"
    }
    return render(request, "services.html", context)

def inventory(request):
    inventory = [
        {"id": 1, "name": "Моторне масло Shell", "quantity": 15, "price": 150},
        {"id": 2, "name": "Повітряний фільтр", "quantity": 8, "price": 250},
        {"id": 3, "name": "Масляний фільтр", "quantity": 12, "price": 180},
        {"id": 4, "name": "Гальмівні колодки", "quantity": 2, "price": 1500},  # Низька кількість
    ]
    
    context = {
        "inventory": inventory,
        "title": "Інвентар"
    }
    return render(request, "inventory.html", context)

def about(request):
    context = {"title": "Про нас"}
    return render(request, "about.html", context)
```

#### 11. URL маршрути

**Файл:** `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("clients/", views.clients_list, name="clients"),
    path("clients/<int:client_id>/", views.client_detail, name="client-detail"),
    path("orders/", views.orders_list, name="orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order-detail"),
    path("services/", views.services_list, name="services"),
    path("inventory/", views.inventory, name="inventory"),
    path("about/", views.about, name="about"),
]
```

---

### Додатковий рівень (за бажанням)

1. **Фільтрування замовлень**
   - Додати фільтри за статусом
   - Добавити пошук по клієнту

2. **Попередження про низькі запаси**
   - Виділити запчастини з малою кількістю червоним
   - Показати попередження на головній сторінці

3. **Карточки клієнтів**
   - Список автомобілів клієнта
   - Історія замовлень клієнта

4. **Розпорядок послуг**
   - Витратити час на послугу та показати у замовленні
   - Календар із зайнятими часами

5. **Статистика**
   - Найпопулярніша послуга
   - Клієнт з найбільшою кількістю замовлень
   - Тренд замовлень за місяцями

---

## Очікуваний результат

**Структура:**
```
service_management/
    templates/
        base.html
        home.html
        clients.html
        client_detail.html
        orders.html
        order_detail.html
        services.html
        inventory.html
        about.html
    static/
        css/
            style.css
        js/
            main.js
        img/
            (logo, favicon тощо)
    views.py
    urls.py
    models.py
    manage.py
```

**Функціональність:**
- ✅ Панель керування з основною інформацією
- ✅ Управління клієнтами та їхніми профілями
- ✅ Система замовлень із фільтруванням
- ✅ Каталог послуг
- ✅ Управління складом / інвентарем
- ✅ Повний CSS дизайн

## Критерії оцінювання

| Критерій | Базовий | Додатковий |
|----------|---------|-----------|
| Головна сторінка | ✅ | - |
| Управління клієнтами | ✅ | - |
| Управління замовленнями | ✅ | - |
| Каталог послуг | ✅ | - |
| Управління складом | ✅ | - |
| Статичні файли | ✅ | - |
| Фільтрування | - | ✅ |
| Попередження про запаси | - | ✅ |
| Розпорядок / календар | - | ✅ |
| Статистика | - | ✅ |

## Рекомендації

1. **Структура:** почніть із `base.html` як основи
2. **Таблиці:** для списків використовуйте `{% for %}` з `{% empty %}`
3. **Статус:** розфарбуйте статуси замовлень CSS класами
4. **Навігація:** активна сторінка повинна бути помітною
5. **Мобільність:** тестуйте з мобільного пристрою, додайте `@media` запити

## Рекомендації для вибору домену

**Auto Service:**
- ✅ Якщо цікавить механіка та технологія
- ✅ Більше технічних термінів

**Beauty Clinic:**
- ✅ Якщо цікавить estetyka і здоров'я
- ✅ Більше "жіночих" услуг (процедури, пілінги)

Estructura і логіка однакові, просто змініть назви та описи.

Успіхів у розробці! 🚗💅
