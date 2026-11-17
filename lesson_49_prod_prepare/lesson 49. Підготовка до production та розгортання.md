# Конспект заняття 49. Підготовка Django-застосунку до production та розгортання

*Матеріал для читання й повторення після заняття. Читайте з відкритим проєктом і пробуйте кожен приклад самі. Розгортайте лише тестові дані й нові секрети.*

## Про що це заняття

До цього часу наш застосунок працював на ноутбуці через `runserver`. Для справжніх користувачів потрібно інше: безпечні налаштування, окрема база даних, сервер, який витримує навантаження, HTTPS, логи й перевірка стану. Сьогодні ми готуємо застосунок до production і запускаємо його в Docker разом із PostgreSQL.

Ми навчимося:

- розуміти, чим production відрізняється від розробки;
- виносити налаштування у змінні оточення й фіксувати залежності в `requirements.txt`;
- підключати PostgreSQL через `DATABASE_URL`;
- віддавати статику через WhiteNoise й запускати застосунок через gunicorn;
- пакувати застосунок у Docker-образ і запускати стек через `docker compose`;
- додавати логи й ендпоінт `/health/`;
- розуміти HTTPS, проксі та `CSRF_TRUSTED_ORIGINS`;
- налаштовувати простий CI і виконувати smoke-перевірку.

## Що потрібно мати перед початком

