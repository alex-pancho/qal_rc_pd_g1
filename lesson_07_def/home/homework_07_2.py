# task 1
""" Задача - надрукувати табличку множення на задане число, але
лише до максимального значення для добутку - 25.
Код майже готовий, треба знайти помилки та випраавити\доповнити.
"""
def multiplication_table(number):
    # Initialize the appropriate variable
    multiplier = 1

    # Complete the while loop condition.
    while multiplier <= 25:
        result = number * multiplier
        # десь тут помилка, а може не одна
        if  result > 25:
            break # Enter the action to take if the result is greater than 25
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
def sum_numbers(a, b):
    return a+b
a=5
b=7
print(f"Сума чисел {a} і {b} дорівнює {sum_numbers(a, b)} ")

# task 3
"""  Написати функцію, яка розрахує середнє арифметичне списку чисел.
"""
def seredne_aryf_list(numbers):
    if len(numbers)==0:
        return 0    
    return sum(numbers)/len(numbers)
num = [2,3,4,5,6,7,8,9]
print(f"Середнє арифметичне списка {num} дорівнює {seredne_aryf_list(num)}")
# task 4
"""  Написати функцію, яка приймає рядок та повертає його у зворотному порядку.
"""
def revers_str(text):
    return text[::-1]
text_str='Hello World!'
print(f"Повертаємо рядок {text_str} у зворотньому порядку {revers_str(text_str)}")
# task 5
"""  Написати функцію, яка приймає список слів та повертає найдовше слово у списку.
"""
def list_word(word):
    if len(word)==0:
        return ""
    return max(word, key=len ) #Порівнюємо  елементи не напряму, а за значенням їхньої довжини.
words=["red", "green", "white", "yellow"]
print(f"Найдовше слово у списку слів {words} є {list_word(words)}")

# task 6
"""  Написати функцію, яка приймає два рядки та повертає індекс першого входження другого рядка
у перший рядок, якщо другий рядок є підрядком першого рядка, та -1, якщо другий рядок
не є підрядком першого рядка."""
def find_substring(str1, str2):

    return str1.find(str2)

str1 = "Hello, world!"
str2 = "world"
print(f"Перевіряємо чи входить {str2} в рядок {str1}. Виводимо позицію з якої {str2} в першому рядку. Ця позиція дорівнює =  {find_substring(str1, str2)}") # поверне 7

str1 = "The quick brown fox jumps over the lazy dog"
str2 = "cat"
print(f"{find_substring(str1, str2)}") # поверне -1

# task 7
def count_vowels(text):
    vowels = "аеиіїоуюя"
    count = 0
    for ch in text.lower():#  робимо усі літери маленькими, а цикл рахує лише ті символи, які є в рядку голосних
        if ch in vowels:
            count+=1
    return count
text  = input("Введіть текст: ")
print(f"Кількість голосних: {count_vowels(text)}")
# task 8
def without_word(fruits,key):
    res=[]
    for fruit in fruits:
        if fruit ==key:
            continue
        res.append(fruit)
    return res
fruits = ["apple", "banana", "orange", "grape", "mango"]
key="orange"
print(without_word(fruits,key))
# task 9
def even_squares(num):
    return[x**2 for x in num if x % 2 == 0]
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(even_squares(numbers))
# task 10
def check_password(password):
    special_char = "!@#%&_"
    errors = []

    have_digit = False
    have_upper = False
    have_special = False

    for ch in password:
        if ch.isdigit():
            have_digit = True
        if ch.isupper():
            have_upper = True
        if ch in special_char:
            have_special = True

    if len(password) < 8:
        errors.append("Пароль має містити не менше 8 символів!")
    if not have_digit:
        errors.append("Пароль має містити хоча б одну цифру!")
    if not have_upper:
        errors.append("Має бути хоча б одна велика літера!")
    if not have_special:
        errors.append("Має бути хоча б один спеціальний символ !@#%&_")

    return errors

password_correct = False
while not password_correct:
    password = input("Введіть пароль: ")
    errors = check_password(password)

    if not errors:
        password_correct = True
        print("Пароль прийнято!")
    else:
        for err in errors:
            print(err)
        print("Спробуйте ще раз!")
"""  Оберіть будь-які 4 таски з попередніх домашніх робіт та
перетворіть їх у 4 функції, що отримують значення та повертають результат.
Обов'язково документуйте функції та дайте зрозумілі імена змінним.
"""