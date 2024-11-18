from typing import Annotated

from fastapi import APIRouter, HTTPException, Form, Request, Depends

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session
from starlette import status
import re

from kinoteatr.backend.database import *
from kinoteatr.backend.models import *

from kinoteatr.schemas import UserAuth, CommentCreate, UserCreate
from kinoteatr.secure import pwd_context


router = APIRouter(prefix="/page", tags=["Страницы сайта для пользователей"])

templates = Jinja2Templates(directory="templates")

router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/main", response_class=HTMLResponse)
async def main_page(request: Request):
    if db_user:
        username = db_user[0]
    else:
        username = 'Гость'
    return templates.TemplateResponse("main_page.html", {'request': request, 'username': username})


@router.get("/fud", response_class=HTMLResponse)
async def fud_page(request: Request, db: Session = Depends(get_database_session)):
    a_treat = db.query(A_treat).all()
    pizza = db.query(Pizza).all()
    drinks = db.query(Drinks).all()
    title_page_fud = ["Лакомства", "Съешь меня", "Выпей меня"]
    return templates.TemplateResponse(request=request, name='fud.html',
                                      context={'a_treat': a_treat, 'pizza': pizza, 'drinks': drinks, 'title_page_fud': title_page_fud})


@router.get("/films", response_class=HTMLResponse)
async def film_page(request: Request, db: Session = Depends(get_database_session)):
    films = db.query(Films).all()
    title_page_today = "Посмотри меня"
    return templates.TemplateResponse(request=request, name='films.html', context={'films': films, 'title_page_today': title_page_today})


@router.get("/multfilm", response_class=HTMLResponse)
async def multfilm_page(request: Request, db: Session = Depends(get_database_session)):
    film = db.query(Film).filter(Film.id == 1).first()
    actor = db.query(Actor).filter(Actor.film_actor == 1)
    foto = db.query(Foto_film).filter(Foto_film.film_foto == 1)
    return templates.TemplateResponse(request=request, name='multfilm.html', context={'film': film, 'actor': actor, 'foto': foto})


@router.get("/film1", response_class=HTMLResponse)
async def film1_page(request: Request, db: Session = Depends(get_database_session)):
    film = db.query(Film).filter(Film.id == 2).first()
    actor = db.query(Actor).filter(Actor.film_actor == 2)
    foto = db.query(Foto_film).filter(Foto_film.film_foto == 2)
    return templates.TemplateResponse('film1.html', {'request': request, 'film': film, 'actor': actor, 'foto': foto})


@router.get("/film2", response_class=HTMLResponse)
async def film2_page(request: Request, db: Session = Depends(get_database_session)):
    film = db.query(Film).filter(Film.id == 3).first()
    actor = db.query(Actor).filter(Actor.film_actor == 3)
    foto = db.query(Foto_film).filter(Foto_film.film_foto == 3)
    return templates.TemplateResponse('film2.html', {'request': request, 'film': film, 'actor': actor, 'foto': foto})


