from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from app.routers.templates import templates, static_files
from app.routers.user import pages, auth
from app.routers.user import comments as user_comments
from app.routers.admin import comments as admin_comments
from app.routers.admin import users

app = FastAPI()

app.include_router(pages.router)
app.include_router(user_comments.router)
app.include_router(auth.router)

app.include_router(users.router)
app.include_router(admin_comments.router)


app.mount("/static", static_files, name="static")

@app.get("/", response_class=HTMLResponse)
async def start_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html")


