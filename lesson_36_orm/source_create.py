from sqlalchemy.orm import sessionmaker
from source_tables import engine, User

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

user = User(
    username="lesya_nikityk",
    email="lesya_nikityk@example.com",
    password_hash="lesya_nikityk_123"
)

if __name__ == "__main__":

    with Session() as session:
        # Вся робота з БД тут
        session.add(user)
        session.commit()
        print(f"✅ Користувач {user.username} створений з ID {user.id}")