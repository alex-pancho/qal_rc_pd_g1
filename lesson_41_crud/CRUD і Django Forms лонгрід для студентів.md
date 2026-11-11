# CRUD і Django Forms: лонгрід для студентів

## 1. Мета і карта кроків

У занятті 40 ми створили моделі `Course`, `Lesson`, `Student`, `Enrollment` і навчилися **читати** дані (R у CRUD). Сьогодні додаємо решту: **Create, Update, Delete** для курсу — через форми Django, у тому самому проєкті `lms`.

Працюємо маленькими кроками. Після кожного кроку: щось запускаємо, бачимо результат і робимо `git commit`.

| Крок | Що робимо | Що побачимо |
| --- | --- | --- |
| 1 | Незв'язана `forms.Form`, сторінка `/courses/new/` | Форма на екрані, але кнопка «нічого не робить» |
| 2 | POST, `is_valid`, помилки, redirect | Курс створюється; дубль slug дає 500 |
| 3 | `ModelForm` | Дубль slug стає помилкою форми |
| 4 | Update: `instance=` | Форма редагування з даними |
| 5 | Delete через сторінку підтвердження | Каскад: разом з курсом зникають уроки |
| 6 | `messages` і кнопки в інтерфейсі | Банер «Курс створено» |
| 7 | `clean_*`, `clean()`, віджети, ручний рендер | Свої правила валідації |
| 8 | Тести | 14 тестів, `OK` |

Стартова точка — проєкт із заняття 40 (є `seed_demo`, 3 курси).

## 2. Ідея: GET, POST і Post/Redirect/Get

**CRUD** — чотири дії з даними: Create, Read, Update, Delete. У Django кожна — це зв'язка *URL → view → шаблон → ORM*.

**Форма** — спосіб отримати дані від користувача. Два методи:

- **GET** — «дай мені сторінку». Дані йдуть в адресі (`/courses/?q=python`). Нічого не змінює на сервері: пошук, фільтр, показ форми.
- **POST** — «ось дані, зміни щось». Дані в тілі запиту. Створення, зміна, видалення.

Одна адреса `/courses/new/` обслуговує **обидва** методи: GET показує порожню форму, POST приймає заповнену.

**Post/Redirect/Get (PRG).** Після успішного POST **ніколи не рендеримо сторінку**, а робимо `redirect`. Інакше F5 повторить POST і створить дублікат. Схема: `POST → 302 → GET /courses/<slug>/`.

**CSRF.** Кожна POST-форма має `{% csrf_token %}` — прихований токен, який доводить, що форму надіслала саме наша сторінка. Без нього Django відповість `403`.

## Крок 1. Незв'язана форма і сторінка «Новий курс»

**Теорія якраз вчасно.** `forms.Form` — клас, що описує поля форми: які вони, які в них обмеження і як підписані. Створена без даних (`CourseForm()`) форма називається **незв'язаною** (unbound): вона лише малюється.

Створюємо `courses/forms.py`:

```python
from django import forms

from .models import Course


class CourseForm(forms.Form):
    title = forms.CharField(max_length=200, label="Назва")
    slug = forms.SlugField(label="Slug (адреса)")
    level = forms.ChoiceField(choices=Course.Level.choices, label="Рівень")
    teacher = forms.CharField(max_length=100, label="Викладач")
    hours = forms.IntegerField(min_value=1, label="Годин")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Опис")
```

View у `courses/views.py` (імпорт `from .forms import CourseForm` додай угорі):

```python
def course_create(request):
    form = CourseForm()
    return render(request, "courses/course_form.html", {"form": form})
```

Шаблон `courses/templates/courses/course_form.html`:

```html
{% extends "base.html" %}

{% block title %}Новий курс{% endblock %}

{% block content %}
<h1>Новий курс</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn" type="submit">Зберегти</button>
</form>
{% endblock %}
```

