# Заняття 34. DQL — отримання даних

**Викладач:** Олександр Панченко / QALight  
**Курс:** Програмування Python · Модуль 5. PostgreSQL

## Цілі заняття

Ми вже вміємо створювати структуру БД (DDL) і наповнювати її даними (DML). Тепер навчимося **отримувати інформацію**. Це найчастіша робота з базою: у реальних застосунках запитів `SELECT` в рази більше, ніж усіх інших команд разом узятих.

Після заняття ви зможете:

1. Писати `SELECT` з потрібними колонками, обчисленнями та унікальними значеннями (`DISTINCT`)
2. Фільтрувати дані: `WHERE`, `IN`, `BETWEEN`, `IS NULL`, `LIKE`/`ILIKE`
3. Сортувати й розбивати результат на сторінки: `ORDER BY`, `LIMIT`, `OFFSET`
4. З'єднувати таблиці: `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN` (і знати про `FULL JOIN`)
5. Складати запити з кількох таблиць за чітким алгоритмом
6. Знаходити «записи без пари»: курси без уроків, студентів без записів тощо
7. Самостійно виконувати практично будь-які вибірки для свого проєкту

Усі приклади працюють на базі навчальної платформи **LMS**, яку ми проєктували на заняттях 32–33. Читайте текст, відразу виконуйте запити в `psql` або DBeaver і порівнюйте з результатами, що наведені в лекції.

---

## Частина 0. Підготовка: база LMS з тестовими даними

Для JOIN-ів потрібні «цікаві» дані: курс без уроків, студент без жодного запису, завдання без здач. Тому в нашому наборі такі випадки навмисно закладені. Виконайте скрипт повністю. Він видаляє старі таблиці й створює все заново, тож його можна запускати скільки завгодно разів.

### 0.1. Структура

```sql
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS lessons;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    role       TEXT NOT NULL CHECK (role IN ('student', 'teacher')),
    phone      VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title        TEXT NOT NULL,
    description  TEXT,
    teacher_id   INTEGER NOT NULL,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    price        NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (price >= 0),
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

CREATE TABLE lessons (
    id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title     TEXT NOT NULL,
    position  INTEGER NOT NULL CHECK (position > 0),
    content   TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE (course_id, position)
);

CREATE TABLE enrollments (
    user_id     INTEGER NOT NULL,
    course_id   INTEGER NOT NULL,
    enrolled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'completed', 'dropped')),
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id)   REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE assignments (
    id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lesson_id INTEGER NOT NULL,
    title     TEXT NOT NULL,
    max_score INTEGER NOT NULL DEFAULT 100 CHECK (max_score > 0),
    due_date  TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

CREATE TABLE submissions (
    id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    assignment_id INTEGER NOT NULL,
    student_id    INTEGER NOT NULL,
    answer_text   TEXT,
    score         INTEGER CHECK (score >= 0),
    submitted_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
    FOREIGN KEY (student_id)    REFERENCES users(id),
    UNIQUE (assignment_id, student_id)
);
```

### 0.2. Дані

```sql
INSERT INTO users (first_name, last_name, email, role, phone) VALUES
    ('Петро',  'Іваненко', 'petro@lms.ua',      'teacher', '+380671234567'),
    ('Олена',  'Шевченко', 'olena@lms.ua',      'teacher', NULL),
    ('Ірина',  'Коваль',   'iryna@mail.com',    'student', '+380501112233'),
    ('Андрій', 'Мельник',  'andrii@gmail.com',  'student', '+380931234567'),
    ('Марія',  'Бондар',   'maria@gmail.com',   'student', NULL),
    ('Тарас',  'Гнатюк',   'taras@mail.com',    'student', NULL),
    ('Софія',  'Лисенко',  'sofia@gmail.com',   'student', NULL),
    ('Василь', 'Кравець',  'vasyl@lms.ua',      'teacher', NULL);

INSERT INTO courses (title, description, teacher_id, is_published, price, created_at) VALUES
    ('Python Basics',   'Основи Python для початківців',  1, TRUE,  1200, '2026-08-01'),
    ('SQL Basics',      'Вступ до баз даних',             1, TRUE,   900, '2026-08-15'),
    ('Python Advanced', 'ООП, декоратори, асинхронність', 2, FALSE, 1500, '2026-09-01'),
    ('QA Fundamentals', 'Основи тестування ПЗ',           2, TRUE,   800, '2026-09-10'),
    ('Git Essentials',  NULL,                             2, TRUE,     0, '2026-09-20');

INSERT INTO lessons (course_id, title, position) VALUES
    (1, 'Змінні та типи даних',  1),
    (1, 'Умови та цикли',        2),
    (1, 'Функції',               3),
    (2, 'Вступ до SQL',          1),
    (2, 'SELECT та WHERE',       2),
    (2, 'З''єднання таблиць',    3),
    (4, 'Що таке тестування',    1),
    (4, 'Тест-кейси',            2);

INSERT INTO enrollments (user_id, course_id, status) VALUES
    (3, 1, 'active'),
    (3, 2, 'active'),
    (4, 1, 'active'),
    (4, 4, 'completed'),
    (5, 1, 'active'),
    (5, 2, 'dropped'),
    (5, 4, 'active'),
    (7, 2, 'active'),
    (7, 4, 'active');

INSERT INTO assignments (lesson_id, title, max_score, due_date) VALUES
    (1, 'Hello, Python',        100, '2026-10-15 23:59'),
    (2, 'Цикли',                100, '2026-10-22 23:59'),
    (3, 'Функція-калькулятор',  100, '2026-10-30 23:59'),
    (5, 'Перші запити',          50, '2026-11-05 23:59'),
    (6, 'Запити з JOIN',         50, NULL),
    (8, 'Тест-кейс для форми',  100, '2026-11-10 23:59');

INSERT INTO submissions (assignment_id, student_id, answer_text, score, submitted_at) VALUES
    (1, 3, 'print("Hello")',          90,   '2026-10-01 10:00'),
    (1, 4, 'print(1 + 1)',            70,   '2026-10-02 12:30'),
    (1, 5, 'print("hi")',             100,  '2026-10-02 09:15'),
    (2, 3, 'for i in range(3): ...',  85,   '2026-10-08 18:00'),
    (2, 4, 'while True: ...',         NULL, '2026-10-09 11:00'),
    (3, 3, 'def calc(): ...',         NULL, '2026-10-10 20:45'),
    (4, 3, 'SELECT * FROM users;',    45,   '2026-10-12 14:20'),
    (4, 7, 'SELECT email FROM users;', 50,  '2026-10-13 16:10'),
    (6, 4, 'Тест-кейс №1',            80,   '2026-10-14 13:00'),
    (6, 7, 'Тест-кейс №2',            NULL, '2026-10-15 17:30');
```

