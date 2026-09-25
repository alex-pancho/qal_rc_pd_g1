import requests
import json
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
    


base_url = "https://jsonplaceholder.typicode.com"
posts = f"{base_url}/posts"
# posts = "https://car-service-api-and-ui.onrender.com/"
response = requests.get(posts)

print(response)
print(response.status_code)
print(response.headers)
# print(response.text)
if response.status_code == 200:
    data = response.json()  # отримання даних у форматі JSON
    print('Отримано дані:', data)
    print(type(data), type(data[0]))
else:
    print('Помилка. Статус-код:', response.status_code)


print("*"*88)
article = f"{posts}/1/comments"
params = {'email': 'Nikita@garfield.biz'}
# params = dict(email='Nikita@garfield.biz')

response = requests.get(article, params=params)
print(response.text)
if response.status_code == 200:
    data = response.json()  # отримання даних у форматі JSON
    print('Отримано дані:', data)
print(response.url)

data_to_send = {'userId': 10, "body": 'bar', 'title': 'Some title'}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0"}

response = requests.post(posts, json=data_to_send, headers=headers)
# Перевірка статус-коду
if response.status_code == 201:
    created_data = response.json()  # отримання даних у форматі JSON
    print('Створено дані:', created_data)
else:
    print('Помилка. Статус-код:', response.status_code)

print("Запит заголовки", response.request.headers)
print("Запит урл", response.request.url)
print("Запит тіло", response.request.body)
print("Відповідь заголовки", response.headers)
print("Відповідь урл", response.url)


first_post = f"{posts}/1"
data_to_send = {'userId': 1, 'id': 1, 'title': 'New title'}

response = requests.put(first_post, data=data_to_send)

# Перевірка статус-коду
if response.status_code == 200:
    updated_data = response.text  # отримання даних у форматі текст
    print('Оновлено дані:', updated_data)
else:
    print('Помилка. Статус-код:', response.status_code)


params = {'userId': 1, 'id':1, 'title': 'New title'}
response = requests.delete(first_post, params=params)

# Перевірка статус-коду
if response.status_code == 200:
    print('Дані успішно видалено')
else:
    print('Помилка. Статус-код:', response.status_code)


# відправка даних
url = 'https://uk.imgbb.com/json'
headers = {'User-Agent': 'MyAgent'}
files = {'file': open('windows_98_logo.png', 'rb')}
timeout = 10

resp = requests.post(url, headers=headers, files=files, timeout=timeout)
print(resp.request.body)
# input("type enter")
print(resp.json())

    
#### ERROR

    
try:
    response = requests.get('https://example.com')
    response.raise_for_status()  # Викликає виняток, якщо код не 2xx 3xx
except HTTPError as e:
    print('HTTP Помилка:', e)
    
try:
    response = requests.get('https://exitisksdjiejjkenjehfuehuele.com')
except ConnectionError as e:
    print('Помилка з\'єднання:', e)

try:
    # Встановлення таймауту
    response = requests.get('https://example.com', timeout=0.2)
except Timeout as e:
    print('Часова помилка:', e)

try:
    data = response.json()
    print('Отримано дані:', data)
except json.JSONDecodeError as e:
    print('Помилка при серіалізації JSON:', e)
    data = {"text": response.text}
