import unittest
try:
    from lesson_14_try_except_log.home.homework_14 import sum_numbers_in_list
except:
    from homework_14 import sum_numbers_in_list


class TestSumNumbersInList(unittest.TestCase):

    def test_01_valid_input(self):
        """" Тест на коректні вхідні дані """
        self.assertEqual(sum_numbers_in_list(["1,2,3", "4,0,6"]), [6, 10])
        self.assertEqual(sum_numbers_in_list(["1,2,3,4", "1,2,3,4,50"]), [10, 60])

    def test_02_invalid_strings(self):
        """ Тест на некоректні типи даних всердині строки """
        self.assertEqual(
            sum_numbers_in_list(["1,2,3", "4/0,6", "asas7,8,9"]),
            [6, "Не можу це зробити!", "Не можу це зробити!"],
        )
        self.assertEqual(
            sum_numbers_in_list(["1,2,3", "asas7,8,9", "4,0,6"]),
            [6, "Не можу це зробити!", 10],
        )

    def test_03_non_string_elements(self):
        """ Тест на некоректні типи даних всередині списку """
        self.assertEqual(
            sum_numbers_in_list(["1,2,3", 7]), 
            [6, "Не можу це зробити! AttributeError"]
        )
        self.assertEqual(
            sum_numbers_in_list(["1,2,3,4", "1,2,3,4,50", sum, min(1, 2)]),
            [
                10,
                60,
                "Не можу це зробити! AttributeError",
                "Не можу це зробити! AttributeError",
            ],
        )

    def test_04_empty_list(self):
        """ Тест на порожній список """
        with self.assertRaises(ValueError):
            sum_numbers_in_list([])

    def test_05_non_list_input(self):
        """ Тест на некоректний тип вхідних даних """
        with self.assertRaises(ValueError):
            sum_numbers_in_list("21")
        with self.assertRaises(ValueError):
            sum_numbers_in_list(3)

    def test_06_mixed_valid_invalid(self):
        """ Тест на суміш коректних і некоректних даних """
        self.assertEqual(
            sum_numbers_in_list(
                [
                    "1,2,3,4",
                    "1,2,3,4,50",
                    "qwerty1,2,3",
                    {"country": "Ukraine", "continent": "Europe", "size": 123},
                ]
            ),
            [
                10,
                60,
                "Не можу це зробити!",
                "Не можу це зробити! AttributeError",
            ],
        )


if __name__ == "__main__":
    unittest.main()
