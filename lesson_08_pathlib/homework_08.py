### Робота з файлами та папками — завдання
"""
1. **Створення файлу**
   Створи текстовий файл `hello.txt` і запиши в нього рядок:

   ```
   Hello, Python!
   ```
"""
# coding here

"""
2. **Читання файлу**
   Відкрий файл `hello.txt` і виведи його вміст на екран.
"""
# coding here

"""   
3. **Дозапис у файл**
   Додай у файл `hello.txt` ще один рядок:

   ```
   Learning file operations.
   ```
"""
# coding here

"""
4. **Читання кількох рядків**
   Виведи всі рядки з файлу `hello.txt` по одному рядку (без додаткових символів `\n`).
"""
# coding here

"""
5. **Підрахунок символів**
   Прочитай файл `hello.txt` і виведи кількість символів у ньому.
"""
# coding here

"""
6. **Створення папки**
   Створи папку з назвою `data`. Усередині неї створи файл `notes.txt` із текстом:

   ```
   My first note.
   ```
"""
# coding here

"""
7. **Список файлів у папці**
   Виведи на екран список усіх файлів у папці `data`.
"""
# coding here

"""
8. **Копіювання вмісту**
   Прочитай вміст файлу `notes.txt` і запиши його у файл `copy.txt` (у тій же папці `data`).
"""
# coding here

"""
9. **Об’єднання файлів**
   Створи два файли: `a.txt` і `b.txt`, кожен із будь-яким текстом.
   Запиши їхній вміст у новий файл `ab.txt`.
"""
# coding here

"""
10. **Пошук слова у файлі**
    У файлі `notes.txt` перевір, чи є слово `"note"`.
    Якщо є — виведи `"Знайдено"`, інакше `"Не знайдено"`.
"""
# coding here
from pathlib import Path
import os

# 6. Створення папки та файлу всередині
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)  # Створює папку 'data', якщо її ще немає

notes_file = data_dir / "notes.txt"
with open(notes_file, "w", encoding="utf-8") as file:
    file.write("My first note.\n")

# 7. Список файлів у папці
print("--- Пункт 7: Список файлів у папці 'data' ---")
files_in_data = os.listdir(data_dir)
for file_name in files_in_data:
    print(file_name)

# 8. Копіювання вмісту з notes.txt у copy.txt
copy_file = data_dir / "copy.txt"
with open(notes_file, "r", encoding="utf-8") as src_file:
    content = src_file.read()

with open(copy_file, "w", encoding="utf-8") as dest_file:
    dest_file.write(content)

# 9. Об’єднання файлів a.txt та b.txt у новий файл ab.txt
file_a = Path("a.txt")
file_b = Path("b.txt")
file_ab = Path("ab.txt")

# Записуємо довільний текст у файли a.txt і b.txt
with open(file_a, "w", encoding="utf-8") as f:
    f.write("Text from file A.\n")

with open(file_b, "w", encoding="utf-8") as f:
    f.write("Text from file B.\n")

# Зчитуємо обидва файли та об'єднуємо їх у ab.txt
with open(file_a, "r", encoding="utf-8") as f_a, open(file_b, "r", encoding="utf-8") as f_b:
    text_a = f_a.read()
    text_b = f_b.read()

with open(file_ab, "w", encoding="utf-8") as f_ab:
    f_ab.write(text_a + text_b)

# 10. Пошук слова у файлі
print("\n--- Пункт 10: Пошук слова ---")
with open(notes_file, "r", encoding="utf-8") as file:
    text = file.read()
    if "note" in text:
        print("Знайдено")
    else:
        print("Не знайдено")