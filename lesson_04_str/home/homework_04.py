adwentures_of_tom_sawer = """\
Tom gave up the brush with reluctance in his .... face but alacrity
in his heart. And while 
the late steamer
"Big Missouri" worked ....
and sweated
in the sun,
the retired artist sat on a barrel in the .... shade close by, dangled his legs,
munched his apple, and planned the slaughter of more innocents.
There was no lack of material;
boys happened along every little while;
they came to jeer, but .... remained to whitewash. ....
By the time Ben was fagged out, Tom had traded the next chance to Billy Fisher for
a kite, in good repair;
and when he played
out, Johnny Miller bought
in for a dead rat and a string to swing it with—and so on, and so on,
hour after hour. And when the middle of the afternoon came, from being a
poor poverty, stricken boy in the .... morning, Tom was literally
rolling in wealth."""

# УВАГА! Перезаписуйте вміст змінної adwentures_of_tom_sawer у завданнях 01-03

# task 01 ==
""" Дані у строці adwentures_of_tom_sawer розбиті випадковим чином, через помилку.
треба замінити кінець абзацу на пробіл .replace("\n", " ")"""
print("Завдання 1")
adwentures_of_tom_sawer = adwentures_of_tom_sawer.replace("\n", " ")
print(adwentures_of_tom_sawer)

# task 02 ==
""" Замініть .... на пробіл
"""
print("Завдання 2")
adwentures_of_tom_sawer = adwentures_of_tom_sawer.replace("....", " ")
print(adwentures_of_tom_sawer)

# task 03 ==
""" Зробіть так, щоб у тексті було не більше одного пробілу між словами.
"""
print("Завдання 3")
adwentures_of_tom_sawer = " ".join(adwentures_of_tom_sawer.split())
print(adwentures_of_tom_sawer)

# task 04
""" Виведіть, скількі разів у тексті зустрічається літера "h"
"""
print("Завдання 4")
count_h = adwentures_of_tom_sawer.count("h")
print(count_h)

# task 05
""" Виведіть, скільки слів у тексті починається з Великої літери?
підказка - порахувати кожну велику літеру напр, .count("A") і їх сумму
"""
print("Завдання 5")
count_uppercase = sum(1 for word in adwentures_of_tom_sawer.split() if word[0].isupper())
print(count_uppercase)

# task 06
""" Виведіть позицію, на якій слово Tom зустрічається вдруге
"""
print("Завдання 6")
first = adwentures_of_tom_sawer.find("Tom")
if first != -1:
    second = adwentures_of_tom_sawer.find("Tom", first + 1)
    print(second)
else:
    print("Слово Tom не знайдено")

# task 07
""" Розділіть змінну adwentures_of_tom_sawer по кінцю речення.
Збережіть результат у змінній adwentures_of_tom_sawer_sentences
"""
print("Завдання 7")
adwentures_of_tom_sawer_sentences = None
adwentures_of_tom_sawer_sentences = adwentures_of_tom_sawer.rstrip(".").split(".")
print(adwentures_of_tom_sawer_sentences)

# task 08
""" Виведіть четверте речення з adwentures_of_tom_sawer_sentences.
Перетворіть рядок у нижній регістр.
"""
print("Завдання 8")
four_th_sentence = adwentures_of_tom_sawer_sentences[3].strip().lower()
print(four_th_sentence)

# task 09
""" Перевірте чи починається якесь речення з "By the time".
"""
print("Завдання 9")
found = False
for sentence in adwentures_of_tom_sawer_sentences:
    sentence = sentence.strip()
    if sentence.startswith("By the time"):
        found = True
if found:
    print("Так, починається.")
else:
    print("Ні, не починається.")

# task 10
""" Виведіть кількість слів останнього речення з adwentures_of_tom_sawer_sentences.
"""
print("Завдання 10")
adwentures_of_tom_sawer = adwentures_of_tom_sawer.rstrip(".")
sentence_last = adwentures_of_tom_sawer_sentences[-1]
count_words = len(sentence_last.split())
print(f"Кількість слів у останньому реченні: {count_words}")