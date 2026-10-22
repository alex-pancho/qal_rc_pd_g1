import psycopg
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

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

def sqlalchemy_engine():
    DATABASE_URL = (
        f"postgresql+psycopg://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:5432/"
        f"{os.getenv('DB_NAME')}"
    )
    engine = create_engine(DATABASE_URL, echo=True)
    return engine
