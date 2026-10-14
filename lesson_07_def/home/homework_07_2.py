# task 1
""" Задача - надрукувати табличку множення на задане число, але
лише до максимального значення для добутку - 25.
Код майже готовий, треба знайти помилки та випраавити\доповнити.
"""


def multiplication_table(number):
    multiplier = 1
    while True:
        result = number * multiplier
        
        if result > 25:
            break
            
        print(f"{number}x{multiplier}={result}")

        multiplier += 1

# Вызов функции
multiplication_table(3)

# task 2
"""  Написати функцію, яка обчислює суму двох чисел.
"""
def sum_two_numbers(a, b):
    return a + b
result = sum_two_numbers(5, 7)
print(f"Сумма чисел: {result}")

# task 3
"""  Написати функцію, яка розрахує середнє арифметичне списку чисел.
"""
def calculate_average(numbers):
    # Если список пустой, возвращаем 0, чтобы избежать ошибки деления на ноль
    if not numbers:
        return 0
        
    return sum(numbers) / len(numbers)

# Пример использования функции:
my_list = [10, 20, 30, 40, 50]
avg_result = calculate_average(my_list)

print(f"Среднее арифметическое: {avg_result}")
# task 4
"""  Написати функцію, яка приймає рядок та повертає його у зворотному порядку.
"""
def reverse_string(text):
    # Срез [::-1] берет всю строку от конца до начала с шагом -1
    return text[::-1]

# Пример использования функции:
original_text = "Привет, мир!"
reversed_text = reverse_string(original_text)

print(f"Оригинал: {original_text}")
print(f"Развернутая строка: {reversed_text}")  # Выведет: !рим ,тевирП
# task 5
"""  Написати функцію, яка приймає список слів та повертає найдовше слово у списку.
"""
def find_longest_word(words):
    # Если список пустой, возвращаем None, чтобы избежать ошибки
    if not words:
        return None
        
    # Функция max находит элемент с максимальным значением длины len()
    return max(words, key=len)
word_list = ["яблоко", "банан", "ананас", "киви", "мандарин"]
longest = find_longest_word(word_list)

print(f"Самое длинное слово: {longest}")
# task 6
"""  Написати функцію, яка приймає два рядки та повертає індекс першого входження другого рядка
у перший рядок, якщо другий рядок є підрядком першого рядка, та -1, якщо другий рядок
не є підрядком першого рядка."""
def find_substring(str1, str2):
    return str1.find(str2)

# Вызовы функций теперь находятся НИЖЕ её объявления
str1 = "Hello, world!"
str2 = "world"
print(find_substring(str1, str2))  # Теперь вернет 7

str1 = "The quick brown fox jumps over the lazy dog"
str2 = "cat"
print(find_substring(str1, str2))  # Теперь вернет -1

# task 7
# task 8
# task 9
# task 10
"""  Оберіть будь-які 4 таски з попередніх домашніх робіт та
перетворіть їх у 4 функції, що отримують значення та повертають результат.
Обов'язково документуйте функції та дайте зрозумілі імена змінним.
"""
# таски взято з домашьоъї роботи №5 з попередніх уроків, де вони були реалізовані без функцій.
from typing import Any, Dict, List, Sequence, TypeVar

T = TypeVar("T")


def get_unique_elements(items: Sequence[T], preserve_order: bool = True) -> List[T]:
    """Повертає список унікальних елементів із переданої послідовності.

    :param items: Вхідна послідовність (список, кортеж тощо).
    :param preserve_order: Якщо True, зберігає початковий порядок елементів.
                           Якщо False, повертає відсортована через set.
    :return: Список унікальних елементів.
    """
    if preserve_order:
        return list(dict.fromkeys(items))
    return list(set(items))


def calculate_mean(numbers: Sequence[int | float]) -> float:
    """Обчислює середнє арифметичне для списку чисел.

    :param numbers: Послідовність чисел (int або float).
    :return: Середнє арифметичне значення у вигляді float.
    :raises ValueError: Якщо передано порожній список.
    """
    if not numbers:
        raise ValueError("Неможливо обчислити середнє арифметичне порожнього списку.")
    return sum(numbers) / len(numbers)


def check_for_duplicates(items: Sequence[Any]) -> bool:
    """Перевіряє, чи містить послідовність хоча б один дублікат.

    :param items: Вхідний список або послідовність елементів.
    :return: True, якщо є дублікати, інакше False.
    """
    return len(items) != len(set(items))


def invert_dictionary(input_dict: Dict[Any, Any]) -> Dict[Any, Any]:
    """Створює новий словник, у якому ключі та значення міняються місцями.

    :param input_dict: Вхідний словник (значення мають бути хешованими).
    :return: Новий словник з інвертованими ключами та значеннями.
    """
    return {value: key for key, value in input_dict.items()}


# ПРИКЛАДИ ВИКОРИСТАННЯ ТА ПЕРЕВІРКА РЕЗУЛЬТАТІВ

# 1. Тест функції 1 (Task 1: Унікальні елементи)
numbers_list = [3, 1, 4, 5, 2, 5, 3]
unique_numbers = get_unique_elements(numbers_list)
print(f"Task 1 (Унікальні елементи): {unique_numbers}")
# Результат: [3, 1, 4, 5, 2]

# 2. Тест функції 2 (Task 2: Середнє арифметичне)
mean_value = calculate_mean(numbers_list)
print(f"Task 2 (Середнє арифметичне): {mean_value:.2f}")
# Результат: 3.29

# 3. Тест функції 3 (Task 3: Перевірка на дублікати)
data_with_duplicates = [3, 5, -2, -1, -3, 0, 1, 4, 5, 2]
has_dup = check_for_duplicates(data_with_duplicates)
print(f"Task 3 (Чи є дублікати?): {has_dup}")
# Результат: True

# 4. Тест функції 4 (Task 5: Інверсія словника)
country_info = {"contry": "Ukraine", "continent": "Europe", "size": 123}
inverted_country_info = invert_dictionary(country_info)
print(f"Task 5 (Інвертований словник): {inverted_country_info}")
# Результат: {'Ukraine': 'contry', 'Europe': 'continent', 123: 'size'}