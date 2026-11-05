"""Журнал спостережень лабораторії."""

from datetime import date

from vernadsky_lab.minerals import get_mineral


_journal = []


def record(researcher, mineral_name, note):
    """Записує нове спостереження."""

    mineral = get_mineral(mineral_name)

    if mineral is None:
        return (
            f"Мінерал '{mineral_name}' не зареєстровано. "
            "Спочатку додайте його до каталогу"
        )

    observation = {
        "researcher": researcher,
        "mineral": mineral_name,
        "note": note,
        "date": date.today(),
    }

    _journal.append(observation)

    return f"Спостереження записано: {researcher} → {mineral_name}"


def get_observations(mineral_name=None):
    """Повертає всі спостереження або лише по одному мінералу."""

    if mineral_name is None:
        return _journal.copy()

    result = []

    for observation in _journal:
        if observation["mineral"] == mineral_name:
            result.append(observation)

    return result