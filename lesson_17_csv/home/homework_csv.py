import csv
from pathlib import Path


def read_file(filepath: Path) -> list:
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_csv(filepath: Path, content: list):
    if not content:
        return

    with open(
        filepath,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=content[0].keys()
        )

        writer.writeheader()
        writer.writerows(content)


def find_duplicates(rows: list) -> tuple:
    unique_rows = []
    seen = set()
    duplicates_count = 0

    for row in rows:
        row_key = tuple(row.items())

        if row_key in seen:
            duplicates_count += 1
        else:
            seen.add(row_key)
            unique_rows.append(row)

    return unique_rows, duplicates_count


def main():
    base_path = Path(__file__).parent

    users_1 = read_file(
        base_path / "users_1.csv"
    )

    users_2 = read_file(
        base_path / "users_2.csv"
    )

    all_users = users_1 + users_2

    unique_users, duplicates_count = (
        find_duplicates(all_users)
    )

    output_file = (
        base_path / "clean_users_3.csv"
    )

    write_csv(
        output_file,
        unique_users
    )

    print(
        f"Знайдено дублікатів: "
        f"{duplicates_count}"
    )

    print(
        f"Унікальних записів збережено: "
        f"{len(unique_users)}"
    )

    print(
        f"Файл: {output_file.name}"
    )


if __name__ == "__main__":
    main()