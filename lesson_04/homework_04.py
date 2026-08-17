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

print("task 01")
umova1=""" Дані у строці adwentures_of_tom_sawer розбиті випадковим чином, через помилку. Треба замінити кінець абзацу на пробіл .replace("\n", " ")"""
print(f"{umova1}")
adwentures_of_tom_sawer=adwentures_of_tom_sawer.replace("\n"," ")
print(f"{adwentures_of_tom_sawer}")


print("task 02")
umova2=""" Замініть .... на пробіл
"""
print(f"{umova2}")
adwentures_of_tom_sawer=adwentures_of_tom_sawer.replace("...."," ")
print(f"{adwentures_of_tom_sawer}")

print("task 03")

umova3=""" Зробіть так, щоб у тексті було не більше одного пробілу між словами.
"""
print(f"{umova3}")
adwentures_of_tom_sawer=" ".join(adwentures_of_tom_sawer.split())
print(f"{adwentures_of_tom_sawer}")

print("task 04")
umova4=""" Виведіть, скількі разів у тексті зустрічається літера "h"
"""
print(f"{umova4}")
count_h=adwentures_of_tom_sawer.count("h")
print(f"У тексті h зустрічається {count_h} разів.")

print("task 05")

umova5=""" Виведіть, скільки слів у тексті починається з Великої літери?
підказка - порахувати кожну велику літеру напр, .count("A") і їх сумму
"""
print(f"{umova5}")
count_litter_upper=0
for upper_letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    count_litter_upper= adwentures_of_tom_sawer.count(upper_letter)+count_litter_upper
print(f"У тексті зустрічається {count_litter_upper} раз.")

print("task 06")
umova6=""" Виведіть позицію, на якій слово Tom зустрічається вдруге
"""
print(f"{umova6}")
posiciya_Tom_first=adwentures_of_tom_sawer.find("Tom")
posiciya_Tom_second=adwentures_of_tom_sawer.find("Tom",posiciya_Tom_first+1)
print(f" Позиція слова Tom, що вдруге зустрічається у тексті є {posiciya_Tom_second}")

print("task 07")
umova7=""" Розділіть змінну adwentures_of_tom_sawer по кінцю речення.
Збережіть результат у змінній adwentures_of_tom_sawer_sentences
"""
print(f"{umova7}")
adwentures_of_tom_sawer_sentences =adwentures_of_tom_sawer.split(". ") # None
print(f"{adwentures_of_tom_sawer_sentences}")

print("task 08")
umova8=""" Виведіть четверте речення з adwentures_of_tom_sawer_sentences.
Перетворіть рядок у нижній регістр.
"""
print(f"{umova8}")
adwentures_of_tom_sawer_sentences_new=adwentures_of_tom_sawer_sentences[3].lower()
print(f"{adwentures_of_tom_sawer_sentences_new}\n")

print("task 09")
umova9=""" Перевірте чи починається якесь речення з "By the time".
"""
print(f"{umova9}")
check=False
for by_the_time in adwentures_of_tom_sawer_sentences:
    if by_the_time.startswith("By the time"):
        check=True
if check==True:
    print(f"Таке речення є, що починаєтьс на By the time")
else: print(f"Немає жодного речення яке б починалося на By the time")

print("task 10")
umova10=""" Виведіть кількість слів останнього речення з adwentures_of_tom_sawer_sentences.
"""
print(f"{umova10}")
last_sentence = adwentures_of_tom_sawer_sentences[-1]
adwentures_of_tom_sawer_sentences_count_last=len(last_sentence.split())
print(f"Кількість слів в останньому реченні {adwentures_of_tom_sawer_sentences_count_last}")