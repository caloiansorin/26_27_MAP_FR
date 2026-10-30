import os
from dotenv import load_dotenv

load_dotenv()
cheie_api_openweather = os.getenv("API_KEY")
print(cheie_api_openweather)