Маршрут у `courses/urls.py`. **Важливо: `new/` стоїть ПЕРЕД `<slug:slug>/`**, інакше Django вирішить, що `new` — це slug курсу:

```python
path("courses/new/", views.course_create, name="course_create"),
path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
```

`{{ form.as_p }}` сам малює кожне поле в `<p>` з `<label>`, а `Course.Level.choices` стає випадним списком. У відповіді сервера:

```html
<p>
  <label for="id_hours">Годин:</label>
  <input type="number" name="hours" min="1" required id="id_hours">
</p>
```

**Покажи результат.** Відкрий `/courses/new/` — форма є. Натисни «Зберегти» з порожніми полями — браузер сам зупинить (`required`). Заповни все і відправ: сторінка просто перезавантажиться, **курс не створюється** (у базі й далі 3 курси). Чому? View ігнорує POST. Це і є наступний крок.

`git commit -m "Step 1: CourseForm and empty form page"`

## Крок 2. POST, валідація, помилки і redirect

**Теорія.** Форма з даними (`CourseForm(request.POST)`) — **зв'язана** (bound). Метод `is_valid()` запускає перевірку; якщо все гаразд, очищені й перетворені на потрібні типи дані лежать у `cleaned_data`, інакше причини — у `form.errors`.

Спробуй у `python manage.py shell`:

```python
>>> from courses.forms import CourseForm
>>> CourseForm().is_bound
False
>>> f = CourseForm({"title": "", "slug": "my course", "level": "x", "teacher": "T", "hours": "0"})
>>> f.is_bound, f.is_valid()
(True, False)
>>> for k, v in f.errors.items(): print(k, list(v))
title ["Це поле обов'язкове."]
slug ['Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.']
level ['Зробить коректний вибір, x немає серед варіантів вибору.']
hours ['Переконайтеся, що це значення більше чи дорівнює 1.']
>>> f = CourseForm({"title": "Python", "slug": "python-basics", "level": "beginner", "teacher": "Автор", "hours": "30"})
>>> f.is_valid(); f.cleaned_data
True
{'title': 'Python', 'slug': 'python-basics', 'level': 'beginner', 'teacher': 'Автор', 'hours': 30, 'description': ''}
```

Зверни увагу: `hours` у `cleaned_data` — число `30`, а не рядок `"30"`.

Тепер view. Одна функція, два сценарії:

```python
from django.shortcuts import get_object_or_404, redirect, render


def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = Course.objects.create(**form.cleaned_data)
            return redirect("course_detail", slug=course.slug)
    else:
        form = CourseForm()
    return render(request, "courses/course_form.html", {"form": form})
```

Логіка: GET → порожня форма; POST і дані невалідні → **та сама форма з даними та помилками** (її `render` в кінці); POST і валідні → зберегли і `redirect` (PRG).

> Чому не `request.POST or None`? Це працює, але порожній POST (наприклад, лише чекбокс без галочки) дає `None` — форма вважається незв'язаною і помилок не покаже. Явний `if request.method == "POST"` читається краще й не має сюрпризів.

**Покажи результат.**

1. Відправ форму з `slug` = `python basics` та `hours` = 0 (вимкни перевірку браузера або використай `novalidate`): сторінка повернеться з червоними помилками, у базі нічого нового — курсів і далі 3.
2. Відправ валідні дані (`python-qa`): відповідь `302 → /courses/python-qa/`, відкривається сторінка курсу.
3. Відправ ще раз **той самий slug**: сервер повертає `500`, у консолі:

```
django.db.utils.IntegrityError: UNIQUE constraint failed: courses_course.slug
```

У звичайній `Form` Django не знає про `unique=True` у моделі, тому помилка прилітає вже з бази. Це мотивація для кроку 3.

**Окремий експеримент про CSRF.** Закоментуй `{% csrf_token %}` і відправ форму: отримаєш сторінку `403 Forbidden`. Поверни тег назад!

Після експериментів видали тестовий курс `python-qa` (з shell: `Course.objects.filter(slug="python-qa").delete()`).

