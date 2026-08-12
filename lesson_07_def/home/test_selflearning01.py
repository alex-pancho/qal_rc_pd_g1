# test_selflearning.py
import unittest
# Важливо: файл selflearning_tasks.py має знаходитись у тій самій директорії,
# що й цей файл для успішного імпорту.

import selflearning01 as sl_tasks

class TestSelfLearningTasks(unittest.TestCase):

    def test_task_1_analyze_list(self):
        """Тест для Завдання 1: аналіз списку."""
        self.assertDictEqual(sl_tasks.analyze_list([1, 2, 3, 4, 5]), {'sum': 15, 'max': 5, 'min': 1, 'len': 5})
        self.assertDictEqual(sl_tasks.analyze_list([-1, -2, -3]), {'sum': -6, 'max': -1, 'min': -3, 'len': 3})
        self.assertDictEqual(sl_tasks.analyze_list([10]), {'sum': 10, 'max': 10, 'min': 10, 'len': 1})
        self.assertDictEqual(sl_tasks.analyze_list([]), {'sum': 0, 'max': None, 'min': None, 'len': 0},
                             "Перевірте випадок з порожнім списком. sum має бути 0, а max/min повинні бути None.")

    def test_task_2_get_sorted_list(self):
        """Тест для Завдання 2: сортування списку без зміни оригіналу."""
        original_list = [5, 2, 8, 1, 9]
        original_list_copy = original_list.copy()
        sorted_list = sl_tasks.get_sorted_list(original_list)
        self.assertEqual(sorted_list, [1, 2, 5, 8, 9], "Список відсортовано неправильно.")
        self.assertEqual(original_list, original_list_copy, "Оригінальний список не повинен змінюватися.")

    def test_task_3_greet(self):
        """Тест для Завдання 3: функція привітання."""
        self.assertEqual(sl_tasks.greet("Іван"), "Привіт, Іван!")
        self.assertEqual(sl_tasks.greet("Олена", "Доброго дня"), "Доброго дня, Олена!")
        self.assertEqual(sl_tasks.greet(name="Петро"), "Привіт, Петро!")
        self.assertEqual(sl_tasks.greet(name="Марія", greeting="Вітаю"), "Вітаю, Марія!")

    def test_task_4_multiply_all(self):
        """Тест для Завдання 4: використання *args."""
        self.assertEqual(sl_tasks.multiply_all(1, 2, 3), 6)
        self.assertEqual(sl_tasks.multiply_all(10, 0.5), 5)
        self.assertEqual(sl_tasks.multiply_all(), 1, "Випадок без аргументів має повертати 1.")
        self.assertEqual(sl_tasks.multiply_all(5), 5)

    def test_task_5_create_profile(self):
        """Тест для Завдання 5: використання **kwargs."""
        profile1 = sl_tasks.create_profile(name="Іван", age=25, status="active")
        self.assertIn("name: Іван", profile1)
        self.assertIn("age: 25", profile1)
        self.assertIn("status: active", profile1)
        # Перевірка сортування ключів
        profile2 = sl_tasks.create_profile(city="Lviv", name="Anna")
        self.assertEqual(profile2, "city: Lviv\nname: Anna", "Ключі мають бути відсортовані за абеткою.")

    def test_task_6_format_data(self):
        """Тест для Завдання 6: комбіновані аргументи."""
        res1 = sl_tasks.format_data("Products", "Apple", "Banana", separator=" | ")
        self.assertEqual(res1, "Products: Item: Apple | Item: Banana")
        res2 = sl_tasks.format_data("Fruits", "Orange", "Grape", separator=" & ", prefix="F")
        self.assertEqual(res2, "Fruits: F: Orange & F: Grape")
        res3 = sl_tasks.format_data("Cities", "Kyiv", "Lviv")
        self.assertEqual(res3, "Cities: Item: Kyiv, Item: Lviv")
        res4 = sl_tasks.format_data("Empty")
        self.assertEqual(res4, "Empty: ")
        res5 = sl_tasks.format_data("Single", "One", prefix="Num")
        self.assertEqual(res5, "Single: Num: One")

    def test_task_7_is_even_lambda(self):
        """Тест для Завдання 7: лямбда-функція."""
        self.assertIsNotNone(sl_tasks.is_even, "Змінна is_even не повинна бути None.")
        self.assertTrue(callable(sl_tasks.is_even), "is_even має бути функцією (lambda).")
        self.assertTrue(sl_tasks.is_even(2))
        self.assertFalse(sl_tasks.is_even(3))
        self.assertTrue(sl_tasks.is_even(0))
        self.assertFalse(sl_tasks.is_even(-5))

    def test_task_8_filter_positive_numbers(self):
        """Тест для Завдання 8: filter з лямбдою."""
        self.assertEqual(sl_tasks.filter_positive_numbers([-1, 2, -3, 4, 0, 5]), [2, 4, 5])
        self.assertEqual(sl_tasks.filter_positive_numbers([1, 2, 3]), [1, 2, 3])
        self.assertEqual(sl_tasks.filter_positive_numbers([-1, -2, -3, 0]), [])
        self.assertEqual(sl_tasks.filter_positive_numbers([]), [])

if __name__ == '__main__':
    unittest.main(verbosity=2)