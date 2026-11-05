#Завдання 1: Клас Cossackм
class Cossack:
    def __init__(self, name: str, kurin: str, weapons=None):
        self.name = name
        self.kurin = kurin
        self.weapons = weapons if weapons else []
        self.__victories = 0   # інкапсуляція
        self.rank = "козак"    # базове звання

    def arm(self, weapon: str):
        if weapon in self.weapons:
            return f"{self.name} вже має {weapon}!"
        self.weapons.append(weapon)
        return f"{self.name} озброївся: {weapon}"

    def win_battle(self, enemy: str):
        self.__victories += 1
        self._update_rank()
        return f"{self.name} переміг {enemy}! Слава козаку!"

    def get_victories(self):
        return self.__victories

    def _update_rank(self):
        if self.__victories >= 7:
            self.rank = "полковник"
        elif self.__victories >= 3:
            self.rank = "осавул"

    def __str__(self):
        weapons = ", ".join(self.weapons) if self.weapons else "без зброї"
        return (f"Козак {self.name} | Курінь: {self.kurin} | "
                f"Перемоги: {self.__victories} | Звання: {self.rank} | "
                f"Зброя: {weapons}")


# Завдання 2: Спадкування — елітні козаки
class Sharpshooter(Cossack):
    def battle_cry(self):
        return f"{self.name} вигукує: Точно в ціль!"

class SabreMaster(Cossack):
    def battle_cry(self):
        return f"{self.name} вигукує: За шаблю і волю!"


# Завдання 3: Композиція — клас ZaporozhianSich
class ZaporozhianSich:
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.cossacks = []

    def enlist(self, cossack: Cossack):
        if len(self.cossacks) >= self.capacity:
            return "Січ переповнена!"
        if any(c.name == cossack.name for c in self.cossacks):
            return f"{cossack.name} вже на Січі!"
        self.cossacks.append(cossack)
        return f"{cossack.name} прибув на Січ!"

    def dismiss(self, name: str):
        for c in self.cossacks:
            if c.name == name:
                self.cossacks.remove(c)
                return f"{name} покинув Січ."
        return f"Козака {name} не знайдено!"

    def call_to_battle(self, enemy: str):
        if not self.cossacks:
            return "Нікому боронити Січ!"
        return (f"Військо Запорозьке виступає проти {enemy}! "
                f"У поході {len(self.cossacks)} козаків!")

    def best_warrior(self):
        if not self.cossacks:
            return "Січ порожня!"
        return max(self.cossacks, key=lambda c: c.get_victories())

    def roster(self):
        if not self.cossacks:
            return "На Січі нікого немає"
        return [c.name for c in self.cossacks]

    def promote_all(self):
        for c in self.cossacks:
            c._update_rank()
        return "Усі козаки перевірені та підвищені за заслуги!"

# Завдання 4: Поліморфізм у дії
def make_battle_cry(cossack):
    # duck typing — важливий метод, а не тип
    return cossack.battle_cry()

# Завдання 5: Статичний та класовий методи
class CossackFactory:
    @staticmethod
    def validate_name(name: str):
        return bool(name) and len(name) <= 50

    @classmethod
    def from_string(cls, data: str):
        name, kurin = data.split(";")
        return Cossack(name.strip(), kurin.strip())




if __name__ == "__main__":
    sich = ZaporozhianSich("Чортомлицька Січ", capacity=3)

    ivan = Sharpshooter("Іван Сірко", "Кальміуський")
    petro = SabreMaster("Петро Сагайдачний", "Канівський")

    ivan.arm("мушкет")
    petro.arm("шабля")

    ivan.win_battle("яничари")
    ivan.win_battle("татари")
    petro.win_battle("поляки")

    print(sich.enlist(ivan))
    print(sich.enlist(petro))

    print(sich.call_to_battle("турки"))
    print(sich.best_warrior())
    print(sich.roster())

    print(make_battle_cry(ivan))
    print(make_battle_cry(petro))



