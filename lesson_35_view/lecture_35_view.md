# Заняття 35. Агрегація, групування та представлення даних

**Викладач:** Олександр Панченко 
**Курс:** Програмування Python · Модуль 5. PostgreSQL

## Цілі заняття

На минулому занятті ми навчилися отримувати рядки з однієї чи кількох таблиць. Але в реальних задачах рідко потрібні самі рядки. Зазвичай питання звучать так: *скільки студентів на курсі? яка середня оцінка? хто найкраще впорався із завданням? як змінювалися оцінки студента з часом?* Відповіді на такі питання дає **агрегація**: стиснення багатьох рядків у числа та підсумки.

Після заняття ви зможете:

1. Рахувати підсумки: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STRING_AGG`, `FILTER`
2. Групувати дані через `GROUP BY` і відфільтровувати групи через `HAVING`
3. Писати вкладені запити: у `WHERE`, у `SELECT`, у `FROM`, з `EXISTS`, а також розбивати запит на частини через `WITH` (CTE)
4. Користуватися `DISTINCT` та `DISTINCT ON` для унікальних значень і «першого рядка в групі»
5. Застосовувати віконні функції з `OVER` та `PARTITION BY`: рейтинги, накопичувальні суми, порівняння з попереднім рядком
6. Створювати й використовувати `VIEW`, щоб зберігати складні запити під зрозумілими іменами

## Як вибрати інструмент

Усі теми заняття відповідають на різні питання. Це зручна шпаргалка, до якої варто повертатися:

| Що потрібно | Інструмент |
| ----------- | ---------- |
| Одне число на всю таблицю («скільки всього здач?») | агрегатна функція без групування |
| Число на кожну групу, рядки згортаються («скільки здач на кожне завдання?») | `GROUP BY` |
| Залишити лише деякі групи («завдання, де більше 2 здач») | `HAVING` |
| Порівняти з результатом іншого запиту («курси дорожчі за середню ціну») | вкладений запит |
| Перший чи найкращий рядок у кожній групі («остання здача студента») | `DISTINCT ON` або `ROW_NUMBER()` |
| Залишити всі рядки й додати до кожного підсумок групи («оцінка і середня по завданню») | віконна функція |
| Багаторазово використовувати складний запит | `VIEW` |

## Порядок заняття

Ми йдемо від простого до складного: спочатку агрегація (частини 1–3), потім вкладені запити, які вже можуть її використовувати (частина 4), далі `DISTINCT` і `DISTINCT ON` (частина 5), віконні функції (частина 6) і наприкінці `VIEW`, яке збирає все вивчене в готові «таблиці-звіти» (частина 7).

---

## Частина 0. Підготовка

Працюємо з тією самою базою LMS і тими самими даними, що й на занятті 34. Виконайте скрипт із **частини 0 заняття 34** (структура та дані). Він створює таблиці заново, тож стан бази буде точно таким, який припускають усі приклади й відповіді цієї лекції.

Перевірте кількості рядків: `users` 8, `courses` 5, `lessons` 8, `enrollments` 9, `assignments` 6, `submissions` 10.

### Довідник по даних

Щоб легше перевіряти результати, тримайте перед очима ці таблиці.

**Здачі (`submissions`):**

| id | завдання | студент | оцінка | коли здано |
| -- | -------- | ------- | ------ | ---------- |
| 1 | 1 | 3 (Ірина) | 90 | 2026-10-01 10:00 |
| 2 | 1 | 4 (Андрій) | 70 | 2026-10-02 12:30 |
| 3 | 1 | 5 (Марія) | 100 | 2026-10-02 09:15 |
| 4 | 2 | 3 (Ірина) | 85 | 2026-10-08 18:00 |
| 5 | 2 | 4 (Андрій) | `NULL` | 2026-10-09 11:00 |
| 6 | 3 | 3 (Ірина) | `NULL` | 2026-10-10 20:45 |
| 7 | 4 | 3 (Ірина) | 45 | 2026-10-12 14:20 |
| 8 | 4 | 7 (Софія) | 50 | 2026-10-13 16:10 |
| 9 | 6 | 4 (Андрій) | 80 | 2026-10-14 13:00 |
| 10 | 6 | 7 (Софія) | `NULL` | 2026-10-15 17:30 |

**Завдання та курси:** завдання 1, 2, 3 належать курсу `Python Basics` (id 1); завдання 4 і 5 належать курсу `SQL Basics` (id 2); завдання 6 належить курсу `QA Fundamentals` (id 4). Максимальний бал: 100 для завдань 1, 2, 3 та 6, і 50 для завдань 4 та 5.

**Записи на курси (`enrollments`):** Ірина: курси 1 та 2 (`active`); Андрій: курс 1 (`active`) і курс 4 (`completed`); Марія: курс 1 (`active`), курс 2 (`dropped`) і курс 4 (`active`); Софія: курси 2 та 4 (`active`); Тарас не записаний ні на що.

**Ціни курсів:** `Python Basics` 1200, `SQL Basics` 900, `Python Advanced` 1500 (чернетка), `QA Fundamentals` 800, `Git Essentials` 0.

---

## Частина 1. Агрегатні функції

### 1.1. Ідея

Агрегатна функція бере **набір рядків** і повертає **одне значення**. Основні функції:

| Функція | Що повертає |
| ------- | ----------- |
| `COUNT(*)` | кількість рядків |
| `COUNT(колонка)` | кількість значень, що **не** `NULL` |
| `COUNT(DISTINCT колонка)` | кількість унікальних значень, що не `NULL` |
| `SUM(колонка)` | сума |
| `AVG(колонка)` | середнє арифметичне |
| `MIN(колонка)` / `MAX(колонка)` | найменше / найбільше |
| `STRING_AGG(колонка, роздільник)` | склеює значення в один рядок |

### 1.2. Підсумки по всій таблиці

```sql
SELECT
    COUNT(*)               AS total,
    COUNT(score)           AS graded,
    SUM(score)             AS total_score,
    ROUND(AVG(score), 2)   AS avg_score,
    MIN(score)             AS min_score,
    MAX(score)             AS max_score
FROM submissions;
```

```text
 total | graded | total_score | avg_score | min_score | max_score
-------+--------+-------------+-----------+-----------+-----------
    10 |      7 |         520 |     74.29 |        45 |       100
```

Зверніть увагу на різницю між `COUNT(*)` та `COUNT(score)`: усього 10 здач, але оцінок лише 7, бо `COUNT(колонка)` пропускає `NULL`.

Запит без `GROUP BY` повертає завжди **один рядок**.

### 1.3. Агрегати та NULL

Усі агрегатні функції, крім `COUNT(*)`, **ігнорують `NULL`**. Це легко пропустити, а наслідки суттєві. Середня оцінка `74.29` — це 520 / 7, тобто неоцінені роботи просто не враховуються. Якщо ж вважати відсутню оцінку нулем:

```sql
SELECT ROUND(AVG(COALESCE(score, 0)), 2) AS avg_with_zeros FROM submissions;
-- 52.00  (520 / 10)
```

Яке з двох чисел правильне, залежить від бізнес-логіки: `74.29` відповідає на питання «яка середня оцінка за оцінені роботи», а `52.00` на «що було б, якби неоцінені вважалися провальними». Завжди усвідомлюйте, що саме ви рахуєте.

Ще одна особливість: на **порожньому** наборі `COUNT` повертає `0`, а `SUM`, `AVG`, `MIN`, `MAX` повертають `NULL`:

```sql
-- Тарас (id 6) не здавав жодної роботи
SELECT COUNT(*) AS cnt, SUM(score) AS total, COALESCE(SUM(score), 0) AS total_or_zero
FROM submissions
WHERE student_id = 6;
```

```text
 cnt | total | total_or_zero
-----+-------+---------------
   0 |       |             0
```

Тому `COALESCE(SUM(...), 0)` це стандартний захист у звітах.

### 1.4. COUNT(DISTINCT ...)

Скільки різних студентів хоч раз здавали роботу:

```sql
SELECT COUNT(DISTINCT student_id) AS active_students FROM submissions;
-- 4  (студенти 3, 4, 5, 7)
```

### 1.5. FILTER: умовні агрегати

У PostgreSQL до будь-якого агрегату можна додати `FILTER (WHERE ...)`. Це зручний спосіб порахувати кілька підсумків за різними умовами в одному запиті:

```sql
SELECT
    COUNT(*)                                AS total,
    COUNT(*) FILTER (WHERE score IS NULL)   AS pending,
    COUNT(*) FILTER (WHERE score >= 80)     AS good