`git commit -m "Step 2: POST, validation and redirect"`

## Крок 3. ModelForm: форма з моделі

**Теорія.** Ми двічі описали одне й те саме: поля в моделі і поля у формі. `forms.ModelForm` будує форму **з моделі**: типи, `max_length`, `unique`, `choices` береться звідти. Бонус: `form.save()` сам створює об'єкт, а валідація знає про `unique`.

Переписуємо `courses/forms.py`:

```python
from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "slug", "level", "teacher", "hours", "is_new", "description"]
```

`fields` — явний список полів. Не використовуй `fields = "__all__"`: нове поле моделі автоматично потрапить у форму.

У `courses/models.py` додаємо метод, щоб `redirect` знав, куди вести (імпорт `from django.urls import reverse`):

```python
class Course(models.Model):
    ...
    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})
```

Міграція **не потрібна** — модель не змінилась у полях (`makemigrations --check` скаже `No changes detected`).

View стає коротшим:

```python
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect(course)
    else:
        form = CourseForm()
    return render(request, "courses/course_form.html", {"form": form})
```

`redirect(course)` бере `course.get_absolute_url()`.

**Покажи результат.** Відправ дубль slug (`django-web`). Тепер замість `500`:

```html
<ul class="errorlist"><li>Course з таким Slug вже існує.</li></ul>
```

Сторінка `200`, форма зберегла введене, у базі **один** курс з цим slug. Валідний POST дає `302 → /courses/python-qa/`.

Ще дві корисні речі в shell:

```python
>>> f = CourseForm({"title": "T", "slug": "t", "level": "beginner", "teacher": "A", "hours": 5})
>>> f.is_valid()
True
>>> obj = f.save(commit=False)   # об'єкт створено, але ще не в базі
>>> obj.pk
>>> obj.save(); obj.pk
6
>>> list(CourseForm().fields)
['title', 'slug', 'level', 'teacher', 'hours', 'is_new', 'description']
```

`save(commit=False)` знадобиться, коли треба дописати поле вручну (наприклад, автора) перед збереженням.

`git commit -m "Step 3: ModelForm"`

## Крок 4. Update: редагування курсу

**Теорія.** Update — це та сама форма, але з `instance=course`. Тоді вона: (1) на GET показує **поточні значення**, (2) на POST **оновлює** цей об'єкт, а не створює новий. Ніяких `initial={...}` вручну і `task.title = ...; task.save()`.

Шаблон став спільним для create і update — заголовок приходить із view:

```html
{% block title %}{{ heading }}{% endblock %}
...
<h1>{{ heading }}</h1>
```

У `course_create` додаємо `"heading": "Новий курс"` у контекст. Нова view:

```python
def course_update(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect(course)
    else:
        form = CourseForm(instance=course)
    context = {"form": form, "heading": f"Редагувати: {course.title}"}
    return render(request, "courses/course_form.html", context)
```

Маршрут (після `<slug:slug>/`):

```python
path("courses/<slug:slug>/edit/", views.course_update, name="course_update"),
```

`get_object_or_404` замість `Course.objects.get(...)`: неіснуючий slug дає чесний `404`, а не `500` з `DoesNotExist`.

**Покажи результат.**

- `GET /courses/django-web/edit/` — поля заповнені: `<input type="text" name="title" value="Django: веб-розробка" ...>`, `hours` = 40.
- `GET /courses/nope/edit/` → `404`.
- Зміни годин на 44 → `302 → /courses/django-web/`, на сторінці курсу вже 44. (Поверни 40.)
- Спробуй змінити slug на `qa-basics` (він уже зайнятий) → помилка «Course з таким Slug вже існує.» Якщо залишити **свій** slug — помилки немає: `ModelForm` знає, що редагується цей самий об'єкт.

