# -*- coding: utf-8 -*-
# Самостійне вивчення методів list, tuple, set, dict
# Виконайте завдання та збережіть результати у вказаних змінних

print("=== РОБОТА З СПИСКАМИ (LIST) ===")

# Task 1. Створіть список з числами від 1 до 5
numbers = []  # Ваш код тут
numbers = [1,2,3,4,5]


# Task 2. Додайте число 6 в кінець списку numbers
# Ваш код тут
numbers.append(6)
# Task 3. Вставте число 0 на початок списку numbers  
# Ваш код тут
numbers.insert(0,0)

# Task 4. Видаліть перше входження числа 3 зі списку numbers
# Ваш код тут
numbers.remove(3)
print(numbers)

# Task 5. Знайдіть індекс елемента 'cherry' у списку fruits
fruits = ['apple', 'banana', 'cherry', 'banana', 'date']
cherry_index = None  # Ваш код тут
cherry_index = fruits.index("cherry")
print(cherry_index)
# Task 6. Порахуйте кількість входжень 'banana' у списку fruits
banana_count = 0  # Ваш код тут
banana_count = fruits.count("banana")
print(banana_count)

# Task 7. Відсортуйте список fruits за алфавітом
# Ваш код тут
sort_peralfabet_fruits = sorted(fruits)
print(sort_peralfabet_fruits)
# Task 8. Створіть копію списку fruits
fruits_copy = fruits  # Ваш код тут
print(fruits)

print("\n=== РОБОТА З КОРТЕЖАМИ (TUPLE) ===")

# Task 9. Створіть кортеж з днями тижня
weekdays = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')  # Ваш код тут

# Task 10. Знайдіть індекс 'Wednesday' у кортежі weekdays
wednesday_index = weekdays.index('Wednesday')  # Ваш код тут
print(wednesday_index)

# Task 11. Порахуйте кількість входжень 'Monday' у кортежі
test_tuple = ('Monday', 'Tuesday', 'Monday', 'Friday', 'Monday')
monday_count = test_tuple.count('Monday')  # Ваш код тут
print(monday_count)

# Task 12. Перетворіть кортеж weekdays на список
weekdays_list = list(weekdays)  # Ваш код тут
print(weekdays_list)

print("\n=== РОБОТА З МНОЖИНАМИ (SET) ===")

# Task 13. Створіть множину з унікальних чисел
unique_numbers =  set([1, 2, 3, 4, 5])  # Ваш код тут: додайте числа 1, 2, 3, 4, 5
print(unique_numbers)

# Task 14. Додайте число 6 до множини unique_numbers
# Ваш код тут
unique_numbers.add(6)
print(unique_numbers)
# Task 15. Видаліть число 3 з множини unique_numbers
# Ваш код тут
unique_numbers.remove(3)
print(unique_numbers)


# Task 16. Створіть дві множини та знайдіть їх об'єднання
set_a = {1, 2, 3}
set_b = {3, 4, 5}
union_set = set_a.union(set_b) #set(set_a + set_b)  # Ваш код тут
print("union_set", union_set)

# Task 17. Знайдіть перетин множин set_a та set_b
intersection_set = set_a.intersection(set_b)  # Ваш код тут
print("intersection_set", intersection_set)

# Task 18. Знайдіть різницю set_a - set_b
difference_set = set_a - set_b  # Ваш код тут
print("difference_set", difference_set)

# Task 19. Перевірте, чи є число 4 у множині unique_numbers
is_four_present = 4 in unique_numbers  # Ваш код тут
print("is_four_present", is_four_present)

print("\n=== РОБОТА З СЛОВНИКАМИ (DICT) ===")

# Task 20. Створіть словник з інформацією про студента
student = {"name":"Mykhailo", "age":48, "group":"qal_rc_pd_g1"} # Ваш код тут: додайте ім'я,вік, група

# Task 21. Додайте до словника student ключ 'grade' зі значенням 'A'
# Ваш код тут
student.update({'grade':'A'})
print("student", student)

# Task 22. Отримайте значення ключа 'name' зі словника student
student_name = student['name']  # Ваш код тут
print("student_name", student_name)

# Task 23. Отримайте всі ключі словника student
student_keys = student.keys()  # Ваш код тут
print("student_keys", student_keys)

# Task 24. Отримайте всі значення словника student  
student_values = []  # Ваш код тут

# Task 25. Видаліть ключ 'grade' зі словника student
# Ваш код тут
student.pop("grade")
print("student", student)

# Task 26. Створіть словник з квадратами чисел від 1 до 5
squares_dict = {}  # Ваш код тут: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
for i in range(1, 6): 
    squares_dict[i] = i**2  
print("squares_dict", squares_dict)

# Task 27. Перевірте, чи існує ключ 3 у словнику squares_dict
key_exists = 3 in squares_dict  # Ваш код тут
print(" Перевірте, чи існує ключ 3 у словнику squares_dict" ,key_exists)

# Task 28. Оновіть словник student новими даними
new_data = {'city': 'Kyiv', 'hobby': 'programming'}
student.update(new_data)
print("student upd", student)
# Ваш код тут
if __name__ == "__main__":
    print("\n=== ЗАВЕРШЕННЯ ===")
    print("Всі завдання виконано! Запустіть test_selflearning.py для перевірки.")