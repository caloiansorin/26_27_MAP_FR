import os
from dotenv import load_dotenv

# pip3 install dotenv
### NU UITATI SA MODIFICATI CALEA CATRE FISIERUL .env DIN LINIA DE MAI JOS ###
# https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
load_dotenv("/Users/spikecsi/Desktop/Projects/MAP FR/26_27_MAP_FR/.env")
cheie_api_openweathermap = os.getenv("API_KEY")
URL_API_O = os.getenv("URL_API_O")

print(
    f"Cheia API OpenWeatherMap: {cheie_api_openweathermap} iar URL API este: {URL_API_O}"
)
