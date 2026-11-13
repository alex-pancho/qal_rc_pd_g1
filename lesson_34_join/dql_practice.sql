#1Виведіть назви та ціни всіх курсів, від найдорожчого до найдешевшого.
 SELECT title, price FROM courses ORDER BY price DESC;
#2Виведіть опубліковані курси з ціною не більше 1000.
 SELECT title, price FROM courses WHERE price <= 1000;
 #3Виведіть користувачів із поштою на `lms.ua`
 SELECT * FROM users WHERE email LIKE '%@lms.ua';
 #Виведіть курси, у яких немає опису
 SELECT * FROM courses WHERE description IS NULL OR description = '';
 #Виведіть студентів, пошта яких не на `gmail.com`.
 SELECT * FROM users WHERE email NOT LIKE '%@gmail.com';
 #6. Виведіть завдання без дедлайну.
 SELECT title, due_date FROM assignments
 WHERE due_date >= '2026-10-15' AND due_date IS NULL;
#7. Виведіть здачі, які ще не оцінені.
SELECT id, student_id, assignment_id FROM submissions WHERE score IS NULL;
#8. Виведіть три найновіші здачі.
SELECT * FROM submissions ORDER BY submitted_at DESC LIMIT 3;
#9. Виведіть другу сторінку курсів (по 2 на сторінці, сортування за `id`).
SELECT * FROM courses ORDER BY id LIMIT 2 OFFSET 2;
#10. Виведіть курси з ціною від 800 до 1200 включно.
SELECT * FROM courses WHERE price BETWEEN 800 AND 1200;
#11. Знайдіть курси, у назві яких є слово `basics`, незалежно від регістру.
SELECT * FROM courses WHERE LOWER(title) LIKE '%basics%';

### Рівень2JOIN

#12. Виведіть усі курси разом з іменем та прізвищем викладача (`INNER JOIN`).
SELECT c.id, c.title, u.first_name, u.last_name
FROM courses c
INNER JOIN users u ON u.id = c.teacher_id
ORDER BY c.id;

#13.Виведіть усі уроки з назвою курсу, відсортовані за курсом і позицією.
SELECT l.id, l.title, c.title AS course_title
FROM lessons l
INNER JOIN courses c ON l.course_id = c.id
ORDER BY c.id, l.position;

#14.Виведіть активних студентів кожного курсу(назва курсу,ім'я,прізвище).
SELECT c.title AS course, u.first_name, u.last_name
FROM enrollments e
JOIN users   u ON u.id = e.user_id
JOIN courses c ON c.id = e.course_id
WHERE e.status = 'active'
ORDER BY c.id, u.id;

#15.Знайдіть курси без жодного уроку.
SELECT c.id, c.title
FROM courses c
LEFT JOIN lessons l ON l.course_id = c.id
WHERE l.id IS NULL;

#16. Знайдіть студентів, які не записані ні на один курс.
SELECT u.id, u.first_name, u.last_name
FROM users u
LEFT JOIN enrollments e ON e.user_id = u.id
WHERE u.role = 'student' AND e.user_id IS NULL;

#17. Знайдіть викладачів, у яких немає курсів.
SELECT u.id, u.first_name, u.last_name
FROM users u
LEFT JOIN courses c ON c.teacher_id = u.id
WHERE u.role = 'teacher' AND c.id IS NULL;

#18. Виведіть усі курси та кількість активних студентів на кожному, включно з нулями.
SELECT c.title AS course, u.first_name, u.last_name
FROM enrollments e
JOIN users   u ON u.id = e.user_id
JOIN courses c ON c.id = e.course_id
WHERE e.status = 'active'
ORDER BY c.id, u.id;

#19. Знайдіть завдання, на які ще ніхто не здав роботу.
SELECT a.id, a.title
FROM assignments a
LEFT JOIN submissions s ON s.assignment_id = a.id
WHERE s.id IS NULL;

#Рівень 3. Складні вибірки

#20. Для викладача Олени (`olena@lms.ua`) виведіть неоцінені здачі: студент, курс, завдання.

SELECT
    student.first_name || ' ' || student.last_name AS student,
    courses.title AS course,
    assignments.title AS assignment
FROM users AS teacher
JOIN courses
    ON courses.teacher_id = teacher.id
JOIN lessons
    ON lessons.course_id = courses.id
JOIN assignments
    ON assignments.lesson_id = lessons.id
JOIN submissions
    ON submissions.assignment_id = assignments.id
JOIN users AS student
    ON student.id = submissions.student_id
WHERE teacher.email = 'olena@lms.ua'
    AND teacher.role = 'teacher'
    AND submissions.score IS NULL
ORDER BY
    courses.title,
    assignments.title,
    student.last_name;

#21. Виведіть журнал студентки Ірини (`iryna@mail.com`): курс, завдання, оцінка, максимальний бал, оцінка у відсотках (округлено до 1 знака).
SELECT
    courses.title AS course,
    assignments.title AS assignment,
    submissions.score AS score,
    assignments.max_score AS max_score,

    ROUND(
        submissions.score::NUMERIC
        / assignments.max_score * 100,
        1
    ) AS score_percent

FROM users

JOIN submissions
    ON submissions.student_id = users.id

JOIN assignments
    ON assignments.id = submissions.assignment_id

JOIN lessons
    ON lessons.id = assignments.lesson_id

JOIN courses
    ON courses.id = lessons.course_id

WHERE users.email = 'iryna@mail.com'
    AND users.role = 'student'

ORDER BY
    courses.title,
    assignments.title;

#22. Виведіть трьох студентів із найбільшою сумою оцінок.

SELECT
    users.id,
    users.first_name,
    users.last_name,
    COALESCE(SUM(submissions.score), 0) AS total_score

FROM users

LEFT JOIN submissions
    ON submissions.student_id = users.id

WHERE users.role = 'student'

GROUP BY
    users.id,
    users.first_name,
    users.last_name

ORDER BY total_score DESC

LIMIT 3;

#23. Для кожного курсу виведіть кількість здач і середню оцінку, включно з курсами без жодної здачі (у них має бути `0` здач).

SELECT
    courses.title AS course,
    COUNT(submissions.id) AS submission_count,
    COALESCE(
        ROUND(AVG(submissions.score), 1),
        0
    ) AS average_score

FROM courses

LEFT JOIN lessons
    ON lessons.course_id = courses.id

LEFT JOIN assignments
    ON assignments.lesson_id = lessons.id

LEFT JOIN submissions
    ON submissions.assignment_id = assignments.id

GROUP BY
    courses.id,
    courses.title

ORDER BY courses.title;