@router.get("/reg", response_class=HTMLResponse)
async def reg_page(request: Request):
    return templates.TemplateResponse("registration.html", {'request': request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {'request': request})

errors = ['Поле должно быть заполнено', 'Пользователь не обнаружен', 'Пользователь с таким именем уже существует!', "Пароли не совпадают!",
          'Пользователь может оставить только один отзыв', 'Введите корректный адрес электронной почты', 'Измените свой отзыв перед сохранением']

db_user = []

regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")


def is_valid(email):
    return re.fullmatch(regex, email)


@router.post("/reg")
async def registration(request: Request, data: Annotated[UserCreate, Form()], db: Session = Depends(get_database_session)):
    if db.scalar(select(User).where(User.username == data.username)):
        message = errors[2]
        return templates.TemplateResponse("registration.html", {'request': request, 'message': message})
    elif data.password1 != data.password2:
        message = errors[3]
        return templates.TemplateResponse("registration.html", {'request': request, 'message': message})
    elif not is_valid(data.email):
        message = errors[5]
        return templates.TemplateResponse("registration.html", {'request': request, 'message': message})
    elif data.username == '' and data.password1 == '' and data.password2 == '' and data.email == '' and data.first_name == '':
        message = errors[0]
        return templates.TemplateResponse("registration.html", {'request': request, 'message': message})
    else:
        hashed_password = pwd_context.hash(data.password1)
        db.execute(insert(User).values(
            username=data.username,
            hashed_password=hashed_password,
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name
            ))
        db.commit()
        db_user.append(data.username),
        username = db_user[0]
    return templates.TemplateResponse("main_page.html", {'request': request, 'db_user': db_user, 'username': username})


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, data: Annotated[UserAuth, Form()], db: Session = Depends(get_database_session)):
    user = db.scalar(select(User).where(User.username == data.username))
    if not user or not verify_password(data.password, user.hashed_password):
        message = errors[1]
        return templates.TemplateResponse("login.html", {'request': request, 'message': message})
    elif data.username == '' or data.password == '':
        message = errors[0]
        return templates.TemplateResponse("comments.html", {'request': request, 'message': message})
    else:
        db_user.append(data.username),
        username = db_user[0]
    return templates.TemplateResponse("main_page.html", {'request': request, 'db_user': db_user, 'username': username})


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    pass
    db_user.clear()
    return templates.TemplateResponse("index.html", {'request': request, 'db_user': db_user})


@router.get("/comm_create", response_class=HTMLResponse)
async def comment_page(request: Request):
    return templates.TemplateResponse(request=request, name="comments.html")


@router.get("/comm_all", response_class=HTMLResponse)
async def comm_all(request: Request, db: Session = Depends(get_database_session)):
    comments = db.query(Comment).all()
    return templates.TemplateResponse("comm_all.html", {'request': request, 'comments': comments})


@router.get("/comm_put")
async def comm_put(request: Request):
    return templates.TemplateResponse("comm_put.html", {'request': request})


@router.post("/comment_create")
async def comment_create(request: Request, data: Annotated[CommentCreate, Form()], db: Session = Depends(get_database_session)):
    if db.scalar(select(Comment).where(db_user[0] == Comment.user_username)):  # type: ignore
        message = errors[4]
        return templates.TemplateResponse("comments.html", {'request': request, 'message': message})
    elif data.text == '':
        message = errors[0]
        return templates.TemplateResponse("comments.html", {'request': request, 'message': message})
    else:
        db.execute(insert(Comment).values(
            text=data.text,
            user_username=db_user[0]
            ))
        db.commit()
        comments = db.query(Comment).all()
    return templates.TemplateResponse("comm_all.html", {'request': request, 'db': db, 'comments': comments})


@router.post("/comment_update")
async def comment_update(request: Request, data: Annotated[CommentCreate, Form()], db: Session = Depends(get_database_session)):
    com = db.scalar(select(Comment).where(Comment.text == data.text))
    if com:
        message = errors[6]
        return templates.TemplateResponse("comm_put.html", {'request': request, 'message': message})
    else:
        db.execute(update(Comment).where(Comment.user_username == db_user[0]).values(  # type: ignore
            text=data.text
            ))
        db.commit()
        comments = db.query(Comment).all()
    return templates.TemplateResponse("comm_all.html", {'request': request, 'db': db, 'comments': comments})


@router.get("/comment_delete", response_class=HTMLResponse)
async def comment_delete(request: Request, db: Session = Depends(get_database_session)):
    com = db.scalar(select(Comment).where(Comment.user_username == db_user[0]))  # type: ignore
    if com is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Вы можете удалить только свой отзыв')
    db.delete(com)
    db.commit()
    comments = db.query(Comment).all()
    return templates.TemplateResponse("comm_all.html", {'request': request, 'db': db, 'comments': comments})
