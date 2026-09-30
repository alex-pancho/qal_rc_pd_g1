import pytest
import logging
from source import BankAccount

# Налаштування конфігурації логування
logging.basicConfig(

    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
            logging.StreamHandler(),  # Виведення в консоль
            logging.FileHandler('example.log', encoding="utf8")  # Запис у файл
    ]
    )

@pytest.fixture()
def zero_account():
    acc = BankAccount(0)
    yield acc
    del acc

@pytest.fixture()
def one_000_account():
    acc = BankAccount(1000)
    yield acc
    del acc
