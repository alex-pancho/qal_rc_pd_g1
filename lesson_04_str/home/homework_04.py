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
#""" Дані у строці adwentures_of_tom_sawer розбиті випадковим чином, через помилку.
#треба замінити кінець абзацу на пробіл .replace("\n", " ")"""


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
adwentures_of_tom_sawer2 = adwentures_of_tom_sawer.replace("\n", " ")
print(adwentures_of_tom_sawer2)


# task 02 ==
#""" Замініть .... на пробіл

adwentures_of_tom_sawer3 = adwentures_of_tom_sawer2.replace("....", " ")
print(adwentures_of_tom_sawer3)



# task 03 ==
#""" Зробіть так, щоб у тексті було не більше одного пробілу між словами.

adwentures_of_tom_sawer4 = adwentures_of_tom_sawer3.split()
adwentures_of_tom_sawer5 = " ".join(adwentures_of_tom_sawer4)
print(adwentures_of_tom_sawer5)

# чи можна це все об'єднати так????? : print(" ".join(dwentures_of_tom_sawer3.split()))


# task 04
#""" Виведіть, скількі разів у тексті зустрічається літера "h"

print(adwentures_of_tom_sawer5.count("h"))




# task 05
#""" Виведіть, скільки слів у тексті починається з Великої літери?
#підказка - порахувати кожну велику літеру напр, .count("A") і їх сумму

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
total = 0
for letter in alphabet:
    total += adwentures_of_tom_sawer5.count(letter)
print(total)



# task 06
#""" Виведіть позицію, на якій слово Tom зустрічається вдруге


print(adwentures_of_tom_sawer5.find("Tom", 2))



# task 07
#""" Розділіть змінну adwentures_of_tom_sawer по кінцю речення.
#Збережіть результат у змінній adwentures_of_tom_sawer_sentences

adwentures_of_tom_sawer_sentences = adwentures_of_tom_sawer5.split(". ")
print(adwentures_of_tom_sawer_sentences)



# task 08
#""" Виведіть четверте речення з adwentures_of_tom_sawer_sentences.
#Перетворіть рядок у нижній регістр.
print(adwentures_of_tom_sawer_sentences[3])
print(adwentures_of_tom_sawer_sentences[3].lower())

# task 09
#""" Перевірте чи починається якесь речення з "By the time".
# Перебираємо кожне речення в списку від першого до останнього
for sentence in adwentures_of_tom_sawer_sentences:
    if sentence.startswith("By the time"):
        print(f"Знайдено речення: {sentence}")


# task 10
#""" Виведіть кількість слів останнього речення з adwentures_of_tom_sawer_sentences.

print(len(adwentures_of_tom_sawer_sentences[-1].split()))

#new_adwentures_of_tom_sawer_sentences = adwentures_of_tom_sawer_sentences[-1].split()
#print(len(new_adwentures_of_tom_sawer_sentences))








