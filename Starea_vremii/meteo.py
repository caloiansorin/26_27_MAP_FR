import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def aflare_ll(oras: str):
    """Opțional: Funcție pentru a căuta coordonatele orașului sau direct datele geografice."""
    # Dacă folosești endpoint-ul direct pe oraș, poți adapta această funcție sau o poți păstra ca helper.
    pass


def afisare_informatii_meteo(oras: str):
    """Interoghează API-ul OpenWeatherMap pentru orașul dat și returnează:

    stare_vreme, viteza_vant, temperatura, iconita
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={oras}&units=metric&appid={API_KEY}&lang=ro"

    raspuns = requests.get(url, timeout=5)
    raspuns.raise_for_status()
    data = raspuns.json()

    # Extragem informațiile cerute de aplicație
    temperatura = data["main"]["temp"]
    viteza_vant = data["wind"]["speed"]
    stare_vreme = data["weather"][0]["description"]
    iconita = data["weather"][0]["icon"]

    return stare_vreme, viteza_vant, temperatura, iconita


# Codul de testare mutat în blocul condțional (nu se execută la import)
if __name__ == "__main__":
    try:
        stare, vant, temp, icon = afisare_informatii_meteo("Bucuresti")
        print(
            f"Test cu succes: Bucuresti - Temp: {temp}°C, Vânt: {vant} m/s, Stare: {stare}"
        )
    except Exception as e:
        print(f"Eroare la testare: {e}")