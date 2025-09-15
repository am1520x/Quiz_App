from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import router

app = FastAPI(title="Pub Quiz Buzzer")

# Static files (JS/CSS) + templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.state.templates = Jinja2Templates(directory="app/templates")

# Routes + WebSockets
app.include_router(router)
