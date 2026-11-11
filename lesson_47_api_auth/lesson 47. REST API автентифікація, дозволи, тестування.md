# Конспект заняття 47. REST API в Django: автентифікація, дозволи та тестування

*Матеріал для читання й повторення після заняття. Читайте з відкритим проєктом і пробуйте кожен приклад самі.*

## Про що це заняття

На занятті 46 ми зробили повний CRUD API: створення, читання, оновлення й видалення постів. Але є проблема: **будь-хто в інтернеті може змінити або видалити будь-який пост**. Сьогодні ми додаємо захист і перевіряємо його тестами.

Ми навчимося:

- розрізняти коди 401 і 403;
- отримувати токен і викликати API з ним;
- обмежувати дії за допомогою дозволів (permissions), зокрема «змінювати може лише автор»;
- перевіряти автентифікацію й дозволи автотестами;
- замінювати прямі виклики до бази на виклики API.

## Що потрібно мати перед початком

- Результат заняття 46: `PostViewSet` (`ModelViewSet`) зареєстрований у роутері, API працює за `/api/posts/` і `/api/posts/{id}/`.
- У прикладах застосунок називається `polls`, а клас API лежить у файлі `api_models.py` (так він називається у проєкті, хоча там views).
- Двоє звичайних користувачів, створених через адмінку. У прикладах це `alice` і `bob`.
- Сервер на порту 5000. Якщо у вас інший, замініть.
- У PowerShell на Windows команда `curl` є аліасом іншої команди, тому використовуйте `curl.exe` або Postman.

## 1. Проблема: відкрите API

Спробуйте створити пост без жодного входу:

```bash
curl -i -X POST http://127.0.0.1:5000/api/posts/ -H "Content-Type: application/json" -d '{"title": "Тест", "content": "Текст"}'
```

У відповіді буде 201, і пост створено. Так само без входу можна видалити будь-який пост. Сервер просто не питає, хто ви. Тому нам потрібні два шари захисту: **автентифікація** і **дозволи**.

## 2. Автентифікація і дозволи: 401 та 403

Це дві різні речі, які ми розбирали ще на занятті 5.5:

- **автентифікація** відповідає на питання «хто ти?»;
- **авторизація (дозволи)** відповідає на питання «що тобі можна?».

Це відображається в кодах відповіді:

| Код | Назва | Значення |
| --- | --- | --- |
| 401 | Unauthorized | Сервер не знає, хто ви. Потрібно представитися (увійти, надіслати токен) |
| 403 | Forbidden | Сервер знає, хто ви, але ця дія вам заборонена |

Щоб запам'ятати: **401 — «хто ви?»**, **403 — «я вас знаю, але ні»**.

## 3. Способи автентифікації в DRF

| Спосіб | Як працює | Для чого |
| --- | --- | --- |
| Session | Після входу браузер зберігає cookie із сесією | Сайт у браузері, адмінка, Swagger |
| Token | Клієнт надсилає в заголовку `Authorization: Token <ключ>` | Мобільні застосунки, скрипти, інші сервіси |
| Basic | Логін і пароль у заголовку, закодовані в base64 | Лише для швидких тестів і лише через HTTPS |
| JWT | Токен із вбудованими даними і терміном дії | Великі проєкти (ми це не робимо, лише знайте, що існує) |

Два важливі застереження:

- Base64 — це **не шифрування**, а кодування. Його легко розкодувати.
- Токен — це як пароль. Його не публікують у чатах і не додають у git.

## 4. Токен: налаштування й використання

**Крок 1. Налаштування.** У `settings.py` додайте застосунок токенів і вкажіть способи автентифікації:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    # Наявні ключі (наприклад, DEFAULT_SCHEMA_CLASS для Swagger) залишаємо!
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

У вашому `REST_FRAMEWORK` уже можуть бути інші ключі, наприклад для Swagger. Не замінюйте весь словник, а додайте до нього, інакше документація зламається.

Порядок у списку має значення. Для відповіді 401 DRF бере заголовок `WWW-Authenticate` від **першого** класу автентифікації. У `SessionAuthentication` такого заголовка немає, тому якби вона стояла першою, ви отримали б 403 замість 401. Тому `TokenAuthentication` ставимо першою.

**Крок 2. Міграція.** Застосунок токенів має власну таблицю в базі:

```bash
python manage.py migrate
```

