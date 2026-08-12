## Практична частина — Арифметичний калькулятор

На цьому занятті ми створимо перший повноцінний структурований Python-проєкт: консольний арифметичний калькулятор із ізольованим середовищем, правильною структурою файлів та точкою входу.

### Крок 1. Ініціалізація проєкту через uv

```bash
# Створюємо новий проєкт
uv init calculator

# Переходимо до папки проєкту
cd calculator

# Перевіряємо структуру
ls -la
```

`uv` автоматично:
- Створить папку `calculator/` із базовою структурою.
- Ініціалізує `pyproject.toml` з метаданими.
- Створить `.venv` (у деяких версіях — при першому `uv run`).
- Додасть базовий `.gitignore`.

```bash
# Перевіряємо, що venv створено
ls .venv/

# Запускаємо тестовий скрипт через uv (uv автоматично активує venv)
uv run main.py
```

### Крок 2. Організація структури файлів

Видалимо стандартний `main.py` і створимо власну структуру:

```
calculator/
├── .venv/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── main.py                 ← точка входу
└── calculator/             ← наш пакет
    ├── __init__.py
    └── operations.py       ← бізнес-логіка
```

Створіть папку `calculator/` усередині проєкту та два файли:

```bash
mkdir calculator
touch calculator/__init__.py
touch calculator/operations.py
```

### Крок 3. Написання модуля operations.py

Відкрийте `calculator/operations.py` у VS Code і додайте чотири функції — по одній на кожну арифметичну операцію.

Кожна функція:
- Приймає два числа типу `float`.
- Повертає результат типу `float`.
- Має рядок документації (`docstring`).
- Обробляє крайні випадки (ділення на нуль).

```python
# calculator/operations.py


def add(a: float, b: float) -> float:
    """Повертає суму двох чисел.

    Args:
        a: Перше число.
        b: Друге число.

    Returns:
        Сума a та b.

    Example:
        >>> add(3, 5)
        8.0
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Повертає різницю двох чисел (a мінус b).

    Args:
        a: Від'ємне число (зменшуване).
        b: Число, яке віднімається (від'ємник).

    Returns:
        Різниця a та b.

    Example:
        >>> subtract(10, 3)
        7.0
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Повертає добуток двох чисел.

    Args:
        a: Перший множник.
        b: Другий множник.

    Returns:
        Добуток a та b.

    Example:
        >>> multiply(4, 3)
        12.0
    """
    return a * b


def divide(a: float, b: float) -> float:
    """Ділить a на b і повертає результат.

    Args:
        a: Ділене.
        b: Дільник. Не може бути нулем.

    Returns:
        Частка a та b.

    Raises:
        ValueError: Якщо b дорівнює нулю.

    Example:
        >>> divide(10, 2)
        5.0
    """
    if b == 0:
        raise ValueError("Ділення на нуль неможливе. Введіть ненульовий дільник.")
    return a / b
```

### Крок 4. Ініціалізація пакету (__init__.py)

Файл `__init__.py` може бути порожнім, але ми додамо імпорти для зручності:

```python
# calculator/__init__.py
"""
Пакет calculator — арифметичні операції.

Надає чотири базові математичні функції:
    - add(a, b)       → a + b
    - subtract(a, b)  → a − b
    - multiply(a, b)  → a × b
    - divide(a, b)    → a ÷ b (з обробкою ділення на нуль)
"""

from calculator.operations import add, subtract, multiply, divide

__all__ = ["add", "subtract", "multiply", "divide"]
```

Завдяки цьому в `main.py` можна буде писати:

```python
from calculator import add, subtract  # коротший імпорт
```

замість:

```python
from calculator.operations import add, subtract  # повний шлях
```

### Крок 5. Написання точки входу main.py

Тепер напишемо `main.py` — інтерактивний консольний інтерфейс калькулятора.

