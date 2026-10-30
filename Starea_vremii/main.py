import os
from dotenv import load_dotenv  # pip3 install dotenv
import requests  # DACA nu es instalata foloseste: pip3 install requests
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

### FORMA APEL API ###
# https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API key}

# http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
# pip3 install uv
# pip3 install fastapi

### NU UITATI SA MODIFICATI CALEA CATRE FISIERUL .env DIN LINIA DE MAI JOS ###
load_dotenv("/home/nistor/Workspace/1_inbox/academic/ub/anul2/RCSP/26_27_MAP_FR/.env")
cheie_api_openweathermap = os.getenv("API_KEY")
url_geo = os.getenv("URL_API_G")
url_api_openweathermap = os.getenv("URL_API_O")

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
            stare_vreme, viteza_vant, temperatura = afisare_informatii_meteo(oras)
            vreme = {
                "stare_vreme": stare_vreme,
                "viteza_vant": viteza_vant,
                "temperatura": temperatura,
            }
        except requests.RequestException as e:
            eroare = "EROARE LA APELUL API !"

        except Exception as e:
            eroare = "ORASUL NU A FOST GASIT !"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "oras": oras,
            "vreme": vreme,
            "eroare": eroare,
        },
    )


# uvicorn main:app --reload --ws none