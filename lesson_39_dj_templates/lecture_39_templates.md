# Заняття 39. Шаблони та статичні файли: крок за кроком збираємо демо-LMS

## Мета заняття

Навчитися будувати HTML-сторінки Django за допомогою шаблонів і підключати до них CSS, JavaScript та зображення. Замість того щоб спочатку вивчати теорію, ми **нарощуємо невеликий сайт — демо-LMS** (каталог курсів, сторінка курсу, уроки, кабінет студента) маленькими кроками. Після кожного кроку сайт працює, і ви бачите результат у браузері.

Після заняття ви зможете:

- пройти повний цикл «дані → view → шаблон → url → перевірка в браузері» для нової сторінки;
- виводити дані в шаблонах: змінні, цикли, умови, фільтри;
- побачити, навіщо потрібен базовий шаблон, і побудувати сторінки через `extends`, `block` та `include`;
- будувати посилання через `{% url %}`;
- підключати CSS, JavaScript і зображення через `{% static %}`;
- налаштувати власну сторінку 404;
- повторити той самий шлях у власному навчальному проєкті (Task & Bug Manager, Expense Tracker, Service Management System).

***

## Ритм заняття

Кожен крок складається з однакових частин. Запам'ятайте цей ритм: за ним ви будете створювати кожну нову сторінку.

```text
1. Дані      — звідки беремо інформацію
2. View      — функція, яка бере дані й готує контекст
3. Шаблон    — як це виглядає в HTML
4. URL       — за якою адресою це відкривається
5. Показати  — запускаємо сервер і дивимося, що вийшло
```

Після кожного кроку робимо `git commit`. Тоді, якщо щось зламалося, можна повернутися до останнього робочого стану (`git status` покаже, що змінилося, а `git diff` — що саме).

***

## План: що з'являється на кожному кроці

| Крок | Що додаємо | Нове в Django-шаблонах | Що побачимо |
| --- | --- | --- | --- |
| 0 | підготовка проєкту | — | сервер запускається |
| 1 | список курсів | змінні, `for`/`empty`, контекст | `/courses/` — маркований список |
| 2 | сторінка курсу | `{% url %}`, вкладені дані | перехід зі списку на курс, 404 |
| 3 | `base.html` | `extends`, `block` | однакова «шапка» на всіх сторінках |
| 4 | головна, меню й підвал | `include`, `with`, `request`, `now` | `/` і підсвічене меню |
| 5 | картки курсів | фільтри, `if`, `include` з даними | сітка карток зі значком «Новий» |
| 6 | уроки | `forloop.counter`, умови | сторінка уроку з кнопками «назад/далі» |
| 7 | кабінет студента | `date`, `default`, таблиці | таблиця з дедлайнами |
| 8 | CSS і логотип | `{% load static %}`, `{% static %}` | сайт стає гарним |
| 9 | пошук | `request.GET`, форма | `/courses/?q=sql` |
| 10 | JavaScript | статичний JS, `defer` | кнопка «пройдено», живий фільтр |
| 11 | власна 404 | `404.html` | своя сторінка помилки |

Шлях запиту, який ми вже знаємо із заняття 38, тепер доповнюється шаблоном:

```text
Браузер: GET /courses/django-web/
   │
   ▼
urls.py  ──►  views.course_detail(request, slug="django-web")
                    │  бере дані, формує контекст
                    ▼
        render(request, "courses/course_detail.html", context)
                    │  Django збирає шаблон: base.html + дочірній шаблон + include
                    ▼
        Готовий HTML  ──►  браузер  ──►  окремі запити за CSS, JS і картинками
```

Останній рядок важливий: HTML приходить першим, а **браузер сам** потім робить додаткові запити за `/static/css/lms.css` та іншими файлами.

***

## Крок 0. Підготовка проєкту

**Мета:** мати проєкт `lms` із порожнім застосунком `courses`, який підключено до адреси `/`.

1. Створіть гілку та застосунок:

```bash
git checkout -b lesson-39
python manage.py startapp courses
```

2. У `lms/settings.py` додайте застосунок і виправте мову та часовий пояс:

```python
INSTALLED_APPS = [
    # ... стандартні застосунки Django ...
    "courses",
]

LANGUAGE_CODE = "uk"            # не "uk-uk": такого коду мови не існує
TIME_ZONE = "Europe/Kyiv"
```

3. У `lms/urls.py` підключіть маршрути застосунку (файл `courses/urls.py` ми створимо на кроці 1):

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("courses.urls")),
]
```

> Якщо у вас лишився застосунок із заняття 38 (наприклад, `studrada`), приберіть його `include` з `lms/urls.py`, щоб не було конфліктів імен маршрутів (`home` тощо).

**Показати:** поки що нічого, сервер запуститься лише після кроку 1 (без `courses/urls.py` Django скаржитиметься, що не може імпортувати модуль).

***

## Крок 1. Перша сторінка: список курсів

**Мета:** показати в браузері назви курсів. Це найпростіший повний цикл.

### 1.1. Дані

У реальному проєкті дані лежатимуть у базі даних. Зараз для простоти створіть файл `courses/data.py` з готовими даними: список курсів, у кожного свій список уроків. Деякі поля (`progress`, `deadline`, `is_new`, `STUDENT`) нам знадобляться лише на наступних кроках.

```python
"""Демо-дані. Пізніше їх замінять моделі та база даних."""
from datetime import date

COURSES = [
    {
        "slug": "qa-basics",
        "title": "QA: основи тестування",
        "level": "Початковий",
        "teacher": "Олександр Панченко",
        "hours": 24,
        "is_new": True,
        "progress": 60,
        "deadline": date(2026, 11, 20),
        "description": "Що таке якість, тест-кейси, баг-репорти та життєвий цикл дефекту. "
                       "Курс для тих, хто починає шлях у QA.",
        "lessons": [
            {"title": "Що таке QA і навіщо воно потрібне", "minutes": 45,
             "summary": "Якість, QA, QC і тестування: чим вони відрізняються."},
            {"title": "Тест-кейси та чек-листи", "minutes": 60,
             "summary": "Як описати перевірку, щоб її міг повторити будь-хто."},
            {"title": "Баг-репорти", "minutes": 50,
             "summary": "Структура дефекту, серйозність і пріоритет."},
        ],
    },
    {
        "slug": "django-web",
        "title": "Django: веб-розробка",
        "level": "Середній",
        "teacher": "Олександр Панченко",
        "hours": 40,
        "is_new": False,
        "progress": 25,
        "deadline": date(2026, 12, 15),
        "description": "Маршрутизація, представлення, шаблони, моделі та форми. "
                       "Поступово збираємо власний навчальний проєкт.",
        "lessons": [
            {"title": "Маршрутизація та представлення", "minutes": 80,
             "summary": "path(), include(), views, render()."},
            {"title": "Шаблони та статичні файли", "minutes": 80,
             "summary": "Успадкування шаблонів, include, CSS і JavaScript."},
            {"title": "Моделі та ORM", "minutes": 80,
             "summary": "Таблиці як класи Python, запити через QuerySet."},
            {"title": "Форми", "minutes": 80,
             "summary": "Прийом даних від користувача та валідація."},
        ],
    },
    {
        "slug": "sql-postgres",
        "title": "SQL та PostgreSQL",
        "level": "Початковий",
        "teacher": "Олександр Панченко",
        "hours": 20,
        "is_new": False,
        "progress": 100,
        "deadline": None,
        "description": "SELECT, JOIN, DML та транзакції на реальній базі PostgreSQL.",
        "lessons": [
            {"title": "SELECT і фільтрація", "minutes": 70,
             "summary": "WHERE, ORDER BY, LIMIT."},
            {"title": "JOIN", "minutes": 70,
             "summary": "INNER та LEFT JOIN на навчальній схемі LMS."},
        ],
    },
]

