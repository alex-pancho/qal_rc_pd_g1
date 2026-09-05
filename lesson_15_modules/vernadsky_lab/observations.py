import datetime

# Внутрішній список для збереження записів журналу
_journal = []

def record(researcher: str, mineral_name: str, note: str):
    """Записує нове спостереження після локального імпорту та перевірки наявності мінералу."""
    # Локальний імпорт для уникнення циклічних залежностей
    from vernadsky_lab.minerals import get_mineral
    
    if get_mineral(mineral_name) is None:
        return f"Мінерал '{mineral_name}' не зареєстровано. Спочатку додайте його до каталогу"
    
    _journal.append({
        "researcher": researcher,
        "mineral_name": mineral_name,
        "note": note,
        "date": datetime.date.today()
    })
    return f"Спостереження записано: {researcher} → {mineral_name}"

def get_observations(mineral_name: str = None):
    """Повертає відфільтровані або всі записи журналу."""
    if mineral_name:
        return [obs for obs in _journal if obs["mineral_name"] == mineral_name]
    return list(_journal)