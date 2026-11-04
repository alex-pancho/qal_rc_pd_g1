# Заняття 40: Моделі, міграції та Django ORM — для студентів

Nov 2, 2026 · @Oleksandr Panchenko

## Мета заняття і що ми побудуємо

На цьому занятті дані демо-LMS переїжджають зі словників у файлі `courses/data.py` у справжню базу даних, а працювати з нею ми будемо через Django ORM, тобто на Python, без жодного рядка SQL. Заняття продовжує проєкт `lms` із заняття 39: шаблони, `base.html`, CSS і JavaScript залишаються, змінюється лише джерело даних.

Після заняття ви зможете:

- описати таблицю базі даних класом Python (модель) і пояснити, що таке поле;
- створити й застосувати міграцію, а також прочитати SQL, який за нею стоїть;
- виконувати CRUD в Django shell: створювати, читати, змінювати й видаляти записи;
- фільтрувати, сортувати й рахувати записи через `QuerySet`;
- зв'язувати моделі через `ForeignKey` та `ManyToManyField` і ходити по цих зв'язках в обидва боки;
- змінити модель, що вже має дані, і не втратити їх: нова міграція, `default`, `null`, `blank`;
- керувати даними через адмінку Django;
- підключити моделі до `views` і шаблонів та помітити проблему «N+1 запитів»;
- повторити цей шлях у власному проєкті (Task & Bug Manager, Expense Tracker, Service Management System).

Маленькими кроками, як і на занятті 39, ми збираємо схему з чотирьох моделей:

| Модель | Що описує | Зв'язки |
| --- | --- | --- |
| `Course` | курс | має багато уроків і багато студентів |
| `Lesson` | урок курсу | належить одному курсу (`ForeignKey`) |
| `Student` | студент | записаний на кілька курсів |
| `Enrollment` | запис студента на курс, його прогрес і дедлайн | з'єднує `Student` і `Course` |

Кроки заняття:

| Крок | Що робимо | Що побачимо |
| --- | --- | --- |
| 1 | перша модель `Course` | клас у `models.py` |
| 2 | міграції | таблиця в `db.sqlite3`, SQL з `sqlmigrate` |
| 3 | Django shell | CRUD і `QuerySet` у терміналі |
| 4 | адмінка | курси додаються мишею |
| 5 | модель у `view` і шаблоні | сторінки показують дані з бази |
| 6 | модель `Lesson` і `ForeignKey` | уроки в базі, нова міграція |
| 7 | зміна моделі, що вже має дані | нова міграція, `default`, `null`, `blank` |
| 8 | `Student` і `Enrollment` | кабінет студента з бази |
| 9 | запити, `select_related`, `annotate` | рахуємо запити до бази |

Ритм заняття той самий, що й на занятті 39: **маленький крок, показати результат, коміт**. Перед початком створіть гілку `git checkout -b lesson-40` і робіть `git commit` після кожного кроку.

## Ідея: модель — це таблиця, міграція — історія змін схеми

**Модель** — це клас Python, який описує одну таблицю бази даних. Django сам складає SQL і для створення цієї таблиці, і для запитів до неї. Вам це знайомо із заняття 33: там були таблиці `lms_*`, тепер вони стануть класами.

| База даних (SQL) | Django ORM |
| --- | --- |
| таблиця | клас-модель (`class Course(models.Model)`) |
| стовпець | поле (`title = models.CharField(...)`) |
| рядок | об'єкт класу (`Course(title="...")`) |
| `SELECT * FROM courses_course` | `Course.objects.all()` |
| `WHERE level = 'beginner'` | `Course.objects.filter(level="beginner")` |
| `INSERT`, `UPDATE`, `DELETE` | `create()`, `save()` / `update()`, `delete()` |
| `JOIN` | запит через зв'язок: `Lesson.objects.filter(course__slug="django-web")` |
| `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE` | поле `id` (додається автоматично), `ForeignKey`, `unique=True` |

Що означає абревіатура ORM: Object-Relational Mapping, тобто «відображення об'єктів на реляційну базу». Ми пишемо Python, а Django перекладає його на SQL для тієї бази, яку підключено в `settings.py` (зараз це файл `db.sqlite3`, пізніше може бути PostgreSQL, а код моделей залишиться тим самим).

**Міграція** — це файл у папці `migrations/`, який описує одну зміну схеми бази: «створити таблицю», «додати стовпець». Міграції працюють як git для структури бази: кожна зміна — окремий файл, і Django знає, які з них уже застосовано.

Цикл роботи з моделями завжди один і той самий:

1. Змінюємо код у `models.py`.
2. `python manage.py makemigrations` — Django порівнює моделі з уже наявними міграціями і створює новий файл міграції.
3. `python manage.py migrate` — Django застосовує нові міграції до бази.
4. Файли міграцій комітимо в git разом із кодом.

Перші дві команди мають різні ролі: `makemigrations` лише створює файл (базу не чіпає), а `migrate` змінює базу. Забути другу команду — найчастіша причина помилок на цьому занятті.

## Крок 1. Перша модель: Course

Мета кроку: описати таблицю курсів класом Python. База даних на цьому кроці ще не змінюється.

Створіть гілку й відкрийте `courses/models.py` (він створений командою `startapp` і поки порожній):

```bash
git checkout -b lesson-40
```

```python
from django.db import models


class Course(models.Model):
    class Level(models.TextChoices):
        BEGINNER = "beginner", "Початковий"
        INTERMEDIATE = "intermediate", "Середній"
        ADVANCED = "advanced", "Просунутий"

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.BEGINNER)
    teacher = models.CharField(max_length=100)
    hours = models.PositiveSmallIntegerField()
    is_new = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
```

Усі моделі наслідують `models.Model`: саме це робить клас таблицею. Кожен атрибут класу з типом `models.…Field` стає стовпцем:

| Поле в моделі | Що означає | Стовпець у SQLite |
| --- | --- | --- |
| `SlugField(unique=True)` | короткий ідентифікатор для адреси (`django-web`); значення не повторюються | `varchar(50) NOT NULL UNIQUE` |
| `CharField(max_length=200)` | короткий текст; `max_length` обов'язковий | `varchar(200) NOT NULL` |
| `CharField(choices=…)` | текст з обмеженим набором значень | `varchar(20) NOT NULL` |
| `PositiveSmallIntegerField()` | мале ціле число, не менше нуля | `smallint unsigned NOT NULL CHECK ("hours" >= 0)` |
| `BooleanField(default=False)` | так/ні | `bool NOT NULL` |
| `TextField(blank=True)` | довгий текст без обмеження довжини | `text NOT NULL` |

Таблиця вище взята з реального SQL, який згенерує Django на наступному кроці. Звернути увагу варто на три речі.

**1. Поле `id` писати не потрібно.** Django сам додає первинний ключ `id` (ціле число, яке збільшується саме).

**2. `choices` зберігає одне, а показує інше.** У базі лежить `"beginner"`, а людині в шаблоні покажемо `"Початковий"` за допомогою методу `course.get_level_display()`. Клас `Level` лише описує допустимі пари «значення, підпис».

**3. `__str__` визначає, як об'єкт виглядає як текст.** Без нього в терміналі й адмінці ви побачите `Course object (1)`, а з ним — назву курсу.

Перегляньте, що Django не знаходить помилок у моделі:

```bash
python manage.py check
```

Очікуваний результат: `System check identified no issues (0 silenced).`

**Показати:** поки що нічого нового в браузері. Таблиці в базі ще немає, її створимо на наступному кроці. Усі існуючі сторінки (які беруть дані з `data.py`) працюють як раніше.

```bash
git add . && git commit -m "Крок 1: модель Course"
```

## Крок 2. Міграції: від класу до таблиці

Мета кроку: створити в базі таблицю для моделі `Course` і побачити, який SQL за цим стоїть. Робимо це трьома командами.

### 2.1. makemigrations: створити файл міграції

```bash
python manage.py makemigrations
```

```text
Migrations for 'courses':
  courses/migrations/0001_initial.py
    + Create model Course
```

У папці `courses/migrations/` з'явився файл `0001_initial.py`. Відкрийте його: це звичайний Python-код, який описує операцію `CreateModel` з усіма полями (скорочено):

```python
class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(unique=True)),
                ("title", models.CharField(max_length=200)),
                # ... решта полів ...
            ],
        ),
    ]
```

Зверніть увагу на `dependencies`: у наступних міграцій там буде посилання на попередню (`("courses", "0001_initial")`). Так Django знає порядок застосування.

На цьому етапі **база ще не змінилася**. `makemigrations` лише порівняв моделі з наявними міграціями й записав різницю у файл.

### 2.2. sqlmigrate: подивитися SQL

Дізнатися, що саме зробить міграція, можна не застосовуючи її:

```bash
python manage.py sqlmigrate courses 0001
```

```sql
BEGIN;
--
-- Create model Course
--
CREATE TABLE "courses_course" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "slug" varchar(50) NOT NULL UNIQUE, "title" varchar(200) NOT NULL, "level" varchar(20) NOT NULL, "teacher" varchar(100) NOT NULL, "hours" smallint unsigned NOT NULL CHECK ("hours" >= 0), "is_new" bool NOT NULL, "description" text NOT NULL);
COMMIT;
```

Це той самий `CREATE TABLE`, який ви писали на заняттях із SQL. Назва таблиці утворюється як `<застосунок>_<модель>`: `courses_course`. Команда виконується в транзакції (`BEGIN … COMMIT`): якщо щось піде не так, таблиця не залишиться наполовину створеною.

### 2.3. migrate: застосувати до бази

```bash
python manage.py migrate
```

```text
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, courses, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
  Applying courses.0001_initial... OK
  Applying sessions.0001_initial... OK
```