Запит `INSERT` для `lessons` містить `'З''єднання таблиць'`: апостроф усередині рядка в SQL подвоюється.

### 0.3. Перевірка

```sql
SELECT 'users' AS table_name, COUNT(*) AS rows FROM users
UNION ALL SELECT 'courses',     COUNT(*) FROM courses
UNION ALL SELECT 'lessons',     COUNT(*) FROM lessons
UNION ALL SELECT 'enrollments', COUNT(*) FROM enrollments
UNION ALL SELECT 'assignments', COUNT(*) FROM assignments
UNION ALL SELECT 'submissions', COUNT(*) FROM submissions;
```

`UNION ALL` просто «склеює» результати кількох запитів, тут він потрібен лише для зручної перевірки. Очікувані кількості рядків: `users` 8, `courses` 5, `lessons` 8, `enrollments` 9, `assignments` 6, `submissions` 10. Якщо числа інші, перезапустіть скрипт.

### 0.4. Карта даних: з чого складається LMS

Для запитів із JOIN потрібно чітко бачити, як таблиці пов'язані. Дивіться на ланцюжок зовнішніх ключів:

```text
users (викладач) ──< courses ──< lessons ──< assignments ──< submissions >── users (студент)
                        │
                        └──< enrollments >── users (студент)
```

Читаємо так: один викладач має багато курсів, курс має багато уроків, урок має багато завдань, завдання має багато здач. Здача належить студенту. Студенти й курси пов'язані через `enrollments`.

Закладені «особливі» випадки, які ми будемо шукати JOIN-ами:

| Випадок | Хто |
| ------- | --- |
| Викладач без курсів | Василь Кравець |
| Курси без уроків | `Python Advanced`, `Git Essentials` |
| Студент без жодного запису | Тарас Гнатюк |
| Курси без записаних студентів | `Python Advanced`, `Git Essentials` |
| Завдання без жодної здачі | `Запити з JOIN` |
| Здачі без оцінки (`NULL`) | з id 5, 6 та 10 |
| Курс без опису (`NULL`) | `Git Essentials` |

---

## Частина 1. Що таке DQL і як PostgreSQL виконує SELECT

**DQL (Data Query Language)** — це частина SQL для читання даних. Фактично вона складається з однієї команди, `SELECT`, але з безліччю можливостей.

`SELECT` нічого не змінює в базі: його можна виконувати скільки завгодно разів, і дані залишаться такими самими.

Повний вигляд запиту:

```sql
SELECT     що показати
FROM       з якої таблиці
JOIN       з чим з'єднати
WHERE      які рядки залишити
GROUP BY   як згрупувати
HAVING     які групи залишити
ORDER BY   як відсортувати
LIMIT      скільки рядків узяти
OFFSET     скільки пропустити;
```

Пишемо ми в такому порядку, а ось **виконує** PostgreSQL їх інакше:

| Крок | Що відбувається |
| ---- | --------------- |
| 1 | `FROM` і `JOIN`: беруться таблиці та з'єднуються |
| 2 | `WHERE`: відкидаються непотрібні рядки |
| 3 | `GROUP BY`, `HAVING`: групування (розглянемо в бонусній частині) |
| 4 | `SELECT`: обчислюються колонки та вирази, видаються псевдоніми |
| 5 | `DISTINCT`: прибираються дублі |
| 6 | `ORDER BY`: сортування |
| 7 | `LIMIT` / `OFFSET`: обрізання результату |

Це не теорія заради теорії, а пояснення двох типових помилок.

- **Псевдонім з `SELECT` не можна використати у `WHERE`.** `WHERE` виконується раніше, і про псевдонім ще нічого не знає. А в `ORDER BY` псевдонім працює, бо сортування йде пізніше.
- **`LIMIT` діє в самому кінці.** Спершу база знаходить і сортує всі рядки, і лише потім залишає перші кілька.

---

## Частина 2. SELECT: що саме показувати

### 2.1. Вибір колонок

```sql
-- Усі колонки
SELECT * FROM users;

-- Конкретні колонки
SELECT first_name, last_name, email FROM users;
```

У навчанні `SELECT *` зручний для швидкого огляду таблиці. У коді застосунків його краще не залишати: ви тягнете зайві дані, а зміна структури таблиці може зламати код.

### 2.2. Псевдоніми (AS)

Псевдонім дає колонці зрозуміле ім'я в результаті:

```sql
SELECT
    first_name AS name,
    email      AS login
FROM users;
```

Псевдоніми також присвоюють таблицям. Це критично важливо для JOIN, і ми активно користуватимемося ними нижче:

```sql
SELECT c.title, c.price
FROM courses AS c;       -- AS можна опускати: FROM courses c
```

### 2.3. Обчислення в SELECT

У `SELECT` можна використовувати вирази.

Склеювання рядків оператором `||`:

```sql
SELECT first_name || ' ' || last_name AS full_name, email
FROM users;
```

Арифметика й округлення:

```sql
SELECT title, price, ROUND(price * 0.9, 2) AS price_with_discount
FROM courses;
```

```text
      title      |  price  | price_with_discount
-----------------+---------+---------------------
 Python Basics   | 1200.00 |             1080.00
 SQL Basics      |  900.00 |              810.00
 Python Advanced | 1500.00 |             1350.00
 QA Fundamentals |  800.00 |              720.00
 Git Essentials  |    0.00 |                0.00
```

`COALESCE(a, b)` повертає перше значення, яке не `NULL`. Корисно, щоб замінити «порожнє» на зрозумілий текст:

