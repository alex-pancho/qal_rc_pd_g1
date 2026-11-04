# Домашнє завдання. Заняття 40. Service Management System — Моделі та база даних

## Мета
Створити моделі Django для управління сервісом: клієнти, послуги, замовлення та інвентар. Практикуватися з ForeignKey, ManyToMany зв'язками та ORM для бізнес-логіки.

## Варіанти
Виберіть один з доменів:
- **Auto Service & Parts Store** — ремонт автомобілів
- **Beauty Clinic & Aesthetic Medicine** — клініка краси

Архітектура буде однакова, просто змініть назви та опис.

## Вимоги до завдання

### Базовий рівень (обов'язково)

#### 1. Створити модель клієнта (Client / Customer)

**Файл:** `models.py`

Для **Auto Service:**
```python
from django.db import models

class Client(models.Model):
    """Клієнт (власник автомобіля)"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
        ]
    
    def __str__(self):
        return self.name
    
    def get_total_spent(self):
        """Скільки клієнт витратив на послуги"""
        return self.orders.aggregate(
            total=models.Sum("total_price")
        )["total"] or 0
```

Для **Beauty Clinic:**
```python
class Client(models.Model):
    """Пацієнт клініки"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    skin_type = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ("oily", "Жирна"),
            ("dry", "Суха"),
            ("combination", "Комбінована"),
            ("sensitive", "Чутлива"),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Пацієнт"
        verbose_name_plural = "Пацієнти"
        ordering = ["name"]
```

#### 2. Створити модель автомобіля / медичної карти (Vehicle / PatientProfile)

Для **Auto Service:**
```python
class Vehicle(models.Model):
    """Автомобіль, який обслуговується"""
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="vehicles"
    )
    make = models.CharField(max_length=100)  # марка
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Автомобіль"
        verbose_name_plural = "Автомобілі"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"
```

Для **Beauty Clinic:**
```python
class PatientProfile(models.Model):
    """Медична карта пацієнта"""
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    allergies = models.TextField(blank=True)
    previous_treatments = models.TextField(blank=True)
    preferred_procedures = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Профіль {self.client.name}"
```

#### 3. Створити модель послуги (Service)

```python
class Service(models.Model):
    """Послуга, яку пропонує сервіс"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.FloatField()  # тривалість у годинах
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"
        ordering = ["name"]
    
    def __str__(self):
        return f"{self.name} ({self.price} ₴)"
```

#### 4. Створити модель замовлення (Order / Appointment)

```python
class Order(models.Model):
    """Замовлення ремонту / запис на процедуру"""
    STATUS_CHOICES = [
        ("new", "Новий"),
        ("in_progress", "У процесі"),
        ("completed", "Готово"),
        ("cancelled", "Скасовано"),
    ]
    
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    # Для Auto Service — зв'язок з Vehicle
    vehicle = models.ForeignKey(
        "Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # Для Beauty Clinic — зв'язок з PatientProfile
    service = models.ManyToManyField(Service, related_name="orders")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    date = models.DateField()
    description = models.TextField(blank=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["-date"]),
        ]
    
    def __str__(self):
        return f"Замовлення #{self.id} - {self.client.name}"
    
    def get_total(self):
        """Розрахувати загальну вартість"""
        return self.service.aggregate(
            total=models.Sum("price")
        )["total"] or 0
```

#### 5. Створити модель інвентарю (Inventory)

```python
class Inventory(models.Model):
    """Запчастини / матеріали на складі"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.IntegerField()
    min_quantity = models.IntegerField(default=5)  # коли замовляти ще
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Запас"
        verbose_name_plural = "Запаси"
        ordering = ["-quantity"]
        indexes = [
            models.Index(fields=["category"]),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.quantity} шт)"
    
    def is_low_stock(self):
        """Чи низьке залишку"""
        return self.quantity < self.min_quantity
```

#### 6. Виконати міграції

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Зареєструвати моделі в адмінці

**Файл:** `admin.py`

```python
from django.contrib import admin
from .models import Client, Vehicle, Service, Order, Inventory

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "created_at"]
    search_fields = ["name", "email", "phone"]
    list_filter = ["created_at"]

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ["make", "model", "license_plate", "client"]
    search_fields = ["license_plate", "vin", "client__name"]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "duration_hours", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "client", "status", "date", "total_price"]
    search_fields = ["client__name", "id"]
    list_filter = ["status", "date"]
    date_hierarchy = "date"

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["name", "quantity", "category", "is_low_stock"]
    search_fields = ["name", "category"]
    list_filter = ["category"]
    actions = ["mark_low_stock"]
    
    def is_low_stock(self, obj):
        return "⚠️" if obj.is_low_stock() else "✅"
    
    def mark_low_stock(self, request, queryset):
        low = queryset.filter(
            quantity__lt=models.F("min_quantity")
        ).count()
        self.message_user(request, f"Знайдено {low} низьких запасів")
```

#### 8. Тестування моделей

```bash
python manage.py shell
```

