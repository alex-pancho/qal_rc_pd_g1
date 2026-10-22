# Заняття 32. DML: INSERT, UPDATE, DELETE, пошук даних та індекси на прикладі LMS

**Тривалість:** 2 години (практика)

**Викладач:** Олександр Панченко / QALight  
**Курс:** Програмування Python · Модуль 5. PostgreSQL

## Цілі заняття

1. Підготувати структуру LMS і за потреби змінити її командою `ALTER TABLE`
2. Наповнювати таблиці даними: `INSERT`, у тому числі кілька рядків, `INSERT ... SELECT`, `RETURNING`, `ON CONFLICT`
3. Читати й фільтрувати дані: `SELECT`, `WHERE`, `LIKE`/`ILIKE`, `DISTINCT`, `ORDER BY`, `LIMIT`/`OFFSET`
4. Безпечно змінювати та видаляти дані: `UPDATE`, `DELETE`, `TRUNCATE`
5. Розуміти транзакції та автоінкремент (`IDENTITY`, `SEQUENCE`)
6. Створювати індекси й перевіряти їх через `EXPLAIN ANALYZE`
7. Виконувати ті самі операції з Python (`psycopg`) і застосувати все у своєму проєкті

## Як побудовано заняття

На попередньому занятті ми проєктували БД для навчальної платформи (LMS) і створили шість таблиць. Сьогодні ми працюємо з цією самою базою. Усі приклади йдуть послідовно і спираються на дані, які ви самі додасте на початку, тому виконуйте команди у `psql` або в DBeaver у тому порядку, у якому вони подані.

Шлях заняття:

1. Підготовка бази й початкова зміна структури
2. Наповнення даними (`INSERT`)
3. Читання даних (`SELECT`)
4. Зміна даних (`UPDATE`)
5. Видалення даних (`DELETE`, `TRUNCATE`)
6. Транзакції та автоінкремент
7. Індекси та продуктивність
8. Те саме з Python
9. Практичні завдання

---

## Частина 0. Підготовка: структура LMS

Нагадаємо схему. Є шість таблиць, і залежності між ними визначають порядок створення:

| Таблиця | Призначення | Залежить від |
| ------- | ----------- | ------------ |
| `users` | студенти та викладачі | немає |
| `courses` | курси | `users` |
| `lessons` | уроки курсу | `courses` |
| `enrollments` | записи студентів на курси (M:N) | `users`, `courses` |
| `assignments` | завдання до уроків | `lessons` |
| `submissions` | здачі завдань студентами | `assignments`, `users` |

Якщо у вас є `schema.sql` з минулого заняття, просто виконайте його. Якщо ні, ось повний скрипт. На початку він видаляє старі таблиці у зворотному порядку, тому його можна запускати повторно.

```sql
DROP TABLE IF EXISTS lms_submissions;
DROP TABLE IF EXISTS lms_assignments;
DROP TABLE IF EXISTS lms_enrollments;
DROP TABLE IF EXISTS lms_lessons;
DROP TABLE IF EXISTS lms_courses;
DROP TABLE IF EXISTS lms_users;

CREATE TABLE IF NOT EXISTS users (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    role       TEXT NOT NULL CHECK (role IN ('student', 'teacher')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title        TEXT NOT NULL,
    description  TEXT,
    teacher_id   INTEGER NOT NULL,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS lessons (
    id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title     TEXT NOT NULL,
    position  INTEGER NOT NULL CHECK (position > 0),
    content   TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE (course_id, position)
);

CREATE TABLE IF NOT EXISTS enrollments (
    user_id     INTEGER NOT NULL,
    course_id   INTEGER NOT NULL,
    enrolled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'completed', 'dropped')),
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id)   REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE IF NOT EXISTS assignments (
    id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lesson_id INTEGER NOT NULL,
    title     TEXT NOT NULL,
    max_score INTEGER NOT NULL DEFAULT 100 CHECK (max_score > 0),
    due_date  TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

CREATE TABLE IF NOT EXISTS submissions (
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

Перевірте результат у `psql`: команда `\dt` має показати шість таблиць.

### 0.1. ALTER TABLE: замовник змінив вимоги

Через тиждень після старту проєкту замовник просить дві речі: зберігати **телефон** користувача та **ціну** курсу. Створювати таблиці заново не потрібно, і дані ми не втратимо. Для цього є `ALTER TABLE`:

```sql
-- Телефон: необов'язкове поле
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Ціна курсу: обов'язкове поле, не може бути від'ємною
ALTER TABLE courses
ADD COLUMN price NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (price >= 0);
```

Зверніть увагу на три моменти:

- Для грошей використовуємо `NUMERIC(10, 2)` (синонім `DECIMAL`): 10 цифр загалом, 2 з них після коми. `FLOAT` для грошей не використовують, бо він округлює неточно.
- Якщо в таблиці вже є рядки, нову колонку з `NOT NULL` можна додати лише разом із `DEFAULT`. Інакше PostgreSQL не знатиме, що записати в існуючі рядки.
- Після `ALTER TABLE` змінюється набір колонок. Це важливо для `INSERT` (див. частину 1).

Інші типові зміни структури:

| Задача | Команда |
| ------ | ------- |
| Видалити колонку | `ALTER TABLE users DROP COLUMN phone;` |
| Змінити тип | `ALTER TABLE users ALTER COLUMN phone TYPE VARCHAR(30);` |
| Зробити поле обов'язковим | `ALTER TABLE users ALTER COLUMN phone SET NOT NULL;` |
| Зняти обов'язковість | `ALTER TABLE users ALTER COLUMN phone DROP NOT NULL;` |
| Змінити значення за замовчуванням | `ALTER TABLE courses ALTER COLUMN price SET DEFAULT 100;` |
| Додати обмеження | `ALTER TABLE courses ADD CONSTRAINT unique_course_title UNIQUE (title);` |
| Видалити обмеження | `ALTER TABLE courses DROP CONSTRAINT unique_course_title;` |

Щоб видалити обмеження, потрібно знати його ім'я. Якщо ви не називали його самі, PostgreSQL дає імена за шаблоном: `users_pkey`, `users_email_key`, `courses_teacher_id_fkey`. Подивитися всі обмеження таблиці можна командою `\d users`. Через це добре давати обмеженням власні імена (`CONSTRAINT unique_course_title ...`).

---

## Частина 1. INSERT: наповнюємо LMS даними

### 1.1. Базовий синтаксис

```sql
INSERT INTO table_name (column1, column2, column3)
VALUES (value1, value2, value3);
```

Колонки, які ми не вказали, отримують значення за замовчуванням (`DEFAULT`) або `NULL`. Так для `users.id` і `created_at` нам нічого передавати не треба.

### 1.2. Додаємо першого викладача

```sql
INSERT INTO users (first_name, last_name, email, role)
VALUES ('Петро', 'Іваненко', 'petro@lms.ua', 'teacher')
RETURNING id, email;
```

`RETURNING` повертає значення з щойно доданого рядка, зокрема згенерований `id`. Це зручно: окремий `SELECT` не потрібен.

Результат:

```text
 id |    email
