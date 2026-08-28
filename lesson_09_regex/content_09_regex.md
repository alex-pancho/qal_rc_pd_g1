# Заняття 10. Регулярні вирази

**Курс:** Програмування Python 

## План заняття

1. Що таке регулярні вирази і навіщо вони потрібні
2. Метасимволи — алфавіт регулярних виразів
3. Модуль `re` — основні функції
4. Об'єкт `Match` та робота з групами
5. Розширені регулярні вирази (lookahead, lookbehind, named groups)
6. Пошук усіх співпадань: `findall` та `finditer`
7. Розділення рядків: `split`
8. Практичні завдання

## 1. Що таке регулярні вирази?

**Регулярний вираз (regex, regexp)** — це шаблон, який описує набір рядків. За допомогою одного шаблону можна перевірити тисячі рядків і знайти саме те, що потрібно.

### Навіщо вони потрібні?

| Задача | Без regex | З regex |
|---|---|---|
| Перевірити email | 10–15 рядків коду | 1 рядок |
| Знайти всі телефони в тексті | Складний цикл | `findall` |
| Замінити всі дати у форматі ДД.ММ.РРРР | Важко | `sub` |
| Витягти IP-адреси з логів | Дуже важко | Простий шаблон |

### Перший приклад — без regex та з regex

```python
# Без regex: перевірити, що рядок містить лише цифри
def is_digits_only(s):
    for ch in s:
        if ch not in "0123456789":
            return False
    return True

print(is_digits_only("12345"))   # True
print(is_digits_only("123a5"))   # False

# З regex — одна строчка
import re
print(bool(re.fullmatch(r"\d+", "12345")))  # True
print(bool(re.fullmatch(r"\d+", "123a5")))  # False
```

## 2. Метасимволи

Метасимволи — це спеціальні символи, які мають особливе значення у шаблоні.

### 2.1 Базові метасимволи

| Символ | Значення | Приклад шаблону | Що знаходить |
|---|---|---|---|
| `.` | Будь-який символ (крім `\n`) | `a.b` | `aXb`, `a1b`, `a b` |
| `^` | Початок рядка | `^Hello` | Рядок, що починається з `Hello` |
| `$` | Кінець рядка | `world$` | Рядок, що закінчується на `world` |
| `*` | 0 або більше повторень | `ab*` | `a`, `ab`, `abb`, `abbb` |
| `+` | 1 або більше повторень | `ab+` | `ab`, `abb`, `abbb` (але не `a`) |
| `?` | 0 або 1 повторення | `colou?r` | `color`, `colour` |
| `{n}` | Рівно n повторень | `\d{4}` | `2024`, `1999` |
| `{n,m}` | Від n до m повторень | `\d{2,4}` | `12`, `123`, `1234` |
| `[]` | Клас символів | `[aeiou]` | Будь-яка голосна |
| `[^]` | Заперечення класу | `[^0-9]` | Будь-який нецифровий символ |
| `\|` | Або | `cat\|dog` | `cat` або `dog` |
| `()` | Група | `(ab)+` | `ab`, `abab`, `ababab` |
| `\` | Екранування | `\.` | Буквальна крапка |

### 2.2 Скорочені класи символів

| Позначення | Що означає | Еквівалент |
|---|---|---|
| `\d` | Цифра | `[0-9]` |
| `\D` | Не цифра | `[^0-9]` |
| `\w` | Слово (літера, цифра, `_`) | `[a-zA-Z0-9_]` |
| `\W` | Не слово | `[^a-zA-Z0-9_]` |
| `\s` | Пробільний символ | `[ \t\n\r\f\v]` |
| `\S` | Не пробільний | `[^ \t\n\r\f\v]` |
| `\b` | Межа слова | — |
| `\B` | Не межа слова | — |

### 2.3 Приклади метасимволів у коді

```python
import re

text = "Python 3.12 вийшов у 2023 році"

# \d+ — одна або більше цифр
numbers = re.findall(r"\d+", text)
print(numbers)  # ['3', '12', '2023']

# \w+ — одне або більше "словесних" символів
words = re.findall(r"\w+", text)
print(words)  # ['Python', '3', '12', 'вийшов', 'у', '2023', 'році']

# . — будь-який символ
dots = re.findall(r"3.12", text)
print(dots)  # ['3.12']

