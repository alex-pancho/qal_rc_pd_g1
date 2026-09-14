# Imperative approach
numbers = [1, 2, 3, 4, 5]
result = []
for n in numbers:
    if n % 2 == 0:
        result.append(n * n)
print(result)  # [4, 16]

# Functional programming
result = list(map(lambda n: n * n, filter(lambda n: n % 2 == 0, numbers)))
print(result)

sqare_func = lambda n: n * n
check_even = lambda n: n % 2 == 0

result = list(map(sqare_func, filter(check_even, numbers)))
print(result)

# Hybryd
result = [n * n for n in numbers if n % 2 == 0]
print(result)

discount = 0.1  # глобальна змінна

def calculate_price(price):
    return price * (1 - discount)

print(calculate_price(100))
discount = 0.2
print(calculate_price(100))


def calculate_price_cear(price, discount):
    return price * (1 - discount)

print(calculate_price_cear(100, 0.1))
print(calculate_price_cear(100, 0.1))

def add_tax_impure(prices):
    for i in range(len(prices)):
        prices[i] *= 1.2  # модифікуємо оригінал!
    return prices

original = [100, 200, 300]
result = add_tax_impure(original)
print(result)
print("print(original)", original)

def add_tax_pure(prices):
    return [price * 1.2 for price in prices]

result = add_tax_pure(original)
print(result)
print(original)

def square(x):
    return x ** 2

bi = 5

square_lambda = lambda x: x ** 2

print(square(bi))        # 25
print(square_lambda(bi)) # 25
print(bi)

def add(a, b):
    return a + b

add_lambda = lambda a, b: a + b

print(add(3, 4))        # 7
print(add_lambda(3, 4)) # 7

students = [
    {"name": "Олена", "grade": 92},
    {"name": "Богдан", "grade": 78},
    {"name": "Марина", "grade": 85},
]

# Сортування за оцінкою
sorted_students = sorted(students, key=lambda s: s["grade"], reverse=True)
for s in sorted_students:
    print(f"{s['name']}: {s['grade']}")

def srt(mydict):
    mylist = []
    for k, v in mydict:
        if k == "grade":
            mylist.append(v)
    return mylist

# Так не можна — lambda не підтримує if/else-блоки, цикли, return
# bad_lambda = lambda x: if x > 0: return x else: return -x  # SyntaxError

abs_value = lambda x: x if x >= 0 else -x


def absolute(x):
    if x >= 0:
        return x
    else:
        return -x

numbers = [1, -3, 5, -2, 8, -6, 4]

# Тільки додатні числа
positive = list(filter(lambda x: x > 0, numbers))
print(positive)

even = list(filter(lambda x: x % 2 == 0, positive))
print(even)

def is_adult(age):
    return age >= 18

ages = [12, 25, 16, 30, 17, 21]
adults = list(filter(is_adult, ages))
print(adults)

words = ["Python", "", "клас", "   ", "функція", "", "              "]

non_empty = list(filter(lambda w: w.strip(), words))
print(non_empty)

products = [
    {"name": "Ноутбук", "price": 35000, "in_stock": True},
    {"name": "Миша", "price": 500, "in_stock": False},
    {"name": "Клавіатура", "price": 1200, "in_stock": True},
    {"name": "Монітор", "price": 12000, "in_stock": False},
]

available = list(filter(lambda p: p["in_stock"], products))
for p in available:
    print(f"{p['name']}: {p['price']} грн")

affordable = list(filter(lambda p: p["price"] < 2000, products))
for p in affordable:
    print(p["name"])

numbers = range(1, 13)

# filter + lambda
squares_filter = list(filter(lambda x: x % 3 == 0, numbers))
squares_list_c = [x for x in numbers if x % 3 == 0]

print(squares_filter)  # [3, 6, 9]
print(squares_list_c)


numbers = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x ** 2, numbers))
print(squares)  # [1, 4, 9, 16, 25]

doubled = list(map(lambda x: x * 2, numbers))
print(doubled)
print(numbers)

raw_input = ["10", "25", "3", "17"]

numbers = list(map(int, raw_input))
print(numbers)

formatted = list(map(lambda p: f"{p} грн.", numbers))
print(formatted)

prices = [10, 20, 30]
quantities = [2, 5, 3]
tax = [1.1, 2.2, 3.3]
totals = list(map(lambda p, q, t: (p * q)/t, prices, quantities, tax))
print(totals)

names = ["  олена  ", "БОГДАН", "марина"]
normalized = list(map(lambda n: n.strip().capitalize(), names))
print(normalized) 

def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

temperatures_c = [0, 20, 37, 100]
temperatures_f = list(map(celsius_to_fahrenheit, temperatures_c))
print(temperatures_f)

transactions = [-500, 200, -100, 800, -50, 1000, 4500]

# Тільки доходи (позитивні), конвертовані у долари (курс 40 грн/$)

usd_incomes = list(map(
    lambda t: t / 45,
    filter(lambda t: t > 0, transactions)
))
print(usd_incomes)