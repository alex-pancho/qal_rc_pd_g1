# Конспект заняття 46. CRUD API та маршрутизація в Django REST Framework

*Матеріал для читання й повторення після заняття. Читайте з відкритим проєктом і пробуйте кожен приклад самі.*

## Про що це заняття

На минулому занятті ми зробили API, яке вміє віддавати список постів (GET) і створювати пост (POST). Але справжньому застосунку потрібно більше: показати один пост, змінити його, видалити. Чотири базові дії з даними називають **CRUD**: Create (створити), Read (прочитати), Update (оновити), Delete (видалити).

На цьому занятті ми:

- зіставили CRUD із HTTP-методами й адресами;
- навчилися повертати правильні **коди відповіді**;
- реалізували PUT, PATCH і DELETE;
- написали автотести для API;
- спростили код за допомогою generic views, а потім ViewSet і Router.

## Що потрібно мати перед початком

- Встановлений Django REST Framework. Це окремий пакет, він не входить у Django: `pip install djangorestframework`.
- Рядок `'rest_framework'` у `INSTALLED_APPS`.
- Модель і серіалайзер із минулого заняття. У прикладах це модель `BlogPost` з полями `title`, `content`, `created_at` і серіалайзер `BlogPostSerializer`.
- У прикладах застосунок називається `blog`, а сервер працює на порту 5000. Замініть на свої значення, якщо вони інші.

## 1. CRUD і HTTP-методи

У REST API кожна дія з даними описується трьома речами: адресою (URL), методом і кодом відповіді. Ось повна карта для нашого блогу:

| Дія | HTTP-метод | URL | Успіх | Помилки |
| --- | --- | --- | --- | --- |
| Створити | POST | /api/posts/ | 201 Created | 400 |
| Прочитати список | GET | /api/posts/ | 200 OK | — |
| Прочитати один | GET | /api/posts/{id}/ | 200 OK | 404 |
| Оновити повністю | PUT | /api/posts/{id}/ | 200 OK | 400, 404 |
| Оновити частково | PATCH | /api/posts/{id}/ | 200 OK | 400, 404 |
| Видалити | DELETE | /api/posts/{id}/ | 204 No Content | 404 |

Запишіть собі просте правило: **URL — це іменник** (що), **метод — це дієслово** (що з ним зробити), **код відповіді — це результат**. Запис `{id}` у таблиці означає номер запису, наприклад `/api/posts/3/`. Кінцевий слеш важливий: без нього деякі запити не спрацюють.

## 2. Коди відповіді

Код відповіді — це число, яким сервер коротко повідомляє, чим закінчився запит. Перша цифра показує групу:

- **2xx** — успіх;
- **4xx** — помилка клієнта, тобто запит був неправильний;
- **5xx** — помилка сервера, тобто зламався код на нашому боці.

Коди, які нам потрібні:

- **200 OK** — все гаразд, у відповіді є дані.
- **201 Created** — новий запис створено.
- **204 No Content** — все гаразд, але відповідь порожня. Так відповідає сервер після видалення.
- **400 Bad Request** — запит дійшов, але дані невалідні. Наприклад, не заповнене обов'язкове поле.
- **404 Not Found** — такого запису або такої адреси немає.
- **405 Method Not Allowed** — адреса існує, але цей метод для неї не дозволений.
- **500 Internal Server Error** — помилка в коді сервера.

Найважливіше розрізняти три помилки. **400** означає «я вас зрозумів, але ваші дані не підходять». **404** означає «такого немає». **405** означає «тут є, але так з цим працювати не можна».

Під час перевірки API завжди дивіться на **код відповіді**, а не лише на тіло. Відповідь може виглядати нормально, а код при цьому буде не тим, що треба.

## 3. Один запис: GET за id і 404

До цього моменту ми вміли працювати зі списком. Тепер додамо адресу для одного поста. Якщо у вас уже є view для списку з минулого заняття, переконайтеся, що воно повертає правильні коди:

```python
# blog/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import BlogPost
from .serializers import BlogPostSerializer


@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

    serializer = BlogPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Тепер view для одного запису. Поки що лише GET:

```python
# blog/views.py
@api_view(['GET'])
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return Response(BlogPostSerializer(post).data)
```

І маршрут:

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/posts/', views.post_list, name='api-post-list'),
    path('api/posts/<int:pk>/', views.post_detail, name='api-post-detail'),
]
```

**Як це працює.** Це і є маршрутизація: Django дивиться на адресу запиту й вирішує, яку функцію викликати. Запис `<int:pk>` — це конвертер шляху. Він бере частину адреси, перетворює її на ціле число й передає у функцію як аргумент `pk`. Для адреси `/api/posts/3/` функція отримає `pk=3`.

