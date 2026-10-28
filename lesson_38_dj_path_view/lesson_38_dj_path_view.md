# Заняття 38. Маршрутизація та представлення (Path, Views)

## Мета заняття

На цьому занятті ми навчимося будувати сторінки Django-застосунку: налаштовувати URL-маршрути, створювати представлення, передавати дані в шаблони та розуміти, як запит проходить через Django до відповіді користувачу.

Після заняття ви зможете:

- налаштовувати URL-маршрути в Django за допомогою `path()` та `include()`;
- відрізняти параметри шляху (`/posts/5/`) від параметрів запиту (`?page=2`);
- пояснювати, що таке `HttpRequest` і `HttpResponse`;
- писати функціональні представлення (views);
- передавати контекст у шаблони через `render()` та правильно розташовувати шаблони;
- повертати помилку 404 і налаштовувати власну сторінку помилки;
- пояснити, що таке middleware і де воно стоїть у ланцюжку обробки запиту;
- читати типові помилки Django і знаходити їхню причину.

***

## Карта заняття: як Django обробляє запит

Спершу подивіться на весь шлях запиту. Далі в конспекті ми розберемо кожну ланку окремо.

```text
Браузер: GET /posts/2/
   │
   ▼
Middleware (зверху вниз: сесії, безпека, наше логування…)
   │
   ▼
Головний urls.py ──include──► urls.py застосунку
   │   шукає перший маршрут, що підійшов: posts/<int:post_id>/
   ▼
View: post_detail(request, post_id=2)
   │   отримує дані, формує контекст
   ▼
render(request, "core/post.html", context)  ──► HTML
   │
   ▼
Middleware (знизу вгору)
   │
   ▼
Браузер отримує HTTP-відповідь (статус 200 + HTML)
```

Ключова ідея: **`urls.py` відповідає на питання «за якою адресою?», а `views.py` — «що показати?».**

***

## URL-маршрутизація

URL-маршрутизація визначає, яке представлення Django має виконати для конкретної адреси в браузері. Коли користувач відкриває сторінку, Django перебирає список маршрутів `urlpatterns` зверху вниз і викликає view першого маршруту, що збігся.

Наприклад:

- `/` — головна сторінка;
- `/about/` — сторінка «Про нас»;
- `/contacts/` — сторінка контактів;
- `/posts/1/` — сторінка конкретного запису.

Маршрутизація — це міст між адресою сторінки та логікою, яка має спрацювати. Якщо жоден маршрут не підійшов, Django повертає помилку 404.

***

## `path()`

`path()` — це основний спосіб описати маршрут у Django. Він зв'язує URL із view-функцією або view-класом.

### Приклад

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
]
```

### Що тут відбувається

- `""` означає головну сторінку;
- `"about/"` — сторінка `/about/`;
- `views.home` і `views.about` — функції, які обробляють запит (їх передаємо **без дужок**: Django викличе їх сам);
- `name="home"` і `name="about"` — імена маршрутів. Їх використовують у шаблонах (`{% url 'home' %}`) і в коді (`reverse("home")`), щоб не прописувати адреси вручну.

### Правила запису шляху

- Шлях **не починається зі слеша**: `"about/"`, а не `"/about/"` (Django попередить про це під час `check`).
- За домовленістю шлях **закінчується слешем**: `"about/"`. Якщо користувач відкриє `/about` без слеша, `CommonMiddleware` (параметр `APPEND_SLASH`) перенаправить його на `/about/`. Навпаки не працює: для маршруту `"about"` адреса `/about/` дасть 404.

### Маршрут із параметром

```python
path("posts/<int:post_id>/", views.post_detail, name="post_detail")
```

Тут `post_id` передається у view як число (`int`). Запит `/posts/5/` викличе `post_detail(request, post_id=5)`, а `/posts/abc/` взагалі не збігається з маршрутом, тому Django віддасть 404 ще до виклику view.

### Типи параметрів (конвертери)

| Конвертер | Що приймає | Приклад значення | Тип у view |
| --- | --- | --- | --- |
| `<int:id>` | ціле число ≥ 0 | `7` | `int` |
| `<str:username>` | будь-який непорожній рядок **без слеша** | `user123` | `str` |
| `<slug:article>` | латиниця, цифри, дефіс, підкреслення | `my-article` | `str` |
| `<uuid:file_id>` | UUID у нижньому регістрі | `075194d3-6885-417e-a8a8-6c931e272f00` | `uuid.UUID` |
| `<path:subpath>` | рядок **зі слешами** | `docs/2026/report.pdf` | `str` |

Якщо конвертер не вказати (`<post_id>`), Django використає `str`. Це не помилка синтаксису, але `post_id` стане рядком `"5"`, а не числом, і підходитиме будь-який текст.

### Приклади маршрутів

```python
path("users/<str:username>/", views.user_profile, name="user_profile")
path("articles/<slug:article>/", views.article_detail, name="article_detail")
path("files/<uuid:file_id>/", views.download_file, name="download_file")
path("posts/<int:post_id>/", views.post_detail, name="post_detail")
```

У view ці параметри передаються як іменовані аргументи функції. **Імена аргументів мають збігатися з іменами в маршруті.**

```python
def user_profile(request, username):
    return render(request, "core/profile.html", {"username": username})

