import requests
    
url = 'http://jsonplaceholder.typicode.com/posts/1/comments'
response = requests.get(url)

# Перевірка статус-коду
if response.status_code == 200:
    data = response.json()  # отримання даних у форматі JSON
    print('Отримано дані:', data)
else:
    print('Помилка. Статус-код:', response.status_code)