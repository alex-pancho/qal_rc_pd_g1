# Домашнє завдання. Заняття 41. Task & Bug Manager — CRUD та форми

## Мета
Реалізувати CRUD операції (Create, Read, Update, Delete) для управління задачами та багами. Практикуватися з формами Django, валідацією та обробкою користувацьких даних.

## Вимоги до завдання

### Базовий рівень (обов'язково)

#### 1. Створити формові класи

**Файл:** `forms.py`

```python
from django import forms
from .models import Issue, Comment

class IssueForm(forms.ModelForm):
    """Форма для створення та редагування завдання"""
    
    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "issue_type",
            "priority",
            "status",
            "assigned_to",
            "deadline"
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Назва завдання",
                "autofocus": True,
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Детальний опис",
            }),
            "issue_type": forms.Select(attrs={
                "class": "form-control",
            }),
            "priority": forms.Select(attrs={
                "class": "form-control",
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
            "assigned_to": forms.Select(attrs={
                "class": "form-control",
            }),
            "deadline": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 3:
            raise forms.ValidationError(
                "Назва повинна містити щонайменше 3 символи"
            )
        if len(title) > 200:
            raise forms.ValidationError(
                "Назва занадто довга (макс. 200 символів)"
            )
        return title
    
    def clean_deadline(self):
        from datetime import date
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < date.today():
            raise forms.ValidationError(
                "Дедлайн не може бути в минулому"
            )
        return deadline


class CommentForm(forms.ModelForm):
    """Форма для додавання коментаря"""
    
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Додайте коментар...",
            }),
        }
```

#### 2. Створити CRUD view функції

**Файл:** `views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Issue, Comment
from .forms import IssueForm, CommentForm

# READ — список всіх завдань
def issue_list(request):
    issues = Issue.objects.all()
    
    # Фільтрування за статусом
    status = request.GET.get("status")
    if status:
        issues = issues.filter(status=status)
    
    # Пошук по назві
    search = request.GET.get("search")
    if search:
        issues = issues.filter(title__icontains=search)
    
    context = {
        "issues": issues,
        "status": status,
        "search": search,
    }
    return render(request, "issues/issue_list.html", context)

# READ — деталі завдання
def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    comments = issue.comments.all()
    comment_form = CommentForm()
    
    context = {
        "issue": issue,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "issues/issue_detail.html", context)

# CREATE — створення нового завдання
@login_required
def issue_create(request):
    form = IssueForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        issue = form.save(commit=False)
        issue.author = request.user
        issue.save()
        messages.success(request, "✓ Завдання створене!")
        return redirect("issue_detail", issue_id=issue.id)
    
    return render(request, "issues/issue_form.html", {"form": form})

# UPDATE — редагування завдання
@login_required
def issue_update(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    
    # Перевіра прав: тільки автор може редагувати
    if issue.author != request.user and not request.user.is_staff:
        messages.error(request, "У вас немає прав для редагування")
        return redirect("issue_detail", issue_id=issue.id)
    
    form = IssueForm(request.POST or None, instance=issue)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "✓ Завдання оновлене!")
        return redirect("issue_detail", issue_id=issue.id)
    
    return render(request, "issues/issue_form.html", 
                  {"form": form, "issue": issue})

# DELETE — видалення завдання
@login_required
def issue_delete(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    
    # Перевіра прав
    if issue.author != request.user and not request.user.is_staff:
        messages.error(request, "У вас немає прав для видалення")
        return redirect("issue_detail", issue_id=issue.id)
    
    if request.method == "POST":
        issue.delete()
        messages.success(request, "✓ Завдання видалене!")
        return redirect("issue_list")
    
    return render(request, "issues/issue_confirm_delete.html", 
                  {"issue": issue})

# Додавання коментаря
@login_required
def comment_create(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.issue = issue
            comment.save()
            messages.success(request, "✓ Коментар додано!")
    
    return redirect("issue_detail", issue_id=issue.id)
```

#### 3. Налаштування URL маршрутів

**Файл:** `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path("issues/", views.issue_list, name="issue_list"),
    path("issues/<int:issue_id>/", views.issue_detail, name="issue_detail"),
    path("issues/create/", views.issue_create, name="issue_create"),
    path("issues/<int:issue_id>/edit/", views.issue_update, name="issue_update"),
    path("issues/<int:issue_id>/delete/", views.issue_delete, name="issue_delete"),
    path("issues/<int:issue_id>/comment/", views.comment_create, name="comment_create"),
]
```

#### 4. Створити шаблони

**Файл:** `templates/issues/issue_list.html`

