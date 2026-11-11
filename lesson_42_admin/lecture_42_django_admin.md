# Заняття 42. Панель адміністратора Django (2 год.)

## Мета заняття

Після завершення заняття студенти зможуть:

* використовувати вбудовану панель адміністрування Django;
* створювати суперкористувачів та звичайних користувачів;
* реєструвати моделі в Django Admin;
* налаштовувати зовнішній вигляд адміністративної панелі;
* працювати з групами та дозволами;
* керувати даними без написання SQL-запитів;
* обмежувати доступ користувачів до окремих моделей.

---

# 1. Що таке Django Admin

Однією з найсильніших сторін Django є готова адміністративна панель.

Вона автоматично створює інтерфейс для роботи з моделями бази даних.

Не потрібно окремо писати сторінки:

* додавання записів;
* редагування;
* видалення;
* пошук;
* фільтрацію;
* сортування.

Все це Django створює автоматично.

Саме тому багато внутрішніх CRM, ERP та адмін-панелей пишуться на Django.

---

## Що потрібно для роботи Admin

У новому проєкті все вже налаштовано.

Переконайтесь, що в `settings.py` присутні:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

У головному `urls.py` має бути маршрут:

```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
```

---

# 2. Створення суперкористувача

Адмін-панель доступна лише авторизованим адміністраторам.

Створюємо першого користувача командою:

```bash
python manage.py createsuperuser
```

Консоль попросить ввести:

```
Username:
Email:
Password:
Password (again):
```

Після успішного створення з'явиться повідомлення:

```
Superuser created successfully.
```

Тепер запускаємо сервер:

```bash
python manage.py runserver
```

Відкриваємо

```
http://127.0.0.1:8000/admin/
```

та авторизуємося.

---

# 3. Структура Django Admin

Після входу відкриється головна сторінка.

У стандартній конфігурації видно два розділи.

Authentication and Authorization

* Users
* Groups

Саме через них можна керувати всіма користувачами системи.

Поки що власних моделей ще немає.

---

# 4. Створення моделі

Нехай у проєкті є модель книги.

```python
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.title
```

Створимо міграції.

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 5. Реєстрація моделі

Поки модель не зареєстрована, її немає в адмінці.

Файл:

```python
admin.py
```

Мінімальна реєстрація:

```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

Після оновлення сторінки модель автоматично з'явиться.

---

# 6. Додавання записів

Тепер можна:

* створювати книги;
* редагувати;
* видаляти;
* переглядати список.

Без написання жодного SQL-запиту.

Наприклад:

| Назва                  | Автор           | Рік  |
| ---------------------- | --------------- | ---- |
| Django для початківців | William Vincent | 2024 |
| Python Crash Course    | Eric Matthes    | 2023 |
| Fluent Python          | Luciano Ramalho | 2022 |

---

# 7. Налаштування відображення моделі

Стандартне відображення не дуже інформативне.

Його легко покращити.

```python
from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "year",
    )
```

Тепер список містить три колонки.

---

## Додавання пошуку

```python
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "year",
    )

    search_fields = (
        "title",
        "author",
    )
```

Тепер зверху з'явиться поле пошуку.

---

## Додавання фільтрів

```python
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "year",
    )

    list_filter = (
        "year",
    )
```

Праворуч з'явиться фільтр за роком.

---

## Сортування

```python
class BookAdmin(admin.ModelAdmin):

    ordering = (
        "-year",
    )
```

Книги відображатимуться від нових до старих.

---

# 8. Створення звичайного користувача

Не всі користувачі повинні бути адміністраторами.

Створити користувача можна в Python Shell.

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

User.objects.create_user(
    username="student",
    password="password123"
)
```

Такий користувач:

* може входити у систему;
* не має адміністративних прав.

---

# 9. Надання доступу до Admin

Якщо потрібно дозволити вхід в Admin без повних прав:

```python
user = User.objects.get(username="student")

user.is_staff = True

user.save()
```

Тепер користувач може авторизуватися в `/admin`.

Але поки що нічого не бачить.

Чому?

Тому що немає дозволів.

---

# 10. Дозволи (Permissions)

Для кожної моделі Django автоматично створює дозволи:

* Add
* Change
* Delete
* View

Наприклад для Book:

* Can add book
* Can change book
* Can delete book
* Can view book

Їх можна призначати окремим користувачам.

---

# 11. Групи

Зручніше використовувати групи.

Наприклад:

```
Editors
Managers
Moderators
Teachers
Students
```

Кожній групі призначаються дозволи.

Після цього достатньо додати користувача до потрібної групи.

---

Приклад.

Група **Editors** має:

* View Book
* Add Book
* Change Book

але не має

* Delete Book

Таким чином редактор може працювати з даними, але не може їх видалити.

---

# 12. Програмне створення груп

Групи можна створювати кодом.

```python
from django.contrib.auth.models import Group

Group.objects.create(name="Editors")
```

Після цього група з'явиться в адмінці.

---

# 13. Надання дозволів через код

```python
from django.contrib.auth.models import Permission

permission = Permission.objects.get(
    codename="change_book"
)

group.permissions.add(permission)
```

Тепер усі користувачі групи можуть редагувати книги.

---

# 14. Перевірка дозволів

У коді можна перевірити права користувача.

```python
if request.user.has_perm("library.change_book"):
    print("Редагування дозволено")
```

або

```python
if request.user.is_superuser:
    print("Адміністратор")
```

---

# 15. Зміна заголовка адмін-панелі

Стандартний напис:

```
Django administration
```

Можна змінити.

```python
from django.contrib import admin

admin.site.site_header = "Library Administration"

admin.site.site_title = "Library"

admin.site.index_title = "Керування бібліотекою"
```

---

# 16. Практична робота

Під час заняття студенти виконують такі завдання.

### Завдання 1

Створити суперкористувача.

---

### Завдання 2

Зареєструвати модель Book.

---

### Завдання 3

Додати декілька книг через Django Admin.

---

### Завдання 4

Налаштувати:

* list_display
* search_fields
* list_filter
* ordering

---

### Завдання 5

Створити користувача **editor**.

---

### Завдання 6

Створити групу **Editors**.

---

### Завдання 7

Надати групі дозволи:

* перегляд книг;
* створення книг;
* редагування книг.

---

### Завдання 8

Додати користувача **editor** до групи Editors.

---

### Завдання 9

Перевірити:

* editor може входити в Admin;
* editor бачить книги;
* editor може створювати нові книги;
* editor не може видаляти книги.

---

# Підсумки

На цьому занятті студенти познайомилися з однією з найпотужніших можливостей Django — автоматичною адміністративною панеллю. Вони навчилися створювати суперкористувачів і звичайних користувачів, реєструвати моделі, налаштовувати їх відображення, виконувати пошук і фільтрацію даних, працювати з групами та дозволами. Також було показано, як реалізувати рольову модель доступу, що є важливою складовою будь-якого реального веб-застосунку. Цих знань достатньо для побудови повноцінної внутрішньої системи керування даними без написання власного адміністративного інтерфейсу.
