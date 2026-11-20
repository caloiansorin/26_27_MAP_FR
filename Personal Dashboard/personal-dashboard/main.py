# uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form    
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import requests

load_dotenv()
CHEIE_WEATHER_API = os.getenv("OPEN_WEATHER_API_KEY")
numele_tau = os.getenv("NUME")

app = FastAPI()
sarcini = {
    1: {
        "titlu": "Citeste capitolul 1 din cartea preferata",
        "prioritate": "medie",
        "finalizata": True
    },
    2: {
        "titlu": "Mergi la sala de sport",
        "prioritate": "mare",
        "finalizata": False
    },
    3: {
        "titlu": "Invata un nou limbaj de programare",
        "prioritate": "mare",
        "finalizata": False
    },
    4: {
        "titlu": "Gateste o reteta noua",
        "prioritate": "mica",
        "finalizata": True
    },
    5: {
        "titlu": "Scrie un articol pe blog",
        "prioritate": "medie",
        "finalizata": False
    },
}

def calculeaza_progres(sarcini):
    total = len(sarcini)
    finalizate = 0
    for sarcina in sarcini.values():
        if sarcina["finalizata"]:
            finalizate += 1
    if total == 0:
        progres = 0
    else:
        progres = (finalizate / total) * 100
    return finalizate, total, round(progres, 2)

templates = Jinja2Templates(directory="templates")

def obtine_vremea(oras):
    url="https://api.openweathermap.org/data/2.5/weather"
    parms = {
        "q": oras,
        "appid": CHEIE_WEATHER_API,
        "units": "metric",
        "lang": "ro"
    }
    raspuns = requests.get(url, params=parms, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()

def obtine_prognoza(oras):
    url="https://api.openweathermap.org/data/2.5/forecast"
    parms = {
        "q": oras,
        "appid": CHEIE_WEATHER_API,
        "units": "metric",
        "lang": "ro"
    }
    raspuns = requests.get(url, params=parms, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()

def calculeaza_temperatura(zile):
    rezultate = {}
    for ziua, intervale in zile.items():
        temperatura_minima = []
        temperatura_maxima = []
        for x in intervale:
            temperatura_minima.append(x["main"]["temp"])
            temperatura_maxima.append(x["main"]["temp_max"])
        media_minima = sum(temperatura_minima) / len(temperatura_minima)
        media_maxima = sum(temperatura_maxima) / len(temperatura_maxima)
        rezultate[ziua] = {"temp_min": round(media_minima, 1), "temp_max": round(media_maxima, 1)}
    return rezultate

def salut(ora:int):
    if ora < 12:
        return "Bună dimineața!"
    elif ora < 18:
        return "Bună ziua!"
    else:
        return "Bună seara!"

def citatul_zilei():
    url = "https://zenquotes.io/api/today"
    try:
        raspuns = requests.get(url, timeout=5)
        raspuns.raise_for_status()
        data = raspuns.json()
        citat = {
            "text": data[0]["q"],
            "autor": data[0]["a"]
        }
        return citat
    except requests.exceptions.RequestException as e:
        return {"eroare": str(e)}

@app.get("/")
def radacina():
    """Ruta / ne trimite direct la /home."""
    return RedirectResponse("/home")

zile_saptamana = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]

@app.post("/sarcini/adauga")
def adauga_sarcina(titlu: str =Form(...), prioritate: str = Form(...)):
    id_nou = max(sarcini.keys(), default=0) + 1
    sarcini[id_nou] = {
        "titlu": titlu,
        "prioritate": prioritate,
        "finalizata": False
    }
    return RedirectResponse("/home", status_code=303)

@app.post("/sarcini/{id}/bifeaza")
def bifeaza_sarcina(id: int):
    sarcini[id]["finalizata"] = not sarcini[id]["finalizata"]
    return RedirectResponse("/home", status_code=303)

@app.post("/sarcini/{id}/sterge")
def sterge_sarcina(id: int):
    if id in sarcini:
        del sarcini[id]
    return RedirectResponse("/home", status_code=303)

@app.get("/home")
def home(request: Request):
    acum = datetime.now()
    ora = acum.strftime("%H:%M")
    mesaj=salut(acum.hour)
    oras = request.query_params.get("oras", "Iasi")
    temperaturi_forecast = {}
    finalizate, total, progres = calculeaza_progres(sarcini)
    citat = citatul_zilei()
    try:
        vreme = obtine_vremea(oras)
        prognoza = obtine_prognoza(oras)
        zile = {}
        for x in prognoza["list"]:
            data = datetime.strptime(x["dt_txt"], "%Y-%m-%d %H:%M:%S")
            ziua = zile_saptamana[data.weekday()]
            if ziua not in zile:
                zile[ziua] = []
            zile[ziua].append(x)
        temperaturi_forecast = calculeaza_temperatura(zile)
        eroare = None
    except requests.exceptions.RequestException as e:
        vreme = None
        eroare = str(e)
    
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "ora": ora,
            "salut": mesaj,
            "oras": oras,
            "vreme": vreme,
            "prognoza": prognoza,
            "eroare": eroare,
            "temperaturi_forecast": temperaturi_forecast,
            "sarcini": sarcini,
            "finalizate": finalizate,
            "total": total,
            "progres": progres,
            "citat": citat,
        },
    )


@app.get("/style.css")
def stil():

    return FileResponse("templates/style.css")

 