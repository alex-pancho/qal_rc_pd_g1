from functools import reduce

# Завдання 1 — Зарплати
salaries = [30000, 45000, 28000, 60000, 52000, 33000]


high_initial = list(filter(lambda s: s > 35000, salaries))


raised = list(map(lambda s: s * 1.1, high_initial))


total = reduce(lambda acc, s: acc + s, raised, 0)

print(f"Сума: {total:.2f} грн")

#Завдання 2 — Слова
text = "Python це потужна мова програмування яка підходить для різних задач"

words = text.split()
long_unique = sorted(set(filter(lambda w: len(w) > 4, map(str.lower, words))))

print(long_unique)