STUDENT = {"name": "Олена Коваль", "email": "olena@example.com"}
```

### 1.2. View

У `courses/views.py` (замість того, що там було):

```python
from django.shortcuts import render

from .data import COURSES


def course_list(request):
    return render(request, "courses/course_list.html", {"courses": COURSES})
```

View робить дві речі: бере дані (`COURSES`) і передає їх у шаблон словником (контекстом).

### 1.3. Шаблон

Створіть `courses/templates/courses/course_list.html`. Зверніть увагу на **подвійну папку** `templates/courses/`: так ми уникаємо конфліктів назв між застосунками (заняття 38).

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Курси</title>
</head>
<body>
    <h1>Каталог курсів</h1>
    <ul>
    {% for course in courses %}
        <li>{{ course.title }}</li>
    {% empty %}
        <li>Курсів поки немає.</li>
    {% endfor %}
    </ul>
</body>
</html>
```

**Що нового в синтаксисі:**

- `{{ course.title }}` — вивести значення. Крапка означає «візьми з цього об'єкта»: для словника — ключ, для об'єкта — атрибут, для списку — індекс (`courses.0`).
- `{% for course in courses %} … {% endfor %}` — цикл.
- `{% empty %}` — що показати, якщо список порожній.

### 1.4. URL

Створіть `courses/urls.py`:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
]
```

### 1.5. Показати

```bash
python manage.py runserver
```

Відкрийте `http://127.0.0.1:8000/courses/`. Має з'явитися заголовок і три назви курсів.

**Експерименти (за 2 хвилини):**

1. У view тимчасово передайте `{"courses": []}` і оновіть сторінку. Що змінилося? Це спрацював блок `{% empty %}`.
2. У шаблоні напишіть `{{ titel }}` замість `{{ course.title }}`. Помилки не буде, а на сторінці порожні пункти: **Django мовчки підставляє порожній рядок**, якщо змінної немає. Це найчастіша причина «на сторінці нічого немає».

Поверніть, як було, і закомітьте:

```bash
git add . && git commit -m "Крок 1: список курсів"
```

***

## Крок 2. Сторінка курсу і посилання між сторінками

**Мета:** із каталогу можна перейти на сторінку окремого курсу.

### 2.1. Дані

Додайте в кінець `courses/data.py` допоміжну функцію пошуку курсу:

```python
def get_course(slug):
    """Повертає курс за slug або None."""
    for course in COURSES:
        if course["slug"] == slug:
            return course
    return None
```

### 2.2. View

Додайте у `courses/views.py` нову функцію і оновіть імпорти (угорі файлу):

```python
from django.http import Http404
from django.shortcuts import render

from .data import COURSES, get_course


def course_detail(request, slug):
    course = get_course(slug)
    if course is None:
        raise Http404(f"Курс {slug} не знайдено")
    return render(request, "courses/course_detail.html", {"course": course})
```

Якщо курсу немає, піднімаємо `Http404` (як на занятті 38).

### 2.3. Шаблон

Створіть `courses/templates/courses/course_detail.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ course.title }}</title>
</head>
<body>
    <p><a href="{% url 'course_list' %}">← Усі курси</a></p>

    <h1>{{ course.title }}</h1>
    <p>Викладач: {{ course.teacher }} · Рівень: {{ course.level }} · {{ course.hours }} год</p>
    <p>{{ course.description }}</p>

    <h2>Програма курсу</h2>
    <ol>
    {% for lesson in course.lessons %}
        <li>{{ lesson.title }} ({{ lesson.minutes }} хв)</li>
    {% endfor %}
    </ol>
</body>
</html>
```

Тут ми вперше пишемо `{% url 'course_list' %}`. Також звернемо увагу на `course.lessons`: це вкладений список, і ми проходимо по ньому ще одним циклом.

### 2.4. URL

Додайте маршрут у `courses/urls.py`:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
]
```

Маршрут має параметр `<slug:slug>`: ця частина адреси потрапляє у view як аргумент `slug`.

### 2.5. Посилання зі списку на курс

Оновіть `course_list.html`: назва курсу стає посиланням.

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Курси</title>
</head>
<body>
    <h1>Каталог курсів</h1>
    <ul>
    {% for course in courses %}
        <li><a href="{% url 'course_detail' course.slug %}">{{ course.title }}</a> — {{ course.level }}</li>
    {% empty %}
        <li>Курсів поки немає.</li>
    {% endfor %}
    </ul>
</body>
</html>
```

**Новий тег `{% url %}`.** Замість ручного запису адреси (`/courses/django-web/`) ми пишемо **ім'я маршруту** і його параметри:

```html
{% url 'course_list' %}                     {# → /courses/ #}
{% url 'course_detail' course.slug %}       {# → /courses/django-web/ #}
```

Якщо змінити шлях у `urls.py`, жоден шаблон правити не треба.

### 2.6. Показати

1. `http://127.0.0.1:8000/courses/` → клік по назві → сторінка курсу → посилання «← Усі курси».
2. `http://127.0.0.1:8000/courses/nope/` → 404 (спрацював `Http404`).
3. `http://127.0.0.1:8000/courses/Bad_Slug!/` → теж 404, але з іншої причини: адреса не підійшла під конвертер `slug`, view навіть не викликався.

```bash
git add . && git commit -m "Крок 2: сторінка курсу та посилання"
```

***

## Крок 3. Бачимо дублювання і створюємо `base.html`

