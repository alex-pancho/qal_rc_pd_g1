import unittest
from quest_room import QuestRoom


class TestQuestRoom(unittest.TestCase):

    def setUp(self):
        """Створюємо новий об'єкт кімнати перед кожним тестом"""
        self.room = QuestRoom("Піратський острів", 3, 2)

    # 1. Тести конструктора
    def test_init(self):
        self.assertEqual(self.room.name, "Піратський острів")
        self.assertEqual(self.room.difficulty, 3)
        self.assertEqual(self.room.limit, 2)
        self.assertEqual(self.room.players, [])
        self.assertEqual(self.room.status, "waiting")
        self.assertEqual(self.room.events_log, [])

    # 2. Тести додавання гравців (add_player)
    def test_add_player_success(self):
        self.room.add_player("Олег")
        self.assertIn("Олег", self.room.players)
        self.assertIn("Player Олег joined", self.room.show_log())

    def test_add_player_limit_exceeded(self):
        self.room.add_player("Олег")
        self.room.add_player("Даша")
        result = self.room.add_player("Ігор")
        self.assertEqual(result, "No free slots!")
        self.assertEqual(len(self.room.players), 2)

    # 3. Тести видалення гравців (remove_player)
    def test_remove_player_success(self):
        self.room.add_player("Олег")
        self.room.remove_player("Олег")
        self.assertNotIn("Олег", self.room.players)
        self.assertIn("Player Олег left", self.room.show_log())

    def test_remove_player_not_found(self):
        result = self.room.remove_player("Невідомий")
        self.assertEqual(result, "Player not found!")

    # 4. Перевірка заповненості (is_full, free_slots)
    def test_is_full_and_free_slots(self):
        self.assertFalse(self.room.is_full())
        self.assertEqual(self.room.free_slots(), 2)

        self.room.add_player("Олег")
        self.assertFalse(self.room.is_full())
        self.assertEqual(self.room.free_slots(), 1)

        self.room.add_player("Даша")
        self.assertTrue(self.room.is_full())
        self.assertEqual(self.room.free_slots(), 0)

    # 5. Тести запуску (start)
    def test_start_empty_room(self):
        result = self.room.start()
        self.assertEqual(result, "Room is empty!")
        self.assertEqual(self.room.status, "waiting")

    def test_start_success(self):
        self.room.add_player("Олег")
        result = self.room.start()
        self.assertEqual(result, "Quest 'Піратський острів' started with 1 players!")
        self.assertEqual(self.room.status, "active")
        self.assertIn("Quest started", self.room.show_log())

    # 6. Тести скидання кімнати (reset_room)
    def test_reset_room(self):
        self.room.add_player("Олег")
        self.room.start()
        result = self.room.reset_room()

        self.assertEqual(result, "Room reset!")
        self.assertEqual(len(self.room.players), 0)
        self.assertEqual(self.room.status, "waiting")
        self.assertIn("Room reset", self.room.show_log())

    # 7. Список гравців (players_list)
    def test_players_list(self):
        self.assertEqual(self.room.players_list(), "No players in the room")
        self.room.add_player("Олег")
        self.assertEqual(self.room.players_list(), ["Олег"])

    # 8. Комбінований сценарій
    def test_combined_scenario(self):
        self.room.add_player("Олег")
        self.room.add_player("Даша")
        self.assertTrue(self.room.is_full())

        self.assertEqual(self.room.add_player("Максим"), "No free slots!")
        self.room.remove_player("Олег")
        self.assertFalse(self.room.is_full())

        self.room.add_player("Максим")
        self.assertTrue(self.room.is_full())

        log = self.room.show_log()
        expected_log = [
            "Player Олег joined",
            "Player Даша joined",
            "Player Олег left",
            "Player Максим joined"
        ]
        self.assertEqual(log, expected_log)


if __name__ == "__main__":
    unittest.main()