# a = 1
# b = 2
# c = a + b
# print(c)

def ledar():
    pass

print(ledar())

def print_song():
    """Друкує пісню"""
    print("Ой у лузі червона калина похилилася")
    print("Чогось наша славна Україна зажурилася")

print_song()

def hello(name):
    """
    Повертає привітання str
    """
    return f"{name} hello!"

output = hello("Nikita")
print(output)

output = hello(1)
print(output)

output = hello((1, 2))
print(output)


def describe_pet(animal_type, pet_name) -> str:
    """Display information about a pet."""
    return f"My {animal_type}'s name is {pet_name.title()}."

print(describe_pet("dog", "rex"))
print(describe_pet("tom", "cat"))

def greet(name: str, greeting: str = "Привіт"):
    """
    Функція виводить привітання для заданого імені.

    :param name: Ім'я для привітання
    :param greeting: Привітання (за замовчуванням "Привіт")
    """
    print(f"{greeting}, {name}!")
    #print(greeting + ", " +  name + "!")

greet("Ільміра")
greet("Максим", "Доброго дня")
print(greet(""))


greet(greeting = "Hello", name = "Genna")
# позиційні - у порядку заданому у коді
# іменовані - ім'я = значення, 

def print_args(*args):
    for arg in args:
        print(arg)
print_args(1, "hello", None)
print("=============")
print_args(1, "hello", 3.14, [1, 2, 3])
# nik_tuple = (1, "hello", 3.14, [1, 2, 3])
# print_args(*nik_tuple)


def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Приклад виклику функції
print_kwargs(name="John", age=25, city="New York")
print("=============")

def print_args_and_kwargs(*args, **kwargs):
    for arg in args:
        print(arg)
    
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Приклад виклику функції
print_args_and_kwargs(1, "hello", 3.14, name="John", age=25)


def minus(a, b):
    return a - b

print(minus(2, 5))
print(minus(5, 2))

print_args_and_kwargs(name="Irina", age=18)

def describe_person(name, age, country="Unknown"):
    print(f"{name} is {age} years old and is from {country}.")

describe_person("Alice", 30)
describe_person("Bob", 25, "USA")

describe_person("Charlie", country="Canada", age=28)

# def plus(a, b):
#     return a + b

plus = lambda a, b: a + b
print(plus(1, 2))

square = lambda x: x**2

print(square(5))

print(all([1, 2, -4]))
print(all([1, 2, 0]))

print(any([1,2,3]))
print(any([0,2,0]))
print(any([0,0,0]))

byte_array = bytearray(b'Hello, World!')
byte_array[0] = 37  # bytearray змінний, тож 0 елемент
                    # змінюється на символ з кодом 37 == %
print(byte_array.decode('utf-8'))   # %ello, World!

print(chr(1111), chr(44))

my_dict = dict(a="a", b=[1,2])
print(my_dict)


def is_even(n):
    return n % 2 == 0

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

filtered_numbers = filter(is_even, numbers)
even_numbers = list(filtered_numbers)
print(even_numbers)


value1 = "abc"
value2 = "DER"
formatted_string = "Some text {} and {}.".format(value1, value2)
print(formatted_string)

hello_my = "hello"  
print(id(hello_my))
hello_my = "ferer"
print(id(hello_my))

list_1 = []
print(id(list_1))
list_1.append(1)
print(id(list_1))

print(int("73") == 73)


x = 5
print(isinstance(x, int))
print(isinstance(x, str))
print(len("len"))

print(max([3, 1, 4]))
print(min([3, 1, 4]))

print(pow(3, 3))
print(3**3)

print(list(reversed([10, 2, 4])))

print(round(2.60))
print(round(2.40))

print(sorted((2, 4, 2, 3, 7)))
print(str(123))


print(sum([1, 2, 3]))

print(type("hello"))
