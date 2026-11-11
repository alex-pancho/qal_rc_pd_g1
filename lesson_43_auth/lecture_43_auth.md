# Заняття 43. Автентифікація та авторизація користувачів у Django

## Мета заняття

Після цього заняття ви навчитеся:

* розуміти різницю між автентифікацією та авторизацією;
* працювати зі стандартною моделлю користувача Django;
* створювати систему реєстрації користувачів;
* реалізовувати вхід та вихід із системи;
* використовувати сесії Django;
* захищати сторінки від неавторизованих користувачів;
* керувати доступом до функціональності за допомогою декораторів та дозволів.

---

# Що таке автентифікація та авторизація?

Дві ці концепції часто плутають, хоча вони виконують різні задачі.

## Автентифікація (Authentication)

Автентифікація відповідає на питання:

> **"Хто ви?"**

Користувач вводить логін і пароль.

Система перевіряє їх правильність.

Якщо вони правильні — користувач вважається автентифікованим.

Приклади:

* вхід через email і пароль;
* вхід через Google;
* вхід через Facebook;
* двофакторна автентифікація.

---

## Авторизація (Authorization)

Авторизація відповідає на питання:

> **"Що вам дозволено робити?"**

Наприклад:

| Користувач    | Може                  |
| ------------- | --------------------- |
| Гість         | лише переглядати сайт |
| Автор         | створювати статті     |
| Модератор     | редагувати коментарі  |
| Адміністратор | все                   |

Тобто користувач уже увійшов у систему, але права у всіх різні.

---

## Як це працює

```
Користувач

     │
     ▼

Вводить логін і пароль

     │
     ▼

Автентифікація

     │
     ▼

Створення сесії

     │
     ▼

Авторизація

     │
     ▼

Доступ до сторінок
```

---

# Вбудована система користувачів Django

Однією з головних переваг Django є готова система керування користувачами.

Не потрібно самостійно створювати таблицю users.

Вона вже існує.

Модель називається:

```python
django.contrib.auth.models.User
```

У базі даних автоматично створюється таблиця

```
auth_user
```

---

## Поля моделі User

Основні поля:

| Поле         | Призначення         |
| ------------ | ------------------- |
| username     | логін               |
| password     | пароль (хеш)        |
| email        | email               |
| first_name   | ім'я                |
| last_name    | прізвище            |
| is_active    | активний користувач |
| is_staff     | доступ до Admin     |
| is_superuser | адміністратор       |
| last_login   | останній вхід       |
| date_joined  | дата реєстрації     |

---

## Перегляд користувачів

Відкрийте shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

User.objects.all()
```

Створення користувача

```python
User.objects.create_user(
    username="ivan",
    password="12345",
    email="ivan@test.com"
)
```

---

# Чому пароль не зберігається відкритим?

Пароль ніколи не записується у БД як текст.

Наприклад

НІКОЛИ не буде

```
123456
```

Натомість Django збереже

```
pbkdf2_sha256$600000$...
```

Це називається **хешуванням пароля**.

Переваги:

* пароль неможливо прочитати;
* навіть адміністратор не бачить пароль;
* використовується сучасний алгоритм PBKDF2.

---

# Створення користувача правильно

Не можна писати

```python
User(
    username="ivan",
    password="12345"
)
```

Так пароль залишиться відкритим.

Потрібно використовувати

```python
User.objects.create_user(
    username="ivan",
    password="12345"
)
```

або

```python
user = User(username="ivan")
user.set_password("12345")
user.save()
```

---

# Автентифікація користувача

Для перевірки логіна використовується функція

```python
authenticate()
```

Приклад

```python
from django.contrib.auth import authenticate

user = authenticate(
    username="ivan",
    password="12345"
)

if user:
    print("Успішний вхід")
else:
    print("Неправильний пароль")
```

Функція повертає:

* User
* або None

---

# Вхід користувача

Після перевірки потрібно виконати вхід

```python
login(request, user)
```

Приклад

```python
from django.contrib.auth import authenticate, login

def user_login(request):

    user = authenticate(
        username="ivan",
        password="12345"
    )

    if user:
        login(request, user)
```

Саме після login()

створюється сесія.

---

# Вихід із системи

Для виходу використовується

```python
logout()
```

```python
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
```

Після цього

* сесія видаляється;
* користувач стає AnonymousUser.

---

# Що таке сесія?

HTTP не пам'ятає попередні запити.

Кожен запит незалежний.

Щоб сайт "пам'ятав" користувача, Django використовує **сесії**.

При вході:

```
Користувач

↓

login()

↓

створюється Session

↓