----+--------------
  1 | petro@lms.ua
```

### 1.3. Додаємо кілька рядків одним запитом

Один запит із кількома наборами значень працює швидше й атомарніше, ніж кілька окремих `INSERT`: або додадуться всі рядки, або жоден.

```sql
INSERT INTO users (first_name, last_name, email, role)
VALUES
    ('Олена', 'Шевченко', 'olena@lms.ua',      'teacher'),
    ('Ірина', 'Коваль',   'iryna@mail.com',    'student'),
    ('Андрій', 'Мельник', 'andrii@gmail.com',  'student'),
    ('Марія', 'Бондар',   'maria@gmail.com',   'student'),
    ('Тест',  'Один',     'test1@mail.com',    'student'),
    ('Тест',  'Два',      'test2@mail.com',    'student');
```

Тепер у нас 7 користувачів: двоє викладачів (id 1 і 2) та п'ятеро студентів (id 3–7). Припускаємо, що таблиці були щойно створені, тому ідентифікатори йдуть від 1. Якщо ви виконували вставки раніше, ваші `id` можуть відрізнятися, і тоді підставляйте свої.

### 1.4. Курси, уроки, записи, завдання та здачі

```sql
INSERT INTO courses (title, description, teacher_id, is_published)
VALUES
    ('Python Basics',        'Основи Python для початківців', 1, TRUE),
    ('SQL Basics',           'Вступ до баз даних',            1, TRUE),
    ('Python Advanced',      'ООП, декоратори, асинхронність', 2, FALSE),
    ('QA Fundamentals',      'Основи тестування ПЗ',          2, TRUE);

INSERT INTO lessons (course_id, title, position)
VALUES
    (1, 'Змінні та типи даних', 1),
    (1, 'Умови та цикли',       2),
    (1, 'Функції',              3),
    (2, 'Вступ до SQL',         1),
    (2, 'SELECT та WHERE',      2);

INSERT INTO enrollments (user_id, course_id)
VALUES (3, 1), (3, 2), (4, 1), (4, 3), (5, 1), (5, 4);

INSERT INTO assignments (lesson_id, title, max_score, due_date)
VALUES
    (1, 'Hello, Python',        100, '2026-10-15 23:59'),
    (3, 'Функція-калькулятор',  100, '2026-10-30 23:59'),
    (5, 'Перші запити',          50, '2026-11-05 23:59');

INSERT INTO submissions (assignment_id, student_id, answer_text, score)
VALUES
    (1, 3, 'print("Hello")', 90),
    (1, 4, 'print(1 + 1)',   70),
    (2, 3, 'def calc(): ...', NULL),
    (3, 3, 'SELECT * FROM users;', 45);
```

Зверніть увагу на порядок: спершу `users`, потім `courses`, `lessons` і так далі. Це той самий порядок, у якому ми створювали таблиці. Зовнішній ключ може посилатися лише на рядок, який уже існує.

Також зверніть увагу: у третьої здачі `score` дорівнює `NULL`. Це означає «ще не оцінено», а не «нуль балів». Різницю між `NULL` і `0` ми використаємо нижче.

Курс 3 (`Python Advanced`) не опублікований. Перевірте дані: `SELECT * FROM courses;`.

### 1.5. Чому не варто вставляти без переліку колонок

Синтаксис без списку колонок працює, але це погана практика:

```sql
-- ❌ Не робіть так
INSERT INTO users
VALUES (8, 'Богдан', 'Лис', 'bohdan@mail.com', 'student', NOW(), NULL);
```

Тут одразу дві проблеми:

- Потрібно знати порядок колонок і передати **всі** значення, включно з `id`. Для `GENERATED ALWAYS AS IDENTITY` PostgreSQL відмовить: `cannot insert a non-DEFAULT value into column "id"`.
- Після `ALTER TABLE ... ADD COLUMN` (як із `phone`) кількість колонок змінилася, і такий запит перестає працювати.

Завжди вказуйте колонки явно.

### 1.6. INSERT ... SELECT: додаємо рядки на основі даних із таблиці

Замість `VALUES` можна передати результат `SELECT`. Задача: записати всіх студентів на вступний курс `QA Fundamentals` (id 4).

```sql
INSERT INTO enrollments (user_id, course_id)
SELECT id, 4
FROM users
WHERE role = 'student';
```

Отримаємо помилку: студентка Марія (id 5) вже записана на цей курс, а пара `(user_id, course_id)` є первинним ключем:

```text
ERROR:  duplicate key value violates unique constraint "enrollments_pkey"
```

Це нормальна робота обмеження. Якщо дублікати в такій задачі очікувані, пропустіть їх:

```sql
INSERT INTO enrollments (user_id, course_id)
SELECT id, 4
FROM users
WHERE role = 'student'
ON CONFLICT (user_id, course_id) DO NOTHING;
```

`ON CONFLICT` обробляє порушення унікальності. Замість `DO NOTHING` можна оновити існуючий рядок: `DO UPDATE SET status = 'active'`. Ця конструкція називається *upsert* («update or insert»), і вона зустрічається в реальних проєктах постійно.

---

## Частина 2. SELECT: читаємо й фільтруємо дані

Щоб перевіряти результати змін, нам потрібно вміти читати дані. Тут ми розглянемо основи, а детальніше про вибірки з кількох таблиць поговоримо пізніше.

### 2.1. Базовий SELECT

```sql
-- Усі колонки
SELECT * FROM courses;

-- Конкретні колонки
SELECT id, title, is_published FROM courses;

-- З псевдонімами
SELECT
    id    AS course_id,
    title AS course_title
