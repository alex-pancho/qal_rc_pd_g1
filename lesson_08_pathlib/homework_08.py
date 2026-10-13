### Робота з файлами та папками — завдання
"""
1. **Створення файлу**
   Створи текстовий файл `hello.txt` і запиши в нього рядок:       
   ```
   Hello, Python!

  
"""
# coding here
from pathlib import Path
file_path = Path("lesson_08_pathlib") / "hello.txt"
with open(file_path, "w", encoding="utf-8") as f:
      f.write("Hello, Python!")

"""
2. **Читання файлу**
   Відкрий файл `hello.txt` і виведи його вміст на екран.
"""
# coding here
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
"""   
3. **Дозапис у файл**
   Додай у файл `hello.txt` ще один рядок:

   ```
   Learning file operations.
   ```
"""
# coding here
with open(file_path, "a", encoding="utf-8") as f:
    f.write("\nLearning file operations.")


"""
4. **Читання кількох рядків**
   Виведи всі рядки з файлу `hello.txt` по одному рядку (без додаткових символів `\n`).
"""
# coding here
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for line in lines:
    print(line.strip())    
"""
5. **Підрахунок символів**
   Прочитай файл `hello.txt` і виведи кількість символів у ньому.
"""
# coding here
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    print(f"Кількість символів у файлі: {len(content)}")
"""
6. **Створення папки**
   Створи папку з назвою `data`. Усередині неї створи файл `notes.txt` із текстом:

   ```
   My first note.
   ```
"""
# coding here
new_directory = Path("lesson_08_pathlib") / "data"
new_directory.mkdir(exist_ok=True)
file_path_1 = Path(new_directory) / "notes.txt"
with open(file_path_1, "w", encoding="utf-8") as f:
    f.write("My first note.")
"""
7. **Список файлів у папці**
   Виведи на екран список усіх файлів у папці `data`.
"""
# coding here
files = [f for f in new_directory.iterdir() if f.is_file()]
for file in files:
    print(file)
"""
8. **Копіювання вмісту**
   Прочитай вміст файлу `notes.txt` і запиши його у файл `copy.txt` (у тій же папці `data`).
"""
# coding here
with open(file_path_1, "r", encoding="utf-8") as f:
    content = f.read()
with open(Path(new_directory) / "copy.txt", "w", encoding="utf-8") as f:
    f.write(content)

"""
9. **Об’єднання файлів**
   Створи два файли: `a.txt` і `b.txt`, кожен із будь-яким текстом.
   Запиши їхній вміст у новий файл `ab.txt`.
"""
# coding here
file_a_path = Path(new_directory) / "a.txt"
file_b_path = Path(new_directory) / "b.txt"
with open(file_a_path, "w", encoding="utf-8") as f:
    f.write("Відомо, що практика вдячності зменшує стрес, підвищує самооцінку та сприяє стійкості навіть у дуже важкі часи")
with open(file_b_path, "w", encoding="utf-8") as f:
    f.write("Подумайте про людей, моменти або речі, які приносять вам якийсь комфорт або щастя, і намагайтеся висловлювати свою вдячність хоча б раз на день")
file_ab_path = Path(new_directory) / "ab.txt"
with open(file_ab_path, "w", encoding="utf-8") as f:
    with open(file_a_path, "r", encoding="utf-8") as a:
        f.write(a.read() + "\n")
    with open(file_b_path, "r", encoding="utf-8") as b:
        f.write(b.read())
"""
10. **Пошук слова у файлі**
    У файлі `notes.txt` перевір, чи є слово `"note"`.
    Якщо є — виведи `"Знайдено"`, інакше `"Не знайдено"`.
"""
# coding here
with open(file_path_1, "r", encoding="utf-8") as f:
   content = f.read()
   if "note" in content:
        print("Знайдено")
   else:
        print("Не знайдено")