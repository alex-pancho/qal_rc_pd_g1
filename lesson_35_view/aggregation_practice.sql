#1. Скільки всього користувачів, студентів і викладачів. Виведіть кількість за кожною роллю.

SELECT
    role,
    COUNT(*) AS users_count
FROM users
GROUP BY role
HAVING COUNT(*) > 0
ORDER BY role;
role 
  |users_count|
-------+-----------+
student|          5|
teacher|          3|

#2. Мінімальна, максимальна й середня ціна курсів.

SELECT
    MIN(price) AS min_price,
    MAX(price) AS max_price,
    AVG(price) AS avg_price
FROM courses;
min_price|max_price|avg_price|
---------+---------+---------+
     0.00|  1500.00|   880.00|

#3. Кількість здач на кожне завдання.
SELECT
    a.id AS assignment_id,
    a.title AS assignment_title,
    COUNT(s.id) AS submissions_count
FROM assignments a
LEFT JOIN submissions s
    ON a.id = s.assignment_id
GROUP BY a.id, a.title
ORDER BY a.id;

assignment_id|assignment_title   |submissions_count|
-------------+-------------------+-----------------+
            1|Hello, Python      |                3|
            2|Цикли              |                2|
            3|Функція-калькулятор|                1|
            4|Перші запити       |                2|
            5|Запити з JOIN      |                0|
            6|Тест-кейс для форми|                2|

#5. Для кожного завдання виведіть кількість оцінених і неоцінених здач (використайте `FILTER`).
SELECT
    a.id AS assignment_id,
    a.title AS assignment_title,

    COUNT(s.id) FILTER (WHERE s.score IS NOT NULL)
        AS graded_submissions,

    COUNT(s.id) FILTER (WHERE s.score IS NULL)
        AS ungraded_submissions

FROM assignments a
LEFT JOIN submissions s
    ON a.id = s.assignment_id

GROUP BY a.id, a.title
ORDER BY a.id;

assignment_id|assignment_title   |graded_submissions|ungraded_submissions|
-------------+-------------------+------------------+--------------------+
            1|Hello, Python      |                 3|                   0|
            2|Цикли              |                 1|                   1|
            3|Функція-калькулятор|                 0|                   1|
            4|Перші запити       |                 2|                   0|
            5|Запити з JOIN      |                 0|                   0|
            6|Тест-кейс для форми|                 1|                   1|

6. Кількість активних записів на кожен курс. Залишіть лише курси, де їх не менше двох.
SELECT
    c.id AS course_id,
    c.title AS course_title,
    COUNT(e.user_id) AS active_enrollments
FROM courses c
JOIN enrollments e
    ON c.id = e.course_id
WHERE e.status = 'active'
GROUP BY c.id, c.title
HAVING COUNT(e.user_id) >= 2
ORDER BY c.id;
course_id|course_title   |active_enrollments|
---------+---------------+------------------+
        1|Python Basics  |                 3|
        2|SQL Basics     |                 2|
        4|QA Fundamentals|                 2|

7. Для кожного викладача (включно з тими, у кого немає курсів): кількість курсів і сума цін курсів (0, якщо курсів немає).
SELECT
    u.id AS teacher_id,
    u.first_name,
    u.last_name,
    COUNT(c.id) AS courses_count,
    COALESCE(SUM(c.price), 0) AS total_course_price
FROM users u
LEFT JOIN courses c
    ON u.id = c.teacher_id
WHERE u.role = 'teacher'
GROUP BY u.id, u.first_name, u.last_name
ORDER BY u.id;

teacher_id|first_name|last_name|courses_count|total_course_price|
----------+----------+---------+-------------+------------------+
         1|Петро     |Іваненко |            2|           2100.00|
         2|Олена     |Шевченко |            3|           2300.00|
         8|Василь    |Кравець  |            0|                 0|

#Рівень 2. Вкладені запити таDISTINCT

8. Курси, дорожчі за середню ціну.

SELECT
    id,
    title,
    price
FROM courses
WHERE price > (
    SELECT AVG(price)
    FROM courses
)
ORDER BY price DESC;
id|title          |price  |
--+---------------+-------+
 3|Python Advanced|1500.00|
 1|Python Basics  |1200.00|
 2|SQL Basics     | 900.00|

Студенти, які не здали жодної роботи (`NOT EXISTS`).
SELECT
    u.id,
    u.first_name,
    u.last_name,
    u.email