def article_detail(request, article):
    return render(request, "core/article.html", {"slug": article})

def download_file(request, file_id):
    return render(request, "core/download.html", {"file_id": file_id})

def post_detail(request, post_id):
    return render(request, "core/post.html", {"post_id": post_id})
```

### Параметри шляху і параметри запиту

Не плутайте два способи передати дані в адресі:

| | Параметр шляху | Параметр запиту |
| --- | --- | --- |
| Вигляд | `/posts/5/` | `/posts/?page=2&sort=new` |
| Де описується | у `path()`: `<int:post_id>` | ніде, читається з `request.GET` |
| Як отримати у view | аргумент функції | `request.GET.get("page")` |
| Для чого | ідентифікує ресурс | фільтри, сортування, пошук |

```python
def search(request):
    query = request.GET.get("q", "")       # /search/?q=django
    return render(request, "core/search.html", {"query": query})
```

***

## `include()`

`include()` використовується для підключення маршрутів іншого файлу. Це дозволяє розділити маршрутизацію за застосунками: кожен застосунок має свій `urls.py`.

### Основний `urls.py` (папка проєкту)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
```

### `core/urls.py` (застосунок)

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
]
```

Префікс із головного `urls.py` додається до кожного маршруту застосунку. Якщо підключити так:

```python
path("blog/", include("core.urls")),
```

то сторінка `about/` стане доступною за адресою `/blog/about/`, і **код самого застосунку змінювати не треба**. Це і є причина розділяти маршрути: застосунок не знає, під яким префіксом його підключено.

> Коли в проєкті кілька застосунків із однаковими іменами маршрутів (наприклад, `home`), додають у `core/urls.py` рядок `app_name = "core"` і звертаються так: `{% url 'core:home' %}`. На цьому занятті достатньо простого варіанта без `app_name`.

***

## Представлення (Views)

View — це частина Django, яка приймає HTTP-запит і повертає HTTP-відповідь. У простому випадку view є звичайною функцією.

### Основна роль view

- отримати запит;
- виконати потрібну логіку;
- звернутися до бази даних або сформувати дані;
- повернути користувачу відповідь.

***

## `HttpRequest`

`HttpRequest` — це об'єкт, який Django створює для кожного запиту й передає першим аргументом у view. У ньому міститься інформація про метод запиту, URL, заголовки, параметри, користувача та інші дані.

### Що можна знайти в `request`

| Атрибут | Що містить |
| --- | --- |
| `request.method` | HTTP-метод: `"GET"`, `"POST"` тощо |
| `request.path` | шлях без домену і параметрів: `/about/` |
| `request.GET` | параметри запиту з адреси (`?q=django`) |
| `request.POST` | дані форми, надіслані методом POST |
| `request.user` | поточний користувач (потрібне middleware автентифікації) |
| `request.headers` | заголовки запиту |

### Приклад

```python
from django.http import HttpResponse

def home(request):
    print(request.method, request.path)   # з'явиться в терміналі, де запущено сервер
    return HttpResponse("Hello")
```

***

## `HttpResponse`

`HttpResponse` — це об'єкт відповіді, який Django повертає браузеру. Через нього можна віддати текст, HTML або інший вміст і вказати статус-код.

### Приклад

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!")
```

### HTML-відповідь

```python
def home(request):
    return HttpResponse("<h1>Hello, Django!</h1>")
```

### Статус-код

```python
return HttpResponse("Не знайдено", status=404)
```

У реальних проєктах частіше використовують `render()`, а не чистий `HttpResponse` з HTML усередині рядка.

