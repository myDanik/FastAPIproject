from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Указываем URL базы данных
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем движок SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем локальную сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
