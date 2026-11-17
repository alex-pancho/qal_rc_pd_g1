# Заняття 45. Створення HTTP API за допомогою Django REST Framework

## Вступ

На попередніх заняттях ми створювали вебзастосунок, який взаємодіяв із користувачем через HTML-сторінки. Такий підхід чудово працює для класичних сайтів, де сервер формує готову сторінку та надсилає її браузеру.

Проте більшість сучасних застосунків працюють інакше. Мобільні додатки, React, Vue, Angular, Flutter, десктопні клієнти та навіть інші сервери взаємодіють із бекендом через HTTP API. Сервер більше не генерує HTML — він повертає дані у форматі JSON.

Саме тому практично кожен сучасний Python/Django-розробник повинен вміти створювати REST API.

У цьому занятті ми познайомимося з Django REST Framework (DRF) — найпопулярнішою бібліотекою для побудови API на Django.

# Що таке API

API (Application Programming Interface) — це набір правил, за якими одна програма може взаємодіяти з іншою.

У випадку веброзробки API працює через HTTP.

Наприклад:

```
Мобільний додаток
        │
        ▼
 HTTP GET /api/posts/
        │
        ▼
 Django REST API
        │
        ▼
 JSON
```

Замість HTML сервер повертає JSON.

Наприклад:

```json
[
    {
        "id": 1,
        "title": "Перший запис",
        "author": "Alex"
    },
    {
        "id": 2,
        "title": "Другий запис",
        "author": "Kate"
    }
]
```

Такий формат однаково легко читається:

* JavaScript
* Python
* Java
* Swift
* Kotlin
* C#
* Go

# REST API

REST (Representational State Transfer) — найпоширеніший стиль побудови HTTP API.

Основна ідея проста:

кожен URL представляє певний ресурс.

Наприклад:

```
/posts/
/users/
/comments/
/categories/
```

Дії виконуються за допомогою HTTP-методів.

| Метод  | Дія              |
| ------ | ---------------- |
| GET    | отримати         |
| POST   | створити         |
| PUT    | повністю оновити |
| PATCH  | частково оновити |
| DELETE | видалити         |

Наприклад:

```
GET    /api/posts/
POST   /api/posts/
GET    /api/posts/15/
PATCH  /api/posts/15/
DELETE /api/posts/15/
```

# SPA-архітектура

SPA (Single Page Application) — це сучасний підхід до побудови вебзастосунків, коли браузер завантажує лише одну HTML-сторінку, а всі подальші дані отримує через API.

Класична схема:

```
Browser
     │
     ▼
 Django
     │
 HTML
```

SPA:

```
Browser
     │
React / Vue
     │
HTTP API
     │
Django REST Framework
     │
JSON
```

У цьому випадку:

* Django відповідає лише за дані;
* React відповідає за інтерфейс;
* мобільний застосунок використовує той самий API.

# Переваги SPA

Основні переваги:

* швидка робота інтерфейсу;
* менше перезавантажень сторінок;
* один API для вебсайту та мобільного застосунку;
* простіша інтеграція з іншими сервісами;
* фронтенд і бекенд можуть розроблятися незалежно.

Саме тому більшість сучасних комерційних проєктів використовують REST API.

# Що таке Django REST Framework

Django REST Framework (DRF) — це надбудова над Django, яка значно спрощує створення API.

DRF додає:

* серіалізатори;
* APIView;
* Generic Views;
* ViewSets;
* Router;
* автоматичну документацію;
* автентифікацію;
* дозволи;
* пагінацію;
* фільтрацію.

Практично всі сучасні Django-проєкти використовують саме DRF.

# Встановлення DRF

Встановлюємо пакет:

```bash
pip install djangorestframework
```

Додаємо його до INSTALLED_APPS.

```python
INSTALLED_APPS = [
    ...
    "rest_framework",
]
```

Після цього можна створювати API.

# JSON — основний формат обміну

REST API майже завжди працює з JSON.

Наприклад модель:

```python
class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
```

Повертається як:

```json
{
    "id": 1,
    "title": "Hello",
    "text": "First post"
}
```

Саме перетворення Python-об'єктів у JSON називається серіалізацією.

# Серіалізатори

Serializer — це аналог Django Form, але для API.

Він:

* перетворює модель у JSON;
* перевіряє вхідні дані;
* створює модель;
* оновлює модель.

Серіалізатор є центральною частиною DRF.

# Створення ModelSerializer

Створимо файл serializers.py.

