from collections import Counter
from vernadsky_lab.minerals import MINERAL_CATALOG, get_mineral
from vernadsky_lab.observations import get_observations


def summary() -> str:
    minerals_count = len(MINERAL_CATALOG)
    observations = get_observations()
    obs_count = len(observations)

    if not observations:
        top_researcher_str = "Спостережень ще немає"
    else:
        researchers = [entry["researcher"] for entry in observations]
        most_common, count = Counter(researchers).most_common(1)[0]
        top_researcher_str = f"{most_common} ({count} записи)"

    return (
        f"=== Загальне зведення ===\n"
        f"Мінералів у каталозі: {minerals_count}\n"
        f"Спостережень у журналі: {obs_count}\n"
        f"Найактивніший дослідник: {top_researcher_str}"
    )


def mineral_report(name: str) -> str:
    mineral = get_mineral(name)
    if not mineral:
        return f"Мінерал '{name}' відсутній у каталозі"

    info = f"Формула: {mineral['formula']} | Твердість: {mineral['hardness']} | Походження: {mineral['origin']} | Відкрито: {mineral['discovered']}"
    obs_list = get_observations(name)

    if not obs_list:
        obs_text = "  Немає записів"
    else:
        lines = [f"  [{entry['date']}] {entry['researcher']}: {entry['note']}" for entry in obs_list]
        obs_text = "\n".join(lines)

    return f"=== Звіт: {name} ===\n{info}\nСпостереження:\n{obs_text}"