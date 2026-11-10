from functools import reduce

print("=== Завдання 1. Охоронці воріт ===")

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
    if not (8 <= len(password) <= 20):
        return False
    if " " in password:
        return False
    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    return has_digit and has_upper


strong_passwords = list(filter(lambda p: is_strong(p), passwords))
for pwd in strong_passwords:
    print(f"✅ {pwd} — надійний")

print()

weak_passwords = list(filter(lambda p: not is_strong(p), passwords))
for pwd in weak_passwords:
    print(f"❌ {pwd} — відхилено")


print("\n=== Завдання 2. Перепис козацького реєстру ===")

raw_registry = [
    "  іван сірко  | полковник | 150",
    "БОГДАН ХМЕЛЬНИЦЬКИЙ | гетьман | 10000",
    "петро дорошенко|сотник|75",
    "  Іван Мазепа | гетьман | 30000 ",
    "семен палій  |  полковник  | 500",
    "  Григорій Сковорода | філософ | 0",
]


def parse_row(row: str) -> dict:
    parts = [p.strip() for p in row.split("|")]
    return {
        "name": parts[0].title(),
        "rank": parts[1].capitalize(),
        "warriors": int(parts[2]),
    }


parsed_registry = list(map(parse_row, raw_registry))
active_cossacks = list(filter(lambda c: c["warriors"] > 0, parsed_registry))
total_warriors = reduce(
    lambda acc, c: acc + c["warriors"], active_cossacks, 0
)
sorted_cossacks = sorted(
    active_cossacks, key=lambda c: c["warriors"], reverse=True
)

print(f"Козацький реєстр ({len(sorted_cossacks)} записи):")
print("─" * 50)
print(f"{'№':<3} {'Ім\'я':<23} {'Посада':<12} {'Воїни':<8}")
print("─" * 50)

for idx, cossack in enumerate(sorted_cossacks, 1):
    print(
        f"{idx:<3} {cossack['name']:<23} {cossack['rank']:<12} {cossack['warriors']:<8}"
    )

print("─" * 50)
print(f"Разом воїнів: {total_warriors}")


print("\n=== Завдання 3. Пошук козацьких шифрів ===")

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


def is_palindrome(s: str) -> bool:
    cleaned = s.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


ciphers = list(filter(lambda msg: is_palindrome(msg), messages))
formatted_ciphers = list(
    map(
        lambda msg: f'🔐 {msg} → {msg.replace(" ", "").lower()}',
        ciphers,
    )
)

for result in formatted_ciphers:
    print(result)