**Що буде без `instance=`?** Форма вважатиме, що створюється новий курс, і при редагуванні без зміни slug скаже, що slug уже існує (бо він справді існує — у цього ж курсу). Саме тому `instance` треба передавати і на GET, і на POST.

`git commit -m "Step 4: update view"`

## Крок 5. Delete: видалення з підтвердженням

**Теорія.** Видалення змінює дані, тому: **тільки POST**, ніколи GET. Якщо видаляти по посиланню `<a href="/delete/">`, то достатньо, щоб браузер чи пошуковий робот «пройшовся» по сторінці — і курс зник. Тому GET показує сторінку підтвердження, а видаляє тільки POST.

У моделі `Lesson` і `Enrollment` стоять `on_delete=CASCADE`, тому з курсом зникнуть **і його уроки та записи студентів**. Користувача про це треба попередити.

Шаблон `courses/templates/courses/course_confirm_delete.html`:

```html
{% extends "base.html" %}

{% block title %}Видалити курс{% endblock %}

{% block content %}
<h1>Видалити курс «{{ course.title }}»?</h1>
<p>Разом із курсом буде видалено уроків: <strong>{{ lessons_count }}</strong>
   і записів студентів: <strong>{{ enrollments_count }}</strong>. Цю дію не можна скасувати.</p>

<form method="post">
    {% csrf_token %}
    <button class="btn danger" type="submit">Так, видалити</button>
    <a href="{{ course.get_absolute_url }}">Скасувати</a>
</form>
{% endblock %}
```

View і маршрут:

```python
def course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == "POST":
        course.delete()
        return redirect("course_list")
    context = {
        "course": course,
        "lessons_count": course.lessons.count(),
        "enrollments_count": course.enrollments.count(),
    }
    return render(request, "courses/course_confirm_delete.html", context)
```

```python
path("courses/<slug:slug>/delete/", views.course_delete, name="course_delete"),
```

**Покажи результат.** Створи тимчасовий курс із одним уроком (через shell або форму) і відкрий `/courses/tmp-delete/delete/`:

- GET → `200`, текст: «Разом із курсом буде видалено уроків: **1** і записів студентів: **0**». Курс у базі **ще є**.
- POST (кнопка) → `302 → /courses/`, курс **і його урок** зникли.
- Повторний GET на видалений slug → `404`.

Що робить `delete()` під капотом, видно в shell:

```python
>>> Course.objects.filter(slug="tmp2").delete()
(1, {'courses.Course': 1})
```

У відповіді — скільки об'єктів і яких моделей видалено (з каскадом там були б і `courses.Lesson`).

`git commit -m "Step 5: delete with confirmation"`

## Крок 6. Повідомлення (`messages`) і кнопки в інтерфейсі

**Теорія.** Після redirect користувач потрапляє на іншу сторінку і не розуміє, чи спрацювало. Фреймворк `messages` зберігає коротке повідомлення до **наступного** запиту і показує один раз. У `settings.py` вже є `MessageMiddleware` і `django.contrib.messages`.

У `views.py` (імпорт `from django.contrib import messages`):

```python
# course_create, після form.save()
course = form.save()
messages.success(request, f"Курс «{course.title}» створено.")
return redirect(course)

# course_update
form.save()
messages.success(request, f"Курс «{course.title}» оновлено.")
return redirect(course)

# course_delete: назву запам'ятовуємо ДО видалення
title = course.title
course.delete()
messages.success(request, f"Курс «{title}» видалено.")
return redirect("course_list")
```

У `templates/base.html`, на початку `<main>`:

```html
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li class="{{ message.tags }}">{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```

Кнопки. У `course_list.html` під заголовком:

```html
<p><a class="btn" href="{% url 'course_create' %}">+ Новий курс</a></p>
```

У `course_detail.html` після опису:

```html
<p>
    <a class="btn" href="{% url 'course_update' course.slug %}">Редагувати</a>
    <a class="btn danger" href="{% url 'course_delete' course.slug %}">Видалити</a>
</p>
```

