class Батьківський:
    pass

class Дочірній(Батьківський):
    pass

class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def speak(self) -> str:
        return f"{self.name} каже щось невизначене"

    def describe(self) -> str:
        return f"Мене звати {self.name}, мені {self.age} років"


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} каже: Гав!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} каже: Няв!"


dog = Dog("Рекс", 3)
cat = Cat("Мурчик", 5)

print(dog.describe())   # Мене звати Рекс, мені 3 років
print(dog.speak())      # Рекс каже: Гав!
print(cat.speak())      # Мурчик каже: Няв!

class OtherAnimal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class BigDog(OtherAnimal):
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)   # викликаємо __init__ батька
        self.breed = breed            # додаємо власний атрибут

    def describe(self) -> str:
        return f"{self.name} ({self.breed}), вік: {self.age}"


# class BigBigDog(OtherAnimal):
#     def __init__(self, breed: str):
#         super().__init__()   # викликаємо __init__ батька
#         self.breed = breed            # додаємо власний атрибут

#     def describe(self) -> str:
#         return f"{self.name} ({self.breed}), вік: {self.age}"


new_dog = BigDog("Рекс", 3, "Лабрадор")
print(new_dog.describe())

# new_new_dog = BigBigDog("Лабрадор")
# print(new_new_dog.describe())

print(isinstance(new_dog, BigDog))
print(isinstance(new_dog, OtherAnimal))
print(type(new_dog) == BigDog)
print(type(new_dog) == OtherAnimal)

class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower
        self.is_on = False

    def __str__(self):
        staus = "запущено" if self.is_on else "зупинено"
        return f"Двигун {self.horsepower} к.с. {staus}"

    def start(self) -> str:
        self.is_on = True
        return str(self)

    def stop(self) -> str:
        self.is_on = False
        return str(self)


class Car:
    def __init__(self, brand: str, horsepower: int):
        self.brand = brand
        self.engine = Engine(horsepower)  # композиція

    def drive(self) -> str:
        engine_status = self.engine.start()
        return f"{self.brand}: {engine_status}"

car = Car("Toyota", 150)
print(car.drive())
print(car.engine.stop())
print(car.engine)

class Flyable:
    def fly(self) -> str:
        return f"{self.__class__.__name__} летить"


class Swimmable:
    def swim(self) -> str:
        return f"{self.__class__.__name__} пливе"


class Duck(Flyable, Swimmable):
    def quack(self) -> str:
        return "Кря!"

duck = Duck()
print(duck.fly())
print(duck.swim())
print(duck.quack())

class A:
    def hello(self):
        return "Привіт від A"

class B(A):
    def hello(self):
        return "Привіт від B"

class C(A):
    def hello(self):
        return "Привіт від C"

class D(B, C):
    pass

d = D()
print(d.hello())
print(D.__mro__)


class AA:
    def hello(self):
        return "AA"

class BA(AA):
    def hello(self):
        return "BA -> " + super().hello()

class CA(AA):
    def hello(self):
        return "CA -> " + super().hello()

class DA(BA, CA):
    def hello(self):
        return "DA -> " + super().hello()

print(DA().hello())

class Shape:
    def area(self) -> float:
        raise NotImplementedError("Підклас має реалізувати area()")

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.141595 * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height

shapes: list[Shape] = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 8),
]

for shape in shapes:
    print(f"{shape.__class__.__name__}: площа = {shape.area():.2f}")

class RoboDog:
    def speak(self) -> str:
        return "Гав!"

class RoboCat:
    def speak(self) -> str:
        return "Няв!"

class Robot:
    def speak(self) -> str:
        return "Біп-буп!"


def make_noise(entity) -> None:  # не вимагає конкретного типу
    print(entity.speak())

for creature in [RoboDog(), RoboCat(), Robot()]:
    make_noise(creature)

class MathHelper:

    def __init__(self, a, b, x):
        pass

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def is_even(n: int) -> bool:
        return n % 2 == 0

print(MathHelper.add(3, 5))
print(MathHelper.is_even(4))

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, data: str) -> Person:
        """Альтернативний конструктор: 'Іван:30' → Person"""
        name, age = data.split(":")
        return cls(name, int(age))

    @classmethod
    def from_birth_year(cls, name: str, birth_year: int) -> Person:
        """Альтернативний конструктор через рік народження"""
        from datetime import datetime
        age = datetime.now().year - birth_year
        return cls(name, age)

    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age})"


p1 = Person("Іван", 30)
p2 = Person.from_string("Марія:25")
p3 = Person.from_birth_year("Олег", 1995)

print(p1)
print(p2)
print(p3)