# \. — буквальна крапка (екранована)
real_dots = re.findall(r"3\.12", text)
print(real_dots)  # ['3.12']
```

> **Важливо:** Завжди використовуйте `r"..."` (raw string) для шаблонів regex, щоб уникнути проблем з екранування. `r"\n"` — це два символи: зворотна коса риска і `n`, а не символ нового рядка.

## 3. Модуль `re` — основні функції

```python
import re
```

### 3.1 `re.match()` — пошук на початку рядка

`match()` перевіряє шаблон **тільки на початку** рядка.

```python
import re

# Повертає об'єкт Match або None
result = re.match(r"\d+", "123 abc")
print(result)         # <re.Match object; span=(0, 3), match='123'>
print(result.group()) # '123'

# Шаблон не на початку — None
result2 = re.match(r"\d+", "abc 123")
print(result2)        # None
```

### 3.2 `re.search()` — пошук по всьому рядку

`search()` знаходить **перше** входження шаблону в будь-якому місці рядка.

```python
import re

text = "Телефон: +380-67-123-45-67, дзвоніть!"

result = re.search(r"\+\d{3}-\d{2}-\d{3}-\d{2}-\d{2}", text)
if result:
    print(result.group())  # +380-67-123-45-67
    print(result.span())   # (9, 27) — позиції початку і кінця
```

### 3.3 Порівняння `match()` vs `search()`

```python
import re

text = "Сьогодні 2024-01-15, а завтра 2024-01-16"

# match() — шукає тільки на початку рядка
m1 = re.match(r"\d{4}-\d{2}-\d{2}", text)
print(m1)  # None — рядок не починається з дати

# search() — шукає по всьому рядку
m2 = re.search(r"\d{4}-\d{2}-\d{2}", text)
print(m2.group())  # 2024-01-15 — знайшов першу дату
```

### 3.4 `re.fullmatch()` — перевірка всього рядка

```python
import re

# Перевірити, що рядок — це саме email
def is_valid_email(email):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return bool(re.fullmatch(pattern, email))

print(is_valid_email("user@example.com"))    # True
print(is_valid_email("not-an-email"))        # False
print(is_valid_email("user@example.com!!!")) # False — є зайві символи
```

### 3.5 `re.sub()` — заміна

```python
import re

text = "Телефон: 067-123-45-67 або 050-987-65-43"

# Замінити всі телефони на [ПРИХОВАНИЙ НОМЕР]
cleaned = re.sub(r"\d{3}-\d{3}-\d{2}-\d{2}", "[ПРИХОВАНИЙ НОМЕР]", text)
print(cleaned)
# Телефон: [ПРИХОВАНИЙ НОМЕР] або [ПРИХОВАНИЙ НОМЕР]

# Замінити лише перше входження
once = re.sub(r"\d{3}-\d{3}-\d{2}-\d{2}", "[ПРИХОВАНИЙ НОМЕР]", text, count=1)
print(once)
# Телефон: [ПРИХОВАНИЙ НОМЕР] або 050-987-65-43
```

## 4. Об'єкт `Match`

Функції `match()`, `search()`, `fullmatch()` повертають об'єкт `Match` (або `None`).

### 4.1 Основні методи об'єкта Match

```python
import re

text = "Замовлення №12345 від 2024-03-15"
pattern = r"№(\d+) від (\d{4}-\d{2}-\d{2})"

m = re.search(pattern, text)

if m:
    print(m.group())    # '№12345 від 2024-03-15' — все співпадіння
    print(m.group(0))   # '№12345 від 2024-03-15' — те саме, що group()
    print(m.group(1))   # '12345'      — перша група ()
    print(m.group(2))   # '2024-03-15' — друга група ()
    print(m.groups())   # ('12345', '2024-03-15') — всі групи
    print(m.start())    # 10 — позиція початку
    print(m.end())      # 33 — позиція кінця
    print(m.span())     # (10, 33) — кортеж (початок, кінець)
```

### 4.2 Іменовані групи `(?P<name>...)`

Іменовані групи роблять код читабельнішим.

```python
import re

log_line = "2024-03-15 14:32:05 ERROR DatabaseConnection failed"

pattern = r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>\w+) (?P<message>.+)"

m = re.search(pattern, log_line)

if m:
    print(m.group("date"))    # 2024-03-15
    print(m.group("time"))    # 14:32:05
    print(m.group("level"))   # ERROR
    print(m.group("message")) # DatabaseConnection failed

    # Або через groupdict()
    info = m.groupdict()
    print(info)
    # {'date': '2024-03-15', 'time': '14:32:05', 'level': 'ERROR', 'message': 'DatabaseConnection failed'}
