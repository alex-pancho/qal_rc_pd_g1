## Вступ в логування

В Python існують різні способи логування подій (logging events). Модуль `logging` є стандартним засобом для логування в Python. Ось декілька прикладів, як ви можете використовувати його для реєстрації подій:

```python
import logging

# Налаштування конфігурації логування
logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Логування подій різного рівня (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.debug('Це повідомлення рівня DEBUG')
logging.info('Це повідомлення рівня INFO')
logging.warning('Це повідомлення рівня WARNING')
logging.error('Це повідомлення рівня ERROR')
logging.critical('Це повідомлення рівня CRITICAL')

```

У цьому прикладі логи будуть зберігатися в файлі "example.log". Ви можете змінити рівень логування за допомогою параметра `level`, і тільки повідомлення з обраного рівня і вище будуть записані.

Якщо ви хочете логувати події в консоль, можете використовувати `StreamHandler`:

```python
import logging

# Налаштування конфігурації логування
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Додавання обробника для виводу в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console_handler)

# Логування подій різного рівня
logging.debug('Це повідомлення рівня DEBUG')
logging.info('Це повідомлення рівня INFO')
logging.warning('Це повідомлення рівня WARNING')
logging.error('Це повідомлення рівня ERROR')
logging.critical('Це повідомлення рівня CRITICAL')

```

В цьому випадку логи будуть виводитися в консоль. Ви можете налаштувати обробник так, як вам потрібно, і додавати його до логера за допомогою `addHandler`.

## Конфігурація логеру

Конфігурація логера може бути виконана різними способами. Одним із підходів є використання файлу конфігурації, який містить параметри налаштувань логування. Інший підхід - використання коду для налаштування логера.

### Використання Файлу Конфігурації:

Створіть файл конфігурації, наприклад, `logging_config.ini`:

```
[loggers]
keys=root,sampleLogger

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=sampleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_sampleLogger]
level=DEBUG
handlers=fileHandler
qualname=sampleLogger
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=sampleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=sampleFormatter
args=('example.log',)

[formatter_sampleFormatter]
format=%(asctime)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S

```

Тепер використайте цей файл для конфігурації логера в коді Python:

```python
import logging
import logging.config

logging.config.fileConfig('logging_config.ini')

# Використання логера
logger = logging.getLogger('sampleLogger')

logger.debug('Це повідомлення рівня DEBUG')
logger.info('Це повідомлення рівня INFO')

```

### Використання Коду для Конфігурації:

```python
import logging

# Створення конфігурації
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),  # Виведення в консоль
                        logging.FileHandler('example.log')  # Запис у файл
                    ])

# Використання логера
logger = logging.getLogger(__name__)

logger.debug('Це повідомлення рівня DEBUG')
logger.info('Це повідомлення рівня INFO')

```

Обирайте підхід, який краще відповідає вашим потребам. Файл конфігурації може бути зручним для великих проектів, де вам потрібно легко змінювати параметри логування без зміни коду. В інших випадках, конфігурація в коді може бути досить зручною.

## Обробники-захоплювачі повідомлень

## Захват у файл

Щоб створити обробник для запису в файл за допомогою модуля `logging`, вам слід використовувати клас `FileHandler`. Ось приклад, як ви можете це зробити:

```python
import logging

# Створення логера
logger = logging.getLogger(__name__)

# Налаштування рівня логування
logger.setLevel(logging.DEBUG)

# Створення обробника для запису в файл
file_handler = logging.FileHandler('logfile.txt')

# Налаштування рівня логування для обробника
file_handler.setLevel(logging.DEBUG)

# Створення форматера для обробника
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Додавання обробника до логера
logger.addHandler(file_handler)

# Логування подій
logger.debug('Це повідомлення рівня DEBUG')
logger.info('Це повідомлення рівня INFO')
logger.warning('Це повідомлення рівня WARNING')
logger.error('Це повідомлення рівня ERROR')
logger.critical('Це повідомлення рівня CRITICAL')

```

У цьому прикладі створюється обробник `FileHandler`, який записує логи у файл з ім'ям "logfile.txt". Форматтер визначає, яким чином буде виглядати кожне повідомлення в файлі.

Важливо пам'ятати, що краще закривати обробник після використання, щоб гарантувати коректне завершення запису в файл:

```python
file_handler.close()

```

Це може бути важливим, особливо якщо ви використовуєте логер в довгостроковому процесі.