- Результат заняття 48: змінні оточення (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_HTTPS`), безпекові налаштування, тести.
- У прикладах застосунок називається `polls`, а пакет проєкту (папка з `settings.py` і `wsgi.py`) — `mysite`. Підставте свою назву. Її видно в `manage.py` у рядку `DJANGO_SETTINGS_MODULE`.
- Встановлені Docker і Docker Compose. Перевірте: `docker --version` і `docker compose version`. На Windows Docker Desktop має бути запущений.
- Gunicorn не працює на «рідній» Windows (потрібна Unix-система), тому ми запускаємо його всередині Docker.

## 1. Розробка проти production

Те, що зручно під час розробки, у production небезпечне або повільне:

|  | Розробка | Production |
| --- | --- | --- |
| Сервер | `runserver` | WSGI-сервер (gunicorn) за проксі |
| `DEBUG` | `True` | `False` |
| База даних | SQLite | PostgreSQL як окремий сервіс |
| Статика | віддає `runserver` | `collectstatic` + WhiteNoise або nginx |
| Секрети | у файлі налаштувань | у змінних оточення |
| HTTPS | немає | є |
| Логи | у консолі | у stdout і збираються |
| Помилки | сторінка з кодом | моніторинг і сповіщення |

Два принципи:

1. Налаштування живуть у **змінних оточення**, а не в коді. Тоді той самий код працює і локально, і на сервері.
2. Образ застосунку збирають **один раз**, а запускають де завгодно з різними змінними.

`runserver` призначений лише для розробки. У документації Django прямо сказано, що його не варто використовувати в production.

## 2. Налаштування та залежності

**Залежності.** Встановіть потрібні пакети й зафіксуйте версії:

```bash
pip install gunicorn whitenoise dj-database-url "psycopg[binary]"
pip freeze > requirements.txt
```

- `gunicorn` — WSGI-сервер;
- `whitenoise` — віддає статику з Django;
- `dj-database-url` — читає `DATABASE_URL`;
- `psycopg` — драйвер PostgreSQL (для Django 4.2 і новіших; для старіших версій потрібен `psycopg2-binary`).

Команда `pip freeze` записує точні версії всіх пакетів, тож збірка завтра буде такою самою, як сьогодні.

**`.gitignore`.** Переконайтеся, що в ньому є:

```
.env
db.sqlite3
staticfiles/
__pycache__/
.venv/
```

**Змінні оточення.** Усе, що змінюється між середовищами, береться зі змінних:

| Змінна | Призначення |
| --- | --- |
| `DJANGO_SECRET_KEY` | секретний ключ |
| `DJANGO_DEBUG` | `0` або `1` |
| `DJANGO_ALLOWED_HOSTS` | дозволені домени через кому |
| `DATABASE_URL` | адреса бази даних |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | довірені джерела форм для HTTPS-домену |
| `DJANGO_BEHIND_PROXY` | `1`, якщо перед Django стоїть довірений проксі |
| `DJANGO_LOG_LEVEL` | рівень логування |
| `DJANGO_HTTPS` | `1` вмикає HTTPS-налаштування |

## 3. PostgreSQL через DATABASE\_URL

SQLite — це файл. Він погано витримує одночасні записи, його не можна поділити між кількома серверами, а в контейнері файл зникає разом із ним. PostgreSQL — окремий сервіс із мережевим доступом, транзакціями й резервними копіями.

У `settings.py`:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
    )
}
```

Якщо змінної `DATABASE_URL` немає, використовується SQLite, і локальна розробка працює як раніше. Якщо вона є, наприклад `postgres://користувач:пароль@хост:5432/назва`, Django підключається до PostgreSQL. Параметр `conn_max_age=600` повторно використовує з'єднання з базою до десяти хвилин.

Швидка спроба з PostgreSQL (пароль без спеціальних символів):

```bash
docker run --name polls-db -e POSTGRES_PASSWORD=secret123 -e POSTGRES_DB=polls -p 5432:5432 -d postgres:16
```

```bash
# Linux / macOS
export DATABASE_URL='postgres://postgres:secret123@localhost:5432/polls'
python manage.py migrate
```

```powershell
# Windows PowerShell
$env:DATABASE_URL = 'postgres://postgres:secret123@localhost:5432/polls'
python manage.py migrate
```

Дані зі SQLite у нову базу не переносяться автоматично. Для навчального проєкту ми створюємо порожню базу й нового суперкористувача (`python manage.py createsuperuser`). Зупиніть контейнер: `docker rm -f polls-db`.

## 4. Статика та WSGI-сервер

При `DEBUG=0` команда `runserver` не віддає статичні файли, і в адмінці зникає оформлення. У production статику віддає не код застосунку, а окремий вебсервер (nginx) або проміжний шар WhiteNoise. Ми беремо WhiteNoise, бо він найпростіший.

У `settings.py`:

```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # одразу після SecurityMiddleware
    # ...решта як була...
]

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
```

Налаштування `STORAGES` підходить для Django 4.2 і новіших. Якщо `STATIC_ROOT` не задано, `collectstatic` завершиться помилкою.

Зберіть статику:

```bash
python manage.py collectstatic --noinput
```

Команда збирає статику всіх застосунків (зокрема адмінки) в одну папку `staticfiles/`. Запустіть сервер із `DJANGO_DEBUG=0` і відкрийте `/admin/`: оформлення з'явилося, бо тепер його віддає WhiteNoise.

**WSGI-сервер.** Django-застосунок експортує об'єкт `application` у файлі `wsgi.py`. WSGI-сервер (gunicorn) імпортує його, запускає кілька процесів-працівників і розподіляє між ними запити:

```bash
gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile -
```

Кількість працівників підбирають за навантаженням; як орієнтир часто беруть `2 × кількість ядер + 1`. Прапорець `--access-logfile -` виводить журнал запитів у stdout.

Gunicorn не запускається на «рідній» Windows. Тому на заняттях ми запускаємо його в Docker. Альтернатива для Windows без Docker: `pip install waitress` і `waitress-serve --port=8000 mysite.wsgi:application`.

## 5. Docker і docker compose

Контейнер — це запакований застосунок разом з усіма залежностями. **Образ** (image) — шаблон, **контейнер** — його запущена копія. `docker compose` описує кілька сервісів (наш застосунок і PostgreSQL) в одному файлі й запускає їх разом. Перевага: застосунок працює однаково на ноутбуці, у CI й на сервері.

**Dockerfile** (у корені проєкту, поруч із `manage.py`):

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Тимчасовий ключ потрібен лише на час збірки, у роботі образ його не використовує
RUN DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]
```

Що тут важливо:

- Спочатку копіюємо лише `requirements.txt` і ставимо залежності. Docker кешує шари, тому при зміні коду залежності не перевстановлюються.
- `collectstatic` виконується під час збірки, тому потрібен тимчасовий ключ.
- Контейнер працює від звичайного користувача `appuser`, а не від root (це продовження теми безпеки із заняття 48).
- Версію Python в образі узгодьте з тією, що підтримує ваша версія Django.

**`.dockerignore`.** Щоб секрети й зайві файли не потрапили в образ:

```
.git
.env
db.sqlite3
__pycache__/
*.pyc
.venv/
staticfiles/
```

**Файл `.env`** (лише локально, у `.gitignore`). Пароль без спеціальних символів, бо він потрапляє в URL:

```
POSTGRES_PASSWORD=secret123
DJANGO_SECRET_KEY=ваш-довгий-випадковий-ключ
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