```sql
SELECT title, COALESCE(description, 'Без опису') AS description
FROM courses;
```

У рядку `Git Essentials` замість `NULL` ви побачите `Без опису`.

### 2.4. DISTINCT: унікальні значення

```sql
SELECT DISTINCT role FROM users;
-- student, teacher

SELECT DISTINCT split_part(email, '@', 2) AS domain FROM users;
-- lms.ua, mail.com, gmail.com
```

`DISTINCT` прибирає повторювані **рядки результату**, а не окремі значення колонок. Якщо ви вибираєте кілька колонок, унікальною має бути комбінація всіх.

---

## Частина 3. WHERE: фільтруємо рядки

`WHERE` залишає лише ті рядки, для яких умова істинна.

### 3.1. Порівняння

```sql
SELECT title, price FROM courses WHERE price > 1000;     -- >  >=  <  <=
SELECT title FROM courses WHERE is_published = TRUE;
SELECT title FROM courses WHERE id <> 3;                 -- не дорівнює (також !=)
```

### 3.2. AND, OR, NOT

```sql
-- Опубліковані курси викладача 1
SELECT title FROM courses
WHERE is_published = TRUE AND teacher_id = 1;
-- Python Basics, SQL Basics

-- Чернетки або безкоштовні курси
SELECT title FROM courses
WHERE is_published = FALSE OR price = 0;
-- Python Advanced, Git Essentials

-- Заперечення
SELECT title FROM courses WHERE NOT is_published;
-- Python Advanced
```

Якщо в умові є і `AND`, і `OR`, **завжди ставте дужки**. `AND` має вищий пріоритет за `OR`, і без дужок результат часто не той, що ви очікуєте:

```sql
-- Опубліковані курси будь-кого з двох викладачів
SELECT title FROM courses
WHERE (teacher_id = 1 OR teacher_id = 2) AND is_published = TRUE;
```

### 3.3. IN: належність до списку

`IN` замінює довгий ланцюжок `OR`:

```sql
SELECT id, email FROM users WHERE id IN (1, 2, 3);
-- те саме, що id = 1 OR id = 2 OR id = 3

SELECT title FROM courses WHERE id NOT IN (3, 5);
```

`IN` також приймає **підзапит**:

```sql
-- Курси, на які записаний хоча б один студент
SELECT title FROM courses
WHERE id IN (SELECT course_id FROM enrollments);
```

Результат: `Python Basics`, `SQL Basics`, `QA Fundamentals`. Для таких задач часто краще підходить JOIN, і про це ми поговоримо нижче.

### 3.4. BETWEEN: діапазон

`BETWEEN a AND b` включає **обидві** межі:

```sql
SELECT title, price FROM courses WHERE price BETWEEN 800 AND 1200;
-- Python Basics (1200), SQL Basics (900), QA Fundamentals (800)

-- Завдання з дедлайном у другій половині жовтня
SELECT title, due_date FROM assignments
WHERE due_date BETWEEN '2026-10-15' AND '2026-10-31';
-- Hello, Python; Цикли; Функція-калькулятор
```

Обережно з датами. Запис `'2026-10-31'` означає `2026-10-31 00:00:00`. Тож завдання з дедлайном `2026-10-31 18:00` у вибірку **не потрапить**. Для надійності використовуйте напіввідкритий проміжок:

```sql
WHERE due_date >= '2026-10-15' AND due_date < '2026-11-01'
```

### 3.5. IS NULL та IS NOT NULL

`NULL` означає «значення невідоме або відсутнє». З ним не можна порівнювати через `=`: умова `score = NULL` ніколи не виконується (результат порівняння з `NULL` є «невідомо», а не «так»). Правильно:

```sql
-- Здачі, які ще не оцінені
SELECT id, student_id, assignment_id FROM submissions WHERE score IS NULL;
-- id: 5, 6, 10

-- Курси з описом
SELECT title FROM courses WHERE description IS NOT NULL;

-- Користувачі без телефону
SELECT first_name, email FROM users WHERE phone IS NULL;
-- 5 користувачів: Олена, Марія, Тарас, Софія, Василь
```

Важливий наслідок: умова `score < 80` **не повертає** рядки з `NULL`. Якщо ви хочете «усі, хто не набрав 80», включно з неоціненими, пишіть явно:

```sql
WHERE score < 80 OR score IS NULL
```

### 3.6. LIKE та ILIKE: пошук за шаблоном

У шаблоні є два спеціальні символи:

| Символ | Значення |
| ------ | -------- |
| `%` | будь-яка кількість будь-яких символів (також нуль) |
| `_` | рівно один будь-який символ |

```sql
-- Починається з 'Python'
SELECT title FROM courses WHERE title LIKE 'Python%';
-- Python Basics, Python Advanced

-- Закінчується на 'Basics'
SELECT title FROM courses WHERE title LIKE '%Basics';
-- Python Basics, SQL Basics

-- Містить 'SQL'
SELECT title FROM lessons WHERE title LIKE '%SQL%';
-- Вступ до SQL

-- Пошта на gmail
SELECT email FROM users WHERE email LIKE '%@gmail.com';
-- andrii@gmail.com, maria@gmail.com, sofia@gmail.com

-- Пошта НЕ на gmail
SELECT email FROM users WHERE email NOT LIKE '%@gmail.com';
```

`LIKE` чутливий до регістру. Для пошуку без урахування регістру в PostgreSQL є `ILIKE`:

```sql
SELECT title FROM courses WHERE title ILIKE '%git%';
-- Git Essentials
```

Підказка щодо продуктивності: `LIKE 'abc%'` (префікс) може використовувати індекс, а `LIKE '%abc'` та `LIKE '%abc%'` на великих таблицях змушують базу перебирати всі рядки.

---

## Частина 4. ORDER BY, LIMIT, OFFSET

### 4.1. ORDER BY: сортування

```sql
-- За зростанням (ASC за замовчуванням)
SELECT title, price FROM courses ORDER BY price;

-- За спаданням
SELECT title, price FROM courses ORDER BY price DESC;
-- Python Advanced, Python Basics, SQL Basics, QA Fundamentals, Git Essentials

-- За кількома колонками: курс, а в ньому позиція уроку
SELECT course_id, position, title FROM lessons ORDER BY course_id, position;
```

