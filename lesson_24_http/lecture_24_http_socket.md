# Заняття 24. Мережеве програмування та сокети

## Мета заняття

Після заняття ви зможете:

* пояснити різницю між TCP та UDP;
* розуміти модель клієнт-сервер;
* використовувати модуль `socket`;
* створювати TCP-клієнтів та сервери;
* реалізовувати Echo Server;
* надсилати HTTP-запити;
* створювати власний HTTP-сервер.

# Що таке мережеве програмування

Мережеве програмування — це обмін даними між програмами через мережу.

Наприклад:

* браузер ↔ веб-сайт
* Telegram ↔ сервер Telegram
* мобільний застосунок ↔ API сервер
* Python клієнт ↔ база даних

Усі ці системи обмінюються повідомленнями через мережу.

# Клієнт і сервер

У більшості випадків взаємодія будується за схемою:

```text
Клієнт  --->  Сервер
          Запит

Клієнт  <---  Сервер
         Відповідь
```

Приклад:

```text
Browser ----> google.com
           GET /

Browser <---- HTML сторінка
```

Клієнт ініціює з'єднання.

Сервер очікує запитів.

# Що таке TCP/IP

TCP/IP — основа сучасного Інтернету.

TCP забезпечує:

* доставку даних;
* правильний порядок пакетів;
* перевірку помилок;
* повторну передачу втрачених пакетів.

Приклад використання:

* HTTP
* HTTPS
* SMTP
* SSH
* PostgreSQL

# Що таке UDP

UDP працює швидше за TCP.

Особливості:

* немає підтвердження доставки;
* немає контролю порядку пакетів;
* менше службової інформації.

Використовується для:

* онлайн-ігор;
* відеодзвінків;
* стрімінгу;
* DNS-запитів.

# TCP проти UDP

| TCP                     | UDP                    |
| ----------------------- | ---------------------- |
| Надійний                | Швидкий                |
| Контроль доставки       | Без контролю           |
| Більше накладних витрат | Менше накладних витрат |
| HTTP, HTTPS             | Відео, ігри            |

Для більшості Python-застосунків використовується TCP.

# IP-адреса

Кожен пристрій у мережі має IP-адресу.

Приклади:

```text
127.0.0.1
192.168.0.10
8.8.8.8
```

# Localhost

Адреса:

```text
127.0.0.1
```

завжди вказує на поточний комп'ютер.

Це дуже зручно для розробки та тестування.

# Порт

На одному комп'ютері може працювати багато програм.

Порт дозволяє визначити, до якої програми потрібно підключитися.

Приклади:

| Сервіс            | Порт |
| ----------------- | ---- |
| HTTP              | 80   |
| HTTPS             | 443  |
| PostgreSQL        | 5432 |
| Django Dev Server | 8000 |

# Socket API

Socket — це програмний інтерфейс для роботи з мережею.

Python надає модуль:

```python
import socket
```

Саме через нього ми будемо працювати із TCP та UDP.

# Створення TCP сокета

```python
import socket

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
```

Параметри:

```python
AF_INET
```

означає IPv4.

```python
SOCK_STREAM
```

означає TCP.

# Життєвий цикл TCP сервера

Сервер зазвичай виконує такі дії:

1. Створити сокет
2. Прив'язати адресу
3. Почати прослуховування
4. Приймати клієнтів
5. Обробляти повідомлення

# Створення TCP сервера

```python
import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(("127.0.0.1", 5000))

server.listen()

print("Server started")
```

# Метод bind()

```python
server.bind(("127.0.0.1", 5000))
```

Означає:

```text
IP:   127.0.0.1
PORT: 5000
```

Сервер починає слухати цей порт.

# Метод listen()

```python
server.listen()
```

Переводить сокет у режим очікування клієнтів.

Після цього можна приймати підключення.

# Прийом клієнта

```python
client_socket, address = server.accept()

print(address)
```

Приклад:

```text
('127.0.0.1', 54500)
```

# Отримання даних

```python
data = client_socket.recv(1024)

print(data)
```

Параметр:

```python
1024
```

означає максимальний розмір буфера.

# Декодування повідомлення

Мережа передає байти.

```python
message = data.decode()

print(message)
```

# Надсилання відповіді

```python
client_socket.send(
    b"Hello Client"
)
```

або

```python
client_socket.send(
    "Hello".encode()
)
```

# Повний Echo Server

Echo Server повертає клієнту те саме повідомлення.

```python
import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(("127.0.0.1", 5000))
server.listen()

print("Server started")

client, address = server.accept()

message = client.recv(1024)

print(message.decode())

client.send(message)

client.close()
server.close()
```

# Echo Client

```python
import socket

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect(("127.0.0.1", 5000))

client.send(
    b"Hello Server"
)

response = client.recv(1024)

print(response.decode())

client.close()
```

# Що відбувається

Клієнт:

```text
Hello Server
```

надсилає серверу.

Сервер:

```text
отримав -> повернув назад
```

Клієнт отримує:

```text
Hello Server
```

# Сервер у циклі

Щоб сервер працював постійно:

```python
while True:
    client, address = server.accept()

    data = client.recv(1024)

    client.send(data)

    client.close()
```

Тепер можна обслуговувати багато клієнтів.

# UDP сокет

Створюється інакше:

```python
import socket

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)
```

Тут використовується:

```python
SOCK_DGRAM
```

замість TCP.

# Основи HTTP

HTTP — це протокол обміну між браузером та сервером.

Запит виглядає так:

```http
GET / HTTP/1.1
Host: localhost
```

# HTTP-відповідь

```http
HTTP/1.1 200 OK

Hello World
```

Код:

```text
200
```

означає успішне виконання.

# Простий HTTP сервер

Python вже має готовий HTTP сервер.

Запуск:

```bash
python -m http.server 8000
```

Після цього браузер може відкрити:

```text
http://localhost:8000
```

# Власний HTTP сервер

```python
import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(("127.0.0.1", 8080))
server.listen()

client, address = server.accept()
```

# Отримання HTTP-запиту

```python
request = client.recv(4096)

print(request.decode())
```

У консолі побачимо HTTP-запит від браузера.

# Формування HTTP відповіді

```python
response = """
HTTP/1.1 200 OK

Hello from Python server
"""
```

# Надсилання відповіді

```python
client.send(
    response.encode()
)
```

# Повний HTTP сервер

```python
import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(("127.0.0.1", 8080))
server.listen()

print("HTTP Server started")

while True:

    client, address = server.accept()

    request = client.recv(4096)

    print(request.decode())

    response = """
HTTP/1.1 200 OK

Hello from Python
"""

    client.send(response.encode())

    client.close()
```

# Перевірка роботи

Запускаємо сервер:

```bash
python server.py
```

Відкриваємо браузер:

```text
http://localhost:8080
```

Отримуємо:

```text
Hello from Python
```

# Де це використовується

Знання сокетів корисні для:

* веб-серверів;
* чатів;
* ігор;
* брокерів повідомлень;
* API;
* систем моніторингу;
* IoT пристроїв.

# Підсумок

На цьому занятті ми:

* розібрали модель клієнт-сервер;
* вивчили TCP та UDP;
* познайомилися з модулем `socket`;
* створили Echo Server;
* створили Echo Client;
* розібрали структуру HTTP;
* написали власний HTTP сервер.

Саме на сокетах побудовані веб-сервери, бази даних, месенджери та більшість сучасних мережевих застосунків.