У `static/css/lms.css` додай стилі (повний набір є в еталоні):

```css
.btn.danger { background: #dc2626; }
.messages { list-style: none; padding: 0; margin: 0 0 16px; }
.messages li { padding: 10px 14px; border-radius: 8px; background: #dcfce7; color: #14532d; }
.errorlist { color: #b91c1c; list-style: none; padding: 0; margin: 4px 0; }
```

**Покажи результат.** Створи курс → бачиш зелений рядок «Курс «Flow» створено.» на сторінці курсу. Онови сторінку (F5) → повідомлення зникло: воно показується **один раз**. Видали курс → на списку «Курс «Flow 2» видалено.».

`git commit -m "Step 6: messages and buttons"`

## Крок 7. Свої правила валідації, віджети й ручний рендер

**Теорія.** Валідація має три рівні:

1. Типи й обмеження полів (`max_length`, `min_value`, `unique`) — автоматично.
2. `clean_<поле>()` — правило для **одного** поля. Повертає очищене значення.
3. `clean()` — правило, що зачіпає **кілька** полів. Помилку до поля додає `self.add_error("поле", "текст")`; загальну — `raise ValidationError`.

**Віджет** — спосіб малювання поля в HTML (`TextInput`, `Textarea`, `Select`, `CheckboxInput`). Через `attrs` додаємо `placeholder`, `rows`, `class`. Назви й підказки задаємо через `labels` і `help_texts`.

Повна версія `courses/forms.py`:

```python
from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "slug", "level", "teacher", "hours", "is_new", "description"]
        labels = {
            "title": "Назва",
            "slug": "Адреса (slug)",
            "level": "Рівень",
            "teacher": "Викладач",
            "hours": "Тривалість, годин",
            "is_new": "Позначити як новий",
            "description": "Опис",
        }
        help_texts = {"slug": "Латиниця, цифри та дефіси. Це частина URL."}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Наприклад: Python для QA"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 5:
            raise forms.ValidationError("Назва має містити щонайменше 5 символів.")
        return title

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("level") == Course.Level.ADVANCED and (cleaned.get("hours") or 0) < 20:
            self.add_error("hours", "Просунутий курс має тривати щонайменше 20 годин.")
        return cleaned
```

У `clean()` завжди пиши `cleaned.get(...)`, а не `cleaned[...]`: якщо поле не пройшло власну перевірку, його в `cleaned_data` немає.

**Ручний рендер.** `as_p` — для старту. Коли треба керувати версткою, обходимо поля самі (`courses/course_form.html`):

```html
<form method="post" novalidate>
    {% csrf_token %}
    {{ form.non_field_errors }}
    {% for field in form %}
    <div class="field">
        {{ field.label_tag }}
        {{ field }}
        {% if field.help_text %}<small class="muted">{{ field.help_text }}</small>{% endif %}
        {{ field.errors }}
    </div>
    {% endfor %}
    <button class="btn" type="submit">Зберегти</button>
    <a href="{% url 'course_list' %}">Скасувати</a>
</form>
```

`novalidate` вимикає перевірку браузера, щоб ти бачив **серверні** помилки.

**Покажи результат.** У shell:

```python
>>> base = {"slug": "x1", "level": "advanced", "teacher": "A", "hours": "10"}
>>> f = CourseForm({**base, "title": "  ab "}); f.is_valid()
False
>>> {k: list(v) for k, v in f.errors.items()}
{'title': ['Назва має містити щонайменше 5 символів.'], 'hours': ['Просунутий курс має тривати щонайменше 20 годин.']}
>>> f = CourseForm({**base, "title": "  Python для QA ", "hours": "30"}); f.is_valid()
True
```

На сторінці: поле «Назва» зберігає `ab`, з'являється підказка `Наприклад: Python для QA`, і під полями — червоні повідомлення. Курс не створено.

`git commit -m "Step 7: clean methods, widgets, manual rendering"`

