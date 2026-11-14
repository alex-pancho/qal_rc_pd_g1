# Homework 25: API Testing with Pytest and Requests

Цей проєкт містить автотести для перевірки REST API [JSONPlaceholder](https://jsonplaceholder.typicode.com).

## Структура проєкту

- `api/client.py` — обгортка над бібліотекою requests.
- `tests/test_api.py` — автотести (Завдання 1–12).
- `conftest.py` — фікстури pytest.

## Інструкція із запуску

1. Встановіть залежності:
   ```bash
   pip install -r requirements.txt