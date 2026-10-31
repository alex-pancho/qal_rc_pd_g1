class ChainOfOrders:
    def __init__(self, names):
        self.names = names
        self.index = 0

        self.dative_names = {
            "Батько": "Батькові",
            "Михайлик": "Михайлику",
            "Василько": "Василькові",
        }

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.names):
            raise StopIteration

        current_name = self.names[self.index]

        if self.index == len(self.names) - 1:
            message = f"{current_name} каже: теля прив'язав!"
        else:
            next_name = self.names[self.index + 1]
            next_name_dative = self.dative_names.get(
                next_name, next_name
            )
            message = (
                f"{current_name} каже {next_name_dative}: "
                "передай далі!"
            )

        self.index += 1
        return message

chain = ChainOfOrders(["Дід", "Батько", "Михайлик", "Василько"])
#chain = ChainOfOrders(["Василько"])

for message in chain:
    print(message)

print("-----")

def village_rumor(start_message, people):
    message = start_message

    for i, person in enumerate(people):
        # Перша людина передає початкове повідомлення
        if i == 0:
            if len(people) == 1:
                yield f'{person} каже: "{message}(і всі дізналися!)"'
            else:
                yield f'{person} каже: "{message}"'

        else:
            # Додаємо до чутки переказ попередньої людини
            previous_person = people[i - 1]
            message += f" (переказала {previous_person})"

            # Остання людина завершує ланцюжок
            if i == len(people) - 1:
                message += " і всі дізналися!"

            yield f'{person} переказує: "{message}"'

for version in village_rumor("Теля втекло!",["Горпина", "Параска", "Явдоха", "Оксана"]
):
        
    print(version)


print("-----")


events = [
    "Михайлик передав доручення",
    "Василько відмовився",
    "Грицько передав доручення",
    "Оленка прив'язала теля",
    "Данилко передав доручення",
]

count = sum(
    1 for name in (
        event.split(" передав доручення")[0]
        for event in events
        if event.endswith(" передав доручення")
    )
)

print(f"Доручення передавали {count} рази")


print("-----")

def toloka_queue(workers):
    if not workers:
        return

    while True:
        for worker in workers:
            yield f"Черга: {worker}"

import itertools

queue = toloka_queue(["Іван", "Марія", "Степан"])

for turn in itertools.islice(queue, 7):
    print(turn)

        
print("-----")

def find_calf(log):
    for line in log:
        if "прив'язав" in line or "прив'язала" in line:
            yield line
            return

journal = [
    "Михайлик отримав доручення",
    "Михайлик передав Василькові",
    "Василько загрався",
    "Василько передав Оленці",
    "Оленка прив'язала теля біля хліва",
    "Оленка пішла додому",
    "Дід заспокоївся",
]

result = next(find_calf(journal))
print(result)
        
