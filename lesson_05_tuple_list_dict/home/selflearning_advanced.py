# -*- coding: utf-8 -*-
# Самостійне вивчення - Поглиблені задачі
# Виконайте завдання та збережіть результати у вказаних змінних

print("=== ПОГЛИБЛЕНІ ЗАДАЧІ ===")

# Task 1. Створіть список з парних чисел від 2 до 20
even_numbers = list(range(2,21,2)) # Ваш код тут
print(f"{even_numbers}")

# Task 2. Відфільтруйте з списку тільки числа більше 10
numbers_list = [5, 12, 8, 15, 3, 18, 7, 20]
filtered_numbers = [x for x in numbers_list if x>10]  # Ваш код тут
print(f"{filtered_numbers}")

# Task 3. Створіть список квадратів непарних чисел від 1 до 9
odd_squares = [x**2 for x in range(1,10) if x % 2 !=0]  # Ваш код тут: [1, 9, 25, 49, 81]
print(f"{odd_squares}")

# Task 4. Об'єднайте два списки без дублікатів
list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
merged_unique = list(set(list1 + list2))  # Ваш код тут
print(f"{merged_unique}")
# Task 5. Створіть кортеж з координатами точок
points = ((0,0), (1,1), (2,2))  # Ваш код тут: ((0,0), (1,1), (2,2))

# Task 6. Розпакуйте кортеж координат
coordinates = (10, 20, 30)
x, y, z = coordinates  # Ваш код тут

# Task 7. Створіть множину голосних літер
vowels = set(['a', 'e', 'i', 'o', 'u'])  # Ваш код тут: {'a', 'e', 'i', 'o', 'u'}
#vowels={'a", 'e', 'i', 'o', 'u'}
# Task 8. Знайдіть унікальні символи у рядку
text = "programming"
unique_chars = set(text)  # Ваш код тут. Множина set прибирає дублікати 
print(f"{unique_chars}")
# Task 9. Створіть множину чисел, які діляться на 3 від 1 до 15
divisible_by_3 = set(range(3,16,3))  # Ваш код тут
print(f"{divisible_by_3}")

# Task 10. Знайдіть симетричну різницю двох множин
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
symmetric_diff = set1.symmetric_difference(set2) # Ваш код тут. Знак симетричної різниці ^
print(f"{symmetric_diff}")

# Task 11. Створіть словник з кількістю символів у кожному слові
words = ["cat", "dog", "elephant", "bee"]
word_lengths = {word: len(word) for word in words }  # Ваш код тут: {"cat": 3, "dog": 3, ...}
print(f"{word_lengths}")

# Task 12. Створіть словник з квадратами та кубами чисел
numbers = [2, 3, 4, 5]
powers_dict={}
for n in numbers:
    powers_dict[n] = {"square":n**2, "cube": n**3}
#powers_dict = {n: {"square" : n**2, "cube" : n**3} for n in numbers}  # Ваш код тут: {2: {"square": 4, "cube": 8}, ...}
print(f"{powers_dict}")

# Task 13. Згрупуйте слова за їх довжиною
word_list = ["apple", "cat", "dog", "banana", "car", "elephant"]
grouped_by_length = {}  # Ваш код тут
for wl in word_list:  #знаходимо довжину слова у  word_list проходимо по кожному слову.
    length=len(wl)
    if length not in grouped_by_length: #перевяємо, чи є вже такий ключ (довжина) у словнику. якщо немає такої довжини 
        grouped_by_length[length]=[]   # створюємо пустий список 
    grouped_by_length[length].append(wl) # додаємо слово до відповідної довжини до списку
print(f"{grouped_by_length}")
# Task 14. Створіть словник частоти символів у рядку
sentence = "hello world"
char_frequency = {}  # Ваш код тут
for symbol in sentence:
    if symbol not in char_frequency:
        char_frequency[symbol]=1
    else: char_frequency[symbol]=char_frequency[symbol]+1
print(f"{char_frequency}")


# Task 15. Об'єднайте декілька словників
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
dict3 = {"e": 5, "f": 6}
combined_dict = {}  # Ваш код тут
combined_dict.update(dict1) # додамо dict1 в combined_dict
combined_dict.update(dict2) # додамо dict2 в combined_dict
combined_dict.update(dict3) # додамо dict3 в combined_dict
print(f"{combined_dict}")

# Task 16. Інвертуйте словник (ключі стають значеннями)
original = {"name": "John", "age": 25, "city": "Kyiv"}
inverted = {}  # Ваш код тут
for key, value in original.items(): # items() — це метод словника, який повертає всі пари «ключ–значення» у вигляді послідовності кортежів
    inverted[value]=key #створюємо новий словник, де старе значення стає ключем, а старий ключ — значенням
print(f"{inverted}")

# Task 17. Створіть список кортежів з словника
scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
score_tuples = []  # Ваш код тут: [("Alice", 95), ...]
for item in scores.items(): #повертає пари (ключ, значення) як кортежі, наприклад("Alice", 95).
    score_tuples.append(item) #додаємо кортеж у список score_tuples
print(f"{score_tuples}")



# Task 18. Знайдіть спільні ключі у двох словниках
dict_a = {"x": 1, "y": 2, "z": 3}
dict_b = {"y": 5, "z": 6, "w": 7}
common_keys = set(dict_a.keys()) & set(dict_b.keys()) # Ваш код тут
print(f"{common_keys}")


# Task 19. Створіть вкладений словник з інформацією про студентів
students_info = {
    "student1":{
        "name": "Olena",
        "age": 43,
        "grade": [99, 81 ,84]
    },
    "student2":{
        "name": "Iruna",
        "age": 38,
        "grade": [90, 87, 89]
    }
}  # Ваш код тут: {"student1": {"name": ..., "grades": [...]}, ...}

# Task 20. Сплюсніть всі списки у словнику
data = {"list1": [1, 2], "list2": [3, 4], "list3": [5, 6]}
flattened = []  
# Ваш код тут: [1, 2, 3, 4, 5, 6]
for val_list in data.values(): #пройдемося по всіх значеннях словника data
    for x in val_list:  #пройдемося по всіх елементах списку val_list
        flattened.append(x) #додамо значення до списку flattened
print(f"{flattened}")

if __name__ == "__main__":
    print("\n=== ЗАВЕРШЕННЯ ===")
    print("Поглиблені завдання виконано! Запустіть test_selflearning.py для перевірки.")