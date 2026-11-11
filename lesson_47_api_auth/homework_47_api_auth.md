# Заняття 47. Домашнє завдання
## REST API: Автентифікація, Дозволи та Тестування

---

# Загальні вимоги

На цьому занятті всі три проєкти отримують один і той же набір вимог:

1. **Token Authentication / JWT** — вибрати на свій розсуд
2. **Permissions** — стандартні DRF + кастомні для власника
3. **Swagger документація** — интерактивна документація API
4. **Тестування в Postman** — мінімум 10 запитів
5. **Автоматизовані тести** — pytest-django з мінімум 15 тестів

---

# 📋 Проєкт 1: Task & Bug Manager

## Задача

Захистити REST API для управління задачами, багами та тест-кейсами.

---

## Base (Обов'язковий рівень)

### 1. Встановити Token Authentication

```python
# settings.py
INSTALLED_APPS += ["rest_framework.authtoken"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ]
}
```

Виконати міграцію:
```bash
python manage.py migrate
```

### 2. Отримання токена через API

Додати URL у `urls.py`:
```python
from rest_framework.authtoken.views import obtain_auth_token

path("api/token/", obtain_auth_token),
```

Користувач может отримати токен:
```
POST /api/token/
{
    "username": "vasyl",
    "password": "secret123"
}
```

### 3. Додати Permissions до ViewSet

```python
# views.py
from rest_framework.permissions import IsAuthenticated

class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

### 4. Встановити Swagger

```bash
pip install drf-spectacular
```

```python
# settings.py
INSTALLED_APPS += ["drf_spectacular"]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```

```python
# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view()),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
```

### 5. Тестування в Postman

Мінімум 10 запитів:
- ❌ GET /api/issues/ без токена → 401
- ✅ POST /api/token/ → отримання токена
- ✅ GET /api/issues/ з токеном → список задач
- ✅ POST /api/issues/ → створення нової задачі (автор = поточний юзер)
- ✅ GET /api/issues/1/ → одна задача
- ✅ PATCH /api/issues/1/ → редагування своєї задачи
- ✅ DELETE /api/issues/1/ → видалення своєї задачи
- ❌ POST /api/issues/2/ від іншого користувача → 403
- ✅ Swagger на /api/docs/ доступний

Експортувати колекцію Postman у файл `postman_collection_issues.json`.

### 6. Автоматизовані тести (pytest-django)

```bash
pip install pytest pytest-django
```

Файл `pytest.ini`:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
testpaths = tests
```

Написати мінімум **15 тестів**:

**Файл `tests/test_issues_auth.py`**

```python
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from app.models import Issue

@pytest.fixture
def user(db):
    return User.objects.create_user(username="vasyl", password="secret")

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_get_issues_unauthorized(api_client):
    """Неавторизований користувач отримує 401"""
    response = api_client.get("/api/issues/")
    assert response.status_code == 401

@pytest.mark.django_db
def test_get_issues_authorized(api_client, user):
    """Авторизований користувач отримує список"""
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/issues/")
    assert response.status_code == 200
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_create_issue(api_client, user):
    """Користувач может створити задачу"""
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/api/issues/",
        {
            "title": "Fix login bug",
            "issue_type": "Bug",
            "status": "Open",
        },
        format="json"
    )
    assert response.status_code == 201
    assert response.data["owner"] == user.id

@pytest.mark.django_db
def test_update_own_issue(api_client, user):
    """Користувач может редагувати свою задачу"""
    api_client.force_authenticate(user=user)
    
    # Створюємо
    create_resp = api_client.post(
        "/api/issues/",
        {"title": "Original", "issue_type": "Task"},
        format="json"
    )
    issue_id = create_resp.data["id"]
    
    # Редагуємо
    response = api_client.patch(
        f"/api/issues/{issue_id}/",
        {"title": "Updated"},
        format="json"
    )
    assert response.status_code == 200
    assert response.data["title"] == "Updated"

@pytest.mark.django_db
def test_cannot_update_others_issue(api_client):
    """Користувач не может редагувати чужу задачу"""
    vasyl = User.objects.create_user(username="vasyl", password="123")
    petro = User.objects.create_user(username="petro", password="123")
    
    # Vasyl創builds issue
    issue = Issue.objects.create(
        title="Bug",
        issue_type="Bug",
        owner=vasyl
    )
    
    # Petro намагається редагувати
    api_client.force_authenticate(user=petro)
    response = api_client.patch(
        f"/api/issues/{issue.id}/",
        {"title": "Hacked"},
        format="json"
    )
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_own_issue(api_client, user):
    """Користувач може видалити свою задачу"""
    api_client.force_authenticate(user=user)
    
    create_resp = api_client.post(
        "/api/issues/",
        {"title": "To delete", "issue_type": "Task"},
        format="json"
    )
    issue_id = create_resp.data["id"]
    
    response = api_client.delete(f"/api/issues/{issue_id}/")
    assert response.status_code == 204

@pytest.mark.django_db
def test_issue_not_found(api_client, user):
    """Звернення до неіснуючої задачи повертає 404"""
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/issues/99999/")
    assert response.status_code == 404

# Ще 7+ тестів на ваш розсуд:
# - тест отримання токена
# - тест з невірним паролем
# - тест зміни статусу
# - тест фільтрації за типом
# - тест поправок з невірними даними
# тощо
```