FROM courses;
```

У реальному коді краще уникати `SELECT *`: ви витягуєте зайві колонки, а після змін у структурі код може зламатися.

### 2.2. WHERE: умови фільтрування

Оператори порівняння:

```sql
SELECT * FROM courses WHERE id = 1;           -- рівність
SELECT * FROM courses WHERE id <> 1;          -- не дорівнює (також !=)
SELECT * FROM assignments WHERE max_score > 50;
SELECT * FROM assignments WHERE max_score >= 50;
SELECT * FROM submissions WHERE score < 80;
SELECT * FROM submissions WHERE score <= 70;
```

Логічні оператори `AND`, `OR`, `NOT`:

```sql
-- Опубліковані курси викладача 1
SELECT * FROM courses WHERE is_published = TRUE AND teacher_id = 1;

-- Неопубліковані курси або безкоштовні
SELECT * FROM courses WHERE NOT is_published OR price = 0;
```

Якщо поєднуєте `AND` та `OR`, завжди ставте дужки: `AND` має вищий пріоритет, і без дужок результат може вас здивувати.

```sql
SELECT * FROM courses
WHERE (teacher_id = 1 OR teacher_id = 2) AND is_published = TRUE;
```

`IN` перевіряє належність до списку, `BETWEEN` задає діапазон (обидві межі включно):

```sql
SELECT * FROM users WHERE id IN (1, 2, 3);
SELECT * FROM users WHERE role IN ('teacher');

SELECT * FROM submissions WHERE score BETWEEN 50 AND 100;
SELECT * FROM assignments
WHERE due_date BETWEEN '2026-10-01' AND '2026-10-31';
```

### 2.3. NULL: порожнє значення

`NULL` означає «значення невідоме». З ним не можна порівнювати через `=`: умова `score = NULL` ніколи не спрацює. Використовуйте `IS NULL` і `IS NOT NULL`:

```sql
-- Здачі, які ще не оцінені
SELECT * FROM submissions WHERE score IS NULL;

-- Оцінені здачі
SELECT * FROM submissions WHERE score IS NOT NULL;

-- Користувачі без телефону (ми щойно додали колонку, тож тут усі)
SELECT id, email FROM users WHERE phone IS NULL;
```

Це типова задача для LMS: викладач хоче побачити список здач, які чекають на перевірку.

### 2.4. LIKE: гнучкий пошук за шаблоном

`LIKE` перевіряє, чи відповідає текст шаблону. У шаблоні є два спеціальні символи:

| Символ | Значення | Приклад шаблону |
| ------ | -------- | --------------- |
| `%` | будь-яка кількість будь-яких символів (також нуль) | `'%SQL%'` |
| `_` | рівно один будь-який символ | `'test_@mail.com'` |

Приклади на даних LMS:

```sql
-- Назва починається з 'Python'
SELECT title FROM courses WHERE title LIKE 'Python%';
-- Python Basics, Python Advanced

-- Назва закінчується на 'Basics'
SELECT title FROM courses WHERE title LIKE '%Basics';
-- Python Basics, SQL Basics

-- Назва містить 'SQL' де завгодно
SELECT title FROM lessons WHERE title LIKE '%SQL%';
-- Вступ до SQL

-- Рівно один символ замість цифри
SELECT email FROM users WHERE email LIKE 'test_@mail.com';
-- test1@mail.com, test2@mail.com (а test10@mail.com не підійде)

-- Усі адреси на gmail
SELECT email FROM users WHERE email LIKE '%@gmail.com';
```

Зверніть увагу: урок `SELECT та WHERE` у третьому прикладі не знайдеться, бо слова `SQL` у його назві немає.

`LIKE` чутливий до регістру. Для пошуку без урахування регістру в PostgreSQL є `ILIKE`:

```sql
SELECT title FROM courses WHERE title ILIKE '%python%';
-- Python Basics, Python Advanced
```

Заперечення: `NOT LIKE` / `NOT ILIKE`:

```sql
-- Усі, хто не використовує gmail
SELECT email FROM users WHERE email NOT LIKE '%@gmail.com';
```

Якщо потрібно знайти сам символ `%` або `_`, його екранують:

```sql
-- Шукаємо знак % у тексті відповіді
SELECT * FROM submissions WHERE answer_text LIKE '%\%%' ESCAPE '\';
```

### 2.5. DISTINCT: унікальні значення

```sql
-- Які домени пошти є у користувачів
SELECT DISTINCT split_part(email, '@', 2) AS domain
FROM users;
-- lms.ua, mail.com, gmail.com

-- Скільки різних доменів
SELECT COUNT(DISTINCT split_part(email, '@', 2)) AS domains_count
FROM users;
```

`split_part(text, роздільник, номер)` розбиває рядок за роздільником і повертає потрібну частину.

### 2.6. ORDER BY: сортування

```sql
-- За зростанням (за замовчуванням)
SELECT title, created_at FROM courses ORDER BY created_at ASC;

-- За спаданням
SELECT * FROM submissions ORDER BY score DESC;

-- За кількома колонками: спершу за курсом, потім за порядком уроку
SELECT course_id, position, title
FROM lessons
ORDER BY course_id, position;

-- Без урахування регістру
SELECT last_name FROM users ORDER BY LOWER(last_name);
```

Важлива особливість PostgreSQL: при сортуванні за спаданням `NULL` ідуть **першими**. Для журналу оцінок це невдало, тому додаємо `NULLS LAST`:

```sql
SELECT id, student_id, score
FROM submissions
ORDER BY score DESC NULLS LAST;
```

### 2.7. LIMIT та OFFSET: пагінація

```sql
-- Перші 2 курси
SELECT id, title FROM courses ORDER BY id LIMIT 2;

-- Пропустити 2 рядки, взяти наступні 2 (друга сторінка)
SELECT id, title FROM courses ORDER BY id LIMIT 2 OFFSET 2;
```

Формула для сторінки `page` з `per_page` записами:

```text
OFFSET = (page - 1) * per_page
```

Завжди додавайте `ORDER BY` разом із `LIMIT`. Без нього порядок рядків не гарантований, і користувач може побачити однакові записи на різних сторінках. Загальну кількість записів для розрахунку кількості сторінок отримують окремим запитом `SELECT COUNT(*) ...`.

---

## Частина 3. UPDATE: змінюємо дані

### 3.1. Базовий синтаксис

```sql
UPDATE table_name
SET column1 = value1, column2 = value2
WHERE condition;
```

### 3.2. Виставляємо ціни курсам

Спершу змінимо один рядок за первинним ключем. Це найбезпечніший вигляд `UPDATE`:

```sql
UPDATE courses
SET price = 1200
WHERE id = 1
RETURNING id, title, price;
```

Тепер кілька рядків за умовою:

```sql
-- Усі курси викладача 2 коштують 800
UPDATE courses
SET price = 800
WHERE teacher_id = 2;

