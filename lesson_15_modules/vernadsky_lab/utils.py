from vernadsky_lab.minerals import MINERAL_CATALOG

def hardest_minerals(n: int = 3):
    """Повертає n найтвердіших мінералів за спаданням."""
    sorted_minerals = sorted(
        MINERAL_CATALOG.keys(),
        key=lambda k: MINERAL_CATALOG[k]["hardness"],
        reverse=True
    )
    return sorted_minerals[:n]

def search_by_origin(origin_keyword: str):
    """Шукає мінерали за ключовим словом у полі origin (без урахування регістру)."""
    keyword_lower = origin_keyword.lower()
    results = []
    
    for name, data in MINERAL_CATALOG.items():
        if keyword_lower in data["origin"].lower():
            results.append(name)
            
    return results