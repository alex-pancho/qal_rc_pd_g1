class QuestRoom:
    def __init__(self, name_room, level, max_players):
        self.name_room = name_room
        self.level = level # від 1 до 5
        self.max_players = max_players
        self.players_list = []
        self.status = "waiting"  # "waiting", "active", "finished"
        self.events_log = []

    def add_player(self, name):
        if self.status != "waiting":
            return f"Cannot add players! Room is {self.status}."#додавання гравця лише в статусі вейтінг
        if len(self.players_list) >= self.max_players:
            return "No free slots!"
        else:
            self.players_list.append(name) 
            self.events_log.append(f"Player {name} joined")  
            return self.players_list 
        
    def  start(self):
        if len(self.players_list) < 1:
           return "Room is empty!"
        self.status = "active"  
        self.events_log.append("Quest started")  # Логування при старті
        return f"Quest {self.name_room} started with {len(self.players_list)} players!" 
        
    def __str__(self):
        return f"QuestRoom: {self.name_room} | Difficulty: {self.level} | Players: {len(self.players_list)}/{self.max_players}"  
    
    def remove_player(self, name):
        if self.status != "waiting":
            return f"Cannot remove players! Room is {self.status}."
        if name in self.players_list:
            self.players_list.remove(name)
            self.events_log.append(f"Player {name} left")  # Логування при видаленні
            return self.players_list 
        return "Player not found!"
        
    def is_full(self):
        if len(self.players_list) == self.max_players:
            return True
        else:
            return False
    def free_slots(self):
        free_place = self.max_players - len(self.players_list)
        return free_place 
    
    def reset_room(self):
        self.status = "finished"      # 1. Змінює стан на "finished"
        self.players_list.clear()     # 2. Очищає гравців
        self.status = "waiting"       # 3. Ставить "waiting"
        self.events_log.append("Room reset")  # Логування при рестарті
        return "Room reset!" 
     
    def get_players_list(self):
        if len(self.players_list) == 0:
            return "No players in the room"
        else:
            return self.players_list        


    def show_log(self):
        """Повертає історію всіх подій кімнати"""
        return self.events_log
      тести на перевірку дозволили не робити на уроці №11)))


        