(Список скорочено. Якщо `migrate` у проєкті запускали вперше, між `admin.0001` і `courses.0001` буде більше рядків: це стандартні таблиці користувачів, груп і сесій, які Django створює разом із вашою. Якщо запускали раніше, ви побачите лише рядок `Applying courses.0001_initial... OK`.)

У корені проєкту з'явився файл `db.sqlite3`: це і є наша база даних, один файл. Перевірити, що застосовано, можна так:

```bash
python manage.py showmigrations courses
```

```text
courses
 [X] 0001_initial
```

`[X]` означає «застосовано», `[ ]` — «ще ні». Django запам'ятовує це в службовій таблиці `django_migrations`, тому повторний `migrate` нічого не зробить.

Якщо у вас встановлено клієнт SQLite або відкрито PyCharm / DBeaver, можете відкрити `db.sqlite3` і побачити таблицю `courses_course`. Структура збігається з тим, що показав `sqlmigrate`.

### Правила міграцій

- Файли міграцій **комітимо в git** разом із моделями. Це частина проєкту.
- Файл `db.sqlite3` зазвичай **не комітять**: це дані, а не код (перевірте `.gitignore`).
- **Не редагуйте** міграцію, яку вже застосовано (або яку вже отримали колеги). Якщо модель треба змінити, створюємо нову міграцію (крок 7).
- Не видаляйте файли міграцій навмання: Django втратить історію, і база розійдеться з кодом.

**Показати:** файл `0001_initial.py`, виведення `sqlmigrate`, наявність `db.sqlite3` й виведення `showmigrations`.

```bash
git add . && git commit -m "Крок 2: міграція Course"
```

## Крок 3. Django shell: CRUD і QuerySet

Мета кроку: навчитися створювати, читати, змінювати та видаляти записи з Python-коду, не пишучи SQL. Для експериментів у Django є інтерактивна консоль, яка вже знає про налаштування проєкту:

```bash
python manage.py shell
```

Далі всі рядки з `>>>` вводимо в цю консоль. Вивід нижче отримано на реальному проєкті. Якщо у вас `id` або порядок інші, це нормально.

```python
>>> from courses.models import Course
>>> Course.objects.all()
<QuerySet []>
```

`Course.objects` — це **менеджер**: через нього ми звертаємось до таблиці. `all()` повертає `QuerySet` (поки порожній: у таблиці немає рядків).

### 3.1. Create: створити запис

Два способи. Перший: створити об'єкт у пам'яті й **окремо** зберегти.

```python
>>> course = Course(slug="qa-basics", title="QA: основи тестування", level="beginner", teacher="Олександр Панченко", hours=24, is_new=True)
>>> print(course.pk)
None
>>> course.save()
>>> print(course.pk)
1
```

До `save()` рядка в базі немає, тому `pk` (первинний ключ, він же `id`) дорівнює `None`. Після `save()` Django виконав `INSERT` і записав у об'єкт номер рядка.

Другий спосіб: `create()` робить обидва кроки разом.

```python
>>> Course.objects.create(slug="django-web", title="Django: веб-розробка", level="intermediate", teacher="Олександр Панченко", hours=40)
<Course: Django: веб-розробка>
```

Те, що у виводі видно назву курсу, а не `Course object (2)`, заслуга методу `__str__` з кроку 1.

### 3.2. Read: прочитати записи

```python
>>> Course.objects.count()
2
>>> Course.objects.all()
<QuerySet [<Course: QA: основи тестування>, <Course: Django: веб-розробка>]>
>>> Course.objects.get(slug="django-web")
<Course: Django: веб-розробка>
```

`get()` повертає **один об'єкт** і чекає, що він єдиний. Дві помилки, які варто знати:

```python
>>> Course.objects.get(slug="nope")
Traceback (most recent call last):
  ...
courses.models.Course.DoesNotExist: Course matching query does not exist.
>>> Course.objects.get(teacher="Олександр Панченко")
Traceback (most recent call last):
  ...
courses.models.Course.MultipleObjectsReturned: get() returned more than one Course -- it returned 2!
```

`DoesNotExist` означає «не знайдено», `MultipleObjectsReturned` означає «знайдено кілька». Саме цю першу помилку у `view` ми замінюємо на `get_object_or_404` (крок 5). Коли потрібен **список**, використовуємо `filter()`.

### 3.3. Фільтрація, сортування, вибірка

```python
>>> Course.objects.filter(level="beginner")
<QuerySet [<Course: QA: основи тестування>]>
>>> Course.objects.exclude(level="beginner")
<QuerySet [<Course: Django: веб-розробка>]>
>>> Course.objects.filter(title__icontains="django")
<QuerySet [<Course: Django: веб-розробка>]>
>>> Course.objects.filter(hours__gte=30)
<QuerySet [<Course: Django: веб-розробка>]>
>>> Course.objects.order_by("-hours")
<QuerySet [<Course: Django: веб-розробка>, <Course: QA: основи тестування>]>
>>> Course.objects.order_by("-hours").first()
<Course: Django: веб-розробка>
>>> Course.objects.values_list("title", flat=True)
<QuerySet ['QA: основи тестування', 'Django: веб-розробка']>
>>> Course.objects.filter(slug="nope").exists()
False
```

Умови записуються як `поле__оператор=значення` (подвійне підкреслення):

| Запис | Що означає | SQL-аналог |
| --- | --- | --- |
| `level="beginner"` | дорівнює | `WHERE level = 'beginner'` |
| `title__icontains="django"` | містить, без урахування регістру | `LIKE '%django%'` |
| `hours__gte=30` | більше або дорівнює (`gt`, `lt`, `lte` теж є) | `hours >= 30` |
| `hours__range=(20, 30)` | у діапазоні | `BETWEEN 20 AND 30` |
| `title__startswith="Django"` | починається з | `LIKE 'Django%'` |
| `deadline__isnull=True` | значення порожнє | `IS NULL` |

`-hours` у `order_by` означає «за спаданням». `values_list(..., flat=True)` дає просто список значень без кортежів.

### 3.4. Update: змінити запис

Два способи: змінити об'єкт і викликати `save()`, або виконати масове `update()` одним запитом.

```python
>>> c = Course.objects.get(slug="django-web")
>>> c.hours = 42
>>> c.save()
>>> Course.objects.filter(slug="django-web").update(hours=40)
1
```

`update()` повертає кількість змінених рядків. Він не викликає `save()` і працює для всіх записів вибірки одразу.

### 3.5. Delete: видалити запис

```python
>>> tmp = Course.objects.create(slug="tmp", title="Тимчасовий", teacher="X", hours=1)
>>> tmp.delete()
(1, {'courses.Course': 1})
```

У відповіді Django повідомляє, скільки рядків і з яких таблиць видалено. Видалення через `Course.objects.filter(...).delete()` працює так само для цілої вибірки.

### 3.6. Обмеження бази діють і з Python

Поле `slug` ми оголосили як `unique=True`. Спроба створити дубль не пройде:

```python
>>> Course.objects.create(slug="qa-basics", title="Дубль", teacher="X", hours=1)
Traceback (most recent call last):
  ...
django.db.utils.IntegrityError: UNIQUE constraint failed: courses_course.slug
```

`IntegrityError` повідомляє, що порушено обмеження цілісності. Це відповідь бази, а не Django: гарантія унікальності живе в самій таблиці (ми бачили `UNIQUE` у SQL з кроку 2).

Коли потрібно «знайти або створити» (щоб не отримати цієї помилки), є `get_or_create`:

```python
>>> Course.objects.get_or_create(slug="qa-basics", defaults={"title": "Не буде застосовано", "teacher": "X", "hours": 1})
(<Course: QA: основи тестування>, False)
```

Перший елемент кортежу — об'єкт, другий — чи створено його щойно (`False`: вже існував, тож `defaults` проігноровано).

### 3.7. QuerySet ледачий

`QuerySet` не звертається до бази, поки результат не знадобиться. Перевіримо:

```python
>>> from django.db import connection, reset_queries
>>> reset_queries()
>>> qs = Course.objects.filter(level="beginner")
>>> len(connection.queries)
0
>>> list(qs)
[<Course: QA: основи тестування>]
>>> len(connection.queries)
1
>>> list(qs)
[<Course: QA: основи тестування>]
>>> len(connection.queries)
1
```

Створення `qs` не зробило жодного запиту (**лічильник 0**). Запит виконався, коли ми «зажадали» дані (`list(qs)`). Повторне читання того самого `qs` нового запиту не створило: результат уже збережений у самому об'єкті. (Лічильник `connection.queries` працює лише при `DEBUG = True`.)

Побачити SQL будь-якого запиту можна так:

```python
>>> print(Course.objects.filter(level="beginner").query)
SELECT "courses_course"."id", "courses_course"."slug", ... FROM "courses_course" WHERE "courses_course"."level" = beginner
```

(У `print` значення показано без лапок, лише для читання; у справжньому запиті воно параметризоване.)

### 3.8. Увага: `icontains` і кирилиця в SQLite

```python
>>> Course.objects.filter(title__icontains="основи").count()
1
>>> Course.objects.filter(title__icontains="ОСНОВИ").count()
0
>>> Course.objects.filter(title__icontains="DJANGO").count()
1
```

На SQLite пошук без урахування регістру працює лише для латиниці. Для кирилиці регістр враховується (на PostgreSQL такої проблеми немає). Для навчального проєкту це знати достатньо: у пошуку вводьте назву так, як вона записана.

**Показати:** весь сеанс у терміналі, особливо `DoesNotExist`, `IntegrityError` і лічильник запитів. Закомітити цей крок нема чого: код не змінювався, лише база (файл `db.sqlite3` у git не йде).

## Крок 4. Адмінка: керуємо даними мишею

Мета кроку: отримати готовий інтерфейс для додавання та редагування курсів без жодного рядка HTML. Адмінка вбудована в Django, вона вже підключена в `INSTALLED_APPS` та в `lms/urls.py` (`path("admin/", ...)`).

