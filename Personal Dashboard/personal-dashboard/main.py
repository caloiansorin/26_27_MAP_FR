# uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def radacina():
    """Ruta / ne trimite direct la /home."""
    return RedirectResponse("/home")


@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {},
    )


@app.get("/style.css")
def stil():

    return FileResponse("templates/style.css")

 