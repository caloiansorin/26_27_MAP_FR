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

#load_dotenv()
#CHEIE_OPEN_WEATHER = os.getenv("OPEN_WEATHER_API_KEY")
#NUME = os.getenv("NUME")

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

# Trecem modulul responsabil cu Vremea de la OpenWeather la Open-Meteo APIs.
# Deoarece Open-Meteo foloseste coordonate pentru locatie, vom include si o functie de conversie
def obtine_coordonate_oras(nume_oras):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": nume_oras, "count": 1, "language": "ro", "format": "json"}
    try:
        raspuns = requests.get(url, params=params, timeout=5)
        raspuns.raise_for_status()
        date = raspuns.json()
        if "results" in date and len(date["results"]) > 0:
            locatie = date["results"][0]
            return {
                "name": locatie.get("name"),
                "country": locatie.get("country", ""),
                "latitude": locatie.get("latitude"),
                "longitude": locatie.get("longitude")
            }
    except Exception:
        pass
    # Valoare de fallback (în caz de eroare sau dacă orașul nu este găsit)
    return {"name": "Iași", "country": "România", "latitude": 47.1585, "longitude": 27.6014}

def obtine_vremea(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m",
        "timezone": "auto"
    }
    raspuns = requests.get(url, params=params, timeout=5)
    raspuns.raise_for_status()
    return raspuns.json()


def obtine_prognoza(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
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

    nume_oras_cautat = request.query_params.get("oras", "Iasi")
    info_oras = obtine_coordonate_oras(nume_oras_cautat)
    try:
        data_vreme = obtine_vremea(info_oras["latitude"], info_oras["longitude"])
        data_prognoza = obtine_prognoza(info_oras["latitude"], info_oras["longitude"])

        # Salvam ora exacta a actualizarii
        ora_actualizarii = datetime.now().strftime("%H:%M")
        
        curent = data_vreme.get("current", {})
        vreme = {
            "name": info_oras["name"],
            "sys": {"country": info_oras.get("country", "")},
            "main": {
                "temp": curent.get("temperature_2m"),
                "humidity": curent.get("relative_humidity_2m"),
                "temp_min": data_prognoza.get("daily", {}).get("temperature_2m_min", [0])[0],
                "temp_max": data_prognoza.get("daily", {}).get("temperature_2m_max", [0])[0],
            },
            "wind": {
                "speed": curent.get("wind_speed_10m", 0) / 3.6
            },
            "weather": [{
                "description": "Vreme curentă",
                "icon": "01d"
            }]
        }
        
        daily = data_prognoza.get("daily", {})
        zile_forecast = daily.get("time", [])
        t_max = daily.get("temperature_2m_max", [])
        t_min = daily.get("temperature_2m_min", [])
        
        temperaturi_forecast = {}
        for i in range(1, min(6, len(zile_forecast))):
            data_zi = datetime.strptime(zile_forecast[i], "%Y-%m-%d")
            nume_zi_complet = zile_saptamana[data_zi.weekday()]

            # Pentru un plus estetic, limitez numele zilelor la primele 3 carcatere
            nume_zi = nume_zi_complet[:3]

            # Tot imbunatatire estetica, rotunjesc temperaturile la numar intreg
            temperaturi_forecast[nume_zi] = {
                "temp_max": round(t_max[i]) if t_max[i] is not None else 0,
                "temp_min": round(t_min[i]) if t_min[i] is not None else 0
            }

        eroare = None
    except requests.exceptions.RequestException as e:
        vreme = None
        ora_actualizarii = "--:--"
        temperaturi_forecast = {}
        eroare = f"Eroare la obținerea vremii: {e}"

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "ora": ora,
            "ora_actualizarii": ora_actualizarii, # Trimitem ora in sablon
            "salut": mesaj,
            "vreme": vreme,
            "eroare": eroare,
            "oras": info_oras["name"], # Afisam orasul cautat sau Iasi implicit
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