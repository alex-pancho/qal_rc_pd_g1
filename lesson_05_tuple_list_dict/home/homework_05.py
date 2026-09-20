# task 1. Знайдіть всі унікальні елементи в списку small_list
small_list = [3, 1, 4, 5, 2, 5, 3]
unique_elements = set(small_list)
print("Унікальні елементи в списку small_list:", unique_elements)


# task 2. Знайдіть середнє арифметичне всіх елементів у списку small_list
serdne_arifm = sum(small_list)/len(small_list)
print("Середнє арифметичне:", serdne_arifm)

# task 3. Перевірте, чи є в списку big_list дублікати
big_list = [3, 5, -2, -1, -3, 0, 1, 4, 5, 2]
if len(big_list) != len(set(big_list)):
    print("У списку big_list є дублікати.")
else:
    print("У списку big_list немає дублікатів.")

# task 4. Знайдіть ключ з максимальним значенням у словнику add_dict
base_dict = {'contry':'Ukraine', 'continent': 'Europe', 'size': 123}
add_dict = {"a":1, "b":2, "c":2, "d":3, 'size': 12}
print("Ключ з максимальним значенням у словнику add_dict:", max(add_dict, key=add_dict.get))


# task 5. Створіть новий словник, в якому ключі та значення base_dict будуть
# замінені місцями ({'Ukraine':'contry'...})
new_dict = {v: k for k, v in base_dict.items()}
print("Новий словник з перевернутими ключами та значеннями:", new_dict)

# task 6. Об'єднайте два словника base_dict та add_dict  в новий словник sum_dict
# Якщо ключі збігаються, то перетворіть значення в строку та об'єднайте їх
sum_dict = {}
base_dict = {'contry':'Ukraine', 'continent': 'Europe', 'size': 123}
add_dict = {"a":1, "b":2, "c":2, "d":3, 'size': 12}
sum_dict = base_dict.copy()

for key, value in add_dict.items():
    if key in sum_dict:
        sum_dict[key] = str(sum_dict[key]) + str(value)
    else:
        sum_dict[key] = value
        print("Об'єднаний словник sum_dict:", sum_dict)


# task 7.
line = "Створіть список з всіх символів, які входять у заданий рядок"
symbols = list(line)
print("Список символів з рядка:", symbols)

# task 8. Обчисліть суму елементів двох змінних через sum()
value_1  = [1, 2, 3, 4, 5]
value_2 = (4, 6, 5, 10)
print("Сума елементів value_1 та value_2:", sum(value_1) + sum(value_2))
