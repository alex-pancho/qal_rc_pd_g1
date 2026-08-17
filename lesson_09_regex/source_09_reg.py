import re

def is_digits_only(chars_for_check:str) -> bool:

    for ch in chars_for_check:
        if ch not in  "0123456789":
            return False
    return True

digit_str = "12345"
alphanum = "123a5"

print(is_digits_only(digit_str))   # True
print(is_digits_only(alphanum))   # False

#regex = "\\d+"
regex = r"\d+"
print(bool(re.fullmatch(regex, digit_str)))
print(bool(re.fullmatch(regex, alphanum)))

"""
.  1 любий символ (крім `\n`)
^  Початок рядка | `^Hello` | Рядок, що починається з `Hello` |
$  кінець `world$`
*  повторення
+ 1 повторення
? 0-1 повторення
{n} Рівно n повторень | `\d{4}` | `2024`, `1999`
{n,m}  Від n до m повторень | `\d{2,4}` | `12`, `123`, `1234`
[]  Клас символів | `[aeiou]` | Будь-яка голосна
[^] Заперечення класу | `[^0-9]` | Будь-який нецифровий символ
|   Або | `cat|dog` | `cat` або `dog`
()  Група | `(ab)+` | `ab`, `abab`, `ababab`
\   Екранування | `\.` | Буквальна крапка
"""

"""
| `\d` | Цифра | `[0-9]` |
| `\D` | Не цифра | `[^0-9]` |
| `\w` | Слово (літера, цифра, `_`) | `[a-zA-Z0-9_]` |
| `\W` | Не слово | `[^a-zA-Z0-9_]` |
| `\s` | Пробільний символ | `[ \t\n\r\f\v]` |
| `\S` | Не пробільний | `[^ \t\n\r\f\v]` |
| `\b` | Межа слова | — |
| `\B` | Не межа слова | — |
"""

text = "Python 3.12 вийшов у 2023 році"

numbers = re.findall(r"\d+", text)
print("findall \\d+", numbers)

words = re.findall(r"\w+", text)
print("findall \\w+",words)

dots = re.findall(r"3.12", text) #
print(dots)

# \. — буквальна крапка (екранована)
real_dots = re.findall(r"3\.12", text)
print(real_dots)

#
# Повертає об'єкт Match або None
result = re.match(r"\d+", "123 abc")
print(result)

result = re.match(r"\d+", "123 abc 456")
print(result)

result = re.match(r"\d+", "123 456")
print(result)


result = re.match(r"\d+", "3456 abc")
print(result)

result = re.match(r"\d+", "abc 123")
print("end", result)

result = re.match(r"\d+", "abc 3456")
print("end", result)

text = "Телефон: +380-67-123-45-67, дзвоніть! +380-96-222-44-66"

pattern = r"\+\d{3}-\d{2}-\d{3}-\d{2}-\d{2}"

result = re.search(pattern, text)
print("phone", result)
if result:
    print(result.group())  # +380-67-123-45-67
    print(result.span())   # (9, 27) — позиції початку і кінця


result = re.findall(pattern, text)
print("phone findall", result)

def is_valid_email(email:str):
    pattern_mail = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    check = re.fullmatch(pattern_mail, email)
    print(check)
    return bool(check)

print(is_valid_email("user@example.com"))
print(is_valid_email("not-an-email"))
print(is_valid_email("user@example.com!!!"))

cleaned = re.sub(pattern, "[ПРИХОВАНИЙ НОМЕР]", text)
print(cleaned)

once = re.sub(pattern, "[ПРИХОВАНИЙ НОМЕР]", text, count=1)
print(once)

text = "Замовлення №12345 від 2024-03-15"
pattern = r"№(\d+) від (\d{4}-\d{2}-\d{2})"

match = re.search(pattern, text)

if match:
    print(match.group())    # '№12345 від 2024-03-15' — все співпадіння
    print(match.group(0))   # '№12345 від 2024-03-15' — те саме, що group()
    print(match.group(1))   # '12345'      — перша група ()
    print(match.group(2))   # '2024-03-15' — друга група ()
    print(match.groups())   # ('12345', '2024-03-15') — всі групи
    print(match.start())    # 10 — позиція початку
    print(match.end())      # 33 — позиція кінця
    print(match.span())     # (10, 33) — кортеж (початок, кінець)


log_line = "2024-03-15 14:32:05 ERROR DatabaseConnection failed"

print("*"*88)

pattern = r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>\w+) (?P<message>.+)"

match = re.search(pattern, log_line)

if match:
    print(match.group("date"))    # 2024-03-15
    print(match.group("time"))    # 14:32:05
    print(match.group("level"))   # ERROR
    print(match.group("message")) # DatabaseConnection failed

    # Або через groupdict()
    info = match.groupdict()
    print(info)


text = "Python python PYTHON"
result = re.findall(r"python", text, re.IGNORECASE)
print(result)

multiline_text = """перший рядок
другий рядок
третій рядок"""

result = re.findall(r"^\w+", multiline_text, re.MULTILINE)
print(result)

text2 = "початок\nкінець"
print(re.search(r"початок.кінець", text2))
print(re.search(r"початок.кінець", text2, re.DOTALL))

"""
За замовчуванням `*`, `+`, `?` — **жадібні**: захоплюють якомога більше символів.  
Додавши `?` після квантифікатора, робимо його **лінивим**: захоплює якомога менше.
"""

html = "<b>жирний</b> і <i>курсив</i>"

greedy = re.findall(r"<.+>", html)
print(greedy)

lazy = re.findall(r"<.+?>", html)
print(lazy)

prices = "100 грн, 250 USD, 75 грн, 1000 EUR"

grn_prices = re.findall(r"\d+(?= грн)", prices)
print(grn_prices)

usd_text = "Ціна: $150, 34 грн знижка: $30"
usd_values = re.findall(r"(?<=\$)\d+", usd_text)
print(usd_values)
