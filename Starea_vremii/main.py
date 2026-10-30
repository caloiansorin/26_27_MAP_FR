from optparse import Values
import os
from dotenv import load_dotenv  # pip3 install dotenv
import requests  # DACA nu es instalata foloseste: pip3 install requests
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from pathlib import Path

from baza_date import creare_tabel, salvare_vreme, citire_vreme
from meteo import afisare_informatii_meteo, aflare_ll

app = FastAPI()
proiect = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=proiect / "templates")


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