```

## 5. Розширені регулярні вирази

### 5.1 Прапорці (Flags)

Прапорці змінюють поведінку шаблону.

```python
import re

text = "Python python PYTHON"

# re.IGNORECASE (re.I) — ігнорувати регістр
result = re.findall(r"python", text, re.IGNORECASE)
print(result)  # ['Python', 'python', 'PYTHON']

# re.MULTILINE (re.M) — ^ та $ для кожного рядка, а не всього тексту
multiline_text = """перший рядок
другий рядок
третій рядок"""

result = re.findall(r"^\w+", multiline_text, re.MULTILINE)
print(result)  # ['перший', 'другий', 'третій']

# re.DOTALL (re.S) — . збігається з \n теж
text2 = "початок\nкінець"
print(re.search(r"початок.кінець", text2))           # None
print(re.search(r"початок.кінець", text2, re.DOTALL)) # Match
```

### 5.2 Жадібний і лінивий квантифікатор

За замовчуванням `*`, `+`, `?` — **жадібні**: захоплюють якомога більше символів.  
Додавши `?` після квантифікатора, робимо його **лінивим**: захоплює якомога менше.

```python
import re

html = "<b>жирний</b> і <i>курсив</i>"

# Жадібний — захоплює від першого < до останнього >
greedy = re.findall(r"<.+>", html)
print(greedy)  # ['<b>жирний</b> і <i>курсив</i>']

# Лінивий — захоплює кожен тег окремо
lazy = re.findall(r"<.+?>", html)
print(lazy)  # ['<b>', '</b>', '<i>', '</i>']
```

### 5.3 Lookahead та Lookbehind (Перегляд вперед і назад)

Ці конструкції перевіряють наявність тексту **навколо** збігу, але **не включають** його до результату.

```python
import re

# Lookahead (?=...) — вперед: знайти число, за яким іде " грн"
prices = "100 грн, 250 USD, 75 грн, 1000 EUR"

grn_prices = re.findall(r"\d+(?= грн)", prices)
print(grn_prices)  # ['100', '75']

# Lookbehind (?<=...) — назад: знайти число, перед яким іде "$ "
usd_text = "Ціна: $ 150, знижка: $ 30"
usd_values = re.findall(r"(?<=\$ )\d+", usd_text)
print(usd_values)  # ['150', '30']

# Negative lookahead (?!...) — вперед, якщо НЕ збігається
# Знайти "python" не перед "3"
text = "python2 python3 python-scripts"
result = re.findall(r"python(?!3)", text)
print(result)  # ['python', 'python']  (python2 і python-scripts, без python3)
```

### 5.4 Компіляція шаблону `re.compile()`

Якщо один і той самий шаблон використовується багато разів — скомпілюйте його заздалегідь. Це пришвидшує роботу.

```python
import re

# Без компіляції — шаблон компілюється щоразу
for line in log_lines:
    re.search(r"\d{4}-\d{2}-\d{2}", line)

# З компіляцією — шаблон компілюється один раз
date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
for line in log_lines:
    date_pattern.search(line)

# Приклад
email_re = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

emails = [
    "valid@example.com",
    "not-valid",
    "another@test.org"
]

for email in emails:
    if email_re.fullmatch(email):
        print(f"✓ {email}")
    else:
        print(f"✗ {email}")
# ✓ valid@example.com
# ✗ not-valid
# ✓ another@test.org
```

## 6. Пошук усіх співпадань: `findall` та `finditer`

### 6.1 `re.findall()` — повертає список рядків

```python
import re

text = """
Контакти відділу:
  - Марія: maria@company.ua, тел. 067-111-22-33
  - Олег: oleg@work.com, тел. 050-444-55-66
  - Підтримка: support@company.ua
"""

# Знайти всі email-адреси
emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
print(emails)
# ['maria@company.ua', 'oleg@work.com', 'support@company.ua']

# Знайти всі телефони
phones = re.findall(r"\d{3}-\d{3}-\d{2}-\d{2}", text)
print(phones)
# ['067-111-22-33', '050-444-55-66']

# Якщо шаблон має групи — findall повертає список кортежів
pattern = r"(\w+): (\S+@\S+)"
contacts = re.findall(pattern, text)
print(contacts)
# [('Марія', 'maria@company.ua,'), ('Олег', 'oleg@work.com,')]
```

### 6.2 `re.finditer()` — повертає ітератор об'єктів Match

`finditer` ефективніший за `findall` для великих текстів: не створює весь список одразу.

```python
import re

