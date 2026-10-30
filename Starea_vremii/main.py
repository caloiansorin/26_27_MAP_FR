from optparse import Values
import os
from dotenv import load_dotenv  # pip3 install dotenv
import requests  # DACA nu es instalata foloseste: pip3 install requests
from fastapi import FastAPI, Request
import requests
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from pathlib import Path

# DACA nu es instalata foloseste: pip3 install requests
### FORMA APEL API ###
# https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API key}

# http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
# pip3 install uv
# pip3 install fastapi

### NU UITATI SA MODIFICATI CALEA CATRE FISIERUL .env DIN LINIA DE MAI JOS ###
load_dotenv("E:/Facultate/MAP/26_27_MAP_FR/.env")
cheie_api_openweathermap = os.getenv("API_KEY")
url_geo = os.getenv("URL_API_G")
url_api_openweathermap = os.getenv("URL_API_O")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def aflare_ll(oras):
    raspuns = requests.get(
        url_geo, params={"q": oras, "appid": cheie_api_openweathermap}
    ).json()
    lat = raspuns[0]["lat"]
    lon = raspuns[0]["lon"]
    return lat, lon


def afisare_informatii_meteo(oras):
    latitudine = aflare_ll(oras)[0]
    longitudine = aflare_ll(oras)[1]
    raspuns = requests.get(
        url_api_openweathermap,
        params={
            "lat": latitudine,
            "lon": longitudine,
            "appid": cheie_api_openweathermap,
            "lang": "ro",
            "units": "metric",
        },
    ).json()
    stare_vreme = raspuns["weather"][0]["description"]
    viteza_vant = raspuns["wind"]["speed"]
    temperatura = raspuns["main"]["temp"]

    return stare_vreme, viteza_vant, temperatura


@app.get("/")
def home(request: Request, oras: str = ""):
    vreme = None
    eroare = None
    oras = oras.strip()
    if oras:
        try:
            vreme = prelucrare_si_salvare(oras)
        except requests.RequestException:
            raise HTTPException(
                status_code=502, detail="Eroare la apelul API-ului OpenWeatherMap"
            )

        except ValueError:
            raise HTTPException(
                status_code=404,
                detail="Nu am putut găsi informații despre vreme pentru orașul specificat.",
            )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "oras": oras,
            "vreme": vreme,
            "eroare": eroare,
        },
    )


@app.get("/api/vreme")
def api_vreme(oras: str = ""):
    oras = oras.strip()
    if not oras:
        raise HTTPException(
            status_code=400, detail="Parametrul 'oras' este obligatoriu."
        )

    try:
        return prelucrare_si_salvare(oras)
    except requests.RequestException:
        raise HTTPException(
            status_code=502, detail="Eroare la apelul API-ului OpenWeatherMap"
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Nu am putut găsi informații despre vreme pentru orașul specificat.",
        )


def prelucrare_si_salvare(oras):
    stare_vreme, viteza_vant, temperatura, iconita = afisare_informatii_meteo(oras)
    salvare_vreme(oras, stare_vreme, viteza_vant, temperatura, iconita)
    return {
        "oras": oras,
        "stare_vreme": stare_vreme,
        "viteza_vant": viteza_vant,
        "temperatura": temperatura,
        "iconita": iconita,
    }


@app.get("/api/istoric")
def api_istoric():
    return citire_vreme()


creare_tabel()
# uvicorn main:app --reload --ws none
