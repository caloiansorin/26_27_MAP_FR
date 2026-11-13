# uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import time
from datetime import datetime

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def salut(ora):
    if ora < 12:
        return "Buna dimineata!"
    elif ora < 18:
        return "Buna ziua!"
    else:
        return "Buna seara!"

@app.get("/")
def radacina():
    """Ruta / ne trimite direct la /home."""
    return RedirectResponse("/home")


@app.get("/home")
def home(request: Request):
    acum = datetime.now()
    ora = acum.strftime("%H:%M")
    mesaj = salut(acum.hour)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "ora": ora,
            "salut": mesaj
        },
    )


@app.get("/style.css")
def stil():

    return FileResponse("templates/style.css")

 