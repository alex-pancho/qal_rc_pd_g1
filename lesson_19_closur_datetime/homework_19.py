from pathlib import Path


# Завдання 1. Фабрика перетворювачів напруги
def make_voltage_converter(factor: float):
    def converter(voltage: float) -> float:
        return voltage * factor
    return converter



# Завдання 2. Лічильник електроенергії
def make_electricity_meter(address: str, initial_kwh: float = 0.0):
    kwh = initial_kwh

    def add(value: float) -> float:
        nonlocal kwh
        kwh += value
        return kwh

    def reset() -> float:
        nonlocal kwh
        kwh = initial_kwh
        return kwh

    def report() -> str:
        return f"Адреса: {address} | Спожито: {kwh} кВт·год"

    return add, reset, report


# Завдання 3. Диспетчер аварійних подій
def log_to_console(message: str):
    print(message)


def log_to_file(message: str):
    log_file = Path(__file__).parent / "dispatch_log.txt"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def make_dispatcher(station_name: str):
    def dispatch(event: str, callback):
        message = f"[{station_name}] {event}"
        callback(message)
    return dispatch


# Завдання 4. Сортування підстанцій
def make_sorter(field: str, reverse: bool = False):
    def sorter(substations_list: list) -> list:
        return sorted(substations_list, key=lambda item: item[field], reverse=reverse)
    return sorter


#  Захисний автомат 
def make_circuit_breaker(max_failures: int):
    failures_count = 0

    def protect(func):
        def wrapper(*args, **kwargs):
            nonlocal failures_count
            if failures_count >= max_failures:
                raise RuntimeError("Автомат вимкнено!")
            try:
                return func(*args, **kwargs)
            except Exception as e:
                failures_count += 1
                raise e
        return wrapper

    return protect


# Перевірка коду
if __name__ == "__main__":
    print("=== Завдання 1 ===")
    step_up = make_voltage_converter(10.0)
    step_down = make_voltage_converter(0.5)

    print(step_up(22.0))     # 220.0
    print(step_down(220.0))  # 110.0
    print(step_up(11.0))     # 110.0

    print("\n=== Завдання 2 ===")
    add, reset, report = make_electricity_meter("вул. Франка, 12", 150.0)

    print(add(30.5))    # 180.5
    print(add(14.0))    # 194.5
    print(report())     # Адреса: вул. Франка, 12 | Спожито: 194.5 кВт·год
    print(reset())      # 150.0
    print(report())     # Адреса: вул. Франка, 12 | Спожито: 150.0 кВт·год

    print("\n=== Завдання 3 ===")
    dispatch = make_dispatcher("Підстанція №7 Івано-Франківськ")

    dispatch("Перевищення напруги", log_to_console)
    dispatch("Коротке замикання", log_to_console)
    dispatch("Відновлення живлення", log_to_file)

    print("\n=== Завдання 4 ===")
    substations = [
        {"name": "Підстанція №3", "region": "Коломия",         "load_kw": 4500},
        {"name": "Підстанція №7", "region": "Івано-Франківськ", "load_kw": 8200},
        {"name": "Підстанція №1", "region": "Калуш",           "load_kw": 3100},
        {"name": "Підстанція №9", "region": "Надвірна",        "load_kw": 6700},
    ]

    sort_by_load = make_sorter("load_kw", reverse=True)
    for s in sort_by_load(substations):
        print(s["name"], s["load_kw"])

    print()
    sort_by_name = make_sorter("name")
    for s in sort_by_name(substations):
        print(s["name"])

    print("\n=== Бонус ===")
    breaker = make_circuit_breaker(max_failures=2)

    def unstable_sensor():
        raise ConnectionError("Сенсор не відповідає")

    safe_sensor = breaker(unstable_sensor)

    for i in range(1, 5):
        try:
            safe_sensor()
        except Exception as err:
            print(f"Спроба {i}: {type(err).__name__}: {err}")