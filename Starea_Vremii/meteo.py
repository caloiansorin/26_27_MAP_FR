import os
from dotenv import load_dotenv  # pip3 install dotenv
from pathlib import Path
import requests

load_dotenv("/Users/spikecsi/Desktop/Projects/MAP FR/26_27_MAP_FR/.env")
cheie_api_openweathermap = os.getenv("API_KEY")
url_geo = os.getenv("URL_API_G")
url_api_openweathermap = os.getenv("URL_API_O")


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
    iconita = raspuns["weather"][0]["icon"]

    return stare_vreme, viteza_vant, temperatura, iconita