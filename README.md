# 🐍 Курс «Програмування Python» — QALight
## Викладач курсу: Олександр Панченко / QALight

**Викладач:** Олександр Панченко  
**Організація:** [QALight](https://qalight.ua) · info@qalight.ua  
**Тривалість:** 4 місяці · 50 занять · 100 годин

## 📁 Структура репозиторію

```
python-course/
├── README.md                  ← цей файл
│
├── lectures/                  ← конспекти лекцій та домашні завдання (.md)
│   ├── lecture_11_inheritance_polymorphism.md
│   ├── lecture_12_encapsulation_abstraction.md
│   └── lecture_15_modules_packages.md
│
├── slides/                    ← слайди до занять (.md)
│   ├── slides_inheritance_polymorphism.md
│   ├── slides_encapsulation_abstraction.md
│   ├── slides_iterators_generators.md
│   ├── slides_exceptions_logging.md
│   └── slides_modules_packages.md
│
├── practical/                  ← практичні завдання та проєкти
│   └── project_xx/             ← наскрізний навчальний проєкт
│
└── tests/                     ← тести до проєктів
```

## 🚀 Як почати працювати з репозиторієм

### 1. Вимоги

Перед початком роботи переконайтеся, що у вас встановлено:

| Інструмент | Мінімальна версія | Де завантажити |
|---|---|---|
| Python | 3.11+ | [python.org](https://python.org) |
| Git | 2.x | [git-scm.com](https://git-scm.com) |
| VS Code | актуальна | [code.visualstudio.com](https://code.visualstudio.com) |
| uv | актуальна | `pip install uv` |

> Налаштування середовища детально розглядається на **Занятті 1** і **Занятті 7**.

### 2. Клонування репозиторію

Ці дії виконуються лише один раз на початку роботи!

1. Зробіть форк репозиторіб натиснувши на кнопку "Fork" (Вилка)

```bash
# 2. Клонувати репозиторій
# 2.1 Відкрийте термінал у зручній для роботи папці, в терміналі виконайте команду
git clone https://github.com/<username>/qal_rc_pd_g1.git

# 3. Перейти в директорію проєкту
cd qal_rc_pd_g1
```

> Робота з Git та GitHub детально розглядається на **Занятті 2**.

### 3. Створення та активація віртуального середовища

```bash
# Варіант A — через uv (рекомендовано)
uv venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# Варіант B — через стандартний venv
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

> Віртуальні середовища та інструмент `uv` розглядаються на **Занятті 7**.

### 4. Встановлення залежностей

```bash
# Через uv
uv pip install -r requirements.txt

# Через pip
pip install -r requirements.txt
```

### 5. Обрати навчальний проект

```bash
# Перейти в директорію проєкту
cd practical
```

> Прочитайте та оберіть один з навчальних проектів

### 6. Запуск тестів

```bash
# Запустити всі тести
pytest tests/

# Запустити конкретний файл
pytest tests/test_task.py

# З детальним виводом
pytest tests/ -v
```

> Тестування за допомогою `pytest` розглядається на **Занятті 28**.

## 📚 Матеріали занять

### Організація матеріалів

- **Конспекти та домашні завдання** — доступні в папках `lesson_<номер>_зміст` (наприклад, `lesson_11_inherit_pmorph\lesson_11_inheritance_polymorphism.md`)
- **Слайди у текстовому вигляді** — розташовані у папці `slides/` з відповідним номером заняття (наприклад,`slides\slides_11_nas_poly.md`)
- **Слайди у форматі PPTX** — доступні в навчальній системі LMS

## 🔧 Основні команди Git

### Щоденна робота

```bash
# Перевірити стан репозиторію
git status

# Додати файли до індексу
git add .                        # всі змінені файли
git add lectures/lecture_11.md   # конкретний файл

# Зробити коміт
git commit -m "feat: додати конспект заняття 11"

# Завантажити зміни на GitHub
git push origin main

# Отримати останні зміни з GitHub
git pull origin main
```

### Робота з гілками

```bash
# Створити нову гілку та перейти в неї
git checkout -b feature/lecture-16

# Переглянути всі гілки
git branch -a

# Злити гілку в main
git checkout main
git merge feature/lecture-16

# Видалити гілку після злиття
git branch -d feature/lecture-16
```

### Перегляд історії

```bash
# Лог комітів
git log --oneline

# Що змінилось у файлі
git diff lectures/lecture_11.md
```

> Детальніше про Git розглядається на **Занятті 2**.

## 📦 Основні команди Python / uv

```bash
# Перевірити версію Python
python --version

# Запустити скрипт
python script.py

# Встановити пакет
uv pip install requests

# Зафіксувати залежності
uv pip freeze > requirements.txt

# Переглянути встановлені пакети
uv pip list

# Деактивувати середовище
deactivate
```

## ✅ Чеклист перед першим заняттям

- [ ] Встановлено Python 3.11+
- [ ] Встановлено VS Code з розширенням Python
- [ ] Встановлено Git та налаштовано `git config`
- [ ] Створено акаунт на GitHub
- [ ] Репозиторій клоновано локально
- [ ] Віртуальне середовище створено та активовано
- [ ] Залежності встановлено через `pip install -r requirements.txt`
- [ ] `python --version` — виводить очікувану версію

## 💡 Корисні посилання

- [Документація Python](https://docs.python.org/3/)
- [PEP 8 — стандарт оформлення коду](https://pep8.org/)
- [Real Python — туторіали](https://realpython.com/)
- [Начальна система QALight](https://restart.qalight.ua/login/index.php)