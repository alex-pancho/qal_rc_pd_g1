from contextlib import contextmanager
from source_create import Session
from source_tables import User, Post
from sqlalchemy import and_, or_, not_

@contextmanager
def get_session():
    """Context manager для сесій"""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Використання
with get_session() as session:
    # user = User(
    #     username="maria",
    #     email="maria@example.com",
    #     password_hash="hash_maria"
    # )
    # session.add(user)
    # users = [
    #     User(username="alice", email="alice@example.com", password_hash="hash1"),
    #     User(username="bob", email="bob@example.com", password_hash="hash2"),
    #     User(username="charlie", email="charlie@example.com", password_hash="hash3"),
    # ]
    # session.add_all(users)
    user = session.query(User).filter_by(id=1).first()
    user = session.query(User).filter_by(email="alice@example.com").first()
    user = session.query(User).filter_by(username="maria").first()
    print(user)
    users = session.query(User).all()
    print(users)
    example_com_users = session.query(User).filter(User.email.like("%@example.com")).all()
    print(example_com_users)
    user = session.query(User).filter_by(email="alice@example.com").first()
    if user:
        user.email = "new_alice@example.com"
        user.is_active = False
    print("*"*8)
    users = session.query(User).filter(
        or_(
            User.username == "bob",
            User.email == "maria@example.com"
        )
    ).all()
    print(">>>>",users)

    users = session.query(User).filter(
    and_(
        User.is_active == True,
        or_(
            User.username.like("%admin%"),
            User.email.like("%@gmail.com%")
        )
    )
    ).all()

    posts_with_authors = session.query(Post, User).join(User).all()
    print(posts_with_authors)
    # Явна умова JOIN
    posts_with_authors_2 = session.query(Post, User).join(
        User, Post.author_id == User.id
    ).all()
