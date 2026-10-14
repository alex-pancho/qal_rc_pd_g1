# task 1
""" Задача - надрукувати табличку множення на задане число, але
лише до максимального значення для добутку - 25.
Код майже готовий, треба знайти помилки та випраавити\доповнити.
"""
from pydoc import text


def multiplication_table(number):
    # Initialize the appropriate variable
    multiplier = 1

    # Complete the while loop condition.
    while True:
        result = number * multiplier
        # десь тут помилка, а може не одна
        if  result > 25:
            # Enter the action to take if the result is greater than 25
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
def sum_numbers(a, b):
    return a + b
result = sum_numbers(8, 6)
print(result)  # Should print 8

# task 3
"""  Написати функцію, яка розрахує середнє арифметичне списку чисел.
"""
def average(numbers):
    return sum(numbers) / len(numbers)
result = average([8, 6, 10, 12])
print(result)  # Should print 9.0

# task 4
"""  Написати функцію, яка приймає рядок та повертає його у зворотному порядку.
"""
def reverse_string(text):
    return text[::-1]
result = reverse_string("Hello, world!")
print(result)  # Should print !dlrow ,olleH

# task 5
"""  Написати функцію, яка приймає список слів та повертає найдовше слово у списку.
"""
def longest_word(words):
    return max(words, key=len)
words = ["кіт", "собака", "слон", "черепаха", "жираф", "крокодил"]

print(longest_word(words))

# task 6
"""  Написати функцію, яка приймає два рядки та повертає індекс першого входження другого рядка
у перший рядок, якщо другий рядок є підрядком першого рядка, та -1, якщо другий рядок
не є підрядком першого рядка."""
def find_substring(str1, str2): 
    return str1.find(str2)

    #return -1

str1 = "Hello, world!"
str2 = "world"
print(find_substring(str1, str2)) # поверне 7

str1 = "The quick brown fox jumps over the lazy dog"
str2 = "cat"
print(find_substring(str1, str2)) # поверне -1

# task 7
# task 8
# task 9
# task 10
"""  Оберіть будь-які 4 таски з попередніх домашніх робіт та
перетворіть їх у 4 функції, що отримують значення та повертають результат.
Обов'язково документуйте функції та дайте зрозумілі імена змінним.
"""
# task 04
""" Виведіть, скількі разів у тексті зустрічається літера "h"
"""
adwentures_of_tom_sawer = """\
Tom gave up the brush with reluctance in his .... face but alacrity
in his heart. And while 
the late steamer
"Big Missouri" worked ....
and sweated
in the sun,
the retired artist sat on a barrel in the .... shade close by, dangled his legs,
munched his apple, and planned the slaughter of more innocents.
There was no lack of material;
boys happened along every little while;
they came to jeer, but .... remained to whitewash. ....
By the time Ben was fagged out, Tom had traded the next chance to Billy Fisher for
a kite, in good repair;
and when he played
out, Johnny Miller bought
in for a dead rat and a string to swing it with—and so on, and so on,
hour after hour.  """

def count_letter_h(adwentures_of_tom_sawer ):
    return adwentures_of_tom_sawer.count("h")
result = count_letter_h(adwentures_of_tom_sawer)
print(result)



# task 05
""" Виведіть, скільки слів у тексті починається з Великої літери?
"""
def count_capital_words(adwentures_of_tom_sawer ):
    capital_count = 0
    for word in adwentures_of_tom_sawer.split():
        if word[0].isupper():
            capital_count += 1
    return capital_count

# task 06
""" Виведіть позицію, на якій слово Tom зустрічається вдруге
"""
def find_second_tom(text):
    first_position = text.find("Tom")
    second_position = text.find("Tom", first_position + 1)
    return second_position
result = find_second_tom(adwentures_of_tom_sawer)
print(result)



# task 07
""" Розділіть змінну adwentures_of_tom_sawer по кінцю речення.
Збережіть результат у змінній adwentures_of_tom_sawer_sentences
"""
def split_into_sentences(text):
    return text.split(".")
adwentures_of_tom_sawer_sentences = split_into_sentences(adwentures_of_tom_sawer)
result = adwentures_of_tom_sawer_sentences
print(result)


# task 08
""" Виведіть четверте речення з adwentures_of_tom_sawer_sentences.
Перетворіть рядок у нижній регістр.
"""
print(adwentures_of_tom_sawer_sentences[3].lower())
