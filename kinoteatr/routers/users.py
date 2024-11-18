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


router = APIRouter(prefix="/user", tags=["Пользователи для администратора сайта"])

templates = Jinja2Templates(directory="templates")

router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/all_users")
async def all_users(db: Annotated[Session, Depends(get_database_session)]):
    users = db.scalars(select(User)).all()
    return users


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



