from vernadsky_lab import register_mineral, record, summary, mineral_report, to_csv

if __name__ == "__main__":
    print("=== Лабораторія Вернадського ===\n")

    print("Реєстрація мінералів:")
    print(register_mineral("Берил", "Be₃Al₂Si₆O₁₈", 8, "Житомирщина", 1830))
    print(register_mineral("Кварц", "SiO₂", 7, "Урал", 1845))
    print(register_mineral("Кварц", "SiO₂", 7, "Урал", 1845))

    print("\nЗапис спостережень:")
    print(record("Вернадський", "Берил", "виявлено родовище високої чистоти"))
    print(record("Ферсман", "Кварц", "прозорий, без включень"))
    print(record("Вернадський", "Кварц", "виражена кристалічна решітка"))
    print(record("Ферсман", "Малахіт", "знайдено гарний зразок"))

    print("\n" + summary())
    print("\n" + mineral_report("Кварц"))

    # Експорт у CSV (Бонус)
    print("\n" + to_csv("observations_export.csv"))