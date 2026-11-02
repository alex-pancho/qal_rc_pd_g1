class Cossack:
    def __init__(self, name: str, kurin: str, weapons: list = None):
        self.name = name
        self.kurin = kurin
        self.weapons = list(weapons) if weapons is not None else []
        self.victories = 0
        self.rank = "козак"

    def _update_rank(self):
        """Автоматичне оновлення звання залежно від перемог."""
        if self.victories >= 7:
            self.rank = "полковник"
        elif self.victories >= 3:
            self.rank = "осавул"
        else:
            self.rank = "козак"

    def arm(self, weapon: str):
        if weapon in self.weapons:
            return f"{self.name} вже має {weapon}!"
        self.weapons.append(weapon)

    def win_battle(self, enemy: str) -> str:
        self.victories += 1
        self._update_rank()
        return f"{self.name} переміг {enemy}! Слава козаку!"

    def __str__(self) -> str:
        weapons_str = ", ".join(self.weapons) if self.weapons else "без зброї"
        return f"Козак {self.name} ({self.rank}) | Курінь: {self.kurin} | Перемоги: {self.victories} | Зброя: {weapons_str}"


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

    def dismiss(self, name: str):
        for c in self.cossacks:
            if c.name == name:
                self.cossacks.remove(c)
                return
        return f"Козака {name} не знайдено!"

    def call_to_battle(self, enemy: str) -> str:
        if not self.cossacks:
            return "Нікому боронити Січ!"
        return f"Військо Запорозьке виступає проти {enemy}! У поході {len(self.cossacks)} козаків!"

    def best_warrior(self):
        if not self.cossacks:
            return "Січ порожня!"
        return max(self.cossacks, key=lambda c: c.victories)

    def roster(self):
        if not self.cossacks:
            return "На Січі нікого немає"
        return [c.name for c in self.cossacks]

    def promote_all(self):
        """Переглядає та оновлює звання всіх козаків."""
        for cossack in self.cossacks:
            cossack._update_rank()


if __name__ == "__main__":
    sich = ZaporozhianSich("Чортомлицька Січ", capacity=3)

    ivan = Cossack("Іван Сірко", "Кальміуський")
    petro = Cossack("Петро Сагайдачний", "Канівський")

    ivan.arm("шабля")
    ivan.arm("мушкет")
    
    ivan.win_battle("яничари")
    ivan.win_battle("татари")
    petro.win_battle("поляки")

    sich.enlist(ivan)
    sich.enlist(petro)

    print(sich.call_to_battle("турки"))
    print("Найкращий воїн:", sich.best_warrior())
    print("Реєстр:", sich.roster())
    print(ivan)