### 4.1. Створити адміністратора

```bash
python manage.py createsuperuser
```

Команда запитає ім'я користувача, email (можна пропустити) і пароль двічі. Пароль під час введення не відображається, це нормально. Для навчання можна обрати простий пароль, Django попередить, що він слабкий, і дозволить продовжити.

### 4.2. Зареєструвати модель

Адмінка показує лише ті моделі, які ви в неї додали. У `courses/admin.py`:

```python
from django.contrib import admin

from .models import Course

admin.site.register(Course)
```

Запустіть сервер, відкрийте `http://127.0.0.1:8000/admin/`, увійдіть. У розділі «Courses» є посилання «Додати». Створіть третій курс із даних `data.py`:

| Поле | Значення |
| --- | --- |
| Slug | `sql-postgres` |
| Title | `SQL та PostgreSQL` |
| Level | Початковий |
| Teacher | `Олександр Панченко` |
| Hours | `20` |
| Is new | не відмічено |
| Description | `SELECT, JOIN, DML та транзакції на реальній базі PostgreSQL.` |

Натисніть «Зберегти»: у списку з'явиться запис, названий за `__str__`. Це той самий `INSERT`, який ви робили в shell, тільки через форму.

Два моменти, на які варто звернути увагу:

- форма побудована з полів моделі. Для `level` Django сам зробив випадаючий список із `choices`, для `is_new` прапорець, для `description` велике текстове поле;
- форма відмовиться зберегти порожній `title` чи `hours`, а також повторний `slug` (це перевірка на `unique=True`).

### 4.3. Налаштувати відображення

Список із самих назв зручний лише поки курсів три. Замініть `courses/admin.py` на версію з класом налаштувань:

```python
from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "teacher", "hours", "is_new")
    list_filter = ("level", "is_new")
    search_fields = ("title", "teacher")
    prepopulated_fields = {"slug": ("title",)}
```

| Параметр | Що робить |
| --- | --- |
| `list_display` | які стовпці показати в списку |
| `list_filter` | панель фільтрів праворуч |
| `search_fields` | поле пошуку над списком; шукає за вказаними полями |
| `prepopulated_fields` | слово `slug` на формі заповнюється з `title` автоматично, коли ви вводите назву |

Декоратор `@admin.register(Course)` робить те саме, що `admin.site.register(Course)`, але разом із класом налаштувань. Старий рядок із `admin.site.register` при цьому треба прибрати: двічі зареєструвати одну модель не можна (`AlreadyRegistered`).

Оновіть сторінку адмінки: з'явилися стовпці, фільтри та пошук.

**Важливо.** Адмінка призначена для співробітників, які керують вмістом, а не для відвідувачів сайту. Звичайним користувачам ми будемо робити окремі сторінки та форми.

**Показати:** додати курс через форму, показати фільтр за рівнем і пошук за словом `Django`, показати, як `slug` заповнюється сам.

```bash
git add . && git commit -m "Крок 4: адмінка для Course"
```

## Крок 5. Модель у view і шаблоні: сторінки показують дані з бази

Мета кроку: щоб каталог і сторінка курсу брали дані з бази, а не зі словників у `data.py`. Переходимо поступово: сторінки, які ще не готові, продовжують читати `data.py`, і сайт увесь час працює.

### 5.1. Заповнити базу: команда seed\_demo

Не вводити ж усі курси руками. Файл `data.py` вже містить готові дані, тож напишемо **власну команду** `manage.py`, яка перенесе їх у базу. Створіть структуру папок із порожніми файлами `__init__.py`:

```text
courses/
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── seed_demo.py
```

Файл `seed_demo.py`:

```python
from django.core.management.base import BaseCommand

from courses.data import COURSES
from courses.models import Course

LEVELS = {"Початковий": "beginner", "Середній": "intermediate", "Просунутий": "advanced"}


class Command(BaseCommand):
    help = "Заповнює базу демо-даними з courses/data.py (можна запускати повторно)"

    def handle(self, *args, **options):
        created = updated = 0
        for item in COURSES:
            course, was_created = Course.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "level": LEVELS[item["level"]],
                    "teacher": item["teacher"],
                    "hours": item["hours"],
                    "is_new": item["is_new"],
                    "description": item["description"],
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Курси: створено {created}, оновлено {updated}"))
```

Нова для вас тут функція `update_or_create`: шукає запис за `slug`; якщо знайшла, оновлює поля з `defaults`, якщо ні, створює новий. Тому команду можна запускати скільки завгодно разів і не отримати дублів. Це стандартний прийом для початкових даних. Словник `LEVELS` перетворює підписи з `data.py` («Початковий») на значення, які зберігає база (`beginner`).

```bash
python manage.py seed_demo
```

```text
Курси: створено 0, оновлено 3
```

У вас рядок може відрізнятися: якщо ви не додавали курс «SQL та PostgreSQL» вручну в адмінці, команда напише `створено 1, оновлено 2`. Другий запуск покаже `створено 0, оновлено 3`. Усе це нормально.

### 5.2. View читають базу

У `courses/views.py` перші три функції переходять на ORM (`lesson_detail` і `dashboard` лишаються як були, вони ще читають `data.py`):

```python
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .data import COURSES, STUDENT, get_course
from .models import Course


def course_list(request):
    query = request.GET.get("q", "").strip()
    courses = Course.objects.all()
    if query:
        courses = courses.filter(title__icontains=query)
    context = {"courses": courses, "query": query}
    return render(request, "courses/course_list.html", context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, "courses/course_detail.html", {"course": course})


def home(request):
    context = {
        "featured": Course.objects.all()[:2],
        "courses_count": Course.objects.count(),
    }
    return render(request, "courses/home.html", context)
```

Що змінилося порівняно із заняттям 39:

- `COURSES` (список словників) замінено на `Course.objects.all()`: шаблон отримує `QuerySet`, а не список;
- пошук тепер робить `filter(title__icontains=query)` у базі, а не перебирає список у Python;
- `get_object_or_404(Course, slug=slug)` робить `get()` і сам піднімає `Http404`, якщо запису немає. Ручна перевірка `if course is None` більше не потрібна;
- `[:2]` на `QuerySet` перетворюється на `LIMIT 2` в SQL;
- `Course.objects.count()` рахує на боці бази, не завантажуючи рядки.

### 5.3. Шаблони: що ламається, коли дані стають об'єктами

Шаблони майже не змінюються, бо `{{ course.title }}` однаково працює і для словника, і для об'єкта. Але є три місця, де потрібні правки.

**1. Рівень курсу.** У базі лежить `beginner`, а не «Початковий». Якщо залишити `{{ course.level }}`, на сторінці з'явиться англійське слово. Для `choices` Django генерує метод `get_level_display`. У `includes/course_card.html` та `course_detail.html`:

```html
{# було #}
{{ course.level }}
{# стало #}
{{ course.get_level_display }}
```

Метод у шаблоні викликаємо без дужок, як і раніше.

**2. Кількість уроків** (`{{ course.lessons|length }}` у картці, список уроків у `course_detail.html`, лічильник «Уроків» на головній). Моделі `Lesson` ще немає, тому ці місця **тимчасово прибираємо**:

- у `includes/course_card.html` видаліть `  · {{ course.lessons|length }} уроків `;
- у `course_detail.html` видаліть блок від `<h2>Програма курсу</h2>` до `</ol>`;
- у `home.html` видаліть `  · Уроків: <strong>{{ lessons_count }}</strong> `.

На кроці 6 ми поверне їх уже з бази. Якби ми залишили `{{ course.lessons|length }}`, помилки б не було: Django мовчки підставив би порожнє значення.

**3. Нічого не змінюємо** у `course_list.html`, `lesson_detail.html` та `dashboard.html`: вони працюють з атрибутами `slug`, `title`, `description`, що є і в об'єкта.

### 5.4. Показати

Перезапустіть сервер і відкрийте:

- `/courses/`: три курси вже з бази, у карток рівень українською, значок «Новий» є лише в QA;
- `/courses/?q=sql`: один курс. Спробуйте `q=django`: теж працює;
- `/courses/qa-basics/`: сторінка курсу (поки без програми);
- `/courses/nope/`: 404 (спрацював `get_object_or_404`);
- `/`: на головній тепер «Курсів: 3» без уроків;
- `/courses/django-web/lessons/2/` та `/dashboard/`: працюють як раніше, бо ще читають `data.py`.

Можна додати четвертий курс в адмінці й одразу побачити його в каталозі: дані справді з бази.

**Запитання до групи:** що буде, якщо зараз у адмінці змінити назву курсу? А якщо змінити її у файлі `data.py`? (Відповідь: на сторінках з бази зміниться лише перше. `data.py` тепер потрібен тільки команді `seed_demo` та ще не переведеним сторінкам.)

```bash
git add . && git commit -m "Крок 5: курси читаються з бази"
```

## Крок 6. Друга модель Lesson і зв'язок ForeignKey

Мета кроку: повернути уроки, але вже як окрему таблицю, пов'язану з курсом. Один курс має багато уроків, це зв'язок «один до багатьох».

### 6.1. Модель Lesson

Додайте в кінець `courses/models.py`:

```python
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    minutes = models.PositiveSmallIntegerField()
    summary = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(fields=["course", "order"], name="unique_lesson_order_per_course"),
        ]

    def __str__(self):
        return f"{self.course.title}: {self.order}. {self.title}"
```

Що тут нового:

- `ForeignKey(Course, ...)` додає в таблицю урок колонку `course_id`, яка вказує на курс. Так виглядає зв'язок «багато уроків до одного курсу».
- `on_delete=models.CASCADE` відповідає на питання «що робити з уроками, коли видалили курс?». `CASCADE` означає видалити й уроки. Аргумент обов'язковий: без нього Django не запуститься. Інші варіанти: `PROTECT` (заборонити видалення курсу з уроками) і `SET_NULL` (залишити урок без курсу, потрібен `null=True`).
- `related_name="lessons"` дає зворотний доступ: `course.lessons` повертає уроки курсу. Саме це ім'я ми використовували в шаблонах із `data.py` (`course.lessons`), тому шаблони майже не доведеться міняти.
- `UniqueConstraint` на пару `(course, order)` забороняє двох уроків з однаковим номером в одному курсі. Це правило живе в базі, а не лише в Python.
- `Meta.ordering = ["order"]` сортує уроки за номером за замовчуванням.

Якщо забути `on_delete`, `makemigrations` одразу скаже:

```text
TypeError: ForeignKey.__init__() missing 1 required positional argument: 'on_delete'
```

### 6.2. Міграція

Той самий цикл, що й на кроці 2:

```bash
python manage.py makemigrations
python manage.py migrate
```

```text
Migrations for 'courses':
  courses/migrations/0002_lesson.py
    + Create model Lesson
```

```text
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, courses, sessions
Running migrations:
  Applying courses.0002_lesson... OK
```

У папці `migrations` тепер два файли: `0001_initial.py` і `0002_lesson.py`. Другий залежить від першого. Так історія бази росте разом із моделями.

### 6.3. Уроки в адмінці: inline

Уроки логічно редагувати на сторінці курсу. Для цього в `courses/admin.py` додайте inline:

```python
from django.contrib import admin

from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "teacher", "hours", "is_new")
    list_filter = ("level", "is_new")
    search_fields = ("title", "teacher")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]
```

У формі курсу з'явилася таблиця «Lessons», де можна додавати уроки рядок за рядком. `extra = 1` показує один порожній рядок.

### 6.4. Заповнити уроки через seed

У `seed_demo.py` імпортуйте `Lesson` (`from courses.models import Course, Lesson`) і додайте в цикл по курсах, одразу після рядків `if was_created: ... else: ...`, ще один цикл:

```python
            for number, lesson in enumerate(item["lessons"], start=1):
                Lesson.objects.update_or_create(
                    course=course,
                    order=number,
                    defaults={
                        "title": lesson["title"],
                        "minutes": lesson["minutes"],
                        "summary": lesson["summary"],
                    },
                )
```

```bash
python manage.py seed_demo
```

```text
Курси: створено 0, оновлено 3
```

Рядок про курси такий самий, бо лічильник рахує лише курси. Уроки створилися тихо, їх перевіримо в shell.

### 6.5. Зв'язок у shell

```bash
python manage.py shell
```

```python
>>> from courses.models import Course, Lesson
>>> course = Course.objects.get(slug="django-web")
>>> course.lessons.all()
<QuerySet [<Lesson: Django: веб-розробка: 1. Маршрутизація та представлення>, <Lesson: Django: веб-розробка: 2. Шаблони та статичні файли>, <Lesson: Django: веб-розробка: 3. Моделі та ORM>, <Lesson: Django: веб-розробка: 4. Форми>]>
>>> course.lessons.count()
4
>>> course.lessons.first().title
'Маршрутизація та представлення'
>>> lesson = Lesson.objects.get(course=course, order=2)
>>> lesson.course
<Course: Django: веб-розробка>
>>> lesson.course.title
'Django: веб-розробка'
```

Зв'язок працює в обидва боки: від курсу до уроків (`course.lessons`) і від уроку до курсу (`lesson.course`).

Тепер найцікавіше: **подвійне підкреслення `__` проходить через зв'язок**.

```python
>>> Lesson.objects.filter(course__slug="django-web")
<QuerySet [<Lesson: Django: веб-розробка: 1. ...>, ... 4 уроки]>
>>> Lesson.objects.filter(course__level="beginner").count()
5
>>> Course.objects.filter(lessons__minutes__gt=75).distinct()
<QuerySet [<Course: Django: веб-розробка>]>
```

- `course__slug` означає «поле `slug` у пов'язаного курсу». Django сам зробить `JOIN`.
- `lessons__minutes__gt` іде в протилежний бік: від курсу до його уроків. Курс потрапляє у вибірку, якщо є хоча б один урок довший за 75 хвилин. `distinct()` потрібен, щоб курс з кількома такими уроками не повторювався.

Створення і видалення через зв'язок:

```python
>>> course.lessons.create(title="Тестовий", minutes=5, order=99)
<Lesson: Django: веб-розробка: 99. Тестовий>
>>> Lesson.objects.filter(order=99).delete()
(1, {'courses.Lesson': 1})
```

`course.lessons.create(...)` сам підставляє `course=course`. А `delete()` повертає кортеж: скільки об'єктів видалено і по моделях.

Нарешті, перевірте обмеження унікальності. Спроба створити другий урок з номером 1 в тому ж курсі:

```python
>>> Lesson.objects.create(course=course, title="Дубль", minutes=1, order=1)
Traceback (most recent call last):
  ...
django.db.utils.IntegrityError: UNIQUE constraint failed: courses_lesson.course_id, courses_lesson.order
```

Це спрацювала саме база даних, а не Python. Тому правило надійне навіть тоді, коли дані потрапляють в обхід вашого коду.

### 6.6. Повернути уроки на сторінки

На кроці 5 ми тимчасово прибрали уроки з шаблонів. Тепер повертаємо їх, уже з бази.

**Картка курсу** (`includes/course_card.html`): повертаємо лічильник уроків:

```html
<p class="muted">{{ course.get_level_display }} · {{ course.hours }} год · уроків: {{ course.lessons.count }}</p>
```

**Сторінка курсу** (`course_detail.html`): повертаємо програму:

```html
<ol class="lessons">
    {% for lesson in course.lessons.all %}
    <li>
        <a href="{% url 'lesson_detail' course.slug lesson.order %}">{{ lesson.title }}</a>
        <span class="muted">{{ lesson.minutes }} хв</span>
    </li>
    {% endfor %}
</ol>
```

**Головна** (`home.html`): повертаємо лічильник:

```html
<p class="stats">Курсів: <strong>{{ courses_count }}</strong> · Уроків: <strong>{{ lessons_count }}</strong></p>
```

У `views.py` імпортуйте `Lesson` і оновіть `home` та `lesson_detail`:

```python
from .models import Course, Lesson


def home(request):
    context = {
        "featured": Course.objects.all()[:2],
        "courses_count": Course.objects.count(),
        "lessons_count": Lesson.objects.count(),
    }
    return render(request, "courses/home.html", context)


def lesson_detail(request, slug, number):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(course.lessons, order=number)
    context = {
        "course": course,
        "lesson": lesson,
        "number": number,
        "prev_number": number - 1 if number > 1 else None,
        "next_number": number + 1 if course.lessons.filter(order=number + 1).exists() else None,
    }
    return render(request, "courses/lesson_detail.html", context)
```

Зверніть увагу на `get_object_or_404(course.lessons, order=number)`: першим аргументом можна передати не лише модель, а й менеджер зв'язку. Тоді пошук іде серед уроків саме цього курсу, а неіснуючий номер дає 404.

### 6.7. Пастка: `courses.Lesson.None`

У шаблоні легко написати:

```html
{{ course.lessons }}
```

На сторінці побачите `courses.Lesson.None`. Помилки немає, Django просто вивів менеджер зв'язку, а не список. Потрібно додати `.all` для списку або `.count` для кількості:

```html
{{ course.lessons.all }}   {# уроки #}
{{ course.lessons.count }} {# кількість #}
```

### 6.8. Показати

- `/courses/django-web/`: програма курсу з чотирма уроками з бази;
- `/courses/django-web/lessons/2/`: сторінка уроку з навігацією;
- `/courses/django-web/lessons/5/`: 404, бо такого номера немає;
- `/`: на головній знову показано кількість уроків.

Перейдіть в адмінку, відкрийте курс і додайте п'ятий урок у таблиці. Оновіть сторінку курсу: він з'явився.