**Мета:** прибрати копіювання однакового HTML.

### 3.1. Проблема

Відкрийте поруч `course_list.html` і `course_detail.html`. Обидва починаються з однакових 6–7 рядків (`<!DOCTYPE>`, `<head>`, `<meta>`, `<title>`…). Уявіть, що таких сторінок буде 10, і треба додати в `<head>` ще одну мета-теґ. Правити доведеться 10 файлів.

### 3.2. Рішення: базовий шаблон і успадкування

Базовий шаблон описує спільний каркас сторінки та **місця, які можна замінити** (`block`). Дочірній шаблон каже `{% extends %}` і заповнює лише ці місця.

Спочатку підкажемо Django, де шукати загальні шаблони (`templates/` у корені проєкту). У `lms/settings.py`:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],      # загальні шаблони проєкту
        "APP_DIRS": True,                      # + templates/ усіх застосунків
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

> `BASE_DIR / "templates"` замість `"templates"`: відносний шлях працює лише тоді, коли сервер запущено з кореня проєкту, а повний шлях працює завжди.

Створіть папку `templates/` поруч із `manage.py` і файл `templates/base.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Демо LMS{% endblock %} | Демо LMS</title>
</head>
<body>
    <header><strong>Демо LMS</strong></header>

    <main class="container">
        {% block content %}{% endblock %}
    </main>

    <footer><small>© Демо LMS</small></footer>

</body>
</html>
```

Тут два блоки: `title` і `content`. Усе інше спільне.

### 3.3. Переписуємо сторінки

Тепер `course_list.html` і `course_detail.html` стають набагато коротшими:

```html
{% extends "base.html" %}

{% block title %}Курси{% endblock %}

{% block content %}
<h1>Каталог курсів</h1>
<ul>
{% for course in courses %}
    <li><a href="{% url 'course_detail' course.slug %}">{{ course.title }}</a> — {{ course.level }}</li>
{% empty %}
    <li>Курсів поки немає.</li>
{% endfor %}
</ul>
{% endblock %}
```

```html
{% extends "base.html" %}

{% block title %}{{ course.title }}{% endblock %}

{% block content %}
<p class="muted"><a href="{% url 'course_list' %}">← Усі курси</a></p>

<h1>{{ course.title }}</h1>
<p class="muted">Викладач: {{ course.teacher }} · Рівень: {{ course.level }} · {{ course.hours }} год</p>
<p>{{ course.description }}</p>

<h2>Програма курсу</h2>
<ol class="lessons">
    {% for lesson in course.lessons %}
    <li>
        {{ lesson.title }}
        <span class="muted">{{ lesson.minutes }} хв</span>
    </li>
    {% endfor %}
</ol>
{% endblock %}
```

**Правила успадкування:**

- `{% extends "base.html" %}` має бути **першим тегом** файлу. Навіть `{% load static %}` перед ним призведе до помилки `{% extends 'base.html' %} must be the first tag in the template`.
- Увесь вміст дочірнього шаблону пишемо **усередині** `{% block %}`. Усе, що поза блоками, не виводиться.
- Атрибути `class="…"` у розмітці поки нічого не роблять: вони знадобляться для CSS на кроці 8.

### 3.4. Показати

Відкрийте `/courses/` та `/courses/django-web/`. Тепер на обох сторінках є «шапка» «Демо LMS», а на вкладці браузера заголовок виглядає як **«Курси | Демо LMS»**.

**Експеримент:** змініть текст у `<header>` у `base.html` і оновіть обидві сторінки. Змінилися обидві, а редагували ми один файл. Саме так працює успадкування.

```bash
git add . && git commit -m "Крок 3: базовий шаблон base.html"
```

***

## Крок 4. Головна сторінка, меню і підвал (`include`)

**Мета:** додати головну сторінку та меню, яке є на кожній сторінці й підсвічує поточний розділ.

### 4.1. View

```python
def home(request):
    context = {
        "featured": COURSES[:2],
        "courses_count": len(COURSES),
        "lessons_count": sum(len(c["lessons"]) for c in COURSES),
    }
    return render(request, "courses/home.html", context)
```

### 4.2. Шаблон головної

`courses/templates/courses/home.html`:

```html
{% extends "base.html" %}

{% block title %}Головна{% endblock %}

{% block content %}
<section class="hero">
    <h1>Вчимося разом</h1>
    <p>Легка демо-LMS: каталог курсів, уроки та особистий кабінет студента.</p>
    <p class="stats">Курсів: <strong>{{ courses_count }}</strong> · Уроків: <strong>{{ lessons_count }}</strong></p>
    <a class="btn" href="{% url 'course_list' %}">Переглянути курси</a>
</section>

<h2>Рекомендовані курси</h2>
<ul>
    {% for course in featured %}
        <li><a href="{% url 'course_detail' course.slug %}">{{ course.title }}</a></li>
    {% empty %}
        <li>Курсів поки немає.</li>
    {% endfor %}
</ul>
{% endblock %}
```

### 4.3. URL

```python
from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("", views.home, name="home"),
]
```

### 4.4. Меню і підвал через `include`

Меню та підвал повторюються на кожній сторінці, але вони не «каркас», а окремі шматки. Їх виносять у файли й підключають тегом `{% include %}`.

Створіть `templates/includes/navbar.html`:

```html
{% with current=request.resolver_match.url_name %}
<header class="site-header">
    <div class="container header-inner">
        <a class="brand" href="{% url 'home' %}">
            <span>Демо LMS</span>
        </a>
        <nav>
            <a href="{% url 'home' %}" {% if current == 'home' %}class="active"{% endif %}>Головна</a>
            <a href="{% url 'course_list' %}"
               {% if current == 'course_list' or current == 'course_detail' or current == 'lesson_detail' %}class="active"{% endif %}>Курси</a>
        </nav>
    </div>
</header>
{% endwith %}
```

Нове тут:

- `request.resolver_match.url_name` — ім'я маршруту поточної сторінки. `request` доступний у шаблонах завдяки context processor `request` у `settings.py` (ми його вже залишили в налаштуваннях).
- `{% with current=... %}` — коротке ім'я для довгого виразу.
- Умова `{% if current == 'home' %}class="active"{% endif %}` додає клас активному пункту меню.

Створіть `templates/includes/footer.html`:

```html
<footer class="site-footer">
    <div class="container">
        <p>Демо LMS · навчальний проєкт Django · {% now "Y" %}</p>
    </div>
</footer>
```

`{% now "Y" %}` виводить поточний рік.

