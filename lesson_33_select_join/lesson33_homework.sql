__Linichenko_Tetiyana

SELECT id, title, price
FROM lms_courses
WHERE published AND price > 1000
ORDER BY price DESC;

BEGIN;
UPDATE lms_courses SET price = price - 100 WHERE title = 'SQL Basics' RETURNING id, title, price;
ROLLBACK;

SELECT c.title, u.last_name
FROM lms_courses c
JOIN lms_users u ON u.id = c.teacher_id
WHERE c.published;

SELECT u.last_name, e.status
FROM lms_enrollments e
JOIN lms_users u   ON u.id = e.user_id
JOIN lms_courses c ON c.id = e.course_id
WHERE c.title = 'Python Basics';

SELECT c.title
FROM lms_courses c
LEFT JOIN lms_enrollments e ON e.course_id = c.id
WHERE e.user_id IS NULL;

SELECT a.title, s.score, a.max_score
FROM lms_submissions s
JOIN lms_users u       ON u.id = s.user_id
JOIN lms_assignments a ON a.id = s.assignment_id
WHERE u.first_name = 'Ірина' AND u.last_name = 'Коваль' AND s.score IS NOT NULL;

SELECT id, title, price
FROM lms_courses
WHERE published AND price > 1000
ORDER BY price DESC;

