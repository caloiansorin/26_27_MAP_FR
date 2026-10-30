import os
from dotenv import load_dotenv

# pip3 install dotenv
load_dotenv(dotenv_path="/home/nistor/Workspace/1_inbox/academic/ub/anul2/RCSP/26_27_MAP_FR/.env")
cheie_api_openweathermap: str | None = os.getenv(key="API_Key")
print(cheie_api_openweathermap)