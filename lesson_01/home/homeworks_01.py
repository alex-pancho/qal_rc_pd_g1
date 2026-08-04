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
side_1 = 1
side_2 = 2
side_3 = 3
side_4 = 4

# task 05 == Порахуйте периметр фігури з task 04
# та виведіть його для користувача
perimetery = side_1 + side_2 + side_3 + side_4
print(perimetery)


# Задачі 06 -10:
# Переведіть задачі з книги "Математика, 2 клас"
# на мову пітон і виведіть відповідь, так, щоб було
# зрозуміло дитині, що навчається в другому класі

# task 06
# У Оксани було 20 марок із серії «Мистецтво» 
# і 7 марок із серії «Звірі».
# 5 марок із серії «Мистецтво» та
# 1 марку із серії «Звірі» вона подарувала подружці. 
# Скільки марок лишилось у Оксани?
art_stamps_start = 20
beast_stamps_start = 7
art_stamps_given = 5
beast_stamps_given = 1
art_stamps_left = art_stamps_start - art_stamps_given
beast_stamps_left = beast_stamps_start - beast_stamps_given
total_stamps_left = art_stamps_left + beast_stamps_left
print(total_stamps_left)

# task 07
# У саду посадили 4 яблуні. Груш на 5 більше яблунь, а слив - на 2 менше.
# Скільки всього дерев посадили в саду?
apple_trees = 4
pear_trees = apple_trees + 5
plum_trees = apple_trees - 2
total_trees = apple_trees + pear_trees + plum_trees
print(total_trees)

# task 08
# До обіда температура повітря була на 5 градусів вище нуля.
# Після обіду температура опустилася на 10 градусів.
# Надвечір потепліло на 4 градуси. Яка температура надвечір?
temp = 5       
temp = temp - 10 
temp = temp + 4
print(temp)

# task 09
# Взагалі у театральному гуртку - 24 хлопчики, а дівчаток - вдвічі менше.
# 1 хлопчик захворів та 2 дівчинки не прийшли сьогодні.
# Скількі сьогодні дітей у театральному гуртку?
boys_total = 24
girls_total = boys_total / 2
boys_present = boys_total - 1
girls_present = girls_total - 2
total_children_today = boys_present + girls_present
print(total_children_today)

# task 10
# Перша книжка коштує 8 грн., друга - на 2 грн. дороже,
# а третя - як половина вартості першої та другої разом.
# Скільки будуть коштувати усі книги, якщо купити по одному примірнику?
book1_price = 8
book2_price = book1_price + 2
book3_price = (book1_price + book2_price) / 2
total_price = book1_price + book2_price + book3_price
print(total_price)

