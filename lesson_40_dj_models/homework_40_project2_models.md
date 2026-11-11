# Домашнє завдання. Заняття 40. Expense Tracker — Моделі та база даних

## Мета
Створити моделі Django для управління фінансами: користувачі, транзакції, бюджети та категорії. Практикуватися з ForeignKey зв'язками, валідацією та ORM запитами для фінансових операцій.

## Вимоги до завдання

### Базовий рівень (обов'язково)

#### 1. Створити модель категорії (Category)

**Файл:** `models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Категорії видатків: їжа, транспорт, розваги тощо"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=20, blank=True)  # emoji або іконка
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]
    
    def __str__(self):
        return self.name
```

#### 2. Створити модель транзакції (Transaction)

**Вимоги:**
- Користувач (ForeignKey на User)
- Категорія (ForeignKey на Category)
- Сума (DecimalField для грошей)
- Тип (CharField з choices: Income, Expense)
- Дата (DateField)
- Опис (TextField)
- Дата створення (DateTimeField, auto_now_add)

```python
class Transaction(models.Model):
    TYPE_CHOICES = [
        ("income", "Дохід"),
        ("expense", "Видаток"),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Сума в гривнях"
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Транзакція"
        verbose_name_plural = "Транзакції"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "-date"]),
            models.Index(fields=["transaction_type"]),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} ₴ ({self.get_transaction_type_display()})"
```

#### 3. Створити модель бюджету (Budget)

**Вимоги:**
- Користувач (ForeignKey на User)
- Категорія (ForeignKey на Category)
- Місячний ліміт (DecimalField)
- Місяць/рік (CharField або DateField)

```python
class Budget(models.Model):
    """Бюджет: ліміт видатків на місяць за категорією"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="budgets"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Максимальна сума видатків на місяць"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Бюджет"
        verbose_name_plural = "Бюджети"
        unique_together = ["user", "category", "month", "year"]
        ordering = ["-year", "-month"]
    
    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.month}/{self.year}): {self.limit} ₴"
    
    def get_spent(self):
        """Скільки вже витрачено цього місяця за цією категорією"""
        spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type="expense",
            date__month=self.month,
            date__year=self.year
        ).aggregate(total=models.Sum("amount"))["total"] or 0
        return spent
    
    def get_remaining(self):
        """Скільки ще можна витратити"""
        return self.limit - self.get_spent()
    
    def is_exceeded(self):
        """Чи перевищено ліміт"""
        return self.get_spent() > self.limit
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
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "transaction_count"]
    search_fields = ["name"]
    
    def transaction_count(self, obj):
        return obj.transactions.count()

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["date", "user", "category", "amount", "transaction_type"]
    search_fields = ["user__username", "description", "category__name"]
    list_filter = ["transaction_type", "date", "category"]
    date_hierarchy = "date"
    readonly_fields = ["created_at"]

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "month", "year", "limit", "spent"]
    search_fields = ["user__username", "category__name"]
    list_filter = ["year", "month"]
    
    def spent(self, obj):
        return f"{obj.get_spent()} ₴"
```

#### 6. Тестування моделей в shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from django.utils import timezone
from myapp.models import Category, Transaction, Budget
from decimal import Decimal

# Створити користувача
user = User.objects.create_user("john", "john@example.com", "pass")

# Створити категорії
food = Category.objects.create(name="Їжа", icon="🍔")
transport = Category.objects.create(name="Транспорт", icon="🚗")
salary = Category.objects.create(name="Зарплата", icon="💰")

# Додати дохід
income = Transaction.objects.create(
    user=user,
    category=salary,
    amount=Decimal("15000.00"),
    transaction_type="income",
    date=timezone.now().date(),
    description="Зарплата від роботодавця"
)

# Додати видатки
expense1 = Transaction.objects.create(
    user=user,
    category=food,
    amount=Decimal("450.00"),
    transaction_type="expense",
    date=timezone.now().date(),
    description="Обід у ресторані"
)

# Перевірити баланс
income_total = Transaction.objects.filter(
    user=user,
    transaction_type="income"
).aggregate(total=models.Sum("amount"))["total"] or 0

expense_total = Transaction.objects.filter(
    user=user,
    transaction_type="expense"
).aggregate(total=models.Sum("amount"))["total"] or 0

balance = income_total - expense_total
print(f"Баланс: {balance} ₴")

# Створити бюджет
budget = Budget.objects.create(
    user=user,
    category=food,
    month=1,
    year=2024,
    limit=Decimal("2000.00")
)

