Так, ось **повний текст до Заняття 39** у форматі, який можна використати як конспект або методичний матеріал.

## Заняття 39. Шаблони та статичні файли

### Тема заняття
Шаблони Django, рендеринг HTML, контекст шаблонів, змінні, теги та фільтри, успадкування шаблонів. Статичні файли: CSS, JavaScript, зображення.

### Мета заняття
Сформувати в учасників розуміння того, як Django генерує HTML-сторінки за допомогою шаблонів, як передавати дані з представлень у шаблони, як використовувати змінні, теги та фільтри, а також як підключати статичні файли для оформлення та інтерактивності веб-застосунку.

### Теоретична частина

#### 1. Що таке шаблони Django
Шаблон у Django — це HTML-файл, який може містити спеціальні конструкції Django Template Language. Завдяки ним сторінка стає динамічною: у шаблон можна підставляти дані, виконувати просту логіку відображення, використовувати повторювані блоки та будувати структуру сайту без дублювання коду.

У класичному HTML сторінка статична, а в Django шаблон заповнюється даними під час обробки запиту. Саме тому один і той самий шаблон може показувати різний вміст залежно від контексту, який передав view.

#### 2. Рендеринг HTML
Рендеринг — це процес перетворення шаблону в готову HTML-сторінку. Django бере шаблон, підставляє в нього значення змінних із контексту, обробляє теги та фільтри, після чого повертає користувачу готовий результат у вигляді HTML.

На практиці це виглядає так: view формує дані, передає їх у шаблон, а шаблон відображає їх у зручному для браузера вигляді. Саме так будується більшість сторінок Django-застосунку.

#### 3. Контекст шаблону
Контекст шаблону — це словник даних, який передається з Python-коду в HTML-шаблон. У ньому можуть бути текст, числа, списки, словники, дати, об’єкти моделей або будь-які інші значення, які потрібно відобразити на сторінці.

Наприклад, якщо у view передати список товарів, то в шаблоні можна вивести кожен товар у циклі. Якщо передати ім’я користувача, його можна показати у заголовку сторінки або в привітальному блоці.

#### 4. Змінні у шаблонах
Змінні в Django-шаблонах записуються через подвійні фігурні дужки. Django підставляє значення змінної під час рендерингу сторінки.

Приклад:
```html
<h1>Привіт, {{ user_name }}!</h1>
<p>Сьогодні: {{ current_date }}</p>
```

Якщо у контексті `user_name = "Олена"`, то на сторінці відобразиться: `Привіт, Олена!`.

#### 5. Теги шаблонів
Теги Django використовуються для керування логікою шаблону. Вони дозволяють створювати цикли, умови, підключати інші шаблони, оголошувати блоки для успадкування та виконувати інші дії, пов’язані зі структурою сторінки.

Найчастіше використовують:
- `if` — для умовного відображення;
- `for` — для циклів;
- `block` — для оголошення змінних частин шаблону;
- `extends` — для успадкування;
- `include` — для вставки інших шаблонів.

Приклад:
```html
{% if user.is_authenticated %}
  <p>Вітаємо, {{ user.username }}!</p>
{% else %}
  <p>Будь ласка, увійдіть у систему.</p>
{% endif %}
```

#### 6. Фільтри шаблонів
Фільтри змінюють вигляд значення під час виведення. Вони не змінюють самі дані в Python, а лише форматують їх у шаблоні.

Приклади фільтрів:
- `upper` — перетворює текст у верхній регістр;
- `lower` — у нижній регістр;
- `title` — робить кожне слово з великої літери;
- `length` — повертає довжину;
- `date` — форматування дати;
- `default` — значення за замовчуванням.

Приклад:
```html
<p>{{ product_name|upper }}</p>
<p>{{ items|length }}</p>
```

#### 7. Успадкування шаблонів
Успадкування шаблонів — це механізм, який дозволяє створити базовий шаблон із загальною структурою сайту, а потім у дочірніх шаблонах перевизначати лише окремі блоки. Це зменшує дублювання коду та спрощує підтримку проєкту.

Зазвичай базовий шаблон містить:
- шапку сайту;
- меню навігації;
- основний блок контенту;
- підвал сайту.

