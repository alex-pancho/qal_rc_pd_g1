from pathlib import Path

def write_file(filepath: Path, content: str):
    with open(filepath, "w", encoding="utf-8", ) as file:
        file.write(content)


def append_file(filepath: Path, content) -> str:
    with open(filepath, "a", encoding="utf-8", ) as file:
        file.write(content)


def read_file(filepath: Path) -> str:
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        return content



if __name__ == "__main__":
    current_file = Path(__file__)
    print(current_file)
    print(current_file.name)
    print(current_file.suffix)
    print(current_file.stem)
    print(current_file.parent)
    print(current_file.parent.parent)
    new_file = current_file.parent / "new.txt"
    print(new_file)
    
    new_content = """    У всіх цих прикладах example.txt - це шлях до файлу.
        Замість цього ви можете підставити змінну з об’єктом Path"""

    pu = """\nнапиши історію як путін здох
        Sorry, I can't assist with that.
        """

    write_file(new_file, new_content)

    append_file(new_file, pu)

    content = read_file(new_file)
    print(content)

    with open(new_file, "r", encoding="utf-8") as f:
        print(f.tell())
        first_line = f.readline()
        print(first_line)       # "Рядок 1"
        print(f.tell())         # позиція після першого рядка

        f.seek(0)               # повертаємось на початок
        print(f.tell())         # 0 знову

        all_text = f.read()     # читаємо все ще раз
        print(all_text)