Сортування рядків із кирилицею залежить від налаштувань мови бази (collation). У різних базах порядок літер, наприклад `І`, може відрізнятися, тому в прикладах лекції ми сортуємо за числами та латинськими полями.

**NULL і сортування.** У PostgreSQL при `DESC` значення `NULL` йдуть **першими**. Для журналу оцінок це неприємно, бо зверху були б неоцінені роботи. Керуйте цим явно:

```sql
SELECT id, score
FROM submissions
ORDER BY score DESC NULLS LAST, id;
```

```text
 id | score
----+-------
  3 |   100
  1 |    90
  4 |    85
  9 |    80
  2 |    70
  8 |    50
  7 |    45
  5 |
  6 |
 10 |
```

### 4.2. LIMIT: обмежуємо кількість рядків

```sql
-- Три найдорожчі курси
SELECT title, price FROM courses ORDER BY price DESC LIMIT 3;
-- Python Advanced, Python Basics, SQL Basics

-- Остання здача
SELECT id, submitted_at FROM submissions ORDER BY submitted_at DESC LIMIT 1;
-- id 10
```

Шаблон «ORDER BY ... DESC LIMIT N» — це спосіб отримати «топ N» або «останні N».

### 4.3. OFFSET: пропускаємо рядки (пагінація)

```sql
-- Сторінка 1: перші 3 користувачі
SELECT id, email FROM users ORDER BY email LIMIT 3 OFFSET 0;
-- andrii@gmail.com, iryna@mail.com, maria@gmail.com

-- Сторінка 2
SELECT id, email FROM users ORDER BY email LIMIT 3 OFFSET 3;
-- olena@lms.ua, petro@lms.ua, sofia@gmail.com

-- Сторінка 3
SELECT id, email FROM users ORDER BY email LIMIT 3 OFFSET 6;
-- taras@mail.com, vasyl@lms.ua
```

Формула для сторінки `page` по `per_page` записів:

```text
OFFSET = (page - 1) * per_page
```

Два правила пагінації:

1. **Завжди додавайте `ORDER BY`.** Без нього порядок рядків не гарантований, і на різних сторінках можуть повторюватися або губитися записи. Якщо сортуєте за неунікальним полем, додайте до нього `id` як другий критерій.
2. Для загальної кількості сторінок виконуйте окремий запит `SELECT COUNT(*) ...`.

---

## Частина 5. JOIN: з'єднуємо таблиці

### 5.1. Навіщо потрібен JOIN

На минулих заняттях ми нормалізували дані: розклали їх по різних таблицях, щоб прибрати дублювання. У таблиці `courses` лежить не ім'я викладача, а його `teacher_id`:

```sql
SELECT id, title, teacher_id FROM courses;
```

```text
 id |      title      | teacher_id
----+-----------------+------------
  1 | Python Basics   |          1
  2 | SQL Basics      |          1
  3 | Python Advanced |          2
  4 | QA Fundamentals |          2
  5 | Git Essentials  |          2
```

Користувачу цифри `1` та `2` нічого не кажуть. Щоб показати ім'я викладача, потрібно «підтягнути» дані з `users`. Це робить **JOIN**: він складає рядки двох таблиць у спільний результат за правилом, яке ми вказуємо в `ON`.

Загальна форма:

```sql
SELECT ...
FROM table_a a
JOIN table_b b ON b.fk_column = a.id;
```

`ON` задає зв'язок, як правило `зовнішній_ключ = первинний_ключ`.

### 5.2. INNER JOIN: лише ті, у кого є пара

```sql
SELECT c.id, c.title, u.first_name, u.last_name
FROM courses c
INNER JOIN users u ON u.id = c.teacher_id
ORDER BY c.id;
```

```text
 id |      title      | first_name | last_name
----+-----------------+------------+-----------
  1 | Python Basics   | Петро      | Іваненко
  2 | SQL Basics      | Петро      | Іваненко
  3 | Python Advanced | Олена      | Шевченко
  4 | QA Fundamentals | Олена      | Шевченко
  5 | Git Essentials  | Олена      | Шевченко
```

`INNER JOIN` залишає лише ті рядки, для яких знайшлася пара в обох таблицях. Слово `INNER` необов'язкове: просто `JOIN` означає те саме.

Зверніть увагу на три речі:

- **Псевдоніми** (`c`, `u`) скорочують запис, а перед іменами колонок (`c.title`, `u.id`) показують, з якої вони таблиці.
- **Колонки з однаковими іменами** треба уточнювати. Якщо написати просто `id`, PostgreSQL повідомить `column reference "id" is ambiguous`, бо `id` є в обох таблицях.
- Викладача Василя Кравця (id 8) у результаті немає: у нього немає курсів, тож пари для нього не знайшлося.

### 5.3. З'єднуємо більше двох таблиць

Кожен наступний `JOIN` додає ще одну таблицю до результату. Задача: хто зі студентів зараз активно навчається на яких курсах.

```sql
SELECT c.title AS course, u.first_name, u.last_name
FROM enrollments e
JOIN users   u ON u.id = e.user_id
JOIN courses c ON c.id = e.course_id
WHERE e.status = 'active'
ORDER BY c.id, u.id;
```

```text
     course      | first_name | last_name
-----------------+------------+-----------
 Python Basics   | Ірина      | Коваль
 Python Basics   | Андрій     | Мельник
 Python Basics   | Марія      | Бондар
 SQL Basics      | Ірина      | Коваль
 SQL Basics      | Софія      | Лисенко
 QA Fundamentals | Марія      | Бондар
 QA Fundamentals | Софія      | Лисенко
```

Сім рядків: рівно стільки записів зі статусом `active` у таблиці `enrollments`. Відкинуті записи `completed` (Андрій на QA) та `dropped` (Марія на SQL).

Тут `enrollments` стоїть у `FROM` як «центральна» таблиця, а `users` і `courses` з'єднуються з нею. Таблицю-зв'язку M:N майже завжди так і використовують.

### 5.4. LEFT JOIN: усі зліва, навіть без пари

Порівняйте. Спробуємо вивести всі курси разом з уроками:

```sql
SELECT c.title AS course, l.position, l.title AS lesson
FROM courses c
INNER JOIN lessons l ON l.course_id = c.id
ORDER BY c.id, l.position;
```

Отримаємо 8 рядків, і в них **немає** курсів `Python Advanced` та `Git Essentials`: у них немає уроків. А тепер `LEFT JOIN`:

```sql
SELECT c.title AS course, l.position, l.title AS lesson
FROM courses c
LEFT JOIN lessons l ON l.course_id = c.id
ORDER BY c.id, l.position;
```

```text
     course      | position |        lesson
-----------------+----------+----------------------
 Python Basics   |        1 | Змінні та типи даних
 Python Basics   |        2 | Умови та цикли
 Python Basics   |        3 | Функції
 SQL Basics      |        1 | Вступ до SQL
 SQL Basics      |        2 | SELECT та WHERE
 SQL Basics      |        3 | З'єднання таблиць
 Python Advanced |          |
 QA Fundamentals |        1 | Що таке тестування
 QA Fundamentals |        2 | Тест-кейси
 Git Essentials  |          |
```

`LEFT JOIN` (повна назва `LEFT OUTER JOIN`) залишає **усі** рядки лівої таблиці (тієї, що стоїть у `FROM`). Якщо для рядка не знайшлося пари справа, колонки правої таблиці заповнюються `NULL`. Усього вийшло 10 рядків.

Як вибрати між ними:

- Потрібні лише повні пари (курс **і** його уроки): `INNER JOIN`.
- Потрібні **всі** об'єкти зліва, навіть якщо пов'язаних даних немає: `LEFT JOIN`.

### 5.5. Знаходимо «записи без пари»: LEFT JOIN + IS NULL

Це один із найкорисніших патернів в SQL. Після `LEFT JOIN` рядки без пари мають `NULL` у колонках правої таблиці. Додаємо `WHERE ... IS NULL` і залишаємо саме їх.

Курси без жодного уроку:

```sql
SELECT c.id, c.title
FROM courses c
LEFT JOIN lessons l ON l.course_id = c.id
WHERE l.id IS NULL;
-- Python Advanced, Git Essentials
```

Студенти, які не записані ні на один курс:

```sql
SELECT u.id, u.first_name, u.last_name
FROM users u
LEFT JOIN enrollments e ON e.user_id = u.id
WHERE u.role = 'student' AND e.user_id IS NULL;
-- Тарас Гнатюк
```

Викладачі без курсів:

```sql
SELECT u.id, u.first_name, u.last_name
FROM users u
LEFT JOIN courses c ON c.teacher_id = u.id
WHERE u.role = 'teacher' AND c.id IS NULL;
-- Василь Кравець
```

Завдання, на які ніхто не здав роботу:

```sql
SELECT a.id, a.title
FROM assignments a
LEFT JOIN submissions s ON s.assignment_id = a.id
WHERE s.id IS NULL;
-- Запити з JOIN
```

Правило для `IS NULL`: перевіряйте колонку, яка в правій таблиці **не може бути** `NULL` у справжніх рядках, найкраще первинний ключ (`l.id`, `s.id`). Інакше ви сплутаєте «немає пари» з «пара є, але значення порожнє».

### 5.6. Пастка: умова в ON чи у WHERE

Задача: вивести **всі** курси і для кожного активних студентів. Курси без студентів теж мають залишитись.

```sql
-- ✅ Правильно: умова про статус у ON
SELECT c.title, e.user_id
FROM courses c
LEFT JOIN enrollments e
       ON e.course_id = c.id AND e.status = 'active'
ORDER BY c.id, e.user_id;
```

Результат містить 9 рядків: курси `Python Advanced` та `Git Essentials` присутні, з `NULL` у `user_id`.

```sql
-- ❌ Помилка: умова про статус у WHERE
SELECT c.title, e.user_id
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
WHERE e.status = 'active'
ORDER BY c.id, e.user_id;
```

Тут лише 7 рядків: курсів без студентів не стало. Причина: у рядків без пари `e.status` дорівнює `NULL`, а `NULL = 'active'` не є істиною, тож `WHERE` їх відкидає. `LEFT JOIN` непомітно перетворився на `INNER JOIN`.

Правило: **умови на правій таблиці `LEFT JOIN` пишемо в `ON`**, а не у `WHERE`. Виняток: якщо ми свідомо шукаємо відсутні пари (`WHERE правий.id IS NULL`, як у 5.5).

### 5.7. RIGHT JOIN та FULL JOIN

`RIGHT JOIN` робить те саме, що `LEFT JOIN`, але дзеркально: залишає **всі рядки правої** таблиці. Ці два запити повертають однаковий результат:

```sql
-- Курси та їхні уроки (усі курси)
SELECT c.title, l.title
FROM courses c
LEFT JOIN lessons l ON l.course_id = c.id;

-- Те саме, таблиці просто поміняли місцями
SELECT c.title, l.title
FROM lessons l
RIGHT JOIN courses c ON l.course_id = c.id;
```

На практиці `RIGHT JOIN` майже не використовують: будь-який `RIGHT JOIN` можна переписати як `LEFT JOIN`, поміняти таблиці місцями, а читати запит «зліва направо» простіше. Але ви маєте його розпізнавати в чужому коді.

`FULL JOIN` (`FULL OUTER JOIN`) залишає всі рядки **обох** таблиць: де немає пари, підставляється `NULL` з відповідного боку. Він рідкісний: знадобиться, коли потрібно побачити неузгодженості в обидва боки, наприклад порівняти два списки.

### 5.8. Підсумкова таблиця типів JOIN

Порівняємо на парі `courses` та `lessons` (5 курсів, 8 уроків, два курси без уроків):

| JOIN | Що залишає | Рядків у результаті |
| ---- | ---------- | ------------------- |
| `courses INNER JOIN lessons` | лише пари | 8 |
| `courses LEFT JOIN lessons` | усі курси + їхні уроки | 10 |
| `courses RIGHT JOIN lessons` | усі уроки + їхні курси | 8 (кожен урок має курс) |
| `courses FULL JOIN lessons` | усе з обох таблиць | 10 |

---

## Частина 6. Як складати запит: покроковий метод

