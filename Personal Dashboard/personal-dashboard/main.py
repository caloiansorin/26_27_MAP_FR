# uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import requests

load_dotenv()
CHEIE_OPEN_WEATHER = os.getenv("OPEN_WEATHER_API_KEY")
NUME = os.getenv("NUME")

app = FastAPI()

def obtine_vremea(oras):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": oras,
        "appid": CHEIE_OPEN_WEATHER,
        "units": "metric",
        "lang": "ro",
    }
    raspuns = requests.get(url, params=params, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()

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
    oras = request.query_params.get("oras", "Iasi")
    try:
        vreme = obtine_vremea(oras)
        eroare = None
    except requests.exceptions.RequestException as e:
        vreme = None
        eroare = f"Eroare la obtinerea vremii: {e}"

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "ora": ora,
            "salut": mesaj,
            "vreme": vreme,
            "eroare": eroare,
            "oras": oras
        },
    )


@app.get("/style.css")
def stil():

    return FileResponse("templates/style.css")

 