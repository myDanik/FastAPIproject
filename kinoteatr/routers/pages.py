from typing import Annotated

from fastapi import APIRouter, HTTPException, Form, Request, Depends

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from kinoteatr.routers.comments import comment_update, all_comment
from kinoteatr.routers.users import db_user, logout, registration, login

from kinoteatr.backend.database import *
from kinoteatr.backend.models import *

from kinoteatr.schemas import UserAuth, CommentCreate, UserCreate
from kinoteatr.secure import pwd_context


router = APIRouter(prefix="/page", tags=["Страницы сайта"])

templates = Jinja2Templates(directory="templates")

router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/main", response_class=HTMLResponse)
async def main_page(request: Request, out: logout = Depends(logout)):
    if db_user:
        username = db_user[0]
    else:
        username = 'Гость'
    return templates.TemplateResponse("main_page.html", {'request': request, 'username': username, 'out': out})


@router.get("/fud", response_class=HTMLResponse)
async def fud_page(request: Request, db: Session = Depends(get_database_session)):
    a_treat = db.query(A_treat).all()
    pizza = db.query(Pizza).all()
    drinks = db.query(Drinks).all()
    title_page_fud = ["Лакомства", "Съешь меня", "Выпей меня"]
    return templates.TemplateResponse(request=request, name='fud.html',
                                      context={'a_treat': a_treat, 'pizza': pizza, 'drinks': drinks, 'title_page_fud': title_page_fud})


@router.get("/film", response_class=HTMLResponse)
async def film_page(request: Request, db: Session = Depends(get_database_session)):
    films = db.query(Films).all()
    title_page_today = "Посмотри меня"
    return templates.TemplateResponse(request=request, name='films.html', context={'films': films, 'title_page_today': title_page_today})


@router.get("/reg", response_class=HTMLResponse)
async def reg_page(request: Request, registr: registration = Depends(registration)):
    return templates.TemplateResponse("registration.html", {'request': request, 'registr': registr})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {'request': request})



























@router.get("/comm_create", response_class=HTMLResponse)
async def comment_page(request: Request):
    return templates.TemplateResponse(request=request, name="comments.html")


@router.get("/comm_all", response_class=HTMLResponse)
async def comm_all(request: Request, comments: all_comment = Depends(all_comment)):
    return templates.TemplateResponse("comm_all.html", {'request': request, 'comments': comments})


@router.get("/comm_put/{form}")
async def comm_put(request: Request, form=Depends(comment_update)):
    return templates.TemplateResponse("comm_put.html", {'request': request, 'form': form})


# @router.post("/reg", response_class=HTMLResponse)
# async def registration(request: Request, data: Annotated[UserCreate, Form()], db: Session = Depends(get_database_session)):
#     if db.scalar(select(User).where(User.username == data.username)):
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Пользователь с таким именем уже существует!')
#     elif data.password1 != data.password2:
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Пароли не совпадают!")
#
#     hashed_password = pwd_context.hash(data.password1)
#     db.execute(insert(User).values(
#         username=data.username,
#         hashed_password=hashed_password,
#         email=data.email,
#         first_name=data.first_name,
#         last_name=data.last_name
#         ))
#     db.commit()
#     db_user.append(data.username),
#     username = db_user[0]
#
#     return templates.TemplateResponse("main_page.html", {'request': request, 'db': db, 'db_user': db_user, 'username': username})
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# db_user = []


# @router.post("/login", response_class=HTMLResponse)
# async def login(request: Request, data: Annotated[UserAuth, Form()], db: Session = Depends(get_database_session)):
#     user = db.scalar(select(User).where(User.username == data.username))
#     if not user or not verify_password(data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='Пользователь не обнаружен')
#     else:
#         db_user.append(data.username),
#         username = db_user[0]
#         return templates.TemplateResponse("main_page.html", {'request': request, 'db_user': db_user, 'username': username})
#
#
# @router.get("/logout", response_class=HTMLResponse)
# async def logout(request: Request):
#     pass
#     db_user.clear()
#     return templates.TemplateResponse("index.html", {'request': request, 'db_user': db_user})


# @router.post("/create", response_class=HTMLResponse)
# async def comment_create(request: Request, data: Annotated[CommentCreate, Form()], db: Session = Depends(get_database_session)):
#     if db.scalar(select(Comment).where(db_user[0] == Comment.user_username)):  # type: ignore
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Пользователь может оставить только один отзыв')
#     db.execute(insert(Comment).values(
#         text=data.text,
#         user_username=db_user[0]
#         ))
#     db.commit()
#     comments_all = db.query(Comment).all()
#     return templates.TemplateResponse("comm_all.html", {'request': request, 'db': db, 'comments_all': comments_all})


