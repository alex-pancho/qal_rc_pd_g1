import csv
from pathlib import Path

prj_folder = Path(__file__).parents[1]


def csv_read_1251(filepath: Path):
    with open(filepath, encoding="windows-1251") as file:
        reader = csv.reader(file)
        return list(reader)

def print_1251(reader):
    # print("next", next(reader))
    for row in reader:
        print(row)

def dict_reader(filepath: Path):
    with open(filepath, encoding="utf8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def main(filepath):
    # result = csv_read_1251(filepath)
    result = dict_reader(filepath)
    print_1251(result)

if __name__ == "__main__":
    filepath = prj_folder / "lesson_17_csv" / "ex.csv"
    filepath_2 = prj_folder / "lesson_17_csv" / "students.csv"
    main(filepath_2)
