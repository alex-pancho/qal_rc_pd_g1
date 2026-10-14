dwentures_of_tom_sawer = """\
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
text = adwentures_of_tom_sawer.replace("\n", " ")

# task 02 ==
""" Замініть .... на пробіл
"""
text = text.replace("....", " ")

# task 03 ==
""" Зробіть так, щоб у тексті було не більше одного пробілу між словами.
"""
words = text.split()
text = " ".join(words)

# task 04
""" Виведіть, скількі разів у тексті зустрічається літера "h"
"""
print(text.count("h"))

# task 05
""" Виведіть, скільки слів у тексті починається з Великої літери?
підказка - порахувати кожну велику літеру напр, .count("A") і їх сумму
"""
capital_count = (
    text.count("A") + text.count("B") + text.count("C") + text.count("D") +
    text.count("E") + text.count("F") + text.count("G") + text.count("H") +
    text.count("I") + text.count("J") + text.count("K") + text.count("L") +
    text.count("M") + text.count("N") + text.count("O") + text.count("P") +
    text.count("Q") + text.count("R") + text.count("S") + text.count("T") +
    text.count("U") + text.count("W") + text.count("X") +
    text.count("Y") + text.count("Z")
)
print(capital_count)

# task 06
""" Виведіть позицію, на якій слово Tom зустрічається вдруге
"""
first = text.find("Tom")
second = text.find("Tom", first + 1)
print(second)

# task 07
""" Розділіть змінну adwentures_of_tom_sawer по кінцю речення.
Збережіть результат у змінній adwentures_of_tom_sawer_sentences
"""
adwentures_of_tom_sawer_sentences = None
adwentures_of_tom_sawer_sentences = text.split(".")

# task 08
""" Виведіть четверте речення з adwentures_of_tom_sawer_sentences.
Перетворіть рядок у нижній регістр.
"""
print(adwentures_of_tom_sawer_sentences[3].lower())

# task 09
""" Перевірте чи починається якесь речення з "By the time".
"""

    if adwentures_of_tom_sawer_sentences.startswith("By the time"):
        result = True

print(result)

# task 10
""" Виведіть кількість слів останнього речення з adwentures_of_tom_sawer_sentences.
"""
word_count = len(adwentures_of_tom_sawer_sentences.split())
print(word_count)