# -*- coding: utf-8 -*-
"""
Тести для перевірки виконання завдань з обробки рядків
Автор: AI Assistant
Дата: 2025

Цей файл містить автоматичні тести для всіх шести завдань:
1. Зрізи строк (_selflearning01.py)
2. Розділення та об'єднання строк (_selflearning02.py)
3. Перевірка початку та кінця строк (_selflearning03.py)
4. Операції з регістром символів (_selflearning04.py)
5. Пошук та заміна в строках (_selflearning05.py)
6. Обрізання зайвих символів (_selflearning06.py)

Як використовувати:
1. Виконайте всі завдання у відповідних файлах
2. Помістіть цей файл у ту ж папку з файлами завдань
3. Запустіть: python test_string_exercises.py
4. Перевірте результати тестування
"""

import sys
import os
import importlib.util
import traceback
from typing import Any, Dict, Optional
from pathlib import Path

class StringExerciseTester:
    """Клас для тестування завдань з обробки рядків"""
    
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = []
        self.error_tests = []
        self.dir = Path(__file__).parent
    
    def load_module(self, file_path: str) -> Optional[Any]:
        """Завантажує модуль з файлу"""
        filename = self.dir / file_path
        try:
            if not os.path.exists(filename):
                print(f"❌ Файл {filename} не знайдено!")
                return None
            
            spec = importlib.util.spec_from_file_location("module", filename)
            if spec is None or spec.loader is None:
                print(f"❌ Не вдалося завантажити специфікацію для {filename}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            
            # Перехоплюємо вивід під час виконання
            import io
            from contextlib import redirect_stdout, redirect_stderr
            
            captured_output = io.StringIO()
            with redirect_stdout(captured_output), redirect_stderr(captured_output):
                spec.loader.exec_module(module)
            
            return module
        except Exception as e:
            print(f"❌ Помилка завантаження {filename}: {str(e)}")
            return None
    
    def test_variable(self, module: Any, var_name: str, expected: Any, test_description: str):
        """Тестує змінну з модуля"""
        self.total_tests += 1
        
        try:
            if not hasattr(module, var_name):
                print(f"❌ {test_description}: ЗМІННА НЕ ЗНАЙДЕНА")
                print(f"   Змінна '{var_name}' не існує або не визначена")
                self.error_tests.append(test_description)
                return
            
            actual = getattr(module, var_name)
            
            # Перевірка на незаповнені завдання
            if str(actual).strip() == "# Ваш код тут" or actual is None:
                print(f"❌ {test_description}: НЕ ВИКОНАНО")
                print(f"   Завдання не виконано - залишився коментар '# Ваш код тут'")
                self.error_tests.append(test_description)
                return
            
            if actual == expected:
                print(f"✅ {test_description}: ПРОЙДЕНО")
                self.passed_tests += 1
            else:
                print(f"❌ {test_description}: ПОМИЛКА")
                print(f"   Очікувалось: {repr(expected)}")
                print(f"   Отримано: {repr(actual)}")
                print(f"   Тип очікуваного: {type(expected).__name__}")
                print(f"   Тип отриманого: {type(actual).__name__}")
                self.failed_tests.append(test_description)
        
        except Exception as e:
            print(f"❌ {test_description}: ПОМИЛКА ВИКОНАННЯ")
            print(f"   Помилка: {str(e)}")
            self.error_tests.append(test_description)
    
    def print_summary(self, task_name: str):
        """Виводить підсумок тестування завдання"""
        print(f"\n{'='*50}")
        print(f"ПІДСУМОК: {task_name}")
        print(f"{'='*50}")
        print(f"Всього тестів: {self.total_tests}")
        print(f"Пройдено: {self.passed_tests}")
        print(f"Провалено: {len(self.failed_tests)}")
        print(f"Помилки виконання: {len(self.error_tests)}")
        
        if self.failed_tests:
            print(f"\nПровалені тести:")
            for test in self.failed_tests:
                print(f"  - {test}")
        
        if self.error_tests:
            print(f"\nПомилки виконання:")
            for test in self.error_tests:
                print(f"  - {test}")
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        print(f"\nВідсоток успіху: {success_rate:.1f}%")
        
        return {
            'total': self.total_tests,
            'passed': self.passed_tests,
            'failed': len(self.failed_tests),
            'errors': len(self.error_tests),
            'success_rate': success_rate
        }

def test_task_1():
    """Тестує завдання 1: Зрізи строк"""
    print("\n" + "="*60)
    print("ТЕСТУВАННЯ ЗАВДАННЯ 1: Зрізи строк (_selflearning01.py)")
    print("="*60)
    
    tester = StringExerciseTester()
    module = tester.load_module("_selflearning01.py")
    
    if module is None:
        print("Пропускаємо тестування через помилку завантаження файлу")
        return {'total': 0, 'passed': 0, 'failed': 0, 'errors': 1, 'success_rate': 0}
    
    # Тестування всіх змінних з завдання 1
    tester.test_variable(module, 'first_char', "H", "1.1 Перший символ")
    tester.test_variable(module, 'last_char', "!", "1.2 Останній символ")
    tester.test_variable(module, 'char_at_7', "o", "1.3 Символ з індексом 7")
    tester.test_variable(module, 'second_last_char', "d", "1.4 Передостанній символ")
    tester.test_variable(module, 'substring_3_to_8', "lo, W", "1.5 Підстроку з 3-го по 8-й")
    tester.test_variable(module, 'first_5_chars', "Hello", "1.6 Перші 5 символів")
    tester.test_variable(module, 'last_6_chars', "World!", "1.7 Останні 6 символів")
    tester.test_variable(module, 'every_second_char', "Hlo ol!", "1.8 Кожен другий символ")
    tester.test_variable(module, 'reversed_text', "!dlroW ,olleH", "1.9 Зворотний рядок")
    tester.test_variable(module, 'chars_1_to_10_step_2', "elo r", "1.10 Символи 1-10 з кроком 2")
    
    return tester.print_summary("Завдання 1 - Зрізи строк")

def test_task_2():
    """Тестує завдання 2: Розділення та об'єднання строк"""
    print("\n" + "="*60)
    print("ТЕСТУВАННЯ ЗАВДАННЯ 2: Розділення та об'єднання (_selflearning02.py)")
    print("="*60)
    
    tester = StringExerciseTester()
    module = tester.load_module("_selflearning02.py")
    
    if module is None:
        print("Пропускаємо тестування через помилку завантаження файлу")
        return {'total': 0, 'passed': 0, 'failed': 0, 'errors': 1, 'success_rate': 0}
    
    # Тестування всіх змінних з завдання 2
    tester.test_variable(module, 'split_by_comma', ['apple', 'orange', 'banana', 'grape'], "2.1 Розділення за комами")
    tester.test_variable(module, 'split_by_space', ['Hello', 'world', 'Python', 'programming'], "2.2 Розділення за пробілами")
    tester.test_variable(module, 'split_by_dash', ['one', 'two', 'three', 'four', 'five'], "2.3 Розділення за дефісами")
    tester.test_variable(module, 'split_by_pipe', ['red', 'green', 'blue', 'yellow'], "2.4 Розділення за |")
    tester.test_variable(module, 'join_with_pipe', "apple | orange | banana | grape", "2.5 Об'єднання через |")
    tester.test_variable(module, 'join_with_dash', "Hello - world - Python - programming", "2.6 Об'єднання через -")
    tester.test_variable(module, 'join_with_plus', "one + two + three + four + five", "2.7 Об'єднання через +")
    tester.test_variable(module, 'join_with_and', "red AND green AND blue AND yellow", "2.8 Об'єднання через AND")
    tester.test_variable(module, 'split_limited', ['apple', 'orange', 'banana,grape'], "2.9 Обмежене розділення")
    tester.test_variable(module, 'join_languages', "Python, Java, JavaScript", "2.10 Мови програмування")
    
    return tester.print_summary("Завдання 2 - Розділення та об'єднання")

def test_task_3():
    """Тестує завдання 3: Перевірка початку та кінця строк"""
    print("\n" + "="*60)
    print("ТЕСТУВАННЯ ЗАВДАННЯ 3: Перевірка початку/кінця (_selflearning03.py)")
    print("="*60)
    
    tester = StringExerciseTester()
    module = tester.load_module("_selflearning03.py")
    
    if module is None:
        print("Пропускаємо тестування через помилку завантаження файлу")
        return {'total': 0, 'passed': 0, 'failed': 0, 'errors': 1, 'success_rate': 0}
    
    # Тестування всіх змінних з завдання 3
    tester.test_variable(module, 'starts_with_hello', True, "3.1 text1 починається з 'Hello'")
    tester.test_variable(module, 'ends_with_exclamation', True, "3.2 text1 закінчується на '!'")
    tester.test_variable(module, 'starts_with_python', True, "3.3 text2 починається з 'Python'")
    tester.test_variable(module, 'ends_with_language', True, "3.4 text2 закінчується на 'language'")
    tester.test_variable(module, 'starts_with_welcome', True, "3.5 text3 починається з 'Welcome'")
    tester.test_variable(module, 'ends_with_ukraine', True, "3.6 text3 закінчується на 'Ukraine'")
    tester.test_variable(module, 'starts_with_bad', False, "3.7 text4 починається з 'Bad'")
    tester.test_variable(module, 'ends_with_everyone', True, "3.8 text4 закінчується на 'everyone'")
    tester.test_variable(module, 'ends_with_py', True, "3.9 text5 закінчується на '.py'")
    tester.test_variable(module, 'starts_with_prog', True, "3.10 text5 починається з 'prog'")
    tester.test_variable(module, 'combined_check1', True, "3.11 Комбінована перевірка 1")
    tester.test_variable(module, 'combined_check2', True, "3.12 Комбінована перевірка 2")
    
    return tester.print_summary("Завдання 3 - Перевірка початку/кінця")

def test_task_4():
    """Тестує завдання 4: Операції з регістром символів"""
    print("\n" + "="*60)
    print("ТЕСТУВАННЯ ЗАВДАННЯ 4: Операції з регістром (_selflearning04.py)")
    print("="*60)
    
    tester = StringExerciseTester()
    module = tester.load_module("_selflearning04.py")
    
    if module is None:
        print("Пропускаємо тестування через помилку завантаження файлу")
        return {'total': 0, 'passed': 0, 'failed': 0, 'errors': 1, 'success_rate': 0}
    
    # Тестування всіх змінних з завдання 4
    tester.test_variable(module, 'text1_upper', "HELLO WORLD", "4.1 text1 верхній регістр")
    tester.test_variable(module, 'text2_lower', "python programming", "4.2 text2 нижній регістр")
    tester.test_variable(module, 'text3_title', "Javascript Is Fun", "4.3 text3 title case")
    tester.test_variable(module, 'text4_swapcase', "wElCoMe To UkRaInE", "4.4 text4 swapcase")
    tester.test_variable(module, 'text5_capitalize', "Good morning", "4.5 text5 capitalize")
    tester.test_variable(module, 'text1_is_upper', False, "4.6 text1 тільки великі літери")
    tester.test_variable(module, 'text2_is_upper', True, "4.7 text2 тільки великі літери")
    tester.test_variable(module, 'text3_is_lower', True, "4.8 text3 тільки малі літери")
    tester.test_variable(module, 'text1_is_title', True, "4.9 text1 у форматі title")
    tester.test_variable(module, 'text5_is_title', True, "4.10 text5 у форматі title")
    tester.test_variable(module, 'text6', "JAVASCRIPT IS FUN", "4.11 text6 (text3 у верхньому регістрі)")
    tester.test_variable(module, 'text6_is_upper', True, "4.12 text6 тільки великі літери")
    
    return tester.print_summary("Завдання 4 - Операції з регістром")

def test_task_5():
    """Тестує завдання 5: Пошук та заміна в строках"""
    print("\n" + "="*60)
    print("ТЕСТУВАННЯ ЗАВДАННЯ 5: Пошук та заміна (_selflearning05.py)")
    print("="*60)
    
    tester = StringExerciseTester()
    module = tester.load_module("_selflearning05.py")
    
    if module is None:
        print("Пропускаємо тестування через помилку завантаження файлу")
        return {'total': 0, 'passed': 0, 'failed': 0, 'errors': 1, 'success_rate': 0}
    
    # Тестування всіх змінних з завдання 5
    tester.test_variable(module, 'position_hello', 0, "5.1 Позиція 'Hello' в text1")
    tester.test_variable(module, 'position_python', 0, "5.2 Позиція 'Python' в text2")
    tester.test_variable(module, 'position_java', -1, "5.3 Позиція 'Java' в text2")
    tester.test_variable(module, 'position_script', 4, "5.4 Позиція 'Script' в text3")
    tester.test_variable(module, 'text1_replaced', "Hi world Hi everyone", "5.5 text1 (Hello -> Hi)")
    tester.test_variable(module, 'text2_replaced', "Java is great, Java is powerful", "5.6 text2 (Python -> Java)")
    tester.test_variable(module, 'text3_replaced', "Python programming language", "5.7 text3 (JavaScript -> Python)")
    tester.test_variable(module, 'text4_replaced', "Great morning, great afternoon, great evening", "5.8 text4 (good -> great)")
    tester.test_variable(module, 'text5_replaced_first', "cherry,banana,apple,orange,apple", "5.9 text5 (перше apple -> cherry)")
    tester.test_variable(module, 'text5_replaced_all', "cherry,banana,cherry,orange,cherry", "5.10 text5 (всі apple -> cherry)")
    tester.test_variable(module, 'position_world', 6, "5.11 Позиція 'world' в text1")
    tester.test_variable(module, 'text5_with_pipes', "apple | banana | apple | orange | apple", "5.12 text5 (коми на |)")
    
    return tester.print_summary("Завдання 5 - Пошук та заміна")

def test_task_6():
    """Тестує завдання 6: Обрізання зайвих символів"""
    print("\n" + "="*60)
    print("ТЕСТУВАННЯ ЗАВДАННЯ 6: Обрізання символів (_selflearning06.py)")
    print("="*60)
    
    tester = StringExerciseTester()
    module = tester.load_module("_selflearning06.py")
    
    if module is None:
        print("Пропускаємо тестування через помилку завантаження файлу")
        return {'total': 0, 'passed': 0, 'failed': 0, 'errors': 1, 'success_rate': 0}
    
    # Тестування всіх змінних з завдання 6
    tester.test_variable(module, 'text1_strip', "Hello World", "6.1 text1 strip()")
    tester.test_variable(module, 'text1_lstrip', "Hello World   ", "6.2 text1 lstrip()")
    tester.test_variable(module, 'text1_rstrip', "   Hello World", "6.3 text1 rstrip()")
    tester.test_variable(module, 'text2_strip', "Python Programming", "6.4 text2 strip()")
    tester.test_variable(module, 'text2_lstrip', "Python Programming\t\t", "6.5 text2 lstrip()")
    tester.test_variable(module, 'text3_strip', "JavaScript", "6.6 text3 strip()")
    tester.test_variable(module, 'text4_strip', "Good morning everyone", "6.7 text4 strip()")
    tester.test_variable(module, 'text5_strip_stars', "Welcome to Ukraine", "6.8 text5 strip('*')")
    tester.test_variable(module, 'text5_lstrip_stars', "Welcome to Ukraine***", "6.9 text5 lstrip('*')")
    tester.test_variable(module, 'text5_rstrip_stars', "***Welcome to Ukraine", "6.10 text5 rstrip('*')")
    tester.test_variable(module, 'text6_length_before', 4, "6.11 text6 довжина до strip")
    tester.test_variable(module, 'text6_stripped', "", "6.11 text6 після strip")
    tester.test_variable(module, 'text6_length_after', 0, "6.11 text6 довжина після strip")
    tester.test_variable(module, 'text1_strip_upper', "HELLO WORLD", "6.12 text1 strip + upper")
    
    return tester.print_summary("Завдання 6 - Обрізання символів")

def run_all_tests():
    """Запускає всі тести"""
    print("🧪 АВТОМАТИЧНЕ ТЕСТУВАННЯ ФАЙЛІВ ЗАВДАНЬ З ОБРОБКИ РЯДКІВ")
    print("="*80)
    print("Цей скрипт імпортує та тестує ваші файли завдань:")
    print("• _selflearning01.py - Зрізи строк")
    print("• _selflearning02.py - Розділення та об'єднання")
    print("• _selflearning03.py - Перевірка початку/кінця")
    print("• _selflearning04.py - Операції з регістром")
    print("• _selflearning05.py - Пошук та заміна")
    print("• _selflearning06.py - Обрізання символів")
    print("="*80)
    
    # Збираємо результати всіх тестів
    all_results = []
    
    try:
        # Запускаємо тести для всіх завдань
        all_results.append(("Завдання 1", test_task_1()))
        all_results.append(("Завдання 2", test_task_2()))
        all_results.append(("Завдання 3", test_task_3()))
        all_results.append(("Завдання 4", test_task_4()))
        all_results.append(("Завдання 5", test_task_5()))
        all_results.append(("Завдання 6", test_task_6()))
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Тестування перервано користувачем.")
        return
    except Exception as e:
        print(f"\n\n❌ Критична помилка: {str(e)}")
        traceback.print_exc()
        return
    
    # Загальна статистика
    print(f"\n{'='*80}")
    print(f"🏆 ЗАГАЛЬНА СТАТИСТИКА ПО ВСІХ ЗАВДАННЯХ")
    print(f"{'='*80}")
    
    total_tests = sum(result['total'] for _, result in all_results)
    total_passed = sum(result['passed'] for _, result in all_results)
    total_failed = sum(result['failed'] for _, result in all_results)
    total_errors = sum(result['errors'] for _, result in all_results)
    
    print(f"📊 Всього тестів: {total_tests}")
    print(f"✅ Пройдено: {total_passed}")
    print(f"❌ Провалено: {total_failed}")
    print(f"⚠️  Помилки: {total_errors}")
    
    if total_tests > 0:
        overall_success = (total_passed / total_tests) * 100
        print(f"📈 Загальний відсоток успіху: {overall_success:.1f}%")
    else:
        overall_success = 0
        print(f"📈 Загальний відсоток успіху: 0.0%")
    
    # Деталізована статистика по завданнях
    print(f"\n📋 Детальна статистика по завданнях:")
    print(f"{'-'*80}")
    print(f"{'Завдання':<20} {'Пройдено':<12} {'Провалено':<12} {'Помилки':<10} {'Успіх %':<10}")
    print(f"{'-'*80}")
    
    for task_name, result in all_results:
        success_rate = result['success_rate']
        status_icon = "🟢" if success_rate == 100 else "🟡" if success_rate >= 50 else "🔴"
        print(f"{status_icon} {task_name:<17} {result['passed']:<12} {result['failed']:<12} {result['errors']:<10} {success_rate:.1f}%")
    
    # Рекомендації
    print(f"\n💡 РЕКОМЕНДАЦІЇ:")
    if overall_success == 100:
        print("🎉 ФЕНОМЕНАЛЬНО! Всі завдання виконано ідеально!")
        print("🌟 Ви чудово засвоїли роботу з рядками в Python!")
    elif overall_success >= 90:
        print("🌟 ВІДМІННО! Майже всі завдання виконано правильно!")
        print("👀 Перевірте залишкові помилки та виправте їх.")
    elif overall_success >= 80:
        print("👍 ДОБРЕ! Більшість завдань виконано правильно!")
        print("📖 Рекомендую перечитати матеріал з проблемних тем.")
    elif overall_success >= 60:
        print("📖 НЕПОГАНО! Основи засвоєно, але є що покращити!")
        print("🔍 Уважно проаналізуйте помилки та повторіть складні теми.")
    elif overall_success >= 40:
        print("⚠️  ПОТРІБНО БІЛЬШЕ ПРАКТИКИ!")
        print("📚 Рекомендую повторити теорію та виконати завдання знову.")
    else:
        print("🚨 КРИТИЧНО! Багато завдань не виконано або виконано неправильно!")
        print("📖 Обов'язково поверніться до вивчення основ роботи з рядками.")
    
    print(f"\n🔧 Поради для покращення:")
    print(f"• Уважно читайте умови завдань")
    print(f"• Перевіряйте типи даних (str, list, bool, int)")
    print(f"• Тестуйте свій код на простих прикладах")
    print(f"• Використовуйте print() для налагодження")
    print(f"• Не забувайте про методи рядків: strip(), split(), join(), find(), replace()")
    
    print(f"\n📄 Завершення тестування!")

def main():
    """Головна функція"""
    try:
        run_all_tests()
    except Exception as e:
        print(f"\n❌ Невідома помилка: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()