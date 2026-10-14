# task 1. Знайдіть всі унікальні елементи в списку small_list
small_list = [3, 1, 4, 5, 2, 5, 3]
unic_element = set(small_list)
print("unic element", unic_element)


# task 2. Знайдіть середнє арифметичне всіх елементів у списку small_list
average = sum(small_list) / len(small_list)

# task 3. Перевірте, чи є в списку big_list дублікати
big_list = [3, 5, -2, -1, -3, 0, 1, 4, 5, 2]
has_duplicates = len(big_list) != len(set(big_list))
print(has_duplicates)

# task 4. Знайдіть ключ з максимальним значенням у словнику add_dict
base_dict = {'contry':'Ukraine', 'continent': 'Europe', 'size': 123}
add_dict = {"a":1, "b":2, "c":2, "d":3, 'size': 12}
max_len = max(add_dict, key=add_dict.get)
print(max_len)

# task 5. Створіть новий словник, в якому ключі та значення base_dict будуть
# замінені місцями ({'Ukraine':'contry'...})
reversed_dict = {}
for k, v in base_dict.items():
        reversed_dict[v] = k

print(reversed_dict)

# task 6. Об'єднайте два словника base_dict та add_dict  в новий словник sum_dict
# Якщо ключі збігаються, то перетворіть значення в строку та об'єднайте їх
sum_dict = base_dict.copy()

for key, value in add_dict.items():
        if key in sum_dict:
                sum_dict[key] = str(sum_dict[key]) + str(value)
        else:
                sum_dict[key] = value

print(sum_dict)

# task 7.
line = "Створіть список з всіх символів, які входять у заданий рядок"
new_list = list(line)
print(new_list)

# task 8. Обчисліть суму елементів двох змінних через sum()
value_1  = [1, 2, 3, 4, 5]
value_2 = (4, 6, 5, 10)

sum_values = sum(value_1) + sum(value_2)
print(sum_values)