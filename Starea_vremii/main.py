import os
from dotenv import load_dotenv

load_dotenv()
##sa se modifice calea din linia de mai jos##
cheie_api_openweather = os.getenv("API_KEY")
print(cheie_api_openweather)