from db_connector import get_connection

create_tables= """
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
"""
insert_data = """
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
"""

select_for_check= """
SELECT 'users' AS table_name, COUNT(*) AS rows FROM users
UNION ALL SELECT 'courses',     COUNT(*) FROM courses
UNION ALL SELECT 'lessons',     COUNT(*) FROM lessons
UNION ALL SELECT 'enrollments', COUNT(*) FROM enrollments
UNION ALL SELECT 'assignments', COUNT(*) FROM assignments
UNION ALL SELECT 'submissions', COUNT(*) FROM submissions;
"""


with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute(select_for_check)
        print(cursor.fetchall())
    conn.commit()
