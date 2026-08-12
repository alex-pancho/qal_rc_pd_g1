#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тести для перевірки виконання завдань з файлу _selflearning01.py
Цей файл аналізує та тестує РЕАЛЬНИЙ код студента
"""

import sys
import io
import os
import re
from contextlib import redirect_stdout
import unittest
from unittest.mock import patch
from pathlib import Path

class StudentCodeAnalyzer:
    """Аналізатор коду студента"""
    
    def __init__(self, file_path="_selflearning01.py"):
        self.dir = Path(__file__).parent
        self.filename = self.dir / file_path
        self.code_content = ""
        self.tasks = {}
        self.load_student_code()

    
    def load_student_code(self):
        """Завантажує код студента з файлу"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.code_content = f.read()
            self.parse_tasks()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.filename} не знайдено! Переконайтеся, що він знаходиться в тій же папці.")
        except Exception as e:
            raise Exception(f"Помилка при читанні файлу: {e}")
    
    def parse_tasks(self):
        """Парсить код на окремі завдання"""
        lines = self.code_content.split('\n')
        current_task = None
        current_code = []
        
        for line in lines:
            # Знаходимо початок завдання
            if '=== ЗАВДАННЯ' in line:
                # Зберігаємо попереднє завдання
                if current_task and current_code:
                    self.tasks[current_task] = '\n'.join(current_code)
                
                # Починаємо нове завдання
                task_match = re.search(r'ЗАВДАННЯ (\d+)', line)
                if task_match:
                    current_task = int(task_match.group(1))
                    current_code = []
            
            # Додаємо код до поточного завдання
            elif current_task and not line.strip().startswith('print("==='):
                current_code.append(line)
        
        # Зберігаємо останнє завдання
        if current_task and current_code:
            self.tasks[current_task] = '\n'.join(current_code)
    
    def get_task_code(self, task_number):
        """Отримує код конкретного завдання"""
        return self.tasks.get(task_number, "")
    
    def has_meaningful_code(self, task_number):
        """Перевіряє, чи є в завданні змістовний код"""
        code = self.get_task_code(task_number)
        # Видаляємо коментарі та порожні рядки
        meaningful_lines = []
        for line in code.split('\n'):
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('# Ваш код тут'):
                meaningful_lines.append(stripped)
        
        return len(meaningful_lines) > 0
    
    def execute_task_code(self, task_number, inputs=None):
        """Виконує код завдання з заданими вхідними даними"""
        code = self.get_task_code(task_number)
        if not code.strip():
            return None, "Код завдання порожній"
        
        try:
            # Перехоплюємо виведення
            output = io.StringIO()
            
            # Підготовка вхідних даних
            if inputs:
                with patch('builtins.input', side_effect=inputs):
                    with redirect_stdout(output):
                        exec(code)
            else:
                with redirect_stdout(output):
                    exec(code)
            
            return output.getvalue(), None
            
        except Exception as e:
            return None, f"Помилка виконання: {str(e)}"


