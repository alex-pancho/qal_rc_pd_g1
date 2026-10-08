from unicodedata import name


class Cossack:
    def __init__(self, name, weapons, kurin, victories, rank = "козак"):
        self.name = name
        self.kurin = kurin
        self.weapons = list(weapons)
        self.victories = victories
        self.rank = rank

    def __str__(self):
        return f"Козак {self.name}   Курінь: {self.kurin}   Перемоги: {self.victories}   Зброя: {', '.join(self.weapons)}   Ранг: {self.rank}"

    def arm(self, weapons):
        if weapons in self.weapons:
            return f"{self.name} вже має {weapons}!"
        
        self.weapons.append(weapons)
        return f"{self.name} тепер має {weapons}!"
    
    def win_battle(self, enemy):
        if isinstance(enemy, Cossack):
            self.victories += 1
            return f"{self.name} переміг {enemy.name}! Слава козаку!"
        else:
            return f"{self.name} переміг {enemy}! Слава козаку!"


ivan = Cossack("Іван Сірко", ["шабля", "мушкет"], "Кальміуський", 5, "осавул")
petro = Cossack("Петро Сагайдачний", ["пістолет"], "Канівський", 3, "козак")
vasil = Cossack("Василь Остріков", ["спис"], "Запорізький", 2, "осавул")
boris = Cossack("Борис Гонта", ["пістолет"], "Канівський", 1, "козак")
sasha = Cossack("Саша Білоус", ["клинок"], "Татарський", 4, "осавул")

print(ivan)
print(petro) 

        
print(ivan.arm("шабля, мушкет"))  # "Іван Сірко вже має шабля!"
print(petro.arm("пістолет"))  # "Петро Сагайда
print(boris.arm("пістолет, мушкет"))  # "Борис Гонта вже має пістолет!"
print(vasil.arm("спис"))  # "Василь Остріков тепер має спис!"

print(ivan.win_battle("Татарина"))  # "Іван Сірко переміг Татарин! Слава козаку!"
print(ivan.win_battle("поляка"))  # "Іван Сірко переміг Татарин! Слава козаку!"

class ZaporozhianSich:
    def __init__(self, name, capacity = 1000, cossacks = None):
        self.name = name
        self.capacity = capacity
        self.cossacks = cossacks if cossacks is not None else []
        
    def enlist(self, cossack):        
            if len(self.cossacks) >= self.capacity:
                return "Січ переповнена!"
    
            if cossack in self.cossacks:
                return f"{cossack.name} вже на Січі!"
    
            self.cossacks.append(cossack)

    def __str__(self):
        return f"Козаки {', '.join(cossack.name for cossack in self.cossacks)} знаходяться на Січі {self.name}."

            
    def dismiss(self, name):
        for cossack in self.cossacks:
            if cossack.name == name:
                self.cossacks.remove(cossack)
                return f"{cossack.name} був відправлений у відставку."
        return f"Козака {name} не знайдено!"

    def call_to_battle(self, enemy):
        if not self.cossacks:
            return f"Нікому боронити Січ!"
        else:
            return f"Військо Запорозьке виступає проти {enemy}! У поході {len(self.cossacks)} козаків!"

        
    def best_warrior(self):
        if not self.cossacks:
            return "Січ порожня!"
        
        best = max(self.cossacks, key=lambda c: c.victories)

        return f"Найкращий козак: {best.name} з {best.victories} перемогами."


    def roster(self):
        if not self.cossacks:
            return "На Січі нікого немає"
        return [cossack.name for cossack in self.cossacks]
    
    
    def promote_all(self):
        for cossack in self.cossacks:
            if cossack.victories >= 7:
                cossack.rank = "полковник"
        
            elif cossack.victories >= 3:
                cossack.rank = "осавул"
        
            else:
                cossack.rank = "козак" 

sich = ZaporozhianSich("Чортомлицька Січ", capacity = 7, cossacks=[ivan, petro, vasil, boris, sasha])

pavlo = Cossack("Павло Павленко", "пістолет, мушкет", "Канівський", 1, "козак")
kurilo = Cossack("Курило Кривоніс", "шабля, спис", "Запорізький", 2, "осавул")
    
print(sich.enlist(pavlo)) # Додаємо Павла Павленко
print(sich.enlist(kurilo)) # Додаємо Курила Кривоноса
print(sich.dismiss("Петро Сагайдачний"))  # "Петро Сагайдачний був відправлений у відставку."
print(sich.dismiss("Вова Калнишевський"))  # "Іван Сірко був відправлений у відставку."
print(sich.call_to_battle("яничарів"))  # "Військо Запорозьке виступає проти яничарів! У поході 6 козаків!"    
print(sich.best_warrior())
print(sich.roster())
print(ivan.rank)