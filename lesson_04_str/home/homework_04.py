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

adwentures_of_tom_sawer_copy_orig = adwentures_of_tom_sawer


# task 01 ==
""" Дані у строці adwentures_of_tom_sawer розбиті випадковим чином, через помилку.
треба замінити кінець абзацу на пробіл .replace("\n", " ")"""

adwentures_of_tom_sawer = adwentures_of_tom_sawer.rstrip("\n").replace("\n", " ")
print(adwentures_of_tom_sawer)


# task 02 ==
""" Замініть .... на пробіл
"""
adwentures_of_tom_sawer = adwentures_of_tom_sawer.replace("....", " ")
print(adwentures_of_tom_sawer)

# task 03 ==
""" Зробіть так, щоб у тексті було не більше одного пробілу між словами.
"""
adwentures_of_tom_sawer = adwentures_of_tom_sawer.replace("   ", " ")
adwentures_of_tom_sawer = adwentures_of_tom_sawer.replace("  ", " ")
print(adwentures_of_tom_sawer)


# task 04
""" Виведіть, скількі разів у тексті зустрічається літера "h"
"""
print(adwentures_of_tom_sawer.count("h"))

# task 05
""" Виведіть, скільки слів у тексті починається з Великої літери?
підказка - порахувати кожну велику літеру напр, .count("A") і їх сумму
"""
print(
    adwentures_of_tom_sawer.count("A") + adwentures_of_tom_sawer.count("B") +
    adwentures_of_tom_sawer.count("C") + adwentures_of_tom_sawer.count("D") +
    adwentures_of_tom_sawer.count("E") + adwentures_of_tom_sawer.count("F") +
    adwentures_of_tom_sawer.count("G") + adwentures_of_tom_sawer.count("H") +
    adwentures_of_tom_sawer.count("I") + adwentures_of_tom_sawer.count("J") +
    adwentures_of_tom_sawer.count("K") + adwentures_of_tom_sawer.count("L") +
    adwentures_of_tom_sawer.count("M") + adwentures_of_tom_sawer.count("N") +
    adwentures_of_tom_sawer.count("O") + adwentures_of_tom_sawer.count("P") +
    adwentures_of_tom_sawer.count("Q") + adwentures_of_tom_sawer.count("R") +
    adwentures_of_tom_sawer.count("S") + adwentures_of_tom_sawer.count("T") +
    adwentures_of_tom_sawer.count("U") + adwentures_of_tom_sawer.count("V") +
    adwentures_of_tom_sawer.count("W") + adwentures_of_tom_sawer.count("X") +
    adwentures_of_tom_sawer.count("Y") + adwentures_of_tom_sawer.count("Z")
)

# task 06
""" Виведіть позицію, на якій слово Tom зустрічається вдруге
"""

first_tom = adwentures_of_tom_sawer.find("Tom")

second_tom = adwentures_of_tom_sawer.find("Tom", first_tom + 1)

print(second_tom)

# task 07
""" Розділіть змінну adwentures_of_tom_sawer по кінцю речення.
Збережіть результат у змінній adwentures_of_tom_sawer_sentences
"""
adwentures_of_tom_sawer_sentences = None

adwentures_of_tom_sawer_sentences = adwentures_of_tom_sawer.split(". ")
print(adwentures_of_tom_sawer_sentences)

# task 08
""" Виведіть четверте речення з adwentures_of_tom_sawer_sentences.
Перетворіть рядок у нижній регістр.
"""
print(adwentures_of_tom_sawer_sentences[3].lower())

# task 09
""" Перевірте чи починається якесь речення з "By the time".
"""
find_by_the_time = any(sentence.startswith("By the time") for sentence in adwentures_of_tom_sawer_sentences)
print(find_by_the_time)

# task 10
""" Виведіть кількість слів останнього речення з adwentures_of_tom_sawer_sentences.
"""

last_sentence = adwentures_of_tom_sawer_sentences[-1]
word_count = len(last_sentence.split())
print(word_count)