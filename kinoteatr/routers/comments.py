from fastapi import APIRouter, FastAPI

from typing import Annotated

from fastapi import Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, insert, update
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from kinoteatr.backend.models import *
from kinoteatr.backend.database import get_database_session
from kinoteatr.schemas import CommentCreate

app = FastAPI()

router = APIRouter(prefix="/comment", tags=["comment"])

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/")
async def comment_page(request: Request):
    return templates.TemplateResponse(request=request, name="comments.html")


@router.post("/create")
async def comment_create(db: Annotated[Session, Depends(get_database_session)], comment_create: CommentCreate = Depends()):
    db.execute(insert(Comment).values(
        text=comment_create.text,
        username=comment_create.username
        ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Успешно'
    }


@router.get("/all_users")
async def all_comment(db: Annotated[Session, Depends(get_database_session)]):
    comment = db.scalars(select(Comment)).all()
    return comment


@router.put("/update_comment")
async def comment_update(db: Annotated[Session, Depends(get_database_session)], comment_id: int,
                         com_update: CommentCreate = Depends()):
    comment = db.scalar(select(Comment).where(Comment.id == comment_id))
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Отзыв не обнаружен'
        )
    db.execute(update(Comment).where(Comment.id == comment_id).values(
        username=com_update.username,
        text=com_update.text
        ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Отзыв успешно изменён'
    }


@router.delete("/delete")
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
