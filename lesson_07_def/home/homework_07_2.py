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