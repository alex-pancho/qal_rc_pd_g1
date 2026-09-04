from vernadsky_lab.minerals import MINERAL_CATALOG


def hardest_minerals(n: int = 3) -> list:
    sorted_minerals = sorted(
        MINERAL_CATALOG.items(),
        key=lambda item: item[1]["hardness"],
        reverse=True
    )
    return [name for name, _ in sorted_minerals[:n]]


def search_by_origin(origin_keyword: str) -> list:
    keyword = origin_keyword.lower()
    return [
        name for name, data in MINERAL_CATALOG.items()
        if keyword in data["origin"].lower()
        ]