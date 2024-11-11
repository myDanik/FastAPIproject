from fastapi import APIRouter, FastAPI

from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from kinoteatr.backend.database import *
from kinoteatr.backend.models import *


app = FastAPI()

router = APIRouter(prefix="/page", tags=["page"])

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/main", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(request=request, name="main_page.html")


@router.get("/fud", response_class=HTMLResponse)
async def fud_page(request: Request, db: Session = Depends(get_database_session)):
    a_treat = db.query(A_treat).all()
    pizza = db.query(Pizza).all()
    drinks = db.query(Drinks).all()
    title_page_fud = ["Лакомства", "Съешь меня", "Выпей меня"]
    return templates.TemplateResponse(request=request, name='fud.html', context={'a_treat': a_treat, 'pizza': pizza, 'drinks': drinks, 'title_page_fud': title_page_fud})


@router.get("/film", response_class=HTMLResponse)
async def film_page(request: Request, db: Session = Depends(get_database_session)):
    films = db.query(Films).all()
    title_page_today = "Посмотри меня"
    return templates.TemplateResponse(request=request, name='films.html', context={'films': films, 'title_page_today': title_page_today})