FROM submissions;
```

```text
 total | pending | good
-------+---------+------
    10 |       3 |    4
```

Без `FILTER` довелося б писати кілька окремих запитів.

### 1.6. STRING_AGG: список в одному рядку

```sql
SELECT
    t.first_name || ' ' || t.last_name AS teacher,
    STRING_AGG(c.title, ', ' ORDER BY c.title) AS courses
FROM users t
JOIN courses c ON c.teacher_id = t.id
GROUP BY t.id, t.first_name, t.last_name
ORDER BY t.id;
```

```text
    teacher    |                         courses
---------------+---------------------------------------------------------
 Петро Іваненко | Python Basics, SQL Basics
 Олена Шевченко | Git Essentials, Python Advanced, QA Fundamentals
```

Цей запит уже містить `GROUP BY`. Саме про нього наступна частина.

---

## Частина 2. GROUP BY: групуємо рядки

### 2.1. Як це працює

`GROUP BY` розбиває рядки на групи за значенням однієї або кількох колонок. Агрегатна функція тоді рахується **окремо для кожної групи**, і кожна група перетворюється на один рядок результату.

```sql
-- Скільки здач на кожне завдання
SELECT assignment_id, COUNT(*) AS submissions
FROM submissions
GROUP BY assignment_id
ORDER BY assignment_id;
```

```text
 assignment_id | submissions
---------------+-------------
             1 |           3
             2 |           2
             3 |           1
             4 |           2
             6 |           2
```

Завдання 5 немає в результаті: на нього немає жодної здачі, тож групи для нього не утворилось.

Ще кілька прикладів на тих самих даних:

```sql
-- Користувачі за ролями
SELECT role, COUNT(*) AS cnt FROM users GROUP BY role ORDER BY role;
-- student 5, teacher 3

-- Записи за статусами
SELECT status, COUNT(*) AS cnt FROM enrollments GROUP BY status ORDER BY status;
-- active 7, completed 1, dropped 1

-- Користувачі за доменом пошти (групування за виразом)
SELECT split_part(email, '@', 2) AS domain, COUNT(*) AS cnt
FROM users
GROUP BY domain
ORDER BY cnt DESC, domain;
-- gmail.com 3, lms.ua 3, mail.com 2
```

### 2.2. Головне правило GROUP BY

Кожна колонка у `SELECT` має бути **або в `GROUP BY`, або всередині агрегатної функції**. Інакше PostgreSQL повідомить про помилку:

```sql
-- ❌ Помилка
SELECT c.title, COUNT(*) FROM courses c JOIN lessons l ON l.course_id = c.id;
-- ERROR: column "c.title" must appear in the GROUP BY clause
--        or be used in an aggregate function
```

Логіка проста: після групування для кожної групи є лише одне значення агрегату, а `title` у групі може бути різним, тож база не знає, яке з них показати.

Практична порада: якщо групуєте за первинним ключем таблиці (`c.id`), PostgreSQL дозволяє вибирати й інші колонки цієї таблиці. Проте для читабельності й переносимості краще перелічувати їх усі: `GROUP BY c.id, c.title`.

### 2.3. Групування за кількома колонками

Група це унікальна комбінація значень:

```sql
-- Скільки записів на кожному курсі в кожному статусі
SELECT course_id, status, COUNT(*) AS cnt
FROM enrollments
GROUP BY course_id, status
ORDER BY course_id, status;
```

```text
 course_id |  status   | cnt
-----------+-----------+-----
         1 | active    |   3
         2 | active    |   2
         2 | dropped   |   1
         4 | active    |   2
         4 | completed |   1
```

### 2.4. GROUP BY разом з JOIN

Задача: прибуток курсів, якщо враховувати активних і завершивших студентів (але не тих, хто вибув):

```sql
SELECT
    c.title,
    COUNT(*)     AS paying_students,
    SUM(c.price) AS revenue
FROM enrollments e
JOIN courses c ON c.id = e.course_id
WHERE e.status <> 'dropped'
GROUP BY c.id, c.title
ORDER BY revenue DESC;
```

```text
      title      | paying_students | revenue
-----------------+-----------------+---------
 Python Basics   |               3 | 3600.00
 QA Fundamentals |               3 | 2400.00
 SQL Basics      |               2 | 1800.00
```

Порядок виконання тут такий: спочатку `JOIN`, потім `WHERE` відкидає записи зі статусом `dropped`, далі `GROUP BY` групує решту, і в кінці рахуються `COUNT` та `SUM`.

Ще приклад: середня оцінка кожного студента.

```sql
SELECT
    u.first_name || ' ' || u.last_name AS student,
    COUNT(*)                           AS submissions,
    COUNT(s.score)                     AS graded,
    ROUND(AVG(s.score), 2)             AS avg_score
FROM submissions s
JOIN users u ON u.id = s.student_id
GROUP BY u.id, u.first_name, u.last_name
ORDER BY avg_score DESC;
```

```text
     student     | submissions | graded | avg_score
-----------------+-------------+--------+-----------
 Марія Бондар    |           1 |      1 |    100.00
 Андрій Мельник  |           3 |      2 |     75.00
 Ірина Коваль    |           4 |      3 |     73.33
 Софія Лисенко   |           2 |      1 |     50.00
```

### 2.5. Групи, яких немає: LEFT JOIN і COUNT

Якщо потрібні **всі** об'єкти, зокрема з нульовою кількістю, групувати слід від потрібної таблиці через `LEFT JOIN`, а рахувати колонку правої таблиці:

```sql
SELECT c.title, COUNT(e.user_id) AS active_students
FROM courses c
LEFT JOIN enrollments e
       ON e.course_id = c.id AND e.status = 'active'
GROUP BY c.id, c.title
ORDER BY c.id;
```

```text
      title      | active_students
-----------------+-----------------
 Python Basics   |               3
 SQL Basics      |               2
 Python Advanced |               0
 QA Fundamentals |               2
 Git Essentials  |               0
```

Саме `COUNT(e.user_id)` (а не `COUNT(*)`) дає `0` для курсів без студентів: `COUNT(*)` порахував би єдиний рядок із `NULL` і повернув `1`.

### 2.6. Пастка: два JOIN-и «один до багатьох»

Спробуємо за один запит порахувати уроки й активних студентів кожного курсу:

```sql
-- ❌ Неправильні числа
SELECT
    c.title,
    COUNT(l.id)      AS lessons_count,
    COUNT(e.user_id) AS active_students
FROM courses c
LEFT JOIN lessons l     ON l.course_id = c.id
LEFT JOIN enrollments e ON e.course_id = c.id AND e.status = 'active'
GROUP BY c.id, c.title
ORDER BY c.id;
```

```text
      title      | lessons_count | active_students
-----------------+---------------+-----------------
 Python Basics   |             9 |               9
 SQL Basics      |             6 |               6
 Python Advanced |             0 |               0
 QA Fundamentals |             4 |               4
 Git Essentials  |             0 |               0
```

Справжні значення для `Python Basics` це 3 уроки та 3 студенти, а не 9 і 9. Причина: кожен з 3 уроків «множиться» на кожного з 3 студентів, і в проміжному результаті виходить 3 × 3 = 9 рядків на курс.

Є два способи виправити:

```sql
-- Спосіб 1: рахувати унікальні значення
COUNT(DISTINCT l.id)      AS lessons_count,
COUNT(DISTINCT e.user_id) AS active_students

-- Спосіб 2 (чистіший): підрахунки у вкладених запитах, див. частину 4.5
```

Загальне правило: **якщо у запиті два і більше JOIN-и типу «один до багатьох», агрегати починають рахувати помилково**. Перевіряйте числа вибірково.

---

## Частина 3. HAVING: фільтруємо групи

### 3.1. WHERE проти HAVING

`WHERE` працює з окремими рядками **до** групування. Агрегатні функції в ньому використовувати не можна, адже груп ще не існує. Щоб відфільтрувати вже готові групи за значенням агрегату, використовують `HAVING`.

```sql
-- ❌ Помилка
SELECT assignment_id, COUNT(*) FROM submissions
WHERE COUNT(*) >= 2
GROUP BY assignment_id;
-- ERROR: aggregate functions are not allowed in WHERE

-- ✅ Правильно
SELECT assignment_id, COUNT(*) AS submissions
FROM submissions
GROUP BY assignment_id
HAVING COUNT(*) >= 2
ORDER BY assignment_id;
```

```text
 assignment_id | submissions
---------------+-------------
             1 |           3
             2 |           2
             4 |           2
             6 |           2