**Запитання до групи:** чому в `Lesson.objects.filter(course__slug="django-web")` ми пишемо `course__slug`, а не `course.slug`? (Відповідь: у запиті до бази крапка не працює, це Python-синтаксис. Подвійне підкреслення є мовою ORM для переходу через зв'язок і для лукапів.)

```bash
git add . && git commit -m "Крок 6: модель Lesson і ForeignKey"
```

## Крок 7. Змінюємо модель, коли в базі вже є дані

Мета кроку: пережити те, що в реальному проєкті буває щотижня: у моделі з'являються нові поля, а в базі вже лежать дані. Додаємо до курсу два поля: `is_published` (чи показувати курс на сайті) і `created_at` (коли створено). Також задаємо порядок за замовчуванням.

### 7.1. Змінити модель

У `Course` додайте два поля після `description` і клас `Meta`:

```python
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
```

- `default=True` потрібен, щоб існуючі курси отримали значення в новій колонці;
- `auto_now_add=True` сам ставить поточний час при створенні запису;
- `Meta.ordering = ["title"]` сортує курси за назвою в усіх запитах, де не вказано інше.

Закінчіть правку **і не запускайте міграцію**. Спершу подивимось, що буде, якщо про неї забути.

### 7.2. Помилка «забули мігрувати»

У `views.py` змініть відбір курсів на опублікованих (у всіх чотирьох місцях, де є `Course.objects` або `get_object_or_404(Course, ...)`):

```python
courses = Course.objects.filter(is_published=True)
course = get_object_or_404(Course, slug=slug, is_published=True)
```

У списку `home` це виглядає так:

```python
"featured": Course.objects.filter(is_published=True)[:2],
"courses_count": Course.objects.filter(is_published=True).count(),
```

Оновіть `/courses/`. Замість сторінки отримаєте помилку:

```text
django.db.utils.OperationalError: no such column: courses_course.is_published
```

Що це означає: **Python-код уже знає про поле, а таблиця в базі ще ні**. Модель змінили, але міграцію не застосували. Це найчастіша помилка з базою в Django. Правило: після кожної правки `models.py` йде пара `makemigrations` і `migrate`.

Перевірте стан перед виправленням:

```bash
python manage.py showmigrations courses
```

```text
courses
 [X] 0001_initial
 [X] 0002_lesson
```

Нової міграції в списку немає: її ще не створили.

### 7.3. Створити міграцію з ненульовим полем

Запустіть тільки перевірку, що зміниться:

```bash
python manage.py makemigrations --check --dry-run
```

```text
Migrations for 'courses':
  courses/migrations/0003_alter_course_options_course_created_at_and_more.py
    ~ Change Meta options on course
    + Add field created_at to course
    + Add field is_published to course
```

Прапорець `--dry-run` нічого не створює, а `--check` повертає код помилки, якщо міграції потрібні (це зручно в CI). Тепер справжня команда:

```bash
python manage.py makemigrations
```

Django зупиниться і запитає:

```text
It is impossible to add the field 'created_at' with 'auto_now_add=True' to course without providing a default. This is because the database needs something to populate existing rows.
 1) Provide a one-off default now which will be set on all existing rows
 2) Quit and manually define a default value in models.py.
Select an option:
```

Поле `created_at` не може бути порожнім (`NOT NULL`), а в базі вже є три курси. Що записати в існуючі рядки? Django просить вас вирішити. Оберіть `1`, а на наступний запит просто натисніть Enter:

```text
[default: timezone.now] >>>
```

Усі існуючі курси отримають час міграції як дату створення. Результат:

```text
Migrations for 'courses':
  courses/migrations/0003_alter_course_options_course_created_at_and_more.py
    ~ Change Meta options on course
    + Add field created_at to course
    + Add field is_published to course
```

Відкрийте новий файл міграції, він читається як звичайний Python:

```python
class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_lesson"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="course",
            options={"ordering": ["title"]},
        ),
        migrations.AddField(
            model_name="course",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="course",
            name="is_published",
            field=models.BooleanField(default=True),
        ),
    ]
```

Три операції: змінити параметри моделі, додати `created_at`, додати `is_published`. Ланцюг `dependencies` гарантує порядок: 0003 виконається тільки після 0002. Файл міграції ви **комітите в git** разом з моделлю.

### 7.4. Подивитися SQL перед застосуванням

```bash
python manage.py sqlmigrate courses 0003
```

```text
BEGIN;
--
-- Change Meta options on course
--
-- (no-op)
--
-- Add field created_at to course
--
-- Add field is_published to course
...
COMMIT;
```

(Скорочено.) Звертаємо увагу на два факти.

- `Meta.ordering` не змінює таблицю: напис `(no-op)` означає, що SQL не потрібен. Порядок записує лише Django у своїх запитах.
- У SQLite додавання колонки виконується так: створюється нова таблиця `new__courses_course` з потрібними колонками, дані копіюються командою `INSERT ... SELECT`, стара таблиця видаляється (`DROP TABLE`), нова перейменовується. У `INSERT ... SELECT` ви побачите значення `'2026-...'` для `created_at` і `1` для `is_published`: це ті самі «значення для існуючих рядків». У PostgreSQL це було б простіше (`ALTER TABLE ... ADD COLUMN`), але ви не мусите цього знати: міграція однакова для будь-якої бази.

### 7.5. Застосувати і відкотити

```bash
python manage.py migrate
```

```text
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, courses, sessions
Running migrations:
  Applying courses.0003_alter_course_options_course_created_at_and_more... OK
```

Сторінка `/courses/` знову працює. Тепер **відкат**: міграції можна скасувати, вказавши ім'я попередньої.

```bash
python manage.py migrate courses 0002
```

```text
Operations to perform:
  Target specific migration: 0002_lesson, from courses
Running migrations:
  Rendering model states... DONE
  Unapplying courses.0003_alter_course_options_course_created_at_and_more... OK
```

```bash
python manage.py showmigrations courses
```

```text
courses
 [X] 0001_initial
 [X] 0002_lesson
 [ ] 0003_alter_course_options_course_created_at_and_more
```

Порожні квадратні дужки означають, що міграцію скасовано: колонки `created_at` та `is_published` зникли з таблиці разом зі своїми даними. Поверніть усе назад:

```bash
python manage.py migrate
```

```text
Applying courses.0003_alter_course_options_course_created_at_and_more... OK
```

**Важливе застереження:** відкат видаляє дані, які були лише в цих колонках. У навчальній базі це не страшно, у робочій відкат потребує обережності.

### 7.6. Пов'язані налаштування полів: null, blank, default

Замість абстрактної теорії, ось три налаштування, які плутають найчастіше, на прикладах з нашого проєкту.

| Налаштування | Що означає | Приклад |
| --- | --- | --- |
| `null=True` | У **базі** значення може бути `NULL` | `deadline` у записі про вступ на курс (крок 8) |
| `blank=True` | У **формі** (адмінка) поле можна лишити порожнім | `description`, `summary` |
| `default=...` | Значення, яке підставиться, якщо його не вказали | `is_new=False`, `is_published=True` |

Запам'ятайте так: `null` стосується **бази даних**, `blank` стосується **перевірки форми**. Для текстових полів (`CharField`, `TextField`) використовуйте `blank=True` **без** `null=True`: порожній рядок `""` уже означає «нічого немає», а два способи «порожнього» лише плутають. `null=True` потрібен переважно числам, датам і зв'язкам, де `""` не підходить.

### 7.7. Показати в shell і на сайті

```bash
python manage.py shell
```

```python
>>> from courses.models import Course
>>> Course.objects.values_list('title', flat=True)
<QuerySet ['Django: веб-розробка', 'QA: основи тестування', 'SQL та PostgreSQL']>
>>> Course.objects.values_list('title', 'created_at')[:1]
<QuerySet [('Django: веб-розробка', datetime.datetime(2026, 11, 2, 17, 15, 52, 670229, tzinfo=datetime.timezone.utc))]>
```

Курси відсортовані за назвою (спрацювала `Meta.ordering`), `created_at` заповнено. У вас дата і час будуть інші.

Прихуємо курс з каталогу:

```python
>>> c = Course.objects.get(slug="sql-postgres")
>>> c.is_published = False
>>> c.save()
>>> Course.objects.filter(is_published=True).count()
2
```

У `/courses/` тепер два курси, а за адресою `/courses/sql-postgres/` буде 404: `get_object_or_404(..., is_published=True)` не знаходить прихований курс. Поверніть усе назад:

```python
>>> c.is_published = True
>>> c.save()
>>> Course.objects.filter(is_published=True).count()
3
```

У адмінці додайте `is_published` у `list_display`, щоб бачити статус у списку:

```python
list_display = ("title", "level", "teacher", "hours", "is_new", "is_published")
```

Це перший приклад того, як `save()` пише зміни в базу: ми змінили атрибут об'єкта, і лише `save()` перетворив це на `UPDATE`.

**Запитання до групи:** чому нова колонка `is_published` не потребувала жодного питання від Django, а `created_at` потребувала? (Відповідь: у `is_published` вже є `default=True`, і Django знає, чим заповнити існуючі рядки. У `created_at` значення за замовчуванням немає, тож Django питає.)

```bash
git add . && git commit -m "Крок 7: is_published, created_at, ordering"
```

## Крок 8. Student і Enrollment: зв'язок «майже багато до багатьох»

Мета кроку: перевести на базу кабінет студента (`/dashboard/`), який досі брав дані з `data.py`. У ньому є студент, курси, на які він записаний, і для кожного курсу — прогрес і дедлайн.

### 8.1. Подумайте, який зв'язок потрібен

Студент може навчатися на кількох курсах, а на одному курсі навчається кілька студентів. Це зв'язок **«багато до багатьох»** (`ManyToMany`). Але для кожної пари «студент + курс» нам потрібні ще й додаткові дані: прогрес і дедлайн. Це не про студента і не про курс, це про **запис на курс**.

Тому робимо три моделі:

- `Student`: студент;
- `Course`: курс (вже є);
- `Enrollment`: запис «студент на курсі». Два `ForeignKey` і додаткові поля. Модель, що з’єднує дві таблиці, називається проміжною (`through`).

### 8.2. Моделі

У початку `courses/models.py` додайте імпорт валідатора:

```python
from django.core.validators import MaxValueValidator
from django.db import models
```

У `Course` додайте поле після `created_at`:

```python
    students = models.ManyToManyField("Student", through="Enrollment", related_name="courses", blank=True)
```

І в кінець файлу дві нові моделі:

```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    progress = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    deadline = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_student_course"),
        ]

    def __str__(self):
        return f"{self.student} → {self.course} ({self.progress}%)"
```

Що нове:

- `ManyToManyField(..., through="Enrollment")` каже: зв'язок студентів і курсів живе в моделі `Enrollment`. Назва моделі в рядку, бо вона описана нижче в файлі.
- `related_name="courses"` дає зворотний доступ `student.courses`.
- `MaxValueValidator(100)` не дозволить ввести у формі прогрес більше 100. Валідатори працюють на рівні форм, а не бази, тож `Enrollment.objects.create(progress=500)` все одно збереже 500.
- `deadline` з `null=True, blank=True`: у завершеного курсу дедлайну може не бути. Це той випадок для `null=True` з кроку 7: дата, де порожній рядок не підходить.
- `UniqueConstraint(student, course)`: один студент не може бути записаний на один курс двічі.
- На `EmailField(unique=True)`: два студенти з однаковою поштою неможливі.

### 8.3. Міграція

```bash
python manage.py makemigrations
python manage.py migrate
```

```text
Migrations for 'courses':
  courses/migrations/0004_student_enrollment_course_students_and_more.py
    + Create model Student
    + Create model Enrollment
    + Add field students to course
    + Create constraint unique_student_course on model enrollment
```

```text
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, courses, sessions
Running migrations:
  Applying courses.0004_student_enrollment_course_students_and_more... OK
```

У папці `migrations` тепер чотири файли. Заважте увагу: `ManyToManyField` не створює окремої таблиці, бо її роль виконує `courses_enrollment`.

### 8.4. Адмінка

У `courses/admin.py` імпортуйте `Enrollment, Student` і додайте в кінець:

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "progress", "deadline")
    list_filter = ("course",)