class TestStudentCode(unittest.TestCase):
    """Тести для перевірки коду студента"""
    
    @classmethod
    def setUpClass(cls):
        """Ініціалізація аналізатора коду"""
        try:
            cls.analyzer = StudentCodeAnalyzer()
        except Exception as e:
            cls.analyzer = None
            print(f"❌ Помилка ініціалізації: {e}")
    
    def setUp(self):
        """Перевірка наявності аналізатора"""
        if not self.analyzer:
            self.skipTest("Аналізатор коду не ініціалізовано")
    
    def test_task_1_age_classification(self):
        """Тест завдання 1: Перевірка віку"""
        print("\n🧪 Тестуємо завдання 1: Перевірка віку")
        
        if not self.analyzer.has_meaningful_code(1):
            self.fail("❌ Завдання 1 не виконано! Додайте код після коментаря '# Ваш код тут:'")
        
        test_cases = [
            (['5'], "Дитина"),
            (['11'], "Дитина"),
            (['12'], "Підліток"),
            (['15'], "Підліток"),
            (['17'], "Підліток"),
            (['18'], "Дорослий"),
            (['25'], "Дорослий")
        ]
        
        for inputs, expected in test_cases[:3]:  # Тестуємо тільки 3 випадки
            with self.subTest(age=inputs[0]):
                output, error = self.analyzer.execute_task_code(1, inputs)
                
                if error:
                    self.fail(f"Помилка в коді завдання 1: {error}")
                
                if expected.lower() not in output.lower():
                    self.fail(f"Для віку {inputs[0]} очікується '{expected}', але отримано: '{output.strip()}'")
        
        # Повідомлення про успіх виводиться тільки якщо всі перевірки пройшли
        print("✅ Завдання 1 виконано правильно!")
    
    def test_task_2_even_odd(self):
        """Тест завдання 2: Парне чи непарне число"""
        print("\n🧪 Тестуємо завдання 2: Парне чи непарне число")
        
        if not self.analyzer.has_meaningful_code(2):
            self.fail("❌ Завдання 2 не виконано! Додайте код після коментаря '# Ваш код тут:'")
        
        test_cases = [
            (['4'], "парне"),
            (['7'], "непарне"),
            (['0'], "парне")
        ]
        
        for inputs, expected in test_cases:
            with self.subTest(number=inputs[0]):
                output, error = self.analyzer.execute_task_code(2, inputs)
                
                if error:
                    self.fail(f"Помилка в коді завдання 2: {error}")
                
                if expected.lower() not in output.lower():
                    self.fail(f"Для числа {inputs[0]} очікується '{expected}', але отримано: '{output.strip()}'")
        
        # Повідомлення про успіх виводиться тільки якщо всі перевірки пройшли
        print("✅ Завдання 2 виконано правильно!")
    
    def test_task_3_grade_calculator(self):
        """Тест завдання 3: Калькулятор оцінок"""
        print("\n🧪 Тестуємо завдання 3: Калькулятор оцінок")
        
        if not self.analyzer.has_meaningful_code(3):
            self.fail("❌ Завдання 3 не виконано! Додайте код після коментаря '# Ваш код тут:'")
        
        test_cases = [
            (['95'], "відмінно"),
            (['85'], "добре"),
            (['75'], "задовільно"),
            (['65'], "незадовільно"),
            (['55'], "погано")
        ]
        
        for inputs, expected in test_cases[:3]:
            with self.subTest(score=inputs[0]):
                output, error = self.analyzer.execute_task_code(3, inputs)
                
                if error:
                    self.fail(f"Помилка в коді завдання 3: {error}")
                
                if expected.lower() not in output.lower():
                    self.fail(f"Для балів {inputs[0]} очікується '{expected}', але отримано: '{output.strip()}'")
        
        # Повідомлення про успіх виводиться тільки якщо всі перевірки пройшли
        print("✅ Завдання 3 виконано правильно!")
    
    def test_task_4_multiplication_table(self):
        """Тест завдання 4: Таблиця множення"""
        print("\n🧪 Тестуємо завдання 4: Таблиця множення")
        
        if not self.analyzer.has_meaningful_code(4):
            self.fail("❌ Завдання 4 не виконано! Додайте код після коментаря '# Ваш код тут:'")
        
        output, error = self.analyzer.execute_task_code(4)
        
        if error:
            self.fail(f"Помилка в коді завдання 4: {error}")
        
        # Перевіряємо наявність кількох результатів множення
        required_results = ["5", "10", "15", "25", "50"]
        found_results = 0
        
        for result in required_results:
            if result in output:
                found_results += 1
        
        if found_results < 3:
            self.fail(f"Таблиця множення неповна. Очікуються результати множення 5 на числа від 1 до 10. Отримано: '{output.strip()}'")
        
        # Повідомлення про успіх виводиться тільки якщо всі перевірки пройшли
        print("✅ Завдання 4 виконано правильно!")
    
    def test_task_5_sum_calculation(self):
        """Тест завдання 5: Сума чисел від 1 до 50"""
        print("\n🧪 Тестуємо завдання 5: Сума чисел")
        
        if not self.analyzer.has_meaningful_code(5):
            self.fail("❌ Завдання 5 не виконано! Додайте код після коментаря '# Ваш код тут:'")
        
        output, error = self.analyzer.execute_task_code(5)
        
        if error:
            self.fail(f"Помилка в коді завдання 5: {error}")
        
        # Перевіряємо наявність правильної суми (1275)
        if "1275" not in output:
            self.fail(f"Сума чисел від 1 до 50 має бути 1275. Отримано: '{output.strip()}'")
        
        # Повідомлення про успіх виводиться тільки якщо всі перевірки пройшли
        print("✅ Завдання 5 виконано правильно!")
    
    def test_task_6_digit_count(self):
        """Тест завдання 6: Підрахунок цифр"""
        print("\n🧪 Тестуємо завдання 6: Підрахунок цифр")
        
        if not self.analyzer.has_meaningful_code(6):
            self.fail("❌ Завдання 6 не виконано! Додайте код після коментаря '# Ваш код тут:'")
        
        test_cases = [
            (['123'], "3"),
            (['1'], "1"),
            (['9999'], "4")
        ]
        
        for inputs, expected in test_cases[:2]:
            with self.subTest(number=inputs[0]):
                output, error = self.analyzer.execute_task_code(6, inputs)
                
                if error:
                    self.fail(f"Помилка в коді завдання 6: {error}")
                
                if expected not in output:
                    self.fail(f"Для числа {inputs[0]} очікується {expected} цифр. Отримано: '{output.strip()}'")
        
        # Повідомлення про успіх виводиться тільки якщо всі перевірки пройшли
        print("✅ Завдання 6 виконано правильно!")
    
    def test_task_7_string_output(self):
        """Тест завдання 7: Виведення символів рядка"""
        print("\n🧪 Тестуємо завдання 7: Виведення символів")
        
        if not self.analyzer.has_meaningful_code(7):
            self.fail("❌ Завдання 7 не виконано! Додайте код після коментаря '# Ваш код тут:'")
        
        test_input = "Test"
        output, error = self.analyzer.execute_task_code(7, [test_input])
        
        if error:
            self.fail(f"Помилка в коді завдання 7: {error}")
        
        # Перевіряємо, чи є символи в окремих рядках
        lines = output.strip().split('\n')
        if len(lines) < len(test_input):
            self.fail(f"Кожен символ має бути на окремому рядку. Отримано: '{output.strip()}'")
        
        # Повідомлення про успіх виводиться тільки якщо всі перевірки пройшли
        print("✅ Завдання 7 виконано правильно!")
    
    def test_task_12_star_pyramid(self):
        """Тест завдання 12: Піраміда зірочок"""
        print("\n🧪 Тестуємо завдання 12: Піраміда зірочок")
        
        if not self.analyzer.has_meaningful_code(12):
            self.fail("❌ Завдання 12 не виконано! Додайте код після коментаря '# Ваш код тут:'")
        
        output, error = self.analyzer.execute_task_code(12)
        
        if error:
            self.fail(f"Помилка в коді завдання 12: {error}")
        
        # Перевіряємо наявність зірочок у правильному форматі
        lines = [line.strip() for line in output.strip().split('\n') if line.strip()]
        
        expected_patterns = ["*", "**", "***", "****", "*****"]
        found_patterns = 0
        
        for pattern in expected_patterns:
            if any(pattern in line for line in lines):
                found_patterns += 1
        
        if found_patterns < 3:
            self.fail(f"Піраміда зірочок неправильна. Очікуються рядки: *, **, ***, ****, *****. Отримано: '{output.strip()}'")
        
        # Повідомлення про успіх виводиться тільки якщо всі перевірки пройшли
        print("✅ Завдання 12 виконано правильно!")