**Крок 3. Адреса для отримання токена.** У `polls/urls.py`:

```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # ...наявні маршрути...
    path('api/token/', obtain_auth_token, name='api-token'),
]
```

**Крок 4. Отримуємо токен і використовуємо його.**

```bash
# Отримати токен за логіном і паролем
curl -i -X POST http://127.0.0.1:5000/api/token/ -H "Content-Type: application/json" -d '{"username": "alice", "password": "ПАРОЛЬ"}'
# У відповіді: {"token": "<довгий рядок>"}

# Викликати API з токеном
curl -i http://127.0.0.1:5000/api/posts/ -H "Authorization: Token ВАШ_ТОКЕН"
```

Зверніть увагу на заголовок: слово `Token`, пробіл і ключ. Якщо ввести неправильний пароль під час отримання токена, ви отримаєте 400 із повідомленням, що увійти не вдалося.

Якщо токен витік, його можна видалити в розділі «Tokens» адмінки.

## 5. Дозволи: IsAuthenticatedOrReadOnly

Дозволи визначають, що **можна** зробити тому, кого сервер уже впізнав. Підключимо перший дозвіл у `polls/api_models.py`:

```python
from rest_framework import permissions, viewsets

from .models import BlogPost
from .serializers import BlogPostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

Основні дозволи DRF:

| Клас | Що дозволяє |
| --- | --- |
| `AllowAny` | Усім |
| `IsAuthenticated` | Лише тим, хто увійшов |
| `IsAuthenticatedOrReadOnly` | Читати всім, змінювати лише тим, хто увійшов |
| `IsAdminUser` | Лише користувачам із прапорцем `is_staff` |

«Читання» означає безпечні методи: GET, HEAD, OPTIONS. Вони не змінюють дані.

Тепер результат такий:

| Запит | Без входу | З токеном |
| --- | --- | --- |
| GET /api/posts/ | 200 | 200 |
| POST /api/posts/ | 401 | 201 |
| PATCH /api/posts/{id}/ | 401 | 200 |
| DELETE /api/posts/{id}/ | 401 | 204 |

Перші проблеми розв'язано, але лишилася одна: з токеном Боба можна видалити пост Аліси. Дозвіл перевіряє лише те, чи ви увійшли, а не чи це ваш пост. Це наступна тема.

## 6. Автор і об'єктні дозволи

Нам потрібне правило: **змінювати й видаляти пост може лише його автор**. Для цього в моделі має бути поле автора.

**Крок 1. Поле автора в моделі** (`polls/models.py`):

```python
from django.conf import settings
from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
```

Поле `null=True`, бо в базі вже є пости без автора. Без цього міграція не пройде. Після зміни моделі створіть і застосуйте міграцію:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Крок 2. Автор не приходить від клієнта.** У `polls/serializers.py`:

```python
class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = ['author']
```

Інакше будь-хто зміг би створити пост від імені іншого користувача, просто вказавши `author` у запиті. Тепер автора підставляє сервер.

**Крок 3. Сервер підставляє автора при створенні.** У `polls/api_models.py`:

```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

Метод `perform_create` DRF викликає перед збереженням нового запису. Тут ми беремо користувача з `request.user`. Це той, кого DRF визначив за токеном або сесією.

**Крок 4. Власний дозвіл.** Створіть файл `polls/permissions.py`:

```python
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
```

І додайте в `api_models.py` імпорт: `from .permissions import IsAuthorOrReadOnly`.

У класі дозволу є два методи. `has_permission` перевіряє запит загалом, а `has_object_permission` перевіряє конкретний запис (чи може саме цей користувач чіпати саме цей пост). Ми використали другий.

Тепер результат виглядає так:

| Запит | Без входу | Боб (чужий пост) | Аліса (автор) |
| --- | --- | --- | --- |
| GET /api/posts/{id}/ | 200 | 200 | 200 |
| PATCH /api/posts/{id}/ | 401 | 403 | 200 |
| DELETE /api/posts/{id}/ | 401 | 403 | 204 |

Зверніть увагу: старі пости без автора тепер не зможе змінити ніхто через API (крім адмінки), бо `None` не дорівнює жодному користувачу. Для експериментів створюйте нові пости через API.

## 7. Автотести автентифікації та дозволів

