
| Тип        | Призначення             |
| --- | ---- |
| INTEGER    | Цілі числа              |
| BIGINT     | Великі числа            |
| TEXT       | Текст                   |
| VARCHAR(n) | Рядок обмеженої довжини |
| BOOLEAN    | True / False            |
| DATE       | Дата                    |
| TIMESTAMP  | Дата і час              |

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
);
```
```sql
CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);
```
```sql
INSERT INTO users (first_name, last_name, email, role)
VALUES ('Петро', 'Іваненко', 'petro@lms.ua', 'teacher')
RETURNING id, email;
```

```sql
INSERT INTO users (first_name, last_name, email, role)
VALUES
    ('Олена', 'Шевченко', 'olena@lms.ua',      'teacher'),
    ('Ірина', 'Коваль',   'iryna@mail.com',    'student'),
    ('Андрій', 'Мельник', 'andrii@gmail.com',  'student'),
    ('Марія', 'Бондар',   'maria@gmail.com',   'student'),
    ('Тест',  'Один',     'test1@mail.com',    'student'),
    ('Тест',  'Два',      'test2@mail.com',    'student');

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