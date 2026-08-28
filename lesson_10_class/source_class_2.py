
# наслідування
class Animal:

    def __init__(self):
        self.legs = 4

    def breathing(self):
        print("this animal has breathing")

    def speak(self):
        pass


class Dog(Animal):
    # поліморфізм 
    def speak(self):
        return "Wof!"

    def seek(self):
        return "I'm looking for a toy"



class Cat(Animal):
    # поліморфізм
    def speak(self):
        return "Meew!"

    def sleep(self):
        return "I'm sleeping now"

class Koza(Animal):

    def __init__(self):
        super().__init__()
        self.legs = 2

    # поліморфізм
    def speak(self):
        return "Meee"

patron = Dog()
murzik = Cat()
bilka = Koza()

print(patron.seek())
print(murzik.sleep())
patron.breathing()
murzik.breathing()

print(bilka.legs)
zhaba = Animal()
print(zhaba.speak())


class BankAccount:

    def __init__(self, initial_balance):
        self.__balance = initial_balance
    
    def __str__(self):
        return f"Available: {self.__balance} USD"
    
    def get_balance(self):
        return self.__balance

    def set_balance(self, value):
        if isinstance(value, (int, float)):
            self.__balance = value

account = BankAccount(1000)
print(account)
print(account.get_balance())
print(account.set_balance(1))
print(account)

alex = BankAccount(10)
nata = BankAccount(25)
print(alex.get_balance() > nata.get_balance())

a_name = "John"
a_age = 25
print(f"{a_name} is {a_age} years old.")

b_name = "Alex"
b_age = 47
print(f"{b_name} is {b_age} years old.")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} is {self.age} years old."

person1 = Person("Jon", 15)
person2 = Person("Daeneris", 15)
person3 = Person("Tyrion", 30)
person4 = Person("Sansa", 15)
person5 = Person("Arya", 10)
person6 = Person("Jaime", 35)
person7 = Person("Cersei", 35)


print(person1)
print(person2)
print(person3)
print(person4)
print(person5)
print(person6)
print(person7)


class Vehicle:
    def __init__(self, color):
        self.color = color

class NewCar(Vehicle):
    def __init__(self, color, brand):
        super().__init__(color)
        # self.color = Vehicle(color)
        self.brand = brand

my_new_car = NewCar("white", "Dodge")
print(my_new_car.color, my_new_car.brand)


class Employee(Person):

    def __init__(self, name, age, job_title):
        super().__init__(name, age)
        self.job_title = job_title

    def __str__(self):
        return f"{self.name} is {self.age} years old and work as {self.job_title}"

new_human = Employee("Kira", 27, "CEO")

print(new_human)