Приклад базового шаблону:
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Мій сайт{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Логотип сайту</h1>
        <nav>Меню</nav>
    </header>

    <main>
        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <p>© 2026 Мій сайт</p>
    </footer>
</body>
</html>
```

Дочірній шаблон:
```html
<!-- home.html -->
{% extends 'base.html' %}

{% block title %}Головна сторінка{% endblock %}

{% block content %}
  <h2>Ласкаво просимо!</h2>
  <p>Це головна сторінка сайту.</p>
{% endblock %}
```

#### 8. Статичні файли
Статичні файли — це файли, які не генеруються сервером динамічно. До них належать CSS, JavaScript, зображення, іконки, шрифти та інші ресурси для оформлення сайту.

У Django для статичних файлів зазвичай використовують окрему папку, а в шаблонах підключають їх через спеціальний тег роботи зі static-ресурсами.

Типова структура може виглядати так:
```text
project/
├── app/
│   ├── templates/
│   │   └── home.html
│   └── static/
│       └── app/
│           ├── css/
│           │   └── style.css
│           ├── js/
│           │   └── script.js
│           └── img/
│               └── logo.png
```

Підключення CSS у шаблоні:
```html
{% load static %}
<link rel="stylesheet" href="{% static 'app/css/style.css' %}">
```

Підключення JavaScript:
```html
{% load static %}
<script src="{% static 'app/js/script.js' %}"></script>
```

Підключення зображення:
```html
{% load static %}
<img src="{% static 'app/img/logo.png' %}" alt="Логотип">
```

***

### Практична частина

#### 1. Створення базового шаблону сайту
На практиці учасники створюють базовий шаблон `base.html`, який містить усі спільні елементи сторінок: header, navigation, footer і блок для основного контенту. Це дозволяє будувати сторінки за єдиним стандартом і не копіювати однаковий HTML у кожному файлі.

#### 2. Підключення CSS
Після створення базової структури проєкту учасники додають CSS-файл. У ньому описуються стилі для тексту, кнопок, відступів, меню, фону та інших елементів інтерфейсу. Це дає змогу зробити сторінку візуально привабливою та зручною для користувача.

Приклад CSS:
```css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    background-color: #f5f5f5;
}

header, footer {
    background-color: #222;
    color: white;
    padding: 20px;
}

main {
    padding: 20px;
}
```

#### 3. Підключення JavaScript
JavaScript додають для інтерактивності: обробки кліків, показу повідомлень, зміни вмісту сторінки без перезавантаження, перевірки форм або інших дій на стороні браузера.

Приклад:
```javascript
document.addEventListener("DOMContentLoaded", function () {
    console.log("Сторінка завантажена");
});
```

#### 4. Формування інтерфейсу застосунку
Наприкінці заняття учасники збирають цілісний інтерфейс застосунку: оформлюють головну сторінку, створюють блоки контенту, підключають стилі та скрипти, перевіряють роботу шаблонів і статичних ресурсів. Це є основою для подальшої розробки більш складного функціоналу Django-застосунку.

### Приклад мінімального комплекту файлів

```html
<!-- base.html -->
{% load static %}
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Мій сайт{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'app/css/style.css' %}">
</head>
<body>
    <header>
        <h1>Мій сайт</h1>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>© 2026</p>
    </footer>

    <script src="{% static 'app/js/script.js' %}"></script>
</body>
</html>
```

```html
<!-- home.html -->
{% extends 'base.html' %}

{% block title %}Головна{% endblock %}

{% block content %}
  <h2>Головна сторінка</h2>
  <p>Це приклад сторінки з успадкуванням шаблону.</p>
{% endblock %}
```

#### 9. Конфігурація шаблонів у settings.py

Важливо знати, **де Django шукає шаблони**. Це налаштовується в файлі `settings.py` у секції `TEMPLATES`:

```python
# settings.py

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],          # Загальні шаблони проєкту
        "APP_DIRS": True,                          # Шукати templates у папках застосунків
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    },
]
```

**Отримується така структура:**
```
project/
    templates/              # Загальні шаблони (рівень проєкту)
        base.html
        
    blog/
        templates/
            blog/           # Шаблони застосунку (шаблон в папці застосунку)
                index.html
                detail.html
