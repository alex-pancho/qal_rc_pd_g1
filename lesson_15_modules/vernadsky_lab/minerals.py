"""Каталог мінералів лабораторії."""


MINERAL_CATALOG = {
    "Кварц": {
        "formula": "SiO2",
        "hardness": 7,
        "origin": "Урал",
        "discovered": 1845,
    },
    "Алмаз": {
        "formula": "C",
        "hardness": 10,
        "origin": "Південна Африка",
        "discovered": 1867,
    },
    "Рубін": {
        "formula": "Al2O3",
        "hardness": 9,
        "origin": "М'янма",
        "discovered": 1800,
    },
    "Топаз": {
        "formula": "Al2SiO4(F,OH)2",
        "hardness": 8,
        "origin": "Бразилія",
        "discovered": 1737,
    },
    "Гранат": {
        "formula": "Fe3Al2(SiO4)3",
        "hardness": 7,
        "origin": "Індія",
        "discovered": 1750,
    },
}


def get_mineral(name):
    """Повертає дані про мінерал або None."""

    return MINERAL_CATALOG.get(name)


def register_mineral(name, formula, hardness, origin, discovered):
    """Додає новий мінерал у каталог."""

    if name in MINERAL_CATALOG:
        return f"Мінерал '{name}' вже зареєстровано в каталозі"

    if hardness < 1 or hardness > 10:
        return "Некоректна твердість: має бути від 1 до 10"

    MINERAL_CATALOG[name] = {
        "formula": formula,
        "hardness": hardness,
        "origin": origin,
        "discovered": discovered,
    }

    return f"Мінерал '{name}' додано до каталогу"