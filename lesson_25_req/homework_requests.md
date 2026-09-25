# Домашнє завдання: API Testing з Python (`requests`)

## Мета

Навчитися працювати з REST API через Python, виконувати HTTP-запити, перевіряти відповіді сервера та писати базові API тести.

## API для роботи

Base URL:

```text
https://jsonplaceholder.typicode.com
```

Документація:

* `/posts`
* `/comments`
* `/albums`
* `/photos`
* `/todos`
* `/users`

# Міні-документація API

## 1. GET — отримання даних

### Отримати всі posts

```http
GET /posts
```

Приклад:

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts")
print(response.status_code)
print(response.json())
```

Очікування:

* status code = 200
* відповідь = list
* list не порожній

### Отримати post по id

```http
GET /posts/1
```

Очікування:

* status code = 200
* `id == 1`

### Query parameters

```http
GET /posts?userId=1
```

Приклад:

```python
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1}
)
```

Очікування:

* всі записи мають `userId == 1`

## 2. POST — створення ресурсу

```http
POST /posts
```

Body:

```json
{
  "title": "my title",
  "body": "my body",
  "userId": 1
}
```

Приклад:

```python
payload = {
    "title": "my title",
    "body": "my body",
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=payload
)
```

Очікування:

* status code = 201
* response body містить створені поля
* згенерований `id`

## 3. PUT — повне оновлення

```http
PUT /posts/1
```

Body:

```json
{
  "id": 1,
  "title": "updated title",
  "body": "updated body",
  "userId": 1
}
```

Очікування:

* status code = 200
* title оновився

## 4. PATCH — часткове оновлення

```http
PATCH /posts/1
```

Body:

```json
{
  "title": "patched title"
}
```

Очікування:

* status code = 200
* змінилось тільки поле `title`

## 5. DELETE — видалення

```http
DELETE /posts/1
```

Очікування:

* status code = 200 або 204

# Завдання

## Частина 1. Базові запити

### Завдання 1

Написати скрипт, який:

1. отримує всі posts
2. перевіряє:

   * статус 200
   * кількість записів = 100

### Завдання 2

Отримати post з id=10.

Перевірити:

* status code 200
* `id == 10`
* є поля:

  * userId
  * id
  * title
  * body

### Завдання 3

Отримати всі todos користувача 2:

```http
GET /todos?userId=2
```

Перевірити:

* всі `userId == 2`

## Частина 2. CRUD

### Завдання 4 — Create

Створити новий post.

Перевірити:

* status 201
* title збігається
* body збігається

### Завдання 5 — Update через PUT

Оновити post id=5.

Перевірити:

* status 200
* нові дані повернулись у response

### Завдання 6 — Partial Update через PATCH

Оновити тільки title.

Перевірити:

* status 200
* title змінився

### Завдання 7 — Delete

Видалити post id=5.

Перевірити:

* status 200/204

## Частина 3. Негативні сценарії

### Завдання 8

Отримати неіснуючий post:

```http
GET /posts/999999
```

Перевірити:

* status 404 або пустий response

### Завдання 9

Відправити POST без required полів.

```json
{}
```

Перевірити поведінку API.

## Частина 4. Робота з headers

### Завдання 10

Відправити GET з custom headers:

```python
headers = {
    "User-Agent": "QA Student"
}
```

Переконатися:

* request виконався успішно

## Bonus ⭐

### Завдання 11

Створити універсальну функцію:

```python
def make_request(method, endpoint, **kwargs):
    ...
```

Щоб можна було викликати:

```python
make_request("GET", "/posts")
make_request("POST", "/posts", json=data)
```

### Завдання 12

Додати assertions через `pytest`

Приклад:

```python
def test_get_post():
    response = requests.get(BASE_URL + "/posts/1")
    assert response.status_code == 200
```

# Критерії оцінювання

| Критерій              | Бали |
| --------------------- | ---- |
| GET tests             | 20   |
| POST/PUT/PATCH/DELETE | 40   |
| Negative tests        | 20   |
| Code quality          | 10   |
| Bonus                 | 10   |

Максимум: **100 балів**

## Що здати

1. GitHub repository
2. файл `requirements.txt`
3. файл `README.md` з інструкцією запуску

```bash
pip install -r requirements.txt
pytest
```

додатковий челендж: оформити це як маленький API framework з папками:

```text
project/
    tests/
    api/
    utils/
    conftest.py
```
