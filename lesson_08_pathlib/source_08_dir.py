from pathlib import Path

unix_path = "/home/alex/homework_10.py"
win_path = r"d:\lesson_13\lesson_13.py"
file_path = Path(unix_path)

print("path is file", file_path.is_file())
print("path is dir", file_path.is_dir())
print("path exsist", file_path.exists())

file_path = Path(win_path)

print("path is file", file_path.is_file())
print("path is dir", file_path.is_dir())
print("path exsist", file_path.exists())


file_path = Path(__file__).parent

print("path is file", file_path.is_file())
print("path is dir", file_path.is_dir())
print("path exsist", file_path.exists())

print(__file__, type(__file__))
current_file = Path(__file__)
print(current_file, type(current_file))

current_dir = current_file.parent
print(current_dir)
project_dir = current_file.parent.parent
print(project_dir)

all_dirs = [d for d in project_dir.iterdir() if d.is_dir()]
print(all_dirs)

all_files = [d for d in project_dir.iterdir() if d.is_file()]
print(all_files)

extension = '.txt'
files_with_extension = [f for f in current_dir.iterdir() if f.suffix == extension]
print(files_with_extension)
print(files_with_extension[0].name)

current_directory = Path.cwd()
print("Поточна робоча директорія:", current_directory)
home_dir = Path.home()
print("Домашня директорія користувача:", home_dir)


# create
# Вказуємо шлях до нової директорії
new_directory = home_dir / "directory" / "subdir"
# Створюємо нову директорію
new_directory.mkdir(parents=True, exist_ok=True) #mode=0o777,  
print("Директорія створена успішно!")