браузеру видається cookie

↓

наступні запити автоматично містять Session ID
```

---

# Cookie та Session

Cookie містить лише ідентифікатор.

Наприклад

```
sessionid=4ab97...
```

Самі дані знаходяться на сервері.

Це набагато безпечніше.

---

# Робота із session

У будь-якому представленні

```python
request.session
```

Можна записувати дані

```python
request.session["cart"] = [5, 7, 9]
```

Читати

```python
cart = request.session["cart"]
```

Або

```python
cart = request.session.get("cart")
```

---

# Стан користувача

Django автоматично додає

```python
request.user
```

Приклад

```python
def profile(request):

    print(request.user)
```

Якщо користувач увійшов

```
ivan
```

Інакше

```
AnonymousUser
```

---

# Перевірка авторизації

```python
if request.user.is_authenticated:
    print("Авторизований")
```

Перевірка гостя

```python
if request.user.is_anonymous:
    print("Гість")
```

---

# Реєстрація користувача

Створимо форму

```python
from django.contrib.auth.forms import UserCreationForm
```

View

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )
```

---

# Шаблон реєстрації

```html
<h2>Реєстрація</h2>

<form method="post">

    {% csrf_token %}

    {{ form.as_p }}

    <button>Зареєструватися</button>

</form>
```

---

# Вхід користувача через LoginView

Django вже містить готове представлення

```python
LoginView
```

urls.py

```python
from django.contrib.auth.views import LoginView

urlpatterns = [

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

]
```

Шаблон

```
registration/login.html
```

---

# Вихід користувача

```python
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    )

]
```

---

# Захист сторінок

Найпростіший спосіб

```python
@login_required
```

```python
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):

    return render(
        request,
        "profile.html"
    )
```

Гість побачити сторінку вже не зможе.

---

# Куди перенаправляється користувач?

За замовчуванням

```
/accounts/login/
```

Краще налаштувати

```python
LOGIN_URL = "login"
```

settings.py

```python
LOGIN_REDIRECT_URL = "profile"

LOGOUT_REDIRECT_URL = "login"
```

---

# Декоратор permission_required

Іноді потрібно перевірити не лише факт входу, а й права.

```python
from django.contrib.auth.decorators import permission_required

@permission_required(
    "blog.add_post"
)
def create_post(request):
    ...
```

---

# Перевірка груп

```python
if request.user.groups.filter(
    name="Managers"
).exists():

    print("Менеджер")
```

---

# Захист функціональності

Наприклад

| Сторінка         | Доступ            |
| ---------------- | ----------------- |
| Головна          | усі               |
| Каталог          | усі               |
| Профіль          | лише авторизовані |
| Створення статті | Автор             |
| Admin            | Адміністратор     |

Саме так зазвичай будуються сучасні веб-застосунки.

---

# Типовий процес роботи користувача

1. Відкрити сторінку реєстрації.
2. Створити обліковий запис.
3. Увійти в систему.
4. Django створює сесію.
5. Користувач відкриває захищені сторінки.
6. Натискає «Вийти».
7. Сесія видаляється.

---

# Типові помилки початківців

### Зберігають пароль відкритим

```python
user.password = "12345"
```

Потрібно

```python
user.set_password("12345")
```

---

### Забувають CSRF

У формах обов'язково

```html
{% csrf_token %}
```

---

### Забувають login()

Після authenticate()

потрібно виконати

```python
login(request, user)
```

Інакше користувач не увійде до системи.

---

### Не захищають сторінки

Якщо забути

```python
@login_required
```

будь-хто зможе відкрити URL.

---

# Найкращі практики

* Ніколи не зберігайте пароль у відкритому вигляді.
* Використовуйте вбудовану модель `User`.
* Для реєстрації застосовуйте `UserCreationForm`.
* Для входу та виходу використовуйте `LoginView` і `LogoutView`.
* Захищайте приватні сторінки декоратором `@login_required`.
* Використовуйте групи та дозволи для розмежування доступу.
* Не зберігайте конфіденційні дані в сесіях.
* Налаштуйте `LOGIN_URL`, `LOGIN_REDIRECT_URL` і `LOGOUT_REDIRECT_URL`.

# Підсумок

На цьому занятті ми ознайомилися з повним циклом роботи системи автентифікації Django. Ви навчилися використовувати вбудовану модель користувача, реєструвати нових користувачів, виконувати вхід і вихід із системи, працювати із сесіями та захищати сторінки від неавторизованого доступу. Ці можливості є фундаментом для створення будь-якого сучасного веб-застосунку, де потрібні персональні кабінети, ролі користувачів і контроль доступу.