Після додавання дозволів тести із заняття 46 почнуть падати з кодом 401, бо вони працювали без входу. Це нормально: тести виявили зміну поведінки. Виправляємо `setUp`:

```python
# polls/tests.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import BlogPost

User = get_user_model()


class PostApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', password='pass12345')
        self.client.force_authenticate(user=self.user)
        self.post = BlogPost.objects.create(
            title='Старий', content='Текст', author=self.user
        )
        self.list_url = '/api/posts/'
        self.detail_url = f'/api/posts/{self.post.pk}/'
    # ...решта тестів із заняття 46 залишається без змін
```

Пост створюється з `author=self.user`, інакше PATCH і DELETE у цих тестах поверталиби 403.

Тепер нові тести для автентифікації та дозволів:

```python
class PostPermissionTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user('alice', password='pass12345')
        self.bob = User.objects.create_user('bob', password='pass12345')
        self.post = BlogPost.objects.create(
            title='Пост Аліси', content='Текст', author=self.alice
        )
        self.list_url = '/api/posts/'
        self.detail_url = f'/api/posts/{self.post.pk}/'

    def test_anonymous_can_read(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create(self):
        data = {'title': 'Х', 'content': 'Х'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_sets_author(self):
        self.client.force_authenticate(user=self.bob)
        data = {'title': 'Пост Боба', 'content': 'Текст'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], self.bob.pk)

    def test_other_user_cannot_edit(self):
        self.client.force_authenticate(user=self.bob)
        response = self.client.patch(self.detail_url, {'title': 'Хак'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_edit(self):
        self.client.force_authenticate(user=self.alice)
        response = self.client.patch(self.detail_url, {'title': 'Нове'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_delete(self):
        self.client.force_authenticate(user=self.bob)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_delete(self):
        self.client.force_authenticate(user=self.alice)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_token_endpoint_returns_token(self):
        creds = {'username': 'alice', 'password': 'pass12345'}
        response = self.client.post('/api/token/', creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_wrong_password_returns_400(self):
        creds = {'username': 'alice', 'password': 'wrong'}
        response = self.client.post('/api/token/', creds, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_header_allows_create(self):
        token = Token.objects.create(user=self.bob)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {'title': 'Через токен', 'content': 'Текст'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

Запуск: `python manage.py test polls -v 2`.

В тестах ми використовуємо два способи автентифікації, і вони відповідають на різні питання:

- `force_authenticate(user=...)` повністю обходить автентифікацію й одразу «вмикає» користувача. Це зручно, щоб перевіряти **дозволи**.
- `client.credentials(HTTP_AUTHORIZATION='Token ...')` додає справжній заголовок. Так ми перевіряємо, що **автентифікація за токеном** справді працює.

Корисна вправа: тимчасово приберіть `IsAuthorOrReadOnly` з `permission_classes` і запустіть тести. Впадуть `test_other_user_cannot_edit` і `test_other_user_cannot_delete`. Поверніть дозвіл, і вони знову зелені. Так видно, що тести справді охороняють правило безпеки.

## 8. Заміна викликів ORM на API

У проєкті є view `blogpost`, яке саме створює й редагує записи через ORM та форму `BlogForm`. Покажемо, як перейти на API.

| Було (view працює з ORM) | Стало (сторінка викликає API) |
| --- | --- |
| `BlogPost.objects.all()` | `GET /api/posts/` |
| `BlogPost.objects.get(id=post_id)` | `GET /api/posts/{id}/` |
| `BlogPost.objects.create(title=..., content=...)` | `POST /api/posts/` |
| `post.title = ...; post.save()` | `PATCH /api/posts/{id}/` |
| `post.delete()` | `DELETE /api/posts/{id}/` |

**Навіщо це.** Правила перевірки даних тепер живуть в одному місці. Раніше `BlogForm` дозволяв заголовок до 100 символів, а модель до 200, тобто це були дві різні перевірки для одного поля. Після переходу на API правило одне, у серіалізаторі. До того ж ті самі дані зможуть використовувати мобільний застосунок і скрипти.

**Крок 1. Спрощуємо view** (`polls/views.py`). Усе, що працювало з ORM і `BlogForm`, видаляємо:

```python
def blogpost(request, post_id=None):
    return render(request, 'blogpost.html', {'post_id': post_id})