FROM users u
WHERE u.role = 'student'
AND NOT EXISTS (
    SELECT 1
    FROM submissions s
    WHERE s.student_id = u.id
)
ORDER BY u.id;

id|first_name|last_name|email         |
--+----------+---------+--------------+
 6|Тарас     |Гнатюк   |taras@mail.com|

10. Курси, у яких є хоча б одне завдання (`EXISTS`, шлях через `lessons` та `assignments`).
SELECT
    c.id AS course_id,
    c.title AS course_title,
    COUNT(a.id) AS assignments_count
FROM courses c
JOIN lessons l
    ON c.id = l.course_id
JOIN assignments a
    ON l.id = a.lesson_id
WHERE EXISTS (
    SELECT 1
    FROM lessons l2
    JOIN assignments a2
        ON l2.id = a2.lesson_id
    WHERE l2.course_id = c.id
)
GROUP BY c.id, c.title
ORDER BY c.id;
course_id|course_title   |assignments_count|
---------+---------------+-----------------+
        1|Python Basics  |                3|
        2|SQL Basics     |                2|
        4|QA Fundamentals|                1|

11. Здачі з оцінкою вищою за середню по своєму завданню (корельований підзапит).
SELECT
    s.id AS submission_id,
    s.assignment_id,
    a.title AS assignment_title,
    u.first_name,
    u.last_name,
    s.score
FROM submissions s
JOIN assignments a
    ON s.assignment_id = a.id
JOIN users u
    ON s.student_id = u.id
WHERE s.score IS NOT NULL
AND s.score > (
    SELECT AVG(s2.score)
    FROM submissions s2
    WHERE s2.assignment_id = s.assignment_id
      AND s2.score IS NOT NULL
)
ORDER BY s.assignment_id, s.score DESC;

submission_id|assignment_id|assignment_title|first_name|last_name|score|
-------------+-------------+----------------+----------+---------+-----+
            3|            1|Hello, Python   |Марія     |Бондар   |  100|
            1|            1|Hello, Python   |Ірина     |Коваль   |   90|
            8|            4|Перші запити    |Софія     |Лисенко  |   50|

12. Середня кількість здач на студента (серед тих, хто здавав), підзапит у `FROM`.

SELECT
    ROUND(AVG(student_submissions.submissions_count), 2)
        AS avg_submissions_per_student
FROM (
    SELECT
        student_id,
        COUNT(*) AS submissions_count
    FROM submissions
    GROUP BY student_id
) AS student_submissions;

avg_submissions_per_student|
---------------------------+
                       2.50|

13. Унікальні пари «викладач, опубліковано» з таблиці `courses`.
SELECT DISTINCT
    teacher_id,
    is_published
FROM courses
ORDER BY teacher_id, is_published;
teacher_id|is_published|
----------+------------+
         1|true        |
         2|false       |
         2|true        |

14. Остання здача кожного студента (`DISTINCT ON`).

SELECT DISTINCT ON (s.student_id)
    s.student_id,
    u.first_name,
    u.last_name,
    s.assignment_id,
    a.title AS assignment_title,
    s.score,
    s.submitted_at
FROM submissions s
JOIN users u
    ON s.student_id = u.id
JOIN assignments a
    ON s.assignment_id = a.id
ORDER BY
    s.student_id,
    s.submitted_at DESC;
student_id|first_name|last_name|assignment_id|assignment_title   |score|submitted_at           |
----------+----------+---------+-------------+-------------------+-----+-----------------------+
         3|Ірина     |Коваль   |            4|Перші запити       |   45|2026-10-12 14:20:00.000|
         4|Андрій    |Мельник  |            6|Тест-кейс для форми|   80|2026-10-14 13:00:00.000|
         5|Марія     |Бондар   |            1|Hello, Python      |  100|2026-10-02 09:15:00.000|
         7|Софія     |Лисенко  |            6|Тест-кейс для форми|     |2026-10-15 17:30:00.000|

15. Найкраща здача кожного завдання (`DISTINCT ON`, `NULL` в кінці).

SELECT DISTINCT ON (s.assignment_id)
    s.assignment_id,
    a.title AS assignment_title,
    s.student_id,
    u.first_name,
    u.last_name,
    s.score,
    s.submitted_at
FROM submissions s
JOIN assignments a
    ON s.assignment_id = a.id
JOIN users u
    ON s.student_id = u.id
ORDER BY
    s.assignment_id,
    s.score DESC NULLS LAST,
    s.submitted_at ASC;

  assignment_id|assignment_title   |student_id|first_name|last_name|score|submitted_at           |
