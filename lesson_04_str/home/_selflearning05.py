# -*- coding: utf-8 -*-
"""
Завдання 5: Пошук та заміна в строках
Навчіться використовувати методи find() та replace()
"""

# Дані для роботи
text1 = "Hello world Hello everyone"
text2 = "Python is great, Python is powerful"
text3 = "JavaScript programming language"
text4 = "Good morning, good afternoon, good evening"
text5 = "apple,banana,apple,orange,apple"

print("Вихідні дані:")
print("text1:", text1)
print("text2:", text2)
print("text3:", text3)
print("text4:", text4)
print("text5:", text5)

# Завдання 5.1: Знайдіть позицію першого входження "Hello" в text1
position_hello = # Ваш код тут

# Завдання 5.2: Знайдіть позицію першого входження "Python" в text2
position_python = # Ваш код тут

# Завдання 5.3: Знайдіть позицію "Java" в text2 (слова, якого там немає)
position_java = # Ваш код тут

# Завдання 5.4: Знайдіть позицію "Script" в text3
position_script = # Ваш код тут

# Завдання 5.5: Замініть всі входження "Hello" на "Hi" в text1
text1_replaced = # Ваш код тут

# Завдання 5.6: Замініть всі входження "Python" на "Java" в text2
text2_replaced = # Ваш код тут

# Завдання 5.7: Замініть "JavaScript" на "Python" в text3
text3_replaced = # Ваш код тут

# Завдання 5.8: Замініть всі входження "good" на "great" в text4
text4_replaced = # Ваш код тут

# Завдання 5.9: Замініть тільки перше входження "apple" на "cherry" в text5
text5_replaced_first = # Ваш код тут (використайте третій параметр у replace)

# Завдання 5.10: Замініть всі входження "apple" на "cherry" в text5
text5_replaced_all = # Ваш код тут

# Завдання 5.11: Знайдіть позицію "world" в text1
position_world = # Ваш код тут

# Завдання 5.12: Замініть "," на " | " в text5
text5_with_pipes = # Ваш код тут

# Виведення результатів
print("\n=== ПОШУК ===")
print("5.1 Позиція 'Hello' в text1:", position_hello)
print("5.2 Позиція 'Python' в text2:", position_python)
print("5.3 Позиція 'Java' в text2:", position_java)
print("5.4 Позиція 'Script' в text3:", position_script)
print("5.11 Позиція 'world' в text1:", position_world)

print("\n=== ЗАМІНА ===")
print("5.5 text1 (Hello -> Hi):", text1_replaced)
print("5.6 text2 (Python -> Java):", text2_replaced)
print("5.7 text3 (JavaScript -> Python):", text3_replaced)
print("5.8 text4 (good -> great):", text4_replaced)
print("5.9 text5 (перше apple -> cherry):", text5_replaced_first)
print("5.10 text5 (всі apple -> cherry):", text5_replaced_all)
print("5.12 text5 (коми на |):", text5_with_pipes)

# Правильні відповіді для самоперевірки:
# 5.1: 0
# 5.2: 0
# 5.3: -1
# 5.4: 4
# 5.5: "Hi world Hi everyone"
# 5.6: "Java is great, Java is powerful"
# 5.7: "Python programming language"
# 5.8: "Great morning, great afternoon, great evening"
# 5.9: "cherry,banana,apple,orange,apple"
# 5.10: "cherry,banana,cherry,orange,cherry"
# 5.11: 6
# 5.12: "apple | banana | apple | orange | apple"