```

Тепер view лише відкриває сторінку. Якщо `BlogForm`, `BlogPost` і `HttpResponse` у `views.py` більше не використовуються, приберіть їхні імпорти.

**Крок 2. Маршрути** (`polls/urls.py`). Додаємо маршрут для редагування і прибираємо дублікат `login/blogpost/`, який має те саме ім'я:

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('blogpost/', views.blogpost, name='blogpost'),
    path('blogpost/<int:post_id>/', views.blogpost, name='blogpost-edit'),
    # ...решта маршрутів...
]
```

**Крок 3. Шаблон** (`blogpost.html`). Замініть розмітку форми на таку:

```html
<form id="post-form">
  {% csrf_token %}
  <p><input id="title" type="text" maxlength="200" placeholder="Заголовок" required></p>
  <p><textarea id="content" rows="8" placeholder="Текст" required></textarea></p>
  <button type="submit">Зберегти</button>
</form>
<p id="message"></p>

<script>
  const postId = {{ post_id|default:"null" }};
  const form = document.getElementById('post-form');
  const message = document.getElementById('message');
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const url = postId ? `/api/posts/${postId}/` : '/api/posts/';

  async function loadPost() {
    if (!postId) return;
    const response = await fetch(url);
    if (response.ok) {
      const post = await response.json();
      document.getElementById('title').value = post.title;
      document.getElementById('content').value = post.content;
    } else {
      message.textContent = `Не вдалося завантажити пост (код ${response.status})`;
    }
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const response = await fetch(url, {
      method: postId ? 'PATCH' : 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        title: document.getElementById('title').value,
        content: document.getElementById('content').value,
      }),
    });

    if (response.ok) {
      message.textContent = 'Збережено';
      if (!postId) form.reset();
    } else if (response.status === 401 || response.status === 403) {
      message.textContent = 'Немає прав. Увійдіть під своїм користувачем або це не ваш пост.';
    } else {
      message.textContent = 'Помилка: ' + JSON.stringify(await response.json());
    }
  });

  loadPost();
</script>
```

Що тут відбувається:

- Сторінка сама звертається до API через `fetch`. Це і є «виклик API замість виклику ORM».
- Браузер надсилає cookie сесії, тому користувач, який увійшов, автентифікується через `SessionAuthentication`.
- Для POST, PATCH і DELETE від користувача із сесією DRF вимагає CSRF-токен. Ми беремо його з прихованого поля `{% csrf_token %}` і передаємо в заголовку `X-CSRFToken`. Без цього буде 403.
- Відповідь API обробляємо за кодом: `ok` — успіх, 401 або 403 — немає прав, інше — помилки валідації (400).

Перевірте результат у браузері: увійдіть через `/login/`, відкрийте `/blogpost/` і створіть пост, потім відкрийте `/blogpost/ID/` і змініть заголовок. У DevTools (вкладка Network) ви побачите запити `POST /api/posts/` і `PATCH /api/posts/ID/` та їхні коди відповіді.

**Той самий API з іншого клієнта.** Скрипт на Python створює пост через токен. Так працюватиме мобільний застосунок:

```python
import requests

BASE = 'http://127.0.0.1:5000'

token = requests.post(
    f'{BASE}/api/token/',
    json={'username': 'alice', 'password': 'ПАРОЛЬ'},
).json()['token']

response = requests.post(
    f'{BASE}/api/posts/',
    json={'title': 'Пост із Python', 'content': 'Текст'},
    headers={'Authorization': f'Token {token}'},
)
print(response.status_code, response.json())
```

Не викликайте власне API з view через `requests`: це зайвий мережевий виклик усередині одного сервера. Якщо логіка потрібна в Python-коді на сервері, використовуйте серіалізатор напряму: `BlogPostSerializer(data=...)`, `is_valid()`, `save()`.

## 9. Типові помилки