### Найчастіші статус-коди

| Код | Значення |
| --- | --- |
| `200` | все гаразд |
| `302` | перенаправлення на іншу адресу |
| `400` | некоректний запит |
| `403` | доступ заборонено |
| `404` | сторінку не знайдено |
| `500` | внутрішня помилка сервера (помилка в нашому коді) |

***

## Функціональні представлення

Функціональне представлення — це view, написане як звичайна функція Python. Вона **першим аргументом приймає `request`** і **обов'язково повертає відповідь**. Це найпростіший і найзрозуміліший спосіб почати працювати з views.

### Приклад

```python
from django.http import HttpResponse

def about(request):
    return HttpResponse("About page")
```

### Приклад із даними

```python
from django.http import HttpResponse

def hello_user(request):
    name = "Olena"
    return HttpResponse(f"Hello, {name}!")
```

Функціональні представлення зручні для початку навчання і для простих сторінок. Пізніше ви познайомитеся з класовими представленнями (Class-Based Views).

***

## `render()`

`render()` — це зручна функція Django, яка бере шаблон, підставляє в нього дані й повертає готовий `HttpResponse`. Вона приймає request, ім'я шаблону та контекст.

### Синтаксис

```python
return render(request, "core/home.html", context)
```

### Приклад

```python
from django.shortcuts import render

def home(request):
    context = {
        "title": "Головна сторінка",
        "message": "Ласкаво просимо до Django!",
    }
    return render(request, "core/home.html", context)
```

### Шаблон `home.html`

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ message }}</h1>
</body>
</html>
```

`render()` — це основний спосіб показувати HTML-сторінки в Django.

***

## Де зберігати шаблони

Шаблони повинні лежати в тому місці, де Django їх шукає. Є два підходи. Оберіть один і не змішуйте.

> **Правило, яке економить години налагодження:** усередині папки `templates/` створюйте ще одну папку з назвою застосунку. Тоді шлях у `render()` виглядає як `"core/home.html"`. Інакше файли з однаковою назвою з різних застосунків (наприклад, два `index.html`) конфліктуватимуть: Django візьме перший знайдений.

### Варіант 1: шаблони в папці застосунку (рекомендовано)

```text
project/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── migrations/
│   ├── templates/
│   │   └── core/              ← назва застосунку
│   │       ├── home.html
│   │       ├── about.html
│   │       └── contacts.html
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   ├── admin.py
│   └── apps.py
└── db.sqlite3
```

Для цього варіанта достатньо, щоб застосунок був у `INSTALLED_APPS`, а в `TEMPLATES` стояло `'APP_DIRS': True` (так за замовчуванням). **Якщо застосунок не додано в `INSTALLED_APPS`, Django не шукатиме шаблони в його папці й видасть `TemplateDoesNotExist`.**

### Варіант 2: загальна папка шаблонів

```text
project/
├── manage.py
├── config/
├── core/
├── templates/                 ← загальна папка в корені проєкту
│   ├── core/
│   │   ├── home.html
│   │   └── about.html
│   └── accounts/
│       └── login.html
└── db.sqlite3
```

Для цього варіанта потрібно вказати папку в `settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # загальна папка шаблонів
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Django шукає шаблон спочатку в папках зі списку `DIRS`, потім у папках `templates/` усіх застосунків з `INSTALLED_APPS`.

**Рекомендація:** почніть із варіанта 1. Це простіше для маленьких проєктів.

***

## Практика: перша сторінка застосунку

У цій частині ми створимо кілька сторінок і навчимося передавати в них дані. Усі три частини працюють з одним застосунком `core`.

### Частина A. Статичні сторінки

**Крок 1. Створити застосунок**

```bash
python manage.py startapp core
```

**Крок 2. Додати застосунок у `settings.py`**

```python
INSTALLED_APPS = [
    # ... стандартні застосунки Django ...
    "core",
]
```

**Крок 3. Створити папку для шаблонів**

Папка складається з двох рівнів: `templates`, а в ній `core`.

```bash
# macOS / Linux / Git Bash
mkdir -p core/templates/core

# Windows (cmd або PowerShell)
mkdir core\templates\core
```

Структура застосунку тепер така:

```text
core/
├── templates/
│   └── core/            ← сюди кладемо home.html, about.html, contacts.html
├── views.py
├── models.py
└── apps.py
```

