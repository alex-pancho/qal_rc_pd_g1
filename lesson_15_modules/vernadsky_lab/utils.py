"""Допоміжні інструменти лабораторії."""

from vernadsky_lab.minerals import MINERAL_CATALOG


def hardest_minerals(n=3):
    """Повертає список n найтвердіших мінералів."""

    sorted_minerals = sorted(
        MINERAL_CATALOG.items(),
        key=lambda mineral: mineral[1]["hardness"],
        reverse=True
    )

    result = []

    for name, data in sorted_minerals[:n]:
        result.append(name)

    return result


def search_by_origin(origin_keyword):
    """Пошук мінералів за місцем походження."""

    result = []

    for name, data in MINERAL_CATALOG.items():
        if origin_keyword.lower() in data["origin"].lower():
            result.append(name)

    return result