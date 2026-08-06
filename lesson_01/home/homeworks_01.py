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
banana = apples + 4 # код тут


# task 04 == виправте назви змінних
storona_1 = 1
storona_2 = 2
storona_3 = 3
storona_4 = 4

# task 05 == Порахуйте периметр фігури з task 04
# та виведіть його для користувача
perimetery = storona_1 + storona_2 + storona_3 + storona_4
print(perimetery)


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

mark_art_oks= 20
mark_animal_oks = 7
mark_art_gifttofriend = 5
mark_animal_gifttofriend = 1
total_mark_oks = (mark_art_oks - mark_art_gifttofriend) + (mark_animal_oks - mark_animal_gifttofriend)
print(total_mark_oks)

# task 07
"""
У саду посадили 4 яблуні. Груш на 5 більше яблунь, а слив - на 2 менше.
Скільки всього дерев посадили в саду?
"""
tree_apple = 4
tree_pear = tree_apple + 5
tree_plum = tree_apple - 2
tree_total = tree_apple + tree_pear + tree_plum
print(tree_total)

# task 08
"""
До обіда температура повітря була на 5 градусів вище нуля.
Після обіду температура опустилася на 10 градусів.
Надвечір потепліло на 4 градуси. Яка температура надвечір?
"""
before_lunch = 5
after_lunch = before_lunch - 10
evening = after_lunch + 4
print(evening)

# task 09
"""
Взагалі у театральному гуртку - 24 хлопчики, а дівчаток - вдвічі менше.
1 хлопчик захворів та 2 дівчинки не прийшли сьогодні.
Скількі сьогодні дітей у театральному гуртку?
"""
boys = 24
girls = 24 / 2
boys_ill = 1
girls_out = 2
total_today = (boys - boys_ill) + (girls - girls_out)
print(total_today)
# task 10
"""
Перша книжка коштує 8 грн., друга - на 2 грн. дороже,
а третя - як половина вартості першої та другої разом.
Скільки будуть коштувати усі книги, якщо купити по одному примірнику?
"""
book_1 = 8
book_2 = book_1 + 2
book_3 = (book_1 + book_2)/2
total_cost = book_1 + book_2 + book_3
print(total_cost)
