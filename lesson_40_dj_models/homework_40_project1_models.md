# Домашнє завдання. Заняття 40. Task & Bug Manager — Моделі та база даних

## Мета
Створити моделі Django для управління задачами, багами та коментарями. Практикуватися з ForeignKey, ManyToMany зв'язками, міграціями та ORM запитами.

## Вимоги до завдання

### Базовий рівень (обов'язково)

#### 1. Створити модель користувача (User)

**Файл:** `models.py`

```python
from django.db import models
from django.contrib.auth.models import User  # Django User модель

# Розширене поле користувача (профіль)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[
            ("user", "Користувач"),
            ("admin", "Адміністратор"),
            ("manager", "Менеджер"),
        ],
        default="user"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
```

#### 2. Створити модель Issue (Задача / Баг)

**Вимоги:**
- Назва (CharField, max_length=200)
- Опис (TextField)
- Тип (CharField з choices: Task, Bug, Test Case)
- Пріоритет (CharField з choices: Low, Medium, High, Critical)
- Статус (CharField з choices: Open, In Progress, Closed, On Hold)
- Автор (ForeignKey на User)
- Призначений (ForeignKey на User, nullable)
- Дедлайн (DateField, nullable)
- Дата створення (DateTimeField, auto_now_add)
- Дата оновлення (DateTimeField, auto_now)

**Приклад:**

```python
class Issue(models.Model):
    TYPE_CHOICES = [
        ("task", "Задача"),
        ("bug", "Баг"),
        ("test", "Тест-кейс"),
    ]
    
    PRIORITY_CHOICES = [
        ("low", "Низька"),
        ("medium", "Середня"),
        ("high", "Висока"),
        ("critical", "Критична"),
    ]
    
    STATUS_CHOICES = [
        ("open", "Відкрито"),
        ("in_progress", "У процесі"),
        ("closed", "Закрито"),
        ("on_hold", "На паузі"),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    issue_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="issues_created"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues_assigned"
    )
    
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["-priority"]),
        ]
    
    def __str__(self):
        return f"[{self.get_issue_type_display()}] {self.title}"
```

#### 3. Створити модель коментаря (Comment)

**Вимоги:**
- Текст (TextField)
- Автор (ForeignKey на User)
- Завдання (ForeignKey на Issue)
- Дата створення (DateTimeField, auto_now_add)

```python
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Коментар {self.author} до {self.issue.title}"
```

#### 4. Виконати міграції

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Зареєструвати моделі в адмінці

**Файл:** `admin.py`

```python
from django.contrib import admin
from .models import UserProfile, Issue, Comment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "created_at"]
    search_fields = ["user__username"]
    list_filter = ["role"]

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["title", "issue_type", "priority", "status", "author"]
    search_fields = ["title", "description"]
    list_filter = ["status", "priority", "issue_type", "created_at"]
    fieldsets = (
        ("Основна інформація", {
            "fields": ("title", "description", "issue_type")
        }),
        ("Важливість", {
            "fields": ("priority", "status")
        }),
        ("Призначення", {
            "fields": ("author", "assigned_to", "deadline")
        }),
    )
    readonly_fields = ["created_at", "updated_at"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "issue", "created_at"]
    search_fields = ["content", "issue__title"]
    list_filter = ["created_at"]
```

#### 6. Тестування моделей в shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from myapp.models import Issue, Comment, UserProfile

# Створити користувача
user = User.objects.create_user(
    username="john",
    email="john@example.com",
    password="12345"
)

# Створити профіль
profile = UserProfile.objects.create(user=user, role="user")

# Створити завдання
issue = Issue.objects.create(
    title="Виправити баг входу",
    description="Користувачі не можуть увійти",
    issue_type="bug",
    priority="critical",
    author=user,
    assigned_to=user
)

# Додати коментар
comment = Comment.objects.create(
    content="Я беру цей баг на себе",
    author=user,
    issue=issue
)

# Запити до БД
all_issues = Issue.objects.all()
open_issues = Issue.objects.filter(status="open")
high_priority = Issue.objects.filter(priority="high")
john_issues = user.issues_created.all()

# Оновити статус
issue.status = "in_progress"
issue.save()

# Видалити
comment.delete()
```

---

### Додатковий рівень (за бажанням)

#### 1. Додати теги (ManyToMany)

```python
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Issue(models.Model):
    # ... інші поля ...
    tags = models.ManyToManyField(Tag, related_name="issues", blank=True)
