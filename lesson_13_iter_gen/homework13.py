import itertools


# ============================================================
# Завдання 1: Ітератор ChainOfOrders
# ============================================================

class ChainOfOrders:
    def __init__(self, people):
        self.people = people
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Порожній список
        if not self.people:
            raise StopIteration

        # Один елемент
        if len(self.people) == 1:
            if self.index == 0:
                self.index += 1
                return f"{self.people[0]} каже: теля прив'язав!"
            raise StopIteration

        # Більше елементів
        if self.index < len(self.people) - 1:
            msg = f"{self.people[self.index]} каже {self.people[self.index + 1]}ові: передай далі!"
            self.index += 1
            return msg
        elif self.index == len(self.people) - 1:
            msg = f"{self.people[self.index]} каже: теля прив'язав!"
            self.index += 1
            return msg
        else:
            raise StopIteration


# ============================================================
# Завдання 2: Генератор village_rumor
# ============================================================

def village_rumor(start_message, people):
    if not people:
        return

    # Перша людина каже оригінальне повідомлення
    message = start_message
    yield f'{people[0]} каже: "{message}"'

    # Далі кожен додає "(переказав <ім'я>)"
    history = f"(переказала {people[0]})"

    for name in people[1:-1]:
        yield f'{name} переказує: "{message} {history}"'
        history += f" (переказала {name})"

    # Остання людина
    last = people[-1]
    yield f'{last} переказує: "{message} {history} (і всі дізналися!)"'


# ============================================================
# Завдання 3: Генераторний вираз
# ============================================================

def count_transfers(events):
    # Один рядок — генераторний вираз
    return sum(
        1
        for e in events
        if "передав доручення" in e
    )


# ============================================================
# Завдання 4: Нескінченний генератор toloka_queue
# ============================================================

def toloka_queue(workers):
    index = 0
    while True:
        yield f"Черга: {workers[index]}"
        index = (index + 1) % len(workers)


# ============================================================
# Завдання 5: Ліниве читання find_calf
# ============================================================

def find_calf(log):
    for line in log:
        if "прив'язав" in line or "прив'язала" in line:
            yield line
            return  # Зупиняємо генератор після першого знайденого


# ============================================================
# Демонстрація роботи (можеш залишити або видалити)
# ============================================================

if __name__ == "__main__":
    print("=== ChainOfOrders ===")
    chain = ChainOfOrders(["Дід", "Батько", "Михайлик", "Василько"])
    for msg in chain:
        print(msg)

    print("\n=== village_rumor ===")
    for version in village_rumor("Теля втекло!", ["Горпина", "Параска", "Явдоха", "Оксана"]):
        print(version)

    print("\n=== count_transfers ===")
    events = [
        "Михайлик передав доручення",
        "Василько відмовився",
        "Грицько передав доручення",
        "Оленка прив'язала теля",
        "Данилко передав доручення",
    ]
    print(f"Доручення передавали {count_transfers(events)} рази")

    print("\n=== toloka_queue ===")
    queue = toloka_queue(["Іван", "Марія", "Степан"])
    for turn in itertools.islice(queue, 7):
        print(turn)

    print("\n=== find_calf ===")
    journal = [
        "Михайлик отримав доручення",
        "Михайлик передав Василькові",
        "Василько загрався",
        "Василько передав Оленці",
        "Оленка прив'язала теля біля хліва",
        "Оленка пішла додому",
        "Дід заспокоївся",
    ]
    print(next(find_calf(journal)))
