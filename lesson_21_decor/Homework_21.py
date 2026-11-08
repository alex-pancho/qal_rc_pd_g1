#Завдання 1.
import logging
from functools import wraps

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s"
)


def chronicle(author="Анонімний"):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Формуємо рядок з аргументами
            arguments = [repr(arg) for arg in args]
            arguments.extend(
                f"{key}={value!r}" for key, value in kwargs.items()
            )

            arguments_str = ", ".join(arguments)

            # Логуємо виклик функції
            logging.info(
                f"[Літописець: {author}] "
                f"Викликано: {func.__name__}({arguments_str})"
            )

            # Виконуємо оригінальну функцію
            result = func(*args, **kwargs)

            # Логуємо результат
            logging.info(f"[Результат]: {result}")

            return result

        return wrapper

    return decorator

@chronicle("Самійло Величко")
def make_decision(action, target):
    return f"Рішення: {action} → {target}"

@chronicle("Козацький літописець")
def add_warriors(regiment, warriors, reserve=0):
    return warriors + reserve


add_warriors("Київський", 300, reserve=50)


@chronicle()
def count_warriors(regiment):
    return 500


make_decision("Атакувати", "Перекоп")
count_warriors("Полтавський")


#Завдання 2.

import logging
from functools import wraps

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s"
)


def guard(secret):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            password = input("Назви пароль: ")

            if password == secret:
                logging.info(f"Доступ надано: {func.__name__}")
                return func(*args, **kwargs)

            logging.warning(
                f"Невдала спроба доступу до: {func.__name__}"
            )

            print("Стій! Доступ заборонено.")
            return None

        return wrapper

    return decorator

@guard(secret="Мамай")
def open_treasury():
    print("Скарбниця відчинена!")
    return "золото, срібло, зброя"

result = open_treasury()

print(result)

#Завдання 3
import logging
import time
from functools import wraps

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s"
)


def retry(times=3, delay=1.0):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(1, times + 1):
                try:
                    result = func(*args, **kwargs)

                    logging.info(
                        f"Успіх на спробі {attempt}/{times}"
                    )

                    return result

                except Exception as error:
                    logging.warning(
                        f"Спроба {attempt}/{times} не вдалася: {error}"
                    )

                    if attempt == times:
                        logging.error(
                            f"Усі {times} спроб вичерпано!"
                        )
                        raise

                    time.sleep(delay)

        return wrapper

    return decorator

import random


@retry(times=4, delay=0.5)
def unreliable_scout():
    if random.random() < 0.7:
        raise ConnectionError("Розвідник не повернувся")

    return "Ворог за річкою!"



result = unreliable_scout()
print(result)