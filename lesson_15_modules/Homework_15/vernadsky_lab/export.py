import csv
from vernadsky_lab.observations import get_observations


def to_csv(filename: str) -> str:
    observations = get_observations()
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "researcher", "mineral", "note"])
        
        for entry in observations:
            writer.writerow([entry["date"], entry["researcher"], entry["mineral"], entry["note"]])

    return f"Журнал експортовано у файл '{filename}'"