# task 01 == Виправте синтаксичні помилки
print("Hello", end = " ")
print("world!")
# task 02  == Виправте назви змінних, щоб текст виводався
hello = "Hello"
world = "world"
print(f"helo word!")
# task 03 == Зробіть так, щоб кількість бананів була
# завжди на чотири штуки більша, ніж яблук
apples = 2
banana = apples + 4  # код тут
print (banana)
# task 04 == виправте назви змінних
storona_1 = 1
storona_2 = 2
storona_3 = 3
storona_4 = 4
print(storona_1, storona_2, storona_3, storona_4)
# task 05 == Порахуйте периметр фігури з task 04
# та виведіть його для користувача
perimetery = storona_1 + storona_2 + storona_3 + storona_4
print(perimetery)


# Задачі 06 -10:
    # Переведіть задачі з книги "Математика, 2 клас"
    # на мову пітон і виведіть відповідь, так, щоб було
    # зрозуміло дитині, що навчається в другому класі


# task 06

#У Оксани було 20 марок із серії «Мистецтво» 
#і 7 марок із серії «Звірі».
#5 марок із серії «Мистецтво» та
#1 марку із серії «Звірі» вона подарувала подружці. 
#Скільки марок лишилось у Оксани?


marks_art_oks = 20
marks_animals_oks = 7
marks_art_given = 5
marks_animals_given = 1

marks_left = (marks_art_oks - marks_art_given) + (marks_animals_oks - marks_animals_given)
print(marks_left)

# task 07
"""
У саду посадили 4 яблуні. Груш на 5 більше яблунь, а слив - на 2 менше.
Скільки всього дерев посадили в саду?
"""
trees_apples = 4
trees_pears = trees_apples + 5
trees_plums = trees_apples - 2  
trees_total = trees_apples + trees_pears + trees_plums
print(trees_total)

# task 08
"""
До обіда температура повітря була на 5 градусів вище нуля.
Після обіду температура опустилася на 10 градусів.
Надвечір потепліло на 4 градуси. Яка температура надвечір?
"""
temp_am = 5
temp_pm = temp_am - 10
temp_evening = temp_pm + 4
print(temp_evening)

# task 09
"""
Взагалі у театральному гуртку - 24 хлопчики, а дівчаток - вдвічі менше.
1 хлопчик захворів та 2 дівчинки не прийшли сьогодні.
Скількі сьогодні дітей у театральному гуртку?
"""
boys_total = 24
girls_total = boys_total // 2
boys_present = boys_total - 1
girls_present = girls_total - 2
children_present = boys_present + girls_present
print(children_present) 

# task 10
"""
Перша книжка коштує 8 грн., друга - на 2 грн. дороже,
а третя - як половина вартості першої та другої разом.
Скільки будуть коштувати усі книги, якщо купити по одному примірнику?
"""
book_1_price = 8
book_2_price = book_1_price + 2
book_3_price = (book_1_price + book_2_price) / 2
total_price = book_1_price + book_2_price + book_3_price
print(total_price, "грн")

"""
Виведіть результат віднімання 5 від 5 під заголовком # Віднімання за допомогою print().
Виведіть результат множення 3 на 5 під заголовком # Множення.

"""
# Віднімання
print(5 - 5)
# Множення
print(3 * 5)

"""
У Python змінна дозволяє посилатися на значення за допомогою імені. 
Щоб створити змінну x із значенням 5, використовуйте =, як у цьому прикладі:
x = 5
Тепер ви можете використовувати ім'я цієї змінної, x, замість фактичного значення, 5.
Пам'ятайте, що = у Python означає присвоювання, а не перевірку рівності! 
Спробуйте це в вправі, замінивши ____ своїм кодом.

Створіть змінну savings із значенням 100.
Перевірте цю змінну, ввівши print(savings) у скрипті.
"""
# Створіть змінну savings із значенням 100.
savings = 100
# Перевірте цю змінну, ввівши print(savings)
print(savings)

"""
Обчислення із змінними
Замість обчислення з фактичними значеннями, ви можете використовувати змінні.

Скільки грошей ви заощадите через чотири місяці, якщо щомісяця заощаджуватимете 10 доларів?

Створіть змінну monthly_savings, рівну 10, та num_months, рівну 4.
Помножте monthly_savings на num_months і присвойте результат new_savings.

"""
# Створіть змінну monthly_savings, рівну 10, та num_months, рівну 4


# Помножте monthly_savings на num_months і збережіть результат в змінну new_savings

# Виведіть new_savings
monthly_savings = 10
num_months = 4
new_savings = monthly_savings * num_months
print(new_savings)  