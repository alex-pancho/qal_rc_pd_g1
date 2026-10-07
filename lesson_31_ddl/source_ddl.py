"""
CREATE TABLE table_name (
    column_name data_type additional_info
);
"""

"""
CREATE TABLE users (
    id SERIAL INTEGER PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    email VARCHAR(500) UNIQUE NOT NULL,

);
"""
"""
CREATE TABLE orders (
    id SERIAL INTEGER PRIMARY KEY,
    user_id INTEGER,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
);

"""
"""
ALTER TABLE users
ADD COLUMN phone TEXT;
ALTER TABLE users
DROP COLUMN phone;

DROP TABLE users;
"""

"""
INSERT INTO users
(name)
values ('Alex')
"""
