from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from app.db.models import *
from app.db.database import get_database_session
from app.routers.templates import templates, static_files
from app.schemas import Comment as CommentSchema

router = APIRouter(prefix="/comment", tags=["Отзывы для администратора сайта"])

router.mount("/static", static_files, name="static")

@router.get("/all_comment", response_model=list[CommentSchema])
async def all_comments(db: Annotated[Session, Depends(get_database_session)]) -> list[CommentSchema]:
    comment_list = db.scalars(select(Comment)).all()
    return [CommentSchema.from_orm(comment) for comment in comment_list]


@router.delete("/delete", response_class=HTMLResponse)
async def delete_comment(db: Annotated[Session, Depends(get_database_session)], comment_id: int) -> dict[str, int | str]:
    comment = db.scalar(select(Comment).where(Comment.id == comment_id))
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Отзыв не обнаружен'
        )
    db.delete(comment)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Отзыв успешно удалён'
    }
