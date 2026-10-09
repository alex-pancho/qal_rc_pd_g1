import psycopg
import os
from dotenv import load_dotenv
load_dotenv()


def get_connection():
    # 2. Підключаємося вже до нашої БД
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=5432,
    )