def check_file_exists():
    """Перевіряє наявність файлу з завданнями"""
    return True


def run_specific_test(task_number):
    """Запуск конкретного тесту"""
    if not check_file_exists():
        return
    
    suite = unittest.TestSuite()
    
    test_methods = {
        1: 'test_task_1_age_classification',
        2: 'test_task_2_even_odd',
        3: 'test_task_3_grade_calculator',
        4: 'test_task_4_multiplication_table',
        5: 'test_task_5_sum_calculation',
        6: 'test_task_6_digit_count',
        7: 'test_task_7_string_output',
        12: 'test_task_12_star_pyramid'
    }
    
    if task_number in test_methods:
        suite.addTest(TestStudentCode(test_methods[task_number]))
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print(f"\n🎉 Завдання {task_number} виконано ПРАВИЛЬНО!")
        else:
            print(f"\n❌ Завдання {task_number} потребує доопрацювання")
    else:
        print(f"❌ Тест для завдання {task_number} не реалізовано")


def run_all_tests():
    """Запуск всіх доступних тестів"""
    if not check_file_exists():
        return
    
    print("🚀 Запускаємо перевірку вашого коду...")
    print("=" * 60)
    
    # Запускаємо тільки реалізовані тести
    available_tests = [1, 2, 3, 4, 5, 6, 7, 12]
    
    for task_num in available_tests:
        print(f"\n{'='*20} ЗАВДАННЯ {task_num} {'='*20}")
        run_specific_test(task_num)
    
    print("\n" + "=" * 60)
    print("📊 ПІДСУМОК:")
    print("✅ Завдання з зеленими галочками виконано правильно")
    print("❌ Завдання з червоними хрестиками потребують доопрацювання")
    print("💡 Виправте помилки та запустіть тести знову")


