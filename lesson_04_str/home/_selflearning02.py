# -*- coding: utf-8 -*-
"""
Завдання 2: Розділення та об'єднання строк
Навчіться використовувати методи split() та join()
"""

# Дані для роботи
text1 = "apple,orange,banana,grape"
text2 = "Hello world Python programming"
text3 = "one-two-three-four-five"
text4 = "red|green|blue|yellow"

print("Вихідні дані:")
print("text1:", text1)
print("text2:", text2)
print("text3:", text3)
print("text4:", text4)

# Завдання 2.1: Розділіть text1 за комами
split_by_comma = # Ваш код тут

# Завдання 2.2: Розділіть text2 за пробілами
split_by_space = # Ваш код тут

# Завдання 2.3: Розділіть text3 за дефісами
split_by_dash = # Ваш код тут

# Завдання 2.4: Розділіть text4 за символом "|"
split_by_pipe = # Ваш код тут

# Завдання 2.5: Об'єднайте результат з 2.1 через " | "
join_with_pipe = # Ваш код тут

# Завдання 2.6: Об'єднайте результат з 2.2 через " - "
join_with_dash = # Ваш код тут

# Завдання 2.7: Об'єднайте результат з 2.3 через " + "
join_with_plus = # Ваш код тут

# Завдання 2.8: Об'єднайте результат з 2.4 через " AND "
join_with_and = # Ваш код тут

# Завдання 2.9: Розділіть text1 за комами, але тільки перші 2 розділення
split_limited = # Ваш код тут

# Завдання 2.10: Створіть список з трьох слів та об'єднайте їх через ", "
word_list = ["Python", "Java", "JavaScript"]
join_languages = # Ваш код тут

# Виведення результатів
print("\n=== РЕЗУЛЬТАТИ ===")
print("2.1 Розділення за комами:", split_by_comma)
print("2.2 Розділення за пробілами:", split_by_space)
print("2.3 Розділення за дефісами:", split_by_dash)
print("2.4 Розділення за |:", split_by_pipe)
print("2.5 Об'єднання через |:", join_with_pipe)
print("2.6 Об'єднання через -:", join_with_dash)
print("2.7 Об'єднання через +:", join_with_plus)
print("2.8 Об'єднання через AND:", join_with_and)
print("2.9 Обмежене розділення:", split_limited)
print("2.10 Мови програмування:", join_languages)

# Правильні відповіді для самоперевірки:
# 2.1: ['apple', 'orange', 'banana', 'grape']
# 2.2: ['Hello', 'world', 'Python', 'programming']
# 2.3: ['one', 'two', 'three', 'four', 'five']
# 2.4: ['red', 'green', 'blue', 'yellow']
# 2.5: "apple | orange | banana | grape"
# 2.6: "Hello - world - Python - programming"
# 2.7: "one + two + three + four + five"
# 2.8: "red AND green AND blue AND yellow"
# 2.9: ['apple', 'orange', 'banana,grape']
# 2.10: "Python, Java, JavaScript"