```

Щоб фільтрувати курси за статусом, у `CourseAdmin` можна також додати `"is_published"` у `list_filter`.

### 8.5. Дані студента через seed

У `data.py` вже є `STUDENT` і поля `progress` та `deadline` у кожному курсі. Оновіть `seed_demo.py`: імпорти вгорі, створення студента перед циклом і запис на курс в кінці циклу:

```python
from courses.data import COURSES, STUDENT
from courses.models import Course, Enrollment, Lesson, Student
```

```python
    def handle(self, *args, **options):
        student, _ = Student.objects.update_or_create(
            email=STUDENT["email"], defaults={"name": STUDENT["name"]}
        )
        created = updated = 0
        for item in COURSES:
            ...
            Enrollment.objects.update_or_create(
                student=student,
                course=course,
                defaults={"progress": item["progress"], "deadline": item["deadline"]},
            )
```

(`...` — весь код циклу зі кроку 6 без змін: створення курсу та уроків.)

```bash
python manage.py seed_demo
```

```text
Курси: створено 0, оновлено 3
```

Запустіть команду ще раз: дублів запису на курс не буде, бо `update_or_create` шукає пару `student + course`.

### 8.6. Зв'язки в shell

```bash
python manage.py shell
```

```python
>>> from courses.models import Course, Student, Enrollment
>>> student = Student.objects.get(email='olena@example.com')
>>> student
<Student: Олена Коваль>
>>> student.enrollments.all()
<QuerySet [<Enrollment: Олена Коваль → QA: основи тестування (60%)>, <Enrollment: Олена Коваль → Django: веб-розробка (25%)>, <Enrollment: Олена Коваль → SQL та PostgreSQL (100%)>]>
>>> student.courses.all()
<QuerySet [<Course: Django: веб-розробка>, <Course: QA: основи тестування>, <Course: SQL та PostgreSQL>]>
>>> student.courses.count()
3
>>> course = Course.objects.get(slug="qa-basics")
>>> course.students.all()
<QuerySet [<Student: Олена Коваль>]>
>>> course.enrollments.count()
1
```

У нашому проєкті тепер два шляхи до тих ж даних:

- `student.courses.all()` — просто курси студента (без прогресу);
- `student.enrollments.all()` — записи на курси з прогресом і дедлайном.

Для кабінету нам потрібен другий, бо прогрес живе саме там.

Фільтри по полях запису:

```python
>>> Enrollment.objects.filter(progress__lt=100).order_by('deadline')
<QuerySet [<Enrollment: Олена Коваль → QA: основи тестування (60%)>, <Enrollment: Олена Коваль → Django: веб-розробка (25%)>]>
>>> Enrollment.objects.filter(deadline__isnull=True)
<QuerySet [<Enrollment: Олена Коваль → SQL та PostgreSQL (100%)>]>
```

- `progress__lt=100` — «менше за 100» (`lt` = less than);
- `deadline__isnull=True` — дедлайну немає (в SQL це `IS NULL`).

І два обмеження унікальності:

```python
>>> Enrollment.objects.create(student=student, course=course)
Traceback (most recent call last):
  ...
django.db.utils.IntegrityError: UNIQUE constraint failed: courses_enrollment.student_id, courses_enrollment.course_id
>>> Student.objects.create(name='Другий', email='olena@example.com')
Traceback (most recent call last):
  ...
django.db.utils.IntegrityError: UNIQUE constraint failed: courses_student.email
```

### 8.7. Кабінет з бази

У `views.py` замініть імпорти та функцію `dashboard`. Імпорт `data.py` більше не потрібен:

```python
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Course, Lesson, Student
```

```python
def dashboard(request):
    student = Student.objects.first()
    if student is None:
        raise Http404("У базі немає студентів")
    enrollments = student.enrollments.select_related("course")
    context = {"student": student, "enrollments": enrollments}
    return render(request, "courses/dashboard.html", context)
```

- `Student.objects.first()` бере першого студента з бази. Тимчасово: коли буде логін, ми будемо брати поточного користувача.
- `first()` повертає `None`, якщо база порожня, тому є перевірка.
- `select_related("course")` додає курс до того ж SQL-запиту (`JOIN`). Без нього кожен `enrollment.course.title` у шаблоні окремо звертався б до бази. Деталі — на кроці 9.

У шаблоні `dashboard.html` цикл тепер йде по `enrollments`, а дані курсу беруться через `enrollment.course`:

```html
{% for enrollment in enrollments %}
    <tr>
        <td><a href="{% url 'course_detail' enrollment.course.slug %}">{{ enrollment.course.title }}</a></td>
        <td>
            <div class="bar"><span style="width: {{ enrollment.progress }}%"></span></div>
            {{ enrollment.progress }}%
        </td>
        <td>{{ enrollment.deadline|date:"d.m.Y"|default:"—" }}</td>
        <td>{% if enrollment.progress == 100 %}Завершено{% else %}У процесі{% endif %}</td>
    </tr>
{% empty %}
    <tr><td colspan="4">Ви ще не записані на жодний курс.</td></tr>
{% endfor %}
```

Замість `course.progress` тепер `enrollment.progress`, бо прогрес належить запису, а не курсу. Це і є результат проміжної моделі.

Дату редагування дедлайну виводить `date:"d.m.Y"`, а `default:"—"` покаже тире для курсу без дедлайну (`None`).

### 8.8. Показати

Оновіть `/dashboard/`:

- вітання «Вітаємо, Олена Коваль!» і пошта з бази;
- три курси з прогресом 60 %, 25 % і 100 %;
- дедлайни 20.11.2026 і 15.12.2026, для SQL — тире;
- статус «Завершено» лише у SQL.

Зайдіть у адмінку в «Enrollments», змініть прогрес QA з 60 на 80 і оновіть кабінет: цифра змінилась. Дані тепер живуть у базі і редагуються без гарної правки коду. (Наступного `seed_demo` цей прогрес знову скине на 60, бо бере значення з `data.py`.)

**Запитання до групи:** чому прогрес не можна було просто додати полем у `Course`? (Відповідь: бо у кожного студента свій прогрес на одному й тому ж курсі; це властивість пари.)

```bash
git add . && git commit -m "Крок 8: Student і Enrollment"
```

## Крок 9. Запити без зайвого: Q, aggregate, annotate, N+1 і тести

Мета кроку: навчитися рахувати дані на боці бази, побачити, скільки SQL-запитів робить сторінка, і зафіксувати поведінку тестами.

### 9.1. Складні умови: Q

Традиційний `filter(a=1, b=2)` поєднує умови через «І». Щоб написати «АБО» або «НЕ», потрібен об'єкт `Q`.

```python
>>> from django.db.models import Count, Avg, Sum, Q
>>> from courses.models import Course, Enrollment
>>> Course.objects.filter(Q(level='beginner') | Q(hours__gte=40))
<QuerySet [<Course: Django: веб-розробка>, <Course: QA: основи тестування>, <Course: SQL та PostgreSQL>]>
>>> Course.objects.filter(is_new=False).exclude(level='beginner')
<QuerySet [<Course: Django: веб-розробка>]>
```

- `Q(...) | Q(...)` — «АБО», `Q(...) & Q(...)` — «І», `~Q(...)` — «НЕ»;
- `exclude(...)` — виключити записи з умовою (видати все, крім цього).

У наших трьох курсах перший запит повернув усі три (два початкові + Django, де часу більше 40 годин). Ваш результат залежить від ваших даних.

### 9.2. Підрахунки: aggregate

`aggregate` повертає **одне значення на весь набір** (словник):

```python
>>> Course.objects.aggregate(n=Count('id'), avg_hours=Avg('hours'), total_hours=Sum('hours'))
{'n': 3, 'avg_hours': 28.0, 'total_hours': 84}
```

Це відповідає SQL-запиту `SELECT COUNT(id), AVG(hours), SUM(hours) FROM courses_course`. Ви вже робили таке в SQL.

### 9.3. Підрахунки на кожен рядок: annotate

`annotate` додає розрахункове поле **кожному об'єкту**. Приклад: кількість уроків у кожного курсу.

```python
>>> Course.objects.annotate(total=Count('lessons')).filter(total__gte=3).values_list('title', 'total')
<QuerySet [('Django: веб-розробка', 4), ('QA: основи тестування', 3)]>
>>> Course.objects.annotate(total=Count('lessons')).order_by('-total').first().title
'Django: веб-розробка'
>>> list(Course.objects.values('level').annotate(n=Count('id')).order_by('level'))
[{'level': 'beginner', 'n': 2}, {'level': 'intermediate', 'n': 1}]
```

- по новому полю `total` можна фільтрувати і сортувати;
- `values('level').annotate(...)` рахує по групах. Це SQL-запит `GROUP BY level`, близький до того, що ви писали на модулі SQL.

Різниця запам'ятається легко: **`aggregate` — одне число на все, `annotate` — число на кожен рядок**.

### 9.4. Вимірюємо: скільки SQL-запитів зробила сторінка

ORM зручний, але він може мовчки робити зайві запити. Порахуємо їх в shell (працює при `DEBUG = True`, як у нашій навчальній налаштованій базі):

```python
>>> from django.db import connection, reset_queries
>>> reset_queries()
>>> for c in Course.objects.all(): print(c.title, c.lessons.count())
Django: веб-розробка 4
QA: основи тестування 3
SQL та PostgreSQL 2
>>> len(connection.queries)
4
```

Чотири запити для трьох курсів: один на список курсів і по одному «построково» на кожен `c.lessons.count()`. Це називається **проблема N+1**: 1 запит + N запитів на N рядків. Для 3 курсів це незаважно, для 300 — вже 301 запит на одну сторінку. Тема важлива, бо саме так сайти повільнішають непомітно.

Тут три виліки.

**1. `annotate(Count(...))`**, якщо потрібна лише кількість:

```python
>>> reset_queries()
>>> for c in Course.objects.annotate(total=Count('lessons')): print(c.title, c.total)
...
>>> len(connection.queries)
1
```

**2. `select_related(...)`** для зв'язку «один до одного» або `ForeignKey` (об'єкт праворуч один). Додає `JOIN` у той же запит:

```python
>>> reset_queries()
>>> for e in Enrollment.objects.all(): print(e.course.title, e.progress)
...
>>> len(connection.queries)
4
>>> reset_queries()
>>> for e in Enrollment.objects.select_related('course'): print(e.course.title, e.progress)
...
>>> len(connection.queries)
1
```

**3. `prefetch_related(...)`** для зворотного зв'язку або `ManyToMany` (багато об'єктів). Виконує два запити і з’єднує результати в Python, тому використовується там, де потрібні самі уроки, а не лише їх кількість:

```python
>>> reset_queries()
>>> for c in Course.objects.prefetch_related('lessons'): print(c.title, len(c.lessons.all()))
...
>>> len(connection.queries)
2
```

| Випадок | Інструмент | Запитів у нашом прикладі |
| --- | --- | --- |
| Лічильник уроків у курсах | `annotate(Count(...))` | було 4, стало 1 |
| Курс у кожному записі | `select_related('course')` | було 4, стало 1 |
| Список уроків у курсах | `prefetch_related('lessons')` | було 4, стало 2 |

### 9.5. Виправляєм список курсів у проєкті

Наша сторінка `/courses/` на кроці 8 робить 4 запити (список + `{{ course.lessons.count }}` у кожній картці), головна — 5. Виправимо через `annotate`. У `views.py` додайте імпорт і поле:

```python
from django.db.models import Count
```

```python
# course_list
courses = Course.objects.filter(is_published=True).annotate(lessons_total=Count("lessons"))
```

```python
# home
"featured": Course.objects.filter(is_published=True).annotate(lessons_total=Count("lessons"))[:2],
```

У `includes/course_card.html` замініть `{{ course.lessons.count }}` на `{{ course.lessons_total }}`:

```html
<p class="muted">{{ course.get_level_display }} · {{ course.hours }} год · уроків: {{ course.lessons_total }}</p>
```

Перевірка: `/courses/` тепер робить **1** запит замість 4, а головна — **3** замість 5 (у неї ще виконуються два лічильники та список рекомендованих). Сторінка виглядає так само, а працює швидше й не залежить від кількості курсів.

Щоб бачити ці числа без shell, існують налагоджені інструменти, наприклад Django Debug Toolbar. Для навчання вистачить `connection.queries` і тесту.

### 9.6. Тести: фіксуємо поведінку

Проєкт вже зайняв багато часу, тому зафіксуємо те, що важливо: прихований курс не показується, а сторінка списку робить один запит. Відкрийте `courses/tests.py`:

```python
from django.test import TestCase
from django.urls import reverse