Функція `get_object_or_404` шукає запис у базі. Якщо запису немає, вона підіймає помилку, а DRF перетворює її на відповідь з кодом 404.

**Спробуйте самі** (у Postman або через curl з прапорцем `-i`, який показує код відповіді):

- `GET /api/posts/1/` повертає 200 і JSON поста;
- `GET /api/posts/9999/` повертає 404 і JSON з полем `detail`;
- `GET /api/posts/abc/` теж повертає 404, але це інша відповідь: адреса не збіглася з жодним шаблоном, тому відповідає сам Django, а наша функція навіть не викликалася.

Отже, 404 буває двох видів: «адреси немає» і «запису з таким id немає». Для клієнта це однаковий код, але причини різні.

## 4. Оновлення: PUT і PATCH

Оновити запис можна двома способами. Розширимо view:

```python
@api_view(['GET', 'PUT', 'PATCH'])
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'GET':
        return Response(BlogPostSerializer(post).data)

    serializer = BlogPostSerializer(
        post,
        data=request.data,
        partial=(request.method == 'PATCH'),
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Ключовий рядок — `partial=(request.method == 'PATCH')`. Параметр `partial=True` каже серіалайзеру: «не вимагай усіх полів, зміни лише ті, що прийшли».

|  | PUT | PATCH |
| --- | --- | --- |
| Що робить | замінює запис повністю | змінює лише надіслані поля |
| Пропущене обов'язкове поле | помилка 400 | нічого, поле лишається як було |
| У DRF | `partial=False` (за замовчуванням) | `partial=True` |

Щоб запам'ятати: **PUT — це переписати документ наново, PATCH — виправити одну помилку олівцем.**

Приклади. Нехай пост має `title` і `content`.

1. `PUT /api/posts/1/` з тілом `{"title": "Новий заголовок", "content": "Новий текст"}` повертає 200, обидва поля змінилися.
2. `PUT /api/posts/1/` з тілом `{"title": "Лише заголовок"}` повертає 400, бо `content` обов'язкове. У відповіді буде повідомлення, що це поле потрібне.
3. `PATCH /api/posts/1/` з тілом `{"title": "Виправлений заголовок"}` повертає 200. Заголовок змінився, `content` залишився старим.
4. `PATCH /api/posts/1/` з тілом `{"title": ""}` повертає 400: порожній заголовок не дозволений.

Після кожного запиту корисно зробити окремий `GET /api/posts/1/` і подивитися, що справді лежить у базі.

Ще одна деталь. Якщо в тілі PUT або PATCH надіслати `created_at`, значення буде проігноровано. Поле з `auto_now_add` не редагується, тому `ModelSerializer` автоматично робить його «тільки для читання».

## 5. Видалення: DELETE і код 405

Додаємо останню дію. Ось фінальна версія view для одного запису з усіма методами:

```python
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'GET':
        return Response(BlogPostSerializer(post).data)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = BlogPostSerializer(
        post,
        data=request.data,
        partial=(request.method == 'PATCH'),
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Що варто запам'ятати:

- Після видалення сервер повертає **204 No Content**: успіх без тіла. Повертати нічого, бо запису вже немає. Клієнт не повинен пробувати розбирати JSON із такої відповіді.
- Якщо повторити DELETE для того самого id, буде **404**: запису вже немає. Стан сервера від цього не змінюється (поста як не було, так і немає). Таку властивість називають **ідемпотентністю**: повторення дії не змінює результат. GET, PUT і DELETE ідемпотентні, POST ні, бо кожен POST створює новий запис.
- Якщо надіслати DELETE на адресу списку (`DELETE /api/posts/`), буде **405 Method Not Allowed**. Адреса існує, але ця дія для неї не передбачена, бо в `@api_view(['GET', 'POST'])` метод DELETE не вказано.

Щоб випробувати DELETE безпечно, спершу створіть пост через POST (у відповіді буде його `id`), а потім видаліть саме його.

## 6. Автотести: записуємо контракт API

Ручна перевірка запитів у Postman добра, але вона не масштабується: кожного разу, коли хтось змінює код, усе довелося б клацати заново. Тому поведінку API записують у **автотести**. Тест фіксує *контракт*: на такий запит сервер відповідає ось так.

```python
# blog/tests.py
from rest_framework import status
from rest_framework.test import APITestCase

from .models import BlogPost


class PostApiTests(APITestCase):
    def setUp(self):
        self.post = BlogPost.objects.create(title='Старий', content='Текст')
        self.list_url = '/api/posts/'
        self.detail_url = f'/api/posts/{self.post.pk}/'

    def test_list_returns_200(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_returns_201(self):
        data = {'title': 'Новий', 'content': 'Текст'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 2)

    def test_create_without_title_returns_400(self):
        response = self.client.post(self.list_url, {'content': 'Текст'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_missing_post_returns_404(self):
        response = self.client.get('/api/posts/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_without_content_returns_400(self):
        response = self.client.put(self.detail_url, {'title': 'Новий'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_changes_only_sent_fields(self):
        response = self.client.patch(self.detail_url, {'title': 'Новий'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Новий')
        self.assertEqual(self.post.content, 'Текст')

    def test_delete_returns_204_then_404(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
```

Запуск: `python manage.py test blog -v 2`. Усі сім тестів мають пройти.

Пояснення до коду:

- `setUp` виконується перед кожним тестом і створює один пост у тестовій базі. Тестова база окрема від вашої, тому реальні дані не постраждають.
- `refresh_from_db()` перечитує запис із бази. Без нього Python-об'єкт `self.post` зберігав би старі значення, і тест нічого б не довів.
- Після DELETE ми перевіряємо ще й 404. Так ми впевнюємося, що запис справді зник, а не лише отримали код 204.
- Адреси записані текстом (`'/api/posts/'`), а не через `reverse()`. Для клієнта API адреса і є контрактом. Якщо хтось її змінить, тест має впасти.

**Корисна вправа.** Спеціально зламайте код: змініть у view `204` на `200` і запустіть тести. Тест `test_delete_returns_204_then_404` впаде. Поверніть `204`, і тест знову зелений. Тест, який жодного разу не падав, не доводить нічого, бо невідомо, чи він узагалі щось перевіряє.

## 7. Менше коду: generic views

Подивіться на наші функції. У кожній ми робимо те саме: знайти запис, серіалізувати, перевірити, зберегти. DRF уже вміє це робити, і ми можемо замінити дві функції на два класи:

```python
# blog/views.py
from rest_framework import generics


class PostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
```

```python
# blog/urls.py
urlpatterns = [
    path('api/posts/', views.PostListCreate.as_view(), name='api-post-list'),
    path('api/posts/<int:pk>/', views.PostDetail.as_view(), name='api-post-detail'),
]
```

- `ListCreateAPIView` вміє GET (список) і POST (створити).
- `RetrieveUpdateDestroyAPIView` вміє GET (один запис), PUT, PATCH і DELETE.
- Клас підключається до URL через `.as_view()`.
- Який запис брати, клас визначає з `queryset` і аргументу `pk` в адресі.

Запустіть тести. Вони мають залишитися зеленими, хоча коду стало набагато менше. Саме так працює **рефакторинг під захистом тестів**: змінюємо код і одразу бачимо, що поведінка не зламалася.

## 8. ViewSet і Router: маршрутизація

Можна ще простіше. Замість двох класів і двох `path` використаємо один клас і один рядок маршруту:

```python
# blog/views.py
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
```

```python
# blog/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

Старі `path('api/posts/', ...)` приберіть, щоб не було дублікатів. Запустіть тести: вони знову зелені, бо адреси (`/api/posts/` і `/api/posts/{id}/`) залишилися тими самими.

**Router** сам створює адреси й прив'язує HTTP-методи до дій ViewSet:

| HTTP-метод | URL | Дія ViewSet |
| --- | --- | --- |
| GET | /api/posts/ | list |
| POST | /api/posts/ | create |
| GET | /api/posts/{id}/ | retrieve |
| PUT | /api/posts/{id}/ | update |
| PATCH | /api/posts/{id}/ | partial\_update |
| DELETE | /api/posts/{id}/ | destroy |

`DefaultRouter` також додає кореневу сторінку `/api/` зі списком доступних ресурсів. Відкрийте її в браузері.

Три способи написати API, і коли який обирати:

| Спосіб | Коду | Контролю | Коли брати |
| --- | --- | --- | --- |
| `@api_view` | найбільше | максимум | нестандартна логіка |
| generic views | середньо | середньо | стандартні дії з кастомізацією |
| `ModelViewSet` + Router | найменше | найменше | стандартний CRUD |

`ModelViewSet` не завжди кращий. Якщо логіка нестандартна, часто зручніше повернутися до явного view.

## 9. Swagger: документація API

Якщо на минулому занятті ви підключили Swagger (адресу дивіться у своєму `urls.py`), відкрийте його знову. Тепер там усі шість дій, параметр `id` і тіло запиту. Натисніть «Try it out» біля PATCH і спробуйте змінити пост прямо в браузері. Для generic views і ViewSet схема будується повністю, а для функцій з `@api_view` Swagger може не знати, яке тіло запиту очікується.

## 10. Типові помилки

1. **PowerShell на Windows.** Команда `curl` там є аліасом `Invoke-WebRequest`, тому команди з прапорцями не працюють. Використовуйте `curl.exe` або Postman.
2. **Немає кінцевого слеша.** POST або PUT на `/api/posts` без `/` дає помилку про відсутність слеша (через налаштування `APPEND_SLASH`). Додайте `/` в кінці.
3. **Код 415 або дані не приходять.** У curl немає `-H "Content-Type: application/json"`. У Postman не вибрано Body, raw, JSON.
4. **`No module named rest_framework`.** Не активоване віртуальне середовище або `rest_framework` не додано в `INSTALLED_APPS`.
5. **405 там, де його не чекали.** У `@api_view([...])` не вказано потрібний метод.
6. **Усі запити в тестах повертають 404.** У головному `urls.py` проєкту не підключено `blog.urls`.
7. **Помилки після переходу на роутер.** Залишилися старі `path(...)` або старі функції, які дублюють маршрути.

## 11. Словничок

- **API**: набір адрес, через які програми обмінюються даними.
- **CRUD**: створити, прочитати, оновити, видалити.
- **REST**: стиль API, де кожна адреса означає ресурс, а дію задає HTTP-метод.
- **Ресурс**: сутність, з якою працює API (пост, завдання).
- **Серіалізація**: перетворення об'єкта на JSON і навпаки.
- **Валідація**: перевірка, що дані правильні (є обов'язкові поля, довжина і так далі).
- **Код відповіді**: число, що повідомляє результат запиту (200, 201, 204, 400, 404, 405).
- **Ідемпотентність**: повторення дії не змінює результат.
- **Маршрутизація**: зіставлення адреси із функцією або класом, який її обробляє.
- **Router**: інструмент DRF, що сам створює адреси для ViewSet.
- **Контракт API**: домовленість, на який запит API відповідає так-то. Тести фіксують цей контракт.

## 12. Запитання для самоперевірки

Спробуйте відповісти без підглядання, потім звірте з відповідями нижче.

1. Яким методом створюють запис і який код очікують при успіху?
2. Чим 400 відрізняється від 404?
3. Що означає 405?
4. Звідки у функції береться `pk`?
5. Що станеться, якщо надіслати PUT лише з `title`, а `content` обов'язкове?
6. Що станеться з `content`, якщо надіслати PATCH лише з `title`?
7. Який параметр серіалізатора перетворює PUT-поведінку на PATCH?
8. Який код повертається після успішного DELETE і чому в відповіді немає тіла?
9. Що поверне повторний DELETE того самого id?
10. Навіщо в тесті викликають `refresh_from_db()`?
11. Що саме створює Router?
12. Яка дія ViewSet відповідає методу PATCH?

**Відповіді.**

1. POST; 201 Created.
2. 400: запит дійшов, але дані невалідні. 404: такого запису або адреси немає.
3. Адреса існує, але цей метод для неї не дозволений.
4. З адреси через конвертер `<int:pk>`.
5. Код 400, бо `content` обов'язкове при повному оновленні.
6. Залишиться без змін, відповідь 200.
7. `partial=True`.
8. 204 No Content; повертати нічого, бо запису вже немає.
9. 404.
10. Щоб перечитати запис із бази: Python-об'єкт у тесті зберігає старі значення.
11. Адреси для списку й одного запису та прив'язку HTTP-методів до дій ViewSet.
12. `partial_update`.

## 13. Завдання для практики

Реалізуйте повний CRUD API для моделі `Task` (або іншої моделі вашого проєкту).

1. Створіть гілку `feature/task-api` від `main`.
2. Напишіть `TaskSerializer` (`ModelSerializer`) і `TaskViewSet` (`ModelViewSet`), зареєструйте їх у роутері: `router.register('tasks', views.TaskViewSet, basename='task')`.
3. Напишіть мінімум п'ять тестів: список повертає 200; створення повертає 201; створення без обов'язкового поля повертає 400; PATCH змінює лише надіслане поле; DELETE повертає 204, а наступний GET цього запису 404.
4. Відкрийте Pull Request у свій `main` з описом: що зроблено, як перевірити (`python manage.py test`), скріншот Swagger.

Перед відправленням перевірте:

- усі тести зелені;
- адреси саме `/api/tasks/` і `/api/tasks/{id}/`;
- коди відповіді правильні;
- у PR є опис.

Якщо щось не виходить, пишіть у Telegram: покажіть код і текст помилки, а не лише «не працює».
