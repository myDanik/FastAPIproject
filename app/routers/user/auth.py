import re

from typing import Annotated
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.db.database import get_database_session
from app.db.models import User
from app.schemas import UserAuth, UserCreate
from app.secure import pwd_context
from app.routers.templates import templates, static_files
from app.routers.user.constants import ERRORS

router = APIRouter(prefix="/auth", tags=["Аутентификация"])

router.mount("/static", static_files, name="static")

db_user = []

regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")


def is_valid(email: str) -> bool:
    return re.fullmatch(regex, email)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.get("/reg", response_class=HTMLResponse)
async def reg_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("registration.html", {'request': request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("login.html", {'request': request})

@router.post("/reg")
async def registration(request: Request, data: Annotated[UserCreate, Form()], db: Session = Depends(get_database_session)) -> HTMLResponse:
    if db.scalar(select(User).where(User.username == data.username)):
        message = ERRORS[2]
        return templates.TemplateResponse("registration.html", {'request': request, 'message': message})
    elif data.password1 != data.password2:
        message = ERRORS[3]
        return templates.TemplateResponse("registration.html", {'request': request, 'message': message})
    elif not is_valid(data.email):
        message = ERRORS[5]
        return templates.TemplateResponse("registration.html", {'request': request, 'message': message})
    elif data.username == '' and data.password1 == '' and data.password2 == '' and data.email == '' and data.first_name == '':
        message = ERRORS[0]
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


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, data: Annotated[UserAuth, Form()], db: Session = Depends(get_database_session)) -> HTMLResponse:
    user = db.scalar(select(User).where(User.username == data.username))
    if not user or not verify_password(data.password, user.hashed_password):
        message = ERRORS[1]
        return templates.TemplateResponse("login.html", {'request': request, 'message': message})
    elif data.username == '' or data.password == '':
        message = ERRORS[0]
        return templates.TemplateResponse("comments.html", {'request': request, 'message': message})
    else:
        db_user.append(data.username),
        username = db_user[0]
    return templates.TemplateResponse("main_page.html", {'request': request, 'db_user': db_user, 'username': username})


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request) -> HTMLResponse:
    pass
    db_user.clear()
    return templates.TemplateResponse("index.html", {'request': request, 'db_user': db_user})
