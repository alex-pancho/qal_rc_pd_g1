# Вправа 1: Проста математика
print("\n=== ВПРАВА 1: Калькулятор ===")
print("Створіть простий калькулятор для двох чисел і двох дій")
print("Підтримувані операції: +, -")

# Початок реалізації:
num1 = float(input("Введіть перше число: "))
operation = input("Введіть операцію (+, -): ")
num2 = float(input("Введіть друге число: "))

if operation == "+":
    print(f"Сума чисел {num1} і {num2} дорівнює {num1+num2}")
elif operation == "-":
    print(f"Різниця чисел {num1} і {num2} дорівнює {num1-num2}")
else: 
    print(" Некоректні вхідні дані!")

# Вправа 2: Перевірка паролю
print("\n=== ВПРАВА 2: Перевірка паролю ===")
print("Створіть систему перевірки паролю")
print("Пароль повинен містити принаймні 8 символів")

special_char="!@#%&_"
password_correct = False
while not password_correct:
    password=input("Введіть пароль: ")

    have_cyfra = False
    have_upper_litera =False
    have_spec_symvol =False

    for ch in password:
        if ch.isdigit():
            have_cyfra = True
        if ch.isupper():
            have_upper_litera = True
        if ch in special_char:
            have_spec_symvol= True

    errors = []
    
    if len(password) < 8:
        errors.append("Пароль має містити не менше 8 символів!!!")
    elif not have_cyfra:
        errors.append("Пароль має містити хоча б одну цифру!")
    elif not have_upper_litera:
        errors.append("Має бути хоча б одна велика літера!")
    elif not have_spec_symvol:
        errors.append("Має б56ути хоча б одни спеціальний символ !@#%&_")
    if not errors:
        password_correct = True
        break
    else:
        for err in errors:
            print(f"{err}")
        print(" Спробуйте ще раз!!!")

# Вправа 3: Визначення високосного року
print("\n=== ВПРАВА 3: Високосний рік ===")
print("Рік є високосним, якщо:")
print("- Ділиться на 4 І не ділиться на 100")
print("- АБО ділиться на 400")
year= int(input(" Введіть рік: "))
if (year % 4 ==0 and year % 100 !=0) or year % 400 ==0:
    print(f"{year} є високосним роком!!!")
else:
    print(f"{year} є не високосним роком!!!")



# Вправа 4: Лічильник голосних
print("\n=== ВПРАВА 4: Лічильник голосних ===")
print("Підрахуйте кількість голосних у рядку")

text = input("Введіть текст: ").lower()
vowels = "аеиіїоуюя"
count = 0

# код тут
for ch in text:
    if ch in vowels:
        count+=1

print(f"Кількість голосних: {count}")


# Вправа 5: Гра 
print("\n=== ВПРАВА 5: Гра ===")
"""
Уявіть, що інопланетянина з кольором alien_color щойно збили в грі.
Створіть змінну під назвою alien_color і призначте їй значення 'green', 'yellow', або 'red'.
Напишіть оператор if, щоб перевірити, чи колір прибульця 'green'.
Якщо колір прибульця green, надрукуйте, що гравець щойно заробив 5 балів.
Якщо колір прибульця yellow, надрукуйте, що гравець щойно заробив 10 балів.
Якщо колір прибульця red - надрукуйте, що гравець щойно заробив 15 балів.
Перевірте роботу гри самостійно, змінюючи значення alien_color
"""
correct_color = ["green", "yellow", "red"]
alien_color = ""

while True:
    alien_color= input("Ведіть колір прибульця (green/yellow/red): ").lower().strip()
    if alien_color not in correct_color:
        print(" Некоректні значення кольору прибульця!!!")
        print(" Повторіть введення правильного значення (green, yrllow, red)")
    else:
        break


if alien_color == "green":
    print("гравець щойно заробив 5 балів")
elif alien_color == "yellow":
    print("гравець щойно заробив 10 балів")
elif alien_color == "red":
    print("гравець щойно заробив 15 балів")


# Вправа 6: Піцерія *
print("\n=== ВПРАВА 6: Начинки для піци (pizza_topping) ===")
"""  Начинки для піци (pizza_topping): напишіть цикл, який пропонує користувачеві ввести ряд начинок
для піци, доки він не введе значення 'quit'. Коли вони введуть кожну начинку,
надрукуйте повідомлення про те, що ви додасте цю начинку до їхньої піци.
"""
topping = []
while True:
    pizza_topping = input("Введіть начинку для піци або quit для завершення замовлення!").strip()

    if pizza_topping.lower() == "quit":
        print("Замовлення прийнято!")
        break
    print(f" Готова піца буде містити:{pizza_topping}")
    topping.append(pizza_topping)
print("\n Готова піца складатеметься з:")
for i in topping:
    print(i)

# Вправа 7: Зворотний порядок цифр
print("\n=== ВПРАВА 7: Зворотний порядок ===")
print("Виведіть цифри числа у зворотному порядку")
number = input(" Ведіть число: ")
revers_number = number[::-1]
print("Цифри у зворотньому порядку: ", revers_number)

# Вправа 8: Пошук максимального числа
print("\n=== ВПРАВА 8: Пошук максимального ===")
print("Знайдіть найбільше число серед введених")
print("Введіть 0 для завершення")

numberss=[]
while True:
   num = int (input("Введіть число: ")) 
   if num == 0:
       break
   numberss.append(num)

if not numberss:
    print("Ви не ввели жодного числа!")
else:
    print(f"Найбільше число серед введених {max(numberss)}")

# Вправа 9: Виключення зі списку
print("\n=== ВПРАВА 9: Виключення зі списку ===")
"""  Задача з використанням циклу for та continue. Задано список фруктів 'fruits'
потрібно вивести на екран всі елементи списку, окрім "orange".
"""
fruits = ["apple", "banana", "orange", "grape", "mango"]
for fruit in fruits:
    if fruit == "orange":
        continue
    print(fruit)

# Вправа 10: Вираз в один рядок
print("\n=== ВПРАВА 10: Вираз з умовою в один рядок ===")
"""  Задано список чисел numbers, потрібно знайти список квадратів
парних чисел зі списку. Спробуйте використати if та цикл for в один рядок.
"""
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = [x**2 for x in numbers if x % 2 == 0 ]
print(result)  #  [4, 16, 36, 64, 100]