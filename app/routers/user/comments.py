from typing import Annotated
from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_database_session
from app.db.models import Comment
from app.schemas import CommentCreate
from app.routers.templates import templates, static_files
from app.routers.user.constants import ERRORS
from app.routers.user.auth import db_user

router = APIRouter(prefix="/user/comment", tags=["Отзывы пользователей"])

router.mount("/static", static_files, name="static")

@router.get("/create", response_class=HTMLResponse)
async def comment_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="comments.html")


@router.get("/all", response_class=HTMLResponse)
async def comment_all(request: Request, db: Session = Depends(get_database_session)) -> HTMLResponse:
    comments = db.query(Comment).all()
    return templates.TemplateResponse("comm_all.html", {'request': request, 'comments': comments})


@router.get("/edit", response_class=HTMLResponse)
async def comment_put(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("comm_put.html", {'request': request})


@router.post("/create", response_class=HTMLResponse)
async def comment_create(request: Request, data: Annotated[CommentCreate, Form()], db: Session = Depends(get_database_session)) -> HTMLResponse:
    if db.scalar(select(Comment).where(db_user[0] == Comment.user_id)):  # type: ignore
        message = ERRORS[4]
        return templates.TemplateResponse("comments.html", {'request': request, 'message': message})
    elif data.text == '':
        message = ERRORS[0]
        return templates.TemplateResponse("comments.html", {'request': request, 'message': message})
    else:
        db.execute(insert(Comment).values(
            text=data.text,
            user_id=db_user[0]
            ))
        db.commit()
        comments = db.query(Comment).all()
    return templates.TemplateResponse("comm_all.html", {'request': request, 'db': db, 'comments': comments})


@router.put("/update")
async def comment_update(request: Request, data: Annotated[CommentCreate, Form()], db: Session = Depends(get_database_session)) -> HTMLResponse:
    com = db.scalar(select(Comment).where(Comment.text == data.text))
    if com:
        message = ERRORS[6]
        return templates.TemplateResponse("comm_put.html", {'request': request, 'message': message})
    else:
        db.execute(update(Comment).where(Comment.user_id == db_user[0]).values(  # type: ignore
            text=data.text
            ))
        db.commit()
        comments = db.query(Comment).all()
    return templates.TemplateResponse("comm_all.html", {'request': request, 'db': db, 'comments': comments})


@router.delete("/delete", response_class=HTMLResponse)
async def comment_delete(request: Request, db: Session = Depends(get_database_session)) -> HTMLResponse:
    com = db.scalar(select(Comment).where(Comment.user_id == db_user[0]))  # type: ignore
    if com is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Вы можете удалить только свой отзыв')
    db.delete(com)
    db.commit()
    comments = db.query(Comment).all()
    return templates.TemplateResponse("comm_all.html", {'request': request, 'db': db, 'comments': comments})