log = """
2024-03-15 10:00:01 INFO  Server started
2024-03-15 10:05:22 ERROR Failed to connect to DB
2024-03-15 10:05:23 ERROR Retry attempt 1
2024-03-15 10:06:00 INFO  Connection restored
"""

pattern = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>\w+)\s+(?P<msg>.+)"
)

print("=== Тільки помилки ===")
for m in pattern.finditer(log):
    if m.group("level") == "ERROR":
        print(f"[{m.group('time')}] {m.group('msg')}")

# === Тільки помилки ===
# [10:05:22] Failed to connect to DB
# [10:05:23] Retry attempt 1
```

### 6.3 Коли використовувати `findall` vs `finditer`?

| | `findall` | `finditer` |
|---|---|---|
| Повертає | `list` рядків або кортежів | ітератор `Match`-об'єктів |
| Пам'ять | Завантажує всі результати одразу | Обчислює по одному |
| Коли використовувати | Мало збігів, потрібен список | Багато збігів, великий текст |
| Доступ до позицій | Ні | Так (`.span()`, `.start()`, `.end()`) |

## 7. Розділення рядків: `re.split()`

`re.split()` схожий на `str.split()`, але шаблон може бути складнішим.

### 7.1 Базовий split

```python
import re

# Звичайний str.split — лише один роздільник
text = "яблуко, груша; банан| лимон"
print(text.split(","))  # ['яблуко', ' груша; банан| лимон'] — лише кома

# re.split — кілька роздільників одночасно
fruits = re.split(r"[,;|]\s*", text)
print(fruits)  # ['яблуко', 'груша', 'банан', 'лимон']
```

### 7.2 Split за пробілами будь-якого типу

```python
import re

messy = "слово1   слово2\t\tслово3\n\nслово4"

# str.split() без аргументів вже це вміє
print(messy.split())  # ['слово1', 'слово2', 'слово3', 'слово4']

# Але re.split дає більше контролю
parts = re.split(r"\s+", messy.strip())
print(parts)  # ['слово1', 'слово2', 'слово3', 'слово4']
```

### 7.3 Збереження роздільника у результаті

Якщо взяти шаблон у дужки `()`, роздільник потрапляє до результату.

```python
import re

text = "Привіт! Як справи? Все добре."

# Без груп — роздільники зникають
parts = re.split(r"[.!?]", text)
print(parts)  # ['Привіт', ' Як справи', ' Все добре', '']

# З групою — роздільники зберігаються
parts_with_sep = re.split(r"([.!?])", text)
print(parts_with_sep)
# ['Привіт', '!', ' Як справи', '?', ' Все добре', '.', '']
```

### 7.4 Обмеження кількості розділень

```python
import re

csv_line = "Іван,Петренко,25,Київ,Python developer"

# Розділити лише на перші 2 частини
parts = re.split(r",", csv_line, maxsplit=2)
print(parts)
# ['Іван', 'Петренко', '25,Київ,Python developer']
```

## 8. Практичні завдання

### Завдання 1 — Валідатор форм

Напишіть функції для валідації:
- Email-адреси
- Українського номера телефону (формат `+380XXXXXXXXX` або `0XXXXXXXXX`)
- Паролю (мінімум 8 символів, є велика літера, мала літера, цифра)

```python
import re

def validate_email(email: str) -> bool:
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return bool(re.fullmatch(pattern, email))

def validate_phone(phone: str) -> bool:
    pattern = r"(\+380|0)\d{9}"
    return bool(re.fullmatch(pattern, phone))

def validate_password(password: str) -> bool:
    # Довжина >= 8
    if len(password) < 8:
        return False
    # Є велика літера
    if not re.search(r"[A-Z]", password):
        return False
    # Є мала літера
    if not re.search(r"[a-z]", password):
        return False
    # Є цифра
    if not re.search(r"\d", password):
        return False
    return True

# Тести
print(validate_email("user@example.com"))   # True
print(validate_email("bad-email"))          # False

print(validate_phone("+380671234567"))      # True
print(validate_phone("0671234567"))         # True
print(validate_phone("12345"))              # False

print(validate_password("MyPass1"))         # False (7 символів)
print(validate_password("MyPassword1"))     # True
print(validate_password("mypassword1"))     # False (немає великої)
```

### Завдання 2 — Парсер логів

Є файл з логами. Знайдіть всі рядки типу `ERROR` і `WARNING`, виведіть час та повідомлення.

```python
import re

