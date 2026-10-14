MINERAL_CATALOG = {
    "Кварц": {"formula": "SiO₂", "hardness": 7, "origin": "Урал", "discovered": 1845},
    "Берил": {"formula": "Be₃Al₂Si₆O₁₈", "hardness": 8, "origin": "Житомирщина", "discovered": 1830},
    "Алмаз": {"formula": "C", "hardness": 10, "origin": "Якутія", "discovered": 1725},
    "Тальк": {"formula": "Mg₃Si₄O₁₀(OH)₂", "hardness": 1, "origin": "Карелія", "discovered": 1817},
    "Корунд": {"formula": "Al₂O₃", "hardness": 9, "origin": "Індія", "discovered": 1794},
}


def get_mineral(name: str):
    return MINERAL_CATALOG.get(name)


def register_mineral(name: str, formula: str, hardness: int, origin: str, discovered: int) -> str:
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