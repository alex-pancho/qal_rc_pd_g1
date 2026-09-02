x = "global" # G — глобальний простір імен

def outer():
    x = "enclosing"  # E — простір імен outer

    def inner():
        x = "local" # L — локальний простір імен inner
        print(x) # "local" — знайдено на рівні L

    inner()
    print(x) # "enclosing" — знайдено на рівні E



# LEGB # B — Built-in (вбудований: print, len, range тощо)

counter = 0  # глобальна змінна

def increment():
    global counter  # явно вказуємо, що працюємо з глобальною
    counter += 1


def outer3():
    count = 0         # змінна outer

    def inner():
        nonlocal count  # звертаємось до змінної enclosing-рівня
        count += 1

    inner()
    inner()
    print("nonlocal:", count)        # 2


# count = 0         # змінна outer
# def outer2(count):
   
#     def inner(count):
#         # nonlocal count  # звертаємось до змінної enclosing-рівня
#         count += 1
#         return count

#     inner(count)
#     inner(count)
#     print("nonlocal:", count)        # 2

def main() -> None:
    """Точка входу — виконується тільки при прямому запуску."""
    print(f"2 + 3 = {2 + 3}")
    print(f"10 - 4 = {10 - 4}")


# outer2(count)
if __name__ == "__main__":
    outer()
    print(x)
    increment()
    increment()
    print(counter)
    outer3()
    print("імена у поточному просторі імен", dir())
    print("глобальний простір імен", globals())
    print("локл простір імен", locals())
    main()