```python
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"
```

Тепер DRF автоматично знає:

* які поля існують;
* які типи даних очікуються;
* які перевірки потрібно виконати.

# Перевірка даних

Serializer може виконувати власну валідацію.

```python
class PostSerializer(serializers.ModelSerializer):

    def validate_title(self, value):

        if len(value) < 5:
            raise serializers.ValidationError(
                "Назва занадто коротка."
            )

        return value
```

При неправильних даних користувач одразу отримує повідомлення про помилку.

# Серіалізація об'єкта

Приклад використання.

```python
post = Post.objects.first()

serializer = PostSerializer(post)

print(serializer.data)
```

Результат:

```json
{
    "id": 1,
    "title": "Python",
    "text": "Hello world"
}
```

# Серіалізація списку

Якщо потрібно повернути багато записів:

```python
posts = Post.objects.all()

serializer = PostSerializer(
    posts,
    many=True
)

return Response(serializer.data)
```

Параметр `many=True` говорить DRF, що потрібно серіалізувати список моделей.

# Вкладена серіалізація

Нехай є дві моделі.

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
```

Можна повернути інформацію про автора разом із постом.

# Nested Serializer

Створимо два серіалізатори.

```python
class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = "__all__"
```

Результат:

```json
{
    "title": "REST API",
    "author": {
        "id": 5,
        "name": "Alex"
    }
}
```

# Перший API Endpoint

Створимо представлення.

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class PostList(APIView):

    def get(self, request):

        posts = Post.objects.all()

        serializer = PostSerializer(
            posts,
            many=True
        )

        return Response(serializer.data)
```

Тепер URL повертає JSON.

# Додавання URL

```python
urlpatterns = [
    path(
        "api/posts/",
        PostList.as_view()
    )
]
```

Запит:

```
GET /api/posts/
```

Відповідь:

```json
[
    {
        "id": 1,
        "title": "Python"
    }
]
```

# Створення нового запису

Метод POST.

```python
def post(self, request):

    serializer = PostSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)
```

Тепер API може створювати нові записи.

# Структура REST API

Зазвичай структура виглядає так:

```
blog/

    serializers.py

    views.py

    urls.py

    models.py
```

Поступово проєкт може містити десятки окремих API-модулів.

# Документація API

Однією з головних переваг сучасних REST API є можливість автоматично генерувати документацію.

Документація дозволяє:

* переглядати доступні ендпоінти;
* бачити параметри запитів;
* тестувати API без Postman;
* бачити приклади відповідей;
* спрощувати інтеграцію для інших розробників.

У DRF це можна зробити за допомогою Swagger/OpenAPI.

# Що таке Swagger

Swagger — це набір інструментів для роботи з OpenAPI Specification.

Він автоматично створює інтерактивну документацію.

Наприклад, відкривши сторінку:

```
/api/docs/
```

ми можемо:

* виконати GET;
* створити POST;
* передати JSON;
* отримати відповідь сервера;
* перевірити коди помилок.

Swagger значно прискорює розробку та тестування API.

# Встановлення drf-spectacular

Для генерації документації використаємо пакет `drf-spectacular`.

```bash
pip install drf-spectacular
```

Додаємо застосунок до `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "drf_spectacular",
]
```

І налаштовуємо DRF:

```python
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS":
        "drf_spectacular.openapi.AutoSchema",
}
```

# Налаштування маршрутів документації

У головному файлі `urls.py` додаємо маршрути:

```python
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
    ),
]
```

Тепер за адресою `/api/docs/` буде доступна інтерактивна Swagger UI.

# Практична робота

Під час практики студенти створять власне REST API для навчального Django-проєкту.

План роботи:

1. Встановити Django REST Framework.
2. Створити серіалізатор для моделі.
3. Реалізувати API-представлення.
4. Додати маршрути.
5. Перевірити роботу через браузер.
6. Встановити `drf-spectacular`.
7. Згенерувати документацію Swagger.
8. Перевірити роботу API через Swagger UI.

# Типові помилки початківців

Під час створення першого API студенти часто припускаються таких помилок:

* забувають додати `rest_framework` до `INSTALLED_APPS`;
* не використовують `many=True` для списків об'єктів;
* плутають `request.POST` і `request.data`;
* не викликають `serializer.is_valid()`;
* забувають викликати `serializer.save()`;
* не додають маршрути до `urls.py`;
* намагаються повертати модель напряму замість використання серіалізатора.
