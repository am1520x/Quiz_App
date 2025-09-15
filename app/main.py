from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    return "<h1>Pub Quiz Buzzer</h1><p>It works!</p>"
# --- IGNORE ---