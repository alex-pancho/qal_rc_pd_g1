# import source_15
try:
    from .source_15 import outer
except ImportError:
    from source_15 import outer

import sys
# source_15.outer()
outer()

import math
print(math.sqrt(16))
print(math.pi)

from math import sqrt, pi
print(sqrt(16))
print(pi)

# import numpy as np          # стандартна угода у спільноті
# print(np.array([1, 2, 3]))

from math import factorial as F
print(F(5))

# from math import *
# print(factorial(7))

"""
1. Вже завантажені модулі (`sys.modules` — кеш)
2. Вбудовані модулі (`sys.builtin_module_names`)
3. Шляхи з `sys.path` — список директорій:
   - директорія поточного скрипта
   - директорії зі змінної середовища `PYTHONPATH`
   - директорії стандартної бібліотеки
   - директорія `site-packages` (сторонні пакети)
"""

print(sys.path)

print(math.__name__)    # 'math'       — ім'я модуля
# print(math.__file__)    # '/usr/.../math.cpython-312.pyc' — шлях до файлу
print(math.__doc__)     # рядок документації модуля
print(dir(math))        # список усіх імен, визначених у модулі
"""
| Модуль | Призначення | Приклад |
|---|---|---|
| `os` | Робота з операційною системою | `os.getcwd()`, `os.listdir()` |
| `sys` | Параметри інтерпретатора | `sys.argv`, `sys.path` |
| `math` | Математичні функції | `math.sqrt()`, `math.pi` |
| `random` | Генерація випадкових чисел | `random.randint()`, `random.choice()` |
| `datetime` | Дата і час | `datetime.now()`, `timedelta` |
| `pathlib` | Сучасна робота з шляхами | `Path("dir") / "file.txt"` |
| `json` | Серіалізація JSON | `json.dumps()`, `json.loads()` |
| `re` | Регулярні вирази | `re.findall()`, `re.sub()` |
| `collections` | Розширені структури даних | `defaultdict`, `Counter`, `deque` |
| `itertools` | Інструменти для ітерацій | `chain()`, `product()` |
| `functools` | Інструменти для функцій | `lru_cache`, `partial`, `reduce` |
"""

def main():
    pass