import os
from dotenv import load_dotenv

# pip3 install dotenv
### NU UITATI SA MODIFICATI CALEA CATRE FISIERUL .env DIN LINIA DE MAI JOS ###
load_dotenv(".env")
cheie_api_openweathermap = os.getenv("API_KEY")
print(cheie_api_openweathermap)