log_data = """
2024-03-15 09:00:00 INFO  Application started
2024-03-15 09:05:12 WARNING Low disk space: 15% remaining
2024-03-15 09:10:33 ERROR  Cannot connect to database: timeout
2024-03-15 09:10:34 ERROR  Retrying connection (attempt 1/3)
2024-03-15 09:11:00 INFO  Connected to database
2024-03-15 09:45:22 WARNING Memory usage above 80%
"""

pattern = re.compile(
    r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (ERROR|WARNING)\s+(.+)"
)

for m in pattern.finditer(log_data):
    date, time, level, msg = m.groups()
    icon = "🔴" if level == "ERROR" else "🟡"
    print(f"{icon} [{date} {time}] {msg}")

# 🟡 [2024-03-15 09:05:12] Low disk space: 15% remaining
# 🔴 [2024-03-15 09:10:33] Cannot connect to database: timeout
# 🔴 [2024-03-15 09:10:34] Retrying connection (attempt 1/3)
# 🟡 [2024-03-15 09:45:22] Memory usage above 80%
```

### Завдання 3 — Обробка тексту

Дано текст з «брудними» даними. Виконайте:
1. Витягніть всі суми у гривнях (формат: `1 500 грн` або `500грн`)
2. Нормалізуйте пробіли (кілька пробілів → один)
3. Розбийте текст на речення

```python
import re

text = """
Квартира   коштує  2 500 000 грн.  Комісія агента — 50000грн.  
Комунальні платежі:   близько 3 500 грн на місяць!   Торг доречний.
"""

# 1. Суми в гривнях
amounts = re.findall(r"[\d\s]+(?=\s*грн)", text)
amounts_clean = [a.strip().replace(" ", "") for a in amounts]
print("Суми:", amounts_clean)
# Суми: ['2500000', '50000', '3500']

# 2. Нормалізація пробілів
normalized = re.sub(r" {2,}", " ", text.strip())
print("Нормалізовано:")
print(normalized)

# 3. Розбити на речення
sentences = re.split(r"[.!?]+\s*", normalized.strip())
sentences = [s.strip() for s in sentences if s.strip()]
print("Речення:")
for i, s in enumerate(sentences, 1):
    print(f"  {i}. {s}")
```

### Завдання 4 — Маскування персональних даних (★ Підвищений рівень)

Напишіть функцію, яка маскує в тексті: email-адреси, телефони, імена у форматі "Ім'я Прізвище" (два слова з великої літери поспіль).

```python
import re

def mask_personal_data(text: str) -> str:
    # Маскувати email
    text = re.sub(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "[EMAIL]",
        text
    )
    # Маскувати телефони
    text = re.sub(
        r"(\+380|0)\d{9}",
        "[ТЕЛЕФОН]",
        text
    )
    # Маскувати ПІБ (два слова поспіль з великої літери)
    text = re.sub(
        r"\b[А-ЯІЇЄ][а-яіїє']+\s+[А-ЯІЇЄ][а-яіїє']+\b",
        "[ІМ'Я]",
        text
    )
    return text

sample = """
Заявку подав Іван Петренко.
Контакт: ivan.petrenko@mail.com або +380671234567.
Співавтор — Олена Коваль, тел. 0501112233.
"""

print(mask_personal_data(sample))
# Заявку подав [ІМ'Я].
# Контакт: [EMAIL] або [ТЕЛЕФОН].
# Співавтор — [ІМ'Я], тел. [ТЕЛЕФОН].
```

## Підсумок заняття

| Що вивчили | Функція/Конструкція |
|---|---|
| Перевірити початок рядка | `re.match()` |
| Знайти перше входження | `re.search()` |
| Перевірити весь рядок | `re.fullmatch()` |
| Знайти всі входження | `re.findall()`, `re.finditer()` |
| Замінити збіги | `re.sub()` |
| Розділити рядок | `re.split()` |
| Прискорити повторний пошук | `re.compile()` |
| Витягти частину збігу | Групи `()`, `m.group(1)` |
| Іменовані групи | `(?P<name>...)`, `m.group("name")` |
| Жадібний / лінивий | `+` vs `+?`, `*` vs `*?` |
| Lookahead / Lookbehind | `(?=...)`, `(?<=...)` |

### Корисні ресурси

- **Тестування regex онлайн:** [regex101.com](https://regex101.com) — вибирайте Python, одразу пояснює кожну частину шаблону
- **Документація Python:** [docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)
- **Шпаргалка:** [pythex.org](https://pythex.org)

*Наступне заняття: **Основи ООП: класи та об'єкти***
