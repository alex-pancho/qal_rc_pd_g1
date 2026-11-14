#Завдання 1.
passwords = [
    "Cossack1",
    "sich",
    "ZAPORIZHZHIA2024",
    "Sich Gate 5",
    "Mazepa99",
    "короткий1",
    "BohunTheBrave",
    "D0br0nich!",
    "аааааааА1",
    "Valid1Pass",
]


def is_strong(password: str) -> bool:
    return (
        8 <= len(password) <= 20
        and any(char.isdigit() for char in password)
        and any(char.isupper() for char in password)
        and not any(char.isspace() for char in password)
    )


# Надійні паролі
strong_passwords = list(
    filter(lambda p: is_strong(p), passwords)
)

# Ненадійні паролі
weak_passwords = list(
    filter(lambda p: not is_strong(p), passwords)
)


for password in strong_passwords:
    print(f"✅ {password} — надійний")

for password in weak_passwords:
    print(f"❌ {password} — відхилено")

print("..........")
   # Завдання 2
from functools import reduce

raw_registry = [
    "  іван сірко  | полковник | 150",
    "БОГДАН ХМЕЛЬНИЦЬКИЙ | гетьман | 10000",
    "петро дорошенко|сотник|75",
    "  Іван Мазепа | гетьман | 30000 ",
    "семен палій  |  полковник  | 500",
    "  Григорій Сковорода | філософ | 0",
]


# 1. Функція для очищення та перетворення рядка
def parse_record(record):
    name, rank, warriors = record.split("|")

    return {
        "name": name.strip().title(),
        "rank": rank.strip().title(),
        "warriors": int(warriors.strip())
    }


# 2. Очищаємо всі записи за допомогою map()
registry = list(map(parse_record, raw_registry))


# 3. Залишаємо козаків, у яких більше 0 воїнів
active_registry = list(
    filter(lambda soldier: soldier["warriors"] > 0, registry)
)


# 4. Підраховуємо загальну кількість воїнів через reduce()
total_warriors = reduce(
    lambda total, soldier: total + soldier["warriors"],
    active_registry,
    0
)


# 5. Сортуємо за кількістю воїнів у спадному порядку
sorted_registry = sorted(
    active_registry,
    key=lambda soldier: soldier["warriors"],
    reverse=True
)


# 6. Виводимо таблицю
print(f"Козацький реєстр ({len(sorted_registry)} записів):")
print("─" * 65)

print(f"{'№':<4}{'Ім’я':<25}{'Посада':<15}{'Воїни':>10}")
print("─" * 65)

for index, soldier in enumerate(sorted_registry, start=1):
    print(
        f"{index:<4}"
        f"{soldier['name']:<25}"
        f"{soldier['rank']:<15}"
        f"{soldier['warriors']:>10}"
    )

print("─" * 65)
print(f"Разом воїнів: {total_warriors}")

print("..........")
   # Завдання 3
   

messages = [
    "А роза упала на лапу азора",
    "Козак",
    "Зараз",
    "level",
    "Python",
    "А баба",
    "racecar",
    "Запоріжжя",
    "noon",
    "Мазепа",
]


# 1. Функція перевірки паліндрома
def is_palindrome(s: str) -> bool:
    cleaned = "".join(s.lower().split())
    return cleaned == cleaned[::-1]


# 2. Відбираємо паліндроми через filter()
palindromes = filter(
    lambda message: is_palindrome(message),
    messages
)


# 3. Перетворюємо кожен паліндром через map()
encrypted = map(
    lambda message: (
        f'🔐 {message} → '
        f'"{"".join(message.lower().split())[::-1]}"'
    ),
    palindromes
)


# 4. Виводимо результат
for message in encrypted:
    print(message)