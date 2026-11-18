# uvicorn main:app --reload

from fastapi import FastAPI, Request, Form
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

# Adaugam dictionare pentru traducere zile si luni
zile_saptamana_ro = {
    0: "Luni", 1: "Marti", 2: "Miercuri", 3: "Joi",
    4: "Vineri", 5: "Sambata", 6: "Duminica"
}

luni_ro = {
    1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie",
    5: "Mai", 6: "Iunie", 7: "Iulie", 8: "August",
    9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"
}

# Lista globala care simuleaza baza de date
sarcini_db = [
    {"id": 1, "titlu": "Citește capitolul 3 la Baze de date", "prioritate": "medie", "done": True},
    {"id": 2, "titlu": "Trimite tema la Programare Web", "prioritate": "mare", "done": True},
    {"id": 3, "titlu": "Pregătește prezentarea pentru seminar", "prioritate": "mare", "done": False},
    {"id": 4, "titlu": "Cumpărături", "prioritate": "mica", "done": False},
    {"id": 5, "titlu": "Sală, ora 19:00", "prioritate": "medie", "done": False},
]

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

def obtine_prognoza(oras):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": oras,
        "appid": CHEIE_OPEN_WEATHER,
        "units": "metric",
        "lang": "ro",
    }
    raspuns = requests.get(url, params=params, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()

def calculeaza_temperatura(zile):
    rezultate = {}
    for ziua, intervale in zile.items():
        temperatura_minima = []
        temperatura_maxima = []
        for x in intervale:
            temperatura_minima.append(x["main"]["temp_min"])
            temperatura_maxima.append(x["main"]["temp_max"])
        media_minima = sum(temperatura_minima) / len(temperatura_minima)
        medie_maxima = sum(temperatura_maxima) / len(temperatura_maxima)
        rezultate[ziua] = {
            "temp_min": round(media_minima, 1),
            "temp_max": round(medie_maxima, 1),
        }
    return rezultate

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

zile_saptamana = [
    "Luni",
    "Marti",
    "Miercuri",
    "Joi",
    "Vineri",
    "Sambata",
    "Duminica"
]

@app.get("/home")
def home(request: Request):
    acum = datetime.now()
    ora = acum.strftime("%H:%M")
    mesaj = salut(acum.hour)

    # Generare data in backend
    ziua_saptamanii = zile_saptamana_ro[acum.weekday()]
    ziua_lunii = acum.day
    luna = luni_ro[acum.month]
    anul = acum.year

    data_curenta = f"{ziua_saptamanii}, {ziua_lunii} {luna} {anul}"

    oras = request.query_params.get("oras", "Bacău")
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
        temperaturi_forecast = dict(list(temperaturi_forecast.items())[1:6])
        for x, y in temperaturi_forecast.items():
            print(x, y["temp_min"], "|", y["temp_max"])
        eroare = None
    except requests.exceptions.RequestException as e:
        vreme = None
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
            "data_curenta": data_curenta, # Trimitem data in sablon
            "sarcini": sarcini_db, # Trimitem lista de sarcini catre sablon
        },
    )

# --- RUTA DE ADAUGARE SARCINĂ ---
@app.post("/sarcini/adauga")
def adauga_sarcina(titlu: str = Form(...), prioritate: str = Form(...)):
    # Generăm un ID unicat bazat pe lungimea listei + 1
    nou_id = max([s["id"] for s in sarcini_db], default=0) + 1
    
    noua_sarcina = {
        "id": nou_id,
        "titlu": titlu,
        "prioritate": prioritate,
        "done": False
    }
    
    sarcini_db.append(noua_sarcina)
    
    # Redirecționăm înapoi către pagina de home pentru a vedea modificarea
    return RedirectResponse("/home", status_code=303)

# --- RUTA DE BIFARE SARCINĂ ---
@app.post("/sarcini/{sarcina_id}/bifeaza")
def bifeaza_sarcina(sarcina_id: int):
    for sarcina in sarcini_db:
        if sarcina["id"] == sarcina_id:
            sarcina["done"] = not sarcina["done"]
            break
    return RedirectResponse("/home", status_code=303)

# --- RUTA DE ȘTERGERE SARCINĂ ---
@app.post("/sarcini/{sarcina_id}/sterge")
def sterge_sarcina(sarcina_id: int):
    global sarcini_db
    sarcini_db = [s for s in sarcini_db if s["id"] != sarcina_id]
    return RedirectResponse("/home", status_code=303)

@app.get("/style.css")
def stil():

    return FileResponse("templates/style.css")