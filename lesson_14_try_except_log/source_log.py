import logging


# Налаштування конфігурації логування
logging.basicConfig(

    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
            logging.StreamHandler(),  # Виведення в консоль
            logging.FileHandler('example.log', encoding="utf8")  # Запис у файл
    ]
    )

logger = logging.getLogger(__name__)

logger.debug('Це повідомлення рівня DEBUG')
logger.info('Це повідомлення рівня INFO')
logger.warning('Це повідомлення рівня WARNING')
logger.error('Це повідомлення рівня ERROR')
logger.critical('Це повідомлення рівня CRITICAL')
"""
- **%(filename)s**: Додає ім'я файлу, з якого було викликано логування.
- **%(funcName)s**: Додає ім'я функції, з якої було викликано логування.
- **%(lineno)d**: Додає номер рядка у файлі, з якого було викликано логування.
- **%(name)s**: Додає ім'я логера.
"""