```html
{% extends "base.html" %}

{% block title %}Завдання{% endblock %}

{% block content %}
<h2>Управління завданнями</h2>

{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}

<a href="{% url 'issue_create' %}" class="btn btn-primary">+ Нове завдання</a>

<!-- Фільтр -->
<form method="get" class="form-inline">
    <input type="text" name="search" value="{{ search }}" 
           placeholder="Пошук..." class="form-control">
    
    <select name="status" class="form-control">
        <option value="">Всі статуси</option>
        <option value="open" {% if status == 'open' %}selected{% endif %}>Відкрито</option>
        <option value="in_progress" {% if status == 'in_progress' %}selected{% endif %}>У процесі</option>
        <option value="closed" {% if status == 'closed' %}selected{% endif %}>Закрито</option>
    </select>
    
    <button type="submit" class="btn btn-secondary">Фільтрувати</button>
</form>

<!-- Таблиця завдань -->
<table class="table">
    <thead>
        <tr>
            <th>Назва</th>
            <th>Тип</th>
            <th>Пріоритет</th>
            <th>Статус</th>
            <th>Автор</th>
            <th>Дії</th>
        </tr>
    </thead>
    <tbody>
    {% for issue in issues %}
        <tr>
            <td><strong>{{ issue.title }}</strong></td>
            <td>{{ issue.get_issue_type_display }}</td>
            <td><span class="badge priority-{{ issue.priority }}">
                {{ issue.get_priority_display }}
            </span></td>
            <td>{{ issue.get_status_display }}</td>
            <td>{{ issue.author.username }}</td>
            <td>
                <a href="{% url 'issue_detail' issue.id %}">Переглянути</a>
                <a href="{% url 'issue_update' issue.id %}">Редагувати</a>
                <a href="{% url 'issue_delete' issue.id %}">Видалити</a>
            </td>
        </tr>
    {% empty %}
        <tr><td colspan="6">Завдань не знайдено</td></tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}
```

**Файл:** `templates/issues/issue_form.html`

```html
{% extends "base.html" %}

{% block title %}{% if issue %}Редагувати{% else %}Створити{% endif %} завдання{% endblock %}

{% block content %}
<h2>{% if issue %}Редагувати{% else %}Створити нове{% endif %} завдання</h2>

<form method="post" novalidate>
    {% csrf_token %}
    
    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            {{ form.non_field_errors }}
        </div>
    {% endif %}
    
    {% for field in form %}
        <div class="form-group">
            {{ field.label_tag }}
            {{ field }}
            {% if field.errors %}
                <div class="alert alert-danger">
                    {{ field.errors }}
                </div>
            {% endif %}
        </div>
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Зберегти</button>
    <a href="{% url 'issue_list' %}" class="btn btn-secondary">Скасувати</a>
</form>
{% endblock %}
```

**Файл:** `templates/issues/issue_detail.html`

```html
{% extends "base.html" %}

{% block title %}{{ issue.title }}{% endblock %}

{% block content %}
<h2>{{ issue.title }}</h2>

{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}

<div class="issue-meta">
    <p><strong>Тип:</strong> {{ issue.get_issue_type_display }}</p>
    <p><strong>Пріоритет:</strong> {{ issue.get_priority_display }}</p>
    <p><strong>Статус:</strong> {{ issue.get_status_display }}</p>
    <p><strong>Автор:</strong> {{ issue.author.username }}</p>
    <p><strong>Призначений:</strong> {{ issue.assigned_to.username or "Не призначений" }}</p>
    {% if issue.deadline %}
        <p><strong>Дедлайн:</strong> {{ issue.deadline|date:"d.m.Y" }}</p>
    {% endif %}
</div>

<div class="issue-description">
    <h3>Опис</h3>
    <p>{{ issue.description }}</p>
</div>

<div class="issue-actions">
    <a href="{% url 'issue_update' issue.id %}" class="btn btn-primary">Редагувати</a>
    <a href="{% url 'issue_delete' issue.id %}" class="btn btn-danger">Видалити</a>
    <a href="{% url 'issue_list' %}" class="btn btn-secondary">До списку</a>
</div>

<!-- Коментарі -->
<h3>Коментарі ({{ comments.count }})</h3>

<div class="comments">
    {% for comment in comments %}
        <div class="comment">
            <p><strong>{{ comment.author.username }}</strong> 
               <small>{{ comment.created_at|date:"d.m.Y H:i" }}</small></p>
            <p>{{ comment.content }}</p>
        </div>
    {% empty %}
        <p>Коментарів немає</p>
    {% endfor %}
</div>

<!-- Форма для нового коментаря -->
{% if user.is_authenticated %}
    <h3>Додати коментар</h3>
    <form method="post" action="{% url 'comment_create' issue.id %}">
        {% csrf_token %}
        {{ comment_form.as_p }}
        <button type="submit" class="btn btn-primary">Додати</button>
    </form>
{% else %}
    <p><a href="{% url 'login' %}">Увійдіть</a> для додавання коментаря</p>
{% endif %}
{% endblock %}
```