from .models import Course, Lesson


class CourseModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(slug="demo", title="Демо", teacher="Автор", hours=10)
        Lesson.objects.create(course=self.course, title="Перший", minutes=30, order=1)

    def test_str(self):
        self.assertEqual(str(self.course), "Демо")

    def test_lessons_relation(self):
        self.assertEqual(self.course.lessons.count(), 1)


class CourseViewTests(TestCase):
    def setUp(self):
        Course.objects.create(slug="open", title="Відкритий", teacher="А", hours=1)
        Course.objects.create(slug="hidden", title="Прихований", teacher="А", hours=1, is_published=False)

    def test_list_shows_only_published(self):
        response = self.client.get(reverse("course_list"))
        self.assertContains(response, "Відкритий")
        self.assertNotContains(response, "Прихований")

    def test_hidden_course_is_404(self):
        response = self.client.get(reverse("course_detail", args=["hidden"]))
        self.assertEqual(response.status_code, 404)

    def test_list_uses_one_query(self):
        with self.assertNumQueries(1):
            self.client.get(reverse("course_list"))
```

Запуск:

```bash
python manage.py test
```

```text
Found 5 test(s).
System check identified no issues (0 silenced).
Creating test database for alias 'default'...
.....
----------------------------------------------------------------------
Ran 5 tests in 0.038s

