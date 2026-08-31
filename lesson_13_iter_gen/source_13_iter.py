my_iterable = iter([1, 2, 3, 4, 5])

print(my_iterable)
print(next(my_iterable))
print(next(my_iterable))
print(next(my_iterable))
print(next(my_iterable))
print(next(my_iterable))
# print(next(my_iterable)) # StopIteration
# print(next(my_iterable))
# print(next(my_iterable))
# Помилка StopIteration при спробі отримати 
# наступний елемент
try:
    print(next(my_iterable))
except StopIteration:
    print("StopIteration: Ітератор закінчився")


class MinIter:

    def __init__(self, max: int):
        self.i = 0
        self.max = max

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i >= self.max:
            raise StopIteration
        self.i += 2
        return self.i

my_easy_iter = MinIter(20)
print(my_easy_iter)
print(next(my_easy_iter))
print(next(my_easy_iter))

for i in my_easy_iter:
    print(">", i)

# print(next(my_easy_iter))


class FibonacciIterator:

    def __init__(self, first:int = 1, second:int = 1):
        self.first = first
        self.second = second
    
    def __iter__(self):
        return self

    def __next__(self):
        self.first, self.second = self.second,  self.second + self.first
        return self.first


print("*"*8)
fib = FibonacciIterator() # 24157817, 39088169

for _ in range(20):
    print(next(fib))

print("Тільки вперед!")
numbers = ["sdhjsd", 56, {"Ok": 1234}, "jksdh", "asd" , "asdsa"]
i = iter(numbers)
print(next(i))
print(next(i))
print("Вичерпність")
print(next(i))
print("1>", *i)
print("2>", *i)
# print(next(i))

iterator = iter([ 0, 1, 2, 0, 3, 4])

print(all(iterator)) # бере доки не зібється
print(any(iterator)) # бере доки не зібється
print(next(iterator))
print(next(iterator))
lst = list(iterator)
print(lst)