```python
from myapp.models import Client, Vehicle, Service, Order, Inventory

# Створити клієнта
client = Client.objects.create(
    name="Іван Петренко",
    email="ivan@example.com",
    phone="+380671234567"
)

# Створити автомобіль
vehicle = Vehicle.objects.create(
    client=client,
    make="Toyota",
    model="Camry",
    year=2020,
    license_plate="AA1234BB",
    vin="ABC123XYZ"
)

# Створити послугу
service = Service.objects.create(
    name="Заміна масла",
    price="500.00",
    duration_hours=1
)

# Створити замовлення
order = Order.objects.create(
    client=client,
    vehicle=vehicle,
    status="new",
    date="2024-01-15",
    total_price="500.00"
)
order.service.add(service)

# Запити
all_clients = Client.objects.all()
ivan_orders = client.orders.all()
open_orders = Order.objects.filter(status="new")
```

---

### Додатковий рівень (за бажанням)

#### 1. Додати модель рейтингу (Rating)

```python
class Rating(models.Model):
    """Оцінка клієнта послуги"""
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="rating"
    )
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"⭐ {self.stars} для замовлення #{self.order.id}"
```

#### 2. Додати методи для статистики

```python
class Client(models.Model):
    # ... поля ...
    
    def get_total_orders(self):
        return self.orders.count()
    
    def get_average_rating(self):
        """Середня оцінка всіх замовлень клієнта"""
        from django.db.models import Avg
        avg = self.orders.aggregate(
            avg=Avg("rating__stars")
        )["avg"]
        return avg or 0
    
    @property
    def is_vip(self):
        """Статус VIP для постійних клієнтів"""
        return self.get_total_spent() > 10000
```

#### 3. Оптимізація запитів

```python
# Отримати замовлення з пов'язаними даними
orders = Order.objects.select_related(
    "client", "vehicle"
).prefetch_related("service")

# Замовлення з невирішеною проблемою
open_orders = Order.objects.filter(
    status="in_progress"
).select_related("client")
```

#### 4. Запити для аналізу

```python
from django.db.models import Count, Sum, Avg

# Найпопулярніша послуга
popular_services = (
    Service.objects
    .annotate(order_count=Count("orders"))
    .order_by("-order_count")
)

# Кількість замовлень по статусах
status_stats = Order.objects.values("status").annotate(
    count=Count("id")
)

# Середня вартість замовлення
avg_price = Order.objects.aggregate(
    avg=Avg("total_price")
)

# Кліліенти, що витратили більше ніж 5000
rich_clients = Client.objects.annotate(
    total_spent=Sum("orders__total_price")
).filter(total_spent__gt=5000)
```

#### 5. Тестувальний скрипт

```python
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from myapp.models import Client, Vehicle, Service, Order

# Тест 1: Створення
client = Client.objects.create(
    name="Test", email="test@test.com", phone="+380"
)
print("✓ Клієнт створений")

# Тест 2: Зв'язки
service = Service.objects.create(name="Test", price="100", duration_hours=1)
order = Order.objects.create(
    client=client, status="new", date="2024-01-01", total_price="100"
)
order.service.add(service)
print("✓ Замовлення створене")

# Тест 3: Запити
assert Client.objects.count() > 0
print("✓ Запит filter() працює")

# Тест 4: Методи
total = client.get_total_spent()
print(f"✓ Всього витрачено: {total}")

print("\nВсі тести пройшли!")
```

---

## Очікуваний результат

**Структура бази даних:**
- `myapp_client`
- `myapp_vehicle` або `myapp_patientprofile`
- `myapp_service`
- `myapp_order`
- `myapp_inventory`
- `myapp_order_service` (для ManyToMany)

**Функціональність:**
- ✅ Керування клієнтами
- ✅ Облік автомобілів / медичних карт
- ✅ Каталог послуг
- ✅ Система замовлень
- ✅ Управління складом

## Критерії оцінювання

| Критерій | Базовий | Додатковий |
|----------|---------|-----------|
| Модель Client | ✅ | - |
| Модель Vehicle / PatientProfile | ✅ | - |
| Модель Service | ✅ | - |
| Модель Order | ✅ | - |
| Модель Inventory | ✅ | - |
| ManyToMany зв'язки | ✅ | - |
| Міграції | ✅ | - |
| Адмін-панель | ✅ | - |
| Методи розрахунку | - | ✅ |
| Модель Rating | - | ✅ |
| Статистичні запити | - | ✅ |
| Оптимізація запитів | - | ✅ |

## Рекомендації

1. **Вибір:** розпочніть з одного варіанту, архітектура буде однакова
2. **ManyToMany:** використовуйте для служб замовлення (одне замовлення може мати багато послуг)
3. **Методи:** розраховуйте суми та статистику в моделях
4. **Адмін:** зареєструйте всі моделі в адмінці для керування
5. **Shell:** тестуйте всі операції CRUD перед тим, як будувати views

Успіхів у розробці! 🚗💅
