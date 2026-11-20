# Registru Echipament Laborator - Principiile SOLID
from dataclasses import asdict
import json


class RegistruImprumuturi:
    def __init__(self):
        self.imprumuturi = []

    def adauga(self, nume, echipament):
        imprumut = {
            "nume": nume,
            "echipament": echipament,
        }
        self.imprumuturi.append(imprumut)


class RaportImprumuturi:
    def afiseaza(self, imprumuturi):
        for imprumut in imprumuturi:
            print(imprumut)


class SalvareImprumuturi:
    def salveaza(self, imprumuturi, format):
        if format == "txt":
            with open("/Users/spikecsi/Desktop/SOLID/imprumuturi.txt", "w") as fisier:
                for imprumut in imprumuturi:
                    fisier.write(str(imprumut) + "\n")
        elif format == "json":
            with open("/Users/spikecsi/Desktop/SOLID/imprumuturi.txt", "w") as fisier:
                json.dump(imprumuturi, fisier)
 
registru = RegistruImprumuturi()
registru.adauga("Ana", "Kit Arduino")
registru.adauga("Marcel", "Kit Raspberry")
registru.adauga("Ionel", "Laptop Thinkpad x230")

raport = RaportImprumuturi()
raport.afiseaza(registru.imprumuturi)

salvare = SalvareImprumuturi()
salvare.salveaza(registru.imprumuturi, json)