**Крок 4. Створити файл `core/urls.py`** (його немає за замовчуванням)

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
]
```

**Крок 5. Підключити маршрути в головному `urls.py`** (`config/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
```

**Крок 6. Створити `core/views.py`**

```python
from django.shortcuts import render


def home(request):
    context = {
        "title": "Головна",
        "message": "Вітаємо на сайті!",
    }
    return render(request, "core/home.html", context)


def about(request):
    context = {
        "title": "Про нас",
        "text": "Це сторінка з інформацією про проєкт.",
    }
    return render(request, "core/about.html", context)


def contacts(request):
    context = {
        "title": "Контакти",
        "email": "info@example.com",
        "phone": "+380 50 123 45 67",
    }
    return render(request, "core/contacts.html", context)
```

**Крок 7. Шаблони**

`core/templates/core/home.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    <nav>
        <ul>
            <li><a href="{% url 'home' %}">Головна</a></li>
            <li><a href="{% url 'about' %}">Про нас</a></li>
            <li><a href="{% url 'contacts' %}">Контакти</a></li>
        </ul>
    </nav>
</body>
</html>
```

Шаблони `about.html` і `contacts.html` створіть самостійно за цим зразком, використавши змінні з їхніх контекстів (`text`, `email`, `phone`).

**Крок 8. Запустити сервер і перевірити**

```bash
python manage.py runserver
```

Відкрийте `http://127.0.0.1:8000/`, `/about/` і `/contacts/`. Перевірте, що посилання в навігації працюють.

> `{% url 'home' %}` будує адресу за **іменем** маршруту (`name="home"`). Це безпечніше, ніж прописувати адреси вручну: якщо ви зміните шлях у `urls.py`, усі посилання оновляться самі.

### Частина B. Параметри в адресі

Додаємо в `core/views.py` ще два view. Для навчання беремо дані зі словників; у справжньому проєкті вони будуть у базі даних.

```python
from django.http import Http404
from django.shortcuts import render

USERS = {
    "john": {"email": "john@example.com", "role": "admin"},
    "jane": {"email": "jane@example.com", "role": "user"},
    "bob": {"email": "bob@example.com", "role": "moderator"},
}

POSTS = {
    1: {"title": "Перший пост", "content": "Це мій перший пост на блозі."},
    2: {"title": "Другий пост", "content": "Продовжую писати про Django."},
    3: {"title": "Третій пост", "content": "Views та URL-маршрути."},
}


def user_profile(request, username):
    user_info = USERS.get(username)
    if user_info is None:
        raise Http404(f"Користувача {username} не знайдено")

    context = {
        "username": username,
        "email": user_info["email"],
        "role": user_info["role"],
    }
    return render(request, "core/profile.html", context)


def post_detail(request, post_id):
    post = POSTS.get(post_id)
    if post is None:
        raise Http404(f"Пост з ID {post_id} не знайдено")

    context = {
        "post_id": post_id,
        "title": post["title"],
        "content": post["content"],
    }
    return render(request, "core/post.html", context)
```

> **Чому `raise Http404`, а не `HttpResponse(..., status=404)`?** `Http404` — це сигнал Django «ресурсу немає». Він спрацьовує так само, як коли жоден маршрут не підійшов, і саме його обробляє сторінка 404, яку ви налаштуєте нижче. Рядок `HttpResponse(..., status=404)` теж повертає код 404, але повз цей механізм.

Додаємо маршрути в `core/urls.py`:

```python
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("users/<str:username>/", views.user_profile, name="user_profile"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
]
```

Шаблон `core/templates/core/profile.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Профіль {{ username }}</title>
</head>
<body>
    <h1>Профіль користувача: {{ username }}</h1>
    <p><strong>Email:</strong> {{ email }}</p>
    <p><strong>Роль:</strong> {{ role }}</p>
    <a href="{% url 'home' %}">Назад на головну</a>
</body>
</html>
```

Шаблон `core/templates/core/post.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>Post ID: {{ post_id }}</p>
    <article>{{ content }}</article>
    <a href="{% url 'home' %}">Назад на головну</a>
</body>
</html>
```

Посилання на сторінку з параметром у шаблоні передає значення другим аргументом:

```html
<a href="{% url 'user_profile' username='john' %}">Профіль John</a>
<a href="{% url 'post_detail' post_id=2 %}">Другий пост</a>
```