## Крок 8. Тести

**Теорія.** Тестовий клієнт Django (`self.client`) викликає view без браузера і сервера. Тест створює **окрему тестову базу**, тому ваші дані не чіпає. Корисні перевірки: `assertRedirects`, `assertContains`, `assertEqual(response.status_code, ...)`.

Додай у `courses/tests.py` (імпорти `TestCase`, `reverse`, `Course` вже є з уроку 40):

```python
class CourseCrudTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(slug="demo-crud", title="Демо CRUD", teacher="Автор", hours=10)
        self.valid = {
            "title": "Новий курс", "slug": "new-course", "level": "beginner",
            "teacher": "Автор", "hours": 12, "description": "",
        }

    def test_create_get_shows_form(self):
        response = self.client.get(reverse("course_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"')

    def test_create_valid_redirects_and_saves(self):
        response = self.client.post(reverse("course_create"), self.valid)
        self.assertRedirects(response, "/courses/new-course/")
        self.assertTrue(Course.objects.filter(slug="new-course").exists())

    def test_create_invalid_shows_errors_and_saves_nothing(self):
        data = {**self.valid, "title": ""}
        response = self.client.post(reverse("course_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "errorlist")
        self.assertFalse(Course.objects.filter(slug="new-course").exists())

    def test_duplicate_slug_is_form_error_not_500(self):
        data = {**self.valid, "slug": "demo-crud"}
        response = self.client.post(reverse("course_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Course.objects.filter(slug="demo-crud").count(), 1)

    def test_advanced_course_needs_20_hours(self):
        data = {**self.valid, "level": "advanced", "hours": 10}
        response = self.client.post(reverse("course_create"), data)
        self.assertContains(response, "щонайменше 20 годин")

    def test_update_changes_object(self):
        data = {**self.valid, "slug": "demo-crud", "title": "Змінена назва"}
        self.client.post(reverse("course_update", args=["demo-crud"]), data)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Змінена назва")

    def test_update_unknown_course_is_404(self):
        response = self.client.get(reverse("course_update", args=["nope"]))
        self.assertEqual(response.status_code, 404)

    def test_delete_get_does_not_delete(self):
        response = self.client.get(reverse("course_delete", args=["demo-crud"]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Course.objects.filter(slug="demo-crud").exists())

    def test_delete_post_deletes_and_shows_message(self):
        response = self.client.post(reverse("course_delete", args=["demo-crud"]), follow=True)
        self.assertFalse(Course.objects.filter(slug="demo-crud").exists())
        self.assertContains(response, "видалено")
```

Запуск: `python manage.py test`. У нас 5 тестів з уроку 40 + 9 нових:

```
Ran 14 tests in 0.098s

OK
```

`follow=True` змушує клієнт піти за redirect, тому в `response` — уже сторінка після нього (з банером).

`git commit -m "Step 8: tests for CRUD"`

## Довідник: карта CRUD

| Дія | URL | Метод | View | Після успіху |
| --- | --- | --- | --- | --- |
| Create | `/courses/new/` | GET, POST | `course_create` | redirect на курс |
| Read | `/courses/<slug>/` | GET | `course_detail` | — |
| Update | `/courses/<slug>/edit/` | GET, POST | `course_update` | redirect на курс |
| Delete | `/courses/<slug>/delete/` | GET (підтвердження), POST | `course_delete` | redirect на список |

**Шаблон логіки view з формою:**

```python
if request.method == "POST":
    form = MyForm(request.POST, instance=obj)   # instance — лише для update
    if form.is_valid():
        form.save()
        messages.success(request, "...")
        return redirect(obj)
else:
    form = MyForm(instance=obj)
return render(request, "form.html", {"form": form})
```

**Терміни.**

- Незв'язана форма — `Form()`, без даних, просто малюється. Зв'язана — `Form(request.POST)`, готова до `is_valid()`.
- `cleaned_data` — перевірені дані нужних типів; `form.errors` — помилки по полях.
- `form.save()` — лише у `ModelForm`; `commit=False` — об'єкт без збереження.
- `get_object_or_404` — об'єкт або чесний 404.

