""" Задача - надрукувати табличку множення на задане число, але
лише до максимального значення для добутку - 25.
Код майже готовий, треба знайти помилки та випраавити\доповнити.
"""
def multiplication_table(number):
    # Initialize the appropriate variable
    multiplier = 1

    # Complete the while loop condition.
    while true  # цикл працює, поки ми його не зупинимо 
        result = number * multiplier
      
        if  result > 25: # якщо добуток більше 25 — стоп
            break
           
        print(str(number) + "x" + str(multiplier) + "=" + str(result))

        # Increment the appropriate variable
        multiplier += 1

multiplication_table(3)
# Should print:
# 3x1=3
# 3x2=6
# 3x3=9
# 3x4=12
# 3x5=15


# task 2
"""  Написати функцію, яка обчислює суму двох чисел.
"""
def add_numbers(a, b):
    """Повертає суму двох чисел."""
    return a + b

# task 3
"""  Написати функцію, яка розрахує середнє арифметичне списку чисел.
"""
def average(numbers):
    """Повертає середнє арифметичне списку чисел."""
    return sum(numbers) / len(numbers)

# task 4
"""  Написати функцію, яка приймає рядок та повертає його у зворотному порядку.
"""
def reverse_string(text):
    """Повертає рядок у зворотному порядку."""
    return "".join(reversed(text))

# task 5
"""  Написати функцію, яка приймає список слів та повертає найдовше слово у списку.
"""
def longest_word(words):
    """Повертає найдовше слово зі списку."""
    return max(words, key=lambda w: len(w))

# task 6
"""  Написати функцію, яка приймає два рядки та повертає індекс першого входження другого рядка
у перший рядок, якщо другий рядок є підрядком першого рядка, та -1, якщо другий рядок
не є підрядком першого рядка."""
def find_substring(str1, str2):

    return str1.find(str2) 

str1 = "Hello, world!"
str2 = "world"
print(find_substring(str1, str2)) # поверне 7

str1 = "The quick brown fox jumps over the lazy dog"
str2 = "cat"
print(find_substring(str1, str2)) # поверне -1

# task 7
def count_vowels(text):
    """
    Повертає кількість голосних у тексті.
    """
    vowels = "аеиіїоуюя"
    count = 0
    for char in text.lower():
        if char in vowels:
            count += 1
    return count

# task 8
def is_leap_year(year):
    """
    Повертає True, якщо рік високосний, і False — якщо ні.
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# task 9
def unique_elements(lst):
    """
    Повертає список унікальних елементів.
    """
    return list(set(lst))

# task 10
def count_capital_words(text):
    """
    Повертає кількість слів, що починаються з великої літери.
    """
    words = text.split()
    count = 0
    for word in words:
        if word[0].isupper():
            count += 1
    return count

"""  Оберіть будь-які 4 таски з попередніх домашніх робіт та
перетворіть їх у 4 функції, що отримують значення та повертають результат.
Обов'язково документуйте функції та дайте зрозумілі імена змінним.
"""