Складні запити не пишуть «з голови» за один раз. Дотримуйтесь алгоритму з шести кроків.

1. **Результат.** Які колонки мають бути у відповіді? Що в рядку: студент, курс, оцінка?
2. **Таблиці.** У яких таблицях лежать ці дані?
3. **Шлях.** Як ці таблиці пов'язані? Знайдіть ланцюжок зовнішніх ключів на карті з частини 0.4.
4. **Тип JOIN.** Чи можуть бути об'єкти без пари, які мені потрібні? Якщо так, то `LEFT JOIN`.
5. **Фільтри.** Які умови залишають потрібні рядки?
6. **Порядок і обсяг.** Як сортувати й чи потрібен `LIMIT`?

Будуйте запит **по частинах**, запускаючи його після кожного кроку, і перевіряйте кількість рядків.

### Приклад: які здачі чекають на перевірку викладача Петра

**Крок 1. Результат:** ідентифікатор здачі, студент, курс, завдання, дата здачі.

**Крок 2–3. Таблиці й шлях.** Ім'я студента береться з `users`, але через здачу. Курс ми знаходимо ланцюжком: `submissions` → `assignments` → `lessons` → `courses`. Викладач курсу задається `courses.teacher_id`.

**Починаємо з основи** і спершу беремо лише здачі без оцінки:

```sql
SELECT * FROM submissions WHERE score IS NULL;
-- 3 рядки: 5, 6, 10
```

**Підключаємо завдання, урок і курс**, щоб дістатися до `teacher_id`:

```sql
SELECT s.id, a.title AS assignment, c.title AS course, c.teacher_id
FROM submissions s
JOIN assignments a ON a.id = s.assignment_id
JOIN lessons     l ON l.id = a.lesson_id
JOIN courses     c ON c.id = l.course_id
WHERE s.score IS NULL;
-- Знову 3 рядки: ми нічого не втратили і не розмножили
```

Кількість рядків не змінилась, і це добрий знак: кожна здача має рівно одне завдання, один урок і один курс.

**Підключаємо студента та додаємо фільтр за викладачем:**

```sql
SELECT
    s.id AS submission_id,
    st.first_name || ' ' || st.last_name AS student,
    c.title AS course,
    a.title AS assignment,
    s.submitted_at
FROM submissions s
JOIN users       st ON st.id = s.student_id
JOIN assignments a  ON a.id  = s.assignment_id
JOIN lessons     l  ON l.id  = a.lesson_id
JOIN courses     c  ON c.id  = l.course_id
WHERE s.score IS NULL
  AND c.teacher_id = 1
ORDER BY s.submitted_at;
```

```text
 submission_id |     student     |     course    |     assignment      |    submitted_at
---------------+-----------------+---------------+---------------------+---------------------
             5 | Андрій Мельник  | Python Basics | Цикли               | 2026-10-09 11:00:00
             6 | Ірина Коваль    | Python Basics | Функція-калькулятор | 2026-10-10 20:45:00
```

Здача 10 (Софія, курс QA Fundamentals) у списку відсутня, бо цей курс веде Олена, а не Петро.

### Ще один приклад: журнал усіх здач

Ось запит, який поєднує п'ять таблиць. Це зручна шпаргалка для будь-яких звітів по успішності:

```sql
SELECT
    s.id,
    st.first_name || ' ' || st.last_name AS student,
    c.title AS course,
    a.title AS assignment,
    s.score,
    a.max_score
FROM submissions s
JOIN users       st ON st.id = s.student_id
JOIN assignments a  ON a.id  = s.assignment_id
JOIN lessons     l  ON l.id  = a.lesson_id
JOIN courses     c  ON c.id  = l.course_id
ORDER BY s.id;
```

```text
 id |     student     |      course     |      assignment      | score | max_score
----+-----------------+-----------------+----------------------+-------+-----------
  1 | Ірина Коваль    | Python Basics   | Hello, Python        |    90 |       100
  2 | Андрій Мельник  | Python Basics   | Hello, Python        |    70 |       100
  3 | Марія Бондар    | Python Basics   | Hello, Python        |   100 |       100
  4 | Ірина Коваль    | Python Basics   | Цикли                |    85 |       100
  5 | Андрій Мельник  | Python Basics   | Цикли                |       |       100
  6 | Ірина Коваль    | Python Basics   | Функція-калькулятор  |       |       100
  7 | Ірина Коваль    | SQL Basics      | Перші запити         |    45 |        50
  8 | Софія Лисенко   | SQL Basics      | Перші запити         |    50 |        50
  9 | Андрій Мельник  | QA Fundamentals | Тест-кейс для форми  |    80 |       100
 10 | Софія Лисенко   | QA Fundamentals | Тест-кейс для форми  |       |       100
```

Завдання `Запити з JOIN` у цьому журналі немає: на нього немає жодної здачі, а `INNER JOIN` бере лише пари. Якби ми хотіли побачити й його, то почали б із `assignments` та використали `LEFT JOIN` до `submissions`.

---

## Частина 7. Бонус: підрахунки та групування

Реальні вибірки рідко обходяться без підрахунків: «скільки студентів на курсі?», «середня оцінка?». Для цього є агрегатні функції та `GROUP BY`. Тут лише короткий огляд, щоб ваші запити були практичними.

| Функція | Що робить |
| ------- | --------- |
| `COUNT(*)` | кількість рядків |
| `COUNT(колонка)` | кількість значень, що не `NULL` |
| `SUM(колонка)` | сума |
| `AVG(колонка)` | середнє (`NULL` ігноруються) |
| `MIN(колонка)`, `MAX(колонка)` | мінімум і максимум |

`GROUP BY` розбиває рядки на групи, і функція рахується окремо для кожної групи. Усі колонки в `SELECT`, які не є агрегатами, мають бути у `GROUP BY`.

### Кількість активних студентів на кожному курсі

```sql
SELECT c.title, COUNT(e.user_id) AS students
FROM courses c
LEFT JOIN enrollments e
       ON e.course_id = c.id AND e.status = 'active'
GROUP BY c.id, c.title
ORDER BY c.id;
```

