### Завдання 1 — Зарплати
from functools import reduce

salaries = [30000, 45000, 28000, 60000, 52000, 33000]

# 1. Підвищення на 10%
raised = list(map(lambda s: s * 1.1, salaries))

# 2. Тільки більше 35000
high = list(filter(lambda s: s > 35000, raised))

# 3. Сума
total = reduce(lambda acc, s: acc + s, high, 0)

print(f"Сума: {total:.2f} грн")  # Сума: 209000.00 грн

### Завдання 2 — Слова


text = "Python це потужна мова програмування яка підходить для різних задач"

# Розбити на слова
words = text.split()

# Тільки довші за 4 символи, в нижньому регістрі, без дублів
long_unique = sorted(set(filter(lambda w: len(w) > 4, map(str.lower, words))))

print(long_unique)
# ['мова', 'програмування', 'python', 'підходить', 'потужна', 'різних', 'задач']
# (порядок залежить від алфавіту)

#Відповідь:
#  1. Сума: 209000.00 грн
# 2.['python', 'задач', 'потужна', 'програмування', 'підходить', 'різних']