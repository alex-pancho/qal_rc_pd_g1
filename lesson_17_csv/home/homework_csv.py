import csv
from pathlib import Path


def read_file(filepath: Path) -> list:
    with open(filepath, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_csv(filepath: Path, content: list, fieldnames: list):
    with open(filepath, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(content)


def main(data_1, data_2):
    l1 = len(data_1)
    l2 = len(data_2)

    set1 = {frozenset(row.items()) for row in data_1}
    set2 = {frozenset(row.items()) for row in data_2}

    duplicates_1 = l1 - len(set1)
    duplicates_2 = l2 - len(set2)

    duplicates_between = len(set1 & set2)

    total_duplicates = duplicates_1 + duplicates_2 + duplicates_between

    unique_rows = set1 | set2
    clean_data = [dict(row) for row in unique_rows]

    print(f"Дублікатів у першому файлі: {duplicates_1}")
    print(f"Дублікатів у другому файлі: {duplicates_2}")
    print(f"Спільних рядків між файлами: {duplicates_between}")
    print(f"Усього знайдено дублікатів: {total_duplicates}")

    return clean_data


if __name__ == "__main__":
    base_path = Path(__file__).parent

    file_1 = base_path / "users_1.csv"
    file_2 = base_path / "users_2.csv"
    output_file = base_path / "clean_users_3.csv"

    data_1 = read_file(file_1)
    data_2 = read_file(file_2)

    clean_data = main(data_1, data_2)

    fieldnames = list(data_1[0].keys() if data_1 else data_2[0].keys())

    write_csv(output_file, clean_data, fieldnames)

    print("Унікальні записи збережено у clean_users_3.csv")