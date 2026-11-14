import psycopg

# Параметри підключення
DSN = "postgresql://postgres:postgres@localhost:5432/lesson_30_test"

try:
    # Підключитися до БД
    with psycopg.connect(DSN) as conn:
        print("Успішно підключені до PostgreSQL!")

        # Отримати інформацію про БД
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"\nPostgreSQL версія:\n{version}\n")

            # Поточний користувач
            cur.execute("SELECT current_user;")
            user = cur.fetchone()[0]
            print(f"Користувач: {user}")

            # Поточна база даних
            cur.execute("SELECT current_database();")
            database = cur.fetchone()[0]
            print(f"Поточна БД: {database}")

except psycopg.Error as e:
    print(f"Помилка підключення: {e}")
