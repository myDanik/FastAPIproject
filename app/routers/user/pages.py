from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import *
from app.db.models import *
from app.routers.templates import templates, static_files
from app.routers.user.auth import db_user


router = APIRouter(prefix="/page", tags=["Страницы сайта для пользователей"])

router.mount("/static", static_files, name="static")

@router.get("/main", response_class=HTMLResponse)
async def main_page(request: Request) -> HTMLResponse:
    if db_user:
        username = db_user[0]
    else:
        username = 'Гость'
    return templates.TemplateResponse("main_page.html", {'request': request, 'username': username})


@router.get("/food", response_class=HTMLResponse)
async def food_page(request: Request, db: Session = Depends(get_database_session)) -> HTMLResponse:
    treat = db.query(Treat).all()
    pizza = db.query(Pizza).all()
    drinks = db.query(Drinks).all()
    title_page_food = ["Лакомства", "Съешь меня", "Выпей меня"]
    return templates.TemplateResponse(request=request, name='food.html',
                                      context={'treat': treat, 'pizza': pizza, 'drinks': drinks, 'title_page_food': title_page_food})


@router.get("/films", response_class=HTMLResponse)
async def film_page(request: Request, db: Session = Depends(get_database_session)) -> HTMLResponse:
    films = db.query(FilmsToday).all()
    title_page_today = "Посмотри меня"
    return templates.TemplateResponse(request=request, name='films.html', context={'films': films, 'title_page_today': title_page_today})


@router.get("/film/{film_id}", response_class=HTMLResponse)
async def film_page(request: Request, film_id: int, db: Session = Depends(get_database_session)) -> HTMLResponse:
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    actor = db.query(Actor).filter(Actor.film_actor == film_id)
    photo = db.query(Photo_film).filter(Photo_film.film_photo == film_id)
    
    template_name = 'multfilm.html' if film_id == 1 else 'film1.html' if film_id == 2 else 'film2.html'
    
    return templates.TemplateResponse(
        template_name,
        {'request': request, 'film': film, 'actor': actor, 'photo': photo}
    )