```text
      title      | students
-----------------+----------
 Python Basics   |        3
 SQL Basics      |        2
 Python Advanced |        0
 QA Fundamentals |        2
 Git Essentials  |        0
```

Тут важливі дві деталі: `LEFT JOIN`, щоб не загубити курси без студентів, та `COUNT(e.user_id)`, а не `COUNT(*)`. `COUNT(*)` для курсу без студентів видав би `1` (рядок із `NULL`), а `COUNT(e.user_id)` правильно дає `0`.

### Статистика оцінок по курсах

```sql
SELECT
    c.title,
    COUNT(*)                  AS submissions,
    COUNT(s.score)            AS graded,
    ROUND(AVG(s.score), 2)    AS avg_score
FROM submissions s
JOIN assignments a ON a.id = s.assignment_id
JOIN lessons     l ON l.id = a.lesson_id
JOIN courses     c ON c.id = l.course_id
GROUP BY c.id, c.title
ORDER BY avg_score DESC;
```

```text
      title      | submissions | graded | avg_score
-----------------+-------------+--------+-----------
 Python Basics   |           6 |      4 |     86.25
 QA Fundamentals |           2 |      1 |     80.00
 SQL Basics      |           2 |      2 |     47.50
```

`AVG` ігнорує `NULL`, тому середнє рахується лише по оцінених роботах (4 з 6 для Python Basics).

### HAVING: фільтр по групах

`WHERE` фільтрує **рядки до** групування, а `HAVING` фільтрує **групи після** нього:

```sql
-- Студенти, які здали щонайменше три роботи
SELECT st.first_name, st.last_name, COUNT(*) AS submissions
FROM submissions s
JOIN users st ON st.id = s.student_id
GROUP BY st.id, st.first_name, st.last_name
HAVING COUNT(*) >= 3
ORDER BY submissions DESC;
-- Ірина Коваль (4), Андрій Мельник (3)
```

---

## Частина 8. Типові помилки

| Помилка | Що відбувається | Як правильно |
| ------- | --------------- | ------------ |
| `WHERE score = NULL` | нічого не знаходить | `WHERE score IS NULL` |
| `JOIN` без `ON` або `FROM a, b` без умови | **декартів добуток**: кожен рядок з кожним (8 × 5 = 40 рядків для `users` і `courses`) | завжди вказуйте `ON` |
| Просто `id` у запиті з JOIN | `column reference "id" is ambiguous` | `c.id`, `u.id` |
| Умова правої таблиці `LEFT JOIN` у `WHERE` | `LEFT JOIN` перетворюється на `INNER` | умову пишіть у `ON` |
| `COUNT(*)` при `LEFT JOIN` | курс без студентів дає `1` | `COUNT(права_таблиця.id)` |
| `LIMIT` без `ORDER BY` | випадковий порядок, дублі між сторінками | завжди сортуйте |
| `AND` та `OR` без дужок | умова працює інакше, ніж задумано | ставте дужки |
| `score < 80` для оцінених і неоцінених | `NULL` не потрапляють у результат | додати `OR score IS NULL` |
| Псевдонім із `SELECT` у `WHERE` | `column does not exist` | повторити вираз або використати підзапит |
| `BETWEEN` для часу з датою-межею | кінець діапазону обрізається о 00:00 | `>= початок AND < наступний день` |
| `SELECT *` у коді застосунку | зайві дані, крихкий код | перелічуйте потрібні колонки |

Корисна звичка: якщо після `JOIN` кількість рядків раптом зросла або зменшилась, зупиніться й розберіться чому, перш ніж писати далі. Часто це означає, що зв'язок «один до багатьох» розмножив рядки, або що `INNER JOIN` загубив об'єкти без пари.

---

## Практичні завдання

Усі запити зберігайте у файлі `dql_practice.sql`. Над кожним запитом пишіть коментарем номер завдання. Відповіді для самоперевірки наведені нижче.

### Рівень 1. Одна таблиця

1. Виведіть назви та ціни всіх курсів, від найдорожчого до найдешевшого.
2. Виведіть опубліковані курси з ціною не більше 1000.
3. Виведіть користувачів із поштою на `lms.ua`.
4. Виведіть курси, у яких немає опису.
5. Виведіть студентів, пошта яких не на `gmail.com`.
6. Виведіть завдання без дедлайну.
7. Виведіть здачі, які ще не оцінені.
8. Виведіть три найновіші здачі.
9. Виведіть другу сторінку курсів (по 2 на сторінці, сортування за `id`).
10. Виведіть курси з ціною від 800 до 1200 включно.
11. Знайдіть курси, у назві яких є слово `basics`, незалежно від регістру.

### Рівень 2. JOIN