**Перевірте:** `/users/john/`, `/users/nobody/` (очікуємо 404), `/posts/2/`, `/posts/99/` (404), `/posts/abc/` (404, але з іншої причини: маршрут не збігся взагалі).

### Частина C. Список у шаблоні

Контекст — це словник, який view передає в шаблон. Через нього можна показувати змінні, списки, дати, числа та інші дані.

```python
def products(request):
    context = {
        "title": "Товари",
        "products": ["Laptop", "Mouse", "Keyboard"],
    }
    return render(request, "core/products.html", context)
```

Маршрут: `path("products/", views.products, name="products")`.

Шаблон `core/templates/core/products.html`:

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>

    {% if products %}
        <ul>
            {% for product in products %}
                <li>{{ product }}</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>Товари відсутні.</p>
    {% endif %}
</body>
</html>
```

Цей шаблон показує:

- підстановку змінної `{{ title }}`;
- цикл `{% for %}`;
- умову `{% if %}…{% else %}…{% endif %}`.

Спробуйте передати `"products": []` і подивіться, що зміниться. Стилізацією (CSS) та успадкуванням шаблонів ми займемося на наступних заняттях.

***

## Помилка 404 і власна сторінка помилки

Django має вбудовані обробники помилок, які спрацьовують, якщо сторінку не знайдено або в коді сталася помилка.

| Код | Коли виникає | Змінна обробника в `urls.py` |
| --- | --- | --- |
| `400` | некоректний запит | `handler400` |
| `403` | доступ заборонено | `handler403` |
| `404` | маршрут не знайдено або піднято `Http404` | `handler404` |
| `500` | необроблений виняток у коді | `handler500` |

### Кастомна сторінка 404

Щоб користувач побачив сторінку у стилі сайту, а не стандартне повідомлення, зробіть три кроки.

**1. View у `core/views.py`** (для 404 він приймає `request` і `exception`):

```python
def custom_404(request, exception):
    return render(request, "core/404.html", status=404)
```

Параметр `status=404` обов'язковий: без нього сторінка відповість кодом 200, хоча показує помилку.

**2. Шаблон `core/templates/core/404.html`:**

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Сторінку не знайдено</title>
</head>
<body>
    <h1>404: такої сторінки немає</h1>
    <a href="{% url 'home' %}">Повернутися на головну</a>
</body>
</html>
```

**3. Зареєструвати обробник у головному `urls.py`** (поряд із `urlpatterns`):

```python
handler404 = "core.views.custom_404"
```

> **Важливо:** під час розробки (`DEBUG = True`) Django завжди показує свою технічну сторінку 404 зі списком маршрутів. Щоб побачити власну сторінку, тимчасово встановіть у `settings.py` `DEBUG = False` і `ALLOWED_HOSTS = ["127.0.0.1", "localhost"]`, а потім поверніть як було.
>
> Обробник `handler500` приймає лише `request` (без `exception`). Для 403 та 400 сигнатура така сама, як для 404.

***

## Middleware

Middleware — це проміжне програмне забезпечення, яке обробляє запит і відповідь між браузером і view. Воно працює як «прослойка» між користувачем і логікою застосунку.

### Що може робити middleware

- перевіряти авторизацію;
- додавати інформацію в `request`;
- обробляти сесії;
- логувати запити;
- змінювати `response`.

### Порядок виконання

1. Запит приходить у Django.
2. Він проходить через middleware **зверху вниз** за списком `MIDDLEWARE`.
3. Потрапляє у view.
4. View формує відповідь.
5. Відповідь проходить через ті самі middleware **знизу вгору** і лише тоді повертається в браузер.

```text
Запит   → Middleware 1 → Middleware 2 → Middleware 3 → View
Відповідь ← Middleware 1 ← Middleware 2 ← Middleware 3 ← View
```

Middleware — важлива частина Django, бо саме тут працюють сесії, автентифікація, захист від CSRF та багато інших системних механізмів.

### Практичний приклад: логування запитів

Створимо власне middleware, яке записує в журнал метод і шлях запиту та статус-код відповіді.

Файл `core/middleware.py`:

```python
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # Виконується один раз, під час запуску сервера
        self.get_response = get_response

    def __call__(self, request):
        # Код ДО view
        logger.info("Запит: %s %s", request.method, request.path)

        response = self.get_response(request)   # тут викликаються наступні middleware і view

        # Код ПІСЛЯ view
        logger.info("Відповідь: %s | статус %s", request.path, response.status_code)
        return response
```

