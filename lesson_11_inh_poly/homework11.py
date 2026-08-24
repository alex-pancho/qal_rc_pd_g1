class Cossack:
    """козака Війська Запорозького"""
    def __init__(self, name, kurin, weapons):
        self.name = name
        self.kurin = kurin #підрозділ, до якого належить
        self.weapons = [] # зброя
        self.victories:int  = 0 # кількість перемог

    def arm(self, weapon):  # додає зброю до арсеналу
        if weapon in   self.weapons:
            return f"{self.name} вже має {weapon}"
        self.weapons.append(weapon) 
        return self.weapons  

    def win_battle(self, enemy): # збільшує лічильник перемог
        self.victories += 1
        return f"{self.name} переміг {enemy}! Слава козаку!"
    def __str__(self):
        weapons_str = ", ".join(self.weapons)
        return f"Козак {self.name} | Курінь: {self.kurin} | Перемоги: {self.victories} | Зброя: {weapons_str}"

cossack = Cossack("Іван Сірко", "Кальміуський", [])

cossack.arm("шабля")
cossack.arm("мушкет")
print(cossack.win_battle("яничари"))
print(cossack)

class ZaporozhianSich:
    def __init__(self, name, cossacks, capacity):
        self.name = name
        self.cossacks = cossacks #список козаків
        self.capacity = capacity #максимальну кількість козаків

    def enlist(self, cossack):
        """приймає об'єкт класу `Cossack` і додає його до Січі"""  
        if len(self.cossacks) >= self.capacity:
            return f"'Січ переповнена!'"
        for c in self.cossacks:
            if c.name == cossack.name:
                return f"{cossack.name} вже на Січі!"
        self.cossacks.append(cossack)
        return self.cossacks

    def dismiss(self, name):
        for c in self.cossacks:
            if c.name == name:  # 1. Порівнюємо з вхідним рядком 'name'
                self.cossacks.remove(c)  # 2. Видаляємо знайдений ОБ'ЄКТ 'c'
                return self.cossacks
        else:
            return f"'Козака {name} не знайдено!'"

    def call_to_battle(self, enemy):
        if len(self.cossacks) < 1:
            return f"'Нікому боронити Січ!'"  
        return f"'Військо Запорозьке виступає проти {enemy}! У поході {len(self.cossacks)} козаків!'" 

    def best_warrior(self):
        if len(self.cossacks) < 1:
            return "Січ порожня!"
        top_warrior = max(self.cossacks, key=lambda c: c.victories)
        return top_warrior  

    def roster(self):
        if len(self.cossacks) < 1:
            return f"'На Січі нікого немає'"
        return self.cossacks