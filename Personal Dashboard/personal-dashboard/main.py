from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from datetime import datetime
import requests

load_dotenv()
CHEIE_OPEN_WEATHER = os.getenv("OPEN_WEATHER_API_KEY")
numele_tau = os.getenv("NUME")

app = FastAPI()

sarcini = {
    1: {
        "titlu": "Citeste capitolul 3 din cartea de Python",
        "prioritate": "medie",
        "finalizata": True,
    },
    2: {
        "titlu": "Scrie un program care sa afiseze vremea",
        "prioritate": "mare",
        "finalizata": False,
    },
    3: {
        "titlu": "Mergi la sala",
        "prioritate": "mica",
        "finalizata": False,
    },
    4: {
        "titlu": "Invata FastAPI",
        "prioritate": "mare",
        "finalizata": False,
    },
    5: {
        "titlu": "Invata Jinja2",
        "prioritate": "mare",
        "finalizata": False,
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
        progres = round((finalizate / total) * 100)
    return finalizate, total, progres


def obtine_vremea(oras):
    url = "https://api.openweathermap.org/data/2.5/weather"
    parms = {
        "q": oras,
        "appid": CHEIE_OPEN_WEATHER,
        "units": "metric",
        "lang": "ro",
    }
    raspuns = requests.get(url, params=parms, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()


def obtine_prognoza(oras):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    parms = {
        "q": oras,
        "appid": CHEIE_OPEN_WEATHER,
        "units": "metric",
        "lang": "ro",
    }
    raspuns = requests.get(url, params=parms, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()


templates = Jinja2Templates(directory="templates")

zile_saptamana = [
    "Luni",
    "Marți",
    "Miercuri",
    "Joi",
    "Vineri",
    "Sâmbătă",
    "Duminică",
]


def calculeaza_temperatura(lista_prognoza):
    zile = {}
    for x in lista_prognoza:
        data = datetime.strptime(x["dt_txt"], "%Y-%m-%d %H:%M:%S")
        ziua = zile_saptamana[data.weekday()]

        if ziua not in zile:
            zile[ziua] = []
        zile[ziua].append(x["main"]["temp"])

    rezultate = {}
    for ziua, temperaturi in zile.items():
        rezultate[ziua] = {
            "min": round(min(temperaturi), 1),
            "max": round(max(temperaturi), 1),
            "medie": round(sum(temperaturi) / len(temperaturi), 1),
        }
    return rezultate


def salut(ora):
    if ora < 12:
        return "Bună dimineața!"
    elif ora < 18:
        return "Bună ziua!"
    else:
        return "Bună seara!"


@app.get("/")
def radacina():
    return RedirectResponse("/home")


@app.get("/home")
def home(request: Request):
    acum = datetime.now()
    ora = acum.strftime("%H:%M")
    mesaj = salut(acum.hour)
    oras = request.query_params.get("oras", "Bacău")
    finalizate, total, progres = calculeaza_progres(sarcini)

    try:
        vreme = obtine_vremea(oras)
        prognoza = obtine_prognoza(oras)
        temperaturi_forecast = calculeaza_temperatura(prognoza["list"])
        temperaturi_forecast = dict(list(temperaturi_forecast.items())[1:])
        eroare = None
    except requests.exceptions.RequestException as e:
        vreme = None
        temperaturi_forecast = {}
        eroare = f"Eroare la obținerea vremii: {e}"

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "ora": ora,
            "salut": mesaj,
            "vreme": vreme,
            "eroare": eroare,
            "oras": oras,
            "temperaturi_forecast": temperaturi_forecast,
            "sarcini": sarcini,
            "finalizate": finalizate,
            "total": total,
            "progres": progres,
        },
    )


@app.post("/sarcini/adauga")
def adauga_sarcina(titlu: str = Form(...), prioritate: str = Form("medie")):
    urmatorul_id = max(sarcini.keys(), default=0) + 1
    sarcini[urmatorul_id] = {
        "titlu": titlu,
        "prioritate": prioritate,
        "finalizata": False,
    }
    return RedirectResponse("/home", status_code=303)


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


