# -*- coding: utf-8 -*-
"""
Завдання 6: Обрізання зайвих символів
Навчіться використовувати методи strip(), lstrip(), rstrip()
"""

# Дані для роботи
text1 = "   Hello World   "
text2 = "\t\tPython Programming\t\t"
text3 = "\n\nJavaScript\n\n"
text4 = "   Good morning everyone   "
text5 = "***Welcome to Ukraine***"
text6 = "    "

print("Вихідні дані (показані з лапками для наочності):")
print("text1: '" + text1 + "'")
print("text2: '" + text2 + "'")
print("text3: '" + text3 + "'")
print("text4: '" + text4 + "'")
print("text5: '" + text5 + "'")
print("text6: '" + text6 + "'")

# Завдання 6.1: Видаліть пробіли з обох кінців text1
text1_strip = # Ваш код тут

# Завдання 6.2: Видаліть пробіли тільки з початку text1
text1_lstrip = # Ваш код тут

# Завдання 6.3: Видаліть пробіли тільки з кінця text1
text1_rstrip = # Ваш код тут

# Завдання 6.4: Видаліть табуляції з обох кінців text2
text2_strip = # Ваш код тут

# Завдання 6.5: Видаліть табуляції тільки з початку text2
text2_lstrip = # Ваш код тут

# Завдання 6.6: Видаліть символи нового рядка з обох кінців text3
text3_strip = # Ваш код тут

# Завдання 6.7: Видаліть пробіли з обох кінців text4
text4_strip = # Ваш код тут

# Завдання 6.8: Видаліть символи "*" з обох кінців text5
text5_strip_stars = # Ваш код тут (використайте strip("*"))

# Завдання 6.9: Видаліть символи "*" тільки з початку text5
text5_lstrip_stars = # Ваш код тут

# Завдання 6.10: Видаліть символи "*" тільки з кінця text5
text5_rstrip_stars = # Ваш код тут

# Завдання 6.11: Перевірте довжину text6 до та після strip
text6_length_before = # Ваш код тут
text6_stripped = # Ваш код тут
text6_length_after = # Ваш код тут

# Завдання 6.12: Комбінована операція - спочатку strip, потім upper для text1
text1_strip_upper = # Ваш код тут

# Виведення результатів
print("\n=== РЕЗУЛЬТАТИ (показані з лапками) ===")
print("6.1 text1 strip(): '" + text1_strip + "'")
print("6.2 text1 lstrip(): '" + text1_lstrip + "'")
print("6.3 text1 rstrip(): '" + text1_rstrip + "'")
print("6.4 text2 strip(): '" + text2_strip + "'")
print("6.5 text2 lstrip(): '" + text2_lstrip + "'")
print("6.6 text3 strip(): '" + text3_strip + "'")
print("6.7 text4 strip(): '" + text4_strip + "'")
print("6.8 text5 strip('*'): '" + text5_strip_stars + "'")
print("6.9 text5 lstrip('*'): '" + text5_lstrip_stars + "'")
print("6.10 text5 rstrip('*'): '" + text5_rstrip_stars + "'")
print("6.11 text6 довжина до strip:", text6_length_before)
print("6.11 text6 після strip: '" + text6_stripped + "'")
print("6.11 text6 довжина після strip:", text6_length_after)
print("6.12 text1 strip + upper: '" + text1_strip_upper + "'")

# Правильні відповіді для самоперевірки:
# 6.1: "Hello World"
# 6.2: "Hello World   "
# 6.3: "   Hello World"
# 6.4: "Python Programming"
# 6.5: "Python Programming\t\t"
# 6.6: "JavaScript"
# 6.7: "Good morning everyone"
# 6.8: "Welcome to Ukraine"
# 6.9: "Welcome to Ukraine***"
# 6.10: "***Welcome to Ukraine"
# 6.11 довжина до: 4, після: 0
# 6.12: "HELLO WORLD"