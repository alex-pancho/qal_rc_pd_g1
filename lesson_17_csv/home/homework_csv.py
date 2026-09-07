import csv
from pathlib import Path


def read_file(filepath: Path) -> list[dict]:
    if not filepath.exists():
        print(f"Попередження: Файл {filepath.name} не знайдено.")
        return []

    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_csv(filepath: Path, content: list[dict]):
    if not content:
        print("Немає даних для запису.")
        return

    with open(filepath, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=content[0].keys())
        writer.writeheader()
        writer.writerows(content)


def find_duplicates(rows: list[dict]) -> tuple[list[dict], int]:
    unique_rows = []
    seen = set()
    duplicates_count = 0

    for row in rows:
        row_tuple = tuple(sorted(row.items()))
        if row_tuple in seen:
            duplicates_count += 1
        else:
            seen.add(row_tuple)
            unique_rows.append(row)

    return unique_rows, duplicates_count


def main():
    base_dir = Path(__file__).parent

    file_1 = base_dir / "users_1.csv"
    file_2 = base_dir / "users_2.csv"
    output_file = base_dir / "clean_users_3.csv"

    data_1 = read_file(file_1)
    data_2 = read_file(file_2)

    all_records = data_1 + data_2

    if not all_records:
        print("Помилка: Не вдалося зчитати жодного запису з файлів.")
        return

    unique_records, duplicates_count = find_duplicates(all_records)

    write_csv(output_file, unique_records)

    print("=== Результат дедублікації ===")
    print(f"Знайдено дублікатів: {duplicates_count}")
    print(f"Унікальних записів збережено: {len(unique_records)}")
    print(f"Файл: {output_file.name}")


if __name__ == "__main__":
    main()