```

**Чому назва папки повторюється?** Якщо просто написати `blog/templates/index.html`, то при двох застосунках може виникнути конфлікт (обидва матимуть `templates/index.html`). Тому прийнято розміщувати: `blog/templates/blog/index.html` — це запобігає дублюванню.

#### 10. Представлення (views) та рендеринг

Одиниця фундаменту Django-застосунку — це **цикл "URL → View → Template → HTML"**:

```
URL запит
    ↓
View оброблює запит
    ↓
Передає контекст у render()
    ↓
Template отримує дані
    ↓
Браузер отримує готовий HTML
```

Приклад:

```python
# views.py
from django.shortcuts import render
from .models import BlogPost

def blog_list(request):
    # 1. Отримуємо дані
    posts = BlogPost.objects.all()
    
    # 2. Готуємо контекст
    context = {
        "title": "Мій блог",
        "posts": posts,
        "author": "Олександр"
    }
    
    # 3. Передаємо у шаблон
    return render(request, "blog/index.html", context)
```

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog-list"),
]
```

#### 11. Робота зі списками та циклами

Часто потрібно вивести список елементів. Використовується тег `{% for %}`:

```html
<!-- posts.html -->
<ul>
{% for post in posts %}
    <li>
        <strong>{{ post.title }}</strong>
        <p>{{ post.description }}</p>
        <small>Автор: {{ post.author }}</small>
    </li>
{% empty %}
    <li>Поки дописів немає. Додайте перший!</li>
{% endfor %}
</ul>
```

Блок `{% empty %}` спрацьовує, якщо список порожній. Це дуже часто використовується в реальних застосунках.

#### 12. Вкладені об'єкти та доступ до атрибутів

Якщо передаємо об'єкт із ORM, шаблон може звертатися до його атрибутів через точку:

```html
<!-- detail.html -->
<h1>{{ post.title }}</h1>
<p>Автор: {{ post.author.full_name }}</p>
<p>Дата: {{ post.created_at }}</p>

<!-- Доступ до методів -->
<p>{{ post.get_status_display }}</p>
```

Це працює для:
- Звичайних атрибутів: `{{ post.title }}`
- Вкладених об'єктів: `{{ post.author.email }}`
- Методів (без дужок): `{{ post.get_status_display }}`
- Списків за індексом: `{{ posts.0.title }}`

#### 13. Розширена робота з фільтрами

Фільтри — це функції, які форматують дані при виведенні. Ось найчастіше використовувані:

| Фільтр | Чим робить | Приклад |
|--------|-----------|---------|
| `upper` | Перетворює в ВЕРХНІЙ РЕГІСТР | `{{ title\|upper }}` → "HELLO WORLD" |
| `lower` | Нижній регістр | `{{ title\|lower }}` → "hello world" |
| `title` | Кожне слово з великої | `{{ title\|title }}` → "Hello World" |
| `length` | Кількість символів / елементів | `{{ items\|length }}` → 5 |
| `slice` | Зріз (як у Python) | `{{ title\|slice:":5" }}` → "Hello" |
| `truncatechars` | Скорочує текст | `{{ post\|truncatechars:50 }}` → "Lorem ipsum dolor..." |
| `date` | Форматує дату | `{{ post.created_at\|date:"d.m.Y" }}` → "15.03.2026" |
| `join` | З'єднує список | `{{ tags\|join:", " }}` → "python, django, web" |
| `default` | Значення за замовчуванням | `{{ user.bio\|default:"Біографія не вказана" }}` |
| `safe` | Виводить HTML (обережно!) | `{{ content\|safe }}` |
| `yesno` | Закодує булів | `{{ is_active\|yesno:"Так,Ні" }}` → "Так" або "Ні" |

Приклад:

```html
<h1>{{ article.title|upper }}</h1>
<p>{{ article.text|truncatechars:100 }}</p>
<small>{{ article.created_at|date:"j F Y" }}</small>

{% if tags %}
    <p>Теги: {{ tags|join:", " }}</p>
{% else %}
    <p>{{ "Тегів немає"|default:"Тегів немає" }}</p>
{% endif %}
```

#### 14. Тег `{% url %}` — найважливіший!

Замість жорсткого написання URL-адреси, використовуйте тег `{% url %}`. Це дозволяє змінювати адреси в `urls.py` без пошуку в шаблонах:

