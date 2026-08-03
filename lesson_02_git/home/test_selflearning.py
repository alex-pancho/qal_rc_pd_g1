#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест з Git та GitHub - True/False
Автор: Assistant
Дата: 2025
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

class GitTest:
    def __init__(self):
        self.questions = [
            {
                "id": 1,
                "statement": "Git - це централізована система контролю версій",
                "answer": False,
                "explanation": "Git - це розподілена система контролю версій. Кожна робоча копія містить повну історію проекту."
            },
            {
                "id": 2,
                "statement": "Команда 'git init' створює новий репозиторій у поточній директорії",
                "answer": True,
                "explanation": "Команда 'git init' ініціалізує новий Git-репозиторій у поточній папці, створюючи приховану директорію .git."
            },
            {
                "id": 3,
                "statement": "Файли у Git можуть перебувати тільки в двох станах: Modified та Committed",
                "answer": False,
                "explanation": "У Git файли можуть перебувати в трьох станах: Modified (змінений), Staged (підготовлений) та Committed (зафіксований)."
            },
            {
                "id": 4,
                "statement": "Команда 'git add' переміщує файли з Working Directory до Staging Area",
                "answer": True,
                "explanation": "Команда 'git add' додає файли до Staging Area (область підготовки), готуючи їх для наступного коміту."
            },
            {
                "id": 5,
                "statement": "Команда 'git pull' еквівалентна виконанню 'git fetch' та 'git merge'",
                "answer": True,
                "explanation": "Команда 'git pull' завантажує зміни з віддаленого репозиторію та автоматично об'єднує їх з поточною гілкою."
            },
            {
                "id": 6,
                "statement": "Fork на GitHub - це копія репозиторію у вашому власному акаунті",
                "answer": True,
                "explanation": "Fork створює копію репозиторію у вашому GitHub акаунті, дозволяючи вам вносити зміни без впливу на оригінал."
            },
            {
                "id": 7,
                "statement": "Pull Request можна створити тільки з форку репозиторію і більше ніяк",
                "answer": False,
                "explanation": "Pull Request можна створити як з форку, так і з гілки в тому ж репозиторії (якщо у вас є права доступу)."
            },
            {
                "id": 8,
                "statement": "Команда 'git reset --hard HEAD~1' безповоротно видаляє всі зміни з останнього коміту",
                "answer": True,
                "explanation": "Команда 'git reset --hard HEAD~1' видаляє останній коміт та всі зміни в робочій директорії. Це небезпечна операція."
            },
            {
                "id": 9,
                "statement": "Лише гілка 'main' або 'master' має завжди містити стабільний, готовий до випуску код",
                "answer": False,
                "explanation": "Хоча це хороша практика, це залежить від стратегії розробки команди. Не всі проекти дотримуються цього правила."
            },
            {
                "id": 10,
                "statement": "Конфлікти злиття виникають тоді і тільки коли два розробники змінюють один і той же файл",
                "answer": False,
                "explanation": "Конфлікти можуть виникати не тільки при зміні одного файлу, а й при різних операціях з файлами (видалення, переміщення тощо)."
            },
            {
                "id": 11,
                "statement": "Команда 'git commit --amend' крім того дозволяє змінити повідомлення останнього коміту",
                "answer": True,
                "explanation": "Команда 'git commit --amend' дозволяє змінити повідомлення або додати файли до останнього коміту."
            },
            {
                "id": 12,
                "statement": "SHA-1 хеш кожного коміту унікальний в межах всіх Git-репозиторіїв світу",
                "answer": True,
                "explanation": "SHA-1 хеш кожного коміту унікальний завдяки включенню timestamp, автора, змісту та хешу батьківського коміту."
            },
            {
                "id": 13,
                "statement": "Команда 'git clone' завантажує тільки останню версію файлів проекту",
                "answer": False,
                "explanation": "Команда 'git clone' завантажує повну історію репозиторію з усіма комітами, гілками та тегами."
            },
            {
                "id": 14,
                "statement": "У Git можна створювати гілки без обмежень по кількості",
                "answer": True,
                "explanation": "Git дозволяє створювати необмежену кількість гілок, і це одна з його переваг для паралельної розробки."
            },
            {
                "id": 15,
                "statement": "Команда 'git revert' видаляє коміт з історії",
                "answer": False,
                "explanation": "Команда 'git revert' створює новий коміт, який скасовує зміни попереднього коміту, не видаляючи його з історії."
            },
            {
                "id": 16,
                "statement": "GitHub Actions дозволяє автоматизувати процеси розробки",
                "answer": True,
                "explanation": "GitHub Actions - це платформа CI/CD, що дозволяє автоматизувати тестування, збірку та розгортання коду."
            },
            {
                "id": 17,
                "statement": "Файл .gitignore варто додавати до репозиторію",
                "answer": True,
                "explanation": "Файл .gitignore варто додавати до репозиторію, щоб всі учасники проекту використовували однакові правила ігнорування файлів."
            },
            {
                "id": 18,
                "statement": "Команда 'git stash' тимчасово зберігає незафіксовані зміни",
                "answer": True,
                "explanation": "Команда 'git stash' зберігає поточні зміни в стеку, дозволяючи перемкнутися на іншу гілку та повернутися пізніше."
            },
            {
                "id": 19,
                "statement": "Merge коміт завжди має двох батьків",
                "answer": True,
                "explanation": "Merge коміт об'єднує дві гілки, тому він завжди має принаймні двох батьків - по одному з кожної гілки."
            },
            {
                "id": 20,
                "statement": "GitHub Desktop - це єдиний GUI клієнт для роботи з Git",
                "answer": False,
                "explanation": "GitHub Desktop - це один з GUI клієнтів. Існує багато інших: GitKraken, SourceTree, TortoiseGit та інші."
            }
        ]
        
        self.user_answers = {}
        self.test_started = False
        self.test_completed = False
    
    def display_header(self):
        """Відображає заголовок тесту"""
        print("=" * 80)
        print("🎯 ТЕСТ З GIT ТА GITHUB - TRUE/FALSE")
        print("=" * 80)
        print(f"📚 Загальна кількість питань: {len(self.questions)}")
        print("💡 Відповідайте True або False (T/F, 1/0, Так/Ні)")
        print("🔄 Ви можете переглянути та змінити відповіді перед завершенням")
        print("-" * 80)
    
    def get_user_input(self, prompt: str) -> str:
        """Отримує введення від користувача з валідацією"""
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input:
                    return user_input
                print("❌ Введіть відповідь!")
            except KeyboardInterrupt:
                print("\n\n👋 Тест перервано користувачем")
                exit(0)
    
    def parse_answer(self, answer: str) -> bool:
        """Перетворює строку відповіді на boolean"""
        answer = answer.lower().strip()
        
        true_answers = ['true', 't', '1', 'так', 'да', 'yes', 'y']
        false_answers = ['false', 'f', '0', 'ні', 'нет', 'no', 'n']
        
        if answer in true_answers:
            return True
        elif answer in false_answers:
            return False
        else:
            raise ValueError("Неправильний формат відповіді")
    
    def ask_question(self, question: Dict) -> None:
        """Задає одне питання користувачу"""
        print(f"\n📝 Питання {question['id']}/{len(self.questions)}:")
        print(f"   {question['statement']}")
        print()
        
        while True:
            try:
                answer_str = self.get_user_input("Ваша відповідь (True/False): ")
                answer = self.parse_answer(answer_str)
                self.user_answers[question['id']] = answer
                break
            except ValueError:
                print("❌ Введіть 'True' або 'False' (можна скорочено: T/F, 1/0, Так/Ні)")
    
    def review_answers(self) -> bool:
        """Дозволяє переглянути та змінити відповіді"""
        print("\n" + "=" * 80)
        print("📋 ПЕРЕГЛЯД ВІДПОВІДЕЙ")
        print("=" * 80)
        
        for question in self.questions:
            q_id = question['id']
            user_answer = self.user_answers.get(q_id, "Немає відповіді")
            
            if isinstance(user_answer, bool):
                answer_text = "True" if user_answer else "False"
            else:
                answer_text = str(user_answer)
            
            print(f"{q_id:2d}. {question['statement']}")
            print(f"    Ваша відповідь: {answer_text}")
            print()
        
        
        while True:
            choice = self.get_user_input(
                "\nВи хочете змінити якусь відповідь? (введіть номер питання або 'завершити'/0): "
            ).lower()
            
            if choice in ['завершити', 'finish', 'done', 'end', 'готово', 'все' '0']:
                return True
            
            try:
                q_num = int(choice)
                if 1 <= q_num <= len(self.questions):
                    question = next(q for q in self.questions if q['id'] == q_num)
                    print(f"\n📝 Питання {q_num}: {question['statement']}")
                    
                    while True:
                        try:
                            new_answer_str = self.get_user_input("Нова відповідь (True/False): ")
                            new_answer = self.parse_answer(new_answer_str)
                            self.user_answers[q_num] = new_answer
                            print(f"✅ Відповідь на питання {q_num} змінено на: {'True' if new_answer else 'False'}")
                            break
                        except ValueError:
                            print("❌ Введіть 'True' або 'False'")
                else:
                    print(f"❌ Введіть номер від 1 до {len(self.questions)}")
            except ValueError:
                print("❌ Введіть номер питання або 'завершити'")
    
    def calculate_results(self) -> Tuple[int, int, List[Dict]]:
        """Обчислює результати тесту"""
        correct = 0
        total = len(self.questions)
        detailed_results = []
        
        for question in self.questions:
            q_id = question['id']
            user_answer = self.user_answers.get(q_id)
            correct_answer = question['answer']
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct += 1
            
            detailed_results.append({
                'question': question,
                'user_answer': user_answer,
                'is_correct': is_correct
            })
        
        return correct, total, detailed_results
    
    def get_grade_info(self, percentage: float) -> Tuple[str, str]:
        """Повертає оцінку та коментар на основі відсотка правильних відповідей"""
        if percentage >= 90:
            return "⭐ ВІДМІННО", "Ви чудово знаєте Git та GitHub! 🎉"
        elif percentage >= 80:
            return "🌟 ДУЖЕ ДОБРЕ", "У вас солідні знання Git та GitHub! 👏"
        elif percentage >= 70:
            return "👍 ДОБРЕ", "Є деякі прогалини, але загалом непогано! 💪"
        elif percentage >= 60:
            return "📚 ЗАДОВІЛЬНО", "Варто повторити матеріал."
        else:
            return "📖 ПОТРІБНА ПРАКТИКА", "Потрібно більше вивчати Git та GitHub."
    
    def display_results(self) -> None:
        """Відображає результати тесту"""
        correct, total, detailed_results = self.calculate_results()
        percentage = (correct / total) * 100
        grade, comment = self.get_grade_info(percentage)
        
        print("\n" + "=" * 80)
        print("🎯 РЕЗУЛЬТАТИ ТЕСТУ")
        print("=" * 80)
        print(f"📊 Правильних відповідей: {correct} з {total}")
        print(f"📈 Відсоток: {percentage:.1f}%")
        print(f"🏆 Оцінка: {grade}")
        print(f"💬 Коментар: {comment}")
        print("=" * 80)
        
        # Детальні результати
        print("\n📋 ДЕТАЛЬНИЙ РОЗБІР:")
        print("-" * 80)
        
        for i, result in enumerate(detailed_results, 1):
            question = result['question']
            user_answer = result['user_answer']
            is_correct = result['is_correct']
            
            status = "✅ ПРАВИЛЬНО" if is_correct else "❌ НЕПРАВИЛЬНО"
            user_text = "True" if user_answer else "False" if user_answer is not None else "Немає відповіді"
            correct_text = "True" if question['answer'] else "False"
            
            print(f"\n{i:2d}. {question['statement']}")
            print(f"    {status}")
            print(f"    Ваша відповідь: {user_text}")
            print(f"    Правильна відповідь: {correct_text}")
            print(f"    💡 Пояснення: {question['explanation']}")
    
    def save_results(self) -> None:
        """Зберігає результати тесту у файл"""
        try:
            correct, total, detailed_results = self.calculate_results()
            percentage = (correct / total) * 100
            grade, comment = self.get_grade_info(percentage)
            
            results_data = {
                'timestamp': datetime.now().isoformat(),
                'score': {
                    'correct': correct,
                    'total': total,
                    'percentage': percentage,
                    'grade': grade,
                    'comment': comment
                },
                'questions': []
            }
            
            for result in detailed_results:
                question = result['question']
                results_data['questions'].append({
                    'id': question['id'],
                    'statement': question['statement'],
                    'correct_answer': question['answer'],
                    'user_answer': result['user_answer'],
                    'is_correct': result['is_correct'],
                    'explanation': question['explanation']
                })
            
            filename = f"git_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Результати збережено у файл: {filename}")
            
        except Exception as e:
            print(f"\n❌ Помилка при збереженні результатів: {e}")
    
    def run_test(self) -> None:
        """Основний метод для запуску тесту"""
        self.display_header()
        
        # Запитання чи користувач готовий
        ready = self.get_user_input("Готові розпочати тест? (Так/Ні): ")
        if not self.parse_answer(ready):
            print("👋 До побачення! Повертайтесь, коли будете готові.")
            return
        
        self.test_started = True
        
        # Основний цикл тесту
        print("\n🚀 Розпочинаємо тест!")
        
        for question in self.questions:
            self.ask_question(question)
        
        # Перегляд відповідей
        print("\n✅ Всі питання пройдено!")
        self.review_answers()
        
        # Підтвердження завершення
        confirm = self.get_user_input("\nЗавершити тест і побачити результати? (Так/Ні): ")
        if not self.parse_answer(confirm):
            print("Тест не завершено. Перезапустіть програму для продовження.")
            return
        
        self.test_completed = True
        
        # Показ результатів
        self.display_results()
        
        # Збереження результатів
        save_choice = self.get_user_input("\nЗберегти результати у файл? (Так/Ні): ")
        if self.parse_answer(save_choice):
            self.save_results()
        
        print("\n🎉 Дякуємо за проходження тесту з Git та GitHub!")
        print("📚 Продовжуйте вивчати та практикуватися!")


def main():
    """Головна функція програми"""
    print("Завантаження тесту...")
    
    try:
        test = GitTest()
        test.run_test()
    except KeyboardInterrupt:
        print("\n\n👋 Програму перервано користувачем")
    except Exception as e:
        print(f"\n❌ Сталася помилка: {e}")
        print("Перезапустіть програму та спробуйте знову.")


if __name__ == "__main__":
    main()