-------------+-------------------+----------+----------+---------+-----+-----------------------+
            1|Hello, Python      |         5|Марія     |Бондар   |  100|2026-10-02 09:15:00.000|
            2|Цикли              |         3|Ірина     |Коваль   |   85|2026-10-08 18:00:00.000|
            3|Функція-калькулятор|         3|Ірина     |Коваль   |     |2026-10-10 20:45:00.000|
            4|Перші запити       |         7|Софія     |Лисенко  |   50|2026-10-13 16:10:00.000|
            6|Тест-кейс для форми|         4|Андрій    |Мельник  |   80|2026-10-14 13:00:00.000|  

### Рівень 3. Віконні функції

16. Усі здачі з середньою оцінкою завдання та відхиленням від неї.

SELECT
    s.id AS submission_id,
    a.title AS assignment_title,
    s.student_id,
    s.score,

    ROUND(
        AVG(s.score) OVER (
            PARTITION BY s.assignment_id
        ), 2
    ) AS avg_assignment_score,

    ROUND(
        s.score - AVG(s.score) OVER (
            PARTITION BY s.assignment_id
        ), 2
    ) AS deviation

FROM submissions s
JOIN assignments a
    ON s.assignment_id = a.id
ORDER BY s.assignment_id, s.id;
submission_id|assignment_title   |student_id|score|avg_assignment_score|deviation|
-------------+-------------------+----------+-----+--------------------+---------+
            1|Hello, Python      |         3|   90|               86.67|     3.33|
            2|Hello, Python      |         4|   70|               86.67|   -16.67|
            3|Hello, Python      |         5|  100|               86.67|    13.33|
            4|Цикли              |         3|   85|               85.00|     0.00|
            5|Цикли              |         4|     |               85.00|         |
            6|Функція-калькулятор|         3|     |                    |         |
            7|Перші запити       |         3|   45|               47.50|    -2.50|
            8|Перші запити       |         7|   50|               47.50|     2.50|
            9|Тест-кейс для форми|         4|   80|               80.00|     0.00|
           10|Тест-кейс для форми|         7|     |               80.00|         |

17. Для кожного завдання місце студента серед оцінених робіт (`RANK`). Залишіть лише першу позицію.
SELECT
    assignment_id,
    assignment_title,
    student_id,
    first_name,
    last_name,
    score,
    student_rank
FROM (
    SELECT
        a.id AS assignment_id,
        a.title AS assignment_title,
        u.id AS student_id,
        u.first_name,
        u.last_name,
        s.score,
        RANK() OVER (
            PARTITION BY s.assignment_id
            ORDER BY s.score DESC
        ) AS student_rank
    FROM submissions s
    JOIN assignments a
        ON s.assignment_id = a.id
    JOIN users u
        ON s.student_id = u.id
    WHERE s.score IS NOT NULL
) AS ranked_submissions
WHERE student_rank = 1
ORDER BY assignment_id;

assignment_id|assignment_title   |student_id|first_name|last_name|score|student_rank|
-------------+-------------------+----------+----------+---------+-----+------------+
            1|Hello, Python      |         5|Марія     |Бондар   |  100|           1|
            2|Цикли              |         3|Ірина     |Коваль   |   85|           1|
            4|Перші запити       |         7|Софія     |Лисенко  |   50|           1|
            6|Тест-кейс для форми|         4|Андрій    |Мельник  |   80|           1|

