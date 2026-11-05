from functools import reduce

print("=== Завдання 1 ===")

salaries = [30000, 45000, 28000, 60000, 52000, 33000]

raised = list(map(lambda s: s * 1.1, salaries))

high = list(filter(lambda s: s > 35000, raised))

total = reduce(lambda acc, s: acc + s, high, 0)

print(f"Сума: {total:.2f} грн")


print("\n=== Завдання 2 ===")

text = (
    "Python це потужна мова програмування "
    "яка підходить для різних задач"
)

words = text.split()

long_unique = sorted(
    set(
        filter(
            lambda w: len(w) > 4,
            map(str.lower, words)
        )
    )
)

print(long_unique)