**`docker-compose.yml`:**

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: polls
      POSTGRES_USER: polls
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U polls -d polls"]
      interval: 5s
      timeout: 5s
      retries: 10

  web:
    build: .
    env_file: .env
    environment:
      DATABASE_URL: postgres://polls:${POSTGRES_PASSWORD}@db:5432/polls
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8000:8000"

volumes:
  pgdata:
```

Що варто зрозуміти у файлі:

- Хост бази в `DATABASE_URL` — `db`, тобто назва сервісу. Усередині контейнера `localhost` означає сам контейнер, а не базу.
- `healthcheck` і `depends_on` змушують `web` чекати, поки база реально готова.
- `pgdata` — іменований том: дані бази живуть окремо від контейнера й переживають його перезапуск.
- Змінні `${POSTGRES_PASSWORD}` Compose бере із файлу `.env` у каталозі проєкту.

**Запуск і перевірка:**

```bash
docker compose up -d --build
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
docker compose logs -f web
```

Відкрийте `http://127.0.0.1:8000/admin/` (оформлення є) і `http://127.0.0.1:8000/api/docs/` (Swagger). Міграції запускають окремою командою, а не в `CMD`: інакше при кількох копіях застосунку вони б виконувалися одночасно.

Перевірте, що дані переживають перезапуск: створіть пост через API, виконайте `docker compose restart web`, а потім `docker compose down` і знову `docker compose up -d`. Пост залишився завдяки тому `pgdata`. Але команда `docker compose down -v` видаляє томи, тобто й дані бази.

## 6. Логи та `/health/`

У контейнері логи пишуть у stdout, а збирає їх платформа (`docker compose logs`). Додайте в `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
    },
}
```

У логи не можна писати паролі, токени й персональні дані (це теж тема заняття 48).

Платформи та системи моніторингу періодично запитують адресу й перевіряють відповідь. Для цього додайте view:

```python
# polls/views.py
from django.db import connection
from django.http import JsonResponse


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception:
        return JsonResponse({'status': 'error'}, status=503)
    return JsonResponse({'status': 'ok'})
```

```python
# polls/urls.py
path('health/', views.health, name='health'),
```

У відповіді немає жодних подробиць про помилку: зловмиснику вони не потрібні. `curl -i http://127.0.0.1:8000/health/` повертає 200, а якщо зупинити базу (`docker compose stop db`), то 503.

Тест:

```python
class HealthTests(TestCase):
    def test_health_returns_ok(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
```

У реальних проєктах помилки відправляють у систему відстеження (наприклад, Sentry), а `/health/` пінгує сервіс аптайм-моніторингу, який надсилає сповіщення при падінні.

## 7. HTTPS, проксі та розгортання на сервері

