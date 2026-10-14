### Робота з файлами та папками — завдання
"""
1. **Створення файлу**
   Створи текстовий файл `hello.txt` і запиши в нього рядок:

   ```
   Hello, Python!
   ```
"""
# coding here
from pathlib import Path
def write_file(filepath, content):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)  
content = "Hello, Python!"        

current_file = Path(__file__)
hello_file = current_file.parent/"hello.txt"
print(hello_file)
write_file(hello_file, content)

"""
2. **Читання файлу**
   Відкрий файл `hello.txt` і виведи його вміст на екран.
"""
def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        return content
content = read_file(hello_file)  
print(content)  

"""   
3. **Дозапис у файл**
   Додай у файл `hello.txt` ще один рядок:

   ```
   Learning file operations.
   ```
"""
def append_file(filepath, content):
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(content)
new_content = "\nLearning file operations."

append_file(hello_file, new_content)


"""
4. **Читання кількох рядків**
   Виведи всі рядки з файлу `hello.txt` по одному рядку (без додаткових символів `\n`).
"""
with open(hello_file, "r", encoding="utf-8") as f:
  for line in f:
      print(line.strip())


"""
5. **Підрахунок символів**
   Прочитай файл `hello.txt` і виведи кількість символів у ньому.
"""
with open(hello_file, "r", encoding="utf-8") as f:
    all_text = f.read()
    print(len(all_text))

"""
6. **Створення папки**
   Створи папку з назвою `data`. Усередині неї створи файл `notes.txt` із текстом:

   ```
   My first note.
   ```
"""
from pathlib import Path
data_directory = Path(__file__).parent / "data"
data_directory.mkdir(mode = 0o777, exist_ok = True, parents = True)

from pathlib import Path
notes_file = data_directory/"notes.txt"
content_in_notes = "My first note."
write_file(notes_file, content_in_notes)
print(notes_file)

"""
7. **Список файлів у папці**
   Виведи на екран список усіх файлів у папці `data`.
"""
all_files = [d for d in data_directory.iterdir() if d.is_file()]

"""
8. **Копіювання вмісту**
   Прочитай вміст файлу `notes.txt` і запиши його у файл `copy.txt` (у тій же папці `data`).
"""
content1 = read_file(notes_file)  
print(content1) 

from pathlib import Path
copy_file = data_directory/"copy.txt"
write_file(copy_file, content1)
print(copy_file)

"""
9. **Об’єднання файлів**
   Створи два файли: `a.txt` і `b.txt`, кожен із будь-яким текстом.
   Запиши їхній вміст у новий файл `ab.txt`.
"""
from pathlib import Path
a_file = data_directory/"a.txt"
content2 = "Home work 8."
write_file(a_file, content2)
print(a_file)

from pathlib import Path
b_file = data_directory/"b.txt"
content3 = "Робота з папками і файлами."
write_file(b_file, content3)
print(b_file)

from pathlib import Path
ab_file = data_directory/"ab.txt"
content4 = content2 +" "+ content3
write_file(ab_file, content4)
print(ab_file)


"""
10. **Пошук слова у файлі**
    У файлі `notes.txt` перевір, чи є слово `"note"`.
    Якщо є — виведи `"Знайдено"`, інакше `"Не знайдено"`.
"""
with open(notes_file, "r", encoding="utf-8") as f:
    all_text = f.read()
    if "note" in all_text:
        print("Знайдено")
    else:
        print("Не знайдено.")
