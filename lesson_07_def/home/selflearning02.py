# -*- coding: utf-8 -*-
"""
Завдання для самостійного вивчення: Функції в Python
===================================================

Це файл з завданнями для закріплення матеріалу про функції в Python.
Виконайте всі завдання послідовно. Перевірити правильність можна запустивши test_selflearning.py

Теми:
- Створення функцій
- Аргументи функцій
- *args і **kwargs
- Позиційні та ключові параметри
- Лямбда-функції
- Вбудовані функції (map, zip, isinstance, type, sort, sorted)
"""

# =============================================================================
# ЗАВДАННЯ 1: Основи створення функцій
# =============================================================================

def greeting(name):
    """
    Завдання 1.1: Створіть функцію, яка приймає ім'я та повертає привітання
    
    Args:
        name (str): Ім'я для привітання
        
    Returns:
        str: Рядок привітання у форматі "Привіт, {name}!"
    """
    return f"Привіт, {name}!"
print(greeting("Олено"))

def calculate_area(length, width):
    """
    Завдання 1.2: Функція для обчислення площі прямокутника
    
    Args:
        length (float): Довжина прямокутника
        width (float): Ширина прямокутника
        
    Returns:
        float: Площа прямокутника
    """
    return f"Площа прямокутника з  довжиною {length} і шириною {width} дорівнює {length*width}"
print(calculate_area(20, 40))

def is_even(number):
    """
    Завдання 1.3: Перевірка чи число парне
    
    Args:
        number (int): Число для перевірки
        
    Returns:
        bool: True якщо число парне, False якщо непарне
    """    
    return number % 2 == 0
if (is_even(5) == True):
    print("Число парне!")
else: print("Число непарне!")

# =============================================================================
# ЗАВДАННЯ 2: Функції з позиційними та ключовими аргументами
# =============================================================================

def create_profile(name, age, city="Не вказано", profession="Не вказано"):
    """
    Завдання 2.1: Створення профілю користувача
    
    Args:
        name (str): Ім'я користувача
        age (int): Вік користувача
        city (str, optional): Місто. За замовчуванням "Не вказано"
        profession (str, optional): Професія. За замовчуванням "Не вказано"
        
    Returns:
        dict: Словник з інформацією про користувача
    """
    return {
        "name": name,
        "age": age,
        "city": city,
        "profession": profession
        }
profile_user = create_profile("Олена" , 25, "Кривий Ріг", "Програміст" )
print(profile_user)

def calculate_price(base_price, discount=0, tax=0.2):
    """
    Завдання 2.2: Розрахунок фінальної ціни з урахуванням знижки та податку
    
    Args:
        base_price (float): Базова ціна
        discount (float, optional): Знижка (від 0 до 1). За замовчуванням 0
        tax (float, optional): Податок (від 0 до 1). За замовчуванням 0.2
        
    Returns:
        float: Фінальна ціна після знижки та податку
    """
    return (base_price * (1 - discount)) * (1 + tax) # використовувати цю формулу для return (base_price * (1 - discount)) * (1 + tax) 
price = calculate_price(1000, discount = 0.1)
print(f"Фінальна ціна після знижки {price}")


# =============================================================================
# ЗАВДАННЯ 3: *args і **kwargs
# =============================================================================

def sum_all(*args):
    """
    Завдання 3.1: Функція для додавання будь-якої кількості чисел
    
    Args:
        *args: Будь-яка кількість чисел
        
    Returns:
        int/float: Сума всіх переданих чисел
    """
    return sum(args) # Поверніть суму всіх переданих аргументів
print(f"Сума всіх чисел дорівнює {sum_all(1,2,3,4,5,6,7,8,9,10)}")


def create_student(**kwargs):
    """
    Завдання 3.2: Створення студента з довільними параметрами
    
    Args:
        **kwargs: Довільні параметри студента
        
    Returns:
        dict: Словник з обов'язковими ключами name, age та всіма переданими параметрами
    """ # Якщо name або age не передані, встановіть їх за замовчуванням
    kwargs.setdefault("name", "Не вказано")
    kwargs.setdefault("age", "Не вказано")
    # Поверніть словник з переданими параметрами
    return kwargs
student = create_student(name = "Irina", age = 22, city = "Крививй Ріг")
print(student)
student = create_student(city="Kyiv")
print(student)


def flexible_function(*args, **kwargs):
    """
    Завдання 3.3: Функція, яка приймає і позиційні, і ключові аргументи
    
    Args:
        *args: Позиційні аргументи
        **kwargs: Ключові аргументи
        
    Returns:
        tuple: Кортеж з двох елементів: (список args, словник kwargs)
    """
    return list(args), kwargs # Поверніть кортеж (list(args), kwargs). 
                              #*args збирає позиційні аргументи в кортеж. 
                              # list(args) перетворює цей кортеж у список. 
                              # **kwargs збирає іменовані аргументи в словник.
result = flexible_function("Banane", "Apple", "Apricot" , name="Fruit" , pakuvanya = "Box")
print(result)