```

Завдання 3 (одна здача) відсіяне.

### 3.2. HAVING з JOIN: курси з високою середньою оцінкою

```sql
SELECT c.title, ROUND(AVG(s.score), 2) AS avg_score
FROM submissions s
JOIN assignments a ON a.id = s.assignment_id
JOIN lessons     l ON l.id = a.lesson_id
JOIN courses     c ON c.id = l.course_id
GROUP BY c.id, c.title
HAVING AVG(s.score) >= 80
ORDER BY avg_score DESC;
```

```text
      title      | avg_score
-----------------+-----------
 Python Basics   |     86.25
 QA Fundamentals |     80.00
```

`SQL Basics` із середньою 47.50 відсіяний.

### 3.3. WHERE і HAVING разом

Вони не конкурують: `WHERE` відбирає рядки, `HAVING` відбирає групи. Задача: студенти, які мали щонайменше **дві** оцінки **від 70 і вище**:

```sql
SELECT student_id, COUNT(*) AS good_works
FROM submissions
WHERE score >= 70
GROUP BY student_id
HAVING COUNT(*) >= 2
ORDER BY student_id;
```

```text
 student_id | good_works
------------+------------
          3 |          2
          4 |          2
```

Марія має одну таку роботу, а Софія жодної (її оцінка 50), тому вони не потрапляють у результат.

### 3.4. Правило ефективності

Якщо умова стосується звичайної колонки, а не агрегату, ставте її у `WHERE`, а не в `HAVING`. База відкине зайві рядки до групування і працюватиме швидше:

```sql
-- Працює, але повільніше
GROUP BY course_id HAVING course_id = 1;

-- Краще
WHERE course_id = 1 GROUP BY course_id;
```

### 3.5. Повний порядок виконання запиту

З урахуванням усього вивченого та віконних функцій, які ми розглянемо нижче:

| Крок | Частина запиту |
| ---- | -------------- |
| 1 | `FROM`, `JOIN` |
| 2 | `WHERE` |
| 3 | `GROUP BY` |
| 4 | `HAVING` |
| 5 | віконні функції (`OVER`) |
| 6 | `SELECT` (вирази, псевдоніми) |
| 7 | `DISTINCT`, `DISTINCT ON` |
| 8 | `ORDER BY` |
| 9 | `LIMIT`, `OFFSET` |

Саме тому в `WHERE` і `HAVING` не можна використати псевдонім із `SELECT`, а віконну функцію не можна поставити у `WHERE`.

---

## Частина 4. Вкладені запити (subqueries)

### 4.1. Що це

Вкладений запит це `SELECT` усередині іншого запиту, у круглих дужках. Його можна поставити в чотири місця.

| Де | Що повертає підзапит | Приклад |
| -- | -------------------- | ------- |
| У `WHERE` | одне значення, список значень, або «є/немає» | `price > (SELECT AVG(...))` |
| У `SELECT` | одне значення на кожен рядок | підрахунок уроків курсу |
| У `FROM` | таблицю (тимчасову, з псевдонімом) | агрегація агрегатів |
| У `WITH` (CTE) | іменований проміжний результат | читабельний запит по крокам |

### 4.2. Скалярний підзапит: одне значення

Підзапит, який повертає **одне число**, можна використовувати як звичайне значення. Виконується він один раз.

```sql
-- Курси, дорожчі за середню ціну
SELECT title, price
FROM courses
WHERE price > (SELECT AVG(price) FROM courses)
ORDER BY price DESC;
```

```text
      title      |  price
-----------------+---------
 Python Advanced | 1500.00
 Python Basics   | 1200.00
 SQL Basics      |  900.00
```

Середня ціна 880.00, тому `QA Fundamentals` (800) і `Git Essentials` (0) не потрапили.

Ще приклад: здачі з оцінкою вище за загальну середню (74.29):

```sql
SELECT id, student_id, score
FROM submissions
WHERE score > (SELECT AVG(score) FROM submissions)
ORDER BY score DESC;
-- id 3 (100), id 1 (90), id 4 (85), id 9 (80)
```

Якщо скалярний підзапит поверне більше одного рядка, буде помилка `more than one row returned by a subquery used as an expression`.

### 4.3. Підзапит зі списком: IN та NOT IN

```sql
-- Студенти, які здавали хоча б одну роботу
SELECT id, first_name, last_name
FROM users
WHERE id IN (SELECT student_id FROM submissions)
ORDER BY id;
-- Ірина (3), Андрій (4), Марія (5), Софія (7)

-- Студенти, які не здали жодної роботи
SELECT id, first_name, last_name
FROM users
WHERE role = 'student'
  AND id NOT IN (SELECT student_id FROM submissions);
-- Тарас Гнатюк (6)
```

Небезпека `NOT IN`: якщо підзапит поверне хоча б одне значення `NULL`, умова `NOT IN` не буде істинною ні для кого, і ви отримаєте порожній результат. Колонка `submissions.student_id` оголошена `NOT NULL`, тому тут усе гаразд, але у загальному випадку надійніше використовувати `NOT EXISTS` (наступний пункт).

### 4.4. EXISTS і NOT EXISTS: чи є пов'язані рядки

`EXISTS` перевіряє, чи повертає підзапит хоча б один рядок. Він повертає `TRUE` або `FALSE` і не залежить від `NULL`. Усередині зазвичай пишуть `SELECT 1`, бо самі значення неважливі.

Тут підзапит посилається на зовнішній запит (`c.id`) і виконується для кожного рядка зовнішнього, тому такий підзапит називають **корельованим**.

```sql
-- Курси, у яких є хоча б один урок
SELECT c.id, c.title
FROM courses c
WHERE EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id)
ORDER BY c.id;
-- Python Basics (1), SQL Basics (2), QA Fundamentals (4)

-- Курси без жодного уроку
SELECT c.id, c.title
FROM courses c
WHERE NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id)
ORDER BY c.id;
-- Python Advanced (3), Git Essentials (5)
```

Той самий результат дає `LEFT JOIN ... WHERE ... IS NULL` із заняття 34. Обидва варіанти правильні: `NOT EXISTS` часто читається природніше, `LEFT JOIN` зручніший, коли потрібні й колонки з іншої таблиці.

### 4.5. Підзапит у SELECT

Підзапит у списку колонок повертає одне значення для кожного рядка. Це чистий спосіб порахувати кілька незалежних підсумків без пастки з частини 2.6:

```sql
SELECT
    c.title,
    (SELECT COUNT(*) FROM lessons l
      WHERE l.course_id = c.id)                         AS lessons_count,
    (SELECT COUNT(*) FROM enrollments e
      WHERE e.course_id = c.id AND e.status = 'active') AS active_students
FROM courses c
ORDER BY c.id;
```

```text
      title      | lessons_count | active_students
-----------------+---------------+-----------------
 Python Basics   |             3 |               3
 SQL Basics      |             3 |               2
 Python Advanced |             0 |               0
 QA Fundamentals |             2 |               2
 Git Essentials  |             0 |               0
```

Тепер числа правильні. Мінус такого підходу: підзапит виконується для кожного рядка, тож на великих таблицях `JOIN` із `GROUP BY` може бути швидшим.

### 4.6. Корельований підзапит порівняння: «краще, ніж у середньому по групі»

Задача: здачі, оцінка яких вища за середню оцінку **свого** завдання.

```sql
SELECT s.id, s.assignment_id, s.score
FROM submissions s
WHERE s.score > (
    SELECT AVG(s2.score)
    FROM submissions s2
    WHERE s2.assignment_id = s.assignment_id
)
ORDER BY s.id;
```

```text
 id | assignment_id | score
----+---------------+-------
  1 |             1 |    90
  3 |             1 |   100
  8 |             4 |    50
```

Перевірка: у завдання 1 середня 86.67, і вище неї 90 та 100; у завдання 4 середня 47.50, і вище неї 50. У завдань 2 і 6 єдина оцінена робота дорівнює середній (85 та 80), тож строго вище середньої нічого немає.

### 4.7. Підзапит у FROM: агрегація агрегатів

Підзапит у `FROM` це тимчасова таблиця, яка **обов'язково** має псевдонім. Це єдиний спосіб порахувати «середнє від підсумків»: агрегат не можна вкласти в агрегат.

Задача: яка середня кількість здач на студента (серед тих, хто здавав)?

```sql
SELECT ROUND(AVG(cnt), 2) AS avg_submissions_per_student
FROM (
    SELECT student_id, COUNT(*) AS cnt
    FROM submissions
    GROUP BY student_id
) AS per_student;
```

```text
 avg_submissions_per_student
-----------------------------
                        2.50
