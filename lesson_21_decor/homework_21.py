import functools
import logging

#стандартний модуль logging для виводу рівнів 
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def chronicle(writer: str = "Анонімний"):
    """Декоратор з параметром для логування викликів функцій."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Формуємо позиційні та іменовані аргументи в зручний рядок
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            all_args = ", ".join(args_repr + kwargs_repr)

            logging.info(f"[Літописець: {writer}] Викликано: {func.__name__}({all_args})")
            
            result = func(*args, **kwargs)
            
            logging.info(f"[Результат]: {result}")
            return result
        return wrapper
    return decorator


# === Перевірка  ===
if __name__ == "__main__":
    @chronicle("Самійло Величко")
    def make_decision(action, target):
        return f"Рішення: {action} → {target}"

    @chronicle()
    def count_warriors(regiment):
        return 500

    make_decision("Атакувати", "Перекоп")
    count_warriors("Полтавський")

    import functools
import logging
import random
import time

# Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


# ==========================================
# Завдання 2. Хранитель фортеці
# ==========================================
def guard(secret: str):
    """Декоратор перевірки паролю перед викликом функції."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user_input = input("Назви пароль: ")
            if user_input == secret:
                logging.info(f"Доступ надано: {func.__name__}")
                return func(*args, **kwargs)
            else:
                logging.warning(f"Невдала спроба доступу до: {func.__name__}")
                print("Стій! Доступ заборонено.")
                return None
        return wrapper
    return decorator


# ==========================================
# Завдання 3. Залізний характер
# ==========================================
def retry(times: int = 3, delay: float = 1.0):
    """Декоратор для повторного виклику функції при помилках."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    result = func(*args, **kwargs)
                    logging.info(f"Успіх на спробі {attempt}/{times}")
                    return result
                except Exception as e:
                    logging.warning(f"Спроба {attempt}/{times} не вдалася: {e}")
                    if attempt == times:
                        logging.error(f"Усі {times} спроби вичерпано для {func.__name__}")
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator


# ==========================================
# Перевірка роботи
# ==========================================
if __name__ == "__main__":
    print("=== Завдання 2: Хранитель фортеці ===")

    @guard(secret="Мамай")
    def open_treasury():
        print("Скарбниця відчинена!")
        return "золото, срібло, зброя"

    treasury_result = open_treasury()
    print(f"Результат: {treasury_result}\n")

    print("=== Завдання 3: Залізний характер ===")

    @retry(times=4, delay=0.5)
    def unreliable_scout():
        if random.random() < 0.7:  # 70% шанс помилки
            raise ConnectionError("Розвідник не повернувся")
        return "Ворог за річкою!"

    try:
        scout_result = unreliable_scout()
        print(f"Результат розвідки: {scout_result}")
    except ConnectionError as err:
        print(f"Фінальна помилка: {err}")