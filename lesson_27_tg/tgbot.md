Створення Telegram-бота на Python — це доволі простий процес, який складається з реєстрації бота через BotFather, встановлення бібліотеки для роботи з API Telegram та написання коду для обробки повідомлень. [freecodecamp](https://www.freecodecamp.org/ukrainian/news/yak-stvoryty-telehram-bota-za-dopomohoyu-python/)

## Крок 1: Отримання токена бота

Спочатку потрібно зареєструвати свого бота в Telegram:

1. Знайдіть у пошуку Telegram офіційного бота **@BotFather**
2. Надішліть команду `/start` для початку діалогу
3. Відправте команду `/newbot` для створення нового бота
4. Введіть ім'я бота (відображається у списку чатів)
5. Створіть унікальний username для бота (має закінчуватися на `bot`, наприклад `my_test_bot`)
6. BotFather видасть вам **API-токен** — довгий рядок символів, який потрібно зберегти [freecodecamp](https://www.freecodecamp.org/ukrainian/news/yak-stvoryty-telehram-bota-za-dopomohoyu-python/)

## Крок 2: Встановлення бібліотеки

Найпопулярніші бібліотеки для роботи з Telegram API:

- **pyTelegramBotAPI** (telebot) — найпростіша для початківців
- **python-telegram-bot** — потужніша, підтримує асинхронність (версії 20.x+)

Встановіть одну з них через pip:

```bash
pip install pyTelegramBotAPI
```

або

```bash
pip install python-telegram-bot
```

## Крок 3: Базовий код бота

Ось приклад мінімального бота з використанням `pyTelegramBotAPI`:

```python
import telebot

# Замініть на ваш токен від BotFather
BOT_TOKEN = 'ВАШ_ТОКЕН_ТУТ'

bot = telebot.TeleBot(BOT_TOKEN)

# Обробник команди /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я ваш Telegram-бот 🤖")

# Обробник текстових повідомлень
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Ви написали: {message.text}")

# Запуск бота
print("Бот запущений...")
bot.infinity_polling()
```

Запустіть файл командою `python bot.py` у терміналі, після чого ваш бот почне відповідати на повідомлення. [freecodecamp](https://www.freecodecamp.org/ukrainian/news/yak-stvoryty-telehram-bota-za-dopomohoyu-python/)

## Крок 4: Додавання кнопок (опціонально)

Для створення кнопок використовуйте `types` з бібліотеки:

```python
from telebot import types

@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('📌 Кнопка 1')
    item2 = types.KeyboardButton('📌 Кнопка 2')
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, "Оберіть опцію:", reply_markup=markup)
```

Це створить клавіатуру з кнопками під полем введення повідомлення. [otus](https://otus.ru/journal/python-bot-dlya-telegram-sozdanie-knopok-i-menju/)

## Крок 5: Запуск на сервері (для цілодобової роботи)

Щоб бот працював постійно, розмістіть його на сервері:

1. Завантажте код на VPS (наприклад, через Git або SCP)
2. Використовуйте `systemd` або `supervisor` для автоматичного запуску
3. Або використайте хмарні сервіси типу Heroku, Railway, Render [sky](https://sky.pro/wiki/python/kak-napisat-i-zapustit-bota-v-telegram-na-python/)

Приклад створення systemd-сервісу:

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Вміст файлу:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 /path/to/bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Після цього виконайте:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-bot
```

## Корисні поради

- Зберігайте токен у змінних оточення або файлі `.env`, а не в коді
- Використовуйте віртуальне оточення (`python -m venv venv`) для ізоляції залежностей
- Для складніших ботів розгляньте асинхронні бібліотеки (`aiogram`, `python-telegram-bot` 20.x+)


https://itisfuture.in.ua/yak-stvoryty-bota-v-telehram-na-python/
