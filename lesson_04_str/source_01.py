my_text = "Всім привіт!"
verse = "Реве та стогне Дніпр"
print(id(verse))
verse = verse + " широкий"
print(id(verse))
print(verse)
print(verse[0])
print(verse[1])
print(verse[2])
print(verse[len(verse) - 1]) #
print(verse[-1])
print(verse[-2])
print(verse[-3])
print(verse[6:12])
print(verse[12])
print(verse[6:16:2])

print("Все до 10 симв>", verse[:10])
print("Все від 15 симв>", verse[15:])

print("Все від 15 симв>", verse[15::2])
word_len = len(verse)
print("Len of variable:", word_len)

for i in verse:
    print(i)

verse_2 = "Сердитий вітер завива"
poems = verse + "\n"  + verse_2
print(poems)

poems = f"{verse} \n{verse_2}"
print(poems)

split_words = poems.split()
print(split_words)

fruit = "apple,orange,banana"
fruit_split = fruit.split(",")
print(fruit_split)
fruit_split_2 = fruit.split("n")
print(fruit_split_2)

filename = "filename.txt"
print("Start with 'file':", filename.startswith("file"))
print(filename.startswith("lie"))
print("End with 'file':", filename.endswith("file"))
print(filename.endswith("txt"))
print(filename.endswith(".txt"))
print(filename.startswith("filename.txt"), filename.endswith("filename.txt"))

hello_upper = "ABBA"
print("hello_upper is upper? ",hello_upper.isupper())

hello_lower = "be my lover"
print("hello_lower is lower? ",hello_lower.islower())

hello_hello = "Good Day"
print("hello_hello is title? ", hello_hello.istitle())

to_upper_hello_lower = hello_lower.upper()
print("hello_lower NOW UPPER:", to_upper_hello_lower)

to_lower = hello_upper.lower()
print("hello_UPPER to lower:", to_lower)

to_capital = "let my people go"
first_up = to_capital.capitalize()
print(first_up)

second_up = to_capital.title()
print(second_up)

index = poems.find("ер")
print(index)
print(poems[index:])

index_2 = poems.find("ер", index + 1)
print(index_2)
print(poems[index_2:])

print(poems.count("ер"))

index_3 = poems.find("Taras")
print(index_3)

new_poems = poems.replace("Дніпр", "Буг")
print(new_poems)

re_string = "Це приклад для заміни у рядку, заміни лише перше входження"
new_re_string = re_string.replace("заміни", "поміняй", 1)
print(new_re_string)

login_with_spaces =  "      my   login      "
clean_string = login_with_spaces.strip()
print(f".{clean_string}.")

russian_dumb = "zzzzzzzzzzzzzzzzzzza russs usrussssssszzz"
clean_string = russian_dumb.strip("z").strip("s")
print(f".{clean_string}.")


some_text = "Fer   df df    fdsf iie    rj dkfksjie wje    wiw ew     ei"
clean_string = some_text.replace("  ", " ").replace("  ", " ")
print(f".{clean_string}.")

clean_string_2 = some_text.split()
print(clean_string_2)


united_text = " ".join(clean_string_2)
print(united_text)

united_text_2 = ", ".join(clean_string_2)
print(united_text_2)

str_number = "12345"
int_number = int(str_number)
print(int_number, type(int_number))

str_fl_number = "12.45"
fl_number = float(str_fl_number)
print(fl_number, type(fl_number))

value = "True"
bool_val = bool(value)
print(bool_val)

value = "xcvdlvjdjkf hjdhg j"
bool_val = bool(value)
print(bool_val)

value = ""
bool_val = bool(value)
print(bool_val)

value = "False"
bool_val = bool(value)
print(bool_val)


value_1 = ""
value_2 = ''
value_3 = ""''""
print(bool(value_1))
print(bool(value_2))
print(bool(value_3))


name = "Ivan"
age = 18
user_data = f"Привіт, {name}! Тобі {age} років."
print(user_data)

a = 5
b = 3
print(f"Сума чисел {a} та {b} дорівнює {a + b}.")

pi = 3.14159265359
print(f"Pi: {pi:.4f}")
