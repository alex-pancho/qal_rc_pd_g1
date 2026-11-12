CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL
        CHECK (role IN ('student', 'teacher')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. КУРСИ
CREATE TABLE courses (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    teacher_id INTEGER NOT NULL,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (teacher_id) REFERENCES users(id)
);


CREATE TABLE lessons (
    id INTEGER GENERATED
    ALWAYS AS IDENTITITY PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    position INTEGER NOT NULL CHECK (position > 0),
    content TEXT NOT NULL,

    FOREIGN KEY (course_id) REFERENCES courses(id),
    UNIQUE (course_id, position)
);

CREATE TABLE enrollments (
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'completed', 'dropped')),

    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);


CREATE TABLE assignments (
    id INTEGER GENERATED
    ALWAYS AS IDENTITITY PRIMARY KEY,
    lesson_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    max_score INTEGER NOT NULL CHECK (max_score > 0),
    due_date TIMESTAMP NOT NULL,

    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

CREATE TABLE submissions (
    id INTEGER GENERATED
    ALWAYS AS IDENTITITY PRIMARY KEY,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    answer TEXT NOT NULL,
    score INTEGER CHECK (score >= 0),
    feedback TEXT,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   

    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
    FOREIGN KEY (student_id) REFERENCES users(id)
);

INSERT INTO users (first_name, last_name, email, role)
VALUES
    ('Марія', 'Петренко', 'maria@lms.ua', 'student'),
    ('Олена', 'Коваль', 'olena@lms.ua', 'student'),
    ('Андрій', 'Мельник', 'andrii@lms.ua', 'student');
    SELECT id, first_name, last_name, email, role
FROM users
ORDER BY id;

INSERT INTO courses (title, description, teacher_id, is_published)
VALUES
    (
        'Python для початківців',
        'Основи програмування мовою Python',
        1,
        TRUE
    ),
    (
        'Основи SQL та PostgreSQL',
        'Робота з базами даних та SQL-запитами',
        1,
        TRUE
    );

    INSERT INTO lessons (course_id, title, position, content)
VALUES
    (
        (SELECT id FROM courses WHERE title = 'Python для початківців'),
        'Знайомство з Python',
        1,
        'Встановлення Python та налаштування середовища розробки'
    ),
    (
        (SELECT id FROM courses WHERE title = 'Python для початківців'),
        'Змінні та типи даних',
        2,
        'Основні типи даних, змінні та операції'
    ),
    (
        (SELECT id FROM courses WHERE title = 'Python для початківців'),
        'Умови та цикли',
        3,
        'Умовні конструкції if та цикли for і while'
    ),
    (
        (SELECT id FROM courses WHERE title = 'Основи SQL та PostgreSQL'),
        'Знайомство з SQL',
        1,
        'Основи мови SQL та структура баз даних'
    ),
    (
        (SELECT id FROM courses WHERE title = 'Основи SQL та PostgreSQL'),
        'SELECT та WHERE',
        2,
        'Вибірка та фільтрація даних'
    ),
    (
        (SELECT id FROM courses WHERE title = 'Основи SQL та PostgreSQL'),
        'JOIN',
        3,
        'Об'єднання даних із декількох таблиць'
    );

    INSERT INTO lessons (course_id, title, position, content)
VALUES
(1, 'Знайомство з Python', 1, 'Встановлення Python та налаштування середовища розробки'),
(1, 'Змінні та типи даних', 2, 'Основні типи даних, змінні та операції'),
(1, 'Умови та цикли', 3, 'Умовні конструкції if та цикли for і while'),
(2, 'Знайомство з SQL', 1, 'Основи мови SQL та структура баз даних'),
(2, 'SELECT та WHERE', 2, 'Вибірка та фільтрація даних'),
(2, 'JOIN', 3, 'Об’єднання даних із декількох таблиць');

SELECT id, title FROM courses ORDER BY id;

INSERT INTO assignments (lesson_id, title, max_score, due_date)
VALUES
(1, 'Встановлення Python', 10, '2026-11-15 23:59:00'),
(2, 'Робота зі змінними', 10, '2026-11-16 23:59:00'),
(3, 'Практика умов та циклів', 20, '2026-11-17 23:59:00'),
(4, 'Перші SQL-запити', 10, '2026-11-18 23:59:00'),
(5, 'Фільтрація даних', 15, '2026-11-19 23:59:00'),
(6, 'Практична робота з JOIN', 20, '2026-11-20 23:59:00')

INSERT INTO enrollments (user_id, course_id, enrolled_at, status)
VALUES
(2, 1, CURRENT_TIMESTAMP, 'active'),
(3, 1, CURRENT_TIMESTAMP, 'active'),
(4, 1, CURRENT_TIMESTAMP, 'active'),
(2, 2, CURRENT_TIMESTAMP, 'active'),
(3, 2, CURRENT_TIMESTAMP, 'active');

SELECT id, first_name, last_name, email, role
FROM users
ORDER BY id;

INSERT INTO enrollments (user_id, course_id, enrolled_at, status)
VALUES
(4, 1, CURRENT_TIMESTAMP, 'active'),
(5, 1, CURRENT_TIMESTAMP, 'active'),
(6, 1, CURRENT_TIMESTAMP, 'active'),
(4, 2, CURRENT_TIMESTAMP, 'active'),
(5, 2, CURRENT_TIMESTAMP, 'active');

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'submissions'
ORDER BY ordinal_position;

INSERT INTO submissions
    (assignment_id, student_id, answer_text, score, submitted_at)
VALUES
(1, 4, 'Python успішно встановлено', 10, CURRENT_TIMESTAMP),
(1, 5, 'Встановила Python та налаштувала середовище', 9, CURRENT_TIMESTAMP),
(2, 4, 'Створила змінні різних типів', 10, CURRENT_TIMESTAMP),
(3, 6, 'Виконав вправи з умовами та циклами', 18, CURRENT_TIMESTAMP),
(4, 5, 'Написала перші SELECT-запити', 9, CURRENT_TIMESTAMP),
(5, 6, 'Виконав фільтрацію за допомогою WHERE', 14, CURRENT_TIMESTAMP),
(6, 4, 'Обєднав таблиці за допомогою JOIN', 19, CURRENT_TIMESTAMP);

SELECT 'users' AS table_name, COUNT(*) AS total FROM users
UNION ALL
SELECT 'courses', COUNT(*) FROM courses
UNION ALL
SELECT 'lessons', COUNT(*) FROM lessons
UNION ALL
SELECT 'assignments', COUNT(*) FROM assignments
UNION ALL
SELECT 'enrollments', COUNT(*) FROM enrollments
UNION ALL
SELECT 'submissions', COUNT(*) FROM submissions;

SELECT
    u.first_name,
    u.last_name,
    c.title AS course,
    l.title AS lesson,
    a.title AS assignment,
    s.answer_text,
    s.score
FROM submissions s
JOIN users u ON s.student_id = u.id
JOIN assignments a ON s.assignment_id = a.id
JOIN lessons l ON a.lesson_id = l.id
JOIN courses c ON l.course_id = c.id
ORDER BY c.id, l.position, u.id;

SELECT
    u.first_name,
    u.last_name,
    c.title AS course,
    e.status,
    e.enrolled_at
FROM enrollments e
JOIN users u ON e.user_id = u.id
JOIN courses c ON e.course_id = c.id
ORDER BY c.id, u.id;