## Типові помилки

| Симптом | Причина | Як виправити |
| --- | --- | --- |
| `403 Forbidden` при відправці | немає `{% csrf_token %}` у `<form method="post">` | додати тег усередину форми |
| кнопка «нічого не робить» | view не перевіряє `request.method == "POST"` | додати гілку POST |
| форма завжди порожня, помилок немає | у шаблон передано нову `CourseForm()` замість `form`, або `form` створена поза `if/else` | в `render` передавати ту форму, що пройшла `is_valid` |
| після F5 дублікат об'єкта | успішний POST без `redirect` | `return redirect(...)` |
| `404` на `/courses/new/` | `new/` стоїть після `<slug:slug>/` у `urls.py` | поставити `new/` вище |
| `500 IntegrityError: UNIQUE constraint failed` | звичайна `Form` не знає про `unique` | перейти на `ModelForm` |
| при редагуванні: «slug уже існує» на власний курс | не передано `instance=course` | `CourseForm(request.POST, instance=course)` |
| `Course.DoesNotExist` → 500 | `objects.get` без перевірки | `get_object_or_404` |
| кнопка «Видалити» стирає одразу | видалення по GET | тільки POST + сторінка підтвердження |
| `KeyError` у `clean()` | `cleaned["hours"]` для поля, що не пройшло валідацію | `cleaned.get("hours")` |

## Перевір себе

1. Чим GET відрізняється від POST і для яких дій кожен?
2. Що таке зв'язана форма? Як дізнатися, чи вона зв'язана (`is_bound`)?
3. Де лежать помилки валідації і де — очищені дані?
4. Для чого `{% csrf_token %}` і що буде без нього?
5. Чому після успішного POST робимо redirect, а не `render`?
6. В чому відмінність `ModelForm` від `Form` і чому дубль slug у `Form` дає 500?
7. Що зміниться, якщо у `course_update` прибрати `instance=course`?
8. Чому видалення робимо лише по POST і чому попереджаємо про каскад?
9. Коли писати `clean_<поле>`, а коли `clean()`?
10. Що робить `form.save(commit=False)` і навіщо воно?

## Домашня робота

Реалізуй повний CRUD для **сутності у своєму проєкті** (Task/Bug, Expense, Service — на вибір). Вимоги:

1. `ModelForm` з явним `fields`, `labels` і принаймні одним `placeholder`.
2. Create, Update, Delete з підтвердженням тільки по POST; після кожної дії redirect і `messages`.
3. `get_object_or_404` у всіх view з одним об'єктом.
4. Одне власне правило валідації (`clean_<поле>` або `clean()`), наприклад: сума витрати > 0, або дедлайн задачі не в минулому.
5. Мінімум 6 тестів (create ok/invalid, update, 404, delete GET/POST).
6. Коміт на кожний крок.

**Додатково (для сильних):** кнопка «Видалити» без сторінки підтвердження, але з `<form method="post">` прямо у списку; або `ModelForm` для `Lesson` з прив'язкою до курсу через `commit=False`.

## Підсумок

- CRUD = чотири дії; для кожної — URL, view, шаблон, ORM.
- GET — отримати, POST — змінити. Після успішного POST — `redirect`.
- Форма буває незв'язаною та зв'язаною; `is_valid()` → `cleaned_data` або `errors`.
- `ModelForm` + `instance=` дають create і update поруч, враховуючи `unique` і `choices`.
- Видалення — тільки POST і з попередженням про каскад.
- `messages` показують результат після redirect; `clean_*` і `clean()` — власні правила.
- Тести перевіряють усе це без браузера.

Еталони кожного кроку (`steps/s1 … s8`) і фінальний проєкт є в архіві від викладача. Застряг — порівняй свій код з ними.
