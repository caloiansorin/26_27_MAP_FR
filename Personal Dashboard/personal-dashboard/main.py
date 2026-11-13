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
CHEIE_OPEN_WEATHER = os.getenv("OPEN_WEATHER_API_KEY")
numele_tau = os.getenv("NUME")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

sarcini = {
    1: {
        "titlu":"Citeste capitolul 3 din cartea de Python",
        "prioritate":"medie",
        "finalizata":True
    },
    2: {
        "titlu":"Scrie un program care sa afiseze vremea",
        "prioritate":"mare",
        "finalizata":False
    },
    3: {
        "titlu":"Mergi la sala",
        "prioritate":"mica",
        "finalizata":False },
    4: {
        "titlu":"Invata FastAPI",
        "prioritate":"mare",
        "finalizata":False
    },
    5: {
        "titlu":"Invata Jinja2",
        "prioritate":"mare",
        "finalizata":False
    }  
}

def calculeaza_progres(sarcini):
    total = len(sarcini)
    finalizate = 0
    for sarcina in sarcini.values():
        if sarcina["finalizata"]:
            finalizate +=1
        if total == 0:
            progres = 0
    progres = (finalizate / total) * 100
    return finalizate, total, progres

def obtine_vremea(oras):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": oras,
        "appid": CHEIE_OPEN_WEATHER,
        "units": "metric",
        "lang": "ro"
    }
    raspuns = requests.get(url, params=params, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()

def obtine_prognoza(oras):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": oras,
        "appid": CHEIE_OPEN_WEATHER,
        "units": "metric",
        "lang": "ro"
    }
    raspuns = requests.get(url, params=params, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()

zile_saptamana = ["Luni", "Marti", "Miercuri", "Joi", "Vineri", "Sambata", "Duminica"]

def salut(ora: int) -> str:
    if ora < 12:
        return "Buna Dimineata!"
    if ora < 18:
        return "Buna ziua!"
    else:
        return "Buna seara!"
    
def calculeaza_temperatura(zile):
    rezultate = {}
    for ziua, intervale in zile.items():
        temperatura_minima = []
        temperatura_maxima = []
        for x in intervale:
            temperatura_minima.append(x["main"]["temp_min"])
            temperatura_maxima.append(x["main"]["temp_max"])
        media_minima = sum(temperatura_minima) / len(temperatura_minima)
        media_maxima = sum(temperatura_maxima) / len(temperatura_maxima)
        rezultate[ziua] = {"temp_min": round(media_minima, 1), "temp_max": round(media_maxima, 1)}
    return rezultate
        

@app.post("/adauga")
def adauga_sarcina(request: Request):
    return RedirectResponse("/home", status_code=303)

@app.post("/sarcini/adauga")
def adauga_sarcina(titlu: str = Form(...), prioritate: str = Form(...)):
    id_nou = max(sarcini.keys(), default=0) + 1
    sarcini[id_nou] = {
        "titlu": titlu,
        "prioritate": prioritate,
        "finalizata": False,
    }
    return RedirectResponse("/home", status_code=303)
    

@app.get("/")
def radacina():
    """Ruta / ne trimite direct la /home."""
    return RedirectResponse("/home")

@app.get("/home")
def home(request: Request):
    acum: datetime = datetime.now()
    ora: str = acum.strftime(format="%H:%M")
    mesaj = salut(acum.hour)
    oras = request.query_params.get("oras", "Roman")
    finalizate, total, progres = calculeaza_progres(sarcini)
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
        temps_forecast = calculeaza_temperatura(zile)      
        eroare = None
        finalizate,total,progres = calculeaza_progres(sarcini)
        
    except requests.exceptions.RequestException as e:
        vreme = None
        eroare = f"Eroare la obtinerea vremii: {e}"
    
    
    return templates.TemplateResponse(
        request,
        "index.html",
        {"ora": ora,
         "salut": mesaj,
         "vreme": vreme,
         "eroare": eroare,
         "oras": oras,
         "temps_forecast": temps_forecast,
         "sarcini": sarcini,
         "finalizate": finalizate,
         "total": total,
         "progres": progres
         },
    )
    
@app.post("/sarcini/{id_sarcina}/bifeaza")
def bifeaza_sarcina(id_sarcina: int):
    if id_sarcina in sarcini:
        sarcini[id_sarcina]["finalizata"] = not sarcini[id_sarcina]["finalizata"]
    return RedirectResponse("/home", status_code=303)


@app.post("/sarcini/{id_sarcina}/sterge")
def sterge_sarcina(id_sarcina: int):
    if id_sarcina in sarcini:
        del sarcini[id_sarcina]
    return RedirectResponse("/home", status_code=303)


@app.get("/style.css")
def stil():
    
    return FileResponse("templates/style.css")

# Baza de date pentru aplicatie
# Implementare carduri ramase