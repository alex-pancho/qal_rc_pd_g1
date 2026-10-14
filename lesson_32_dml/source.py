from db_connector import get_connection

create_lms = """
CREATE TABLE IF NOT EXISTS lms_users (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    role       TEXT NOT NULL CHECK (role IN ('student', 'teacher')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lms_courses (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title        TEXT NOT NULL,
    description  TEXT,
    teacher_id   INTEGER NOT NULL,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES lms_users(id)
);

CREATE TABLE IF NOT EXISTS lms_lessons (
    id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title     TEXT NOT NULL,
    position  INTEGER NOT NULL CHECK (position > 0),
    content   TEXT,
    FOREIGN KEY (course_id) REFERENCES lms_courses(id),
    UNIQUE (course_id, position)
);

CREATE TABLE IF NOT EXISTS lms_enrollments (
    user_id     INTEGER NOT NULL,
    course_id   INTEGER NOT NULL,
    enrolled_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'completed', 'dropped')),
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id)   REFERENCES lms_users(id),
    FOREIGN KEY (course_id) REFERENCES lms_courses(id)
);

CREATE TABLE IF NOT EXISTS lms_assignments (
    id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lesson_id INTEGER NOT NULL,
    title     TEXT NOT NULL,
    max_score INTEGER NOT NULL DEFAULT 100 CHECK (max_score > 0),
    due_date  TIMESTAMP,
    FOREIGN KEY (lesson_id) REFERENCES lms_lessons(id)
);

CREATE TABLE IF NOT EXISTS lms_submissions (
    id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    assignment_id INTEGER NOT NULL,
    student_id    INTEGER NOT NULL,
    answer_text   TEXT,
    score         INTEGER CHECK (score >= 0),
    submitted_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assignment_id) REFERENCES lms_assignments(id),
    FOREIGN KEY (student_id)    REFERENCES lms_users(id),
    UNIQUE (assignment_id, student_id)
);
"""

db_update = """
-- Телефон: необов'язкове поле
ALTER TABLE lms_users ADD COLUMN phone VARCHAR(20);

-- Ціна курсу: обов'язкове поле, не може бути від'ємною
ALTER TABLE lms_courses
ADD COLUMN price NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (price >= 0);
"""
insert_data = """

INSERT INTO lms_users (first_name, last_name, email, role)
VALUES
    ('Олена', 'Шевченко', 'olena@lms.ua',      'teacher'),
    ('Ірина', 'Коваль',   'iryna@mail.com',    'teacher'),
    ('Андрій', 'Мельник', 'andrii@gmail.com',  'student'),
    ('Марія', 'Бондар',   'maria@gmail.com',   'student'),
    ('Тест',  'Один',     'test1@mail.com',    'student'),
    ('Тест',  'Два',      'test2@mail.com',    'student');

INSERT INTO lms_courses (title, description, teacher_id, is_published)
VALUES
    ('Python Basics',        'Основи Python для початківців', 1, TRUE),
    ('SQL Basics',           'Вступ до баз даних',            1, TRUE),
    ('Python Advanced',      'ООП, декоратори, асинхронність', 2, FALSE),
    ('QA Fundamentals',      'Основи тестування ПЗ',          2, TRUE);

INSERT INTO lms_lessons (course_id, title, position)
VALUES
    (1, 'Змінні та типи даних', 1),
    (1, 'Умови та цикли',       2),
    (1, 'Функції',              3),
    (2, 'Вступ до SQL',         1),
    (2, 'SELECT та WHERE',      2);

INSERT INTO lms_enrollments (user_id, course_id)
VALUES (3, 1), (3, 2), (4, 1), (4, 3), (5, 1), (5, 4);

INSERT INTO lms_assignments (lesson_id, title, max_score, due_date)
VALUES
    (1, 'Hello, Python',        100, '2026-10-15 23:59'),
    (3, 'Функція-калькулятор',  100, '2026-10-30 23:59'),
    (5, 'Перші запити',          50, '2026-11-05 23:59');

INSERT INTO lms_submissions (assignment_id, student_id, answer_text, score)
VALUES
    (1, 3, 'print("Hello")', 90),
    (1, 4, 'print(1 + 1)',   70),
    (2, 3, 'def calc(): ...', NULL),
    (3, 3, 'SELECT * FROM users;', 45);

"""
sql = """
SELECT * FROM lms_courses;
"""
sql_ext = """
SELECT
    id    AS course_id,
    title AS course_title    
FROM lms_courses;
"""

with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute(sql_ext)
        print(cursor.fetchall())
    conn.commit()