## Захват stdout

Щоб створити обробник для виводу в `stdout` (стандартний вивід), ви можете використовувати клас `StreamHandler` з модуля `logging`. Ось приклад:

```python
import logging

# Створення логера
logger = logging.getLogger(__name__)

# Налаштування рівня логування
logger.setLevel(logging.DEBUG)

# Створення обробника для виводу в stdout
console_handler = logging.StreamHandler()

# Налаштування рівня логування для обробника
console_handler.setLevel(logging.DEBUG)

# Створення форматера для обробника
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Додавання обробника до логера
logger.addHandler(console_handler)

# Логування подій
logger.debug('Це повідомлення рівня DEBUG')
logger.info('Це повідомлення рівня INFO')
logger.warning('Це повідомлення рівня WARNING')
logger.error('Це повідомлення рівня ERROR')
logger.critical('Це повідомлення рівня CRITICAL')

```

У цьому прикладі створюється обробник `StreamHandler`, який виводить логи на стандартний вивід (`stdout`). Ви можете налаштувати рівень логування, вибрати формат повідомлень та додати цей обробник до логера.

Якщо вам не потрібно виводити повідомлення з певного рівня, ви можете змінити рівень логування для обробника. Наприклад, якщо ви хочете виводити тільки повідомлення рівня INFO і вище, встановіть `console_handler.setLevel(logging.INFO)`.

## Одночасне використання StreamHandler та FileHandler

Ви можете одночасно використовувати обидва обробники (`StreamHandler` і `FileHandler`) у логері для виводу інформації як в консоль, так і в файл. Ось приклад:

```python
import logging

# Створення логера
logger = logging.getLogger(__name__)

# Налаштування рівня логування
logger.setLevel(logging.DEBUG)

# Створення обробника для виводу в stdout (консоль)
console_handler = logging.StreamHandler()

# Створення обробника для запису в файл
file_handler = logging.FileHandler('logfile.txt')

# Налаштування рівня логування для обробників
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# Створення форматера для обробників
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Налаштування форматера для обробників
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Додавання обробників до логера
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Логування подій
logger.debug('Це повідомлення рівня DEBUG')
logger.info('Це повідомлення рівня INFO')
logger.warning('Це повідомлення рівня WARNING')
logger.error('Це повідомлення рівня ERROR')
logger.critical('Це повідомлення рівня CRITICAL')

```

У цьому прикладі обидва обробники (`console_handler` і `file_handler`) додаються до логера, і повідомлення будуть виводитися як у консоль, так і у файл.

Цей підхід дозволяє вам налаштовувати вивід логів для різних цілей, таких як відладка в консолі та зберігання повідомлень в файлі для подальшого аналізу чи архівації.

## Рівні логування

Рівні логування визначають важливість повідомлень логів і дозволяють вам керувати тим, які повідомлення будуть виводитись або записуватись у лог-файл. У модулі `logging` в Python існує п'ять стандартних рівнів логування:

1. **DEBUG (10):** Найнижчий рівень. Використовується для відладки. Зазвичай виводить деталі про внутрішню роботу програми.
2. **INFO (20):** Інформаційний рівень. Використовується для передачі інформації про хід виконання програми.
3. **WARNING (30):** Рівень попереджень. Використовується для вказівки на можливі проблеми, які не призводять до відмови програми, але вимагають уваги.
4. **ERROR (40):** Рівень помилок. Використовується для вказівки на серйозні проблеми, які призводять до відмови програми.
5. **CRITICAL (50):** Найвищий рівень. Використовується для вказівки на критичні помилки, які можуть призвести до зупинки програми.

Щоб використовувати рівні логування в коді, ви можете встановити рівень для логера чи обробника. Наприклад:

```python
import logging

# Створення логера
logger = logging.getLogger(__name__)

# Встановлення рівня логування для логера
logger.setLevel(logging.DEBUG)

# Створення обробника для виводу логів на консоль
console_handler = logging.StreamHandler()

# Встановлення рівня логування для обробника
console_handler.setLevel(logging.WARNING)

# Додавання обробника до логера
logger.addHandler(console_handler)

# Приклад використання
logger.debug('Це повідомлення для відладки')
logger.info('Це інформаційне повідомлення')
logger.warning('Це повідомлення-попередження')
logger.error('Це повідомлення про помилку')
logger.critical('Це критичне повідомлення')

```