На справжньому сервері gunicorn стоїть за зворотним проксі (nginx або Caddy), який приймає HTTPS і передає запити застосунку по HTTP:

```
Браузер --HTTPS--> проксі (Caddy/nginx) --HTTP--> gunicorn (web) --> PostgreSQL (db)
```

Два налаштування, без яких на домені буде біда (`settings.py`):

```python
CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin
]

if os.environ.get('DJANGO_BEHIND_PROXY', '0') == '1':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

- `DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com` (зі схемою `https://`). Без цього форми на домені за проксі отримають 403 CSRF.
- `DJANGO_BEHIND_PROXY=1` вмикайте лише тоді, коли перед Django стоїть довірений проксі, який сам виставляє заголовок `X-Forwarded-Proto`. Без цього Django вважає всі запити HTTP, і разом з `SECURE_SSL_REDIRECT` вийде нескінченне перенаправлення. Якщо проксі не контролюється вами, заголовок можна підробити.

**Caddy як проксі.** Додайте сервіс у `docker-compose.yml` (на сервері порт 8000 назовні не відкривають) і том `caddy_data` у розділ `volumes`:

```yaml
  caddy:
    image: caddy:2
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
    depends_on:
      - web
```

```
example.com {
    reverse_proxy web:8000
}
```

Якщо домен вказує на сервер, а порти 80 і 443 відкриті, Caddy сам отримує й оновлює HTTPS-сертифікат.

**Кроки розгортання на VPS:**

1. Сервер із Docker, відкриті лише порти 22, 80 і 443.
2. `git clone` репозиторію.
3. Створити `.env` із реальними секретами (поза git).
4. `docker compose up -d --build`.
5. Міграції та `createsuperuser`.
6. Smoke-перевірка (розділ 8).
7. Оновлення: `git pull`, потім `docker compose up -d --build`.
8. Резервна копія бази: `docker compose exec -T db pg_dump -U polls polls > backup.sql`. Копію обов'язково потрібно хоч раз перевірити на відновлення.

**Варіант без власного сервера (PaaS).** Платформи на кшталт Render, Railway чи Fly.io беруть на себе сервер і HTTPS. Загальна схема: підключити репозиторій; задати команду збірки (`pip install -r requirements.txt && python manage.py collectstatic --noinput`) і команду запуску (`gunicorn mysite.wsgi:application`); задати змінні оточення; додати керовану PostgreSQL (платформа дає `DATABASE_URL`); виконувати `python manage.py migrate` як окремий крок перед запуском. Умови безкоштовних планів змінюються, тому перевіряйте актуальні на сайті платформи.

## 8. CI та smoke-перевірка

**CI** — це автоматична перевірка при кожному коміті: тести й `check --deploy`. Файл `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    env:
      DJANGO_SECRET_KEY: ci-only-secret-key-for-tests-0123456789-abcdefghijklmnopqrstuvwxyz
      DJANGO_DEBUG: '0'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
      - run: pip install -r requirements.txt
      - run: python manage.py test
      - run: python manage.py check --deploy --fail-level WARNING
        env:
          DJANGO_HTTPS: '1'
```

Примітки. Перевірте актуальні версії дій (`actions/checkout`, `actions/setup-python`) у документації GitHub. Ключ для CI має бути довгим: `check --deploy` попереджає про занадто короткий `SECRET_KEY`. Якщо після увімкнення `--fail-level WARNING` залишаються попередження (наприклад, про HSTS для піддоменів або preload), приймайте рішення свідомо: або налаштуйте, або вимкніть перевірку через `SILENCED_SYSTEM_CHECKS` із коментарем, чому. Не вимикайте перевірки лише «щоб пройшло».

**Smoke-перевірка після розгортання** — коротка перевірка, що найважливіше працює:

