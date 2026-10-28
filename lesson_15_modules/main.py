from vernadsky_lab import (
    register_mineral,
    record,
    summary,
    mineral_report,
)


def main():
    print("=== Лабораторія Вернадського ===")

    print("\nРеєстрація мінералів:")

    print(
        register_mineral(
            "Берил",
            "Be3Al2Si6O18",
            8,
            "Україна",
            1901,
        )
    )

    print(
        register_mineral(
            "Кальцит",
            "CaCO3",
            3,
            "Карпати",
            1870,
        )
    )

    print(
        register_mineral(
            "Кальцит",
            "CaCO3",
            3,
            "Карпати",
            1870,
        )
    )

    print("\nЗапис спостережень:")

    print(
        record(
            "Вернадський",
            "Берил",
            "Знайдено включення слюди",
        )
    )

    print(
        record(
            "Ферсман",
            "Кварц",
            "Прозорий кристал",
        )
    )

    print(
        record(
            "Вернадський",
            "Кварц",
            "Виражена кристалічна решітка",
        )
    )

    print(
        record(
            "Вернадський",
            "Малахіт",
            "Зелений колір",
        )
    )

    print("\n=== Загальне зведення ===")
    print(summary())

    print("\n=== Детальний звіт ===")
    print(mineral_report("Кварц"))


if __name__ == "__main__":
    main()