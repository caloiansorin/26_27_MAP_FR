# Starea vremii

Aplicatie web (FastAPI) care afiseaza vremea curenta pentru un oras folosind API-ul OpenWeatherMap si salveaza fiecare cautare intr-o baza de date SQLite locala (`vreme.db`).

## Structura proiectului

```
Starea_vremii/
├── main.py         # aplicatia FastAPI (rutele /, /api/vreme, /api/istoric)
├── meteo.py        # apelurile catre OpenWeatherMap (geocodare + vreme)
├── baza_date.py    # crearea tabelului, salvarea si citirea din vreme.db
├── test.py         # script de test care citeste istoricul prin API
├── vreme.db        # baza de date SQLite (se creeaza automat daca lipseste)
└── templates/
    ├── index.html  # pagina principala
    └── header.html # componenta reutilizabila (antet + navigare)
```

## 1. Cerinte

- Python 3.10 sau mai nou (testat cu Python 3.12)
- O cheie API gratuita de la [OpenWeatherMap](https://home.openweathermap.org/api_keys)

## 2. Instalarea bibliotecilor

Din folderul `Starea_vremii`, ideal intr-un mediu virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate        # pe Windows: .venv\Scripts\activate

pip install fastapi "uvicorn[standard]" jinja2 requests python-dotenv
```

| Biblioteca      | La ce foloseste                                      |
| --------------- | ---------------------------------------------------- |
| `fastapi`       | framework-ul web                                     |
| `uvicorn`       | serverul care ruleaza aplicatia                      |
| `jinja2`        | randarea sabloanelor HTML din `templates/`           |
| `requests`      | apelurile HTTP catre OpenWeatherMap (si in `test.py`) |
| `python-dotenv` | citirea variabilelor din fisierul `.env`             |

> Atentie: pachetul corect este `python-dotenv`, nu `dotenv`.

`sqlite3` si `pathlib` fac parte din biblioteca standard Python, nu trebuie instalate.

## 3. Fisierul `.env`

Creeaza un fisier `.env` (nu se urca pe GitHub, este in `.gitignore`) cu urmatorul continut:

```env
API_KEY=cheia_ta_openweathermap
URL_API_G=http://api.openweathermap.org/geo/1.0/direct
URL_API_O=https://api.openweathermap.org/data/2.5/weather
```

## 4. Caile care trebuie modificate manual

Proiectul contine doua cai absolute, specifice calculatorului pe care a fost scris. **Inlocuieste-le cu caile de pe calculatorul tau**, altfel aplicatia nu va porni sau nu va gasi cheia API.

### `meteo.py` – calea catre `.env`

```python
load_dotenv("/Users/spikecsi/Desktop/Projects/MAP FR/26_27_MAP_FR/.env")
```

Schimb-o cu calea completa catre fisierul tau `.env`, de exemplu:

```python
load_dotenv("C:/Users/NumeleTau/Proiecte/26_27_MAP_FR/.env")   # Windows
load_dotenv("/home/numele_tau/26_27_MAP_FR/.env")               # Linux / macOS
```

### `baza_date.py` – calea catre baza de date

```python
cale_db = "/Users/spikecsi/Desktop/Projects/MAP FR/26_27_MAP_FR/Starea_vremii/vreme.db"
```

Schimb-o cu calea unde vrei sa fie salvat `vreme.db` (de obicei chiar folderul `Starea_vremii`). Daca fisierul nu exista, tabelul se creeaza automat la pornirea aplicatiei.

## 5. Pornirea aplicatiei

Din folderul `Starea_vremii`:

```bash
uvicorn main:app --reload --ws none
```

Apoi deschide in browser: <http://127.0.0.1:8000>

## 6. Rute disponibile

| Ruta                       | Descriere                                              |
| -------------------------- | ------------------------------------------------------ |
| `/`                        | pagina principala cu formularul de cautare             |
| `/?oras=Bacau`             | afiseaza vremea pentru oras si o salveaza in baza de date |
| `/api/vreme?oras=Bacau`    | returneaza vremea in format JSON si o salveaza         |
| `/api/istoric`             | returneaza toate cautarile salvate, in format JSON     |
| `/docs`                    | documentatia interactiva generata de FastAPI           |

## 7. Testare

Cu serverul pornit, intr-un alt terminal:

```bash
python3 test.py
```

Scriptul citeste istoricul de la `/api/istoric` si afiseaza inregistrarile pentru orasul Bacau.
