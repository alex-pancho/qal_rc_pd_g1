print("task 1")
print("Hello", end = " ")
print("world!")
print("task 2")
print(f"hello world!")
print("task 3")
apples = 2
banana = apples + 4
print(f"apples: {apples}, banana: {banana}")
print("task 4")
storona_1 = 1
storona_2 = 2
storona_3 = 3
storona_4 = 4
print("task 5")
perimetr = storona_1 + storona_2 + storona_3 + storona_4
print(f"perimetr: {perimetr}")  
print("task 6")
#Oksana has 20 stamps from the art series and 7 stamps from the nature series. She wants to give 5 stamps from the art series and 1 stamp from the nature series to her friend. How many stamps will Oksana have left after giving the stamps to her friend?
#Oksana starts with 20 stamps from the art series and 7 stamps from the nature series. She gives away 5 stamps from the art series and 1 stamp from the nature series.
art = 20
nature = 7
art_given = 5
nature_given = 1
art_left = art - art_given
nature_left = nature - nature_given
total_left = art_left + nature_left
print(total_left)
print("task 7")
#У саду посадили 4 яблуні. Груш на 5 більше яблунь, а слив - на 2 менше.
#Скільки всього дерев посадили в саду?
груші = 4 + 5
сливи = 4 - 2
total_trees = 4 + груші + сливи
print(total_trees)
print("task 8")
#До обіда температура повітря була на 5 градусів вище нуля.
#Після обіду температура опустилася на 10 градусів.
#Надвечір потепліло на 4 градуси. Яка температура надвечір?
До_обіда_температура = 5
Після_обіду_температура = До_обіда_температура - 10
температура_надвечір = Після_обіду_температура + 4
print(температура_надвечір)
print(" task 9")
#Взагалі у театральному гуртку - 24 хлопчики, а дівчаток - вдвічі менше.
#1 хлопчик захворів та 2 дівчинки не прийшли сьогодні.
#Скількі сьогодні дітей у театральному гуртку?
хлопчики = 24
дівчатка = хлопчики / 2
хлопчики_сьогодні = хлопчики - 1
дівчатка_сьогодні = дівчатка - 2
total_children = хлопчики_сьогодні + дівчатка_сьогодні
print(total_children)
print("task 10")
#Перша книжка коштує 8 грн., друга - на 2 грн. дороже,
#а третя - як половина вартості першої та другої разом.
#Скільки будуть коштувати усі книги, якщо купити по одному примірнику?
book_1 = 8
book_2 = book_1 + 2
book_3 = (book_1 + book_2) / 2
total_cost = book_1 + book_2 + book_3
print(total_cost)