18. Накопичувальна сума балів кожного студента за часом здачі.
SELECT
    s.student_id,
    u.first_name,
    u.last_name,
    s.assignment_id,
    a.title AS assignment_title,
    s.score,
    s.submitted_at,

    SUM(s.score) OVER (
        PARTITION BY s.student_id
        ORDER BY s.submitted_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_score

FROM submissions s
JOIN users u
    ON s.student_id = u.id
JOIN assignments a
    ON s.assignment_id = a.id

ORDER BY s.student_id, s.submitted_at;

student_id|first_name|last_name|assignment_id|assignment_title   |score|submitted_at           |cumulative_score|
----------+----------+---------+-------------+-------------------+-----+-----------------------+----------------+
         3|Ірина     |Коваль   |            1|Hello, Python      |   90|2026-10-01 10:00:00.000|              90|
         3|Ірина     |Коваль   |            2|Цикли              |   85|2026-10-08 18:00:00.000|             175|
         3|Ірина     |Коваль   |            3|Функція-калькулятор|     |2026-10-10 20:45:00.000|             175|
         3|Ірина     |Коваль   |            4|Перші запити       |   45|2026-10-12 14:20:00.000|             220|
         4|Андрій    |Мельник  |            1|Hello, Python      |   70|2026-10-02 12:30:00.000|              70|
         4|Андрій    |Мельник  |            2|Цикли              |     |2026-10-09 11:00:00.000|              70|
         4|Андрій    |Мельник  |            6|Тест-кейс для форми|   80|2026-10-14 13:00:00.000|             150|
         5|Марія     |Бондар   |            1|Hello, Python      |  100|2026-10-02 09:15:00.000|             100|
         7|Софія     |Лисенко  |            4|Перші запити       |   50|2026-10-13 16:10:00.000|              50|
         7|Софія     |Лисенко  |            6|Тест-кейс для форми|     |2026-10-15 17:30:00.000|              50|

         19. Для кожної оціненої здачі: попередня оцінка того ж студента (`LAG`) і зміна.

         SELECT
    student_id,
    first_name,
    last_name,
    assignment_id,
    assignment_title,
    score,
    previous_score,
    score - previous_score AS score_change
FROM (
    SELECT
        s.student_id,
        u.first_name,
        u.last_name,
        s.assignment_id,
        a.title AS assignment_title,
        s.score,
        LAG(s.score) OVER (
            PARTITION BY s.student_id
            ORDER BY s.submitted_at
        ) AS previous_score
    FROM submissions s
    JOIN users u
        ON s.student_id = u.id
    JOIN assignments a
        ON s.assignment_id = a.id
    WHERE s.score IS NOT NULL
) AS student_scores
ORDER BY student_id, assignment_id;
student_id|first_name|last_name|assignment_id|assignment_title   |score|previous_score|score_change|
----------+----------+---------+-------------+-------------------+-----+--------------+------------+
         3|Ірина     |Коваль   |            1|Hello, Python      |   90|              |            |
         3|Ірина     |Коваль   |            2|Цикли              |   85|            90|          -5|
         3|Ірина     |Коваль   |            4|Перші запити       |   45|            85|         -40|
         4|Андрій    |Мельник  |            1|Hello, Python      |   70|              |            |
         4|Андрій    |Мельник  |            6|Тест-кейс для форми|   80|            70|          10|
         5|Марія     |Бондар   |            1|Hello, Python      |  100|              |            |
         7|Софія     |Лисенко  |            4|Перші запити       |   50|              |            |

20. Порядковий номер здачі кожного студента за часом (`ROW_NUMBER`). Виведіть студентів, які мають четверту здачу.

SELECT
    student_id,
    first_name,
    last_name,
    assignment_id,
    assignment_title,
    submitted_at,
    submission_number
FROM (
    SELECT
        s.student_id,
        u.first_name,
        u.last_name,
        s.assignment_id,
        a.title AS assignment_title,
        s.submitted_at,
        ROW_NUMBER() OVER (
            PARTITION BY s.student_id
            ORDER BY s.submitted_at
        ) AS submission_number
    FROM submissions s
    JOIN users u
        ON s.student_id = u.id
    JOIN assignments a
        ON s.assignment_id = a.id
) AS numbered_submissions
WHERE submission_number = 4
ORDER BY student_id;

student_id|first_name|last_name|assignment_id|assignment_title|submitted_at           |submission_number|
----------+----------+---------+-------------+----------------+-----------------------+-----------------+
         3|Ірина     |Коваль   |            4|Перші запити    |2026-10-12 14:20:00.000|                4|

### Рівень 4. VIEW

21. Створіть `v_student_progress` (студент, курс, кількість оцінених робіт, середня оцінка) на основі `v_gradebook`. Скільки в ньому рядків?

CREATE OR REPLACE VIEW v_student_progress AS
SELECT
    student_id,
    course_id,
    COUNT(*) AS total_assignments,
    AVG(score) AS average_score
FROM v_gradebook
GROUP BY student_id, course_id;

student_id|course_id|total_assignments|average_score       |
----------+---------+-----------------+--------------------+
         3|        1|                3| 87.5000000000000000|
         3|        2|                1| 45.0000000000000000|
         4|        1|                2| 70.0000000000000000|
         4|        4|                1| 80.0000000000000000|
         5|        1|                1|100.0000000000000000|
         7|        2|                1| 50.0000000000000000|
         7|        4|                1|                    |