-- Курс SQL Basics: ціна 900
UPDATE courses SET price = 900 WHERE id = 2;
```

Для `UPDATE` без `RETURNING` PostgreSQL повертає лише кількість змінених рядків, наприклад `UPDATE 2`. Корисно дивитися на цю цифру: якщо ви очікували один рядок, а змінилося п'ятдесят, це сигнал зупинитися.

### 3.3. Оцінюємо роботу студента

Викладач перевірив здачу. Оцінка проставляється в той самий рядок `submissions`:

```sql
UPDATE submissions
SET score = 80
WHERE assignment_id = 2 AND student_id = 3 AND score IS NULL
RETURNING id, student_id, score;
```

Умова `score IS NULL` захищає від випадкового перезапису: якщо викладач вже виставив оцінку, запит нічого не змінить.

### 3.4. Оновлення з виразом

У `SET` можна використовувати вирази, зокрема й значення тієї ж колонки:

```sql
-- Знижка 10% на всі опубліковані курси
UPDATE courses
SET price = ROUND(price * 0.9, 2)
WHERE is_published = TRUE
RETURNING id, title, price;

-- Продовжити дедлайни завдань першого курсу на 3 дні
UPDATE assignments
SET due_date = due_date + INTERVAL '3 days'
WHERE lesson_id IN (
    SELECT id FROM lessons WHERE course_id = 1
);
```

Другий запит використовує підзапит: ми шукаємо завдання, чий урок належить курсу 1.

### 3.5. UPDATE ... FROM: зміна на основі іншої таблиці

Іноді умова залежить від даних в іншій таблиці. Задача: скасувати всі активні записи на неопублікованих курсах.

```sql
UPDATE enrollments
SET status = 'dropped'
FROM courses
WHERE enrollments.course_id = courses.id
  AND courses.is_published = FALSE
  AND enrollments.status = 'active';
```

Після `FROM` підключається друга таблиця, а в `WHERE` ми з'єднуємо рядки двох таблиць за ключем.

### 3.6. ⚠️ Небезпека: UPDATE без WHERE

```sql
-- ❌ Опублікує ВСІ курси, навіть чернетки!
UPDATE courses SET is_published = TRUE;
```

Це один із найпоширеніших інцидентів у роботі з БД. Щоб його уникнути, дотримуйтесь трьох правил.

1. **Спочатку SELECT.** Перш ніж змінювати, виконайте `SELECT` з тією самою умовою й переконайтесь, що вибираються саме ті рядки.
2. **Спочатку WHERE.** Пишіть запит, починаючи з `WHERE`, а `UPDATE` додавайте останнім. Тоді випадковий запуск недописаного запиту нічого не зламає.
3. **Користуйтесь транзакцією.** Вона дозволяє перевірити результат і відкотити зміни (див. частину 5).

---

## Частина 4. DELETE та TRUNCATE: видаляємо дані

### 4.1. Базовий синтаксис

```sql
DELETE FROM table_name
WHERE condition;
```

### 4.2. Приклади

Видаляємо тестових студентів за шаблоном пошти й одразу бачимо, кого саме видалили:

```sql
DELETE FROM users
WHERE email LIKE 'test_@mail.com'
RETURNING id, email;
```

Видаляємо записи, які студенти скасували, на неопублікованих курсах:

```sql
DELETE FROM enrollments
WHERE status = 'dropped'
  AND course_id IN (
      SELECT id FROM courses WHERE is_published = FALSE
  );
```

### 4.3. Що робити, якщо видалення блокується зовнішнім ключем

Спробуємо видалити курс, у якого є уроки:

```sql
DELETE FROM courses WHERE id = 1;
```

```text
ERROR:  update or delete on table "courses" violates foreign key
constraint "lessons_course_id_fkey" on table "lessons"
```

Це зовнішній ключ виконує свою роботу: не дозволяє залишити уроки без курсу. Є три шляхи.

**Шлях 1. Видалити залежні дані вручну**, від найзалежніших до головних. Порядок зворотний до створення таблиць:

```sql
DELETE FROM submissions WHERE assignment_id IN (
    SELECT a.id FROM assignments a WHERE a.lesson_id IN (
        SELECT l.id FROM lessons l WHERE l.course_id = 1));
DELETE FROM assignments WHERE lesson_id IN (
    SELECT id FROM lessons WHERE course_id = 1);
DELETE FROM enrollments WHERE course_id = 1;
DELETE FROM lessons WHERE course_id = 1;
DELETE FROM courses WHERE id = 1;
```

**Шлях 2. `ON DELETE CASCADE`.** Зовнішній ключ сам видаляє залежні рядки. Для цього обмеження потрібно перестворити:

```sql
ALTER TABLE lessons DROP CONSTRAINT lessons_course_id_fkey;

ALTER TABLE lessons
ADD CONSTRAINT lessons_course_id_fkey
FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE;
```

Після цього видалення курсу автоматично видалить його уроки. Але каскад працює лише там, де він налаштований: якщо завдання посилаються на уроки без `CASCADE`, видалення знову зупиниться. Каскад зручний і небезпечний водночас: один `DELETE` може стерти багато даних, тому використовуйте його свідомо.

**Шлях 3. М'яке видалення (soft delete).** У LMS видаляти курс із усією історією оцінок студентів рідко потрібно. Натомість рядок позначають неактивним:

```sql
UPDATE courses SET is_published = FALSE WHERE id = 1;
```

Дані зберігаються, і курс можна повернути. У реальних системах так роблять із користувачами, замовленнями, платежами: все, що може знадобитися для аудиту.

### 4.4. ⚠️ Небезпека: DELETE без WHERE

```sql
-- ❌ Видалить ВСІХ користувачів (якщо не завадять зовнішні ключі)
DELETE FROM users;
```

Правила ті самі, що й для `UPDATE`: спершу `SELECT` з такою ж умовою, а для важливих даних транзакція.

### 4.5. TRUNCATE: швидко очистити таблицю

`TRUNCATE` видаляє **всі** рядки таблиці, але саму таблицю залишає:

```sql
-- Очистити здачі (на них ніхто не посилається)
TRUNCATE TABLE submissions;