```

Внутрішній запит дає 4, 3, 1, 2 здачі для студентів 3, 4, 5, 7, а зовнішній рахує їхнє середнє: 10 / 4 = 2.50.

### 4.8. CTE (WITH): запит по крокам

Коли запит із вкладеннями стає складно читати, його розбивають на іменовані частини через `WITH`. Це називається **CTE** (Common Table Expression). Фактично це підзапит у `FROM`, але з іменем, який визначений зверху і читається як послідовність кроків.

```sql
WITH student_stats AS (
    SELECT
        student_id,
        COUNT(*)               AS submissions,
        ROUND(AVG(score), 2)   AS avg_score
    FROM submissions
    GROUP BY student_id
)
SELECT u.first_name || ' ' || u.last_name AS student,
       ss.submissions,
       ss.avg_score
FROM student_stats ss
JOIN users u ON u.id = ss.student_id
WHERE ss.submissions >= 3
ORDER BY u.id;
```

```text
     student     | submissions | avg_score
-----------------+-------------+-----------
 Ірина Коваль    |           4 |     73.33
 Андрій Мельник  |           3 |     75.00
```

Крок 1 рахує статистику по студентах, крок 2 приєднує імена та фільтрує. CTE також знадобиться нам у частині 6, щоб відфільтрувати за результатом віконної функції.

### 4.9. Підзапит чи JOIN?

| Ситуація | Що краще |
| -------- | -------- |
| Потрібні колонки з іншої таблиці | `JOIN` |
| Лише перевірка наявності чи відсутності | `EXISTS` / `NOT EXISTS` |
| Порівняння з одним числом («вище середнього») | скалярний підзапит |
| Підсумок від підсумків | підзапит у `FROM` або CTE |
| Складний запит, який важко читати | CTE |

---

## Частина 5. DISTINCT та DISTINCT ON

### 5.1. DISTINCT: унікальні рядки

`DISTINCT` залишає в результаті лише унікальні **рядки** (за всіма вибраними колонками):

```sql
SELECT DISTINCT student_id FROM submissions ORDER BY student_id;
-- 3, 4, 5, 7

-- Унікальні комбінації
SELECT DISTINCT teacher_id, is_published FROM courses ORDER BY 1, 2;
```

```text
 teacher_id | is_published
------------+--------------
          1 | t
          2 | f
          2 | t
```

Для `DISTINCT` значення `NULL` вважаються **однаковими**, тому дублікати `NULL` схлопуються в один:

```sql
SELECT DISTINCT score FROM submissions ORDER BY score;
-- 45, 50, 70, 80, 85, 90, 100, NULL  (8 рядків: 7 оцінок і один NULL)
```

`DISTINCT` та `GROUP BY` без агрегатів дають однаковий результат. `DISTINCT` коротший, коли потрібні лише унікальні значення; `GROUP BY` потрібен, щойно з'являються підрахунки.

### 5.2. Проблема: потрібен лише один рядок з кожної групи

Іноді потрібно не унікальні значення, а **один цілий рядок на групу**: остання здача кожного студента, найкраща здача кожного завдання, найновіший запис на кожному курсі. Звичайний `DISTINCT` тут не допоможе, а `GROUP BY` дозволяє брати лише агрегати.

Для цього в PostgreSQL є спеціальна можливість: `DISTINCT ON`.

### 5.3. DISTINCT ON: перший рядок у групі

```sql
SELECT DISTINCT ON (ключ_групи) колонки
FROM таблиця
ORDER BY ключ_групи, колонка_для_вибору_першого;
```

Як це працює: база сортує рядки за `ORDER BY`, а потім для кожного значення `ключ_групи` залишає **перший** рядок. Тож у сортуванні ви самі визначаєте, який рядок вважається «першим».

Остання здача кожного студента:

```sql
SELECT DISTINCT ON (student_id)
    student_id, id AS submission_id, submitted_at, score
FROM submissions
ORDER BY student_id, submitted_at DESC;
```

```text
 student_id | submission_id |    submitted_at     | score
------------+---------------+---------------------+-------
          3 |             7 | 2026-10-12 14:20:00 |    45
          4 |             9 | 2026-10-14 13:00:00 |    80
          5 |             3 | 2026-10-02 09:15:00 |   100
          7 |            10 | 2026-10-15 17:30:00 |
```

Найкраща здача кожного завдання:

```sql
SELECT DISTINCT ON (assignment_id)
    assignment_id, id AS submission_id, student_id, score
FROM submissions
ORDER BY assignment_id, score DESC NULLS LAST, id;
```

```text
 assignment_id | submission_id | student_id | score
---------------+---------------+------------+-------
             1 |             3 |          5 |   100
             2 |             4 |          3 |    85
             3 |             6 |          3 |
             4 |             8 |          7 |    50
             6 |             9 |          4 |    80
```

Для завдання 3 єдина здача не оцінена, тому в `score` порожньо.

### 5.4. Правила DISTINCT ON

1. Вирази в `DISTINCT ON (...)` мають збігатися з **початком** `ORDER BY`. Інакше буде помилка: `SELECT DISTINCT ON expressions must match initial ORDER BY expressions`.
2. Без `ORDER BY` результат непередбачуваний: який рядок вважати першим, база вирішує сама.
3. Додавайте в `ORDER BY` унікальне поле (наприклад, `id`) останнім. Якщо кілька рядків мають однакове значення в критерії вибору, без нього результат може змінюватись між запусками.
4. `DISTINCT ON` це розширення PostgreSQL, його немає у стандарті SQL. В інших СУБД ту саму задачу розв'язують через `ROW_NUMBER()`, який ми розглянемо далі.

---

## Частина 6. Віконні функції та PARTITION BY

### 6.1. Проблема, яку не розв'язує GROUP BY

`GROUP BY` **згортає** рядки: з кількох здач завдання виходить один рядок. Але часто потрібно залишити всі рядки і додати до кожного інформацію про групу. Приклад: показати кожну оцінку поряд із середньою по її завданню та різницею.

З `GROUP BY` це вимагає складного підзапиту (див. 4.6). Із віконною функцією це простий запит:

```sql
SELECT
    id,
    assignment_id,
    score,
    ROUND(AVG(score) OVER (PARTITION BY assignment_id), 2)         AS assignment_avg,
    ROUND(score - AVG(score) OVER (PARTITION BY assignment_id), 2) AS diff
FROM submissions
ORDER BY id;
```

```text
 id | assignment_id | score | assignment_avg |  diff
----+---------------+-------+----------------+--------
  1 |             1 |    90 |          86.67 |   3.33
  2 |             1 |    70 |          86.67 | -16.67
  3 |             1 |   100 |          86.67 |  13.33
  4 |             2 |    85 |          85.00 |   0.00
  5 |             2 |       |          85.00 |
  6 |             3 |       |                |
  7 |             4 |    45 |          47.50 |  -2.50
  8 |             4 |    50 |          47.50 |   2.50
  9 |             6 |    80 |          80.00 |   0.00
 10 |             6 |       |          80.00 |