| Що перевіряємо | Команда | Очікуваний результат |
| --- | --- | --- |
| Стан застосунку | `curl -i https://example.com/health/` | 200 і `{"status": "ok"}` |
| Читання API | `curl -i https://example.com/api/posts/` | 200 |
| Захист запису | `curl -i -X POST https://example.com/api/posts/ -H "Content-Type: application/json" -d '{"title": "x", "content": "y"}'` | 401 |
| Перенаправлення на HTTPS | `curl -I http://example.com/` | 301 на `https://` |
| Адмінка з оформленням | відкрити `/admin/login/` у браузері | сторінка зі стилями |

## 9. Чек-ліст готовності до production

1. Секрети лише у змінних оточення; `.env` поза git.
2. `DEBUG=False`, правильні `ALLOWED_HOSTS` і `CSRF_TRUSTED_ORIGINS`.
3. PostgreSQL замість SQLite; дані на томі; резервні копії перевірені.
4. Залежності зафіксовані в `requirements.txt`.
5. Статика зібрана (`collectstatic`) і віддається (WhiteNoise або nginx).
6. gunicorn (або інший WSGI-сервер) за проксі з HTTPS.
7. Міграції виконуються окремим кроком.
8. Логи у stdout; помилки відстежуються.
9. `/health/` і моніторинг.
10. CI із тестами та `check --deploy`.
11. Контейнер працює не від root.
12. План відкату: попередній образ, який можна швидко запустити знову.

## 10. Типові помилки

1. **`docker: command not found` або Docker Desktop не запущений.** Запустіть Docker Desktop. Без Docker: `DJANGO_DEBUG=0`, база за замовчуванням (SQLite), `collectstatic`, а далі на Linux/macOS `gunicorn`, на Windows `waitress-serve --port=8000 mysite.wsgi:application`.
2. **`No module named 'fcntl'` при запуску gunicorn.** Це Windows: gunicorn працює лише на Unix. Запускайте в Docker або використайте `waitress`.
3. **Збірка падає з `KeyError: 'DJANGO_SECRET_KEY'`.** У `RUN` з `collectstatic` немає тимчасового ключа.
4. **`ModuleNotFoundError` у контейнері.** Пакета немає в `requirements.txt` (забули оновити `pip freeze`).
5. **`could not connect to server` до бази.** Хост у `DATABASE_URL` має бути `db`, а не `localhost`; або база ще не готова.
6. **Пароль зі спецсимволами в `DATABASE_URL`.** Використайте простий пароль або закодуйте символи в URL.
7. **`You're using the staticfiles app without having set the STATIC_ROOT`.** Не задано `STATIC_ROOT`.
8. **Адмінка без стилів у контейнері.** Не виконано `collectstatic`, немає `WhiteNoiseMiddleware` або він стоїть не одразу після `SecurityMiddleware`.
9. **400 `DisallowedHost`.** Хоста немає в `DJANGO_ALLOWED_HOSTS`.
10. **Нескінченне перенаправлення після `DJANGO_HTTPS=1` за проксі.** Не вказано `DJANGO_BEHIND_PROXY=1` або проксі не передає `X-Forwarded-Proto`.
11. **403 CSRF на домені за проксі.** Немає `DJANGO_CSRF_TRUSTED_ORIGINS` зі схемою `https://`.
12. **Порт 8000 або 5432 зайнятий.** Зупиніть інший процес або змініть порт у `ports`.
13. **Дані зникли.** Виконували `docker compose down -v`, який видаляє томи.

## 11. Словничок

