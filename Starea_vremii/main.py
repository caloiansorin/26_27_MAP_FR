import os
from dotenv import load_dotenv

# pip3 install dotenv
load_dotenv("/Users/spikecsi/Desktop/Projects/MAP FR/26_27_MAP_FR/.env")
cheie_api_openweathermap = os.getenv("API_KEY")
print(cheie_api_openweathermap)