### 7. Результат

У репозиторії мають бути:
- ✅ `requirements.txt` з усіма залежностями
- ✅ Папка `tests/` з тестами
- ✅ Файл `postman_collection_issues.json` з запитами
- ✅ README розтлумачує, як запустити тести: `pytest -v`

---

## Advanced (Додатковий рівень)

### JWT замість Token Authentication

Замінити Token на JWT:

```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}
```

```python
# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

path("api/token/", TokenObtainPairView.as_view()),
path("api/token/refresh/", TokenRefreshView.as_view()),
```

Тест отримання JWT:

```python
@pytest.mark.django_db
def test_obtain_jwt_token():
    User.objects.create_user(username="vasyl", password="secret")
    
    api_client = APIClient()
    response = api_client.post(
        "/api/token/",
        {"username": "vasyl", "password": "secret"},
        format="json"
    )
    
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
```

### Кастомна дозвіл для власника

```python
# permissions.py
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.owner == request.user
```

### 25+ тестів

Розширити набір тестів на 25+ (охопити усі ендпоінти та граничні випадки).

### Bonus: API для коментарів

Додати Comments у API:

```python
class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

Додати 10+ тестів для Comments API.

---

## Bonus (За спеціальні 🌟)

- ✅ Додати фільтрацію за statuses через query-параметри
- ✅ Додати пошук за title за допомогою `/api/issues/?search=bug`
- ✅ Додати сортування за created_at
- ✅ Документувати API у README з прикладами curl-запитів
- ✅ Додати GitHub Actions для запуску тестів на кожен push

---

---

# 💰 Проєкт 2: Expense & Budget Tracker

## Задача

Захистити REST API для управління доходами, витратами та бюджетами.

---

## Base (Обов'язковий рівень)

### 1. Встановити JWT (рекомендовано для фінансових даних)

```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ]
}
```

### 2. Додати ендпоінти для токенів

```python
# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
```

### 3. Permissions для транзакцій

```python
class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Користувач бачить лише свої транзакції
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

### 4. Swagger

```bash
pip install drf-spectacular
```

```python
# settings.py
INSTALLED_APPS += ["drf_spectacular"]
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# urls.py
path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
```

### 5. Тестування в Postman

Мінімум 10 запитів:
- ✅ POST /api/token/ → отримання access + refresh токенів
- ✅ GET /api/transactions/ → список своїх транзакцій
- ✅ POST /api/transactions/ → додавання витрати
- ✅ POST /api/transactions/ → додавання доходу
- ✅ GET /api/transactions/{id}/ → деталі однієї транзакції
- ✅ PATCH /api/transactions/{id}/ → редагування своєї транзакції
- ✅ DELETE /api/transactions/{id}/ → видалення своєї
- ❌ Спроба доступу до чужої транзакції → 404
- ✅ POST /api/token/refresh/ → оновлення токена
- ✅ GET /api/budgets/ → список бюджетів

