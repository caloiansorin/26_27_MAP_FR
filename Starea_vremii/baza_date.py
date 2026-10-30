import sqlite3
from pathlib import Path

proiect = Path(__file__).resolve().parent
cale_db = proiect / "vreme.db"


def creare_tabel():
    with sqlite3.connect(cale_db) as conexiune:
        conexiune.execute("""
        CREATE TABLE IF NOT EXISTS vreme (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        oras TEXT NOT NULL,
        stare_vreme TEXT NOT NULL,
        viteza_vant REAL NOT NULL,  
        temperatura REAL NOT NULL,
        iconita TEXT NOT NULL,
        data_inregistrare TEXT DEFAULT CURRENT_TIMESTAMP)
        """)


def salvare_vreme(oras, stare_vreme, viteza_vant, temperatura, iconita):
    with sqlite3.connect(cale_db) as conexiune:
        conexiune.execute(
            """
        INSERT INTO vreme (oras, stare_vreme, viteza_vant, temperatura, iconita)
        VALUES (?, ?, ?, ?, ?)
        """,
            (oras, stare_vreme, viteza_vant, temperatura, iconita),
        )


def citire_vreme():
    with sqlite3.connect(cale_db) as conexiune:
        conexiune.row_factory = sqlite3.Row
        rezultat = conexiune.execute("""
        SELECT * FROM vreme ORDER BY id ASC
        """).fetchall()
        return [dict(rand) for rand in rezultat]