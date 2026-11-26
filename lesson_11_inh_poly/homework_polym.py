class Cossack:
    def __init__(self, name: str, kurin: str, weapons: list[str] | None = None):
        self.name = name
        self.kurin = kurin
        self.weapons: list[str] = list(weapons) if weapons is not None else []
        self.victories: int = 0
        self.rank: str = "козак"

    def _update_rank(self) -> None:
        if self.victories >= 7:
            self.rank = "полковник"
        elif self.victories >= 3:
            self.rank = "осавул"
        else:
            self.rank = "козак"

    def arm(self, weapon: str) -> str | None:
        if weapon in self.weapons:
            return f"{self.name} вже має {weapon}!"
        self.weapons.append(weapon)
        return None

    def win_battle(self, enemy: str) -> str:
        self.victories += 1
        self._update_rank()
        return f"{self.name} переміг {enemy}! Слава козаку!"

    def __str__(self) -> str:
        weapons_str = ", ".join(self.weapons) if self.weapons else "немає"
        return (
            f"Козак {self.name} | Курінь: {self.kurin} | Звання: {self.rank} | "
            f"Перемоги: {self.victories} | Зброя: {weapons_str}"
        )


class ZaporozhianSich:
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.cossacks: list[Cossack] = []

    def enlist(self, cossack: Cossack) -> str:
        if any(c.name == cossack.name for c in self.cossacks):
            return f"{cossack.name} вже на Січі!"
        if len(self.cossacks) >= self.capacity:
            return "Січ переповнена!"
        self.cossacks.append(cossack)
        return f"{cossack.name} зарахований до «{self.name}»."

    def dismiss(self, name: str) -> str:
        for idx, cossack in enumerate(self.cossacks):
            if cossack.name == name:
                self.cossacks.pop(idx)
                return f"Козака {name} звільнено зі Січі."
        return f"Козака {name} не знайдено!"

    def call_to_battle(self, enemy: str) -> str:
        if not self.cossacks:
            return "Нікому боронити Січ!"
        return (
            f"Військо Запорозьке виступає проти {enemy}! "
            f"У поході {len(self.cossacks)} козаків!"
        )

    def best_warrior(self) -> Cossack | str:
        if not self.cossacks:
            return "Січ порожня!"
        return max(self.cossacks, key=lambda c: c.victories)

    def roster(self) -> list[str] | str:
        if not self.cossacks:
            return "На Січі нікого немає"
        return [cossack.name for cossack in self.cossacks]

    def promote_all(self) -> None:
        for cossack in self.cossacks:
            cossack._update_rank()


if __name__ == "__main__":
    cossack = Cossack("Іван Сірко", "Кальміуський")
    cossack.arm("шабля")
    cossack.arm("мушкет")
    print(cossack.arm("шабля"))
    print(cossack.win_battle("яничари"))
    print(cossack)

    sich = ZaporozhianSich("Чортомлицька Січ", capacity=3)
    ivan = Cossack("Іван Сірко", "Кальміуський")
    petro = Cossack("Петро Сагайдачний", "Канівський")

    for _ in range(7):
        ivan.win_battle("яничари")
    for _ in range(3):
        petro.win_battle("поляки")

    print(sich.enlist(ivan))
    print(sich.enlist(petro))
    print(sich.enlist(ivan))

    print(sich.call_to_battle("турки"))
    print("Найкращий воїн:", sich.best_warrior())
    print("Реєстр:", sich.roster())

    sich.promote_all()
    print("Після оновлення звань:")
    print(" ", ivan)
    print(" ", petro)