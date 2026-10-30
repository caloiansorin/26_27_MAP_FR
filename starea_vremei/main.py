import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
cheie_api_openwheathermap: str | None = os.getenv(key="API_KEY")
print(cheie_api_openwheathermap)