# Перевірити витрати по бюджету
print(f"Витрачено: {budget.get_spent()} ₴")
print(f"Залишилось: {budget.get_remaining()} ₴")
```

---

### Додатковий рівень (за бажанням)

#### 1. Додати модель рахунку (Account)

```python
class Account(models.Model):
    """Банківський рахунок або гаманець"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # "Карта Приватбанку", "Готівка"
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="UAH")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.balance} {self.currency})"
```

#### 2. Додати методи для статистики

```python
class Transaction(models.Model):
    # ... поля ...
    
    @classmethod
    def get_monthly_stats(cls, user, month, year):
        """Статистика за місяць"""
        transactions = cls.objects.filter(
            user=user,
            date__month=month,
            date__year=year
        )
        income = transactions.filter(
            transaction_type="income"
        ).aggregate(total=models.Sum("amount"))["total"] or 0
        expense = transactions.filter(
            transaction_type="expense"
        ).aggregate(total=models.Sum("amount"))["total"] or 0
        return {
            "income": income,
            "expense": expense,
            "balance": income - expense
        }
    
    @classmethod
    def get_by_category(cls, user):
        """Видатки по категоріях"""
        return (
            cls.objects
            .filter(user=user, transaction_type="expense")
            .values("category__name")
            .annotate(total=models.Sum("amount"))
            .order_by("-total")
        )
```

#### 3. Додати валідацію

```python
from django.core.exceptions import ValidationError

class Transaction(models.Model):
    # ... поля ...
    
    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Сума повинна бути більше нуля")
        if self.transaction_type == "expense" and self.amount > 100000:
            raise ValidationError("Сумніви у видатку більш ніж 100,000 ₴")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
```

#### 4. Запити для аналізу видатків

```python
from django.db.models import Sum, Avg, Count

# Середній видаток на місяць
avg_expense = Transaction.objects.filter(
    user=user,
    transaction_type="expense"
).aggregate(avg=Avg("amount"))["avg"]

# Найбільше витратили в якій категорії
top_category = (
    Transaction.objects
    .filter(user=user, transaction_type="expense")
    .values("category__name")
    .annotate(total=Sum("amount"))
    .order_by("-total")
    .first()
)

# Кількість транзакцій по типам
stats = Transaction.objects.filter(user=user).aggregate(
    income_count=Count("id", filter=models.Q(transaction_type="income")),
    expense_count=Count("id", filter=models.Q(transaction_type="expense"))
)
```

#### 5. Тестувальний скрипт

```python
import django
import os
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from myapp.models import Category, Transaction, Budget

# Тест 1: Створення
user = User.objects.create_user("test", "test@test.com", "pass")
cat = Category.objects.create(name="Test")
trans = Transaction.objects.create(
    user=user, category=cat, amount=Decimal("100"),
    transaction_type="expense", date=timezone.now().date()
)
print("✓ Моделі створені")

# Тест 2: ORM запити
assert Transaction.objects.count() == 1
print("✓ Запит count() працює")

# Тест 3: Фільтрування
expenses = Transaction.objects.filter(transaction_type="expense")
assert expenses.count() == 1
print("✓ Запит filter() працює")

# Тест 4: Агрегація
from django.db.models import Sum
total = Transaction.objects.aggregate(Sum("amount"))
print(f"✓ Сумарна сума: {total}")

print("\nВсі тести пройшли!")
```

---

## Очікуваний результат

**Структура проєкту:**
```
expense_tracker/
    migrations/
        0001_initial.py
    models.py           # Category, Transaction, Budget, Account
    admin.py
    views.py
    urls.py
    manage.py
```

**База даних:**
- `myapp_category`
- `myapp_transaction`
- `myapp_budget`
- `myapp_account` (опціонально)

**Функціональність:**
- ✅ Користувачі можуть додавати транзакції
- ✅ Розпоління транзакцій по категоріях
- ✅ Управління бюджетами
- ✅ Розрахунок залишку та витрат
- ✅ Фінансова статистика

## Критерії оцінювання

| Критерій | Базовий | Додатковий |
|----------|---------|-----------|
| Модель Category | ✅ | - |
| Модель Transaction | ✅ | - |
| Модель Budget | ✅ | - |
| ForeignKey зв'язки | ✅ | - |
| Міграції | ✅ | - |
| Адмін-панель | ✅ | - |
| DecimalField для грошей | ✅ | - |
| Методи розрахунку | - | ✅ |
| Модель Account | - | ✅ |
| Статистичні запити | - | ✅ |
| Валідація даних | - | ✅ |

## Рекомендації

1. **Грошові поля:** завжди використовуйте `DecimalField`, не `FloatField`
2. **Унікальність:** бюджет повинен бути унікальний для користувача + категорія + місяць
3. **Дати:** для фільтрування по місяцях зберігайте числа 1-12
4. **Методи:** виконуйте розрахунки в моделях, не в views
5. **ORM:** використовуйте `.aggregate()` для статистики

Успіхів! 💰
