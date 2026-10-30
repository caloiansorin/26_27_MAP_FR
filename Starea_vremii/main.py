import os
from dotenv import load_dotenv
# pip3 install dotenv
## https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}

load_dotenv(dotenv_path="C:/Users/AlexPC/26_27_MAP_FR/.env")
cheie_api_openweathermap: str | None = os.getenv(key="API_KEY")
print(cheie_api_openweathermap)

URL_API: str | None = os.getenv(key="URL_API")

