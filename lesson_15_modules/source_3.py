import os
import sys
from pathlib import Path
from datetime import datetime
import random

from geometry import *

# os — система
print(os.getcwd())                     # поточна директорія
print(os.path.exists("myfile.txt"))    # чи існує файл
# os.makedirs("new_dir", exist_ok=True)  # створити директорію

# sys — інтерпретатор
print(sys.version)       # версія Python
print(sys.argv)          # аргументи командного рядка

# pathlib — сучасні шляхи
base = Path("project")
config_path = base / "config" / "settings.json"  # OS-незалежний шлях
print(config_path)       # project/config/settings.json

# datetime
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M"))  # 2024-01-15 10:30

# random
print(random.randint(1, 100))          # випадкове число 1–100
print(random.choice(["яблуко", "груша", "слива"]))  # випадковий елемент

def ono_one():
    pass

def two_two():
    pass

__all__ = ["ono_one"]

c = Circle(2)
r = Rectangle(10, 20)
# i = _InternalHelper()