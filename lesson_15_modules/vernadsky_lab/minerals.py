# Каталог мінералів лабораторії (мінімум 5 базових записів)
MINERAL_CATALOG = {
    "Топаз": {
        "formula": "Al2SiO4(F,OH)2",
        "hardness": 8,
        "origin": "Волинь, Україна",
        "discovered": 1737
    },
    "Кальцит": {
        "formula": "CaCO3",
        "hardness": 3,
        "origin": "Крим, Україна",
        "discovered": 1836
    },
    "Алмаз": {
        "formula": "C",
        "hardness": 10,
        "origin": "Кімберлі, ПАР",
        "discovered": 1867
    },
    "Гіпс": {
        "formula": "CaSO4·2H2O",
        "hardness": 2,
        "origin": "Донбас, Україна",
        "discovered": 1758
    },
    "Корунд": {
        "formula": "Al2O3",
        "hardness": 9,
        "origin": "Індія",
        "discovered": 1798
    }
}

def get_mineral(name: str):
    """Повертає словник із даними про мінерал або None, якщо його не знайдено."""
    return MINERAL_CATALOG.get(name, None)

def register_mineral(name: str, formula: str, hardness: int, origin: str, discovered: int):
    """Додає новий мінерал до каталогу з попередньою перевіркою даних."""
    if name in MINERAL_CATALOG:
        return f"Мінерал '{name}' вже зареєстровано в каталозі"
    
    if not (1 <= hardness <= 10):
        return "Некоректна твердість: має бути від 1 до 10"
    
    MINERAL_CATALOG[name] = {
        "formula": formula,
        "hardness": hardness,
        "origin": origin,
        "discovered": discovered
    }
    return f"Мінерал '{name}' додано до каталогу"