OK
Destroying test database for alias 'default'...
```

У вас можуть з’явитися рядки `Запит: GET ...` між крапками: це друкує middleware з заняття 39, на результат тестів воно не впливає.

Що важливо зрозуміти про тести:

- `TestCase` створює **окрему тимчасову базу** і видаляє її після запуску. Ваша `db.sqlite3` не чіпається.
- `setUp` виконується перед кожним тестом, дані кожного тесту ізольовані.
- `self.client` — вбудований «браузер»: робить запити без запуску сервера.
- `assertNumQueries(1)` валить тест, якщо запитів було більше або менше. Якщо хтось поверне `{{ course.lessons.count }}` у картку, кожна картка додасть свій запит, і тест почервоніє.

Спробуйте замінити в `views.py` тільки один рядок: зніміть `is_published=True` у `course_list`, і перший же тест покаже помилку. Тести для того й потрібні.

```bash
git add . && git commit -m "Крок 9: annotate, select_related, тести"
```

**Запитання до групи:** який інструмент вибрати, якщо у картці курсу треба показати назви всіх уроків? (Відповідь: `prefetch_related('lessons')`, бо зворотний зв'язок «багато» і потрібен список, а не лише число.)

## Довідник: поля, опції та методи

### Типи полів, які ми використали

| Поле | Для чого | Типові аргументи |
| --- | --- | --- |
| `CharField` | короткий текст | `max_length` (обов'язково), `choices` |
| `TextField` | довгий текст | `blank=True` |
| `SlugField` | частина URL без пробілів | `unique=True` |
| `EmailField` | пошта з перевіркою формату | `unique=True` |
| `PositiveSmallIntegerField` | невелике ціле число від 0 | `default`, `validators` |
| `BooleanField` | так/ні | `default` |
| `DateField`, `DateTimeField` | дата, дата і час | `null`, `blank`, `auto_now_add` |
| `ForeignKey` | «багато до одного» | `on_delete` (обов'язково), `related_name` |
| `ManyToManyField` | «багато до багатьох» | `through`, `related_name` |

### Спільні опції полів

| Опція | Що робить |
| --- | --- |
| `null=True` | у базі може бути `NULL` |
| `blank=True` | у формі поле необов'язкове |
| `default=...` | значення за замовчуванням |
| `unique=True` | значення не може повторюватись у таблиці |
| `choices=...` | обмежений набір значень; додає метод `get_<поле>_display()` |
| `validators=[...]` | додаткові перевірки (на рівні форми, не бази) |
| `auto_now_add=True` | час створення, ставиться один раз |

### on\_delete

| Значення | Що стається, коли видаляють «батьківський» об'єкт |
| --- | --- |
| `CASCADE` | видаляються й пов'язані записи |
| `PROTECT` | видалення заборонено, поки є пов'язані записи |
| `SET_NULL` | посилання стає `NULL` (потрібен `null=True`) |

### Команди manage.py для бази

| Команда | Що робить |
| --- | --- |
| `makemigrations` | створює файл міграції за змінами моделей |
| `makemigrations --check --dry-run` | показує, чи є зміни, нічого не створює |
| `sqlmigrate courses 0001` | показує SQL міграції |
| `migrate` | застосовує незастосовані міграції |
| `migrate courses 0002` | відкатує до вказаної міграції |
| `showmigrations` | показує, що застосовано (`[X]`) і що ні (`[ ]`) |
| `shell` | інтерактивна консоль Python з уже налаштованим Django |
| `createsuperuser` | створює користувача для адмінки |
| `seed_demo` | наша команда для заповнення бази |
| `test` | запускає тести на тимчасовій базі |

### Методи QuerySet

| Метод | Повертає | Приклад |
| --- | --- | --- |
| `all()` | усі записи | `Course.objects.all()` |
| `filter(...)` | записи за умовою | `filter(level="beginner")` |
| `exclude(...)` | записи без умови | `exclude(is_new=True)` |
| `get(...)` | **один** об'єкт (або помилка) | `get(slug="qa-basics")` |
| `order_by(...)` | відсортований `QuerySet` | `order_by("-hours")` |
| `first()`, `last()` | один об'єкт або `None` | `Student.objects.first()` |
| `count()` | число записів (рахує база) | `Course.objects.count()` |
| `exists()` | `True` / `False` | `filter(slug="x").exists()` |
| `values_list(...)` | кортежі значень | `values_list("title", flat=True)` |
| `create(...)` | створює і зберігає | `Course.objects.create(...)` |
| `get_or_create(...)` | `(об'єкт, чи_створено)` | `get_or_create(slug="x", defaults={...})` |
| `update_or_create(...)` | `(об'єкт, чи_створено)` | у `seed_demo` |
| `update(...)` | кількість змінених рядків | `filter(...).update(is_new=False)` |
| `delete()` | кортеж кількості видалених | `filter(order=99).delete()` |
| `annotate(...)` | додає поле кожному об'єкту | `annotate(total=Count("lessons"))` |
| `aggregate(...)` | словник з підсумками | `aggregate(Avg("hours"))` |
| `select_related(...)` | `JOIN` для `ForeignKey` | `select_related("course")` |
| `prefetch_related(...)` | 2-гий запит для «багато» | `prefetch_related("lessons")` |

### Умови в filter (lookups)

| Суфікс | Значення | Приклад |
| --- | --- | --- |
| `__exact` (за замовчуванням) | рівно | `level="beginner"` |
| `__icontains` | містить, без врахування регістру (для латиниці) | `title__icontains="sql"` |
| `__startswith` | починається з | `title__startswith="QA"` |
| `__gt`, `__gte`, `__lt`, `__lte` | більше / не менше / менше / не більше | `hours__gte=40` |
| `__in` | значення зі списку | `level__in=["beginner", "advanced"]` |
| `__range` | у діапазоні | `hours__range=(10, 30)` |
| `__isnull` | чи є `NULL` | `deadline__isnull=True` |
| `зв'язок__поле` | поле пов'язаної моделі | `course__slug="django-web"` |

**Увага до кирилиці в SQLite:** `icontains` не відрізняє великі та малі кириличні літери не завжди. Пошук `q=веб` може не знайти «Веб». Це особливість SQLite, у PostgreSQL поведінка інша.

### Cheat sheet імен у зв'язках нашого проєкту

| Що треба | Вираз |
| --- | --- |
| Уроки курсу | `course.lessons.all()` |
| Курс уроку | `lesson.course` |
| Записи на курс у студента | `student.enrollments.all()` |
| Курси студента | `student.courses.all()` |
| Студенти курсу | `course.students.all()` |
| Курс у записі | `enrollment.course` |
| У шаблоні кількість уроків | `{{ course.lessons.count }}` або `annotate` |
| У шаблоні рівень курсу | `{{ course.get_level_display }}` |

## Типові помилки та що з ними робити

Помилки видно у терміналі або у журналі сервера. Текст нижче взято з реального прогону проєкту.

| Текст помилки | Що зараз відбувається | Дія |
| --- | --- | --- |
| `OperationalError: no such table: courses_course` | міграції застосовані не до тієї бази, або їх ще не було | `python manage.py migrate`; перевірте середовище та папку запуску |
| `OperationalError: no such column: courses_course.is_published` | модель змінили, а таблиця стара | `makemigrations`, потім `migrate` |
| `Migrations for 'courses'` не з'являється; пише `No changes detected` | застосунок не в `INSTALLED_APPS`, або модель не збережена | перевірте `INSTALLED_APPS` і `models.py`; `makemigrations courses` |
| `TypeError: ForeignKey.__init__() missing 1 required positional argument: 'on_delete'` | у `ForeignKey` немає `on_delete` | додайте `on_delete=models.CASCADE` |
| `IntegrityError: UNIQUE constraint failed: courses_course.slug` | спроба створити дубль значення з `unique` | використайте `get_or_create`/`update_or_create` або змініть значення |
| `Course.DoesNotExist: Course matching query does not exist.` | `get()` нічого не знайшов | у view — `get_object_or_404`; у shell — `filter(...).first()` |
| `MultipleObjectsReturned: get() returned more than one Course -- it returned 3!` | `get()` знайшов кілька записів | уточніть умову, або `filter(...)` |
| `FieldError: Cannot resolve keyword 'titl' into field. Choices are: ...` | опечатка в імені поля | перевірте список полів у самій помилці |
| на сторінці `courses.Lesson.None` | у шаблоні `{{ course.lessons }}` без `.all` | `.all` для списку, `.count` для числа |
| у картці написано `beginner` замість «Початковий» | у шаблоні `course.level` | `course.get_level_display` |
| пошук по кирилиці не знаходить курс | особливість SQLite з `icontains` | шукайте з тим же регістром; у PostgreSQL працює інакше |
| міграція питає значення за замовчуванням | нове обов'язкове поле без `default` у непорожній таблиці | додайте `default` у модель, або оберіть опцію 1 |

### Два правила на пам'ять

1. Після кожної зміни `models.py` — `makemigrations` і `migrate`.
2. Помилка «немає таблиці/колонки» завжди означає розбіжність між кодом і базою, а не помилку в шаблоні.

Якщо нічого не допомагає і база в навчальному проєкті заплуталася, можна видалити файл `db.sqlite3` і заново виконати `migrate`, `createsuperuser`, `seed_demo`. Дані з адмінки будуть втрачені, тому це варіант тільки для навчальної бази. Файли міграцій не видаляйте.

## Самоперевірка

Спершу відповідайте самі, потім перевіряйте.

1. В чому різниця між `makemigrations` і `migrate`?
2. Ви додали поле в модель і оновили сторінку. Бачите `no such column`. Що зробили не так?
3. В чому різниця між `get()` і `filter()`? Які помилки може дати `get()`?
4. Що значить `related_name="lessons"` у `ForeignKey`? Як буде виглядати доступ до уроків курсу, якщо цього параметра немає?
5. В чому різниця між `null=True` і `blank=True`? Для яких полів ви використаєте тільки `blank`?
6. Що напише шаблон, якщо в ньому `{{ course.lessons }}`? Чи буде помилка?
7. В чому різниця між `aggregate` і `annotate`?
8. Скільки запитів до бази зробить цикл `for c in Course.objects.all(): c.lessons.count()` при 10 курсах? Як це виправити?
9. Для чого ми створили окрему модель `Enrollment`, а не просто `ManyToManyField` без `through`?
10. Чи можна видалити файл міграції із папки `migrations`, якщо він вже застосований і закомічений? Чому?

### Відповіді

1. `makemigrations` створює файл з описом змін (базу не чіпає). `migrate` застосовує ці файли до бази.
2. Ви забули пару `makemigrations` і `migrate` після зміни `models.py`. Код вже знає про нове поле, а таблиця — ще ні.
3. `get()` повертає один об'єкт і кидає `DoesNotExist` (немає) або `MultipleObjectsReturned` (більше одного). `filter()` завжди повертає `QuerySet` (може бути порожнім).
4. Це ім'я зворотного зв'язку: `course.lessons.all()`. Без нього ім'я буде стандартне: `course.lesson_set.all()`.
5. `null=True` — у базі може бути `NULL`; `blank=True` — форма не вимагає значення. Тільки `blank` — для текстових полів (`description`, `summary`).
6. Помилки немає. Виведе дивний текст `courses.Lesson.None`, бо це менеджер зв'язку. Потрібен `.all` або `.count`.
7. `aggregate` — один підсумок на весь набір (словник). `annotate` — розрахунок на кожен об'єкт.
8. 11 запитів: один на список і по одному на кожен курс. Виправляється `annotate(total=Count('lessons'))`: один запит.
9. У кожного запису на курс є додаткові дані (прогрес, дедлайн), і їх треба десь зберігати. Звичайний `ManyToManyField` має лише пару ідентифікаторів.
10. Не можна. Це історія бази: інші міграції залежать від неї, а бази колег чи сервера вже залежать на ній. Зміни роблять новою міграцією.

## Домашнє завдання: моделі у вашому проєкті

Застосуйте те, що пройшли, у **вашому власному проєкті** (Task & Bug Manager, Expense Tracker, Service Management System або інший). Демо-LMS — це приклад, а оцінюємо ваш проєкт.

### Мінімум (обов'язково)

1. Опишіть **дві моделі**, пов'язані `ForeignKey`, для свого проєкту. Підказки:
   - Task & Bug Manager: `Project` → `Task` (або `Bug`);
   - Expense Tracker: `Category` → `Expense`;
   - Service Management System: `Client` → `ServiceRequest`.
2. У кожній моделі: мінімум 4 поля різних типів, `__str__`, `Meta.ordering`. У одному полі — `choices` (статус, пріоритет, тип).
3. Створіть міграцію, застосуйте її, закомітьте все в git (моделі + файли міграцій разом).
4. Зареєструйте моделі в адмінці з `list_display`, `list_filter` і `search_fields`.
5. Заповніть базу: мінімум 3 батьківських записи та 8 дочірніх, бажано командою `seed_demo` (або через адмінку).
6. В одній сторінці списку покажіть дані з бази через view і шаблон (як `/courses/`).

### Додатково (бажано)

- Сторінка деталей з `get_object_or_404`.
- Пошук або фільтр у списку (`?status=open`) за допомогою `filter`.
- Лічильник дочірніх записів через `annotate(Count(...))`.
- Два тести: модель (`__str__`) і сторінка списку (200 і вміст).

### Що здавати

- посилання на репозиторій з комітами по кроках;
- скріншот адмінки з даними та сторінки списку;
- запис з `shell`: три запити з виводом (один через зв'язок, один з `Q` або `exclude`, один з `annotate`).

### Якщо зависли

Підказка по завданню: щоразу, коли бачите помилку, спершу перевірте таблицю «Типові помилки» вище. Робіть коміти часто, так легше відкотитися. Повертайтеся з питаннями на наступне заняття.

## Підсумок

Що ви вмієте після цього заняття:

- описувати дані моделями: поля, `choices`, `__str__`, `Meta.ordering`, обмеження унікальності;
- створювати і застосовувати міграції, дивитися SQL, відкочувати зміни;
- рахувати дані через `shell` і адмінку;
- заповнювати базу власною командою `seed_demo`;
- пов'язувати моделі (`ForeignKey`, `ManyToManyField` через `through`) і ходити по зв'язках (`course.lessons`, `course__slug`);
- видавати дані з бази в сторінки через view і шаблон;
- будувати запити (`filter`, `exclude`, `Q`, `aggregate`, `annotate`) і не забувати про N+1 (`select_related`, `prefetch_related`);
- писати прості тести на моделі та сторінки.

**Чого ще немає в нашом проєкті (далі):** форми, щоб записувати дані зі сторінок; автентифікація (щоб кабінет показував поточного користувача, а не `Student.objects.first()`); `ListView`/`DetailView` як коротша версія тих же view; PostgreSQL замість SQLite.

**Шпаргалка в одному рядку:** змінили `models.py` → `makemigrations` → `migrate` → перевірили в `shell` або на сторінці → `git commit`.
