from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base
from app.db.database import engine
# Базовый класс для моделей
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String, nullable=True)

    comment = relationship('Comment', back_populates="user")


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'), autoincrement=True)

    user = relationship("User", back_populates='comment')


class Treat(Base):
    __tablename__ = "treat"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    description = Column(Text)
    photo = Column(String)


class Pizza(Base):
    __tablename__ = "pizza"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    description = Column(Text)
    photo = Column(String)


class Drinks(Base):
    __tablename__ = "drink"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    description = Column(Text)
    photo = Column(String)


class FilmsToday(Base):
    __tablename__ = "films_today"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    price = Column(Integer)
    time = Column(String)
    photo = Column(String)


class Film(Base):
    __tablename__ = "film"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(Text)
    year = Column(String)
    country = Column(String)
    age = Column(String)
    film_actor = relationship('Actor', back_populates="film")
    film_photo = relationship('Photo_film', back_populates="film" )


class Actor(Base):
    __tablename__ = "film_actor"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    photo = Column(String)
    role = Column(String)
    film_actor = Column(Integer, ForeignKey('film.id'))

    film = relationship("Film", back_populates='film_actor')


class Photo_film(Base):
    __tablename__ = "film_photo"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True, index=True)
    photo = Column(String)
    film_photo = Column(Integer, ForeignKey('film.id'))

    film = relationship("Film", back_populates='film_photo')