# =============================================================================
# ЗАВДАННЯ 4: Лямбда-функції
# =============================================================================

# Завдання 4.1: Створіть лямбда-функцію для піднесення числа до квадрату
square = lambda num: num**2  #  Замініть None на лямбда-функцію
print(square(7))
# Завдання 4.2: Лямбда-функція для перевірки чи число більше 10
is_greater_than_10 = lambda num: num>10  # TODO: Замініть None на лямбда-функцію
if is_greater_than_10(12) == True:
    print("Число більше 10")
else: print("Число менше або дорівнює 10")

# Завдання 4.3: Лямбда-функція для об'єднання двох рядків
concatenate = lambda str1, str2: str1 + str2  #  Замініть None на лямбда-функцію
print(concatenate("Hello ", "world!"))

# =============================================================================
# ЗАВДАННЯ 5: Робота з вбудованими функціями
# =============================================================================


def check_type_vs_isinstance(value, check_type):
    """
    Завдання 5.1: Порівняння type() та isinstance() 

    type(value) == check_type перевіряє точний тип об’єкта.
    isinstance(value, check_type) перевіряє, чи є значення екземпляром типу або його підкласу.
    
    Args:
        value: Значення для перевірки
        check_type: Тип для перевірки
        
    Returns:
        tuple: (результат type(), результат isinstance())
    """
    return  type(value) == check_type, isinstance(value, check_type) # Поверніть кортеж з результатами type(value) == check_type та isinstance(value, check_type)
print(check_type_vs_isinstance(99.0, float))


def sort_vs_sorted_demo(numbers):
    """
    Завдання 5.2: Різниця між sort() та sorted()

    sort() змінює сам список,
    sorted() створює новий відсортований список, а оригінал не змінює.

    Args:
        numbers (list): Список чисел
        
    Returns:
        tuple: (оригінальний список після sort(), новий відсортований список)
    """
    original_list_numbers = numbers.copy()
    original_list_numbers.sort()
    return f" Оригіналний список {numbers}. Список відсортований sort {original_list_numbers}. Список відсортований sorted  {sorted(numbers)}" # Застосуйте sort() до оригінального списку і поверніть його разом з sorted()

print(sort_vs_sorted_demo([9, 5, 4, 8, 2, 12, 1]))


# =============================================================================
# ЗАВДАННЯ 6: Складніші завдання
# =============================================================================

def filter_and_process(data, filter_func, process_func):
    """
    Завдання 6.1: Фільтрація та обробка даних
    
    Args:
        data (list): Список даних
        filter_func (function): Функція для фільтрації
        process_func (function): Функція для обробки
        
    Returns:
        list: Список оброблених елементів, які пройшли фільтрацію
    """
    new_list = []# Відфільтруйте дані та обробіть їх
    for i in data:
        if filter_func(i):
            new_list.append(process_func(i))
    return new_list
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filter_func = lambda a: a % 2 != 0
process_func = lambda a: a**3
print(f" Беремо список  {data}, перевіряємо, якщо елемент непарний, підносимо його до кубу {filter_and_process(data, filter_func, process_func)}")


def create_multiplier(factor):
    """
    Завдання 6.2: Функція, яка повертає функцію (замикання)
    
    Args:
        factor (int/float): Множник
        
    Returns:
        function: Функція, яка множить переданий аргумент на factor
    """
    def multiplier(number):
        return number * factor #  Поверніть функцію, яка множить аргумент на factor  
    return multiplier

zminna_create = create_multiplier(100)
print(f"множимо аргумент на factor  {zminna_create(2)}")

def advanced_calculator(*args, operation="sum", **kwargs):
    """
    Завдання 6.3: Розширений калькулятор
    
    Args:
        *args: Числа для обчислення
        operation (str): Операція ("sum", "multiply", "max", "min")
        **kwargs: Додаткові параметри
        
    Returns:
        float/int: Результат обчислення
    """
    #  Реалізуйте калькулятор з різними операціями
    if not args:
        return 0
    if operation == "sum":
        return sum(args)
    elif operation == "multiply":
        mul = 1
        for i in args:
            mul = mul*i
        return mul
    elif operation == "max":
        return  max(args)
    elif operation == "min":
        return min(args)
    else:
        return None
args1=[1,2,3,4,5]
operation_calc="multiply"
print(f" Знайдемо {operation_calc} зі списку {args1}. {operation_calc} = {advanced_calculator(*args1,operation = operation_calc)}")
  



# =============================================================================
# ПРИКЛАДИ ВИКОРИСТАННЯ (для розуміння)
# =============================================================================

if __name__ == "__main__":
    # Приклади використання функцій
    print("=== Приклади використання ===")
    
    # Після реалізації функцій, розкоментуйте код нижче:
    
    # print(greeting("Олексій"))
    # print(calculate_area(5, 3))
    # print(is_even(4))
    
    # profile = create_profile("Марія", 25, city="Київ")
    # print(profile)
    
    # print(sum_all(1, 2, 3, 4, 5))

    
    print("Реалізуйте всі функції та перевірте їх за допомогою test_selflearning.py")