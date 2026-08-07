#!/usr/bin/env python3
"""
Автотестування для файлів selflearning_basics.py та selflearning_advanced.py
Запустіть цей файл після виконання завдань для перевірки правильності рішень
"""

import sys
import importlib.util
from typing import Any, Dict, List, Tuple
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def load_module(file_path: str):
    dir = Path(__file__).parent
    filename = dir / file_path
    """Завантажує модуль з файлу"""
    try:
        spec = importlib.util.spec_from_file_location("student_module", filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except FileNotFoundError:
        print(f"{Colors.RED}Файл {filename} не знайдено!{Colors.END}")
        return None
    except Exception as e:
        print(f"{Colors.RED}Помилка завантаження {file_path}: {e}{Colors.END}")
        return None

def test_basics():
    """Тестування базових завдань"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}=== ТЕСТУВАННЯ БАЗОВИХ ЗАВДАНЬ ==={Colors.END}")
    
    module = load_module("selflearning_basics.py")
    if not module:
        return 0, 0
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: numbers list
    total_tests += 1
    if hasattr(module, 'numbers') and module.numbers == [0, 1, 2, 3, 4, 5, 6]:
        print(f"{Colors.GREEN}✓ Task 1-3: Список numbers правильний{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 1-3: Список numbers неправильний. Очікувано: [0, 1, 2, 3, 4, 5, 6]{Colors.END}")
    
    # Test 2: fruits manipulation
    total_tests += 1
    expected_fruits = ['apple', 'banana', 'cherry', 'banana', 'date']
    if hasattr(module, 'fruits') and 'cherry' not in module.fruits:
        expected_fruits.remove('cherry')
        if sorted(module.fruits) == sorted(expected_fruits):
            print(f"{Colors.GREEN}✓ Task 4: cherry видалено з fruits{Colors.END}")
            tests_passed += 1
        else:
            print(f"{Colors.RED}✗ Task 4: Неправильна маніпуляція з fruits{Colors.END}")
    else:
        print(f"{Colors.RED}✗ Task 4: cherry не видалено або fruits не знайдено{Colors.END}")
    
    # Test 3: cherry index
    total_tests += 1
    original_fruits = ['apple', 'banana', 'cherry', 'banana', 'date']
    if hasattr(module, 'cherry_index') and module.cherry_index == 2:
        print(f"{Colors.GREEN}✓ Task 5: Індекс cherry правильний{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 5: Індекс cherry неправильний. Очікувано: 2{Colors.END}")
    
    # Test 4: banana count
    total_tests += 1
    if hasattr(module, 'banana_count') and module.banana_count == 2:
        print(f"{Colors.GREEN}✓ Task 6: Кількість banana правильна{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 6: Кількість banana неправильна. Очікувано: 2{Colors.END}")
    
    # Test 5: weekdays tuple
    total_tests += 1
    expected_weekdays = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    if hasattr(module, 'weekdays') and len(module.weekdays) == 7:
        print(f"{Colors.GREEN}✓ Task 9: Кортеж weekdays створено{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 9: Кортеж weekdays неправильний{Colors.END}")
    
    # Test 6: monday count in tuple
    total_tests += 1
    if hasattr(module, 'monday_count') and module.monday_count == 3:
        print(f"{Colors.GREEN}✓ Task 11: Кількість Monday правильна{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 11: Кількість Monday неправильна. Очікувано: 3{Colors.END}")
    
    # Test 7: unique numbers set
    total_tests += 1
    if hasattr(module, 'unique_numbers') and isinstance(module.unique_numbers, set) and len(module.unique_numbers) >= 3:
        print(f"{Colors.GREEN}✓ Task 13-15: Множина unique_numbers створена та оброблена{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 13-15: Множина unique_numbers неправильна{Colors.END}")
    
    # Test 8: set operations
    total_tests += 1
    if (hasattr(module, 'union_set') and hasattr(module, 'intersection_set') and 
        hasattr(module, 'difference_set')):
        if (module.union_set == {1, 2, 3, 4, 5} and 
            module.intersection_set == {3} and
            module.difference_set == {1, 2}):
            print(f"{Colors.GREEN}✓ Task 16-18: Операції з множинами правильні{Colors.END}")
            tests_passed += 1
        else:
            print(f"{Colors.RED}✗ Task 16-18: Операції з множинами неправильні{Colors.END}")
    else:
        print(f"{Colors.RED}✗ Task 16-18: Змінні для операцій з множинами не знайдені{Colors.END}")
    
    # Test 9: student dictionary
    total_tests += 1
    if hasattr(module, 'student') and isinstance(module.student, dict) and len(module.student) >= 3:
        print(f"{Colors.GREEN}✓ Task 20-21: Словник student створено та оброблено{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 20-21: Словник student неправильний{Colors.END}")
    
    # Test 10: squares dictionary
    total_tests += 1
    expected_squares = {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
    if hasattr(module, 'squares_dict') and module.squares_dict == expected_squares:
        print(f"{Colors.GREEN}✓ Task 26: Словник квадратів правильний{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 26: Словник квадратів неправильний{Colors.END}")
    
    return tests_passed, total_tests

def test_advanced():
    """Тестування поглиблених завдань"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}=== ТЕСТУВАННЯ ПОГЛИБЛЕНИХ ЗАВДАНЬ ==={Colors.END}")
    
    module = load_module("selflearning_advanced.py")
    if not module:
        return 0, 0
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: even numbers
    total_tests += 1
    expected_even = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    if hasattr(module, 'even_numbers') and module.even_numbers == expected_even:
        print(f"{Colors.GREEN}✓ Task 1: Парні числа правильні{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 1: Парні числа неправильні{Colors.END}")
    
    # Test 2: odd squares
    total_tests += 1
    expected_odd_squares = [1, 9, 25, 49, 81]
    if hasattr(module, 'odd_squares') and module.odd_squares == expected_odd_squares:
        print(f"{Colors.GREEN}✓ Task 3: Квадрати непарних чисел правильні{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 3: Квадрати непарних чисел неправильні{Colors.END}")
    
    # Test 3: vowels set
    total_tests += 1
    expected_vowels = {'a', 'e', 'i', 'o', 'u'}
    if hasattr(module, 'vowels') and module.vowels == expected_vowels:
        print(f"{Colors.GREEN}✓ Task 7: Множина голосних правильна{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 7: Множина голосних неправильна{Colors.END}")
    
    # Test 4: unique chars
    total_tests += 1
    expected_unique = set("programming")
    if hasattr(module, 'unique_chars') and module.unique_chars == expected_unique:
        print(f"{Colors.GREEN}✓ Task 8: Унікальні символи правильні{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 8: Унікальні символи неправильні{Colors.END}")
    
    # Test 5: divisible by 3
    total_tests += 1
    expected_div3 = {3, 6, 9, 12, 15}
    if hasattr(module, 'divisible_by_3') and module.divisible_by_3 == expected_div3:
        print(f"{Colors.GREEN}✓ Task 9: Числа, що діляться на 3, правильні{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 9: Числа, що діляться на 3, неправильні{Colors.END}")
    
    # Test 6: word lengths
    total_tests += 1
    expected_lengths = {"cat": 3, "dog": 3, "elephant": 8, "bee": 3}
    if hasattr(module, 'word_lengths') and module.word_lengths == expected_lengths:
        print(f"{Colors.GREEN}✓ Task 11: Довжини слів правильні{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 11: Довжини слів неправильні{Colors.END}")
    
    # Test 7: char frequency
    total_tests += 1
    if hasattr(module, 'char_frequency') and isinstance(module.char_frequency, dict):
        # Перевіряємо, чи є правильна частота для деяких символів
        correct_freq = (module.char_frequency.get('l', 0) == 3 and 
                       module.char_frequency.get('o', 0) == 2)
        if correct_freq:
            print(f"{Colors.GREEN}✓ Task 14: Частота символів правильна{Colors.END}")
            tests_passed += 1
        else:
            print(f"{Colors.RED}✗ Task 14: Частота символів неправильна{Colors.END}")
    else:
        print(f"{Colors.RED}✗ Task 14: char_frequency не знайдено або не словник{Colors.END}")
    
    # Test 8: coordinates unpacking
    total_tests += 1
    if (hasattr(module, 'x') and hasattr(module, 'y') and hasattr(module, 'z') and
        module.x == 10 and module.y == 20 and module.z == 30):
        print(f"{Colors.GREEN}✓ Task 6: Розпакування координат правильне{Colors.END}")
        tests_passed += 1
    else:
        print(f"{Colors.RED}✗ Task 6: Розпакування координат неправильне{Colors.END}")
    
    return tests_passed, total_tests

