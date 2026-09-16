### Робота з файлами та папками — завдання
"""
1. **Створення файлу**
   Створи текстовий файл `hello.txt` і запиши в нього рядок:

   ```
   Hello, Python!
   ```
"""
# coding here 
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("Hello, Python!\n")

"""
2. **Читання файлу**
   Відкрий файл `hello.txt` і виведи його вміст на екран.
"""
# coding here
with open("hello.txt", "r", encoding="utf-8") as f:
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
with open("hello.txt", "a", encoding="utf-8") as f:
    f.write("Learning file operations.\n")

"""
4. **Читання кількох рядків**
   Виведи всі рядки з файлу `hello.txt` по одному рядку (без додаткових символів `\n`).
"""
# coding here
with open("hello.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

"""
5. **Підрахунок символів**
   Прочитай файл `hello.txt` і виведи кількість символів у ньому.
"""
# coding here
with open("hello.txt", "r", encoding="utf-8") as f:
    text = f.read()
    print(len(text))

"""
6. **Створення папки**
   Створи папку з назвою `data`. Усередині неї створи файл `notes.txt` із текстом:

   ```
   My first note.
   ```
"""
# coding here
from pathlib import Path

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

notes_path = data_dir / "notes.txt"
notes_path.write_text("My first note.\n", encoding="utf-8")

"""
7. **Список файлів у папці**
   Виведи на екран список усіх файлів у папці `data`.
"""
# coding here
from pathlib import Path

data_dir = Path("data")
files = [f for f in data_dir.iterdir() if f.is_file()]
print(files)

"""
8. **Копіювання вмісту**
   Прочитай вміст файлу `notes.txt` і запиши його у файл `copy.txt` (у тій же папці `data`).
"""
# coding here
from pathlib import Path

notes_path = Path("data") / "notes.txt"
copy_path = Path("data") / "copy.txt"

text = notes_path.read_text(encoding="utf-8")
copy_path.write_text(text, encoding="utf-8")

"""
9. **Об’єднання файлів**
   Створи два файли: `a.txt` і `b.txt`, кожен із будь-яким текстом.
   Запиши їхній вміст у новий файл `ab.txt`.
"""
# coding here
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("Text A\n")

with open("b.txt", "w", encoding="utf-8") as f:
    f.write("Text B\n")

with open("a.txt", "r", encoding="utf-8") as fa, \
     open("b.txt", "r", encoding="utf-8") as fb, \
     open("ab.txt", "w", encoding="utf-8") as fab:
    fab.write(fa.read())
    fab.write(fb.read())

"""
10. **Пошук слова у файлі**
    У файлі `notes.txt` перевір, чи є слово `"note"`.
    Якщо є — виведи `"Знайдено"`, інакше `"Не знайдено"`.
"""
# coding here
with open("data/notes.txt", "r", encoding="utf-8") as f:
    text = f.read()

if "note" in text:
    print("Знайдено")
else:
    print("Не знайдено")