```

Усі 10 рядків на місці, а до кожного додано середню по завданню та відхилення від неї. Зверніть увагу на рядок 6: у завдання 3 немає жодної оцінки, тож середнє `NULL`.

**Віконна функція** обчислює значення по «вікну», тобто набору пов'язаних рядків, **не зменшуючи кількість рядків** результату.

### 6.2. Синтаксис

```sql
функція(...) OVER (
    PARTITION BY колонки    -- на які групи розбити (необов'язково)
    ORDER BY колонки        -- порядок усередині групи (необов'язково)
    рамка                   -- які рядки групи враховувати (необов'язково)
)
```

- Порожній `OVER ()` означає, що вікно це **вся** таблиця.
- `PARTITION BY` ділить рядки на незалежні вікна, як `GROUP BY`, але без згортання.
- `ORDER BY` у вікні впорядковує рядки всередині кожного вікна. Він потрібен для рейтингів, накопичувальних сум та функцій «попередній/наступний».

| Тип | Функції |
| --- | ------- |
| Агрегатні як віконні | `SUM`, `AVG`, `COUNT`, `MIN`, `MAX` із `OVER` |
| Рейтингові | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE` |
| Зсув | `LAG`, `LEAD` |
| Значення з вікна | `FIRST_VALUE`, `LAST_VALUE` |

### 6.3. PARTITION BY: кілька розрізів в одному запиті

Велика перевага віконних функцій: **у кожної функції може бути своє `PARTITION BY`**. Тоді в одному запиті ми бачимо кілька різних «розрізів» даних. З `GROUP BY` це неможливо.

Покажемо для кожної оціненої здачі середню оцінку студента та середню оцінку завдання:

```sql
SELECT
    id,
    student_id,
    assignment_id,
    score,
    ROUND(AVG(score) OVER (PARTITION BY student_id), 2)    AS student_avg,
    ROUND(AVG(score) OVER (PARTITION BY assignment_id), 2) AS assignment_avg
FROM submissions
WHERE score IS NOT NULL
ORDER BY id;
```

```text
 id | student_id | assignment_id | score | student_avg | assignment_avg
----+------------+---------------+-------+-------------+----------------
  1 |          3 |             1 |    90 |       73.33 |          86.67
  2 |          4 |             1 |    70 |       75.00 |          86.67
  3 |          5 |             1 |   100 |      100.00 |          86.67
  4 |          3 |             2 |    85 |       73.33 |          85.00
  7 |          3 |             4 |    45 |       73.33 |          47.50
  8 |          7 |             4 |    50 |       50.00 |          47.50
  9 |          4 |             6 |    80 |       75.00 |          80.00
```

Тут видно, що роботи Ірини (90, 85, 45) у середньому нижчі за її найкращий результат, а робота Марії (100) вища за середнє по завданню.

Зверніть увагу, що `WHERE score IS NOT NULL` виконується **до** віконних функцій: вікно складається вже з відфільтрованих рядків. Саме тому середнє по завданню 2 тут дорівнює 85.00 (одна оцінена здача).

### 6.4. ORDER BY у вікні: накопичувальні підсумки

Якщо у вікно додати `ORDER BY`, агрегат рахується наростаючим підсумком: від першого рядка вікна до поточного.

Накопичувальна сума балів студента в хронологічному порядку:

```sql
SELECT
    student_id,
    id,
    submitted_at::date AS day,
    score,
    SUM(score) OVER (
        PARTITION BY student_id
        ORDER BY submitted_at
    ) AS running_sum
FROM submissions
ORDER BY student_id, submitted_at;
```

```text
 student_id | id |    day     | score | running_sum
------------+----+------------+-------+-------------
          3 |  1 | 2026-10-01 |    90 |          90
          3 |  4 | 2026-10-08 |    85 |         175
          3 |  6 | 2026-10-10 |       |         175
          3 |  7 | 2026-10-12 |    45 |         220
          4 |  2 | 2026-10-02 |    70 |          70
          4 |  5 | 2026-10-09 |       |          70
          4 |  9 | 2026-10-14 |    80 |         150
          5 |  3 | 2026-10-02 |   100 |         100
          7 |  8 | 2026-10-13 |    50 |          50
          7 | 10 | 2026-10-15 |       |          50
```

Запис `submitted_at::date` перетворює час на дату. Неоцінені роботи (`NULL`) не змінюють суму.

**Рамка вікна.** Коли в `OVER` є `ORDER BY`, за замовчуванням рахуються рядки від початку вікна до поточного, **разом із рядками з тим самим значенням `ORDER BY`**. Якщо в нас можуть бути однакові значення (наприклад, дві здачі в одну секунду), накопичувальна сума для них збігатиметься. Щоб рахувати суворо по рядках, вказують рамку явно:

```sql
SUM(score) OVER (
    PARTITION BY student_id
    ORDER BY submitted_at, id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

Рамкою можна задати й ковзне вікно, наприклад середнє з поточної та попередньої оцінки: `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW`.

### 6.5. Рейтингові функції: ROW_NUMBER, RANK, DENSE_RANK

| Функція | Що робить при однакових значеннях |
| ------- | --------------------------------- |
| `ROW_NUMBER()` | нумерує рядки 1, 2, 3, 4... завжди без повторів |
| `RANK()` | однакові значення мають однакове місце, наступне місце **пропускається** (1, 2, 2, 4) |
| `DENSE_RANK()` | однакові значення мають однакове місце, без пропусків (1, 2, 2, 3) |

У нашій таблиці `submissions` немає однакових оцінок, тому наочно покажемо різницю на невеликому наборі значень, створеному прямо в запиті через `VALUES`:

```sql
SELECT
    score,
    ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num,
    RANK()       OVER (ORDER BY score DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM (VALUES (100), (90), (90), (80)) AS t(score);
```

```text
 score | row_num | rank | dense_rank
-------+---------+------+------------
   100 |       1 |    1 |          1
    90 |       2 |    2 |          2
    90 |       3 |    2 |          2
    80 |       4 |    4 |          3
```

Тепер рейтинг студентів **усередині кожного завдання**: це поєднання `PARTITION BY` з рейтинговою функцією.

```sql
SELECT
    assignment_id,
    student_id,
    score,
    RANK() OVER (
        PARTITION BY assignment_id
        ORDER BY score DESC NULLS LAST
    ) AS place
FROM submissions
ORDER BY assignment_id, place, student_id;
```

```text
 assignment_id | student_id | score | place
---------------+------------+-------+-------
             1 |          5 |   100 |     1
             1 |          3 |    90 |     2
             1 |          4 |    70 |     3
             2 |          3 |    85 |     1
             2 |          4 |       |     2
             3 |          3 |       |     1
             4 |          7 |    50 |     1
             4 |          3 |    45 |     2
             6 |          4 |    80 |     1
             6 |          7 |       |     2
```

Нумерація починається знову для кожного завдання: це і є `PARTITION BY`.

### 6.6. Топ-N у кожній групі

Віконну функцію не можна поставити в `WHERE` (вона обчислюється пізніше), тому для фільтрації за місцем використовують CTE або підзапит:

```sql
WITH ranked AS (
    SELECT
        assignment_id,
        student_id,
        score,
        RANK() OVER (
            PARTITION BY assignment_id
            ORDER BY score DESC
        ) AS place
    FROM submissions
    WHERE score IS NOT NULL
)
SELECT assignment_id, student_id, score
FROM ranked
WHERE place = 1
ORDER BY assignment_id;
```

```text
 assignment_id | student_id | score
---------------+------------+-------
             1 |          5 |   100
             2 |          3 |    85
             4 |          7 |    50
             6 |          4 |    80
```

Це той самий результат, що ми отримали через `DISTINCT ON` у 5.3 (тільки без неоціненого завдання 3, бо ми їх відфільтрували). Чим вони відрізняються:

| | `DISTINCT ON` | `ROW_NUMBER()` / `RANK()` |
| - | ------------- | ------------------------- |
| Складність | коротший запис | потрібен CTE або підзапит |
| Топ-1 на групу | так | так |
| Топ-3 на групу | ні | так (`WHERE place <= 3`) |
| Переносимість | лише PostgreSQL | стандарт SQL |
| Рівні місця | вибирає один рядок | `RANK` залишає всі рівні (кілька переможців), `ROW_NUMBER` рівно один |

### 6.7. LAG і LEAD: сусідні рядки

`LAG(колонка)` повертає значення з **попереднього** рядка вікна, `LEAD(колонка)` з **наступного**. Для першого рядка (у `LAG`) чи останнього (у `LEAD`) результат `NULL`.

Задача: як змінювалася оцінка студента від роботи до роботи?

```sql
SELECT
    student_id,
    id,
    score,
    LAG(score) OVER w          AS prev_score,
    score - LAG(score) OVER w  AS change
FROM submissions
WHERE score IS NOT NULL
WINDOW w AS (PARTITION BY student_id ORDER BY submitted_at)
ORDER BY student_id, submitted_at;
```

```text
 student_id | id | score | prev_score | change
------------+----+-------+------------+--------
          3 |  1 |    90 |            |
          3 |  4 |    85 |         90 |     -5
          3 |  7 |    45 |         85 |    -40
          4 |  2 |    70 |            |
          4 |  9 |    80 |         70 |     10
          5 |  3 |   100 |            |
          7 |  8 |    50 |            |
```

Тут використано **іменоване вікно**: опис `PARTITION BY ... ORDER BY ...` винесено в розділ `WINDOW w AS (...)`, а в функціях написано просто `OVER w`. Це зручно, коли те саме вікно потрібне кілька разів.

Так ми одразу бачимо, що в Ірини оцінки погіршуються (-5, потім -40), а в Андрія покращуються (+10).

### 6.8. Корисні правила для віконних функцій

1. **Порядок виконання:** віконні функції обчислюються після `WHERE`, `GROUP BY` та `HAVING`. Тому `WHERE` впливає на вікно (див. 6.3), а в `WHERE` саму функцію використати не можна, тільки через CTE чи підзапит.
2. **Віконні й агрегатні разом:** можна використовувати віконну функцію над результатом `GROUP BY`, наприклад `RANK() OVER (ORDER BY SUM(score) DESC)` для рейтингу студентів за сумою балів.
3. **Завжди додавайте унікальний ключ** в `ORDER BY` вікна, якщо порядок рівних значень важливий.
4. **GROUP BY чи вікно?** Потрібен один рядок на групу: `GROUP BY`. Потрібно залишити всі рядки та додати до них підсумок групи або рейтинг: віконна функція.

Приклад поєднання з пункту 2: рейтинг студентів за сумою балів.

```sql
SELECT
    u.first_name || ' ' || u.last_name AS student,
    SUM(s.score)                        AS total_score,
    RANK() OVER (ORDER BY SUM(s.score) DESC) AS place
FROM submissions s
JOIN users u ON u.id = s.student_id
GROUP BY u.id, u.first_name, u.last_name
ORDER BY place;
```

```text
     student     | total_score | place
-----------------+-------------+-------
 Ірина Коваль    |         220 |     1
 Андрій Мельник  |         150 |     2
 Марія Бондар    |         100 |     3
 Софія Лисенко   |          50 |     4
```

---

## Частина 7. VIEW: представлення

### 7.1. Що таке VIEW

**VIEW** (представлення) це **збережений запит із ім'ям**. Дані у ньому не копіюються: щоразу, коли ви звертаєтесь до `VIEW`, PostgreSQL виконує збережений запит заново і повертає актуальні дані. Для користувача представлення виглядає як звичайна таблиця.

Навіщо воно потрібне:

- **Повторне використання.** Складний запит із п'ятьма JOIN-ами пишеться один раз, а далі використовується як `SELECT * FROM v_gradebook`.
- **Зрозумілі імена.** Замість того, щоб кожного разу пам'ятати шлях `submissions` → `assignments` → `lessons` → `courses`, є готовий журнал.
- **Стабільний інтерфейс.** Застосунок працює з `VIEW`, і якщо структура таблиць змінюється, достатньо оновити `VIEW`, не чіпаючи код.
- **Безпека.** `VIEW` може показувати лише частину колонок чи рядків, наприклад без телефонів і пошти.

### 7.2. Створення і використання

Синтаксис:

```sql
CREATE VIEW view_name AS
SELECT ...;
```

**Перший приклад: огляд курсів.** Збираємо запит із підзапитами з частини 4.5 і додаємо викладача.

```sql
CREATE VIEW v_course_overview AS
SELECT
    c.id    AS course_id,
    c.title,
    c.price,
    c.is_published,
    t.first_name || ' ' || t.last_name AS teacher,
    (SELECT COUNT(*) FROM lessons l
      WHERE l.course_id = c.id)                         AS lessons_count,
    (SELECT COUNT(*) FROM enrollments e
      WHERE e.course_id = c.id AND e.status = 'active') AS active_students
FROM courses c
JOIN users t ON t.id = c.teacher_id;
```

Тепер звертаємось до нього як до таблиці:

```sql
SELECT * FROM v_course_overview ORDER BY course_id;
```

```text
 course_id |      title      |  price  | is_published |    teacher     | lessons_count | active_students
-----------+-----------------+---------+--------------+----------------+---------------+-----------------
         1 | Python Basics   | 1200.00 | t            | Петро Іваненко |             3 |               3
         2 | SQL Basics      |  900.00 | t            | Петро Іваненко |             3 |               2
         3 | Python Advanced | 1500.00 | f            | Олена Шевченко |             0 |               0
         4 | QA Fundamentals |  800.00 | t            | Олена Шевченко |             2 |               2
         5 | Git Essentials  |    0.00 | t            | Олена Шевченко |             0 |               0
```

До `VIEW` можна застосовувати `WHERE`, `ORDER BY`, `JOIN`, `GROUP BY`, як до будь-якої таблиці:

```sql
-- Опубліковані курси, де щонайменше двоє активних студентів
SELECT title, teacher, active_students
FROM v_course_overview
WHERE is_published AND active_students >= 2
ORDER BY title;
-- Python Basics (3), QA Fundamentals (2), SQL Basics (2)
```

**Другий приклад: журнал оцінок.** Це запит із п'ятьма таблицями з заняття 34, який тепер пишемо один раз.

```sql
CREATE VIEW v_gradebook AS
SELECT
    s.id                                  AS submission_id,
    st.id                                 AS student_id,
    st.first_name || ' ' || st.last_name  AS student,
    c.id                                  AS course_id,
    c.title                               AS course,
    a.title                               AS assignment,
    s.score,
    a.max_score,
    ROUND(100.0 * s.score / a.max_score, 1) AS percent,
    s.submitted_at
FROM submissions s
JOIN users       st ON st.id = s.student_id
JOIN assignments a  ON a.id  = s.assignment_id
JOIN lessons     l  ON l.id  = a.lesson_id
JOIN courses     c  ON c.id  = l.course_id;
```

Тепер навіть складні питання стають короткими:

```sql
-- Журнал однієї студентки
SELECT course, assignment, score, max_score, percent
FROM v_gradebook
WHERE student = 'Ірина Коваль'
ORDER BY submitted_at;
```

```text
     course    |     assignment      | score | max_score | percent
---------------+---------------------+-------+-----------+---------
 Python Basics | Hello, Python       |    90 |       100 |    90.0
 Python Basics | Цикли               |    85 |       100 |    85.0
 Python Basics | Функція-калькулятор |       |       100 |
 SQL Basics    | Перші запити        |    45 |        50 |    90.0
```

```sql
-- Середній відсоток по курсах: агрегація поверх VIEW
SELECT course, ROUND(AVG(percent), 1) AS avg_percent
FROM v_gradebook
GROUP BY course
ORDER BY course;
```

```text
      course      | avg_percent
-----------------+-------------
 Python Basics   |        86.3
 QA Fundamentals |        80.0
 SQL Basics      |        95.0
```

Зверніть увагу: `avg_percent` рахується від відсотків окремих робіт, а не від суми балів, тому для `SQL Basics` це 95.0 (середнє від 90.0 та 100.0), а не 47.50 з абсолютних балів. Ці числа відповідають на різні питання.

### 7.3. Керування представленнями

| Задача | Команда |
| ------ | ------- |
| Список представлень у `psql` | `\dv` |
| Подивитись визначення | `\d+ v_course_overview` або `SELECT pg_get_viewdef('v_course_overview', true);` |
| Замінити запит | `CREATE OR REPLACE VIEW ...` |
| Видалити | `DROP VIEW IF EXISTS v_course_overview;` |

Обмеження `CREATE OR REPLACE VIEW`: можна змінити сам запит і **додати нові колонки в кінець**, але не можна змінити імена, порядок чи типи наявних колонок. Для такої зміни представлення видаляють і створюють заново.

### 7.4. VIEW і залежності: оновлюємо скрипт

Представлення залежить від таблиць, з яких воно читає. Тому видалити таблицю, на яку посилається `VIEW`, не вийде:

```text
ERROR:  cannot drop table courses because other objects depend on it
DETAIL: view v_course_overview depends on table courses
```

Це означає, що у `schema.sql` представлення потрібно видаляти **до** таблиць (так само, як ми видаляємо залежні таблиці першими):

```sql
-- На початку schema.sql
DROP VIEW IF EXISTS v_gradebook;
DROP VIEW IF EXISTS v_course_overview;

DROP TABLE IF EXISTS submissions;
-- ... далі як раніше
```

А `CREATE VIEW` ставимо в самому кінці скрипта, після створення таблиць. Якщо одне представлення читає з іншого, видаляти їх треба у зворотному порядку створення.

### 7.5. ORDER BY і VIEW

Не додавайте `ORDER BY` усередину `VIEW` без потреби: сортування краще задавати в запиті, який звертається до `VIEW`, адже в кожному місці воно може бути потрібне різне. Виняток це `ORDER BY` разом із `LIMIT` (наприклад, «топ-10»), де порядок є частиною результату.

### 7.6. Безпека: показати лише частину даних

Припустимо, застосунку потрібно показувати список викладачів, але без пошти й телефону. Створимо представлення лише з потрібними колонками:

```sql
CREATE VIEW v_teachers_public AS
SELECT id, first_name, last_name
FROM users
WHERE role = 'teacher';
```

Доступ видають командою `GRANT`:

```sql
GRANT SELECT ON v_teachers_public TO app_reader;   -- app_reader: роль застосунку
```

Тоді застосунок бачить лише ці три колонки та лише викладачів. Ролі та права доступу детально вивчатимуться окремо, поки достатньо знати, що `VIEW` це інструмент обмеження видимості даних. Важливо: `VIEW` **сам по собі** не захищає, якщо користувач має прямий доступ до таблиці `users`.

### 7.7. Оновлення даних через VIEW

Прості представлення, які читають **одну таблицю** без агрегатів, `DISTINCT`, `GROUP BY` та віконних функцій, PostgreSQL дозволяє оновлювати: `INSERT`, `UPDATE` і `DELETE` проходять до базової таблиці. Складні представлення (з JOIN-ами, агрегатами) для запису не призначені.

Опція `WITH CHECK OPTION` не дозволяє через `VIEW` зробити рядок, який перестане в нього потрапляти:

```sql
CREATE VIEW v_published_courses AS
SELECT id, title, price, teacher_id, is_published
FROM courses
WHERE is_published = TRUE
WITH CHECK OPTION;
```

Виконайте перевірку всередині транзакції, щоб не змінити реальні дані:

```sql
BEGIN;

-- ✅ Працює: курс залишається опублікованим, змінюється таблиця courses
UPDATE v_published_courses SET price = 1000 WHERE id = 2;

-- ❌ Помилка: після зміни рядок вийшов би за межі VIEW
UPDATE v_published_courses SET is_published = FALSE WHERE id = 2;
-- ERROR: new row violates check option for view "v_published_courses"

ROLLBACK;
```

### 7.8. MATERIALIZED VIEW: збережений результат

Звичайний `VIEW` щоразу виконує запит. Якщо запит дуже важкий, а свіжі дані щосекунди не потрібні, використовують **матеріалізоване представлення**: PostgreSQL зберігає результат запиту як таблицю, а оновлюється воно лише за командою.

```sql
CREATE MATERIALIZED VIEW mv_course_scores AS
SELECT
    course_id,
    course,
    COUNT(score)            AS graded,
    ROUND(AVG(score), 2)    AS avg_score
FROM v_gradebook
GROUP BY course_id, course;

SELECT * FROM mv_course_scores ORDER BY course_id;
```

```text
 course_id |      course      | graded | avg_score
-----------+------------------+--------+-----------
         1 | Python Basics    |      4 |     86.25
         2 | SQL Basics       |      2 |     47.50
         4 | QA Fundamentals  |      1 |     80.00
```

Оновити збережений результат після зміни даних:

```sql
REFRESH MATERIALIZED VIEW mv_course_scores;
```

| | `VIEW` | `MATERIALIZED VIEW` |
| - | ------ | ------------------- |
| Зберігає дані | ні, виконує запит щоразу | так, фізично |
| Актуальність | завжди свіжі дані | на момент останнього `REFRESH` |
| Швидкість читання | як у запиту всередині | швидко, як у таблиці |
| Індекси | немає | можна створювати |
| Типове використання | зручність і безпека | важкі звіти, дашборди |

У схему тепер додається ще одне правило видалення: матеріалізоване представлення, яке читає з `v_gradebook`, видаляємо **першим**: `DROP MATERIALIZED VIEW IF EXISTS mv_course_scores;`.

### 7.9. Використання з Python

Для застосунку `VIEW` виглядає як звичайна таблиця. Складний запит із п'ятьма JOIN-ами перетворюється на короткий:

```python
import psycopg

DSN = "postgresql://postgres:password@localhost:5432/lms"

def get_student_gradebook(student_id: int):
    """Журнал оцінок студента, беремо готові дані з VIEW."""
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT course, assignment, score, max_score, percent
                   FROM v_gradebook
                   WHERE student_id = %s
                   ORDER BY submitted_at;""",
                (student_id,),
            )
            return cur.fetchall()

for course, assignment, score, max_score, percent in get_student_gradebook(3):
    print(f"{course} / {assignment}: {score}/{max_score} ({percent}%)")
```

### 7.10. Поради щодо іменування та використання

- Давайте представленням префікс `v_` (а матеріалізованим `mv_`), щоб одразу відрізняти їх від таблиць.
- Не будуйте довгі ланцюжки «представлення з представлень»: їх важко налагоджувати, а PostgreSQL розгортає їх у один великий запит.
- Явно перелічуйте колонки (без `SELECT *`): якщо в таблицю додадуть колонку, `VIEW` не змінить склад колонок несподівано.
- Зберігайте `CREATE VIEW` у скрипті разом зі структурою БД, а не лише в базі.

---

## Частина 8. Типові помилки

| Помилка | Що відбувається | Як правильно |
| ------- | --------------- | ------------ |
| Колонка в `SELECT` без `GROUP BY` | `must appear in the GROUP BY clause` | додати в `GROUP BY` або обгорнути в агрегат |
| Агрегат у `WHERE` | `aggregate functions are not allowed in WHERE` | умова на агрегат у `HAVING` |
| Звичайна умова в `HAVING` | працює, але повільно | звичайні умови у `WHERE` |
| `COUNT(*)` після `LEFT JOIN` | курс без студентів дає `1` | `COUNT(права_таблиця.id)` |
| Два JOIN-и «один до багатьох» у `GROUP BY` | завищені підсумки | `COUNT(DISTINCT ...)` або підзапити |
| Не врахували `NULL` в `AVG` | середнє тільки по заповнених значеннях | свідомо вирішити, чи рахувати `NULL` нулем |
| `SUM` на порожньому наборі | `NULL` замість `0` | `COALESCE(SUM(...), 0)` |
| `NOT IN` з підзапитом, що може повернути `NULL` | порожній результат | `NOT EXISTS` |
| Скалярний підзапит повернув кілька рядків | `more than one row returned` | уточнити умову або агрегувати |
| Підзапит у `FROM` без псевдоніма | `subquery in FROM must have an alias` | `... ) AS name` |
| `DISTINCT ON` не збігається з `ORDER BY` | помилка `must match initial ORDER BY` | почати `ORDER BY` з тих самих виразів |
| Віконна функція у `WHERE` | `window functions are not allowed in WHERE` | CTE або підзапит |
| Накопичувальна сума без унікального ключа в `ORDER BY` | однакові суми для рівних значень | додати `id` до `ORDER BY` вікна |
| Видалення таблиці, від якої залежить `VIEW` | `other objects depend on it` | спочатку видалити `VIEW` |
| Застарілі дані в `MATERIALIZED VIEW` | показує старий стан | `REFRESH MATERIALIZED VIEW` |

---

## Практичні завдання

Усі запити зберігайте у файлі `aggregation_practice.sql`. Над кожним пишіть коментарем номер завдання. Відповіді для самоперевірки наведені нижче.

### Рівень 1. Агрегати, GROUP BY, HAVING

1. Скільки всього користувачів, студентів і викладачів. Виведіть кількість за кожною роллю.
2. Мінімальна, максимальна й середня ціна курсів.
3. Кількість здач на кожне завдання.
4. Для кожного студента (ім'я та прізвище): кількість здач і середня оцінка. Залишіть лише студентів, які здали щонайменше 2 роботи. Сортуйте за кількістю здач за спаданням.
5. Для кожного завдання виведіть кількість оцінених і неоцінених здач (використайте `FILTER`).
6. Кількість активних записів на кожен курс. Залишіть лише курси, де їх не менше двох.
7. Для кожного викладача (включно з тими, у кого немає курсів): кількість курсів і сума цін курсів (0, якщо курсів немає).

### Рівень 2. Вкладені запити та DISTINCT

8. Курси, дорожчі за середню ціну.
9. Студенти, які не здали жодної роботи (`NOT EXISTS`).
10. Курси, у яких є хоча б одне завдання (`EXISTS`, шлях через `lessons` та `assignments`).
11. Здачі з оцінкою вищою за середню по своєму завданню (корельований підзапит).
12. Середня кількість здач на студента (серед тих, хто здавав), підзапит у `FROM`.
13. Унікальні пари «викладач, опубліковано» з таблиці `courses`.
14. Остання здача кожного студента (`DISTINCT ON`).
15. Найкраща здача кожного завдання (`DISTINCT ON`, `NULL` в кінці).

### Рівень 3. Віконні функції

16. Усі здачі з середньою оцінкою завдання та відхиленням від неї.
17. Для кожного завдання місце студента серед оцінених робіт (`RANK`). Залишіть лише першу позицію.
18. Накопичувальна сума балів кожного студента за часом здачі.
19. Для кожної оціненої здачі: попередня оцінка того ж студента (`LAG`) і зміна.
20. Порядковий номер здачі кожного студента за часом (`ROW_NUMBER`). Виведіть студентів, які мають четверту здачу.

### Рівень 4. VIEW

21. Створіть `v_student_progress` (студент, курс, кількість оцінених робіт, середня оцінка) на основі `v_gradebook`. Скільки в ньому рядків?
22. На основі `v_course_overview` знайдіть курси без жодного активного студента.
23. Створіть `v_pending_review` (здачі без оцінки: id здачі, `teacher_id`, студент, курс, завдання, час здачі). Виберіть із неї роботи, що чекають на перевірку викладача Петра (id 1).
24. Створіть `mv_course_scores`. Потім змініть оцінку здачі 5 на 60, перегляньте `v_gradebook` і `mv_course_scores`, виконайте `REFRESH` і порівняйте. Усередині транзакції з `ROLLBACK`, щоб повернути дані.

### Рівень 5. Власний проєкт

25. Для своєї БД напишіть: 3 запити з `GROUP BY`/`HAVING`, 2 з підзапитами (один корельований), 1 з `DISTINCT ON`, 2 з віконними функціями, та створіть 2 представлення, які спрощують найчастіші запити.
26. До кожного запиту напишіть коментарем питання, на яке він відповідає, і приблизну кількість рядків у результаті.

---

## Відповіді для самоперевірки

| № | Очікуваний результат |
| - | -------------------- |
| 1 | `student` 5, `teacher` 3 (разом 8) |
| 2 | мін. 0.00, макс. 1500.00, середня 880.00 |
| 3 | завдання 1: 3, 2: 2, 3: 1, 4: 2, 6: 2 |
| 4 | Ірина Коваль 4 (73.33), Андрій Мельник 3 (75.00), Софія Лисенко 2 (50.00); Марія відсіяна |
| 5 | завдання 1: 3 оцінених, 0 ні; 2: 1 і 1; 3: 0 і 1; 4: 2 і 0; 6: 1 і 1 |
| 6 | Python Basics 3, SQL Basics 2, QA Fundamentals 2 |
| 7 | Петро: 2 курси, 2100.00; Олена: 3 курси, 2300.00; Василь: 0 курсів, 0.00 |
| 8 | Python Basics, SQL Basics, Python Advanced |
| 9 | Тарас Гнатюк |
| 10 | Python Basics, SQL Basics, QA Fundamentals |
| 11 | здачі 1, 3, 8 |
| 12 | 2.50 |
| 13 | (1, `t`), (2, `f`), (2, `t`) |
| 14 | студент 3: здача 7; студент 4: здача 9; студент 5: здача 3; студент 7: здача 10 |
| 15 | завдання 1: здача 3 (100); 2: здача 4 (85); 3: здача 6 (`NULL`); 4: здача 8 (50); 6: здача 9 (80) |
| 16 | 10 рядків (див. частину 6.1) |
| 17 | 4 рядки: (завдання 1, студент 5, 100), (2, 3, 85), (4, 7, 50), (6, 4, 80) |
| 18 | підсумкові суми: студент 3: 220, студент 4: 150, студент 5: 100, студент 7: 50 (див. частину 6.4) |
| 19 | 7 рядків; зміни: Ірина -5 та -40, Андрій +10; в інших `prev_score` дорівнює `NULL` |
| 20 | четверту здачу має лише Ірина (студент 3); найбільші номери: Ірина 4, Андрій 3, Софія 2, Марія 1 |
| 21 | 7 рядків: Ірина (Python Basics: 2 оцінених, 87.50; SQL Basics: 1, 45.00), Андрій (Python Basics: 1, 70.00; QA Fundamentals: 1, 80.00), Марія (Python Basics: 1, 100.00), Софія (SQL Basics: 1, 50.00; QA Fundamentals: 0, `NULL`) |
| 22 | Python Advanced, Git Essentials |
| 23 | 2 рядки: здача 5 (Андрій Мельник, Python Basics, Цикли) та здача 6 (Ірина Коваль, Python Basics, Функція-калькулятор) |
| 24 | після зміни `v_gradebook` одразу показує оцінку 60 для здачі 5; `mv_course_scores` до `REFRESH` лишається старою (Python Basics: 4 оцінених, 86.25), після `REFRESH` стає 5 оцінених і середня 81.00 |

Підказки до складніших завдань:

- **Завдання 7:** потрібні `LEFT JOIN` від `users` (з умовою `role = 'teacher'`), `COUNT(c.id)` та `COALESCE(SUM(c.price), 0)`.
- **Завдання 17:** спочатку відфільтруйте `NULL`-оцінки, порахуйте місце у CTE, потім залиште `place = 1` у зовнішньому запиті.
- **Завдання 20:** `ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY submitted_at)` у CTE, потім `WHERE row_num = 4`.
- **Завдання 21:** групуйте за `student_id, student, course_id, course` і рахуйте `COUNT(score)` та `ROUND(AVG(score), 2)`.
- **Завдання 24:** після зміни оцінки на 60 у `Python Basics` стає 5 оцінених робіт із сумою 90 + 70 + 100 + 85 + 60 = 405, а це дає середню 81.00.

---

## Підсумок

На цьому занятті ми навчилися перетворювати рядки на відповіді:

- Агрегатні функції (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STRING_AGG`) стискають набір рядків в одне значення, а `NULL` вони ігнорують
- `GROUP BY` рахує підсумки окремо для кожної групи; кожна колонка у `SELECT` має бути в групуванні або в агрегаті
- `HAVING` відбирає групи за агрегатом, а `WHERE` відбирає рядки до групування
- Вкладені запити бувають скалярні, зі списком, корельовані, з `EXISTS`, у `FROM`; CTE (`WITH`) робить складні запити читабельними
- `DISTINCT` прибирає дублікати, а `DISTINCT ON` залишає перший рядок кожної групи
- Віконні функції (`OVER`, `PARTITION BY`, `ORDER BY`) додають підсумки та рейтинги, не згортаючи рядки: `RANK`, `ROW_NUMBER`, накопичувальні суми, `LAG`/`LEAD`
- `VIEW` зберігає запит під іменем, спрощує код і обмежує видимість даних; `MATERIALIZED VIEW` зберігає результат і оновлюється через `REFRESH`

Із цими інструментами ви можете будувати повноцінні звіти: від успішності студентів до виручки курсів.

## Питання для самоперевірки

1. Яка різниця між `COUNT(*)`, `COUNT(колонка)` і `COUNT(DISTINCT колонка)`?
2. Як агрегатні функції поводяться з `NULL`? Чим відрізняються `AVG(score)` та `AVG(COALESCE(score, 0))`?
3. Чому кожна колонка в `SELECT` має бути в `GROUP BY` або в агрегаті?
4. Чим `WHERE` відрізняється від `HAVING`? Чому агрегат не можна вживати у `WHERE`?
5. Чому два `LEFT JOIN`-и «один до багатьох» дають завищені підсумки і як цьому запобігти?
6. Чим скалярний підзапит відрізняється від підзапиту зі списком? Що таке корельований підзапит?
7. Чому `NOT EXISTS` надійніший за `NOT IN`?
8. Для чого потрібен підзапит у `FROM` і чому він має псевдонім? Чим CTE кращий?
9. Що робить `DISTINCT ON` і чому його `ORDER BY` має збігатися з початком виразу?
10. Чим віконна функція відрізняється від `GROUP BY`?
11. Що робить `PARTITION BY`? Чим цей підхід відрізняється від групування?
12. Чим відрізняються `ROW_NUMBER`, `RANK` і `DENSE_RANK` при однакових значеннях?
13. Чому віконну функцію не можна використати у `WHERE` і як це обійти?
14. Що таке `VIEW` і які його переваги? Чи зберігає він дані?
15. Чому представлення потрібно видаляти до таблиць?
16. Коли використовувати `MATERIALIZED VIEW`, і що потрібно робити, щоб оновити його дані?

## Корисні посилання

- Агрегатні функції: https://www.postgresql.org/docs/current/functions-aggregate.html
- GROUP BY та HAVING: https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP
- Підзапити та вирази (`EXISTS`, `IN`): https://www.postgresql.org/docs/current/functions-subquery.html
- WITH-запити (CTE): https://www.postgresql.org/docs/current/queries-with.html
- DISTINCT та DISTINCT ON: https://www.postgresql.org/docs/current/sql-select.html#SQL-DISTINCT
- Віконні функції (вступ): https://www.postgresql.org/docs/current/tutorial-window.html
- Список віконних функцій: https://www.postgresql.org/docs/current/functions-window.html
- CREATE VIEW: https://www.postgresql.org/docs/current/sql-createview.html
- Матеріалізовані представлення: https://www.postgresql.org/docs/current/sql-creatematerializedview.html