if __name__ == "__main__":
    print("🎯 ПЕРЕВІРКА КОДУ СТУДЕНТА")
    print("=" * 50)
    
    if not check_file_exists():
        input("\nНатисніть Enter для виходу...")
        sys.exit(1)
    
    print("Доступні опції:")
    print("1. Перевірити всі завдання")
    print("2. Перевірити конкретне завдання")
    print("3. Показати статистику файлу")
    
    try:
        choice = input("\nВведіть номер опції (1-3): ").strip()
        
        if choice == "1":
            run_all_tests()
        elif choice == "2":
            print("Доступні завдання для перевірки: 1, 2, 3, 4, 5, 6, 7, 12")
            task_num = int(input("Введіть номер завдання: "))
            run_specific_test(task_num)
        elif choice == "3":
            analyzer = StudentCodeAnalyzer()
            print(f"\n📈 СТАТИСТИКА ФАЙЛУ '{analyzer.filename}':")
            print("-" * 40)
            total_tasks = len(analyzer.tasks)
            completed_tasks = sum(1 for i in analyzer.tasks if analyzer.has_meaningful_code(i))
            print(f"Всього завдань знайдено: {total_tasks}")
            print(f"Завдань з кодом: {completed_tasks}")
            print(f"Завдань без коду: {total_tasks - completed_tasks}")
            
            print("\nДетальна інформація:")
            for task_num in sorted(analyzer.tasks.keys()):
                status = "✅ Виконано" if analyzer.has_meaningful_code(task_num) else "❌ Потрібно виконати"
                print(f"  Завдання {task_num}: {status}")
        else:
            print("❌ Невірний вибір")
            
    except (ValueError, KeyboardInterrupt):
        print("\n👋 До побачення!")
    except Exception as e:
        print(f"\n❌ Помилка: {e}")
        
    input("\nНатисніть Enter для виходу...")
    print("\n🎓 Успіхів у навчанні Python!")