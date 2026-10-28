# Домашнє завдання. Заняття 39. Task & Bug Manager

## Мета
Створити веб-інтерфейс для керування задачами та багами. Практикуватися з шаблонами Django, статичними файлами, успадкуванням шаблонів та динамічним рендерингом даних.

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
    <title>{% block title %}Task & Bug Manager{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <header>
        <nav>
            <h1>Task & Bug Manager</h1>
            <ul>
                <li><a href="{% url 'home' %}">Головна</a></li>
                <li><a href="{% url 'tasks' %}">Завдання</a></li>
                <li><a href="{% url 'bugs' %}">Баги</a></li>
                <li><a href="{% url 'about' %}">Про застосунок</a></li>
            </ul>
        </nav>
    </header>

    <main class="container">
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2026 Task & Bug Manager | Олександр Панченко</p>
    </footer>

    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
```

#### 2. Створити сторінку списку задач `tasks.html`

**Файл:** `templates/tasks/tasks.html`

Вимоги:
- Успадковується від `base.html`
- Виводить список всіх завдань (мок-дані або із бази даних)
- Кожне завдання показує: назву, статус, пріоритет, дедлайн
- Якщо завдань немає, показати повідомлення
- Використовувати `{% for %}` та `{% empty %}`
- Кожне завдання має посилання на деталі (використовувати `{% url %}`)

**Приклад структури:**
```html
{% extends 'base.html' %}

{% block title %}Завдання | Task & Bug Manager{% endblock %}

{% block content %}
<h2>Список завдань</h2>

<table class="tasks-table">
    <thead>
        <tr>
            <th>Назва</th>
            <th>Статус</th>
            <th>Пріоритет</th>
            <th>Дедлайн</th>
            <th>Дія</th>
        </tr>
    </thead>
    <tbody>
    {% for task in tasks %}
        <tr>
            <td>{{ task.title }}</td>
            <td class="status-{{ task.status|lower }}">{{ task.status }}</td>
            <td class="priority-{{ task.priority|lower }}">{{ task.priority }}</td>
            <td>{{ task.deadline|date:"d.m.Y" }}</td>
            <td>
                <a href="{% url 'task-detail' task.id %}">Переглянути</a>
            </td>
        </tr>
    {% empty %}
        <tr>
            <td colspan="5">Завдань немає. Створіть перше завдання!</td>
        </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}
```

#### 3. Створити сторінку деталей завдання `task_detail.html`

**Файл:** `templates/tasks/task_detail.html`

Вимоги:
- Успадковується від `base.html`
- Показує повну інформацію про одне завдання
- Виводить: назву, опис, статус, пріоритет, дедлайн, автора
- Посилання назад на список задач
- Кнопки редагування та видалення

#### 4. Створити сторінку багів `bugs.html`

**Аналогічна до `tasks.html`**, але для багів:
- Виводить список багів
- Показує: назву, пріоритет, статус, дату сповіщення
- Посилання на деталі кожного багу

#### 5. Статичні файли

**Файл:** `static/css/style.css`

Мінімальні стилі для:
- Header (колір фону, навігація)
- Main контент (поля, таблиці)
- Footer (колір, вирівнювання)
- Статус та пріоритет завдань (різні кольори)

**Приклад:**
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
}

header {
    background-color: #2c3e50;
    color: white;
    padding: 20px;
}

header h1 {
    margin-bottom: 10px;
}

header nav ul {
    list-style: none;
    display: flex;
    gap: 20px;
}

header nav a {
    color: white;
    text-decoration: none;
}

header nav a:hover {
    text-decoration: underline;
}

.container {
    max-width: 900px;
    margin: 20px auto;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
}

.tasks-table {
    width: 100%;
    border-collapse: collapse;
}

.tasks-table th {
    background-color: #ecf0f1;
    padding: 10px;
    text-align: left;
    border-bottom: 2px solid #bdc3c7;
}

.tasks-table td {
    padding: 10px;
    border-bottom: 1px solid #ecf0f1;
}

.status-open {
    color: #e74c3c;
    font-weight: bold;
}

.status-closed {
    color: #27ae60;
    font-weight: bold;
}

.priority-high {
    background-color: #ffe5e5;
    color: #c0392b;
}

.priority-medium {
    background-color: #fff3cd;
    color: #856404;
}

.priority-low {
    background-color: #e3f2fd;
    color: #1565c0;
}

footer {
    background-color: #2c3e50;
    color: white;
    padding: 20px;
    text-align: center;
    margin-top: 40px;
}
```

**Файл:** `static/js/main.js`

Мінімальна логіка:
```javascript
document.addEventListener("DOMContentLoaded", function () {
    console.log("Task & Bug Manager завантажився!");
    
    // Приклад: колір статусу
    const openStatus = document.querySelectorAll(".status-open");
    openStatus.forEach(el => {
        el.style.cursor = "pointer";
    });
});
```

#### 6. View функції

**Файл:** `views.py`

