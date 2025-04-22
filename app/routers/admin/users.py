from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import select


from app.db.models import *
from app.db.database import get_database_session
from app.routers.templates import static_files
from app.schemas import User as UserSchema

router = APIRouter(prefix="/user", tags=["Пользователи для администратора сайта"])

router.mount("/static", static_files, name="static")


@router.get("/all", response_model=list[UserSchema])
async def all_users(db: Annotated[Session, Depends(get_database_session)]) -> list[UserSchema]:
    users = db.scalars(select(User)).all()
    return [UserSchema.from_orm(user) for user in users]


@router.delete("/delete")
async def user_delete(db: Annotated[Session, Depends(get_database_session)], user_id: int) -> dict[str, int | str]:
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



