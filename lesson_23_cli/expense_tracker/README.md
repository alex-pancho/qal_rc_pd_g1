expense_tracker/
├── main.py          ← точка входу, зв'язує CLI, конфіг та логіку
├── cli.py           ← парсер команд та аргументів (argparse)
├── config.py        ← завантаження .env та config.ini
├── models.py        ← класи Transaction, User та винятки
├── storage.py       ← бізнес-логіка Budget + збереження у JSON/CSV
├── .env             ← секретні/середовищні змінні
├── config.ini       ← публічні налаштування (валюта, шляхи)
└── .gitignore       ← ігнорування .env, логів та файлів даних

