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
hour after hour.  """

# УВАГА! Перезаписуйте вміст змінної adwentures_of_tom_sawer у завданнях 01-03

# task 01 ==
""" Дані у строці adwentures_of_tom_sawer розбиті випадковим чином, через помилку.
треба замінити кінець абзацу на пробіл .replace("\n", " ")"""
new_adwentures_of_tom_sawer = adwentures_of_tom_sawer.replace("\n", " ")
print(new_adwentures_of_tom_sawer)
# task 02 ==
""" Замініть .... на пробіл
"""
new_adwentures_of_tom_sawer_2 = adwentures_of_tom_sawer.replace("....", " ")
print(new_adwentures_of_tom_sawer_2)
# task 03 ==
""" Зробіть так, щоб у тексті було не більше одного пробілу між словами.
"""
new_adwentures_of_tom_sawer_3 = adwentures_of_tom_sawer.replace("  ", " ")
print(new_adwentures_of_tom_sawer_3)


# task 04
""" Виведіть, скількі разів у тексті зустрічається літера "h"
"""
kilkist = adwentures_of_tom_sawer.count("h")
print(kilkist)

# task 05
""" Виведіть, скільки слів у тексті починається з Великої літери?
підказка - порахувати кожну велику літеру напр, .count("A") і їх сумму
"""
kilkist_A = adwentures_of_tom_sawer.count("A")
kilkist_B = adwentures_of_tom_sawer.count("B")
kilkist_T = adwentures_of_tom_sawer.count("T")
print(kilkist_A + kilkist_B + kilkist_T)

# task 06
""" Виведіть позицію, на якій слово Tom зустрічається вдруге
"""
position = adwentures_of_tom_sawer.find("Tom")
if position != 1:
    position = adwentures_of_tom_sawer.find("Tom", position + 1)
print(position)


# task 07
""" Розділіть змінну adwentures_of_tom_sawer по кінцю речення.
Збережіть результат у змінній adwentures_of_tom_sawer_sentences
"""
adwentures_of_tom_sawer_sentences = (adwentures_of_tom_sawer.split('.'))
print(adwentures_of_tom_sawer_sentences)

# task 08
""" Виведіть четверте речення з adwentures_of_tom_sawer_sentences.
Перетворіть рядок у нижній регістр.
"""
text = """By the time Ben was fagged out, Tom had traded the next chance to Billy Fisher for
a kite, in good repair;
and when he played
out, Johnny Miller bought
in for a dead rat and a string to swing it with—and so on, and so on,
hour after hour. And when the middle of the afternoon came, from being a
poor poverty, stricken boy in the .... morning, Tom was literally
rolling in wealth."""
little = text.lower()
print(little)

# task 09
""" Перевірте чи починається якесь речення з "By the time".
"""
print(adwentures_of_tom_sawer[3].startswith("By the time"))


# task 10
""" Виведіть кількість слів останнього речення з adwentures_of_tom_sawer_sentences.
"""
text_2="""And when the middle of the afternoon came, from being a
poor poverty, stricken boy in the .... morning, Tom was literally
rolling in wealth."""
words = text_2.split()
print(len(words))