def main():
    """Головна функція тестування"""
    print(f"{Colors.BOLD}{Colors.BLUE}АВТОТЕСТУВАННЯ ЗАВДАНЬ SELF-LEARNING{Colors.END}")
    print("=" * 50)
    
    # Тестування базових завдань
    basic_passed, basic_total = test_basics()
    
    # Тестування поглиблених завдань
    advanced_passed, advanced_total = test_advanced()
    
    # Підсумки
    total_passed = basic_passed + advanced_passed
    total_tests = basic_total + advanced_total
    
    print(f"\n{Colors.BOLD}=== ПІДСУМКИ ==={Colors.END}")
    print(f"Базові завдання: {basic_passed}/{basic_total}")
    print(f"Поглиблені завдання: {advanced_passed}/{advanced_total}")
    print(f"{Colors.BOLD}ЗАГАЛОМ: {total_passed}/{total_tests}{Colors.END}")
    
    percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    if percentage >= 90:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ВІДМІННО! ({percentage:.1f}%){Colors.END}")
    elif percentage >= 70:
        print(f"{Colors.YELLOW}{Colors.BOLD}✨ ДОБРЕ! ({percentage:.1f}%){Colors.END}")
    elif percentage >= 50:
        print(f"{Colors.YELLOW}📚 ЗАДОВІЛЬНО ({percentage:.1f}%) - потрібна додаткова практика{Colors.END}")
    else:
        print(f"{Colors.RED}❌ ПОТРІБНО ПОПРАЦЮВАТИ ({percentage:.1f}%){Colors.END}")
    
    if percentage < 100:
        print(f"\n{Colors.BLUE}💡 Поради:{Colors.END}")
        print("- Уважно прочитайте завдання")
        print("- Перевірте назви змінних")
        print("- Використовуйте правильні методи для кожного типу даних")
        print("- При потребі зверніться до документації Python")

if __name__ == "__main__":
    main()