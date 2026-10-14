import csv
from pathlib import Path
from typing import Set, Tuple

def read_file_as_set(filepath: Path) -> Set[Tuple[Tuple[str, str], ...]]:
    """Зчитує CSV-файл і повертає його рядки у вигляді сету незмінних кортежів."""
    rows_set = set()
    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Перетворюємо словник на заморожений кортеж пар (ключ, значення)
                row_tuple = tuple(sorted(row.items()))
                rows_set.add(row_tuple)
    except FileNotFoundError:
        print(f"⚠️ Попередження: Файл '{filepath}' не знайдено.")
    return rows_set


def write_csv_from_set(filepath: Path, rows_set: Set[Tuple[Tuple[str, str], ...]]) -> None:
    """Конвертує кортежі назад у словники та записує їх у CSV із заголовком."""
    if not rows_set:
        print("⚠️ Немає даних для запису.")
        return

    # Перетворюємо назад у список словників
    dict_rows = [dict(row_tuple) for row_tuple in rows_set]
    
    # Витягуємо заголовки колонок з першого елемента
    fieldnames = list(dict_rows[0].keys())

    with open(filepath, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_rows)


def main() -> None:
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    file1 = current_dir / "users_1.csv"
    file2 = current_dir / "users_2.csv"
    output_file = current_dir / "clean_users_3.csv"

    # 1. Зчитуємо обидва файли одразу як сети
    set1 = read_file_as_set(file1)
    set2 = read_file_as_set(file2)

    if not set1 and not set2:
        print("❌ Помилка: Обидва файли порожні або відсутні.")
        return

    # 2. Математика сетів:
    # Перетин (&) знаходить тільки ті рядки, що є в обох файлах одночасно (дублікати)
    duplicates = set1 & set2
    duplicate_count = len(duplicates)

    # Об'єднання (|) залишає тільки унікальні рядки з обох файлів
    unique_rows = set1 | set2

    # 3. Записуємо чистий результат
    write_csv_from_set(output_file, unique_rows)

    # 4. Обов'язкове виведення статистики за ТЗ
    print(f"Знайдено дублікатів: {duplicate_count}")
    print(f"Унікальних записів збережено: {len(unique_rows)}")
    print(f"Файл: {output_file.name}")


if __name__ == "__main__":
    # Автоматичне створення тестових файлів, якщо їх немає в папці
    dir_path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    if not (dir_path / "users_1.csv").exists():
        with open(dir_path / "users_1.csv", "w", encoding="utf-8", newline="") as f:
            f.write("id,name,email\n1,Олександр,alex@test.com\n2,Марія,maria@test.com\n")
    if not (dir_path / "users_2.csv").exists():
        with open(dir_path / "users_2.csv", "w", encoding="utf-8", newline="") as f:
            f.write("id,name,email\n2,Марія,maria@test.com\n4,Олена,elena@test.com\n")

    main()
    