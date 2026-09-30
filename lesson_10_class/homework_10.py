class QuestRoom:
    def __init__(self, name, level, limit_players):
       self.level = level
       self.limit_players = limit_players
       self.name = name
       self.players = []
       self.status = []
       self.events_log = []



    def add_players(self, name):
        self.players.append(name)
        self.events_log.append(f"Гравець {name} приєднується до гри.")
        if len(self.players) > self.limit_players:
            print("No free slots!")
            self.players.pop()

    def start(self):
        if len(self.players) == 0:
            print("Room is empty!")
        else:
            print(f"Quest '{self.name}' started with {len(self.players)} players!")
            self.status = "active"
            self.events_log.append("Quest started")

    def __str__(self):
        return f"QuestRoom: {self.name}, рівень: {self.level}, учасники: {len(self.players)}/ліміт: {self.limit_players}"

    def remove_player(self, name):
       if name in self.players:
           self.players.remove(name)
           self.events_log.append(f"Player {name} left the room.")
       else:
            print(f"Player {name} not found!")

    def is_full(self):
        if len(self.players) >= self.limit_players:
            return True
        else:
            return False

    def free_slots(self):
        if len(self.players) < self.limit_players:
            return f"Вільних місць: {self.limit_players - len(self.players)}"

    #def reset_room(self):
        #self.status = "finished"
        #self.players.clear()
        #self.status = "waiting"
        #self.events_log.append("Room reset")        
    
    def players_list(self):
        if self.players:
            return f"Список учасників: {', '.join(self.players)}"
        else:
            return "Список учасників порожній."

    def show_log(self):
        if self.events_log:
            return "\n".join(self.events_log)
        else:
            return (f"Журнал подій порожній.")
        

    
room = QuestRoom("Піратський острів", 4, 5)

room.add_players("Марк")
room.add_players("Тетяна")
room.add_players("Кирило")
room.add_players("Вікторія")
room.add_players("Максим")
room.add_players("Олександр")

room.remove_player("Кирило")
room.remove_player("Валентина")

print(room.players)
room.start()

print(room)
print(room.is_full())
print(room.free_slots())
#print(room.reset_room())
print(room.players_list())
print(room.status)
print(room.events_log)