```python
from django.shortcuts import render
from datetime import datetime, timedelta

def home(request):
    context = {
        "title": "Головна"
    }
    return render(request, "home.html", context)

def tasks_list(request):
    # Мок-дані (по частинам замінити на запити до БД)
    tasks = [
        {
            "id": 1,
            "title": "Виправити баг входу",
            "status": "Open",
            "priority": "High",
            "deadline": datetime.now() + timedelta(days=3)
        },
        {
            "id": 2,
            "title": "Додати функцію сортування",
            "status": "In Progress",
            "priority": "Medium",
            "deadline": datetime.now() + timedelta(days=7)
        },
        {
            "id": 3,
            "title": "Написати документацію",
            "status": "Closed",
            "priority": "Low",
            "deadline": datetime.now() - timedelta(days=2)
        },
    ]
    
    context = {
        "tasks": tasks,
        "title": "Завдання"
    }
    return render(request, "tasks/tasks.html", context)

def task_detail(request, task_id):
    # Мок-дані для деталей
    task = {
        "id": task_id,
        "title": "Виправити баг входу",
        "description": "Користувачі не можуть увійти з цифрами у паролі.",
        "status": "Open",
        "priority": "High",
        "author": "Іван Петренко",
        "deadline": datetime.now() + timedelta(days=3),
        "created_at": datetime.now() - timedelta(days=5)
    }
    
    context = {
        "task": task,
        "title": task['title']
    }
    return render(request, "tasks/task_detail.html", context)

def bugs_list(request):
    bugs = [
        {
            "id": 1,
            "title": "Вихід з системи виснажує пам'ять",
            "priority": "High",
            "status": "Open",
            "reported_at": datetime.now() - timedelta(days=1)
        },
        {
            "id": 2,
            "title": "Невірне сортування списків",
            "priority": "Medium",
            "status": "In Progress",
            "reported_at": datetime.now() - timedelta(days=3)
        },
    ]
    
    context = {
        "bugs": bugs,
        "title": "Баги"
    }
    return render(request, "bugs/bugs.html", context)

def about(request):
    context = {
        "title": "Про застосунок"
    }
    return render(request, "about.html", context)
```

#### 7. URL маршрути

**Файл:** `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.tasks_list, name="tasks"),
    path("tasks/<int:task_id>/", views.task_detail, name="task-detail"),
    path("bugs/", views.bugs_list, name="bugs"),
    path("about/", views.about, name="about"),
]
```

---

### Додатковий рівень (за бажанням)

1. **Фільтрування завдань**
   - Додати можливість фільтрувати завдання за статусом та пріоритетом
   - Передавати параметри в шаблон
   - Використовувати `{% if %}` для умовного відображення

2. **Вулички для коментарів**
   - Додати сторінку списку коментарів (реальні дані або мок)
   - Показувати коментарі під кожним завданням

3. **Покращена навігація**
   - Активна сторінка у навігації (добавляти клас `active` до посилання)
   - Хлібні крихти (breadcrumbs)

4. **Поле пошуку**
   - Додати форму пошуку на основній сторінці
   - Фільтрувати завдання за назвою

5. **Часові файли**
   - Використовувати фільтр `date` для коректного форматування дат
   - Додати фільтр `timesince` для " 3 дні тому"

---

## Очікуваний результат

**Структура проєкту:**
```
task_manager/
    templates/
        base.html
        home.html
        about.html
        tasks/
            tasks.html
            task_detail.html
        bugs/
            bugs.html
            bug_detail.html
        includes/
            header.html
            footer.html
    static/
        css/
            style.css
        js/
            main.js
        img/
            logo.png (за бажанням)
    views.py
    urls.py
    models.py (де вже є моделі)
    manage.py
```

**Функціональність:**
- ✅ Шаблони успадковуються від базового
- ✅ Динамічні посилання через `{% url %}`
- ✅ Таблиці з даними, які рендяться через `{% for %}`
- ✅ Статичні файли підключені коректно
- ✅ Сторінка відображається без помилок
- ✅ Навігація працює

## Критерії оцінювання

| Критерій | Базовий | Додатковий |
|----------|---------|-----------|
| Базовий шаблон `base.html` | ✅ | - |
| Сторінка завдань із таблицею | ✅ | - |
| Сторінка деталей завдання | ✅ | - |
| Статичні файли (CSS + JS) | ✅ | - |
| Сторінка багів | ✅ | - |
| Правильна структура папок | ✅ | - |
| Успадкування шаблонів | ✅ | - |
| Динамічні посилання `{% url %}` | ✅ | - |
| Фільтрування / пошук | - | ✅ |
| Часові фільтри | - | ✅ |
| Коментарі | - | ✅ |

## Рекомендації

1. **Початок:** обов'язково створіть `base.html` — це основа для всіх інших
2. **Статичні файли:** не забудьте `{% load static %}` у базовому шаблоні
3. **Посилання:** завжди використовуйте `{% url 'name' %}` замість жорсткої адреси
4. **Мок-дані:** поки у моделей немає — використовуйте словники у views.py
5. **CSS:** почніть зі простих стилів, потім покращуйте дизайн

## Домашня робота на наступне заняття

Підготуватися до роботи з формами Django:
- Прочитати про `django.forms.Form`
- Прочитати про HTML теги `<form>`, `<input>`, `<textarea>`
- Підумати, як виглядатиме форма для створення нового завдання

Бажаю успіхів! 🚀
