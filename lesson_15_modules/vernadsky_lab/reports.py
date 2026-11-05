"""Формування звітів лабораторії."""

from vernadsky_lab.minerals import MINERAL_CATALOG, get_mineral
from vernadsky_lab.observations import get_observations


def summary():
    """Повертає загальне зведення по лабораторії."""

    observations = get_observations()

    if not observations:
        active_researcher = "Спостережень ще немає"
    else:
        researchers = {}

        for observation in observations:
            researcher = observation["researcher"]

            if researcher in researchers:
                researchers[researcher] += 1
            else:
                researchers[researcher] = 1

        active_name = max(researchers, key=researchers.get)
        active_count = researchers[active_name]

        active_researcher = (
            f"{active_name} ({active_count} записи)"
        )

    return (
        f"Мінералів у каталозі: {len(MINERAL_CATALOG)}\n"
        f"Спостережень у журналі: {len(observations)}\n"
        f"Найактивніший дослідник: {active_researcher}"
    )


def mineral_report(name):
    """Повертає детальний звіт по мінералу."""

    mineral = get_mineral(name)

    if mineral is None:
        return f"Мінерал '{name}' відсутній у каталозі"

    observations = get_observations(name)

    report = (
        f"=== Звіт: {name} ===\n"
        f"Формула: {mineral['formula']} | "
        f"Твердість: {mineral['hardness']} | "
        f"Походження: {mineral['origin']} | "
        f"Відкрито: {mineral['discovered']}\n"
        f"Спостереження:\n"
    )

    if not observations:
        report += "  Спостережень немає\n"
    else:
        for observation in observations:
            report += (
                f"  [{observation['date']}] "
                f"{observation['researcher']}: "
                f"{observation['note']}\n"
            )

    return report