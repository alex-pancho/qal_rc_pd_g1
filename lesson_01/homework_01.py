# task 01 == Виправте синтаксичні помилки
print("Hello", end = " ")
print("world!")

# task 02  == Виправте назви змінних, щоб текст виводався
hello = "Hello"
world = "world"
print(f"{hello} {world}!")

# task 03 == Зробіть так, щоб кількість бананів була
# завжди на чотири штуки більша, ніж яблук
apples = 2
banana = apples+4


# task 04 == виправте назви змінних
storona_1 = 1
storona_2 = 2
storona_3 = 3
storona_4 = 4

# task 05 == Порахуйте периметр фігури з task 04
# та виведіть його для користувача
perimetery = storona_1 + storona_2 + storona_3 + storona_4
print(f"task 5: Perymetry is {perimetery}")


"""
    # Задачі 06 -10:
    # Переведіть задачі з книги "Математика, 2 клас"
    # на мову пітон і виведіть відповідь, так, щоб було
    # зрозуміло дитині, що навчається в другому класі
"""

# task 06
"""
У Оксани було 20 марок із серії «Мистецтво» 
і 7 марок із серії «Звірі».
5 марок із серії «Мистецтво» та
1 марку із серії «Звірі» вона подарувала подружці. 
Скільки марок лишилось у Оксани?
"""
#Define variables
art_marks_total=20
animal_marks_total=7
art_marks_gift_for_friend=5
animal_marks_gift_for_friend=1
#calculate result
remain_art_marks=art_marks_total-art_marks_gift_for_friend
remain_animal_marks=animal_marks_total-animal_marks_gift_for_friend
remain_total=remain_art_marks+remain_animal_marks
#Output
print(f"Oxana has {art_marks_total} Art marks and {animal_marks_total} Animal marks")
print(f"{art_marks_gift_for_friend} Art marks and {animal_marks_gift_for_friend} Animal marks she gift for friend")
print(f"Remain Art Marks={remain_art_marks}")
print(f"Remain Animal Marks={remain_animal_marks}")
print(f"Remain total {remain_total}")
# task 07
"""
У саду посадили 4 яблуні. Груш на 5 більше яблунь, а слив - на 2 менше.
Скільки всього дерев посадили в саду?
"""
apple_tree=4
pear_tree_cof=5
plum_tre_cof=2

pear_tree=apple_tree+pear_tree_cof
plum_tree=apple_tree-plum_tre_cof
total_tree=apple_tree+pear_tree+plum_tree

print(f"At the garden was {apple_tree} Apple treas, pear treas gross for {pear_tree_cof},and plum treas less for {plum_tre_cof}. How many treas at the garden")
print(f"Apple tree {apple_tree}")
print(f"Pear tree {pear_tree}")
print(f"Plum tree {plum_tree}")
print(f"Answer: {total_tree}")
# task 08
"""
До обіда температура повітря була на 5 градусів вище нуля.
Після обіду температура опустилася на 10 градусів.
Надвечір потепліло на 4 градуси. Яка температура надвечір?
"""
#define variables
zerro_temp=0
morning_change=5
day_change=10
evening_chamge=4
 #calculate
morning_temp=zerro_temp+5
day_temp=morning_temp-day_change
evening_temp=day_temp+evening_chamge
#print
print(f"Morning temp is {morning_temp},day temp is {day_temp}, Evening temp is {evening_temp}")
# task 09
"""
Взагалі у театральному гуртку - 24 хлопчики, а дівчаток - вдвічі менше.
1 хлопчик захворів та 2 дівчинки не прийшли сьогодні.
Скількі сьогодні дітей у театральному гуртку?
"""
#define variables
boys=24
girl_cof=2
boys_out=1
girls_out=2
#calculate
girls=boys/girl_cof
boys_today=boys-boys_out
girls_today=girls-girls_out
children_today=boys_today+girls_today
#print
print(f"boys are {boys},girls are les in {girl_cof} times {boys_out} boy ill, {girls_out} girls doesnot came. How many children today?")
print(f"answer: {children_today}")
# task 10
"""
Перша книжка коштує 8 грн., друга - на 2 грн. дороже,
а третя - як половина вартості першої та другої разом.
Скільки будуть коштувати усі книги, якщо купити по одному примірнику?
"""
#deefine functions
def second_book_calc(first_b,increce):
    return first_b+increce
def threed_book_calc(first_b,second_b,cof):
    return (first_b+second_b)/cof
def total_books_calc(first_b,second_b,threed_b):
    return first_b+second_b+threed_b
#define variables
first_book=8
increce_index=2
devide_index=2
#calculate
second_book=second_book_calc(first_book,increce_index)
threed_book=threed_book_calc(first_book,second_book,devide_index)
total_books=total_books_calc(first_book,second_book,threed_book)
#print
print(f"first book cost {first_book}UAH,Second book on {increce_index}UAH more exp. Thread book costs as half of first with second. How much all books cost?")
print(f"First book: {first_book}UAH")
print(f"Second book: {second_book}UAH")
print(f"Threedß book: {threed_book}UAH")
print(f"Answer: All books costs {total_books}UAH")

