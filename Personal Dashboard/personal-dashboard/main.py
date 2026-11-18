# uvicorn main:app --reload

from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import sqlite3
import time
from datetime import datetime
import requests

load_dotenv()
CHEIE_OPEN_WEATHER = os.getenv("OPEN_WEATHER_API_KEY")
NUME = os.getenv("NUME")

app = FastAPI()

DB_FILE = "sarcini.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sarcini (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titlu TEXT NOT NULL,
            prioritate TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

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

# Preluam sarcinile ordonate direct din baza de date
def obtine_sarcini_din_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Ne permite să accesăm coloanele după nume
    cursor = conn.cursor()
    
    # Ordonare: întâi cele nefinalizate (done = 0), apoi după prioritate
    cursor.execute("""
        SELECT * FROM sarcini 
        ORDER BY done ASC, 
        CASE prioritate 
            WHEN 'mare' THEN 1 
            WHEN 'medie' THEN 2 
            WHEN 'mica' THEN 3 
            ELSE 4 
        END ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    # Convertim rândurile în dicționare obișnuite
    return [dict(row) for row in rows]

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

    # Preluam sarcinile direct din baza de date SQLite
    sarcini_ordonate = obtine_sarcini_din_db()

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
            "sarcini": sarcini_ordonate, # Trimitem lista de sarcini ordonata catre sablon
        },
    )

# --- RUTA DE ADAUGARE SARCINĂ ---
@app.post("/sarcini/adauga")
def adauga_sarcina(titlu: str = Form(...), prioritate: str = Form(...)):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sarcini (titlu, prioritate, done) VALUES (?, ?, ?)",
        (titlu, prioritate, False)
    )
    conn.commit()
    conn.close()
    
    # Redirecționăm înapoi către pagina de home pentru a vedea modificarea
    return RedirectResponse("/home", status_code=303)

# --- RUTA DE BIFARE SARCINĂ ---
@app.post("/sarcini/{sarcina_id}/bifeaza")
def bifeaza_sarcina(sarcina_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Inversăm starea curentă a lui 'done' (1 devine 0, 0 devine 1)
    cursor.execute("UPDATE sarcini SET done = NOT done WHERE id = ?", (sarcina_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/home", status_code=303)

# --- RUTA DE ȘTERGERE SARCINĂ ---
@app.post("/sarcini/{sarcina_id}/sterge")
def sterge_sarcina(sarcina_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sarcini WHERE id = ?", (sarcina_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/home", status_code=303)

@app.get("/style.css")
def stil():

    return FileResponse("templates/style.css")