Підключіть обидва фрагменти в `templates/base.html`, замінивши тимчасові `<header>` і `<footer>`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Демо LMS{% endblock %} | Демо LMS</title>
</head>
<body>
    {% include "includes/navbar.html" %}

    <main class="container">
        {% block content %}{% endblock %}
    </main>

    {% include "includes/footer.html" %}

</body>
</html>
```

### 4.5. Показати

Відкрийте `/`, натисніть «Курси». Меню однакове на всіх сторінках, а активний пункт змінюється (поки що без кольору, бо стилів немає, але в інструментах розробника (F12) видно `class="active"`).

```bash
git add . && git commit -m "Крок 4: головна, меню та підвал через include"
```

***

## Крок 5. Картки курсів: `include` з даними, фільтри, умови

**Мета:** замінити прості списки на картки, які використовуються і на головній, і в каталозі.

### 5.1. Шаблон картки

Картка повторюється в двох місцях, тому це ще один `include`. Створіть `courses/templates/courses/includes/course_card.html`:

```html
<article class="card" data-title="{{ course.title|lower }}">
    {% if course.is_new %}<span class="badge">Новий</span>{% endif %}
    <h3><a href="{% url 'course_detail' course.slug %}">{{ course.title }}</a></h3>
    <p class="muted">{{ course.level }} · {{ course.hours }} год · {{ course.lessons|length }} уроків</p>
    <p>{{ course.description|truncatechars:80 }}</p>
    <a class="btn" href="{% url 'course_detail' course.slug %}">Детальніше</a>
</article>
```

Включений шаблон бачить змінну `course` з циклу, у якому його викликано.

**Фільтри** змінюють вигляд значення під час виведення (самі дані не змінюються):

| Де в картці | Що робить |
| --- | --- |
| `{{ course.lessons\|length }}` | кількість уроків у списку |
| `{{ course.description\|truncatechars:80 }}` | обрізає опис до 80 символів (три крапки теж входять у ліміт) |
| `{{ course.title\|lower }}` | малі літери (використаємо для пошуку на кроці 10) |

**Умова** `{% if course.is_new %}…{% endif %}` показує значок «Новий» лише для нових курсів.

### 5.2. Використання

Замініть списки на картки в обох сторінках:

```html
{% extends "base.html" %}

{% block title %}Головна{% endblock %}

{% block content %}
<section class="hero">
    <h1>Вчимося разом</h1>
    <p>Легка демо-LMS: каталог курсів, уроки та особистий кабінет студента.</p>
    <p class="stats">Курсів: <strong>{{ courses_count }}</strong> · Уроків: <strong>{{ lessons_count }}</strong></p>
    <a class="btn" href="{% url 'course_list' %}">Переглянути курси</a>
</section>

<h2>Рекомендовані курси</h2>
<div class="grid">
    {% for course in featured %}
        {% include "courses/includes/course_card.html" %}
    {% empty %}
        <p>Курсів поки немає.</p>
    {% endfor %}
</div>
{% endblock %}
```

```html
{% extends "base.html" %}

{% block title %}Курси{% endblock %}

{% block content %}
<h1>Каталог курсів</h1>

<div class="grid">
    {% for course in courses %}
        {% include "courses/includes/course_card.html" %}
    {% empty %}
        <p>Курсів поки немає.</p>
    {% endfor %}
</div>
{% endblock %}
```

### 5.3. Показати

Відкрийте `/` і `/courses/`. Картки поки без оформлення: це нормально, стилі будуть на кроці 8. Перевірте, що:

- у курсу «QA: основи тестування» є слово «Новий»;
- опис обрізано трьома крапками;
- видно кількість уроків.

**Експерименти:** змініть `truncatechars:80` на `40`; у `data.py` поставте `is_new: True` для іншого курсу. Оновіть сторінку.

```bash
git add . && git commit -m "Крок 5: картки курсів"
```

***

## Крок 6. Уроки: умови і навігація «назад/далі»

**Мета:** окрема сторінка уроку з переходами між уроками.

### 6.1. View

```python
def lesson_detail(request, slug, number):
    course = get_course(slug)
    if course is None or not 1 <= number <= len(course["lessons"]):
        raise Http404("Урок не знайдено")
    context = {
        "course": course,
        "lesson": course["lessons"][number - 1],
        "number": number,
        "prev_number": number - 1 if number > 1 else None,
        "next_number": number + 1 if number < len(course["lessons"]) else None,
    }
    return render(request, "courses/lesson_detail.html", context)
```

Тут ми окремо обчислюємо `prev_number` і `next_number`, а в шаблоні просто перевіряємо, чи вони існують. Логіку краще залишати у view, а шаблон лишати простим.

### 6.2. Шаблон

`courses/templates/courses/lesson_detail.html`:

```html
{% extends "base.html" %}

{% block title %}{{ lesson.title }}{% endblock %}

{% block content %}
<p class="muted">
    <a href="{% url 'course_detail' course.slug %}">← {{ course.title }}</a>
</p>

<h1>Урок {{ number }}. {{ lesson.title }}</h1>
<p class="muted">Тривалість: {{ lesson.minutes }} хв</p>
<p>{{ lesson.summary }}</p>

<div class="pager">
    {% if prev_number %}
        <a href="{% url 'lesson_detail' course.slug prev_number %}">← Попередній урок</a>
    {% else %}
        <span></span>
    {% endif %}
    {% if next_number %}
        <a href="{% url 'lesson_detail' course.slug next_number %}">Наступний урок →</a>
    {% endif %}
</div>
{% endblock %}
```

### 6.3. URL

```python
from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("", views.home, name="home"),
    path("courses/<slug:slug>/lessons/<int:number>/", views.lesson_detail, name="lesson_detail"),
]
```

Тут два параметри: `<slug:slug>` і `<int:number>`. У шаблоні вони передаються у `{% url %}` у тому ж порядку: `{% url 'lesson_detail' course.slug prev_number %}`.

### 6.4. Посилання з програми курсу на уроки

У `course_detail.html` зробіть кожен урок посиланням. Номер уроку візьмемо з `forloop.counter` (лічильник циклу, починається з 1):

```html
{% extends "base.html" %}

{% block title %}{{ course.title }}{% endblock %}

{% block content %}
<p class="muted"><a href="{% url 'course_list' %}">← Усі курси</a></p>

<h1>{{ course.title }}</h1>
<p class="muted">Викладач: {{ course.teacher }} · Рівень: {{ course.level }} · {{ course.hours }} год</p>
<p>{{ course.description }}</p>

<h2>Програма курсу</h2>
<ol class="lessons">
    {% for lesson in course.lessons %}
    <li>
        <a href="{% url 'lesson_detail' course.slug forloop.counter %}">{{ lesson.title }}</a>
        <span class="muted">{{ lesson.minutes }} хв</span>
    </li>
    {% endfor %}
