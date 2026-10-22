# Лекція 33: SELECT, JOIN і добір DML — конспект для студентів

Oleksandr Panchenko

## 1. Про що заняття

Після цього заняття ви зможете змінювати й видаляти дані, не зіпсувавши базу, шукати потрібні рядки через `SELECT` і з'єднувати кілька таблиць через `JOIN`.

На минулих заняттях ми спроєктували базу LMS, створили таблиці (`CREATE TABLE`) і вставили дані (`INSERT`). Сьогодні:

1. Уточнення до минулих лекцій (розділ 3).
2. `UPDATE` і `DELETE`: як змінювати й видаляти безпечно (розділ 4).
3. Індекси: що це і навіщо (розділ 5).
4. `SELECT`: `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT` (розділ 6).
5. `JOIN`: як зібрати дані з кількох таблиць (розділ 7).

Кожен приклад із цього конспекту виконуйте самі в DBeaver. Читати запит і виконати його це різні речі, а запам'ятовується друге.

## 2. Навчальна база LMS

Усі приклади сьогодні виконуються на навчальній базі `lms_*`: викладачі створюють курси, курси складаються з уроків, до уроків є завдання, студенти записуються на курси й здають відповіді. Це та сама схема, яку ми проєктували 07.10.

| Таблиця | Що зберігає | Ключові зв'язки |
| --- | --- | --- |
| `lms_users` | викладачі й студенти (`role`) | первинний ключ `id`, унікальний `email` |
| `lms_courses` | курси | `teacher_id` посилається на `lms_users` |
| `lms_lessons` | уроки курсу | `course_id` посилається на `lms_courses` (із каскадом) |
| `lms_enrollments` | хто на який курс записаний | складений ключ `(user_id, course_id)` |
| `lms_assignments` | завдання до уроків | `lesson_id` посилається на `lms_lessons` (із каскадом) |
| `lms_submissions` | відповіді студентів | `assignment_id`, `user_id`, оцінка `score` |

**Запустіть цей скрипт на початку заняття** (`Alt+X` у DBeaver, щоб виконати весь скрипт). Він видаляє й створює таблиці `lms_*` заново, тож **виконуйте його лише в навчальній базі, не в базі свого проєкту**. Дані в таблицях тестові.

```sql
-- Навчальна база LMS для заняття 33. Лише для навчальної бази!
DROP TABLE IF EXISTS lms_submissions, lms_assignments, lms_enrollments,
                     lms_lessons, lms_courses, lms_users CASCADE;

CREATE TABLE lms_users (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    email      VARCHAR(255) NOT NULL UNIQUE,
    role       VARCHAR(20)  NOT NULL CHECK (role IN ('student', 'teacher')),
    created_at TIMESTAMP    NOT NULL DEFAULT now()
);

CREATE TABLE lms_courses (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    teacher_id  INTEGER NOT NULL REFERENCES lms_users(id),
    published   BOOLEAN NOT NULL DEFAULT FALSE,
    price       NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (price >= 0),
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE lms_lessons (
    id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES lms_courses(id) ON DELETE CASCADE,
    title     VARCHAR(200) NOT NULL,
    position  INTEGER NOT NULL CHECK (position > 0),
    content   TEXT
);

CREATE TABLE lms_enrollments (
    user_id     INTEGER NOT NULL REFERENCES lms_users(id),
    course_id   INTEGER NOT NULL REFERENCES lms_courses(id),
    status      VARCHAR(20) NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'completed', 'dropped')),
    enrolled_at TIMESTAMP NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, course_id)
);

CREATE TABLE lms_assignments (
    id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lesson_id INTEGER NOT NULL REFERENCES lms_lessons(id) ON DELETE CASCADE,
    title     VARCHAR(200) NOT NULL,
    max_score INTEGER NOT NULL DEFAULT 100,
    due_date  DATE
);

CREATE TABLE lms_submissions (
    id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    assignment_id INTEGER NOT NULL REFERENCES lms_assignments(id),
    user_id       INTEGER NOT NULL REFERENCES lms_users(id),
    answer        TEXT,
    score         INTEGER CHECK (score BETWEEN 0 AND 100),
    submitted_at  TIMESTAMP NOT NULL DEFAULT now()
);

-- Користувачі: 2 викладачі (id 1, 2) і 4 студенти (id 3-6)
INSERT INTO lms_users (first_name, last_name, email, role) VALUES
    ('Петро',  'Іваненко', 'p.ivanenko@example.com', 'teacher'),
    ('Олена',  'Шевченко', 'o.shevchenko@example.com', 'teacher'),
    ('Ірина',  'Коваль',   'i.koval@example.com', 'student'),
    ('Андрій', 'Мельник',  'a.melnyk@example.com', 'student'),
    ('Ігор',   'Петренко', 'i.petrenko@example.com', 'student'),
    ('Марія',  'Бондар',   'm.bondar@example.com', 'student');

-- Курси: Docker не опублікований, на Docker і Django ніхто не записаний
INSERT INTO lms_courses (title, description, teacher_id, published, price) VALUES
    ('Python Basics', 'Основи Python', 1, TRUE,  1500.00),
    ('SQL Basics',    'Основи SQL',    2, TRUE,  1200.00),
    ('Docker Basics', NULL,            1, FALSE, 0),
    ('Django',        'Веб на Django', 2, TRUE,  2000.00);

INSERT INTO lms_lessons (course_id, title, position) VALUES
    (1, 'Hello Python', 1),
    (1, 'Variables and types', 2),
    (1, 'Loops', 3),
    (2, 'Hello SQL', 1),
    (2, 'SELECT basics', 2),
    (3, 'What is Docker', 1);

INSERT INTO lms_enrollments (user_id, course_id, status) VALUES
    (3, 1, 'active'),
    (3, 2, 'active'),
    (4, 1, 'completed'),
    (5, 2, 'active'),
    (5, 1, 'dropped'),
    (6, 2, 'active');

INSERT INTO lms_assignments (lesson_id, title, max_score, due_date) VALUES
    (1, 'Hello world',     100, '2026-10-05'),
    (2, 'Types quiz',       50, '2026-10-12'),
    (3, 'Loops task',      100, '2026-10-20'),
    (4, 'Create table',    100, '2026-10-10'),
    (5, 'Select practice',  80, '2026-10-30'),
    (6, 'Docker intro',    100, '2026-11-05');

-- Відповіді: у деяких score = NULL (ще не оцінено)
INSERT INTO lms_submissions (assignment_id, user_id, answer, score) VALUES
    (1, 3, 'print("Hello")', 95),
    (1, 4, 'print("Hi")',    70),
    (2, 3, 'quiz answers',   45),
    (2, 4, 'quiz answers',   NULL),
    (4, 3, 'CREATE TABLE',   88),
    (4, 5, 'CREATE TABLE',   65),
    (4, 6, 'CREATE TABLE',   NULL),
    (5, 3, 'SELECT *',       NULL);
```

