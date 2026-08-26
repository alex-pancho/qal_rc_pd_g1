#import math

class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value: int|float):
        if value < 0:
            print("Баланс цього рахунку не може бути відємним")
            return
        self.__balance = value


account = BankAccount("Іван", 1000)
# account.__balance = -99999  # ніхто не зупинить!
print(account.balance)

account.balance = 50
print(account.balance)
# _ClassName__name
print(account._BankAccount__balance) ##

class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Геттер: читаємо значення"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Сеттер: валідація при записі"""
        if value < -273.15:
            raise ValueError(f"Температура {value}°C нижча за абсолютний нуль")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Обчислювана властивість (лише читання)"""
        return self._celsius * 9 / 5 + 32


t = Temperature(100)
print(t.celsius)
print(t.fahrenheit)

t.celsius = 0
print(t.fahrenheit)

# t.celsius = -300

class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Радіус має бути позитивним")
        self._radius = value

    @property
    def area(self) -> float:
        return 3.1415 * self._radius ** 2   # read-only: немає setter

    @property
    def diameter(self) -> float:
        return self._radius * 2 

print("Circle")
c = Circle(5)
print(c.area)
print(c.diameter)
# c.diameter = 25
c.radius = 10
print(c.area)


class Employee:
    MIN_SALARY = 7000   # мінімальна зарплата (грн)

    def __init__(self, name: str, salary: float, age: int):
        self.name = name        # публічний (не потребує валідації)
        self.salary = salary    # через setter
        self.age = age          # через setter

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Зарплата має бути числом")
        if value < self.MIN_SALARY:
            raise ValueError(f"Зарплата не може бути меншою за {self.MIN_SALARY} грн")
        self._salary = float(value)

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Вік має бути цілим числом")
        if not (18 <= value <= 65):
            raise ValueError("Вік працівника має бути від 18 до 65 років")
        self._age = value

    def __repr__(self) -> str:
        return f"Employee(name='{self.name}', salary={self._salary}, age={self._age})"

emp = Employee("Олена", 15000, 30)
print(emp)
emp.salary = 20000
print(emp)
# emp.MIN_SALARY = 1
# emp.salary = 5000
# print(emp)

class PasswordManager:
    def __init__(self, password: str):
        self.__password_hash = self.__hash(password)

    def __hash(self, password: str) -> int:
        """Приватний метод — внутрішня деталь реалізації"""
        return hash("new secret " + password + "salt_secret")

    def check_password(self, password: str) -> bool:
        """Публічний метод — єдиний спосіб взаємодії ззовні"""
        return self.__hash(password) == self.__password_hash

    def change_password(self, old_password: str, new_password: str) -> None:
        if not self.check_password(old_password):
            raise PermissionError("Невірний поточний пароль")
        if len(new_password) < 8:
            raise ValueError("Новий пароль занадто короткий")
        self.__password_hash = self.__hash(new_password)
        print("Пароль успішно змінено")

pm = PasswordManager("secret123")
print(pm.check_password("secret123"))
print(pm.check_password("secret!23"))
#print(pm._PasswordManager__password_hash)
pm.change_password("secret123", "newpass456")
print(pm.check_password("secret123"))