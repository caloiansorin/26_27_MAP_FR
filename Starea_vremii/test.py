import requests

raspuns = requests.get(
    "http://127.0.0.1:8000/api/vreme",
    params={"oras": "Bucuresti"},
    timeout=5,
)


if raspuns.ok:
    data = raspuns.json()
    print("Oras:", data["oras"])
    print("Temperatura:", data["temperatura"])
    print("Vreme", data["stare_vreme"])
    print("Viteza vant:", data["viteza_vant"])
else:
    print("EROARE:", raspuns.json()["detail"])
