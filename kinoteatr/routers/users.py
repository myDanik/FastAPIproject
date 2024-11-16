from fastapi import APIRouter, Depends, status, HTTPException, Form, Request
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update
from starlette.status import HTTP_400_BAD_REQUEST

from kinoteatr.backend.models import *
from kinoteatr.backend.database import get_database_session
from kinoteatr.schemas import UserCreate, UserAuth
from kinoteatr.secure import pwd_context


router = APIRouter(prefix="/user", tags=["Пользователи"])

templates = Jinja2Templates(directory="templates")

router.mount("/static", StaticFiles(directory="static"), name="static")


@router.post("/create")
async def user_create(db: Annotated[Session, Depends(get_database_session)], user_create: UserCreate = Depends()):
    db. execute(insert(User).values(
        email=user_create.email,
        username=user_create.username,
        hashed_password=pwd_context.hash(user_create.password1),
        first_name=user_create.first_name,
        last_name=user_create.last_name))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Успешно'
    }


@router.get("/all_users")
async def all_users(db: Annotated[Session, Depends(get_database_session)]):
    users = db.scalars(select(User)).all()
    return users


@router.post("/reg")
async def registration(request: Request, data: Annotated[UserCreate, Form()], db: Session = Depends(get_database_session)):
    # errors = []
    if db.scalar(select(User).where(User.username == data.username)):
        # errors = "Пользователь с таким именем уже существует!"
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Пользователь с таким именем уже существует!')
        # return templates.TemplateResponse("main_page.html", {'request': request, 'errors': errors})

    elif data.password1 != data.password2:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Пароли не совпадают!")
    hashed_password = pwd_context.hash(data.password1)
    db_user = User(
        username=data.username,
        hashed_password=hashed_password,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name
        )
    db.add(db_user)
    db.commit()

    return templates.TemplateResponse("main_page.html", {'request': request, 'db_user': db_user})


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


db_user = []


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, data: Annotated[UserAuth, Form()], db: Session = Depends(get_database_session)):
    user = db.scalar(select(User).where(User.username == data.username))
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не обнаружен')
    else:
        db_user.append(data.username),
        username = db_user[0]
        return templates.TemplateResponse("main_page.html", {'request': request, 'db_user': db_user, 'username': username})










# @router.post("/login", response_class=HTMLResponse)
# async def login(request: Request, data: Annotated[UserAuth, Form()], db: Session = Depends(get_database_session)):
#     user = db.scalar(select(User).where(User.username == data.username))
#     if not user or not verify_password(data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='Пользователь не обнаружен')
#     else:
#         # db_user = User(username=data.username)
#         # db.add(db_user)
#
#         # db.add(data)
#         db_user.append(data.username)
#         return templates.TemplateResponse("main_page.html", {'request': request, 'db_user': db_user})


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    pass
    db_user.clear()
    return templates.TemplateResponse("index.html", {'request': request, 'db_user': db_user})


@router.delete("/delete")
async def user_delete(db: Annotated[Session, Depends(get_database_session)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не обнаружен'
        )
    db.delete(user)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Пользователь успешно удалён'
    }