**Файл:** `templates/issues/issue_confirm_delete.html`

```html
{% extends "base.html" %}

{% block title %}Видалення завдання{% endblock %}

{% block content %}
<h2>Видалення завдання</h2>

<div class="alert alert-warning">
    <p>Ви впевнені, що хочете видалити "<strong>{{ issue.title }}</strong>"?</p>
    <p>Це не можна буде скасувати!</p>
</div>

<form method="post" style="display: inline;">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Так, видалити</button>
</form>

<a href="{% url 'issue_detail' issue.id %}" class="btn btn-secondary">Скасувати</a>
{% endblock %}
```

---

### Додатковий рівень (за бажанням)

#### 1. Фільтрування за призначеною особою

```python
def issue_list(request):
    issues = Issue.objects.all()
    
    # Фільтр за статусом
    status = request.GET.get("status")
    if status:
        issues = issues.filter(status=status)
    
    # Фільтр за пріоритетом
    priority = request.GET.get("priority")
    if priority:
        issues = issues.filter(priority=priority)
    
    # Фільтр за призначеною особою
    assigned = request.GET.get("assigned")
    if assigned:
        issues = issues.filter(assigned_to_id=assigned)
    
    context = {
        "issues": issues,
        "status": status,
        "priority": priority,
        "assigned": assigned,
    }
    return render(request, "issues/issue_list.html", context)
```

#### 2. Сортування завдань

```python
# В шаблоні додайте посилання на сортування
<a href="?{% if sort == 'created_at' %}sort=-created_at{% else %}sort=created_at{% endif %}">
    За датою
</a>

# У view:
sort = request.GET.get("sort", "-created_at")
issues = issues.order_by(sort)
```

#### 3. Перевірка прав користувача

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView

class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # Тільки автор або адмін може редагувати
        issue = self.get_object()
        return self.request.user == issue.author or self.request.user.is_staff
```

#### 4. CSV експорт завдань

```python
import csv
from django.http import HttpResponse

def export_issues_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="issues.csv"'
    
    writer = csv.writer(response)
    writer.writerow(["Назва", "Тип", "Пріоритет", "Статус"])
    
    for issue in Issue.objects.all():
        writer.writerow([
            issue.title,
            issue.get_issue_type_display(),
            issue.get_priority_display(),
            issue.get_status_display(),
        ])
    
    return response
```

#### 5. Пакетне оновлення статусу

```python
def issue_bulk_update_status(request):
    if request.method == "POST":
        issue_ids = request.POST.getlist("issue_ids")
        new_status = request.POST.get("new_status")
        
        Issue.objects.filter(id__in=issue_ids).update(
            status=new_status
        )
        messages.success(request, f"✓ Оновлено {len(issue_ids)} завдань!")
    
    return redirect("issue_list")
```

---

## Очікуваний результат

**Структура файлів:**
```
task_manager/
    forms.py                    # IssueForm, CommentForm
    views.py                    # CRUD функції
    urls.py                     # Маршрути
    templates/
        issues/
            issue_list.html     # Список завдань з фільтром
            issue_form.html     # Форма для створення/редагування
            issue_detail.html   # Деталі завдання та коментарі
            issue_confirm_delete.html
```

**Функціональність:**
- ✅ Створення завдань (CREATE)
- ✅ Перегляд списку та деталей (READ)
- ✅ Редагування завдань (UPDATE)
- ✅ Видалення завдань (DELETE)
- ✅ Додавання коментарів
- ✅ Фільтрування та пошук
- ✅ Flash-повідомлення
- ✅ Перевірка прав доступу

## Критерії оцінювання

| Критерій | Базовий | Додатковий |
|----------|---------|-----------|
| IssueForm | ✅ | - |
| issue_list view | ✅ | - |
| issue_detail view | ✅ | - |
| issue_create view | ✅ | - |
| issue_update view | ✅ | - |
| issue_delete view | ✅ | - |
| Шаблони | ✅ | - |
| CSRF токен | ✅ | - |
| Валідація форми | ✅ | - |
| Фільтрування | - | ✅ |
| Перевірка прав | - | ✅ |
| Пакетне оновлення | - | ✅ |
| CSV експорт | - | ✅ |

## Рекомендації

1. **Безпека:** перевіряйте `request.user` перед редагуванням/видаленням
2. **Форми:** завжди використовуйте `{% csrf_token %}`
3. **Валідація:** додавайте `clean_` методи для важливих полів
4. **Повідомлення:** показуйте feedback користувачу через `messages`
5. **Шаблони:** перевіряйте `user.is_authenticated` перед видаленням

Успіхів у розробці! 🚀