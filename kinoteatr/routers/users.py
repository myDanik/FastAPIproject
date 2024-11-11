from fastapi import APIRouter, Depends, status, HTTPException, Form, Request, FastAPI
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

app = FastAPI()

router = APIRouter(prefix="/user", tags=["user"])

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/reg")
async def reg_page(request: Request):
    return templates.TemplateResponse(request=request, name="registration.html")


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


@router.post("/reg", response_class=HTMLResponse)
async def registration(request: Request, data: Annotated[UserCreate, Form()], db: Session = Depends(get_database_session)):
    if db.scalar(select(User).where(User.username == data.username)):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Пользователь с таким именем уже существует!')
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


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@router.post("/login")
async def login(request: Request, db: Annotated[Session, Depends(get_database_session)], user_id: int) -> HTMLResponse:
    # if db_login:
    #     login_id = len(db_login)
    # else:
    #     login_id = 0
    # db_login.append(UserAuth(id=login_id, username=data.username, password=data.password))
    # # hashed_password = pwd_context.hash(user.password1)
    # login = User(
    #         id=data.id,
    #         username=data.username,
    #         password=pwd_context.hash(data.password))
    # db.add(login)
    # db.commit()
    return templates.TemplateResponse("login.html", {'request': request, "login": login})


@router.delete("/delete")
async def user_delete(db: Annotated[Session, Depends(get_database_session)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    # user = db.query(User).filter(User.id == user_id).first
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