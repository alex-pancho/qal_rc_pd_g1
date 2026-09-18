from dataclasses import dataclass
from functools import reduce

# class Student:

#     def __init__(self, name, age, score):
#         self.name = name
#         self.age = age
#         self.score = score
"""
* `__init__()`
* `__repr__()`
* `__eq__()`
"""

@dataclass
class Student:
    name: str
    age: int = 25
    score: float = 0

@dataclass
class User:
    name: str
    active: bool = True


@dataclass
class Employee:
    name: str
    salary: int

    def __post_init__(self):
        if self.salary < 0:
            raise ValueError("Salary cannot be negative")


student = Student("Alex", 25, 95.5)

print(student)
print(student.age)
print(student.name)
print(student.score)

student2 = Student(name='Alex', age=25, score=95.5)

print(student2 == student)

user = User("John")

print(user)

employee = Employee("Bob", 1000)
print(employee)
try:
    employee2 = Employee("John", -1)
    print(employee2)
except ValueError as e:
    print(e)

@dataclass
class Product:
    id: int
    name: str
    price: float

# products = [
#     Product(1, "Laptop", 1200),
#     Product(2, "Mouse", 25),
#     Product(3, "Keyboard", 50)
# ]
# print(products)

# products = [
#     Product(*data)
#     for data in [
#         (1, "Laptop", 1200),
#         (2, "Mouse", 25),
#         (3, "Keyboard", 50)
#     ]
# ]


products = list(map(
    lambda data: Product(*data),
    [
        (1, "Laptop", 1200),
        (2, "Mouse", 25),
        (3, "Keyboard", 50)
    ]
    )
)
print(products)

def is_prime(number):

    if number < 2:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True

numbers = range(1, 51)

primes = list(filter(is_prime, numbers))

print(primes)

numbers = range(1, 51)

primes = list(
    filter(
        lambda n: n > 1 and all(
            n % d != 0
            for d in range(2, int(n ** 0.5) + 1)
        ),
        numbers
    )
)

print(primes)

def is_palindrome(word):
    return word == word[::-1]

words = [
    "radar",
    "python",
    "anna",
    "car",
    "level",
    "hello"
]

result = list(filter(is_palindrome, words))

print(result)

numbers = [10, 12, 13, 11, 15, 14, 300]

average = sum(numbers) / len(numbers)

filtered = list(
    filter(
        lambda x: x < average * 2,
        numbers
    )
)

print(filtered)

temperatures = [
    16, 12, 32, 44,
    22, 23, 21, 24,
    25, 23, 22, 120,
    57, 33, 47, 250
]

clean_data = list(
    filter(
        lambda t: 18 <= t <= 45,
        temperatures
    )
)

print(clean_data)

ids = [
    "12345",
    "ABC12",
    "99999",
    "TEST",
    "54321"
]

valid_ids = list(
    filter(
        lambda x: x.isdigit(),
        ids
    )
)

print(valid_ids)

ids = [
    "12345",
    "123",
    "ABCDE",
    "99999"
]

valid_ids = list(
    filter(
        lambda x: x.isdigit() and len(x) >= 5,
        ids
    )
)

print(">", valid_ids)

result = list(
    map(
        lambda x: int(x),
        valid_ids
    )
)

print(result)

numbers = [1, 2, 3, 4]

result = reduce(
    lambda acc, x: acc + [x * 2],
    numbers,
    []
)

print(result)

students3 = [
    Student(name=n, score=s)
    for n, s in [
        ("Alex", 90),
        ("John", 75),
        ("Kate", 95),
        ("Bob", 60)
    ]
]

print(students3)

scores = list(
    map(
        lambda student: student.score,
        students3
    )
)

print(scores)

best_students = list(
    filter(
        lambda student: student.score > 80,
        students3
    )
)
print(best_students)