-- Очистити і скинути лічильник id до 1
TRUNCATE TABLE submissions RESTART IDENTITY;
```

Порівняння з `DELETE`:

| Параметр | `DELETE` | `TRUNCATE` |
| -------- | -------- | ---------- |
| Умова `WHERE` | є | немає, видаляє все |
| Швидкість на великих таблицях | повільніше, видаляє рядок за рядком | значно швидше |
| Лічильник `id` | не скидається | скидається з `RESTART IDENTITY` |
| Якщо на таблицю посилаються зовнішні ключі | помилка, поки є залежні рядки | помилка, навіть якщо таблиця-посилання порожня, без `CASCADE` |
| Відкат у транзакції | можливий | у PostgreSQL також можливий |

`TRUNCATE users CASCADE` очистить `users` і **всі таблиці, що на неї посилаються**: `courses`, `enrollments`, `submissions` і далі по ланцюжку. Використовуйте такі команди лише на тестовій БД.

### 4.6. DROP TABLE: коротке нагадування

`DROP TABLE` видаляє саму таблицю разом з даними та структурою. `DROP TABLE IF EXISTS` не видає помилку, якщо таблиці немає. Таблиці видаляємо у порядку, зворотному до створення: так працює скрипт із початку заняття.

---

## Частина 5. Транзакції

### 5.1. Навіщо вони потрібні

Студентка просить перевести її з курсу `Python Basics` на `SQL Basics`. Це **дві** операції:

1. позначити старий запис як `dropped`;
2. створити новий запис на другий курс.

Якщо між ними станеться збій, студентка залишиться без курсу або з двома записами. Транзакція об'єднує кілька команд в одну неподільну операцію: або виконуються всі, або жодна.

```sql
BEGIN;

UPDATE enrollments
SET status = 'dropped'
WHERE user_id = 4 AND course_id = 1;

INSERT INTO enrollments (user_id, course_id)
VALUES (4, 2);

COMMIT;   -- зберегти зміни
-- ROLLBACK;  -- або скасувати все, що було після BEGIN
```

### 5.2. Транзакція як страховка

Транзакція також дозволяє безпечно перевіряти небезпечні команди:

```sql
BEGIN;

