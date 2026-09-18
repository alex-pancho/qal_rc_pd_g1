# task 1. Знайдіть всі унікальні елементи в списку small_list
small_list = [3, 1, 4, 5, 2, 5, 3]

small_list_unique = list(set(small_list))
print(small_list_unique)

unique_preserve_order = list(dict.fromkeys(small_list))
print(unique_preserve_order)  # [3, 1, 4, 5, 2]

# task 2. Знайдіть середнє арифметичне всіх елементів у списку small_list
small_list_mean = sum(small_list) / len(small_list)
print(small_list_mean)

import statistics
small_list_mean_stat = statistics.mean(small_list)
print(small_list_mean_stat)


# task 3. Перевірте, чи є в списку big_list дублікати
big_list = [3, 5, -2, -1, -3, 0, 1, 4, 5, 2]
has_duplicates = len(big_list) != len(set(big_list))
print(has_duplicates)
from collections import Counter
duplicates = [item for item, count in Counter(big_list).items() if count > 1]
print(duplicates)


# task 4. Знайдіть ключ з максимальним значенням у словнику add_dict
base_dict = {'contry':'Ukraine', 'continent': 'Europe', 'size': 123}
add_dict = {"a":1, "b":2, "c":2, "d":3, 'size': 12}

add_dict = {"a": 1, "b": 2, "c": 2, "d": 3, "size": 12}

max_key = max(add_dict, key=add_dict.get)
print(max_key)
max_key, max_value = max(add_dict.items(), key=lambda item: item[1])
print(f"Ключ: {max_key}, Значення: {max_value}")
# task 5. Створіть новий словник, в якому ключі та значення base_dict будуть
# замінені місцями ({'Ukraine':'contry'...})
base_dict = {'contry': 'Ukraine', 'continent': 'Europe', 'size': 123}

# Генератор словника
inverted_dict = {value: key for key, value in base_dict.items()}

print(inverted_dict)

# task 6. Об'єднайте два словника base_dict та add_dict  в новий словник sum_dict
# Якщо ключі збігаються, то перетворіть значення в строку та об'єднайте їх
sum_dict = {}
sum_dict = base_dict.copy()

for key, value in add_dict.items():
    if key in sum_dict:
        # Збіг ключів: перетворюємо в строки та об'єднуємо
        sum_dict[key] = str(sum_dict[key]) + str(value)
    else:
        sum_dict[key] = value

print(sum_dict)

# task 7.
line = "Створіть список з всіх символів, які входять у заданий рядок"
char_list = list(line)

print(char_list)

# task 8. Обчисліть суму елементів двох змінних через sum()
value_1  = [1, 2, 3, 4, 5]
value_2 = (4, 6, 5, 10)

total_sum = sum(value_1 + list(value_2))

print(total_sum)
total_sum = sum([*value_1, *value_2])

print(total_sum)