```

Використання:
```python
issue.tags.add(tag1, tag2)
tagged_issues = Tag.objects.get(name="frontend").issues.all()
```

#### 2. Додати методи до моделей

```python
class Issue(models.Model):
    # ... поля ...
    
    def close(self):
        """Закрити завдання"""
        self.status = "closed"
        self.save()
    
    def reassign(self, user):
        """Переприз начити завдання іншому користувачу"""
        self.assigned_to = user
        self.save()
    
    @property
    def is_overdue(self):
        """Перевірка: чи минув дедлайн"""
        if self.deadline:
            from datetime import date
            return date.today() > self.deadline
        return False
    
    def get_comments_count(self):
        """Кількість коментарів"""
        return self.comments.count()
```

#### 3. Улучшена адмінка: inline редагування

```python
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    # ... попередній код ...
    inlines = [CommentInline]
```

Тепер коментарі можна редагувати прямо на сторінці завдання!

#### 4. Фільтри та пошук за ORM

```python
# Завдання, які вже минули дедлайн і не закриті
from datetime import date
overdue = Issue.objects.filter(
    deadline__lt=date.today(),
    status__ne="closed"
)

# Завдання, які призначені конкретному користувачу
user_tasks = Issue.objects.filter(assigned_to__username="john")

# Кількість відкритих багів
open_bugs = Issue.objects.filter(
    issue_type="bug",
    status="open"
).count()

# Найпопулярніші теги
from django.db.models import Count
popular_tags = Tag.objects.annotate(
    count=Count("issues")
).order_by("-count")[:5]
```

#### 5. Тестувальне завдання для перевірки

Створіть скрипт `test_models.py`:

```python
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from myapp.models import Issue, Comment, Tag

# Тест 1: Створення
user = User.objects.create_user("test_user", "test@test.com", "pass")
issue = Issue.objects.create(
    title="Test Issue",
    description="Test",
    issue_type="task",
    priority="high",
    author=user
)
print("✓ Моделі створені")

# Тест 2: Читання
assert Issue.objects.count() == 1
print("✓ Запис створений")

# Тест 3: Оновлення
issue.status = "closed"
issue.save()
assert issue.status == "closed"
print("✓ Запис оновлений")

# Тест 4: Видалення
issue.delete()
assert Issue.objects.count() == 0
print("✓ Запис видалений")

print("\nВсі тести пройшли!")
```

Запустити:
```bash
python test_models.py
```

---

## Очікуваний результат

**Структура проєкту:**
```
task_manager/
    migrations/
        0001_initial.py
        0002_add_tags.py
        ...
    models.py          # Моделі Issue, Comment, UserProfile, Tag
    admin.py           # Реєстрація в адмінці
    views.py
    urls.py
    tests.py (опціонально)
    manage.py
```

**База даних матиме таблиці:**
- `auth_user` (вбудована Django)
- `myapp_userprofile`
- `myapp_issue`
- `myapp_comment`
- `myapp_tag` (якщо додано)
- `myapp_issue_tags` (для ManyToMany)

**Функціональність:**
- ✅ Користувачі можуть створювати завдання
- ✅ Завдання можуть бути призначені іншим користувачам
- ✅ До завдань можна додавати коментарі
- ✅ Завдання мають пріоритети та статуси
- ✅ Адмін-панель для керування всіма даними

## Критерії оцінювання

| Критерій | Базовий | Додатковий |
|----------|---------|-----------|
| Модель Issue | ✅ | - |
| Модель Comment | ✅ | - |
| Модель UserProfile | ✅ | - |
| ForeignKey зв'язки | ✅ | - |
| Міграції | ✅ | - |
| Адмін-панель | ✅ | - |
| Shell тестування | ✅ | - |
| ManyToMany (теги) | - | ✅ |
| Методи моделей | - | ✅ |
| Inline редагування | - | ✅ |
| Оптимізація запитів | - | ✅ |

## Рекомендації

1. **Порядок:** спочатку простові моделі, потім зв'язки
2. **Міграції:** завжди виконуйте `makemigrations` а потім `migrate`
3. **Тестування:** використовуйте shell для перевірки моделей
4. **Адмін-панель:** зареєструйте моделі якомога швидше
5. **ORM:** пишіть запити через ORM, не SQL

## Домашня робота на наступне заняття

Підготуватися до роботи з формами Django:
- Прочитати про `ModelForm`
- Дізнатися про валідацію форм
- Подумати, які поля потребуватимуть форми

Успіхів! 🚀
