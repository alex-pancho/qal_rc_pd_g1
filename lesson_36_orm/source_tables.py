from db_connetor import sqlalchemy_engine
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship


# Створити Base
class Base(DeclarativeBase):
    pass

# СтворитиEngine
engine = sqlalchemy_engine()


class User(Base):
    __tablename__ = "orm_users"
    
    # Атрибути = Стовпці
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    
    # Зв'язок (relationship) — один користувач до багатьох постів
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    
    # Методи
    def __repr__(self):
        return f"User (id={self.id}, username='{self.username}', email='{self.email}')\n"

class Post(Base):
    __tablename__ = "orm_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(5000), nullable=True)
    author_id = Column(Integer, ForeignKey("orm_users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    
    # Зв'язок (relationship) — багато постів до одного користувача
    author = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', author_id={self.author_id})>"

Base.metadata.create_all(engine)

# Альтернативно для SQLite (для тестування)
# engine = create_engine("sqlite:///test.db")
