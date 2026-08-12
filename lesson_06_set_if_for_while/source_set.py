# set

fruits = {"яблуко", "банан", "апельсин", "apple", "apple", "яблуко"}
print(fruits)

print("apple" in fruits)
print(1 in fruits)
popped_element = fruits.pop()
print(f"Видалений елемент: {popped_element}, Залишок: {fruits}")
fruits.update({"apple"})
fruits.remove("apple") # може бути помилка
print(f"Множина після видалення: {fruits}")


my_set = {1, 2, 3, 4}
add_set = {3, 4, 5, 6, 7}

uni_set = my_set.union(add_set)
# або
# uni_set = my_set | add_set
print(uni_set)

# logical_intersection = my_set.intersection(add_set)
# або
logical_intersection = my_set & add_set
print(logical_intersection)
#
logical_difference_1 = my_set - add_set
print(logical_difference_1)
logical_difference_2 = add_set - my_set
print(logical_difference_2)

# logical_symmetric_difference = set1.symmetric_difference(set2)
# або
logical_symmetric_difference = add_set ^ my_set
print(logical_symmetric_difference)



my_text_set = set("Приклади створення множини в Python з інших типів даних за допомогою")
print(my_text_set)

f_list = ["яблуко", "банан", "апельсин", "apple", "apple"]
set_from_list = set(f_list)
print(set_from_list, len(set_from_list) == len(f_list))

name_1 = "Олександр"
name_2 = "Alex"

ukrainian_letters = set("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'")
name_set = set(name_1.lower())
diff = name_set - ukrainian_letters
print(diff)

name_set_2 = set(name_2.lower())
diff = name_set_2 - ukrainian_letters
print(diff)
