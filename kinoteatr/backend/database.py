from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Указываем URL базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Создаем движок SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем локальную сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