Рядок `response = self.get_response(request)` ділить код навпіл: усе, що написано до нього, працює на шляху «вниз» до view, усе, що після нього, — на шляху «вгору».

Додаємо middleware у кінець списку в `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.RequestLoggingMiddleware',  # ← наше middleware
]
```

**Без налаштування журналу повідомлення `INFO` у терміналі не з'являться**, бо стандартний рівень — `WARNING`. Додайте в `settings.py`:

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "core": {"handlers": ["console"], "level": "INFO"},
    },
}
```

Тепер у терміналі з `runserver` для кожного запиту з'являтимуться два рядки: що прийшло і що ми відповіли.

> Старіший стиль middleware з методами `process_request` та `process_response` (через `MiddlewareMixin`) ви можете зустріти в прикладах в інтернеті. Він працює, але в нових проєктах використовують сучасний стиль, показаний вище.

***

## Типові помилки та як їх виправити

Перш ніж шукати рішення, **прочитайте останній рядок помилки та знайдіть перший рядок із вашим файлом і номером рядка**.

### Помилка 1: Застосунок не в `INSTALLED_APPS`

**Симптом:**

```text
TemplateDoesNotExist: core/home.html
```

Шаблони з папки застосунку Django шукає лише в застосунках зі списку `INSTALLED_APPS`. Також без цього не працюватимуть моделі й міграції застосунку.

**Виправлення:**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # ← додайте ваш застосунок
]
```

Якщо ж у назві застосунку є опечатка, ви побачите `ModuleNotFoundError: No module named 'cor'`.

### Помилка 2: View не імпортовано в `urls.py`

**Симптом:**

```python
urlpatterns = [
    path("", home, name="home"),   # NameError: name 'home' is not defined
]
```

**Виправлення:**

```python
from . import views  # або from .views import home

urlpatterns = [
    path("", views.home, name="home"),
]
```

### Помилка 3: Шаблон не знайдено

**Симптом:**

```text
TemplateDoesNotExist: core/home.html
```

Перевірте по черзі:

1. Застосунок є в `INSTALLED_APPS` (див. помилку 1).
2. Файл лежить саме тут: `core/templates/core/home.html` (дві папки: `templates` і `core`).
3. Шлях у `render()` збігається з шляхом після `templates/`:

```python
# Правильно:
return render(request, "core/home.html", context)

# Неправильно:
return render(request, "templates/core/home.html", context)
```

4. Якщо шаблони лежать в окремій папці `templates/` у корені проєкту, її додано в `DIRS` (див. «Де зберігати шаблони»).
5. На сторінці помилки прокрутіть до блоку **Template-loader postmortem**: Django перелічив усі місця, де шукав файл. Порівняйте їх із тим, де файл лежить насправді.

### Помилка 4: Параметр без конвертера

```python
path("posts/<post_id>/", views.post_detail)   # post_id буде рядком "5", а не числом 5
```

Маршрут працює, але `POSTS.get("5")` не знайде ключ `5` у словнику з цілими ключами, і ви отримаєте 404 навіть для існуючого поста.

**Виправлення:**

```python
path("posts/<int:post_id>/", views.post_detail)
```

### Помилка 5: View не приймає параметр

**Симптом:**

```python
path("users/<str:username>/", views.user_profile)

def user_profile(request):   # забули username
    return render(request, "core/profile.html")
```

Django викличе `user_profile(request, username="john")`, а функція такого аргументу не має. Результат: `TypeError: user_profile() got an unexpected keyword argument 'username'`.

**Виправлення:**

```python
def user_profile(request, username):
    return render(request, "core/profile.html", {"username": username})
```

### Помилка 6: Слеші в шляху

- `path("/about/", ...)` — зайвий слеш на початку; маршрут ніколи не збігається.
- `path("about", ...)` — працює для `/about`, але `/about/` дасть 404. За домовленістю шляхи закінчують слешем: `path("about/", ...)`.

### Помилка 7: Забули `return` або повернули не відповідь

**Симптом:**

```text
ValueError: The view core.views.home didn't return an HttpResponse object. It returned None instead.
```

**Причина:** у функції немає `return` (або він залишився лише в одній гілці `if`). View завжди має повертати відповідь.

### Алгоритм пошуку помилки