```html
<!-- Погано: жорсткої посилання -->
<a href="/blog/posts/">Всі дописи</a>

<!-- Добре: динамічне посилання -->
<a href="{% url 'blog-list' %}">Всі дописи</a>

<!-- Ще краще: з параметрами -->
<a href="{% url 'blog-detail' post.id %}">Читати далі</a>

<!-- З декількома параметрами -->
<a href="{% url 'post-comment' post.id comment.id %}">Перейти до коментаря</a>
```

**Як це працює:**
```python
# urls.py
urlpatterns = [
    path("posts/", views.blog_list, name="blog-list"),
    path("posts/<int:post_id>/", views.blog_detail, name="blog-detail"),
]
```

Якщо потім змінити URL на `path("articles/", ...)`, всі посилання в шаблонах оновляться автоматично!

#### 15. Тег `{% include %}` для повторного використання

Замість копіювання однакового HTML, використовуйте `{% include %}`:

```
templates/
    includes/
        header.html
        footer.html
        sidebar.html
        card.html
```

```html
<!-- base.html -->
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% include "includes/header.html" %}
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    {% include "includes/sidebar.html" %}
    {% include "includes/footer.html" %}
</body>
</html>
```

```html
<!-- includes/header.html -->
<header>
    <h1>Мій сайт</h1>
    <nav>
        <a href="{% url 'home' %}">Головна</a>
        <a href="{% url 'blog-list' %}">Блог</a>
        <a href="{% url 'about' %}">Про нас</a>
    </nav>
</header>
```

Можна передавати контекст прямо у `include`:

```html
{% include "card.html" with item=post %}
```

#### 16. Статичні файли: налаштування та структура

Статичні файли розташовуються у папці `static`. Потрібно налаштувати `settings.py`:

```python
# settings.py

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"  # Для production
```

Типова структура:

```
project/
    static/                    # Статичні файли рівня проєкту
        css/
            style.css
        js/
            main.js
        img/
            logo.png
    
    blog/
        static/
            blog/              # Назва папки повторюється!
                css/
                    blog.css
                js/
                    blog.js
```

Підключення у шаблоні:

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <link rel="stylesheet" href="{% static 'blog/css/blog.css' %}">
</head>
<body>
    <img src="{% static 'img/logo.png' %}" alt="Логотип">
    
    <script src="{% static 'js/main.js' %}"></script>
    <script src="{% static 'blog/js/blog.js' %}"></script>
</body>
</html>
```

#### 17. Використання CDN для фреймворків (Bootstrap, FontAwesome)

Більшість сайтів використовують готові CSS-фреймворки замість написання всього з нуля:

```html
<!-- Підключення Bootstrap через CDN -->
<link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    rel="stylesheet">

<script
    src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<!-- Тепер можна використовувати класи Bootstrap -->
<button class="btn btn-primary">Натисни мене</button>
<div class="alert alert-success">Успіх!</div>
```

#### 18. Контекстні процесори (опціонально, основи)

Деякі дані потрібно передавати в кожен шаблон автоматично (наприклад, поточний користувач). Для цього існують контекстні процесори:

```python
# settings.py
TEMPLATES = [
    {
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",  # Додає {{ user }}
                "django.template.context_processors.request",    # Додає {{ request }}
            ],
        },
    },
]
```

Тепер у кожному шаблоні автоматично доступні `{{ user }}` та `{{ request }}`:

```html
{% if user.is_authenticated %}
    <p>Привіт, {{ user.username }}!</p>
{% else %}
    <p><a href="{% url 'login' %}">Увійти</a></p>
{% endif %}
```


### Домашнє завдання
1. Створити базовий шаблон `base.html` для Django-застосунку.
2. Створити дочірній шаблон головної сторінки.
3. Передати в шаблон 2–3 змінні через контекст і вивести їх на сторінці.
4. Підключити CSS-файл для оформлення сторінки.
5. Підключити JavaScript-файл і додати просту дію, наприклад повідомлення в консолі або зміну тексту на сторінці.
6. Додати зображення в інтерфейс через статичні файли.

### Очікуваний результат
Після виконання заняття учасник повинен уміти:
- створювати шаблони Django;
- використовувати змінні, теги та фільтри;
- будувати шаблони з успадкуванням;
- підключати статичні файли;
- формувати базову структуру інтерфейсу веб-застосунку.
