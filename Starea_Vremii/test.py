import requests

raspuns = requests.get(
    "http://127.0.0.1:8000/api/istoric",
    timeout=5,
)

raspuns.raise_for_status()  # Ridică o excepție dacă răspunsul nu este 2xx
inregistrari_db = raspuns.json()
if not inregistrari_db:
    print("Nu există înregistrări în baza de date.")

for vreme in inregistrari_db:
    if vreme["oras"].strip().casefold() in ("Bacau", "bacau", "Bacău", "bacău"):
        print(
            f"ID: {vreme['id']}, Oras: {vreme['oras']}, Stare vreme: {vreme['stare_vreme']}, "
            f"Viteza vant: {vreme['viteza_vant']}, Temperatura: {vreme['temperatura']}, "
            f"Iconita: {vreme['iconita']}, Data inregistrare: {vreme['data_inregistrare']}"
        )