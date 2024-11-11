from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from kinoteatr.routers import pages, users, comments
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def start_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


app.include_router(pages.router)
app.include_router(users.router)
app.include_router(comments.router)