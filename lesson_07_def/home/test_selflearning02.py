# -*- coding: utf-8 -*-
"""
Тести для перевірки завдань з функцій Python
============================================

Цей файл містить тести для автоматичної перевірки правильності виконання завдань
з файлу selflearning02.py

Для запуску тестів виконайте: python test_selflearning.py
"""

import unittest
import sys
import os
import logging

# Додаємо поточну директорію до шляху для імпорту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ])

try:
    from selflearning02 import *
except ImportError as e:
    logging.info(f"Помилка імпорту: {e}")
    logging.info("Переконайтеся, що файл selflearning02.py знаходиться в тій же папці")
    sys.exit(1)


class TestFunctions(unittest.TestCase):
    """Тести для перевірки функцій"""
    
    def setUp(self):
        """Підготовка даних для тестів"""
        self.test_numbers = [1, 2, 3, 4, 5]
        self.test_names = ["Олена", "Іван", "Марія"]
        self.test_ages = [25, 30, 28]
    
    # =========================================================================
    # ТЕСТИ ДЛЯ ЗАВДАННЯ 1: Основи створення функцій
    # =========================================================================
    
    def test_01_greeting(self):
        """Тест функції greeting"""
        result = greeting("Олексій")
        self.assertEqual(result, "Привіт, Олексій!")
        logging.info("✓ greeting() - працює правильно")

    
    def test_calculate_area(self):
        """Тест функції calculate_area"""
        result = calculate_area(5, 3)
        self.assertEqual(result, 15)
        
        result = calculate_area(4.5, 2.5)
        self.assertEqual(result, 11.25)
        logging.info("✓ calculate_area() - працює правильно")

    
    def test_is_even(self):
        """Тест функції is_even"""
        self.assertTrue(is_even(4))
        self.assertFalse(is_even(5))
        self.assertTrue(is_even(0))
        self.assertFalse(is_even(-3))
        logging.info("✓ is_even() - працює правильно")

    
    # =========================================================================
    # ТЕСТИ ДЛЯ ЗАВДАННЯ 2: Позиційні та ключові аргументи
    # =========================================================================
    
    def test_create_profile(self):
        """Тест функції create_profile"""
            # Тест з мінімальними параметрами
        profile = create_profile("Іван", 25)
        expected = {"name": "Іван", "age": 25, "city": "Не вказано", "profession": "Не вказано"}
        self.assertEqual(profile, expected)
        
        # Тест з усіма параметрами
        profile = create_profile("Марія", 30, city="Київ", profession="Розробник")
        expected = {"name": "Марія", "age": 30, "city": "Київ", "profession": "Розробник"}
        self.assertEqual(profile, expected)
        logging.info("✓ create_profile() - працює правильно")

    
    def test_calculate_price(self):
        """Тест функції calculate_price"""
        # Без знижки та податку
        result = calculate_price(100)
        self.assertEqual(result, 120)  # 100 * 1.2
        
        # З знижкою
        result = calculate_price(100, discount=0.1)
        self.assertEqual(result, 108)  # 100 * 0.9 * 1.2
        
        # З власним податком
        result = calculate_price(100, tax=0.1)
        self.assertEqual(result, 110)  # 100 * 1.1
        
        logging.info("✓ calculate_price() - працює правильно")
    
    # =========================================================================
    # ТЕСТИ ДЛЯ ЗАВДАННЯ 3: *args і **kwargs
    # =========================================================================
    
    def test_sum_all(self):
        """Тест функції sum_all"""
        self.assertEqual(sum_all(1, 2, 3), 6)
        self.assertEqual(sum_all(1), 1)
        self.assertEqual(sum_all(), 0)
        self.assertEqual(sum_all(1.5, 2.5, 3), 7)
        logging.info("✓ sum_all() - працює правильно")

    
    def test_create_student(self):
        """Тест функції create_student"""
        # З параметрами
        student = create_student(name="Петро", age=20, course="Python")
        self.assertIn("name", student)
        self.assertIn("age", student)
        self.assertIn("course", student)
        self.assertEqual(student["name"], "Петро")
        
        # Без параметрів (перевірка значень за замовчуванням)
        student = create_student()
        self.assertIn("name", student)
        self.assertIn("age", student)
        
        logging.info("✓ create_student() - працює правильно")

    
    def test_flexible_function(self):
        """Тест функції flexible_function"""
        result = flexible_function(1, 2, 3, name="Іван", age=25)
        self.assertEqual(result, ([1, 2, 3], {"name": "Іван", "age": 25}))
        
        result = flexible_function()
        self.assertEqual(result, ([], {}))
        
        logging.info("✓ flexible_function() - працює правильно")

    
    # =========================================================================
    # ТЕСТИ ДЛЯ ЗАВДАННЯ 4: Лямбда-функції
    # =========================================================================
    
    def test_lambda_functions_01(self):
        """Тест лямбда-функцій"""
            # Перевірка square
        if square is not None:
            self.assertEqual(square(5), 25)
            self.assertEqual(square(0), 0)
            logging.info("✓ square lambda - працює правильно")
        else:
            logging.info("✗ square lambda - не реалізована")
            self.assertTrue(False, "Лямбда-функція square не реалізована")
    
    def test_lambda_functions_02(self):
        """Тест лямбда-функцій"""    
        # Перевірка is_greater_than_10
        if is_greater_than_10 is not None:
            self.assertTrue(is_greater_than_10(15))
            self.assertFalse(is_greater_than_10(5))
            logging.info("✓ is_greater_than_10 lambda - працює правильно")
        else:
            self.assertTrue(False, "Лямбда-функція is_greater_than_10 не реалізована")

    def test_lambda_functions_03(self):
        """Тест лямбда-функцій"""        
            # Перевірка concatenate
        if concatenate is not None:
            self.assertEqual(concatenate("Привіт", " світ"), "Привіт світ")
            logging.info("✓ concatenate lambda - працює правильно")
        else:
            logging.info("✗ concatenate lambda - не реалізована")
            self.assertTrue(False, "Лямбда-функція concatenate не реалізована")
    
    # =========================================================================
    # ТЕСТИ ДЛЯ ЗАВДАННЯ 5: Вбудовані функції
    # =========================================================================
    
    def test_check_type_vs_isinstance(self):
        """Тест функції check_type_vs_isinstance"""
        # Тест з int
        result = check_type_vs_isinstance(5, int)
        self.assertEqual(result, (True, True))
        
        # Тест з bool (bool є підкласом int)
        result = check_type_vs_isinstance(True, int)
        self.assertEqual(result, (False, True))
        
        logging.info("✓ check_type_vs_isinstance() - працює правильно")


    def test_sort_vs_sorted_demo(self):
        """Тест функції sort_vs_sorted_demo"""
        original = [3, 1, 4, 1, 5]
        result = sort_vs_sorted_demo(original.copy())
        
        # Перевіряємо, що повертається кортеж
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        
        # Перевіряємо, що обидва результати відсортовані
        self.assertEqual(result[0], [1, 1, 3, 4, 5])
        self.assertEqual(result[1], [1, 1, 3, 4, 5])
        
        logging.info("✓ sort_vs_sorted_demo() - працює правильно")
    
    # =========================================================================
    # ТЕСТИ ДЛЯ ЗАВДАННЯ 6: Складніші завдання
    # =========================================================================
    
    def test_filter_and_process(self):
        """Тест функції filter_and_process"""
            # Фільтруємо парні числа та піднімаємо до квадрату
        data = [1, 2, 3, 4, 5, 6]
        result = filter_and_process(data, lambda x: x % 2 == 0, lambda x: x ** 2)
        self.assertEqual(result, [4, 16, 36])
        
        logging.info("✓ filter_and_process() - працює правильно")

    
    def test_create_multiplier(self):
        """Тест функції create_multiplier"""
        multiply_by_3 = create_multiplier(3)
        self.assertEqual(multiply_by_3(5), 15)
        self.assertEqual(multiply_by_3(2), 6)
        
        multiply_by_10 = create_multiplier(10)
        self.assertEqual(multiply_by_10(5), 50)
        
        logging.info("✓ create_multiplier() - працює правильно")

    
    def test_advanced_calculator(self):
        """Тест функції advanced_calculator"""
            # Сума (за замовчуванням)
        result = advanced_calculator(1, 2, 3, 4)
        self.assertEqual(result, 10)
        
        # Множення
        result = advanced_calculator(2, 3, 4, operation="multiply")
        self.assertEqual(result, 24)
        
        # Максимум
        result = advanced_calculator(1, 5, 3, 2, operation="max")
        self.assertEqual(result, 5)
        
        # Мінімум
        result = advanced_calculator(1, 5, 3, 2, operation="min")
        self.assertEqual(result, 1)
        
        logging.info("✓ advanced_calculator() - працює правильно")