- **Production**: середовище, у якому застосунком користуються справжні користувачі.
- **Змінні оточення**: налаштування, що передаються застосунку ззовні, а не зберігаються в коді.
- **`requirements.txt`**: файл із точними версіями залежностей.
- **PostgreSQL**: окремий сервер бази даних.
- **`DATABASE_URL`**: адреса бази даних в одному рядку.
- **`collectstatic`**: збирає статичні файли в одну папку.
- **WhiteNoise**: бібліотека, що віддає статику прямо з Django-застосунку.
- **WSGI-сервер (gunicorn)**: сервер, що запускає Django-застосунок у кількох процесах.
- **Образ (image)**: шаблон, з якого створюють контейнери.
- **Контейнер**: запущена копія образу.
- **Том (volume)**: сховище даних контейнера, яке переживає його перезапуск.
- **Зворотний проксі**: сервер перед застосунком, що приймає HTTPS і передає запити далі.
- **`/health/`**: адреса, за якою перевіряють, що застосунок живий.
- **CI**: автоматична перевірка коду при кожному коміті.
- **Smoke-перевірка**: коротка перевірка найважливішого після розгортання.

## 12. Запитання для самоперевірки

Спробуйте відповісти без підглядання, потім звірте з відповідями нижче.

1. Назвіть три відмінності production від розробки.
2. Чому налаштування краще тримати у змінних оточення?
3. Чому SQLite погано підходить для production?
4. Що станеться, якщо не задати `DATABASE_URL`?
5. Навіщо `collectstatic` і WhiteNoise?
6. Чому в production не використовують `runserver`?
7. Чим образ відрізняється від контейнера?
8. Чому хост бази в compose називається `db`, а не `localhost`?
9. Навіщо том `pgdata`?
10. Чому міграції не запускають у `CMD`?
11. Для чого `/health/`?
12. Що буде без `DJANGO_BEHIND_PROXY=1` і з `SECURE_SSL_REDIRECT`?
13. Навіщо `CSRF_TRUSTED_ORIGINS`?
14. Для чого smoke-перевірка після розгортання?

**Відповіді.**

1. `DEBUG=False`, окрема СУБД замість SQLite, WSGI-сервер замість `runserver`, секрети у змінних оточення, HTTPS, логи та моніторинг.
2. Код один для всіх середовищ, а секрети не потрапляють у git.
3. Це файл, який погано витримує одночасні записи й зникає разом із контейнером.
4. Використовується SQLite за замовчуванням.
5. `collectstatic` збирає статику в одну папку, а WhiteNoise віддає її з застосунку.
6. Він призначений лише для розробки: не розрахований на навантаження й безпеку.
7. Образ — шаблон, контейнер — його запущена копія.
8. `db` — назва сервісу в compose; `localhost` усередині контейнера — це сам контейнер.
9. Дані бази зберігаються окремо від контейнера й не втрачаються при його перезапуску.
10. При кількох копіях застосунку міграції виконувалися б одночасно; це окремий крок розгортання.
11. Щоб платформа чи моніторинг могли автоматично перевіряти, що застосунок і база живі.
12. Django вважатиме запити HTTP і зациклить перенаправлення.
13. Щоб форми на HTTPS-домені за проксі проходили перевірку CSRF.
14. Швидко переконатися, що найважливіше працює в реальному середовищі.

## 13. Завдання для практики

1. Додайте в репозиторій `requirements.txt`, `Dockerfile`, `.dockerignore`, `docker-compose.yml` та `.env.example` (із вигаданими значеннями, без справжніх секретів). Переконайтеся, що `.env` у `.gitignore`.
2. Запустіть `docker compose up --build`, виконайте міграції, створіть суперкористувача і зробіть скріншоти `/admin/` (зі стилями) та `/api/docs/`.
3. Додайте `/health/` і тест.
4. Додайте налаштування `LOGGING` у stdout.
5. Налаштуйте GitHub Actions: тести та `check --deploy`. Додайте посилання на зелений запуск.
6. Необов'язково: розгорніть застосунок на PaaS або VPS (лише тестові дані) або опишіть кроки.
7. Відкрийте Pull Request з описом: як запустити, які змінні оточення потрібні (без значень), як перевірити.

Якщо щось не виходить, пишіть у Telegram: покажіть код і текст помилки, а не лише «не працює».
