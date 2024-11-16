from fastapi import APIRouter

from typing import Annotated

from fastapi import Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, insert, update
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from kinoteatr.backend.models import Comment
from kinoteatr.backend.database import get_database_session
from kinoteatr.schemas import CommentCreate
from kinoteatr.routers.users import db_user


router = APIRouter(prefix="/comment", tags=["Отзывы"])

templates = Jinja2Templates(directory="templates")

router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/all_comment")
async def all_comment(db: Annotated[Session, Depends(get_database_session)]):
    comment = db.scalars(select(Comment)).all()
    return comment


@router.put("/comment_update")
async def comment_update(request: Request, data: Annotated[CommentCreate, Form()], db: Session = Depends(get_database_session)):
    com = db.scalar(select(Comment).where(Comment.user_username == db_user[0]))  # type: ignore
    if com is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Вы можете изменять только свой отзыв'
        )
    com = db.scalar(select(Comment).where(Comment.text != CommentCreate.text))
    if com is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Измените свой отзыв перед сохранением'
        )
    db.execute(update(Comment).where(Comment.user_username == db_user[0]).values(  # type: ignore
        text=data.text
        ))
    db.commit()
    comments = db.query(Comment).all()
    return templates.TemplateResponse("comm_all.html", {'request': request, 'db': db, 'comments': comments})


@router.delete("/delete", response_class=HTMLResponse)
async def comment_delete(db: Annotated[Session, Depends(get_database_session)], comment_id: int ):
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
