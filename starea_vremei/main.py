import os
from dotenv import load_dotenv
from typing import Any
import requests

#https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
load_dotenv(dotenv_path="E:/Facultate/MAP/26_27_MAP_FR/.env")
cheie_api_openwheathermap: str | None = os.getenv(key="API_KEY")
url_geo: str | None = os.getenv(key="URL_GEO")
url_api_openwheather: str | None = os.getenv(key="URL_API_0")

def aflare_ll(oras) -> None:
    raspuns: Any = requests.get(
        url=url_geo, params={"q": oras, "appid": cheie_api_openwheathermap}    
    ).json()
    lat: Any = raspuns[0]["lat"]
    lon: Any = raspuns[0]["lon"]
    return raspuns
    
def afisare_informatii_meteo(latitudine, longitudine):
    raspuns: Any = requests.get(
        url=url_api_openwheather,
        params={
            "lat": latitudine,
            "lon": longitudine,
            "appid": cheie_api_openwheathermap,
            "lang": "ro",
            "units": "metric"
        },
    ).json()
    stare_vreme: Any = raspuns ["weather"] [0] ["description"]
    viteza_vant: Any = raspuns ["wind"] ["speed"]
    termperatura: Any = raspuns ["main"] ["temp"]
    return stare_vreme, viteza_vant, termperatura


afisare_informatii_meteo(oras=input("Introdu numele orasului: "))

    