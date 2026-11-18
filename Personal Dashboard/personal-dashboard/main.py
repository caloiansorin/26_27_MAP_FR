# uvicorn main:app --reload

from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import sqlite3
import time
from datetime import datetime, date
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

# Variabile globale pentru cache-ul citatului
cache_citat = {
    "data": None,
    "citat": "Cea mai mare glorie nu o obții atunci când nu cazi niciodată, ci atunci când te ridici după fiecare cădere.",
    "autor": "Confucius"
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

def obtine_curs_valutar():
    # Folosim noul endpoint v2 de la api.frankfurter.dev
    url = "https://api.frankfurter.dev/v2/rates"
    params = {
        "base": "RON",
        "quotes": "EUR,USD,GBP"
    }
    try:
        raspuns = requests.get(url, params=params, timeout=5)
        raspuns.raise_for_status()
        date = raspuns.json()
        
        rates = {}
        data_actualizarii = "-"
        
        if isinstance(date, list) and len(date) > 0:
            for item in date:
                quote = item.get("quote")
                rate = item.get("rate")
                if quote and rate:
                    # Deoarece baza este RON, rate-ul primit ne spune câți EUR/USD/GBP obținem pe 1 RON.
                    # Noi vrem inversul (câți RON costă 1 EUR/USD/GBP), adică 1 / rate.
                    rates[quote] = round(1 / rate, 4)
                if "date" in item:
                    data_actualizarii = item.get("date")
        
        return {
            "EUR": rates.get("EUR", 4.9700),
            "USD": rates.get("USD", 4.6000),
            "GBP": rates.get("GBP", 5.8000),
            "data": data_actualizarii
        }
    except Exception as e:
        print(f"Eroare curs valutar: {e}")
        # Valori de fallback în caz de eroare de rețea
        return {"EUR": 4.97, "USD": 4.60, "GBP": 5.80, "data": "Indisponibil"}

def obtine_citat_zilei():
    global cache_citat
    azi = datetime.now().strftime("%Y-%m-%d")

    # Dacă am preluat deja citatul astăzi, îl refolosim din memorie (fără apel API)
    if cache_citat["data"] == azi:
        return {
            "citat": cache_citat["citat"],
            "autor": cache_citat["autor"]
        }

    # ALtfel, apelam API-ul cel mult odata pe zi
    url = "https://zenquotes.io/api/today"
    try:
        raspuns = requests.get(url, timeout=5)
        raspuns.raise_for_status()
        date = raspuns.json()
        
        if isinstance(date, list) and len(date) > 0:
            citat_obj = date[0]
            # Actualizam cache-ul cu noua zi si noul citat
            cache_citat["data"] = azi
            cache_citat["citat"] = citat_obj.get("q", cache_citat["citat"])
            cache_citat["autor"] = citat_obj.get("a", cache_citat["autor"])
    except Exception as e:
        print(f"Eroare citat zilei (se folosește fallback/cache vechi): {e}")
    
    return {
        "citat": cache_citat["citat"],
        "autor": cache_citat["autor"]
    }

def obtine_urmatoarea_sarbatoare():
    an_curent = datetime.now().year
    url = f"https://date.nager.at/api/v3/PublicHolidays/{an_curent}/RO"
    
    try:
        raspuns = requests.get(url, timeout=5)
        raspuns.raise_for_status()
        sarbatori = raspuns.json()
        
        azi = date.today()
        
        for s in sarbatori:
            data_sarbatoare = datetime.strptime(s.get("date"), "%Y-%m-%d").date()
            if data_sarbatoare >= azi:
                # Calculăm diferența de zile
                diferenta_zile = (data_sarbatoare - azi).days
                
                # Formatăm textul conform cerinței
                if diferenta_zile == 0:
                    text_zile = "azi"
                elif diferenta_zile == 1:
                    text_zile = "mâine"
                elif diferenta_zile == 2:
                    text_zile = "2 zile"
                else:
                    text_zile = f"{diferenta_zile} zile"
                
                zi = data_sarbatoare.day
                luni_ro_local = ["", "ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"]
                luna_nume = luni_ro_local[data_sarbatoare.month]
                
                return {
                    "nume": s.get("localName"),
                    "data": f"{zi} {luna_nume}",
                    "text_zile": text_zile
                }
    except Exception as e:
        print(f"Eroare preluare sărbători legale: {e}")
    
    return {
        "nume": "Crăciunul",
        "data": "25 decembrie",
        "text_zile": "curând"
    }

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

    # Preluare curs valutar
    curs_valutar = obtine_curs_valutar()

    # Preluare citatul zilei
    citat_zilei = obtine_citat_zilei()

    # Preluare urmatoarea sarbatoare legala
    urmatoarea_sarbatoare = obtine_urmatoarea_sarbatoare()

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
            "curs_valutar": curs_valutar, # Trimitem cursurile valutare in sablon
            "citat_zilei": citat_zilei,
            "urmatoarea_sarbatoare": urmatoarea_sarbatoare,
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