1. Прочитайте **останній рядок** помилки: він каже, що саме сталося.
2. Знайдіть **перший рядок із шляхом до вашого файлу** та номером рядка. Відкрийте цей файл.
3. Якщо це 404: порівняйте адресу з переліком маршрутів на сторінці помилки.
4. Перевірте маршрут у `urls.py`: чи вказує на правильний view і чи імена параметрів збігаються?
5. Перевірте імпорти і сам view: чи приймає він усі параметри і чи повертає відповідь?
6. Якщо проблема з шаблоном: перевірте `INSTALLED_APPS`, структуру папок і блок Template-loader postmortem.
7. Змінюйте **одну річ за раз** і перезавантажуйте сторінку. `runserver` сам перезапускається після змін у `.py`-файлах; якщо сервер завершився з помилкою, читайте її в терміналі.

***

## Самоперевірка

Відповідайте без підказок, потім звіртеся з відповідями нижче.

1. Яка різниця між `urls.py` і `views.py`?
2. Що станеться, якщо відкрити `/posts/abc/`, коли в маршруті стоїть `<int:post_id>`?
3. Для чого потрібен `name="home"` у `path()`?
4. Чим `/posts/5/` відрізняється від `/posts/?page=5` і як view отримує кожне значення?
5. Чому шаблон краще класти в `templates/core/home.html`, а не в `templates/home.html`?
6. Чим `raise Http404` відрізняється від `return HttpResponse(..., status=404)`?
7. У якому порядку виконуються middleware під час запиту і під час відповіді?

**Відповіді**

1. `urls.py` визначає, за якою адресою викликається view; `views.py` визначає, що саме показати користувачу.
2. Маршрут не збігається, view не викликається, Django повертає 404 (технічну сторінку при `DEBUG = True`).
3. Ім'я дозволяє будувати адресу через `{% url 'home' %}` або `reverse("home")`, і зміна шляху в `urls.py` не ламає посилання.
4. `/posts/5/` — параметр шляху, потрапляє у view як аргумент `post_id`. `?page=5` — параметр запиту, view читає його через `request.GET.get("page")`.
5. Додаткова папка з назвою застосунку створює простір імен: файли з однаковими назвами з різних застосунків не конфліктують.
6. `Http404` обробляється механізмом Django (зокрема `handler404`, тобто вашою власною сторінкою), а `HttpResponse(status=404)` лише повертає код без цього механізму.
7. Запит: зверху вниз за списком `MIDDLEWARE`. Відповідь: знизу вгору.

***

## Практичне завдання

Застосуйте вивчене до свого навчального проєкту (Task & Bug Manager, Expense Tracker або Service Management System). Дані поки що беріть зі словників або списків у коді, база даних буде пізніше.

1. Створіть застосунок для головної сутності вашого проєкту (`issues`, `transactions` або `orders`) і підключіть його через `include()` з префіксом, наприклад `path("issues/", include("issues.urls"))`.
2. Зробіть три сторінки:
   - головну сторінку застосунку;
   - сторінку-список (цикл `{% for %}` із умовою `{% if %}` для порожнього списку);
   - сторінку однієї сутності за адресою `<int:pk>`, яка піднімає `Http404`, якщо запису немає.
3. Усі посилання між сторінками зробіть через `{% url %}`. Шаблони розмістіть у `templates/<назва застосунку>/`.
4. Налаштуйте власну сторінку 404 і перевірте її з `DEBUG = False`.
5. **За бажанням:** додайте middleware, яке логує час виконання кожного запиту (підказка: `time.perf_counter()` до і після `self.get_response(request)`).

Результат закомітьте в окрему гілку від `main`. У README коротко опишіть, які адреси доступні у вашому застосунку.

***

## Підсумок

На цьому занятті ви навчилися будувати просту структуру Django-сторінок: налаштовувати маршрути, створювати views, передавати дані в шаблони, повертати помилку 404 та розуміти шлях HTTP-запиту від браузера до відповіді.

Запам'ятайте головне:

- `urls.py` — **де**, `views.py` — **що**, шаблон — **як виглядає**;
- шаблони кладіть у `templates/<назва застосунку>/`, а застосунок додавайте в `INSTALLED_APPS`;
- параметри шляху описуємо в `path()`, параметри запиту читаємо з `request.GET`;
- помилку читаємо знизу вгору, а змінюємо одну річ за раз.

Це основа для наступних тем: шаблони, форми, Django ORM і побудова повноцінного веб-застосунку.