Експортувати: `postman_collection_transactions.json`

### 6. Автоматизовані тести (мінімум 15)

```python
# tests/test_transactions.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from app.models import Transaction

@pytest.fixture
def user(db):
    return User.objects.create_user(username="mykola", password="secret")

@pytest.mark.django_db
def test_transaction_list_requires_auth():
    """Без авторизації → 401"""
    client = APIClient()
    response = client.get("/api/transactions/")
    assert response.status_code == 401

@pytest.mark.django_db
def test_create_transaction(db):
    user = User.objects.create_user(username="mykola", password="secret")
    client = APIClient()
    client.force_authenticate(user=user)
    
    response = client.post(
        "/api/transactions/",
        {
            "amount": 1000,
            "transaction_type": "income",
            "category": "Salary",
        },
        format="json"
    )
    
    assert response.status_code == 201
    assert response.data["user"] == user.id

@pytest.mark.django_db
def test_user_sees_only_own_transactions():
    """Користувач бачить лише свої транзакції"""
    mykola = User.objects.create_user(username="mykola", password="123")
    oksana = User.objects.create_user(username="oksana", password="123")
    
    # Mykola創建
    Transaction.objects.create(
        user=mykola,
        amount=1000,
        transaction_type="income"
    )
    
    # Oksana創建
    Transaction.objects.create(
        user=oksana,
        amount=500,
        transaction_type="expense"
    )
    
    # Mykola дивиться список
    client = APIClient()
    client.force_authenticate(user=mykola)
    response = client.get("/api/transactions/")
    
    assert len(response.data) == 1
    assert response.data[0]["user"] == mykola.id

@pytest.mark.django_db
def test_obtain_jwt_token():
    """Користувач отримує JWT"""
    User.objects.create_user(username="mykola", password="secret")
    
    client = APIClient()
    response = client.post(
        "/api/token/",
        {"username": "mykola", "password": "secret"},
        format="json"
    )
    
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_invalid_credentials():
    """Неправильний пароль → 401"""
    User.objects.create_user(username="mykola", password="secret")
    
    client = APIClient()
    response = client.post(
        "/api/token/",
        {"username": "mykola", "password": "wrong"},
        format="json"
    )
    
    assert response.status_code == 401

@pytest.mark.django_db
def test_update_own_transaction():
    """Редагування своєї транзакції"""
    user = User.objects.create_user(username="mykola", password="123")
    trans = Transaction.objects.create(
        user=user,
        amount=1000,
        category="Food"
    )
    
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.patch(
        f"/api/transactions/{trans.id}/",
        {"amount": 1500},
        format="json"
    )
    
    assert response.status_code == 200
    assert response.data["amount"] == "1500.00"

@pytest.mark.django_db
def test_delete_transaction():
    """Видалення своєї транзакції"""
    user = User.objects.create_user(username="mykola", password="123")
    trans = Transaction.objects.create(user=user, amount=100)
    
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete(f"/api/transactions/{trans.id}/")
    
    assert response.status_code == 204
    assert not Transaction.objects.filter(id=trans.id).exists()

# Ще 7+ тестів:
# - тест фільтрації за типом
# - тест калькуляції балансу
# - тест бюджету
# - тест перевищення бюджету
# - тест сортування
# - тест експорту в CSV
# тощо
```

### 7. Результат

- ✅ `requirements.txt`
- ✅ Папка `tests/` з 15+ тестами
- ✅ `postman_collection_transactions.json`
- ✅ README з інструкціями

---

## Advanced

### Фільтрація й пошук

```python
class TransactionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['transaction_type', 'category']
    search_fields = ['category', 'description']
    ordering_fields = ['date', 'amount']
```

### Розрахунки й аналітика

Додати ендпоінт для місячного звіту:

```python
@action(detail=False, methods=['get'])
def monthly_report(self, request):
    # Розрахунок доходів, витрат, балансу за місяць
    ...
```

### 25+ тестів

---

## Bonus

- ✅ API для категорій
- ✅ API для бюджетів
- ✅ Вебхук для сповіщень при перевищенні бюджету
- ✅ Інтеграція з Exchange API для конвертації валют
- ✅ GitHub Actions