Контрольний запит. Після скрипта мають вийти 6 користувачів, 4 курси й 6 записів на курси:

```sql
SELECT (SELECT count(*) FROM lms_users)       AS users,
       (SELECT count(*) FROM lms_courses)     AS courses,
       (SELECT count(*) FROM lms_enrollments) AS enrollments;
```

Перше, що варто перевіряти завжди: до якої бази ви підключені.

```sql
SELECT current_database(), current_user;
```

## 3. Уточнення до лекцій 07.10 і 09.10

Після занять ми перевірили документацію PostgreSQL і уточнили кілька тверджень. Якщо ви записали щось інакше, виправте записи за цією таблицею.

| Тема | Як правильно в PostgreSQL | Приклад |
| --- | --- | --- |
| `UNIQUE` і `NULL` | `UNIQUE` не вимагає значення: у колонці може бути багато `NULL`, бо `NULL` не дорівнює `NULL`. Заборонити пропуск може лише `NOT NULL` | `email TEXT UNIQUE` приймає два рядки з `NULL`, але два однакових `'a@x.com'` ні |
| `PRIMARY KEY` | Це одразу `UNIQUE` і `NOT NULL`, і він один на таблицю | `INSERT` без значення для `id INTEGER PRIMARY KEY` дає помилку |
| Значення за замовчуванням | Якщо колонка не заповнена й немає `DEFAULT`, там буде `NULL`, а не 0 | `INSERT INTO t (name) VALUES ('Alex')` залишить `id` як `NULL` (для ключа це помилка) |
| `varchar` і `text` | `varchar(n)` лише обмежує довжину. За місцем і швидкістю він не відрізняється від `text`. Файл бази зменшує `VACUUM FULL`, а не звичайний `VACUUM` | `price VARCHAR(10)` нічого не «стискає» |
| `integer` і `bigint` | `integer`: приблизно від −2,1 млрд до 2,1 млрд. `bigint`: приблизно ±9,2·10¹⁸ | кількість користувачів вмістить `integer`, кількість подій у журналі вже `bigint` |
| `numeric(10,2)` | 10 цифр загалом, із них 2 після коми. Тип точний, його використовують для грошей. `float` наближений | `0.1 + 0.2 = 0.3` істинне для `numeric` і хибне для `float` |
| Нормалізація | 1NF: одна клітинка містить одне значення (ім'я й прізвище вже окремі колонки). 2NF: кожна неключова колонка залежить від усього ключа. 3NF: неключові колонки не залежать одна від одної. Скорочено: «від ключа, від цілого ключа і ні від чого, крім ключа» | назва курсу в `lms_enrollments` порушила б 2NF, бо залежить лише від `course_id` |
| Каскадне видалення | Воно працює лише якщо ви написали `ON DELETE CASCADE`. Без цього PostgreSQL забороняє видалити рядок, на який є посилання | див. розділ 4.3 |
| Функції в базі | Крім `VIEW`, у PostgreSQL є `CREATE FUNCTION`, `CREATE PROCEDURE` і тригери | цього курсу вони не стосуються, але вони існують |
| Транзакції | `BEGIN` починає, `COMMIT` підтверджує, `ROLLBACK` скасовує. У PostgreSQL відкочується навіть зміна структури таблиці | див. розділ 4.2 |
| `ALTER TABLE` | Змінює таблицю, а не створює її. У реальних проєктах це щоденні міграції, а небезпечною є саме `DROP COLUMN` | `ALTER TABLE lms_users ADD COLUMN phone VARCHAR(20)` |
| `LIKE` | `%` замінює будь-яку послідовність символів, `_` один символ. `ILIKE` не залежить від регістру. Регулярні вирази це окремі оператори `~` і `~*` | `title ILIKE '%python%'` |
| SQL-ін'єкції | Від них захищають параметризовані запити (у `psycopg` це `%s`), а не склеювання рядків | `cur.execute("SELECT ... WHERE id = %s", (user_id,))` |
| `UUID` | Сам не заповнюється: потрібен `DEFAULT gen_random_uuid()` | `id UUID DEFAULT gen_random_uuid()` |

Про виконання скриптів у DBeaver: `Ctrl+Enter` виконує один запит, а `Alt+X` весь скрипт. Якщо виконався лише один запит із кількох, це найімовірніша причина.

## 4. `UPDATE` і `DELETE`

Головне правило: **перш ніж змінювати або видаляти, напишіть `SELECT` з тим самим `WHERE` і подивіться, які рядки потраплять під зміну.** `UPDATE` і `DELETE` без `WHERE` змінюють або видаляють усі рядки таблиці.

### 4.1 `UPDATE`: змінити дані

Шаблон:

```sql
UPDATE таблиця
SET колонка1 = значення1, колонка2 = значення2
WHERE умова;
```

Приклади:

```sql
-- 1. Спочатку SELECT
SELECT id, title, price FROM lms_courses WHERE id = 2;

-- 2. Змінити одну колонку
UPDATE lms_courses SET price = 1300 WHERE id = 2;

-- 3. Кілька колонок
UPDATE lms_courses SET published = TRUE, price = 500 WHERE id = 3;

-- 4. Нове значення обчислюється зі старого
UPDATE lms_courses SET price = price * 1.10 WHERE published;

-- 5. RETURNING одразу показує змінені рядки
UPDATE lms_users SET email = 'olena.s@example.com' WHERE id = 2 RETURNING id, email;
```

`UPDATE` змінює дані, а не структуру таблиці. Структуру змінює `ALTER TABLE`.

### 4.2 Транзакція: `BEGIN`, `COMMIT`, `ROLLBACK`

Транзакція це група команд, які виконуються «або всі, або жодна». `BEGIN` її починає, `COMMIT` підтверджує зміни, `ROLLBACK` скасовує. Вона рятує, якщо ви помилилися або якщо щось збилося посередині.

```sql
BEGIN;
UPDATE lms_courses SET price = 0;               -- забули WHERE: змінилося ВСЕ
SELECT id, title, price FROM lms_courses;       -- усі ціни нульові
ROLLBACK;                                       -- скасували
SELECT id, title, price FROM lms_courses;       -- усе на місці
```

Виконуйте такий блок одним скриптом (`Alt+X`). Якщо всередині транзакції сталася помилка, наступні команди відповідатимуть `current transaction is aborted`. Це означає, що треба виконати `ROLLBACK;` і почати знову.

### 4.3 `DELETE` і зовнішні ключі

Шаблон:

```sql
DELETE FROM таблиця WHERE умова;
```

```sql
-- 1. Спочатку SELECT
SELECT * FROM lms_submissions WHERE user_id = 6 AND score IS NULL;

-- 2. Видалити й одразу побачити, що видалилося
DELETE FROM lms_submissions WHERE user_id = 6 AND score IS NULL RETURNING *;
```

**Зовнішній ключ захищає від видалення «батька».** Викладача 1 видалити не вдасться, бо на нього посилаються курси:

```sql
DELETE FROM lms_users WHERE id = 1;
-- ERROR: update or delete on table "lms_users" violates foreign key constraint ...
```

Вчіться читати помилку: вона називає таблицю, яку ви намагалися змінити, і зв'язок, який це забороняє.

**Каскад.** Для уроків і завдань ми задали `ON DELETE CASCADE`. Тому видалення курсу без студентів прибирає і його уроки, і завдання:

```sql
BEGIN;
DELETE FROM lms_courses WHERE id = 3;                       -- курс Docker
SELECT count(*) FROM lms_lessons WHERE course_id = 3;       -- 0
ROLLBACK;
```

А курс Python видалити не вдасться: на нього посилаються записи студентів, а до завдань з відповідями каскад не доходить. Каскад працює лише там, де його явно ввімкнули.

```sql
BEGIN;
DELETE FROM lms_courses WHERE id = 1;    -- ERROR: порушення зовнішнього ключа
ROLLBACK;
```

Що чим є: `DELETE` без `WHERE` видаляє всі рядки таблиці, `TRUNCATE` робить те саме швидше, а `DROP TABLE` видаляє саму таблицю.

### 4.4 «М'яке» видалення

У реальних системах (банк, облік, навчальна платформа) записи рідко видаляють остаточно: податкова може згадати про людину, а обладнання, яке списали, досі входить в історію. Замість `DELETE` додають позначку:

```sql
BEGIN;
ALTER TABLE lms_users ADD COLUMN deleted_at TIMESTAMP;   -- зміна структури теж відкочується
UPDATE lms_users SET deleted_at = now() WHERE id = 6;
SELECT id, last_name FROM lms_users WHERE deleted_at IS NULL;   -- без «видаленого»
ROLLBACK;
```

У запитах такі записи просто виключають через `WHERE deleted_at IS NULL`.

### 4.5 Перевірте себе

Спробуйте розв'язати самі, потім порівняйте з відповідями нижче.

1. Підніміть на 10% ціну всіх опублікованих курсів і поверніть змінені рядки.
2. Змініть e-mail користувача 4 і поверніть рядок.
3. Видаліть усі відповіді користувача 6 без оцінки.
4. Спробуйте видалити користувача 3. Прочитайте помилку: чому її видно?

```sql
-- 1
UPDATE lms_courses SET price = price * 1.10 WHERE published RETURNING id, title, price;
-- 2
UPDATE lms_users SET email = 'andriy.m@example.com' WHERE id = 4 RETURNING id, email;
-- 3
DELETE FROM lms_submissions WHERE user_id = 6 AND score IS NULL RETURNING *;
-- 4
DELETE FROM lms_users WHERE id = 3;   -- ERROR: на користувача 3 посилаються записи на курси і відповіді
```

Після практики дані змінилися. Щоб повернутися до вихідного стану, перезапустіть seed-скрипт із розділу 2.

## 5. Індекси

Індекс це відсортований «покажчик» до значень колонки, як алфавітний покажчик у кінці книги: замість читати все підряд, база переходить одразу до потрібного місця.

- Без індексу PostgreSQL читає таблицю рядок за рядком (у плані запиту це `Seq Scan`).
- З індексом він іде напряму до потрібних рядків (`Index Scan`). Це помітно на таблицях із сотнями тисяч і мільйонами рядків.

Що варто знати:

- `PRIMARY KEY` і `UNIQUE` створюють індекс автоматично.
- `FOREIGN KEY` індексу сам не створює. Колонки зовнішніх ключів (наприклад, `teacher_id`) часто індексують вручну, бо за ними роблять `JOIN` і перевірки при видаленні.

Синтаксис:

```sql
CREATE INDEX idx_lms_courses_teacher_id ON lms_courses (teacher_id);
```

**Приклад із різницею.** Створимо тимчасову таблицю на мільйон рядків. Виконайте блок по порядку й порівняйте `Execution Time` у двох планах (цифри залежать від комп'ютера: у першому випадку це десятки мілісекунд, у другому частки):

```sql
CREATE TABLE lms_big_demo AS
SELECT g AS id, 'user' || g || '@example.com' AS email
FROM generate_series(1, 1000000) AS g;
ANALYZE lms_big_demo;

EXPLAIN ANALYZE
SELECT * FROM lms_big_demo WHERE email = 'user777777@example.com';   -- Seq Scan

CREATE INDEX idx_big_demo_email ON lms_big_demo (email);

EXPLAIN ANALYZE
SELECT * FROM lms_big_demo WHERE email = 'user777777@example.com';   -- Index Scan

DROP TABLE lms_big_demo;
```

У плані запиту дивіться на два рядки: тип сканування (`Seq Scan` або `Index Scan`) і `Execution Time`.

**Ціна індексу.** Індекс займає місце на диску й сповільнює `INSERT`, `UPDATE` та `DELETE`, бо його теж треба оновлювати. На таблицях із десятками чи тисячами рядків виграшу майже немає: база сама вибере `Seq Scan`. Індекс має сенс там, де рядків багато і за колонкою часто шукають.

**Обмеження.** Звичайний індекс не допомагає для `LIKE '%python%'`, бо шаблон починається з `%`. Складені й часткові індекси, GIN і GiST існують, але виходять за рамки цього курсу.

## 6. `SELECT`: вибір даних

Шаблон запиту (так пишемо):

```sql
SELECT   колонки
FROM     таблиця
WHERE    умова
ORDER BY сортування
LIMIT    скільки;
```

Виконується `WHERE` раніше за `SELECT`, тому псевдонім колонки (розділ 6.4) не можна використати у `WHERE`, але можна в `ORDER BY`. Після `FROM` стоїть таблиця, `VIEW` або підзапит.

Пишіть назви колонок, а не `*`: ви бачите, що саме вибираєте, а запит не зламається, коли в таблицю додадуть колонку.

### 6.1 `WHERE`: умови

| Що потрібно | Оператор | Приклад |
| --- | --- | --- |
| порівняння | `=`, `<>`, `<`, `<=`, `>`, `>=` | `price > 1000` |
| «і», «або», «не» | `AND`, `OR`, `NOT` | `published AND price < 1500` |
| значення зі списку | `IN (...)` | `teacher_id IN (1, 2)` |
| діапазон (обидві межі включно) | `BETWEEN a AND b` | `score BETWEEN 50 AND 100` |
| шаблон тексту | `LIKE`, `ILIKE` (без урахування регістру) | `title ILIKE '%python%'` |
| відсутність значення | `IS NULL`, `IS NOT NULL` | `score IS NULL` |

У шаблоні `LIKE`: `%` замінює будь-яку послідовність символів, `_` рівно один символ.

```sql
SELECT id, title, price FROM lms_courses WHERE published AND price > 1000;
SELECT first_name, last_name FROM lms_users WHERE role = 'student' AND last_name <> 'Коваль';
SELECT id, title FROM lms_courses WHERE teacher_id IN (1, 2);
SELECT id, assignment_id, score FROM lms_submissions WHERE score BETWEEN 50 AND 100;
SELECT * FROM lms_users WHERE email LIKE '%@example.com';
SELECT * FROM lms_courses WHERE title ILIKE '%python%';
SELECT id, user_id, assignment_id FROM lms_submissions WHERE score IS NULL;
```

### 6.2 `NULL`: пастка, у яку потрапляють усі

`NULL` означає «значення невідоме». Тому порівняння з ним не істинне й не хибне, і його не можна перевіряти через `=`. Спрогнозуйте результат перед запуском:

```sql
SELECT * FROM lms_submissions WHERE score = NULL;    -- 0 рядків, завжди
SELECT * FROM lms_submissions WHERE score IS NULL;   -- правильно
SELECT * FROM lms_submissions WHERE score <> 70;     -- рядки з NULL сюди теж не потрапляють
```

### 6.3 `ORDER BY`, `LIMIT`, `OFFSET`

```sql
SELECT id, title, price FROM lms_courses ORDER BY price DESC;                      -- спадання
SELECT first_name, last_name FROM lms_users ORDER BY last_name, first_name;       -- за двома колонками

-- три найкращі оцінки
SELECT id, user_id, score FROM lms_submissions
WHERE score IS NOT NULL
ORDER BY score DESC
LIMIT 3;

-- друга сторінка по 2 курси
SELECT id, title FROM lms_courses ORDER BY id LIMIT 2 OFFSET 2;
```

- Без `ORDER BY` порядок рядків не гарантований, тому `LIMIT` без сортування повертає «якісь» рядки.
- У PostgreSQL при `DESC` значення `NULL` йдуть першими. Щоб їх відсунути, пишуть `ORDER BY score DESC NULLS LAST`.

### 6.4 `DISTINCT` і псевдоніми

`DISTINCT` залишає лише унікальні значення. Псевдонім `AS` дає колонці нову назву в результаті.

```sql
SELECT DISTINCT role FROM lms_users;
SELECT DISTINCT status FROM lms_enrollments;

SELECT first_name || ' ' || last_name AS full_name, email FROM lms_users;
SELECT title, price, price * 0.9 AS price_with_discount FROM lms_courses;
```

Оператор `||` склеює рядки.

### 6.5 Дата й діапазони

Для колонки типу `DATE` діапазон за жовтень можна написати двома способами:

```sql
SELECT id, title, due_date FROM lms_assignments
WHERE due_date BETWEEN '2026-10-01' AND '2026-10-31';

-- безпечніша форма: «від включно, до не включно» (працює і для TIMESTAMP)
SELECT id, title, due_date FROM lms_assignments
WHERE due_date >= '2026-10-01' AND due_date < '2026-11-01';
```

Для `TIMESTAMP` перша форма «губить» 31 жовтня після 00:00, тому звичка писати другу форму безпечніша.

### 6.6 Перевірте себе

1. Опубліковані курси дешевші за 1500, від дешевших до дорожчих.
2. Студенти, чиє прізвище починається на «К».
3. Три найкращі оцінки (без непроставлених).
4. Завдання з терміном здачі у жовтні 2026.
5. Відповіді, які ще не оцінені.

```sql
-- 1
SELECT id, title, price FROM lms_courses WHERE published AND price < 1500 ORDER BY price;
-- 2
SELECT first_name, last_name FROM lms_users WHERE role = 'student' AND last_name LIKE 'К%';
-- 3
SELECT id, user_id, score FROM lms_submissions WHERE score IS NOT NULL ORDER BY score DESC LIMIT 3;
-- 4
SELECT id, title, due_date FROM lms_assignments
WHERE due_date >= '2026-10-01' AND due_date < '2026-11-01';
-- 5
SELECT id, user_id, assignment_id FROM lms_submissions WHERE score IS NULL;
```

## 7. `JOIN`: з'єднання таблиць

Ми розклали дані по таблицях заради нормалізації. У таблиці `lms_courses` є `teacher_id = 1`, але з нього не видно, хто це. `JOIN` збирає дані з кількох таблиць назад в один результат.

### 7.1 Основа: `JOIN ... ON`

```sql
SELECT c.id, c.title, u.first_name, u.last_name
FROM lms_courses AS c
JOIN lms_users   AS u ON u.id = c.teacher_id;
```

- `FROM lms_courses AS c` основна таблиця і короткий псевдонім `c`.
- `JOIN lms_users AS u` таблиця, яку приєднуємо, і її псевдонім `u`.
- `ON u.id = c.teacher_id` умова зв'язку. Майже завжди це «зовнішній ключ = первинний ключ».
- Префікс `c.` або `u.` вказує, з якої таблиці колонка. Якщо колонка з такою назвою є в обох таблицях, префікс обов'язковий:

```sql
SELECT id, title FROM lms_courses c JOIN lms_users u ON u.id = c.teacher_id;
-- ERROR: column reference "id" is ambiguous
```

### 7.2 `INNER JOIN` і `LEFT JOIN`

`JOIN` без уточнення це те саме, що `INNER JOIN`: у результат потрапляють лише ті рядки, для яких знайшлася пара в обох таблицях. `LEFT JOIN` залишає всі рядки лівої таблиці, а де пари немає, у колонках правої стоїть `NULL`.

| Тип | Що повертає |
| --- | --- |
| `INNER JOIN` (або просто `JOIN`) | лише рядки з парою в обох таблицях |
| `LEFT JOIN` | усі рядки лівої таблиці, і пару з правої, якщо вона є (інакше `NULL`) |

Спрогнозуйте кількість рядків перед запуском:

```sql
-- INNER: лише курси, на які хтось записаний
SELECT c.title, e.user_id
FROM lms_courses c
JOIN lms_enrollments e ON e.course_id = c.id;           -- 6 рядків

-- LEFT: усі курси, навіть без студентів
SELECT c.title, e.user_id
FROM lms_courses c
LEFT JOIN lms_enrollments e ON e.course_id = c.id;      -- 8 рядків: для Docker і Django user_id = NULL

-- Курси без жодного студента
SELECT c.title
FROM lms_courses c
LEFT JOIN lms_enrollments e ON e.course_id = c.id
WHERE e.user_id IS NULL;
```

`RIGHT JOIN` це `LEFT JOIN` із переставленими таблицями, а `FULL JOIN` бере всі рядки з обох боків. Вони трапляються рідше.

### 7.3 Зв'язок «багато-до-багатьох» і ланцюжки

Студент може бути на кількох курсах, а курс має кількох студентів. Такий зв'язок реалізується проміжною таблицею `lms_enrollments`: щоб побачити, хто на що записаний, приєднуємо дві таблиці до середньої.

```sql
SELECT u.first_name, u.last_name, c.title, e.status
FROM lms_enrollments e
JOIN lms_users   u ON u.id = e.user_id
JOIN lms_courses c ON c.id = e.course_id
ORDER BY c.title, u.last_name;
```

Щоб залишити лише активні записи, додайте `WHERE e.status = 'active'` перед `ORDER BY`.

З'єднувати можна скільки завгодно таблиць. Ланцюжок із п'яти таблиць: від відповіді студента до курсу.

```sql
SELECT u.last_name,
       c.title AS course,
       a.title AS assignment,
       s.score,
       a.max_score
FROM lms_submissions s
JOIN lms_users       u ON u.id = s.user_id
JOIN lms_assignments a ON a.id = s.assignment_id
JOIN lms_lessons     l ON l.id = a.lesson_id
JOIN lms_courses     c ON c.id = l.course_id
WHERE s.score IS NOT NULL
ORDER BY s.score DESC;
```

Читайте такий запит від `FROM` вниз: відповідь, її автор, її завдання, урок цього завдання, курс цього уроку.

### 7.4 Типові помилки

- **Немає умови зв'язку.** Запис `FROM a, b` без `WHERE` дає декартів добуток: кожен рядок однієї таблиці з кожним рядком другої. На великих таблицях це завалить базу.
- **`WHERE` по правій таблиці в `LEFT JOIN`.** Умова на колонку правої таблиці відкидає рядки з `NULL`, і `LEFT JOIN` стає `INNER`:

```sql
SELECT c.title, e.status
FROM lms_courses c
LEFT JOIN lms_enrollments e ON e.course_id = c.id
WHERE e.status = 'active';       -- Docker і Django зникли, бо NULL не дорівнює 'active'
```

- **Дублі рядків.** Курс із трьома студентами в результаті з'являється тричі. Це не помилка, а властивість зв'язку «один-до-багатьох». Підрахунок «скільки студентів на курсі» буде на наступній лекції (`GROUP BY`).
- **Неоднозначні колонки.** Завжди пишіть псевдонім перед назвою колонки.

### 7.5 Перевірте себе

1. Список опублікованих курсів із прізвищем викладача.
2. Хто записаний на курс «Python Basics» (прізвище, статус).
3. Курси, на які ніхто не записаний.
4. Оцінки Ірини Коваль: назва завдання, `score`, `max_score` (лише виставлені).

```sql
-- 1
SELECT c.title, u.last_name
FROM lms_courses c
JOIN lms_users u ON u.id = c.teacher_id
WHERE c.published;

-- 2
SELECT u.last_name, e.status
FROM lms_enrollments e
JOIN lms_users u   ON u.id = e.user_id
JOIN lms_courses c ON c.id = e.course_id
WHERE c.title = 'Python Basics';

-- 3
SELECT c.title
FROM lms_courses c
LEFT JOIN lms_enrollments e ON e.course_id = c.id
WHERE e.user_id IS NULL;

-- 4
SELECT a.title, s.score, a.max_score
FROM lms_submissions s
JOIN lms_users u       ON u.id = s.user_id
JOIN lms_assignments a ON a.id = s.assignment_id
WHERE u.first_name = 'Ірина' AND u.last_name = 'Коваль' AND s.score IS NOT NULL;
```

## 8. Типові помилки й як їх читати

Помилка PostgreSQL складається з кількох частин. `ERROR` це суть, `DETAIL` називає конкретні значення або таблиці, `HINT` іноді підказує рішення, а `Position` (або підсвітка в DBeaver) вказує місце в запиті. Читайте її вголос і повністю, а не лише перше слово.

| Повідомлення | Що це означає | Що робити |
| --- | --- | --- |
| `relation "lms_users" does not exist` | такої таблиці немає в поточній базі | перевірте `SELECT current_database();`, виконайте seed-скрипт, оновіть дерево бази (`F5`) |
| `column "Коваль" does not exist` | текст узято в подвійні лапки, і PostgreSQL шукає колонку | рядки пишуться в одинарних лапках: `'Коваль'` |
| `column reference "id" is ambiguous` | `id` є в кількох таблицях запиту | додайте псевдонім: `c.id`, `u.id` |
| `syntax error at or near "FROM"` | помилка поруч із цим словом, часто зайва кома перед ним | подивіться на слово перед ним і на кому |
| `null value in column "x" violates not-null constraint` | у колонку з `NOT NULL` не передали значення | додайте значення в `INSERT`/`UPDATE` |
| `duplicate key value violates unique constraint` | таке значення вже є в колонці з `UNIQUE` або `PRIMARY KEY` | змініть значення або оновіть існуючий рядок |
| `insert or update on table ... violates foreign key constraint` | `INSERT` або `UPDATE` посилається на неіснуючий рядок | перевірте значення зовнішнього ключа (наприклад, `teacher_id = 999`) |
| `update or delete on table ... violates foreign key constraint` | `DELETE` рядка, на який є посилання | спершу видаліть дочірні рядки або перегляньте зв'язок |
| `new row ... violates check constraint` | значення не пройшло `CHECK` | перевірте допустиме значення (наприклад, `role` лише `student` або `teacher`) |
| `current transaction is aborted, commands ignored until end of transaction block` | у транзакції була помилка | виконайте `ROLLBACK;` і почніть заново |
| `WHERE score = NULL` нічого не повертає | `NULL` не порівнюється через `=` | `WHERE score IS NULL` |
| Дані «не збереглися» | транзакція не завершена | виконайте `COMMIT;` (або `ROLLBACK;`, якщо зміни не потрібні) |

Два загальні правила налагодження:

1. Скоротіть запит до найпростішого, який ще падає, і додавайте частини по одній.
2. Для `UPDATE` і `DELETE` спочатку виконайте `SELECT` з тим самим `WHERE`.

## 9. Шпаргалка

| Завдання | Шаблон | Приклад |
| --- | --- | --- |
| змінити дані | `UPDATE t SET c = v WHERE ...;` | `UPDATE lms_courses SET price = 1300 WHERE id = 2;` |
| видалити рядки | `DELETE FROM t WHERE ...;` | `DELETE FROM lms_submissions WHERE score IS NULL;` |
| побачити змінене | `... RETURNING колонки;` | `UPDATE ... WHERE id = 2 RETURNING id, price;` |
| транзакція | `BEGIN; ... COMMIT;` або `ROLLBACK;` | див. розділ 4.2 |
| індекс | `CREATE INDEX назва ON t (колонка);` | `CREATE INDEX idx_c_teacher ON lms_courses (teacher_id);` |
| вибрати колонки | `SELECT c1, c2 FROM t;` | `SELECT id, title FROM lms_courses;` |
| умова | `WHERE ... AND/OR/NOT ...` | `WHERE published AND price < 1500` |
| зі списку | `IN (...)` | `WHERE teacher_id IN (1, 2)` |
| діапазон | `BETWEEN a AND b` (межі включно) | `WHERE score BETWEEN 50 AND 100` |
| шаблон тексту | `LIKE` / `ILIKE`, `%` і `_` | `WHERE title ILIKE '%sql%'` |
| відсутнє значення | `IS NULL` / `IS NOT NULL` | `WHERE score IS NULL` |
| сортування | `ORDER BY c ASC/DESC [NULLS LAST]` | `ORDER BY score DESC NULLS LAST` |
| кількість рядків | `LIMIT n OFFSET m` | `LIMIT 3` |
| унікальні значення | `SELECT DISTINCT c` | `SELECT DISTINCT role FROM lms_users;` |
| псевдонім | `колонка AS назва` | `price * 0.9 AS price_with_discount` |
| з'єднання | `JOIN t2 ON t2.fk = t1.pk` | `JOIN lms_users u ON u.id = c.teacher_id` |
| усі зліва | `LEFT JOIN t2 ON ...` | курси без студентів: `LEFT JOIN ... WHERE e.user_id IS NULL` |

Три правила, які варто запам'ятати:

1. Перед `UPDATE` і `DELETE` пишіть `SELECT` з тим самим `WHERE`.
2. `NULL` перевіряють через `IS NULL`, а не через `=`.
3. У `JOIN` завжди пишіть псевдонім перед назвою колонки.

## 10. Домашнє завдання

Напишіть файл `lesson33_homework.sql` із десятьма запитами до навчальної бази `lms_*` і здайте його тим самим способом, що й попередні SQL-скрипти. **Перед початком перезапустіть seed-скрипт із розділу 2**, щоб працювати з чистими даними.

| № | Завдання | Очікувана кількість рядків на чистій базі |
| --- | --- | --- |
| 1 | Опубліковані курси дорожчі за 1000, від дорожчих до дешевших: `id`, `title`, `price` | 3 |
| 2 | Студенти з e-mail на `@example.com`, відсортовані за прізвищем: `last_name`, `first_name`, `email` | 4 |
| 3 | Три найгірші оцінки (лише виставлені): `id`, `user_id`, `score` | 3 |
| 4 | Завдання з `max_score` не менше 80 і терміном здачі не пізніше 15.10.2026: `id`, `title`, `max_score`, `due_date` | 2 |
| 5 | Знизити ціну курсу «SQL Basics» на 100 й повернути змінений рядок | 1 |
| 6 | Позначити запис користувача 5 на курс 1 як `completed` і повернути рядок | 1 |
| 7 | Видалити відповіді без оцінки до завдання 4 і повернути видалені рядки | 1 |
| 8 | `JOIN`: назва курсу і прізвище викладача для всіх курсів | 4 |
| 9 | `JOIN`: студент (прізвище), курс (назва), статус, лише для активних записів | 4 |
| 10 | `LEFT JOIN`: курси, на які ніхто не записаний | 2 |

Додатково (за бажанням): завдання, до яких немає жодної відповіді студента (`LEFT JOIN` до `lms_submissions`). Очікується 2 рядки.

**Вимоги до файлу:**

1. Над кожним запитом коментар в один рядок: що він робить.
2. Запити 5–7 (`UPDATE` і `DELETE`) обгорніть у `BEGIN; ... ROLLBACK;`, щоб файл можна було запускати знову, а дані не змінювалися.
3. У `UPDATE` і `DELETE` обов'язковий `WHERE`.
4. Без `SELECT *`: перелічуйте колонки.
5. У `JOIN` перед кожною колонкою псевдонім таблиці.

**Шаблон початку файлу:**

```sql
-- lesson33_homework.sql
-- Автор: <ваше ім'я>

-- 1. Опубліковані курси дорожчі за 1000, від дорожчих
SELECT id, title, price
FROM lms_courses
WHERE published AND price > 1000
ORDER BY price DESC;

-- 5. Знизити ціну SQL Basics на 100
BEGIN;
UPDATE lms_courses SET price = price - 100 WHERE title = 'SQL Basics' RETURNING id, title, price;
ROLLBACK;
```

**Як перевіряють.** Файл запускають на чистій seed-базі, звіряють кількість рядків і дивляться на структуру запитів (наявність `WHERE`, `ROLLBACK`, коментарів, псевдонімів).

Якщо щось не виходить, надішліть запит і текст помилки: вчимося читати помилку, а не лякатися її.

**Наступне заняття:** `GROUP BY`, `COUNT`/`SUM`/`AVG`, `HAVING` і `VIEW`. Вони відповідають на питання на кшталт «скільки студентів на кожному курсі» і «яка середня оцінка за завдання».
