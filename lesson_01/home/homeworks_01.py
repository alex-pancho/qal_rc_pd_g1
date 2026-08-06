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
print("Кількість бананів:", banana,)


# task 04 == виправте назви змінних

storona_1 = 1
storona_2 = 2
storona_3 = 3
storona_4 = 4

# task 05 == Порахуйте периметр фігури з task 04
# та виведіть його для користувача

print()
perimetery = storona_1 + storona_2 + storona_3 + storona_4
print(f"Периметр фігури: {perimetery}")


"""
1 марку із серії «Звірі» вона подарувала подружці. 
Скільки марок лишилось у Оксани?
"""
art = 20
animals = 7
art_gift = 5
animals_gift = 1
total_art = art - art_gift
total_animals = animals - animals_gift
total_left = total_animals + total_art
print(f"У Оксани залишилось {total_left} марок, з яких {total_art} марок із серії «Мистецтво» та {total_animals} марок із серії «Звірі».")

# task 07
"""
У саду посадили 4 яблуні. Груш на 5 більше яблунь, а слив - на 2 менше.
Скільки всього дерев посадили в саду?
"""
apples = 4
pears = apples + 5
plums = apples - 2
total_trees = apples + pears + plums
print(f"Всього дерев посадили в саду: {total_trees}")


# task 08
"""
До обіда температура повітря була на 5 градусів вище нуля.
Після обіду температура опустилася на 10 градусів.
Надвечір потепліло на 4 градуси. Яка температура надвечір?
"""
temperature_before = 5
temperature_after = temperature_before - 10
temperature_later = temperature_after + 4
print(f"Температура надвечір: {temperature_later} градусів")

# task 09
"""
Взагалі у театральному гуртку - 24 хлопчики, а дівчаток - вдвічі менше.
1 хлопчик захворів та 2 дівчинки не прийшли сьогодні.
Скількі сьогодні дітей у театральному гуртку?
"""
boys = 24
girls = boys//2
boys_today = boys - 1
girls_today = girls - 2
total_children = boys_today + girls_today
print(f"Сьгодні прийшло {total_children} дітей у театральний гурток")


# task 10
"""
Перша книжка коштує 8 грн., друга - на 2 грн. дороже,
а третя - як половина вартості першої та другої разом.
Скільки будуть коштувати усі книги, якщо купити по одному примірнику?
"""

book_1 = 8
book_2 = book_1 + 2
book_3 = ((book_1 + book_2) // 2)
books_together = book_1 + book_2 + book_3
print(f"Три книжки разом коштують {books_together} гривень")