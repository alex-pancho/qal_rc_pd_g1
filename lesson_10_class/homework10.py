class QuestRoom:
    def __init__(self, name: str, difficulty: int, limit: int):
        self.name = name
        self.difficulty = difficulty
        self.limit = limit
        self.players = []
        self.status = "waiting"     # waiting → active → finished → waiting
        self.events_log = []

    # -----------------------------
    # Додавання гравця
    # -----------------------------
    def add_player(self, name: str):
        if len(self.players) >= self.limit:
            return "No free slots!"
        self.players.append(name)
        self.events_log.append(f"Player {name} joined")
        return f"Player {name} added"

    # -----------------------------
    # Видалення гравця
    # -----------------------------
    def remove_player(self, name: str):
        if name not in self.players:
            return "Player not found!"
        self.players.remove(name)
        self.events_log.append(f"Player {name} left")
        return f"Player {name} removed"

    # -----------------------------
    # Перевірка заповненості
    # -----------------------------
    def is_full(self):
        return len(self.players) >= self.limit

    def free_slots(self):
        return self.limit - len(self.players)

    # -----------------------------
    # Старт квесту
    # -----------------------------
    def start(self):
        if not self.players:
            return "Room is empty!"
        self.status = "active"
        self.events_log.append("Quest started")
        return f"Quest '{self.name}' started with {len(self.players)} players!"

    # -----------------------------
    # Скидання кімнати
    # -----------------------------
    def reset_room(self):
        self.status = "finished"
        self.events_log.append("Room reset")
        self.players.clear()
        self.status = "waiting"
        return "Room reset!"

    # -----------------------------
    # Список гравців
    # -----------------------------
    def players_list(self):
        if not self.players:
            return "No players in the room"
        return self.players

    # -----------------------------
    # Лог подій
    # -----------------------------
    def show_log(self):
        return self.events_log

    # -----------------------------
    # Красивий вивід
    # -----------------------------
    def __str__(self):
        return (f"QuestRoom: {self.name} | Difficulty: {self.difficulty} | "
                f"Players: {len(self.players)}/{self.limit} | Status: {self.status}")

room = QuestRoom("Лабіринт Минотавра", 5, 3)

room.add_player("Анна")
room.add_player("Ігор")
room.add_player("Максим")

print(room.is_full())        # True
print(room.free_slots())     # 0

print(room.remove_player("Ігор"))
print(room.free_slots())     # 1

print(room.start())
print(room.reset_room())
print(room.players_list())
print(room.show_log())


юніт-тест
import unittest
from quest_room import QuestRoom

class TestQuestRoom(unittest.TestCase):

    def test_constructor(self):
        room = QuestRoom("Test", 3, 4)
        self.assertEqual(room.name, "Test")
        self.assertEqual(room.difficulty, 3)
        self.assertEqual(room.limit, 4)
        self.assertEqual(room.players, [])
        self.assertEqual(room.status, "waiting")
        self.assertEqual(room.events_log, [])

    def test_add_player(self):
        room = QuestRoom("Test", 3, 2)
        room.add_player("A")
        self.assertIn("A", room.players)
        self.assertIn("Player A joined", room.events_log)

        room.add_player("B")
        self.assertEqual(room.add_player("C"), "No free slots!")

    def test_remove_player(self):
        room = QuestRoom("Test", 3, 3)
        room.add_player("A")
        self.assertEqual(room.remove_player("A"), "Player A removed")
        self.assertEqual(room.remove_player("X"), "Player not found!")

    def test_is_full(self):
        room = QuestRoom("Test", 3, 2)
        room.add_player("A")
        self.assertFalse(room.is_full())
        room.add_player("B")
        self.assertTrue(room.is_full())

    def test_start(self):
        room = QuestRoom("Test", 3, 3)
        self.assertEqual(room.start(), "Room is empty!")
        room.add_player("A")
        msg = room.start()
        self.assertIn("started", msg)
        self.assertEqual(room.status, "active")

    def test_reset_room(self):
        room = QuestRoom("Test", 3, 3)
        room.add_player("A")
        room.start()
        room.reset_room()
        self.assertEqual(room.players, [])
        self.assertEqual(room.status, "waiting")
        self.assertIn("Room reset", room.events_log)

    def test_players_list(self):
        room = QuestRoom("Test", 3, 3)
        self.assertEqual(room.players_list(), "No players in the room")
        room.add_player("A")
        self.assertEqual(room.players_list(), ["A"])

    def test_show_log(self):
        room = QuestRoom("Test", 3, 3)
        room.add_player("A")
        room.start()
        room.reset_room()
        self.assertEqual(
            room.show_log(),
            ["Player A joined", "Quest started", "Room reset"]
        )

if __name__ == "__main__":
    unittest.main()

