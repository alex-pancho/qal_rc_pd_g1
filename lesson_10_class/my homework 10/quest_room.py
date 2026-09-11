class QuestRoom:
    def __init__(self, name: str, difficulty: int, limit: int):
        self.name = name
        self.difficulty = difficulty
        self.limit = limit
        self.players = []
        self.status = "waiting"
        self.events_log = []

    def add_player(self, name: str):
        if len(self.players) >= self.limit:
            return "No free slots!"
        self.players.append(name)
        self.events_log.append(f"Player {name} joined")

    def remove_player(self, name: str):
        if name not in self.players:
            return "Player not found!"
        self.players.remove(name)
        self.events_log.append(f"Player {name} left")

    def is_full(self) -> bool:
        return len(self.players) >= self.limit

    def free_slots(self) -> int:
        return max(0, self.limit - len(self.players))

    def start(self) -> str:
        if not self.players:
            return "Room is empty!"
        self.status = "active"
        self.events_log.append("Quest started")
        return f"Quest '{self.name}' started with {len(self.players)} players!"

    def reset_room(self) -> str:
        self.status = "finished"
        self.players.clear()
        self.events_log.append("Room reset")
        self.status = "waiting"
        return "Room reset!"

    def players_list(self):
        if not self.players:
            return "No players in the room"
        return self.players.copy()

    def show_log(self) -> list:
        return self.events_log.copy()

    def __str__(self) -> str:
        return f"QuestRoom: {self.name} | Difficulty: {self.difficulty} | Players: {len(self.players)}/{self.limit}"