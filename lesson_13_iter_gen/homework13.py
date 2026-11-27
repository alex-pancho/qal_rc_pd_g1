class ChainOfOrders:
    def __init__(self, people):
        self.people = people
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.people):
            raise StopIteration

        current = self.people[self.index]
        if self.index == len(self.people) - 1:
            result = f"{current} каже: О, я теля прив'язав!"
        else:
            next_person = self.people[self.index + 1]
            result = f"{current} каже {next_person}: нумо передай далі!"

        self.index += 1
        return result


chain = ChainOfOrders(["Дід", "Батько", "Михайлик", "Василько"])

for message in chain:
    print(message)


def village_rumor(start_message, people):
    if not people:
        return

    story = start_message
    yield f'{people[0]} каже: "{story}"'

    for i in range(1, len(people)):
        person = people[i]
        prev_person = people[i - 1]
        story += f" (переказала {prev_person})"

        if i == len(people) - 1:
            yield f'{person} переказує: "{story} (і всі дізналися!)"'
        else:
            yield f'{person} переказує: "{story}"'


for version in village_rumor("Теля втекло!", ["Горпина", "Параска", "Явдоха", "Оксана"]):
    print(version)


events = [
    "Михайлик передав доручення",
    "Василько відмовився",
    "Грицько передав доручення",
    "Оленка прив'язала теля",
    "Данилко передав доручення",
]

count = sum(
    1
    for name in (
        event.split(" передав доручення")[0]
        for event in events
        if "передав доручення" in event
    )
)

print(f"Доручення передавали {count} рази")
import itertools


def toloka_queue(workers):
    if not workers:
        return

    while True:
        for worker in workers:
            yield f"Черга: {worker}"


queue = toloka_queue(["Іван", "Марія", "Степан"])

for turn in itertools.islice(queue, 7):
    print(turn)
