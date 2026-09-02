from source_log import logger

def div(a, b):
    try:
        result = a / b
    except ZeroDivisionError as e:
        logger.error(f"Помилка ділення на нуль: {e}")
        result = None
    except TypeError as e:
        logger.error(f"Помилка даних: {e}")
        if not isinstance(a, (int,float)):
            a = float(a)
        if not isinstance(b, (int,float)):
            b = float(b)
        return div(a, b)
    return result

a = 1
b = "0.000000"
result = div(a, b)

logger.info(result)


def sum(a, b):
    try:
        return a + b
    except (ValueError, TypeError):
        logger.error("Do not use different type  here")
        return None

result = sum(a, b)

logger.info(result)

logger.info("*"*88)
def divide_numbers(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logger.error("Помилка: Ділення на нуль.")
    else:
        "Блок else виконується, якщо в блоку try не виникло жодного виключення"
        logger.info(f"Результат ділення {a} на {b}: {result}")
    finally:
        # наприклад збереження в файл
        logger.info("Цей блок завжди виконується, незалежно від того, чи виникла помилка чи ні")

a = 1
b = 1
result = divide_numbers(a, b)
logger.info(f"result {result}")

# while True:
#     #logger.info("**")
#     try:
#         logger.info("**")
#     except:
#         pass #

# try:
#     pass
# finally:
#     pass


def check_age(age):
    if age < 0:
        raise ValueError("Вік не може бути від'ємним")
    return age

# input_age = input("Ваш вік ")
# check_age(-5)


def check_email(mail:str):
    if not isinstance(mail, str):
        raise TypeError("String type only expected")
    if mail.count("@") < 1:
        raise ValueError("@ expected in mailbox")
    return mail

#ZeroDivisionError
#ValueError
#TypeError
#IndexError
#KeyError
#StopIteration

#AssertionError


def sum_2(a, b):
    assert isinstance(a, (int, float)) and isinstance(b, (int, float)), "int, float is expected"
    #if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
    #   raise AssertionError("int, float is expected")
    return a + b

#logger.info(sum_2("a",0))

logger.info(check_email("some@gmail.com"))
logger.info(check_email("s@g.c"))
logger.info(check_email("@"))
# logger.info(check_email(""))
# logger.info(check_email(1))


class TooLargeValueError(Exception):

    def __init__(self, value, limit):
        self.value = value
        self.limit = limit
        message = f"Значення {value} перевищує ліміт {limit}"
        super().__init__(message)

try:
    limit = 100
    user_input = int(input("Введіть число: "))

    if user_input > limit:
        raise TooLargeValueError(user_input, limit)
    else:
        logger.info("Дякую! Ви ввели припустиме значення.")
except TooLargeValueError as e:
    logger.error(f"Помилка: {e}")
except ValueError:
    logger.error("Помилка: Будь ласка, введіть ціле число.")


with open("example.log", "r") as file:
    content = file.read()

file = None
try:
    # Відкриття файлу для читання
    file = open("example.log", "r")

    # Операції змістом файлу
    content = file.read()
except:
    logger.error(f"Виникла помилка: {e}")
finally:
    # Закриття файлу у блоку finally, щоб гарантувати його виклик навіть якщо виникає помилка
    if file is not None:
        file.close()
