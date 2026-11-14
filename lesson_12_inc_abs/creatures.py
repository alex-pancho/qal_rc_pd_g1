from abc import ABC, abstractmethod


class MagicCreature(ABC):
    def __init__(self, name: str, magic_level: int, health: int):
        self.name = name
        self._validate_magic_level(magic_level)
        self._magic_level = magic_level

        self._validate_health(health)
        self.__health = health
        self.__alive = health > 0

    # Валідатори
    def _validate_magic_level(self, value: int):
        if not (1 <= value <= 10):
            raise ValueError("Рівень магії має бути від 1 до 10!")

    def _validate_health(self, value: int):
        if not (0 <= value <= 100):
            raise ValueError("Здоров'я має бути від 0 до 100!")

    # Properties
    @property
    def magic_level(self) -> int:
        return self._magic_level

    @magic_level.setter
    def magic_level(self, value: int):
        self._validate_magic_level(value)
        self._magic_level = value

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, value: int):
        self._validate_health(value)
        self.__health = value
        if self.__health == 0:
            self.__alive = False

    @property
    def is_alive(self) -> bool:
        return self.__alive

    # Абстрактні методи
    @abstractmethod
    def use_ability(self) -> str:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass

    # Публічні методи
    def take_damage(self, amount: int):
        if not self.__alive:
            return f"{self.name} вже переміг смерть... або ні."

        new_health = max(0, self.__health - amount)
        self.health = new_health

    def __str__(self) -> str:
        return f"{self.name} | Магія: {self.magic_level} | HP: {self.health} | Живий: {self.is_alive}"


class Molfar(MagicCreature):
    def __init__(self, name: str, magic_level: int, health: int, element: str, spells: int):
        super().__init__(name, magic_level, health)
        self.element = element
        self.spells = spells

    @property
    def spells(self) -> int:
        return self.__spells

    @spells.setter
    def spells(self, value: int):
        if value < 0:
            raise ValueError("Кількість заклинань не може бути від'ємною!")
        self.__spells = value

    def use_ability(self) -> str:
        if self.spells > 0:
            self.spells -= 1
            return f"Мольфар {self.name} закликає {self.element}! Залишилось заклинань: {self.spells}"
        return f"Мольфар {self.name} виснажений — сила стихій покинула його!"

    def describe(self) -> str:
        return f"Мольфар {self.name}, повелитель стихії {self.element}. Рівень магії: {self.magic_level}"


class Rusalka(MagicCreature):
    def __init__(self, name: str, magic_level: int, health: int, river: str, charm_power: int):
        super().__init__(name, magic_level, health)
        self.river = river
        self.charm_power = charm_power

    @property
    def charm_power(self) -> int:
        return self.__charm_power

    @charm_power.setter
    def charm_power(self, value: int):
        if not (1 <= value <= 5):
            raise ValueError("Сила чар має бути від 1 до 5!")
        self.__charm_power = value

    def use_ability(self) -> str:
        res = f"Русалка {self.name} з річки {self.river} зачаровує мандрівника! Сила чар: {self.charm_power}"
        if self.charm_power == 5:
            res += " Ніхто не встоїть!"
        return res

    def describe(self) -> str:
        return f"Русалка {self.name}, мешканка річки {self.river}. Сила чар: {self.charm_power}/5"


class Perelesnyk(MagicCreature):
    def __init__(self, name: str, magic_level: int, health: int, speed: int, form: str = "вогняна куля"):
        super().__init__(name, magic_level, health)
        self.speed = speed
        self.form = form

    @property
    def speed(self) -> int:
        return self.__speed

    @speed.setter
    def speed(self, value: int):
        if not (1 <= value <= 100):
            raise ValueError("Швидкість має бути від 1 до 100!")
        self.__speed = value

    def change_form(self) -> str:
        self.form = "людська" if self.form == "вогняна куля" else "вогняна куля"
        return f"Перелесник перетворився на {self.form}!"

    def use_ability(self) -> str:
        res = f"Перелесник {self.name} мчить крізь ніч зі швидкістю {self.speed}! Форма: {self.form}"
        if self.form == "людська":
            res += " Ніхто не здогадається..."
        return res

    def describe(self) -> str:
        return f"Перелесник {self.name}. Швидкість: {self.speed}. Зараз у формі: {self.form}"


class EnchantedForest:
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.__creatures = []

    @property
    def creatures_count(self) -> int:
        return len([c for c in self.__creatures if c.is_alive])

    def add_creature(self, creature: MagicCreature):
        if len(self.__creatures) >= self.capacity:
            return f"Зачарований ліс {self.name} переповнений!"
        if not creature.is_alive:
            return "Мертві істоти не можуть оселитись у лісі!"
        if any(c.name == creature.name for c in self.__creatures):
            return f"{creature.name} вже мешкає у цьому лісі!"
        
        self.__creatures.append(creature)

    def remove_creature(self, name: str):
        for c in self.__creatures:
            if c.name == name:
                self.__creatures.remove(c)
                return
        return f"Істоту {name} не знайдено у лісі!"

    def most_powerful(self):
        if not self.__creatures:
            return "Ліс порожній — нема кому чаклувати!"
        return max(self.__creatures, key=lambda c: c.magic_level)

    def attack_intruder(self, intruder_name: str):
        alive_creatures = [c for c in self.__creatures if c.is_alive]
        if not alive_creatures:
            return f"Ліс беззахисний перед {intruder_name}!"
        return [c.use_ability() for c in alive_creatures]

    def census(self):
        if not self.__creatures:
            return "Ліс порожній"
        return [c.describe() for c in self.__creatures]


# --- Перевірка роботи ---
if __name__ == "__main__":
    forest = EnchantedForest("Чорний Ліс", capacity=5)

    molfar = Molfar("Юрій", magic_level=8, health=90, element="вогонь", spells=3)
    rusalka = Rusalka("Калина", magic_level=6, health=100, river="Дніпро", charm_power=5)
    perelesnyk = Perelesnyk("Іскра", magic_level=7, health=85, speed=95, form="вогняна куля")

    forest.add_creature(molfar)
    forest.add_creature(rusalka)
    forest.add_creature(perelesnyk)

    print("Найсильніший:", forest.most_powerful())
    print("\nАтака чужинця:")
    for attack in forest.attack_intruder("мисливець"):
        print(" -", attack)

    molfar.take_damage(90)
    print("\nМольфар живий після 90 шкоди?:", molfar.is_alive)

    print("\nПерепис істот у лісі:")
    print(forest.census())