UPDATE courses SET price = 0;          -- ми щойно змінили всі курси
SELECT id, title, price FROM courses;  -- дивимося на результат
-- Результат не влаштовує, тож відкочуємо:
ROLLBACK;
```

Після `ROLLBACK` ціни повертаються до попередніх значень. Це хороша звичка для будь-яких масових змін.

---

## Частина 6. Автоінкремент та SEQUENCE

### 6.1. Як генеруються id

У нашій схемі `id` оголошено як `INTEGER GENERATED ALWAYS AS IDENTITY`. Під капотом PostgreSQL створює **послідовність** (`SEQUENCE`), яка видає числа 1, 2, 3 ... Кожен `INSERT` бере наступне число.

У старих проєктах і навчальних матеріалах ви часто зустрінете `SERIAL`:

```sql
CREATE TABLE IF NOT EXISTS tags (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
```

Принцип той самий. `IDENTITY` є сучасним стандартним синтаксисом SQL, тому в нових проєктах краще використовувати його.

Типи за розміром:

| Тип | Базовий тип | Максимум |
| --- | ----------- | -------- |
| `SMALLSERIAL` | `SMALLINT` | 32 767 |
| `SERIAL` | `INTEGER` | 2 147 483 647 |
| `BIGSERIAL` | `BIGINT` | 9 223 372 036 854 775 807 |

Для таблиць, які можуть вирости до мільярдів рядків (наприклад, журнал дій користувачів), використовуйте `BIGINT GENERATED ALWAYS AS IDENTITY`.

### 6.2. Робота з послідовністю напряму

Ім'я послідовності не обов'язково запам'ятовувати: його повертає функція `pg_get_serial_sequence`.

```sql
-- Наступне значення (і збільшити лічильник)
SELECT nextval(pg_get_serial_sequence('users', 'id'));

-- Поточне значення в цій сесії (після nextval)
SELECT currval(pg_get_serial_sequence('users', 'id'));

-- Встановити значення вручну
SELECT setval(pg_get_serial_sequence('users', 'id'), 1000);
```

Після `setval(..., 1000)` наступний користувач отримає `id = 1001`.

### 6.3. Скидання лічильника

```sql
-- Разом з очищенням таблиці
TRUNCATE TABLE submissions RESTART IDENTITY;

-- Окремо, для IDENTITY-колонки
ALTER TABLE users ALTER COLUMN id RESTART WITH 1000;
```

На production-базах лічильник не скидають: нові `id` могли б збігтися зі старими, які вже збережені в інших системах.

### 6.4. Дірки в нумерації: це нормально

Спробуйте двічі додати користувача з однаковим email: перший `INSERT` пройде, другий завершиться помилкою `UNIQUE`. Подивіться на `id` наступного успішно доданого користувача: він пропустить число. Послідовність видає номер ще до перевірки обмежень, і назад його не повертає. Те саме відбувається при `ROLLBACK`.

Висновок: `id` гарантує лише унікальність, а не відсутність пропусків. Ніколи не будуйте логіку на тому, що номери йдуть підряд.

---

## Частина 7. Індекси

### 7.1. Що таке індекс

**Індекс** є додатковою структурою даних, яка прискорює пошук по таблиці. Аналогія: предметний покажчик у книзі. Без нього, щоб знайти слово, треба гортати всі сторінки. З ним ви одразу відкриваєте потрібну.

Без індексу PostgreSQL виконує **Seq Scan** (послідовне сканування): перевіряє кожен рядок таблиці. З індексом використовується **Index Scan**, який швидко переходить до потрібних рядків.

Як це впливає на роботу:

| Операція | З індексом | Без індексу |
| -------- | ---------- | ----------- |
| Пошук (`SELECT ... WHERE`) | швидко | повільно на великих таблицях |
| `INSERT` | трохи повільніше, бо треба оновити індекс | швидше |
| `UPDATE` індексованих колонок | трохи повільніше | швидше |
| Місце на диску | займає додатково | менше |

Індекс прискорює читання, але сповільнює запис і займає місце. Тому індекси створюють не на всі колонки, а на ті, за якими справді часто шукають.

### 7.2. Що вже індексоване автоматично

Для `PRIMARY KEY` та `UNIQUE` PostgreSQL створює індекс сам. Перевіримо:

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'users';
```

Результат містить `users_pkey` (індекс по `id`) та `users_email_key` (індекс по `email`).

А ось для **зовнішніх ключів** PostgreSQL індекс **не створює**. Подивіться на нашу схему:

| Колонка | Чи є індекс |
| ------- | ----------- |
| `courses.teacher_id` | ні |
| `lessons.course_id` | так, у складі `UNIQUE (course_id, position)` |
| `enrollments.user_id` | так, перша колонка складеного ключа |
| `enrollments.course_id` | ні |
| `assignments.lesson_id` | ні |
| `submissions.assignment_id` | так, перша колонка в `UNIQUE (assignment_id, student_id)` |
| `submissions.student_id` | ні |

Колонки без індексу, за якими ми шукаємо чи з'єднуємо таблиці («усі курси викладача», «усі здачі студента»), потрібно проіндексувати вручну.

### 7.3. Створення індексів

Простий індекс по одній колонці:

```sql
CREATE INDEX idx_courses_teacher_id ON courses (teacher_id);
CREATE INDEX idx_submissions_student_id ON submissions (student_id);
CREATE INDEX idx_assignments_lesson_id ON assignments (lesson_id);
CREATE INDEX idx_enrollments_course_id ON enrollments (course_id);
```

Складений індекс по кількох колонках. Порядок колонок має значення: індекс працює для запитів, що використовують **першу** колонку (або першу й другу разом):

```sql
-- Для запитів: "оцінені здачі студента, найновіші першими"
CREATE INDEX idx_submissions_student_date
ON submissions (student_id, submitted_at DESC);
```

Частковий індекс охоплює лише частину рядків і економить місце:

```sql
-- Нас цікавлять лише опубліковані курси
CREATE INDEX idx_courses_published_created
ON courses (created_at DESC)
WHERE is_published = TRUE;
```

Індекс на виразі потрібен, коли в запиті шукають за результатом функції:

```sql
-- Для пошуку email без урахування регістру
CREATE INDEX idx_users_email_lower ON users (LOWER(email));

-- Тепер цей запит використовує індекс:
SELECT * FROM users WHERE LOWER(email) = 'petro@lms.ua';
```

Унікальний індекс гарантує унікальність і працює як `UNIQUE`-обмеження:

```sql
CREATE UNIQUE INDEX idx_courses_title_unique ON courses (title);
```

### 7.4. Типи індексів

| Тип | Для чого | Приклад |
| --- | -------- | ------- |
| **B-tree** | за замовчуванням; `=`, `<`, `>`, `BETWEEN`, `ORDER BY`, префікс `LIKE 'abc%'` | `CREATE INDEX ... ON users (email);` |
| **Hash** | лише точне порівняння `=` | `CREATE INDEX ... ON users USING HASH (email);` |
| **GIN** | масиви, `JSONB`, повнотекстовий пошук | теги курсу, `JSONB`-метадані |
| **GiST** | геодані, діапазони, текстовий пошук | координати, періоди дат |

У 95% випадків вам вистачить B-tree. Решту типів потрібно знати як факт: вони існують для спеціальних даних.

### 7.5. Коли індекс допомагає, а коли ні

Створюйте індекс, якщо колонка:

- часто використовується в `WHERE` або `JOIN`;
- часто використовується в `ORDER BY`;
- має багато різних значень (висока селективність: `email`, `student_id`).

Не створюйте індекс, якщо:

- таблиця мала (кілька десятків рядків): PostgreSQL сам вибере Seq Scan, і так буде швидше;
- колонка має мало різних значень (`is_published`, `role`): індекс майже нічого не відсіює;
- у таблицю дуже часто пишуть, а читають рідко.

Також варто знати: B-tree допомагає для `LIKE 'Python%'` (пошук за префіксом), але **не допомагає** для `LIKE '%python'` чи `LIKE '%python%'`: початок рядка невідомий. Для префіксного пошуку в базах з локаллю, відмінною від «C», індекс потрібно створювати з класом операторів: `CREATE INDEX ... ON courses (title text_pattern_ops);`. Для пошуку в середині тексту використовують спеціальні розширення (наприклад, `pg_trgm`).

### 7.6. EXPLAIN ANALYZE: перевіряємо на практиці

На п'яти рядках різниці не видно, тому згенеруємо тестові дані. Це лише для експерименту, потім ми їх приберемо:

```sql
INSERT INTO users (first_name, last_name, email, role)
SELECT 'User' || g, 'Load', 'user' || g || '@load.test', 'student'
FROM generate_series(1, 100000) AS g;
```

Шукаємо за колонкою `first_name`, на якій індексу ще немає:

```sql
EXPLAIN ANALYZE
SELECT * FROM users WHERE first_name = 'User77777';
```

Приблизний результат:

```text
Seq Scan on users  (cost=0.00..2137.00 rows=1 width=72)
  Filter: (first_name = 'User77777')
  Rows Removed by Filter: 100004
Execution Time: 18.4 ms
```

`Seq Scan` означає, що база перевірила всі ~100 000 рядків. Створимо індекс і повторимо запит:

```sql
CREATE INDEX idx_users_first_name ON users (first_name);

EXPLAIN ANALYZE
SELECT * FROM users WHERE first_name = 'User77777';
```

```text
Index Scan using idx_users_first_name on users  (cost=0.42..8.44 rows=1 width=72)
  Index Cond: (first_name = 'User77777')
Execution Time: 0.05 ms
```

Тепер це `Index Scan`, і час впав на кілька порядків. Конкретні цифри на вашому комп'ютері будуть іншими, але різницю ви побачите чітко.

Приберемо експериментальні дані й індекс:

```sql
DELETE FROM users WHERE email LIKE '%@load.test';
DROP INDEX IF EXISTS idx_users_first_name;
```

Перевіряти запити варто так: `EXPLAIN` показує план, `EXPLAIN ANALYZE` реально виконує запит і показує фактичний час. Увага: `EXPLAIN ANALYZE` справді виконує команду, тож для `UPDATE` та `DELETE` загортайте його в транзакцію з `ROLLBACK`.

### 7.7. Видалення індексів

```sql
DROP INDEX idx_courses_teacher_id;
DROP INDEX IF EXISTS idx_courses_teacher_id;
```

Індекси, які не використовуються, шкодять: сповільнюють запис і займають місце. Знайти список індексів таблиці можна через `pg_indexes` (див. 7.2) або `\d table_name`.

---

## Частина 8. Те саме з Python (psycopg)

Тепер оформимо операції LMS як функції. Бібліотека: `psycopg` (версія 3).

```python
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/lms"
```

### 8.1. Правило №1: ніколи не підставляйте значення в SQL рядком

Значення передаємо окремим аргументом через `%s`. Бібліотека сама екранує їх і захищає від SQL-ін'єкцій.

```python
# ❌ Небезпечно: SQL-ін'єкція
cur.execute(f"SELECT * FROM users WHERE email = '{email}'")

# ✅ Правильно
cur.execute("SELECT * FROM users WHERE email = %s", (email,))
```

Блок `with psycopg.connect(DSN) as conn` автоматично виконує `COMMIT` при нормальному виході та `ROLLBACK`, якщо всередині виникла помилка.

### 8.2. CRUD для курсів

```python
def add_course(title: str, teacher_id: int, price: float = 0):
    """INSERT: створити курс і повернути його id."""
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO courses (title, teacher_id, price)
                   VALUES (%s, %s, %s)
                   RETURNING id, title, price;""",
                (title, teacher_id, price),
            )
            return cur.fetchone()


def get_course(course_id: int):
    """SELECT: отримати курс за id."""
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, price, is_published FROM courses WHERE id = %s;",
                (course_id,),
            )
            return cur.fetchone()


def update_course_price(course_id: int, new_price: float):
    """UPDATE: змінити ціну курсу."""
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE courses SET price = %s
                   WHERE id = %s
                   RETURNING id, title, price;""",
                (new_price, course_id),
            )
            return cur.fetchone()   # None, якщо такого курсу немає


def delete_enrollment(user_id: int, course_id: int):
    """DELETE: прибрати запис студента на курс."""
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """DELETE FROM enrollments
                   WHERE user_id = %s AND course_id = %s
                   RETURNING user_id, course_id;""",
                (user_id, course_id),
            )
            return cur.fetchone()
```

### 8.3. Пошук курсів із пагінацією

```python
def search_courses(term: str, page: int = 1, per_page: int = 10):
    """Пошук за назвою (без урахування регістру) з пагінацією."""
    pattern = f"%{term}%"
    offset = (page - 1) * per_page

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM courses WHERE title ILIKE %s;",
                (pattern,),
            )
            total = cur.fetchone()[0]

            cur.execute(
                """SELECT id, title, price
                   FROM courses
                   WHERE title ILIKE %s
                   ORDER BY created_at DESC, id
                   LIMIT %s OFFSET %s;""",
                (pattern, per_page, offset),
            )
            courses = cur.fetchall()

    return {
        "courses": courses,
        "total": total,
        "page": page,
        "total_pages": (total + per_page - 1) // per_page,
    }


result = search_courses("python", page=1, per_page=10)
print(f"Знайдено курсів: {result['total']}")
for course_id, title, price in result["courses"]:
    print(f"  {course_id}. {title}: {price} грн")
```

Зверніть увагу: символи `%` у шаблон ми додаємо самі в Python, а в SQL передаємо готовий шаблон як параметр. Якщо користувач сам введе `%` чи `_`, вони теж спрацюють як метасимволи. Для навчального застосунку це нормально, а в production їх екранують.

### 8.4. Транзакція: переведення студента на інший курс

Це те саме, що ми робили у `psql` у частині 5, тільки з перевіркою помилок. Якщо виникне виняток, `with` автоматично відкотить усі зміни.

```python
def move_student(user_id: int, from_course_id: int, to_course_id: int):
    """Перевести студента з одного курсу на інший однією транзакцією."""
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE enrollments SET status = 'dropped'
                   WHERE user_id = %s AND course_id = %s AND status = 'active'
                   RETURNING user_id;""",
                (user_id, from_course_id),
            )
            if cur.fetchone() is None:
                raise ValueError("Студент не записаний на вихідний курс")

            cur.execute(
                """INSERT INTO enrollments (user_id, course_id)
                   VALUES (%s, %s)
                   ON CONFLICT (user_id, course_id)
                   DO UPDATE SET status = 'active',
                                 enrolled_at = CURRENT_TIMESTAMP;""",
                (user_id, to_course_id),
            )


try:
    move_student(user_id=5, from_course_id=1, to_course_id=2)
    print("Студента переведено")
except ValueError as e:
    print(f"Не вдалося: {e}")
```

Ми не викликаємо `commit()` і `rollback()` вручну: `with` робить це за нас. `ON CONFLICT ... DO UPDATE` обробляє ситуацію, коли студент раніше вже був записаний на цей курс і вибув.

### 8.5. Помилка N+1 запити

Задача: вивести кожен курс і кількість його уроків.

```python
# ❌ ПОГАНО: 1 запит на курси + N запитів на уроки
cur.execute("SELECT id, title FROM courses;")
for course_id, title in cur.fetchall():
    cur.execute("SELECT COUNT(*) FROM lessons WHERE course_id = %s;", (course_id,))
    count = cur.fetchone()[0]
    print(f"{title}: {count}")
# Для 100 курсів це 101 запит до БД.
```

Кожен запит до бази має накладні витрати: мережа, розбір запиту. Тому замість циклу пишемо один запит:

```python
# ✅ ДОБРЕ: один запит
cur.execute("""
    SELECT c.title, COUNT(l.id) AS lessons_count
    FROM courses c
    LEFT JOIN lessons l ON l.course_id = c.id
    GROUP BY c.id, c.title
    ORDER BY c.title;
""")
for title, count in cur.fetchall():
    print(f"{title}: {count}")
```

Тут ми скористалися `JOIN`, щоб з'єднати курси з їхніми уроками, і `GROUP BY`, щоб порахувати уроки по кожному курсу. `LEFT JOIN` залишає в результаті й курси без жодного уроку (з нулем). Загальне правило: якщо ви робите запит у циклі, подумайте, чи не можна замінити його одним запитом.

---

## Частина 9. Типові помилки та поради

| Помилка | Наслідок | Як правильно |
| ------- | -------- | ------------ |
| `UPDATE` / `DELETE` без `WHERE` | змінено чи видалено всі рядки | `SELECT` з тією ж умовою, потім транзакція |
| `INSERT` без переліку колонок | ламається після `ALTER TABLE` | завжди вказувати колонки |
| `score = NULL` в умові | нічого не знаходить | `score IS NULL` |
| `LIKE '%text%'` на великій таблиці | повне сканування, індекс не допомагає | `LIKE 'text%'` або спеціальні індекси |
| `LIMIT` без `ORDER BY` | порядок рядків випадковий | завжди сортувати |
| Підстановка значень у SQL через f-string | SQL-ін'єкції | параметри `%s` |
| Запит у циклі (N+1) | багато зайвих звернень до БД | один запит із `JOIN` |
| Немає індексу на зовнішньому ключі | повільні `JOIN` та видалення | індекс на колонках `*_id` |
| Масове видалення без транзакції | неможливо відкотити помилку | `BEGIN` ... `ROLLBACK` / `COMMIT` |
| Індекс на кожній колонці «про всяк випадок» | повільний запис, зайве місце | індекс лише там, де є запити |

Короткий список порад щодо продуктивності:

1. Індексуйте колонки з `WHERE`, `JOIN`, `ORDER BY`.
2. Перевіряйте запити через `EXPLAIN ANALYZE`.
3. Вибирайте лише потрібні колонки замість `SELECT *`.
4. Обмежуйте результат через `LIMIT`.
5. Групуйте пов'язані зміни в одну транзакцію.
6. Бази потребують обслуговування: `VACUUM` та `ANALYZE` оновлюють статистику, яку використовує планувальник. У PostgreSQL це зазвичай виконується автоматично (autovacuum).

---

## Практичні завдання

Виконуйте завдання на базі LMS із цього заняття. Усі команди збережіть у файлі `dml_practice.sql`.

### Завдання 1. Наповнення

1. Додайте ще двох студентів і одного викладача в одному `INSERT`.
2. Створіть для нового викладача курс і три уроки до нього.
3. Запишіть усіх студентів на цей курс одним `INSERT ... SELECT`. Додайте `ON CONFLICT DO NOTHING`.
4. Додайте до курсу завдання і дві здачі.

### Завдання 2. Пошук

Напишіть запити, які знаходять:

1. Усі курси, у назві яких є слово `Python`, незалежно від регістру.
2. Усіх студентів з поштою не на `gmail.com`.
3. Усі здачі, які ще не оцінені.
4. Три найвищі оцінки. `NULL` не повинні потрапити в результат.
5. Другу сторінку списку користувачів, відсортованих за прізвищем, по 3 записи на сторінці.

### Завдання 3. Зміна та видалення

1. Перенесіть дедлайн одного завдання на тиждень уперед.
2. Оцініть усі неоцінені здачі одного завдання. Спочатку перегляньте їх через `SELECT`.
3. Позначте один курс неопублікованим (м'яке видалення).
4. Видаліть тестових студентів. Перевірте, що `RETURNING` показує саме їх.
5. Спробуйте видалити викладача, у якого є курси, і поясніть повідомлення про помилку.
6. Виконайте масову зміну всередині транзакції та відкотіть її через `ROLLBACK`.

### Завдання 4. Індекси

1. Створіть індекси на зовнішніх ключах, де їх бракує.
2. Згенеруйте 100 000 тестових користувачів, як у розділі 7.6.
3. Порівняйте `EXPLAIN ANALYZE` для пошуку за неіндексованою колонкою до і після створення індексу.
4. Перегляньте індекси таблиці `users` через `pg_indexes`.
5. Видаліть тестові дані та експериментальний індекс.

### Завдання 5. Python

Напишіть модуль `lms_db.py` з функціями `add_user`, `get_course`, `enroll_student`, `grade_submission` та `search_courses` (з пагінацією). Усі значення передавайте через параметри `%s`.

### Завдання 6. Власний проєкт

1. Підготуйте тестові дані для всіх таблиць вашого проєкту (мінімум 3 рядки на таблицю).
2. Складіть 5 запитів `SELECT` з `LIKE`, `ORDER BY` і `LIMIT`.
3. Складіть по одному безпечному `UPDATE` і `DELETE` (спочатку `SELECT`, потім транзакція).
4. Додайте індекси на зовнішні ключі та перевірте один із запитів через `EXPLAIN ANALYZE`.

---

## Підсумок

На цьому занятті ми на прикладі LMS:

- Змінили структуру таблиць через `ALTER TABLE`
- Навчилися наповнювати БД: `INSERT` з кількома рядками, `INSERT ... SELECT`, `RETURNING`, `ON CONFLICT`
- Читали й фільтрували дані: `WHERE`, `NULL`, `LIKE`/`ILIKE`, `DISTINCT`, `ORDER BY`, `LIMIT`/`OFFSET`
- Безпечно змінювали та видаляли дані: `UPDATE`, `DELETE`, `TRUNCATE`, `ON DELETE CASCADE`, м'яке видалення
- Об'єднували кілька операцій в одну за допомогою транзакцій
- Розібралися з автоінкрементом: `IDENTITY`, `SEQUENCE` і дірки в нумерації
- Створювали індекси й перевіряли їхню роботу через `EXPLAIN ANALYZE`
- Виконали всі операції з Python через `psycopg` і навчилися уникати N+1 запитів

## Питання для самоперевірки

1. Яка різниця між `DDL` (`CREATE`, `ALTER`, `DROP`) і `DML` (`INSERT`, `UPDATE`, `DELETE`)?
2. Чому `INSERT` потрібно писати з явним переліком колонок?
3. Для чого потрібен `RETURNING` і чим він зручний?
4. Що робить `ON CONFLICT DO NOTHING` і коли він корисний?
5. Чому `score = NULL` не працює і як правильно перевірити відсутність значення?
6. Що станеться, якщо виконати `UPDATE` або `DELETE` без `WHERE`? Як цього уникнути?
7. Чим `TRUNCATE` відрізняється від `DELETE`?
8. Чому видалення курсу може завершитись помилкою? Які є способи це вирішити?
9. Що таке транзакція і навіщо потрібні `COMMIT` та `ROLLBACK`?
10. Чому в нумерації `id` бувають пропуски?
11. Що таке індекс? Як він впливає на швидкість читання і запису?
12. Для яких колонок у нашій схемі PostgreSQL не створює індекс автоматично?
13. Чим відрізняються `Seq Scan` та `Index Scan` у виводі `EXPLAIN`?
14. Чому не можна підставляти значення в SQL через f-string?
15. Що таке проблема N+1 запитів і як її уникнути?

## Корисні посилання

- PostgreSQL SQL Reference: https://www.postgresql.org/docs/current/sql.html
- INSERT (зокрема `ON CONFLICT`): https://www.postgresql.org/docs/current/sql-insert.html
- Типи індексів: https://www.postgresql.org/docs/current/indexes-types.html
- EXPLAIN: https://www.postgresql.org/docs/current/sql-explain.html
- Документація psycopg 3: https://www.psycopg.org/psycopg3/docs/

**Підготовлено:** Олександр Панченко  
**QALight Training Center**