---

---

# 🏢 Проєкт 3: Service Management System

## Задача

Захистити REST API для управління клієнтами, замовленнями та послугами (за вибором: Auto Service або Beauty Clinic).

---

## Base (Обов'язковий рівень)

### 1. Token або JWT Authentication

Вибрати на свій розсуд. Рекомендується **Token** для простоти.

```python
# settings.py
INSTALLED_APPS += ["rest_framework.authtoken"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ]
}
```

### 2. Отримання токена

```python
# urls.py
from rest_framework.authtoken.views import obtain_auth_token
path("api/token/", obtain_auth_token),
```

### 3. Кастомна дозвіл для員員

```python
# permissions.py
from rest_framework.permissions import BasePermission

class IsStaffOrAdmin(BasePermission):
    """Лише сотрудники (персонал) й адміни"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
```

Використання:

```python
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]
```

### 4. Різні дозволи для різних операцій

```python
class ClientViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    # Створення й редагування доступні сотрудникам
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Лише персонал може додавати клієнтів")
        return super().create(request, *args, **kwargs)
```

### 5. Swagger

```bash
pip install drf-spectacular
```

Додати у `urls.py`:

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view()),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
```

### 6. Тестування в Postman (10+ запитів)

- ✅ Отримання токена (staff користувач)
- ✅ GET /api/clients/ → список клієнтів
- ✅ POST /api/clients/ → додавання нового клієнта
- ✅ GET /api/orders/ → список замовлень
- ✅ POST /api/orders/ → створення замовлення
- ✅ PATCH /api/orders/{id}/status/ → зміна статусу
- ✅ GET /api/services/ → список послуг
- ✅ POST /api/services/ → додавання послуги (тільки адміни)
- ❌ Спроба доступу неавторизованого → 401
- ❌ Звичайний користувач намагається додати клієнта → 403

Експортувати: `postman_collection_service_management.json`

### 7. Автоматизовані тести (мінімум 15)

```python
# tests/test_service_api.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from app.models import Client, Order

@pytest.fixture
def staff_user(db):
    user = User.objects.create_user(
        username="ivan",
        password="secret",
        is_staff=True
    )
    return user

@pytest.fixture
def regular_user(db):
    return User.objects.create_user(username="petro", password="secret")

@pytest.mark.django_db
def test_unauthorized_cannot_access():
    """Неавторизований користувач отримує 401"""
    client = APIClient()
    response = client.get("/api/clients/")
    assert response.status_code == 401

@pytest.mark.django_db
def test_regular_user_cannot_create_client(regular_user):
    """Звичайний користувач не може додати клієнта"""
    client = APIClient()
    client.force_authenticate(user=regular_user)
    
    response = client.post(
        "/api/clients/",
        {"name": "Vasyl", "phone": "380501234567"},
        format="json"
    )
    
    assert response.status_code == 403

@pytest.mark.django_db
def test_staff_can_create_client(staff_user):
    """Сотрудник может додати клієнта"""
    client = APIClient()
    client.force_authenticate(user=staff_user)
    
    response = client.post(
        "/api/clients/",
        {"name": "Vasyl", "phone": "380501234567"},
        format="json"
    )
    
    assert response.status_code == 201

@pytest.mark.django_db
def test_get_clients_list(staff_user):
    """Список клієнтів доступний авторизованим"""
    Client.objects.create(name="Vasyl", phone="380501234567")
    
    client = APIClient()
    client.force_authenticate(user=staff_user)
    response = client.get("/api/clients/")
    
    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_create_order(staff_user):
    """Створення замовлення"""
    client_obj = Client.objects.create(
        name="Vasyl",
        phone="380501234567"
    )
    
    client = APIClient()
    client.force_authenticate(user=staff_user)
    
    response = client.post(
        "/api/orders/",
        {
            "client": client_obj.id,
            "status": "Pending",
            "total_price": 5000,
        },
        format="json"
    )
    
    assert response.status_code == 201