12. Виведіть усі курси разом з іменем та прізвищем викладача (`INNER JOIN`).
13. Виведіть усі уроки з назвою курсу, відсортовані за курсом і позицією.
14. Виведіть активних студентів кожного курсу (назва курсу, ім'я, прізвище).
15. Знайдіть курси без жодного уроку.
16. Знайдіть студентів, які не записані ні на один курс.
17. Знайдіть викладачів, у яких немає курсів.
18. Виведіть усі курси та кількість активних студентів на кожному, включно з нулями.
19. Знайдіть завдання, на які ще ніхто не здав роботу.

### Рівень 3. Складні вибірки

20. Для викладача Олени (`olena@lms.ua`) виведіть неоцінені здачі: студент, курс, завдання.
21. Виведіть журнал студентки Ірини (`iryna@mail.com`): курс, завдання, оцінка, максимальний бал, оцінка у відсотках (округлено до 1 знака).
22. Виведіть трьох студентів із найбільшою сумою оцінок.
23. Для кожного курсу виведіть кількість здач і середню оцінку, включно з курсами без жодної здачі (у них має бути `0` здач).

### Рівень 4. Власний проєкт

24. Складіть для своєї БД 10 запитів: 4 без JOIN (з `WHERE`, `LIKE`, `ORDER BY`, `LIMIT`), 4 з `INNER JOIN` та `LEFT JOIN`, 2 на пошук «записів без пари».
25. До кожного запиту напишіть коментарем, яке питання бізнесу він відповідає, і приблизно, скільки рядків очікуєте.

---

## Відповіді для самоперевірки

| № | Очікуваний результат |
| - | -------------------- |
| 1 | 5 рядків: Python Advanced 1500, Python Basics 1200, SQL Basics 900, QA Fundamentals 800, Git Essentials 0 |
| 2 | 3 рядки: SQL Basics, QA Fundamentals, Git Essentials |
| 3 | 3 рядки: Петро, Олена, Василь |
| 4 | 1 рядок: Git Essentials |
| 5 | 2 рядки: Ірина Коваль, Тарас Гнатюк |
| 6 | 1 рядок: Запити з JOIN |
| 7 | 3 рядки: id 5, 6, 10 |
| 8 | 3 рядки: id 10, 9, 8 |
| 9 | 2 рядки: Python Advanced, QA Fundamentals |
| 10 | 3 рядки: Python Basics, SQL Basics, QA Fundamentals |
| 11 | 2 рядки: Python Basics, SQL Basics |
| 12 | 5 рядків: Петро веде курси 1 і 2, Олена веде 3, 4 і 5 |
| 13 | 8 рядків; курсів `Python Advanced` та `Git Essentials` у результаті немає |
| 14 | 7 рядків (див. частину 5.3) |
| 15 | 2 рядки: Python Advanced, Git Essentials |
| 16 | 1 рядок: Тарас Гнатюк |
| 17 | 1 рядок: Василь Кравець |
| 18 | 5 рядків: 3, 2, 0, 2, 0 (за порядком `id` курсів) |
| 19 | 1 рядок: Запити з JOIN |
| 20 | 1 рядок: здача 10, Софія Лисенко, QA Fundamentals, Тест-кейс для форми |
| 21 | 4 рядки (здачі 1, 4, 6, 7): 90.0%, 85.0%, `NULL` (ще не оцінено), 90.0% |
| 22 | Ірина Коваль 220, Андрій Мельник 150, Марія Бондар 100 |
| 23 | 5 рядків. Python Basics: 6 здач, середня 86.25; SQL Basics: 2, 47.50; QA Fundamentals: 2, 80.00; Python Advanced і Git Essentials: 0 здач (середня `NULL`) |

Підказки до завдань, які найчастіше викликають труднощі:

- **Завдання 18 і 23:** потрібен `LEFT JOIN` та `COUNT` по колонці правої таблиці. Для 23 пам'ятайте, що курс пов'язаний зі здачами ланцюжком `courses` → `lessons` → `assignments` → `submissions`, і всі ці з'єднання мають бути `LEFT JOIN`, інакше курси без уроків зникнуть.
- **Завдання 21:** щоб відсоток був дробовим, множте на `100.0`, а не на `100`: `ROUND(100.0 * s.score / a.max_score, 1)`. Цілочисельне ділення відкине дробову частину.
- **Завдання 22:** потрібні `SUM`, `GROUP BY`, `ORDER BY ... DESC` та `LIMIT 3`. `NULL`-оцінки `SUM` ігнорує.

---

## Підсумок

На цьому занятті ми навчилися отримувати інформацію з бази даних:

- `SELECT` вибирає колонки, обчислює вирази, а `DISTINCT` прибирає дублікати
- `WHERE` фільтрує рядки: порівняння, `AND`/`OR`/`NOT`, `IN`, `BETWEEN`, `IS NULL`, `LIKE`/`ILIKE`
- `ORDER BY`, `LIMIT`, `OFFSET` задають порядок, обсяг і сторінки результату
- `INNER JOIN` залишає лише пари; `LEFT JOIN` зберігає всі рядки лівої таблиці; `RIGHT JOIN` робить те саме дзеркально; `FULL JOIN` зберігає все з обох сторін
- Патерн `LEFT JOIN ... WHERE правий.id IS NULL` знаходить записи без пари
- Умови правої таблиці `LEFT JOIN` пишемо в `ON`, а не у `WHERE`
- Складні запити будуємо покроково: результат → таблиці → шлях → тип JOIN → фільтри → сортування
- `COUNT`, `AVG`, `GROUP BY`, `HAVING` перетворюють вибірки на звіти

Тепер ви можете відповісти SQL-запитом практично на будь-яке питання про дані вашого проєкту.

## Питання для самоперевірки

1. У якому порядку PostgreSQL виконує частини запиту `SELECT`? Чому псевдонім не працює у `WHERE`, але працює в `ORDER BY`?
2. Чому `score = NULL` ніколи не спрацює? Як перевірити відсутність значення?
3. Чому умова `score < 80` не знаходить неоцінені здачі?
4. Чим `BETWEEN` відрізняється від пари `>=` та `<`? У чому небезпека `BETWEEN` для дат із часом?
5. Чим `LIKE` відрізняється від `ILIKE`? Які символи є метасимволами?
6. Чому `LIMIT` потрібно завжди поєднувати з `ORDER BY`? Як обчислити `OFFSET` для заданої сторінки?
7. Для чого в `JOIN` потрібен `ON`? Що станеться, якщо його пропустити?
8. Чим `INNER JOIN` відрізняється від `LEFT JOIN`? Наведіть приклад з LMS, коли потрібен саме `LEFT JOIN`.
9. Як знайти студентів, які не записані на жодний курс?
10. Чому `RIGHT JOIN` майже не використовують?
11. Чому умову для правої таблиці `LEFT JOIN` треба писати в `ON`, а не у `WHERE`?
12. Чому для підрахунку студентів на курсі після `LEFT JOIN` потрібен `COUNT(e.user_id)`, а не `COUNT(*)`?
13. Як визначити, через які таблиці потрібно з'єднати `submissions` і `courses`?

## Корисні посилання

- SELECT: https://www.postgresql.org/docs/current/sql-select.html
- Запити до кількох таблиць (JOIN): https://www.postgresql.org/docs/current/tutorial-join.html
- Оператори порівняння та `IS NULL`: https://www.postgresql.org/docs/current/functions-comparison.html
- Пошук за шаблоном (`LIKE`): https://www.postgresql.org/docs/current/functions-matching.html
- Агрегатні функції: https://www.postgresql.org/docs/current/functions-aggregate.html

**Підготовлено:** Олександр Панченко  
**QALight Training Center**