
def add(a, b):
    return a + b

class BankAccount:

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("For deposit amount should be large than zero")
        self.balance += amount