@pytest.mark.django_db
def test_update_order_status(staff_user):
    """Зміна статусу замовлення"""
    client_obj = Client.objects.create(name="Vasyl", phone="380501")
    order = Order.objects.create(
        client=client_obj,
        status="Pending"
    )
    
    client = APIClient()
    client.force_authenticate(user=staff_user)
    
    response = client.patch(
        f"/api/orders/{order.id}/",
        {"status": "Completed"},
        format="json"
    )
    
    assert response.status_code == 200
    assert response.data["status"] == "Completed"

@pytest.mark.django_db
def test_delete_client(staff_user):
    """Видалення клієнта"""
    client_obj = Client.objects.create(name="Vasyl", phone="380501")
    
    client = APIClient()
    client.force_authenticate(user=staff_user)
    
    response = client.delete(f"/api/clients/{client_obj.id}/")
    assert response.status_code == 204

# Ще 7+ тестів:
# - тест фільтрації замовлень
# - тест сортування
# - тест пошуку клієнтів
# - тест відстеження інвентарю
# - тест сповіщень
# тощо
```

### 8. Результат

- ✅ `requirements.txt`
- ✅ Папка `tests/` з 15+ тестами
- ✅ `postman_collection_service_management.json`
- ✅ README

---

## Advanced

### Фільтрація за статусом

```python
class OrderViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'client', 'created_at']
```

### Анотація для статистики

```python
@action(detail=False, methods=['get'])
def statistics(self, request):
    total_orders = Order.objects.count()
    completed = Order.objects.filter(status='Completed').count()
    return Response({
        'total': total_orders,
        'completed': completed,
    })
```

### 25+ тестів

---

## Bonus

- ✅ API для запису на послугу (booking calendar)
- ✅ API для інвентарю (низькі запаси)
- ✅ Сповіщення клієнтам
- ✅ Експорт у PDF
- ✅ GitHub Actions

---

---

# 📝 Загальні інструкції для всіх проєктів

## Структура кода

```
your_project/
├── manage.py
├── requirements.txt
├── pytest.ini
├── README.md
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── app/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   └── urls.py
│
├── tests/
│   ├── conftest.py
│   ├── test_authentication.py
│   ├── test_permissions.py
│   ├── test_api.py
│   └── test_edge_cases.py
│
└── postman/
    └── collection.json
```

## requirements.txt

```
Django==4.2
djangorestframework==3.14
djangorestframework-simplejwt==5.2
drf-spectacular==0.26
pytest==7.3
pytest-django==4.5
```

## Запуск тестів

```bash
# Всі тести
pytest

# З покриттям
pip install pytest-cov
pytest --cov=app tests/

# Конкретний файл
pytest tests/test_api.py -v
```

## Запуск сервера

```bash
python manage.py runserver
```

Swagger буде на: `http://localhost:8000/api/docs/`

## Завантаження на GitHub

```bash
git add .
git commit -m "feat: Add DRF authentication, permissions, and tests (lesson 47)"
git push origin main
```

---

# ✅ Чеклист перед здачею

Для кожного проєкту перевірити:

- [ ] ✅ Встановлена Token Authentication або JWT
- [ ] ✅ Додана ендпоінт для отримання токена
- [ ] ✅ ViewSets мають `permission_classes`
- [ ] ✅ Додана Swagger документація
- [ ] ✅ Тестовані в Postman мінімум 10 запитів
- [ ] ✅ Написано мінімум 15 тестів
- [ ] ✅ Всі тести проходять: `pytest -v`
- [ ] ✅ Синтаксис коректний: `python manage.py check`
- [ ] ✅ Міграції застосовані: `python manage.py migrate`
- [ ] ✅ README описує як запустити
- [ ] ✅ `postman_collection.json` експортован
- [ ] ✅ Все завантажено на GitHub

---

# 🎯 Підсумок

На цьому занятті всі три проєкти отримали:

✅ **Безпеку** — Token / JWT автентифікація

✅ **Контроль доступу** — DRF Permissions

✅ **Документацію** — Swagger на `/api/docs/`

✅ **Тестування** — Postman + pytest-django

✅ **Production-ready код** — готов до дійсного використання

Успіхів у розробці! 🚀