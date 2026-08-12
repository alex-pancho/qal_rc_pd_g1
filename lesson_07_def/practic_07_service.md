```layout
1
```
# Module 1 · Практична робота
## CLI-система для записів клієнтів і замовлень
Python Basics + Git · QALight Training Center```layout
3
```
# Що будуємо
## Простий CLI-застосунок без збереження даних

Користувач може:

- **Додати клієнта** — ввести ім'я та зберегти у список
- **Створити запис/замовлення** — обрати клієнта та деталі
- **Переглянути список** — вивести всі записи
- **Видалити запис** — прибрати за номером
- **Вийти** — завершити програму

> Дані зберігаються тільки під час роботи програми (у пам'яті)```layout
4
```
# Точка входу
## `main.py` — цикл меню

```python
def main():
    clients = []
    orders = []

    while True:
        print("\n1. Add client")
        print("2. Create appointment/order")
        print("3. Show appointments/orders")
        print("4. Delete")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_client(clients)
        elif choice == "2":
            create_order(clients, orders)
        elif choice == "3":
            show_orders(orders)
        elif choice == "4":
            delete_order(orders)
        elif choice == "5":
            print("Goodbye!"); break
        else:
            print("Unknown option, try again")
``````layout
9
```
# Функція: додати клієнта
## `add_client()` — `input()` + `list.append()`

```python
def add_client(clients):
    name = input("Client name: ").strip()

    if name == "":
        print("Name cannot be empty")
        return

    clients.append(name)
    print(f"Client '{name}' added")
``````layout
4
```
# Структура запису
## Auto Service vs Beauty Clinic

```python
# Auto Service
order = {
    "client": "John",
    "vehicle": "Toyota Camry",
    "status": "Created"
}

# Beauty Clinic
appointment = {
    "client": "Anna",
    "procedure": "Facial Cleaning",
    "status": "Scheduled"
}
``````layout
9
```
# Функція: створити запис
## `create_order()` — dict + список клієнтів

```python
def create_order(clients, orders):
    if len(clients) == 0:
        print("No clients yet. Add a client first.")
        return

    print("Clients:", clients)
    client = input("Client name: ").strip()

    if client not in clients:
        print("Client not found")
        return

    vehicle = input("Vehicle (e.g. Toyota Camry): ").strip()

    order = {
        "client": client,
        "vehicle": vehicle,
        "status": "Created"
    }
    orders.append(order)
    print("Order created!")
``````layout
4
```
# Функція: показати записи
## `show_orders()` — `enumerate()` + `for`

```python
def show_orders(orders):
    if len(orders) == 0:
        print("No orders yet")
        return

    print("\n--- Orders ---")
    for i, order in enumerate(orders):
        print(f"{i + 1}. {order['client']} | "
              f"{order['vehicle']} | "
              f"{order['status']}")
``````layout
9
```
# Функція: видалити запис
## `delete_order()` — `int()` + `list.pop()`

```python
def delete_order(orders):
    if len(orders) == 0:
        print("Nothing to delete")
        return

    show_orders(orders)
    raw = input("Enter order number to delete: ")

    if not raw.isdigit():
        print("Please enter a number")
        return

    index = int(raw) - 1

    if index < 0 or index >= len(orders):
        print("Order not found")
        return

    removed = orders.pop(index)
    print(f"Deleted: {removed['client']} — {removed['vehicle']}")
``````layout
3
```
# Що практикуємо
## Концепції модуля 1 у цій роботі

| Концепція | Де використовується |
|-----------|---------------------|
| `input()` / `print()` | Меню, введення даних |
| `if / elif / else` | Вибір пункту меню, валідація |
| `while True` | Головний цикл програми |
| `for` + `enumerate` | Виведення списку записів |
| `def` + аргументи | Кожна з 4 функцій |
| `list` | Список клієнтів і замовлень |
| `dict` | Структура одного запису |```layout
4
```
# Git — фіксуємо результат
## Три команди після завершення роботи

```bash
# Ініціалізація репозиторію (один раз)
git init

# Додати всі файли до індексу
git add .

# Зробити перший коміт
git commit -m "lesson 1-7 service management"
``````layout
3
```
# Самостійне завдання
## Розширте застосунок — оберіть одне або більше

- **Лічильник** — показати кількість записів у меню
- **Статус** — функція зміни статусу замовлення (`Created → In Progress → Done`)
- **Пошук** — знайти всі записи конкретного клієнта
- **Beauty Clinic** — замість vehicle зробити `procedure` + `master`
- **Валідація** — заборонити дублікати імен клієнтів```layout
13
```
# Підсумок модуля 1
## Що реалізували

- CLI-застосунок із меню на `while` + `if/elif`
- Чотири функції з чіткою відповідальністю
- Дані у списках словників (`list of dicts`)
- Базова валідація введення користувача
- Репозиторій Git із першим комітом```layout
10
```
# Що далі: ООП + файли

У наступному модулі перепишемо цей самий застосунок із класами, додамо збереження у файл і покриємо тестами