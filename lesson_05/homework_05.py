# task 1. Знайдіть всі унікальні елементи в списку small_list
small_list = [3, 1, 4, 5, 2, 5, 3]
unique_elements=list(set(small_list))
print(f"{unique_elements}")

# task 2. Знайдіть середнє арифметичне всіх елементів у списку small_list
ser_arifmetychne=sum(small_list)/len(small_list)
print(f"{ser_arifmetychne:.2f}")

# task 3. Перевірте, чи є в списку big_list дублікати
big_list = [3, 5, -2, -1, -3, 0, 1, 4, 5, 2]
if len(big_list)==set(big_list):
    print(f"Дублікатів немає!")
else: print(f"Є дублікати!!!")

# task 4. Знайдіть ключ з максимальним значенням у словнику add_dict
base_dict = {'contry':'Ukraine', 'continent': 'Europe', 'size': 123}
add_dict = {"a":1, "b":2, "c":2, "d":3, 'size': 12}

max_key_add_dict=max(add_dict, key=add_dict.get)
print(f"{max_key_add_dict}")
# task 5. Створіть новий словник, в якому ключі та значення base_dict будуть
# замінені місцями ({'Ukraine':'contry'...})
inverted_base_dict={}
for key, value in base_dict.items():
    inverted_base_dict[value]=key
print(f"{inverted_base_dict}")

# task 6. Об'єднайте два словника base_dict та add_dict  в новий словник sum_dict
# Якщо ключі збігаються, то перетворіть значення в строку та об'єднайте їх
sum_dict = {}
for key, value in base_dict.items():
    sum_dict[key]=value
for key, value in add_dict.items():
    if key in sum_dict: #перевіряємо чи є ключ у sum_dict
        sum_dict[key]=str(sum_dict[key])+str(value) #об'єднуємо два значення з однаковими ключами
    else:
        sum_dict[key]=value
print(f"{sum_dict}")   
# task 7.
line = "Створіть список з всіх символів, які входять у заданий рядок"
char_list=list(line)
print(f"{char_list}")

# task 8. Обчисліть суму елементів двох змінних через sum()
value_1  = [1, 2, 3, 4, 5]
value_2 = (4, 6, 5, 10)
total_sum=sum(value_1)+sum(value_2)
print(f"{total_sum}")