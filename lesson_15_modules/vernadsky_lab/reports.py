from vernadsky_lab.minerals import MINERAL_CATALOG, get_mineral
from vernadsky_lab.observations import get_observations

def summary():
    """Повертає коротке зведення по лабораторії у заданому форматі."""
    total_minerals = len(MINERAL_CATALOG)
    all_obs = get_observations()
    total_observations = len(all_obs)
    
    if total_observations == 0:
        most_active_str = "Спостережень ще немає"
    else:
        researcher_counts = {}
        for obs in all_obs:
            name = obs["researcher"]
            researcher_counts[name] = researcher_counts.get(name, 0) + 1
        
        most_active = max(researcher_counts, key=researcher_counts.get)
        count = researcher_counts[most_active]
        
        if count == 1:
            suffix = "запис"
        elif 2 <= count <= 4:
            suffix = "записи"
        else:
            suffix = "записів"
            
        most_active_str = f"{most_active} ({count} {suffix})"
        
    return (
        f"Мінералів у каталозі: {total_minerals}\n"
        f"Спостережень у журналі: {total_observations}\n"
        f"Найактивніший дослідник: {most_active_str}"
    )

def mineral_report(name: str):
    """Повертає розгорнутий звіт для конкретного мінералу з точним форматуванням."""
    mineral_data = get_mineral(name)
    if mineral_data is None:
        return f"Мінерал '{name}' відсутній у каталозі"
        
    obs_list = get_observations(name)
    formula = mineral_data['formula'].replace('2', '₂')
    
    report_lines = [
        f"=== Звіт: {name} ===",
        f"Формула: {formula} | Твердість: {mineral_data['hardness']} | Походження: {mineral_data['origin']} | Відкрито: {mineral_data['discovered']}",
        "Спостереження:"
    ]
    
    if obs_list:
        for obs in obs_list:
            report_lines.append(f"  [{obs['date']}] {obs['researcher']}: {obs['note']}")
    else:
        report_lines.append("  (немає спостережень)")
            
    return "\n".join(report_lines)