У цьому прикладі логер встановлює рівень логування на `DEBUG`, що дозволяє логувати повідомлення всіх рівнів. Однак обробник `console_handler` встановлює свій власний рівень на `WARNING`, тому будуть виводитись тільки повідомлення рівнів `WARNING`, `ERROR` і `CRITICAL`.

## Можливості форматування логеру

Форматування логера визначає те, які інформаційні елементи включаються у кожне повідомлення логу. Ви можете використовувати ключові слова форматування для додавання різних атрибутів, таких як час логування, рівень логування, текст повідомлення та інші. Ось пояснення деяких з них:

- **%(asctime)s**: Додає час логування у форматі "рік-місяць-день година:хвилина:секунда,мілісекунда".
- **%(levelname)s**: Додає рівень логування (наприклад, DEBUG, INFO, WARNING, ERROR, CRITICAL).
- **%(message)s**: Додає текстове повідомлення логу.
- **%(filename)s**: Додає ім'я файлу, з якого було викликано логування.
- **%(funcName)s**: Додає ім'я функції, з якої було викликано логування.
- **%(lineno)d**: Додає номер рядка у файлі, з якого було викликано логування.
- **%(name)s**: Додає ім'я логера.

Ви можете використовувати ці ключові слова у своєму форматі для створення власного шаблону логування. Ось приклад, як встановити форматування для логера:

```python
import logging

# Створення логера
logger = logging.getLogger(__name__)

# Налаштування рівня логування
logger.setLevel(logging.DEBUG)

# Створення обробника для виводу в stdout (консоль)
console_handler = logging.StreamHandler()

# Налаштування рівня логування для обробника
console_handler.setLevel(logging.DEBUG)

# Створення форматера для обробника
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(name)s - %(filename)s - %(lineno)d - %(funcName)s')

# Налаштування форматера для обробника
console_handler.setFormatter(formatter)

# Додавання обробника до логера
logger.addHandler(console_handler)

# Логування подій
logger.debug('Це повідомлення рівня DEBUG')
logger.info('Це повідомлення рівня INFO')

```

В цьому прикладі `%` перед ключовим словом вказує на використання цього ключового слова для форматування. Можете змінити порядок, додавати або видаляти ключові слова, щоб відповідати вашим потребам форматування логування.

## Примусове завершення логування

Метод `logging.shutdown()` використовується для видалення всіх обробників логування та інших ресурсів, які можуть бути використані модулем `logging`. Виклик цього методу вказує, що логування в програмі завершило свою роботу, і можна видалити всі налаштування.

Цей метод корисний у випадках, коли програма завершує свою роботу, і ви хочете звільнити всі ресурси, пов'язані із системою логування. Приклад використання:

```python
import logging

# Налаштовуємо логер та обробники
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('app.log')
logger.addHandler(file_handler)

# Використовуємо логер
logger.info('Це інформаційне повідомлення')

# Завершуємо логування та видаляємо ресурси
logging.shutdown()

```

При виклику `logging.shutdown()`, всі обробники логів будуть закриті, і буде виконано інші дії, які можуть бути необхідні для завершення логування.

## Строгі твердження assert

В мові програмування Python твердження `assert` використовується для перевірки істинності виразу. Якщо вираз є `False`, тобто не відповідає очікуваному стану, то виконання програми призупиняється, і викидається виключення `AssertionError`.

Синтаксис твердження `assert` виглядає наступним чином:

```python
assert вираз, [повідомлення_про_помилку]
```

- `вираз` - це умова, яка повинна бути істинною.
- `повідомлення_про_помилку` (необов'язково) - це рядок, який буде виведено у випадку, якщо твердження виявиться хибним. Це дає можливість зазначити більш детальне повідомлення про те, що пішло не так.

Приклади використання твердження `assert`:

```python
x = -5
assert x > 0, f"x=={x}, але повинно бути додатнім числом"
```

У цьому прикладі, якщо значення `x` не є додатнім числом, виконається твердження про помилку і виведеться повідомлення `"повинно бути додатнім числом"`.

Твердження `assert` часто використовується для перевірки попередніх умов, допомагаючи забезпечити коректність програми та розробляти її в тестовому режимі. 

<aside>
💡 Важливо враховувати, що в релізному коді використання тверджень `assert` може бути відключено за допомогою флага `-O` при запуску програми (наприклад, `python -O script.py`).
</aside>