class TestRunner:
    """Клас для запуску тестів з детальним звітом"""
    
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def run_all_tests(self):
        """Запуск всіх тестів"""
        logging.info("=" * 60)
        logging.info("АВТОМАТИЧНА ПЕРЕВІРКА ЗАВДАНЬ З ФУНКЦІЙ PYTHON")
        logging.info("=" * 60)
        
        # Створюємо тестовий набір
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFunctions)
        
        # Запускаємо тести
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w', encoding="utf8"))
        result = runner.run(suite)
        
        # Виводимо результати
        self.total_tests = result.testsRun
        self.failed_tests = len(result.failures) + len(result.errors)
        self.passed_tests = self.total_tests - self.failed_tests
        
        logging.info("\n" + "=" * 60)
        logging.info("РЕЗУЛЬТАТИ ТЕСТУВАННЯ:")
        logging.info("=" * 60)
        logging.info(f"Всього тестів: {self.total_tests}")
        logging.info(f"Пройдено: {self.passed_tests}")
        logging.info(f"Не пройдено: {self.failed_tests}")
        
        if self.failed_tests == 0:
            logging.info("\n🎉 Вітаємо! Всі тести пройдено успішно!")
            logging.info("Ви успішно виконали всі завдання з функцій Python.")
        else:
            logging.info(f"\n⚠️  Потрібно виправити {self.failed_tests} помилок.")
            logging.info("Перевірте свої рішення та спробуйте знову.")
        
        logging.info("=" * 60)
        
        # Виводимо детальні помилки
        if result.failures:
            logging.info("\nДЕТАЛЬНІ ПОМИЛКИ:")
            for test, traceback in result.failures:
                logging.info(f"\n❌ {test}: {traceback}")
        
        if result.errors:
            logging.info("\nПОМИЛКИ ВИКОНАННЯ:")
            for test, traceback in result.errors:
                logging.info(f"\n❌ {test}: {traceback}")


def main():
    """Головна функція для запуску тестів"""
    try:
        # Перевіряємо, чи можемо імпортувати модуль
        import selflearning02
        
        # Запускаємо тести
        test_runner = TestRunner()
        test_runner.run_all_tests()
        
    except ImportError:
        logging.info("❌ Не вдалося знайти файл selflearning02.py")
        logging.info("Переконайтеся, що файл знаходиться в тій же папці що й цей тест.")
    except Exception as e:
        logging.info(f"❌ Помилка при запуску тестів: {e}")


if __name__ == "__main__":
    main()