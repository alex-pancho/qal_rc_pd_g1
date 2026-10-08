from typing import Union, Any


def square(number: int | float) -> int | float:  # noqa
    return number * number


def multiply(
    a: int | float,
    b: int | float,
) -> int | float:

    return a * b


def greet(name: str) -> str:
    return f"Hello {name}"


def is_adult(age: int) -> bool:
    return age >= 18


numbers: list[int] = [1, 2, 3]
names: list[str] = ["Alex", "Ben", "Cindy"]
userdata: list[dict[str, list[int]]] = [{"Alex": [1, 2], "Ben": [3, 4]}]

value: Union[int, str]

value2: Any


class User:

    def __init__(self, name: str, age: int):

        self.name = name
        self.age = age

    def get_name(self) -> str:
        return self.name


def calculate_total(prices: list[float]) -> float:

    return sum(prices)


# def get_name() -> str:
#     return 123

my_users: list[User] = []

if __name__ == "__main__":

    name: str = "Alex"
    age: int = 30
    price: float = 99.5
    is_active: bool = True

    print(square(10))
    print(multiply(2.05, 0.03))
    # print(square("10"))

"""
* flake8 # 4 
* pylint # 3
* ruff # 5
* black # 5
* mypy # 3,5-4
"""