```python
# main.py
"""
Арифметичний калькулятор — точка входу програми.

Запуск:
    uv run main.py
    або
    python main.py
"""

from calculator.operations import add, subtract, multiply, divide


# Словник операцій: символ → функція
OPERATIONS: dict[str, callable] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def get_number(prompt: str) -> float:
    """Запитує у користувача число, повторює при невалідному введенні.

    Args:
        prompt: Текст запиту для користувача.

    Returns:
        Число типу float, введене користувачем.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            return float(user_input)
        except ValueError:
            print(f"  Помилка: '{user_input}' — не є числом. Спробуйте ще раз.\n")


def get_operation() -> str:
    """Запитує у користувача операцію, повторює при невалідному введенні.

    Returns:
        Рядок з символом операції (+, -, *, /) або 'q' для виходу.
    """
    available = list(OPERATIONS.keys())
    while True:
        user_input = input(f"Оберіть операцію {available} або 'q' для виходу: ").strip()
        if user_input == "q":
            return "q"
        if user_input in OPERATIONS:
            return user_input
        print(f"  Помилка: операція '{user_input}' не підтримується.\n")


def calculate(a: float, op: str, b: float) -> float | None:
    """Виконує обрану операцію над двома числами.

    Args:
        a: Перше число.
        op: Символ операції.
        b: Друге число.

    Returns:
        Результат обчислення або None у разі помилки.
    """
    try:
        result = OPERATIONS[op](a, b)
        return result
    except ValueError as error:
        print(f"  Помилка: {error}\n")
        return None


def format_result(a: float, op: str, b: float, result: float) -> str:
    """Форматує рядок результату, видаляючи зайві нулі у цілих чисел.

    Args:
        a: Перше число.
        op: Символ операції.
        b: Друге число.
        result: Результат обчислення.

    Returns:
        Відформатований рядок із результатом.
    """
    # Виводимо ціле число без .0, якщо результат цілий
    def fmt(n: float) -> str:
        return str(int(n)) if n == int(n) else str(n)

    return f"  {fmt(a)} {op} {fmt(b)} = {fmt(result)}"


def main() -> None:
    """Головна функція — запускає інтерактивний цикл калькулятора."""
    print("=" * 40)
    print("  Арифметичний калькулятор")
    print("=" * 40)
    print("Підтримувані операції: +, -, *, /")
    print("Введіть 'q' для виходу.\n")

    while True:
        op = get_operation()

        if op == "q":
            print("\nДо побачення!")
            break

        a = get_number("Введіть перше число:  ")
        b = get_number("Введіть друге число:  ")

        result = calculate(a, op, b)

        if result is not None:
            print("\nРезультат:")
            print(format_result(a, op, b, result))
            print()


if __name__ == "__main__":
    main()
```

### Крок 6. Запуск та тестування

```bash
# Запускаємо через uv (рекомендовано)
uv run main.py

# Або напряму через python (якщо venv активовано)
python main.py
```

**Сценарії для перевірки під час заняття:**

| Сценарій | Що перевіряємо |
|:---------|:---------------|
| `10 + 5` | Базове додавання, форматування цілого результату |
| `7.5 - 3.2` | Робота з дробовими числами |
| `6 * 7` | Множення |
| `15 / 4` | Ділення з дробовим результатом |
| `10 / 0` | Обробка помилки ділення на нуль |
| `abc + 5` | Обробка невалідного введення числа |
| `# + 5` | Обробка невідомої операції |
| `q` | Коректний вихід із програми |

### Крок 7. Перегляд залежностей та структури

```bash
# Переглянути поточний pyproject.toml
cat pyproject.toml

# Переглянути структуру проєкту
find . -not -path './.venv/*' -not -name '*.pyc' -not -path './__pycache__/*'

# Додати нову залежність (наприклад, для красивого виведення)
uv add rich

# Перевірити, що залежність з'явилася в pyproject.toml
cat pyproject.toml
```

## Самостійна робота

### Завдання 1 (базовий рівень)

Розширте калькулятор двома новими операціями:

- `**` — піднесення до степеня (`a ** b`)
- `%` — залишок від ділення (`a % b`)

**Що потрібно зробити:**

1. Додайте дві нові функції до `calculator/operations.py`:
   - `power(a, b)` — повертає `a ** b`
   - `modulo(a, b)` — повертає `a % b` з перевіркою ділення на нуль

2. Додайте нові операції до словника `OPERATIONS` у `main.py`.

3. Перевірте роботу: `2 ** 8` має повернути `256`, `17 % 5` — `2`.

### Завдання 2 (поглиблений рівень)

Додайте **історію обчислень**:

1. Зберігайте кожен успішний результат у список `history` всередині функції `main()`.
2. Додайте операцію `h` (history) — виведіть останні 5 обчислень.
3. Додайте операцію `c` (clear) — очистіть історію.

Приклад формату виведення:

```
Останні обчислення:
  1. 10 + 5 = 15
  2. 7.5 - 3.2 = 4.3
  3. 6 * 7 = 42
```

### Завдання 3 (для допитливих)

Дослідіть поведінку `__name__`:

1. Додайте у `calculator/operations.py` рядок:
   ```python
   print(f"operations.py: __name__ = {__name__}")
   ```

2. Запустіть `uv run main.py` — що виводиться?

3. Запустіть `uv run calculator/operations.py` — що змінилося і чому?

4. Видаліть рядок із `print` після перевірки.