1. **Swagger зламався після зміни `REST_FRAMEWORK`.** Ви перезаписали словник і втратили наявні ключі, наприклад `DEFAULT_SCHEMA_CLASS`. Додавайте ключі, а не замінюйте словник.
2. **Очікували 401, а отримали 403.** `SessionAuthentication` стоїть у списку першою. Поставте `TokenAuthentication` на перше місце.
3. **401 із правильним токеном.** Заголовок має виглядати як `Authorization: Token <ключ>`, зі словом `Token` і пробілом. У Postman це розділ Headers.
4. **`no such table: authtoken_token`.** Забули `python manage.py migrate` після додавання `rest_framework.authtoken`.
5. **Помилка про відсутню колонку `author`.** Не застосовано міграцію: виконайте `makemigrations` і `migrate`.
6. **Старі пости не редагуються (403).** Це очікувано: в них немає автора. Створіть новий пост через API.
7. **У тестах 401.** Клієнт не автентифікований: додайте `force_authenticate` або `credentials`.
8. **З браузера 403 при збереженні.** У формі немає `{% csrf_token %}` або в `fetch` немає заголовка `X-CSRFToken`.
9. **Сторінка `/blogpost/5/` повертає 404.** Немає маршруту `blogpost/<int:post_id>/`.

## 10. Словничок

- **Автентифікація**: перевірка, хто робить запит.
- **Авторизація (дозволи)**: перевірка, що цьому користувачу дозволено.
- **401 Unauthorized**: сервер не знає, хто ви.
- **403 Forbidden**: сервер знає, хто ви, але дію заборонено.
- **Токен**: ключ, який клієнт надсилає в заголовку замість логіна й пароля.
- **Сесія**: спосіб, яким браузер «пам'ятає» користувача після входу (cookie).
- **CSRF-токен**: захист від підроблених запитів із чужих сайтів. Підтверджує, що форма прийшла з нашого сайту.
- **Permission (дозвіл)**: клас DRF, який вирішує, чи можна виконати запит.
- **Об'єктний дозвіл**: перевірка прав щодо конкретного запису (наприклад, чи ви автор).
- **`read_only`**: поле, яке сервер віддає, але не приймає від клієнта.
- **`perform_create`**: метод ViewSet, який викликається перед збереженням нового запису.
- **Міграція**: опис змін у структурі бази даних.

## 11. Запитання для самоперевірки

Спробуйте відповісти без підглядання, потім звірте з відповідями нижче.

1. Чим автентифікація відрізняється від дозволів?
2. Чим 401 відрізняється від 403?
3. У якому заголовку й у якому форматі надсилають токен?
4. Навіщо після додавання `rest_framework.authtoken` потрібна міграція?
5. Що робить `IsAuthenticatedOrReadOnly`?
6. Чому поле `author` зроблено `read_only`?
7. Для чого потрібен метод `perform_create`?
8. Чому поле `author` у моделі зроблено з `null=True`?
9. Чим `force_authenticate` відрізняється від `credentials`?
10. Чому тести із заняття 46 впали після додавання дозволів?
11. Навіщо в `fetch` потрібен заголовок `X-CSRFToken`?
12. Які переваги дає перехід від викликів ORM до викликів API?

**Відповіді.**

1. Автентифікація відповідає на питання «хто ти», дозволи на «що тобі можна».
2. 401: сервер не знає, хто ви. 403: сервер знає, але дію заборонено.
3. У заголовку `Authorization` у форматі `Token <ключ>`.
4. Щоб створити в базі таблицю токенів.
5. Читати можуть усі, а створювати, змінювати й видаляти лише ті, хто увійшов.
6. Щоб клієнт не міг створити пост від чужого імені. Автора підставляє сервер.
7. DRF викликає його перед збереженням нового запису. Там ми підставляємо автора з `request.user`.
8. У базі вже є пости без автора.
9. `force_authenticate` обходить автентифікацію, `credentials` додає справжній заголовок і проходить усю перевірку токена.
10. Вони працювали без входу, а тепер потрібна автентифікація. Тести зловили зміну поведінки.
11. Для користувача із сесією DRF вимагає CSRF-токен на POST, PATCH і DELETE. Без нього буде 403.
12. Одна перевірка даних замість двох, а ті самі дані доступні мобільним клієнтам і скриптам.

## 12. Завдання для практики

1. Для `TaskViewSet` (якщо він є після заняття 46) встановіть дозвіл `IsAuthenticated`: користувачі без входу не бачать завдань (401).
2. Напишіть три тести: анонімний список повертає 401; список із автентифікацією повертає 200; створення другого завдання з тим самим `email` повертає 400 (поле унікальне).
3. Необов'язково: виведіть на сторінці список постів, завантажений через `fetch('/api/posts/')`.
4. Відкрийте Pull Request із описом: що зроблено і як перевірити (`python manage.py test`).

Якщо щось не виходить, пишіть у Telegram: покажіть код і текст помилки, а не лише «не працює».
