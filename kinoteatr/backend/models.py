from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

# Базовый класс для моделей
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String, nullable=True)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    username = Column(String)


class A_treat(Base):
    __tablename__ = "Лакомства"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    description = Column(Text)
    foto = Column(String)


class Pizza(Base):
    __tablename__ = "Пицца"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    description = Column(Text)
    foto = Column(String)


class Drinks(Base):
    __tablename__ = "Напитки"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    description = Column(Text)
    foto = Column(String)


class Films(Base):
    __tablename__ = "Фильмы"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    price = Column(Integer)
    time = Column(String)
    foto = Column(String)
