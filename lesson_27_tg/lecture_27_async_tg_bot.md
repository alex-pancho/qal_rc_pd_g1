# Заняття 27. Асинхронне програмування та паралельність

## Мета заняття

Після заняття ви зможете:

* пояснити різницю між синхронним та асинхронним кодом;
* розуміти поняття блокуючих операцій;
* використовувати модуль `asyncio`;
* створювати асинхронні функції;
* запускати кілька задач одночасно;
* використовувати багатопоточність;
* виконувати асинхронні HTTP-запити;
* створювати Telegram-ботів на Python.

# Чому виникла асинхронність

У багатьох програмах більшість часу витрачається не на обчислення.

Програма чекає:

* відповідь сервера;
* базу даних;
* файл на диску;
* повідомлення користувача.

Приклад:

```python
response = requests.get(
    "https://example.com"
)
```

Поки сервер відповідає, Python нічого не робить.

# Блокуючі операції

Блокуюча операція зупиняє виконання програми.

Приклад:

```python
import time

print("Start")

time.sleep(5)

print("Finish")
```

Результат:

```text
Start
(очікування 5 секунд)
Finish
```

У цей момент програма повністю заблокована.

# Синхронне виконання

Задачі виконуються одна за одною.

```python
download_file_1()

download_file_2()

download_file_3()
```

Схематично:

```text
Task1 ------
             \
Task2 --------
               \
Task3 ----------
```

Кожна задача чекає завершення попередньої.

# Проблема синхронного підходу

Уявімо три HTTP-запити.

Кожен виконується 2 секунди.

```python
request_1()
request_2()
request_3()
```

Час виконання:

```text
2 + 2 + 2 = 6 секунд
```

# Асинхронне виконання

Асинхронність дозволяє виконувати кілька операцій очікування одночасно.

```text
Task1 ------
Task2 ------
Task3 ------

Загальний час ≈ 2 секунди
```

# Що таке asyncio

`asyncio` — стандартний модуль Python для асинхронного програмування.

Він використовує:

* Event Loop
* Coroutines
* Tasks

# Перша асинхронна функція

```python
import asyncio

async def hello():

    print("Hello")

asyncio.run(
    hello()
)
```

Ключове слово:

```python
async
```

створює корутину.

# Що таке coroutine

Coroutine — спеціальна функція, яку можна призупиняти.

```python
async def my_function():
    pass
```

Виклик:

```python
my_function()
```

не запускає функцію.

Створюється об'єкт coroutine.

# Await

Для запуску корутини використовується:

```python
await
```

Приклад:

```python
import asyncio

async def hello():

    await asyncio.sleep(1)

    print("Hello")
```

# Асинхронний sleep

```python
await asyncio.sleep(3)
```

На відміну від:

```python
time.sleep(3)
```

не блокує програму.

# Приклад

```python
import asyncio

async def task():

    print("Start")

    await asyncio.sleep(2)

    print("Finish")

asyncio.run(task())
```

# Кілька задач

```python
import asyncio

async def worker(name):

    print(f"{name} started")

    await asyncio.sleep(3)

    print(f"{name} finished")
```

# Запуск кількох задач

```python
import asyncio

async def main():

    await asyncio.gather(
        worker("A"),
        worker("B"),
        worker("C")
    )

asyncio.run(main())
```

# Результат

```text
A started
B started
C started

(3 секунди)

A finished
B finished
C finished
```

Усі задачі працювали одночасно.

# Event Loop

Event Loop — серце asyncio.

Його завдання:

* запускати корутини;
* переключатися між задачами;
* виконувати готові операції.

Схематично:

```text
Task A
Task B
Task C

↓
Event Loop
```

# Асинхронні HTTP-запити

Бібліотека:

```bash
pip install aiohttp
```

дозволяє виконувати HTTP-запити без блокування.

# Перший aiohttp запит

```python
import aiohttp
import asyncio

async def main():

    async with aiohttp.ClientSession() as session:

        async with session.get(
            "https://example.com"
        ) as response:

            print(response.status)

asyncio.run(main())
```

# Отримання тексту сторінки

```python
text = await response.text()

print(text[:100])
```

# Багато HTTP-запитів

```python
import asyncio
import aiohttp

async def fetch(url):

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as response:

            return response.status
```

# Паралельне виконання

```python
async def main():

    results = await asyncio.gather(
        fetch("https://google.com"),
        fetch("https://github.com"),
        fetch("https://python.org")
    )

    print(results)

asyncio.run(main())
```

# Потоки

Не всі задачі підходять для asyncio.

Іноді використовують потоки.

Модуль:

```python
threading
```

# Перший потік

```python
import threading

def worker():

    print("Working")
```

# Запуск потоку

```python
thread = threading.Thread(
    target=worker
)

thread.start()
```

# Кілька потоків

```python
import threading

for i in range(5):

    thread = threading.Thread(
        target=worker
    )

    thread.start()
```

# Коли використовувати потоки

Потоки добре працюють для:

* роботи з файлами;
* HTTP-запитів;
* читання логів;
* інтеграційних задач.

# Asyncio чи Threading

| Asyncio               | Threading                  |
| --------------------- | -------------------------- |
| Менше пам'яті         | Більше пам'яті             |
| Висока продуктивність | Простий підхід             |
| Підходить для мережі  | Підходить для старого коду |
| Один потік            | Багато потоків             |

# Telegram Bot

Telegram Bot — звичайна програма, яка отримує повідомлення та надсилає відповіді.

Для роботи потрібен токен.

Приклад:

```text
123456:ABCDEF...
```

# Створення бота

1. Відкрити BotFather
2. Виконати:

```text
/newbot
```

3. Отримати токен

# Встановлення бібліотеки

```bash
pip install python-telegram-bot
```

# Перший бот

```python
from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)
```

# Команда /start

```python
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Hello!"
    )
```

# Реєстрація команди

```python
app.add_handler(
    CommandHandler(
        "start",
        start
    )
)
```

# Запуск бота

```python
app.run_polling()
```

# Повний приклад

```python
from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

TOKEN = "YOUR_TOKEN"

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Hello from Python Bot!"
    )

app = Application.builder() \
    .token(TOKEN) \
    .build()

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.run_polling()
```

# Додавання команди /time

```python
from datetime import datetime

async def current_time(
    update,
    context
):

    await update.message.reply_text(
        str(datetime.now())
    )
```

# Реєстрація команди

```python
app.add_handler(
    CommandHandler(
        "time",
        current_time
    )
)
```

# Міні-проєкт

Створимо Telegram бота:

Команди:

```text
/start
/time
/help
```

Можливості:

* привітання користувача;
* поточний час;
* список доступних команд.

# Де використовується асинхронність

* Telegram боти
* FastAPI
* WebSocket сервери
* Чат-системи
* Біржові сервіси
* Веб-скрапери
* Системи моніторингу

# Підсумок

На цьому занятті ми:

* розібрали синхронне та асинхронне програмування;
* вивчили asyncio;
* створювали coroutine;
* використовували await;
* запускали кілька задач через gather();
* виконували асинхронні HTTP-запити;
* познайомилися з потоками;
* створили асинхронного Telegram-бота.

Асинхронне програмування є основою сучасних FastAPI-застосунків, Telegram-ботів, чатів, API-сервісів та високонавантажених мережевих систем.
