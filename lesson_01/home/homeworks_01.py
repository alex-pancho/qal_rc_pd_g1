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
banana = apples + 4


# task 04 == виправте назви змінних
storona_1 = 1
storona_2 = 2
сторона_3 = 3
сторона_4 = 4

# task 05 == Порахуйте периметр фігури з task 04
# та виведіть його для користувача
perimeter = storona_1 + storona_2 + сторона_3 + сторона_4
print(f"Периметр фігури: {perimeter}")

# task 06
art_stamps = 20
animal_stamps = 7

art_given = 5
animal_given = 1

total_start = art_stamps + animal_stamps
total_given = art_given + animal_given
stamps_left = total_start - total_given

print(f"Спочатку у Оксани було {total_start} марок.")
print(f"Вона подарувала подружці {total_given} марок.")
print(f"У Оксани залишилося {stamps_left} марок.")

# task 07
apple_trees = 4
pear_trees = apple_trees + 5
plum_trees = pear_trees - 2

total_trees = apple_trees + pear_trees + plum_trees

print(f"У саду посадили {apple_trees} яблуні, {pear_trees} груш та {plum_trees} слив.")
print(f"Усього в саду посадили {total_trees} дерев.")

# task 08
temp_start = 5
temp_after_lunch = temp_start - 10
temp_evening = temp_after_lunch + 4

print(f"Спочатку було {temp_start} градусів тепла.")
print(f"Після обіду стало {temp_after_lunch} градусів.")
print(f"Надвечір температура піднялася до {temp_evening} градусів нижче нуля (-1 градус).")

# task 09
boys = 24
girls = boys // 2

boys_absent = 1
girls_absent = 2

present_boys = boys - boys_absent
present_girls = girls - girls_absent
total_children_today = present_boys + present_girls

print(f"У гуртку {boys} хлопчиків і {girls} дівчаток.")
print(f"Сьогодні прийшло {present_boys} хлопчиків та {present_girls} дівчаток.")
print(f"Сьогодні на занятті {total_children_today} дітей.")

# task 10
book1_price = 8
book2_price = book1_price + 2
book3_price = (book1_price + book2_price) // 2

total_cost = book1_price + book2_price + book3_price

print(f"Перша книжка коштує {book1_price} грн, друга — {book2_price} грн, а третя — {book3_price} грн.")
print(f"За всі три книжки разом треба заплатити {total_cost} грн.")
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

# task 07
"""
У саду посадили 4 яблуні. Груш на 5 більше яблунь, а слив - на 2 менше.
Скільки всього дерев посадили в саду?
"""

# task 08
"""
До обіда температура повітря була на 5 градусів вище нуля.
Після обіду температура опустилася на 10 градусів.
Надвечір потепліло на 4 градуси. Яка температура надвечір?
"""

# task 09
"""
Взагалі у театральному гуртку - 24 хлопчики, а дівчаток - вдвічі менше.
1 хлопчик захворів та 2 дівчинки не прийшли сьогодні.
Скількі сьогодні дітей у театральному гуртку?
"""

# task 10
"""
Перша книжка коштує 8 грн., друга - на 2 грн. дороже,
а третя - як половина вартості першої та другої разом.
Скільки будуть коштувати усі книги, якщо купити по одному примірнику?
"""

