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

    comments = relationship('Comment', back_populates="user")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_username = Column(String, ForeignKey('users.username'), autoincrement=True)

    user = relationship("User", back_populates='comments')


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
    __tablename__ = "Фильмы сегодня"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    price = Column(Integer)
    time = Column(String)
    foto = Column(String)


class Film(Base):
    __tablename__ = "film"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(Text)
    year = Column(String)
    country = Column(String)
    age = Column(String)

    film_actor = relationship('Actor', back_populates="film")
    film_foto = relationship('Foto_film', back_populates="film" )


class Actor(Base):
    __tablename__ = "film_actor"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    foto = Column(String)
    role = Column(String)
    film_actor = Column(Integer, ForeignKey('film.id'))

    film = relationship("Film", back_populates='film_actor')


class Foto_film(Base):
    __tablename__ = "film_foto"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    foto = Column(String)
    film_foto = Column(Integer, ForeignKey('film.id'))

    film = relationship("Film", back_populates='film_foto')
