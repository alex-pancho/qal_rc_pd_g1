def greet(name: str) -> str:
    return f"Привіт, {name}!"

# var = greet("alex")
# print(var)

say_hello = greet
print(type(say_hello))
print(say_hello("Олена"))

def apply(func, value):
    return func(value)

result = apply(greet, "Максим")
print(result)

def outer():
    print("Зовнішня функція")

    def inner():
        print("Внутрішня функція")

    inner()  # Виклик зсередини зовнішньої

outer()
# inner()

def make_greeting(greeting: str):
    def greet(name: str) -> str:
        return f"{greeting}, {name}!"  # greeting — захоплена змінна
    return greet

hello = make_greeting("Привіт")
hi = make_greeting("Вітаю")

print(hello("Соломія"))
print(hi("Богдан"))

print(hello.__closure__)               # (<cell at 0x...>,)
print(hello.__closure__[0].cell_contents)  # Привіт

functions = [] # 0, 1, 2
for i in range(4):
    def f():
        return i  # Захоплює посилання на i, а не поточне значення
    functions.append(f)

print(functions[0]())
print(functions[1]())
print(functions[2]())

def make_multiplier(factor: int):
    def multiply(number: float) -> float:
        return number * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10.0
print(triple(5))   # 15.0
print(double(7))
print(triple(7))

def make_validator(min_val: float, max_val: float):
    def validate(value: float) -> bool:
        return min_val <= value <= max_val
    return validate

is_valid_age = make_validator(0, 150)
is_valid_grade = make_validator(0, 100)

print("0", is_valid_age(0))
print("150", is_valid_age(150))
print("151", is_valid_age(151))
print("")
print("g 2", is_valid_grade(2))
print("g 85", is_valid_grade(85))
print("g 20085", is_valid_grade(20085))
"10.09.26 19:59"
"9/10/26 7:59PM"