</ol>
{% endblock %}
```

### 6.5. Показати

1. `/courses/django-web/` → клік по першому уроку.
2. На уроці 1 немає «Попередній урок», на уроці 4 немає «Наступний урок».
3. `/courses/django-web/lessons/5/` → 404.

```bash
git add . && git commit -m "Крок 6: сторінка уроку"
```

***

## Крок 7. Кабінет студента: таблиця, `date`, `default`

**Мета:** сторінка з таблицею, у якій є дати й значення, що можуть бути порожніми.

### 7.1. View

Імпорти змінюються: додається `STUDENT`.

```python
from django.http import Http404
from django.shortcuts import render

from .data import COURSES, STUDENT, get_course


def dashboard(request):
    context = {"student": STUDENT, "courses": COURSES}
    return render(request, "courses/dashboard.html", context)
```

### 7.2. Шаблон

`courses/templates/courses/dashboard.html`:

```html
{% extends "base.html" %}

{% block title %}Мій кабінет{% endblock %}

{% block content %}
<h1>Вітаємо, {{ student.name }}!</h1>
<p class="muted">{{ student.email }} · Сьогодні: {% now "d.m.Y" %}</p>

<h2>Мої курси</h2>
<table>
    <thead>
        <tr><th>Курс</th><th>Прогрес</th><th>Дедлайн</th><th>Статус</th></tr>
    </thead>
    <tbody>
    {% for course in courses %}
        <tr>
            <td><a href="{% url 'course_detail' course.slug %}">{{ course.title }}</a></td>
            <td>
                <div class="bar"><span style="width: {{ course.progress }}%"></span></div>
                {{ course.progress }}%
            </td>
            <td>{{ course.deadline|date:"d.m.Y"|default:"—" }}</td>
            <td>{% if course.progress == 100 %}Завершено{% else %}У процесі{% endif %}</td>
        </tr>
    {% empty %}
        <tr><td colspan="4">Ви ще не записані на жоден курс.</td></tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}
