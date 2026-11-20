# Magazin online - respectarea principiilor SOLID
# Fiecare client trebuie sa aiba propriile comenzi
# Reducerile aplicate individual

# Bonus task: daca ar exista o campanie de BlackFriday unde sa zicem ca oricine achita cu Revolut, primeste o reducere extra de 5%

import json

# Clasa care tine datele unei comenzi
class Comanda:
    def __init__(self, produs, pret, cantitate):
        self.produs = produs
        self.pret = pret
        self.cantitate = cantitate

    def calculeaza_valoare(self):
        return self.pret * self.cantitate

    def to_dict(self):
        return {
            "produs": self.produs,
            "pret": self.pret,
            "cantitate": self.cantitate,
            "valoare_totala": self.calculeaza_valoare()
        }

# Clasa care tine datele despre client
class Client:
    def __init__(self, nume):
        self.nume = nume
        self.comenzi = []

    def adauga_comanda(self, comanda):
        self.comenzi.append(comanda)

# Clasa pentru calcule
class CalculatorTotal:
    def calculeaza(client):
        return sum(c.calculeaza_valoare() for c in client.comenzi)


# Clasele pentru Reduceri
class StrategieReducere:
    def aplica(self, suma):
        raise NotImplementedError

class ReducereStudent(StrategieReducere):
    def aplica(self, suma):
        return suma * 0.8   # Reducere 20%

class ReducereProfesor(StrategieReducere):
    def aplica(self, suma):
        return suma * 0.9  # Reducere 10%


# Clasele pentru plati
class MetodaPlata:
    def proceseaza(self, suma):
        raise NotImplementedError

class PlataCard(MetodaPlata):
    def proceseaza(self, suma):
        print(f"[Card] Suma de {suma} lei a fost înregistrată.")

class PlataCash(MetodaPlata):
    def proceseaza(self, suma):
        print(f"[Cash] Suma de {suma} lei a fost înregistrată.")

class PlataTransfer(MetodaPlata):
    def proceseaza(self, suma):
        print(f"[Transfer] Suma de {suma} lei a fost înregistrată.")


# Clasele pentru Facturare
class GeneratorFactura:
    def genereaza(self, client, suma_finala):
        raise NotImplementedError

class FacturaJson(GeneratorFactura):
    def genereaza(self, client, suma_finala):
        nume_fisier = f"factura_{client.nume}.json"
        date_factura = {
            "client": client.nume,
            "produse": [c.to_dict() for c in client.comenzi],
            "total_de_plata": suma_finala
        }
        with open(nume_fisier, "w", encoding="utf-8") as fisier:
            json.dump(date_factura, fisier, indent = 3, ensure_ascii=False)
        print(f"Am generat factura in format JSON -> '{nume_fisier}'.")

class FacturaTxt(GeneratorFactura):
    def genereaza(self, client, suma_finala):
        nume_fisier = f"factura_{client.nume}.txt"
        
        with open(nume_fisier, "w", encoding="utf-8") as fisier:
            fisier.write("========================================\n")
            fisier.write(f"FACTURĂ FISCALĂ - Client: {client.nume}\n")
            fisier.write("========================================\n")
            fisier.write("Produse comandate:\n")
            
            for c in client.comenzi:
                valoare_produs = c.calculeaza_valoare()
                fisier.write(f" - {c.cantitate}x {c.produs} | Preț unitar: {c.pret} lei | Total: {valoare_produs} lei\n")
                
            fisier.write("----------------------------------------\n")
            fisier.write(f"TOTAL DE PLATĂ (cu reducere): {suma_finala:.2f} lei\n")
            fisier.write("========================================\n")
            
        print(f"Am generat factura în format TXT -> '{nume_fisier}'.")


# Magazinul Online - va gestiona doar colectia de comenzi
class MagazinOnline:
    def __init__(self):
        self.clienti = []

    def adauga_client(self, client):
        self.clienti.append(client)


# --- UTILIZARE ---

magazin = MagazinOnline()

# Cream clienti cu comenzi proprii
client1 = Client("Ion")
client1.adauga_comanda(Comanda("Laptop", 3500, 1))
client2 = Client("Maria")
client2.adauga_comanda(Comanda("Mouse", 100, 2))
client3 = Client("Robert")
client3.adauga_comanda(Comanda("Tastatura", 200, 5))

magazin.adauga_client(client1)
magazin.adauga_client(client2)
magazin.adauga_client(client3)

# Procesam fluxul pentru un client anume
client_curent = client2
total_brut = CalculatorTotal.calculeaza(client_curent)
total_final = ReducereStudent().aplica(total_brut)

PlataTransfer().proceseaza(total_final)
FacturaJson().genereaza(client_curent, total_final)
FacturaTxt().genereaza(client_curent, total_final)