```

Нове тут:

- `{{ course.deadline|date:"d.m.Y" }}` — формат дати: `20.11.2026`;
- `|default:"—"` — якщо значення порожнє (`None`), покажи тире (у курсу SQL дедлайну немає). Фільтри можна **ланцюжити**;
- `style="width: {{ course.progress }}%"` — змінну можна підставити в будь-яке місце HTML, зокрема в атрибут;
- `{% now "d.m.Y" %}` — сьогоднішня дата.

### 7.3. URL і меню

```python
from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("", views.home, name="home"),
    path("courses/<slug:slug>/lessons/<int:number>/", views.lesson_detail, name="lesson_detail"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
```

Додайте пункт «Мій кабінет» у `templates/includes/navbar.html`:

```html
{% with current=request.resolver_match.url_name %}
<header class="site-header">
    <div class="container header-inner">
        <a class="brand" href="{% url 'home' %}">
            <span>Демо LMS</span>
        </a>
        <nav>
            <a href="{% url 'home' %}" {% if current == 'home' %}class="active"{% endif %}>Головна</a>
            <a href="{% url 'course_list' %}"
               {% if current == 'course_list' or current == 'course_detail' or current == 'lesson_detail' %}class="active"{% endif %}>Курси</a>
            <a href="{% url 'dashboard' %}" {% if current == 'dashboard' %}class="active"{% endif %}>Мій кабінет</a>
        </nav>
    </div>
</header>
{% endwith %}
```

### 7.4. Показати

`/dashboard/`: таблиця з трьома курсами; дедлайни у форматі `20.11.2026`, у третього курсу замість дати «—». Прогрес поки виводиться лише числом, а смуга стане видимою з CSS.

> **Українські дати.** Для місяця словами використовуйте формат `E`: `{{ d|date:"j E Y" }}` → «15 березня 2026». Формат `F` дасть «15 Березень 2026».

```bash
git add . && git commit -m "Крок 7: кабінет студента"
```

***

## Крок 8. Статичні файли: CSS і логотип

**Мета:** нарешті зробити сайт гарним. Усі сторінки зміняться одночасно, бо вони всі спираються на `base.html`.

### 8.1. Що таке статика

Статичні файли — це файли, які сервер віддає «як є»: CSS, JavaScript, зображення, шрифти. Для них потрібно:

1. застосунок `django.contrib.staticfiles` в `INSTALLED_APPS` (є за замовчуванням);
2. `STATIC_URL` — префікс адреси, за яким файли доступні в браузері;
3. `STATICFILES_DIRS` — де файли лежать на диску;
4. у шаблоні: `{% load static %}` і `{% static 'шлях/файлу' %}`.

У `lms/settings.py` перевірте (або додайте):

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

Створіть структуру поруч із `manage.py`:

```text
static/
├── css/lms.css
├── js/lms.js            ← з'явиться на кроці 10
└── img/qa.png           ← логотип (візьміть із поточного проєкту)
```

| Варіант | Розташування | Коли |
| --- | --- | --- |
| Загальна папка проєкту | `static/css/lms.css` (поруч із `manage.py`) | спільні стилі, логотип, загальний JS |
| Папка застосунку | `courses/static/courses/css/courses.css` | файли, що належать одному застосунку; подвійна назва потрібна з тієї ж причини, що й у шаблонах |

### 8.2. CSS

`static/css/lms.css`:

```css
:root {
    --bg: #f5f6f8;
    --text: #1f2430;
    --muted: #6b7280;
    --brand: #2563eb;
    --dark: #222;
    --card: #fff;
    --line: #e5e7eb;
}

* { box-sizing: border-box; }

body {
    font-family: Arial, sans-serif;
    margin: 0;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
}

.container { max-width: 960px; margin: 0 auto; padding: 0 16px; }
main.container { padding-top: 24px; padding-bottom: 40px; min-height: 60vh; }

a { color: var(--brand); }
.muted { color: var(--muted); }

.site-header, .site-footer { background: var(--dark); color: #fff; padding: 14px 0; }
.header-inner { display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }
.brand { display: flex; align-items: center; gap: 10px; color: #fff; text-decoration: none; font-weight: bold; }
.site-header nav a { color: #cbd5e1; text-decoration: none; margin-left: 16px; padding-bottom: 4px; }
.site-header nav a.active, .site-header nav a:hover { color: #fff; border-bottom: 2px solid var(--brand); }
.site-footer { font-size: 14px; color: #cbd5e1; }
.site-footer p { margin: 0; }

.hero { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 32px; margin-bottom: 28px; }
.hero h1 { margin-top: 0; }

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
.card { position: relative; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 18px; }
.card h3 { margin: 0 0 6px; }
.card[hidden] { display: none; }
.badge { position: absolute; top: 12px; right: 12px; background: #16a34a; color: #fff; font-size: 12px; padding: 2px 8px; border-radius: 999px; }

.btn { display: inline-block; background: var(--brand); color: #fff; border: 0; border-radius: 8px; padding: 9px 16px; font-size: 15px; text-decoration: none; cursor: pointer; }
.btn.done { background: #16a34a; }

.search { display: flex; gap: 8px; margin-bottom: 16px; }
.search input { flex: 1; padding: 9px 12px; border: 1px solid var(--line); border-radius: 8px; font-size: 15px; }

.lessons li { padding: 8px 0; border-bottom: 1px solid var(--line); }
.lessons .muted { margin-left: 8px; font-size: 14px; }
.pager { display: flex; justify-content: space-between; margin-top: 28px; }

table { width: 100%; border-collapse: collapse; background: var(--card); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
th, td { text-align: left; padding: 10px 14px; border-bottom: 1px solid var(--line); }
th { background: #eef0f4; font-size: 14px; }
.bar { height: 8px; background: var(--line); border-radius: 999px; overflow: hidden; width: 140px; margin-bottom: 4px; }
.bar span { display: block; height: 100%; background: var(--brand); }
```

### 8.3. Підключення в шаблонах

У `base.html` додаються `{% load static %}` угорі та тег `<link>`:

```html
{% load static %}
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Демо LMS{% endblock %} | Демо LMS</title>
    <link rel="stylesheet" href="{% static 'css/lms.css' %}">
</head>
<body>
    {% include "includes/navbar.html" %}

    <main class="container">
        {% block content %}{% endblock %}
    </main>

    {% include "includes/footer.html" %}

</body>
</html>
```

Логотип підключається в меню. Оскільки `navbar.html` підключається через `include`, **`{% load static %}` потрібен і в ньому**: бібліотека тегів не успадковується.

```html
{% load static %}
{% with current=request.resolver_match.url_name %}
<header class="site-header">
    <div class="container header-inner">
        <a class="brand" href="{% url 'home' %}">
            <img src="{% static 'img/qa.png' %}" alt="Логотип" width="36" height="36">
            <span>Демо LMS</span>
        </a>
        <nav>
            <a href="{% url 'home' %}" {% if current == 'home' %}class="active"{% endif %}>Головна</a>
            <a href="{% url 'course_list' %}"
               {% if current == 'course_list' or current == 'course_detail' or current == 'lesson_detail' %}class="active"{% endif %}>Курси</a>
            <a href="{% url 'dashboard' %}" {% if current == 'dashboard' %}class="active"{% endif %}>Мій кабінет</a>
        </nav>
    </div>
</header>
{% endwith %}
```

### 8.4. Показати

Оновіть `/` (краще `Ctrl+F5`, щоб скинути кеш). Усі сторінки змінилися: темна шапка, картки, таблиця, прогрес-бар, підсвічений пункт меню.

Подивіться, як це працює:

1. Відкрийте інструменти розробника (F12) → вкладка Network → оновіть сторінку. Спершу іде запит за самою сторінкою, потім окремі запити за `lms.css` і `qa.png`.
2. У терміналі, де працює сервер, з'явилися рядки на кшталт `GET /static/css/lms.css 200`.
3. **Зламайте шлях:** у `base.html` напишіть `{% static 'css/lms2.css' %}`. Сторінка залишиться без стилів, а в терміналі буде `GET /static/css/lms2.css 404`. Це головний спосіб виявляти проблеми зі статикою: дивіться у термінал. Поверніть назад.

```bash
git add . && git commit -m "Крок 8: CSS та логотип"
```

***

## Крок 9. Пошук: дані з адреси (`request.GET`)

**Мета:** фільтрувати каталог за назвою, використовуючи параметр запиту `?q=…` (заняття 38).

### 9.1. View

Оновіть `course_list`:

```python
def course_list(request):
    query = request.GET.get("q", "").strip()
    courses = COURSES
    if query:
        courses = [c for c in COURSES if query.lower() in c["title"].lower()]
    context = {"courses": courses, "query": query}
    return render(request, "courses/course_list.html", context)
```

### 9.2. Шаблон

Додайте форму пошуку. Метод `get` додасть слова запиту в адресу:

```html
{% extends "base.html" %}

{% block title %}Курси{% endblock %}

{% block content %}
<h1>Каталог курсів</h1>

<form method="get" class="search">
    <input type="search" name="q" value="{{ query }}" placeholder="Пошук за назвою" id="course-search">
    <button class="btn" type="submit">Знайти</button>
</form>

{% if query %}
    <p class="muted">Результати за запитом «{{ query }}»: {{ courses|length }}</p>
{% endif %}

<div class="grid">
    {% for course in courses %}
        {% include "courses/includes/course_card.html" %}
    {% empty %}
        <p>Нічого не знайдено. <a href="{% url 'course_list' %}">Скинути пошук</a></p>
    {% endfor %}
</div>
{% endblock %}
```

`value="{{ query }}"` повертає введений текст у поле, щоб він не зникав після пошуку.

### 9.3. Показати

1. На `/courses/` введіть `sql` і натисніть «Знайти»: адреса стає `/courses/?q=sql`, у каталозі лишається один курс.
2. Введіть `zzz`: з'являється «Нічого не знайдено» (спрацював `{% empty %}`).
3. Вручну змініть адресу: `/courses/?q=django`.

```bash
git add . && git commit -m "Крок 9: пошук за назвою"
```

***

## Крок 10. JavaScript: інтерактивність

**Мета:** додати дві дрібні дії на стороні браузера: кнопку «Позначити пройденим» і миттєвий фільтр карток.

### 10.1. Розмітка

Для JavaScript нам потрібні «зачіпки» в HTML. Дві вже є з попередніх кроків: `id="course-search"` у пошуку (крок 9) та `data-title` у картці (крок 5). Додайте кнопку на сторінку уроку:

```html
{% extends "base.html" %}

{% block title %}{{ lesson.title }}{% endblock %}

{% block content %}
<p class="muted">
    <a href="{% url 'course_detail' course.slug %}">← {{ course.title }}</a>
</p>

<h1>Урок {{ number }}. {{ lesson.title }}</h1>
<p class="muted">Тривалість: {{ lesson.minutes }} хв</p>
<p>{{ lesson.summary }}</p>

<button class="btn" id="done-btn" data-key="{{ course.slug }}-{{ number }}">Позначити пройденим</button>

<div class="pager">
    {% if prev_number %}
        <a href="{% url 'lesson_detail' course.slug prev_number %}">← Попередній урок</a>
    {% else %}
        <span></span>
    {% endif %}
    {% if next_number %}
        <a href="{% url 'lesson_detail' course.slug next_number %}">Наступний урок →</a>
    {% endif %}
</div>
{% endblock %}
```

Атрибут `data-key` зберігає ідентифікатор уроку, за яким JavaScript запам'ятовує стан.

### 10.2. Скрипт

`static/js/lms.js`:

```javascript
document.addEventListener("DOMContentLoaded", function () {
    // 1. Кнопка «Позначити пройденим» (стан зберігаємо в браузері)
    var doneBtn = document.getElementById("done-btn");
    if (doneBtn) {
        var key = "lms-done-" + doneBtn.dataset.key;
        var render = function (isDone) {
            doneBtn.textContent = isDone ? "Пройдено ✓" : "Позначити пройденим";
            doneBtn.classList.toggle("done", isDone);
        };
        try { render(localStorage.getItem(key) === "1"); } catch (e) { render(false); }
        doneBtn.addEventListener("click", function () {
            var isDone = !doneBtn.classList.contains("done");
            try { localStorage.setItem(key, isDone ? "1" : "0"); } catch (e) { /* ігноруємо */ }
            render(isDone);
        });
    }

    // 2. Миттєвий фільтр карток курсів під час введення тексту
    var search = document.getElementById("course-search");
    if (search) {
        search.addEventListener("input", function () {
            var q = search.value.trim().toLowerCase();
            document.querySelectorAll(".card").forEach(function (card) {
                card.hidden = q !== "" && card.dataset.title.indexOf(q) === -1;
            });
        });
    }
});
```

### 10.3. Підключення

В кінці `<body>` у `base.html` додається скрипт. Атрибут `defer` каже браузеру спочатку показати сторінку, а потім виконати код.

```html
{% load static %}
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Демо LMS{% endblock %} | Демо LMS</title>
    <link rel="stylesheet" href="{% static 'css/lms.css' %}">
</head>
<body>
    {% include "includes/navbar.html" %}

    <main class="container">
        {% block content %}{% endblock %}
    </main>

    {% include "includes/footer.html" %}

    <script src="{% static 'js/lms.js' %}" defer></script>
</body>
</html>
```

### 10.4. Показати

1. Відкрийте урок, натисніть «Позначити пройденим»: кнопка зеленіє, текст змінюється. Оновіть сторінку: стан збережено (браузер запам'ятовує його в `localStorage`).
2. На `/courses/` починайте вводити текст у поле пошуку: картки зникають **без перезавантаження**. Це JavaScript, а не Django.
3. Відкрийте консоль (F12 → Console): помилок немає.

```bash
git add . && git commit -m "Крок 10: JavaScript"
```

***

## Крок 11. Власна сторінка 404

**Мета:** показувати помилку у стилі сайту.

Достатньо створити файл `templates/404.html`: Django сам використовує його, коли `DEBUG = False`. Реєструвати `handler404` для цього не потрібно (він знадобиться, лише якщо потрібна власна логіка у view, як на занятті 38).

```html
{% extends "base.html" %}

{% block title %}Сторінку не знайдено{% endblock %}

{% block content %}
<h1>404: такої сторінки немає</h1>
<p>Перевірте адресу або поверніться на головну.</p>
<a class="btn" href="{% url 'home' %}">На головну</a>
{% endblock %}
```

**Перевірка:**

1. У `settings.py` тимчасово встановіть `DEBUG = False` та `ALLOWED_HOSTS = ["127.0.0.1", "localhost"]`.
2. Запустіть: `python manage.py runserver --insecure` (прапорець змушує `runserver` віддавати статику й за `DEBUG = False`; без нього сторінка 404 буде без стилів).
3. Відкрийте `http://127.0.0.1:8000/nope/`.
4. **Поверніть** `DEBUG = True` та `ALLOWED_HOSTS = []`.

```bash
git add . && git commit -m "Крок 11: сторінка 404"
```

***

## Підсумкова перевірка: усе разом

```bash
python manage.py runserver
```

| Відкрийте | Очікуваний результат |
| --- | --- |
| `/` | «Вчимося разом», лічильники, дві картки; у меню активний пункт «Головна» |
| `/courses/` | Три картки; введення в пошук миттєво фільтрує їх; кнопка «Знайти» формує `?q=…` |
| `/courses/django-web/` | Опис курсу і чотири уроки-посилання; у меню активні «Курси» |
| `/courses/django-web/lessons/2/` | Урок із «назад/далі»; кнопка «пройдено» зберігає стан |
| `/courses/django-web/lessons/5/` | 404 |
| `/dashboard/` | Таблиця з прогрес-барами та датами; «—» там, де дедлайну немає |

***

## Довідник: теги та фільтри

### Теги

| Тег | Призначення |
| --- | --- |
| `{% if %}…{% elif %}…{% else %}…{% endif %}` | умова |
| `{% for x in list %}…{% empty %}…{% endfor %}` | цикл; `empty` спрацьовує, якщо список порожній |
| `{% url 'name' arg1 arg2 %}` | адреса за ім'ям маршруту; аргументи в порядку з `path()` |
| `{% extends "base.html" %}` | успадкування (завжди першим тегом) |
| `{% block name %}…{% endblock %}` | змінювана частина шаблону; `{{ block.super }}` додає вміст батьківського блока |
| `{% include "file.html" %}` | вставити фрагмент; `with x=y` передає змінні |
| `{% load static %}` | підключити бібліотеку для `{% static %}` (у кожному файлі окремо) |
| `{% with x=a.b.c %}…{% endwith %}` | коротке ім'я для довгого виразу |
| `{% now "Y" %}` | поточна дата/час у заданому форматі |

Усередині циклу доступні `forloop.counter` (з 1), `forloop.counter0` (з 0), `forloop.first`, `forloop.last`.

### Фільтри

| Фільтр | Що робить | Приклад → результат |
| --- | --- | --- |
| `upper`, `lower`, `title` | регістр | `{{ "hello world"\|title }}` → `Hello World` |
| `length` | кількість елементів чи символів | `{{ items\|length }}` → `3` |
| `slice` | зріз, як у Python | `{{ "Hello World"\|slice:":5" }}` → `Hello` |
| `truncatechars` | обрізає текст | `{{ text\|truncatechars:10 }}` → `Маршрутиз…` |
| `join` | з'єднує список | `{{ tags\|join:", " }}` → `a, b` |
| `default` | значення, якщо вихідне «порожнє» (`None`, `""`, `0`, `[]`) | `{{ x\|default:"—" }}` |
| `yesno` | булеве значення → текст | `{{ flag\|yesno:"Так,Ні" }}` → `Так` |
| `date` | форматує дату | `{{ d\|date:"d.m.Y" }}` → `15.03.2026` |
| `safe` | вимикає екранування (небезпечно!) | `{{ html\|safe }}` |

> **Безпека.** Усе, що виводиться через `{{ }}`, Django автоматично екранує: `<` стає `&lt;`. Це захищає від XSS-атак. Фільтр `|safe` вимикає захист, тому **ніколи не застосовуйте його до тексту, який ввів користувач.**
>
> Вбудований `pluralize` розрахований на англійську і не вміє три форми української («1 урок, 2 уроки, 5 уроків»), тому в демо ми пишемо «уроків: N».

***

## Типові помилки

| Симптом | Причина | Що робити |
| --- | --- | --- |
| `TemplateDoesNotExist: courses/home.html` | неправильний шлях, немає папки `courses/` усередині `templates/`, застосунок не в `INSTALLED_APPS` | звірте шлях із блоком Template-loader postmortem на сторінці помилки |
| `Invalid block tag on line 5: 'static'. Did you forget to register or load this tag?` | немає `{% load static %}` у цьому файлі | додайте `{% load static %}` угорі файлу (у дочірньому шаблоні після `extends`) |
| `{% extends 'base.html' %} must be the first tag in the template` | перед `extends` стоїть інший тег (наприклад, `load`) | `extends` завжди першим |
| `Unclosed tag on line 7: 'for'. Looking for one of: empty, endfor.` | забули закрити тег | додайте `{% endfor %}` / `{% endif %}` / `{% endblock %}` |
| `NoReverseMatch: Reverse for 'course_detail' with no arguments not found` | `{% url %}` без обов'язкового параметра або з неправильним ім'ям | перевірте `name=` у `urls.py` і кількість аргументів |
| На сторінці немає даних, помилки немає | опечатка в імені змінної: Django підставляє порожній рядок | порівняйте ім'я в шаблоні з ключем у контексті |
| Сторінка без стилів, у терміналі `GET /static/css/lms.css 404` | неправильний шлях у `{% static %}` або файл лежить не там | перевірте, що файл існує за шляхом `static/css/lms.css`, і що є `STATICFILES_DIRS` |
| Стилі змінено, а на сторінці все по-старому | кеш браузера | `Ctrl+F5` |
| 404 без стилів при `DEBUG = False` | `runserver` не роздає статику | запускайте з `--insecure` (лише для навчання) |

На справжньому сервері статику збирає `collectstatic` (потрібен `STATIC_ROOT`), а віддає веб-сервер, а не Django. На заняттях до цього не доходимо.

***

## Самоперевірка

1. Яка послідовність дій потрібна для нової сторінки? (Назвіть п'ять частин ритму заняття.)
2. Чим відрізняються `{{ ... }}` і `{% ... %}`?
3. Що побачить користувач, якщо в шаблоні написати `{{ titel }}` замість `{{ title }}`?
4. Для чого потрібні `{% extends %}` і `{% block %}`? А `{% include %}`?
5. Чому `{% load static %}` треба писати і в `base.html`, і в `navbar.html`?
6. Чому `{% url 'course_list' %}` краще, ніж `<a href="/courses/">`?
7. Що станеться з кодом `<script>alert(1)</script>`, який користувач ввів у поле, якщо вивести його через `{{ text }}`? А через `{{ text|safe }}`?
8. Сторінка відкрилася без стилів. Де знайти причину?

**Відповіді**

1. Дані → view → шаблон → url → перевірка в браузері.
2. `{{ }}` виводить значення змінної, `{% %}` виконує логіку (цикл, умову, підключення).
3. Нічого: Django не видасть помилки, а підставить порожній рядок.
4. `extends` вказує базовий шаблон, `block` позначає місця, які дочірній шаблон може замінити. `include` вставляє готовий фрагмент в одне місце сторінки.
5. Бібліотека тегів підключається окремо для кожного шаблону. `include` не наслідує `load` із батьківського файлу.
6. Адреса береться за ім'ям маршруту; якщо змінити шлях у `urls.py`, посилання оновляться автоматично.
7. Через `{{ text }}` код буде екрановано і показано як звичайний текст. Через `|safe` скрипт виконається в браузері, тобто це вразливість (XSS).
8. У терміналі, де працює сервер: рядок `GET /static/... 404` вкаже, який файл не знайдено. Також у F12 → Network.

***

## Домашнє завдання

Повторіть **той самий ритм і ті самі кроки** на своєму навчальному проєкті (Task & Bug Manager, Expense Tracker або Service Management System). Дані беріть зі словників або списків у Python. Після кожного кроку робіть коміт.

1. **Дані + список:** файл з даними, view, шаблон і URL списку ваших сутностей (задачі / витрати / заявки), цикл із `{% empty %}`.
2. **Деталі:** сторінка однієї сутності за `<int:pk>`, якщо запису немає, `Http404`. Посилання зі списку через `{% url %}`.
3. **База:** `templates/base.html` з блоками `title` та `content`, обидві сторінки успадковують його.
4. **Include:** меню та підвал у `templates/includes/`, активний пункт меню.
5. **Фільтри:** використайте щонайменше два різні фільтри (наприклад, `date`, `default`, `truncatechars`, `length`).
6. **Статика:** свій CSS (`static/css/…`) та зображення.
7. **JavaScript:** одна дія (кнопка, фільтр, показ/приховування блока).
8. **404:** `templates/404.html`, перевірити при `DEBUG = False`.
9. **За бажанням:** винесіть картку сутності в `include` і використовуйте її в двох місцях.

У README коротко опишіть, які адреси доступні і як запустити проєкт.

***

## Підсумок

- Нову сторінку завжди будуємо за ритмом: **дані → view → шаблон → url → показати**. Рухаємося маленькими кроками й комітимо кожен робочий стан.
- Шаблон показує дані, а не обчислює їх: логіка залишається у `views.py`.
- `base.html` задає каркас, дочірні шаблони заповнюють блоки, `include` прибирає дублювання.
- Посилання будуємо через `{% url %}`, статику підключаємо через `{% static %}`; `{% load static %}` пишемо в кожному файлі, де він потрібен, а `{% extends %}` ставимо першим тегом.
- Якщо щось пішло не так: читаємо останній рядок помилки, дивимося у термінал із сервером і змінюємо одну річ за раз.

Далі нас чекають **моделі та ORM**: замість `courses/data.py` дані будуть у справжній базі даних, а шаблони залишаться майже без змін.
