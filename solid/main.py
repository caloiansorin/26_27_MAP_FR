# SOLID
from dataclasses import asdict
import json
import csv
from os import write


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
    def salveaza(self, imprumuturi):
        raise NotImplementedError


class SalvareTXT(SalvareImprumuturi):
    def salveaza(self, imprumuturi):
        with open("D:/Cursuri_Facultate/RCSP/26_27_MAP_FR/solid/imprumuturi.txt", "w") as fisier:
            for imprumut in imprumuturi:
                fisier.write(str(imprumut) + "\n")


class SalvareJSON(SalvareImprumuturi):
    def salveaza(self, imprumuturi):
        with open("D:/Cursuri_Facultate/RCSP/26_27_MAP_FR/solid/imprumuturi.json", "w") as fisier:
            json.dump(imprumuturi, fisier, indent=3)


class SalvareCSV(SalvareImprumuturi):
    def salveaza(self, imprumuturi):
        with open(
            "D:/Cursuri_Facultate/RCSP/26_27_MAP_FR/solid/imprumuturi.csv", "w", newline=""
        ) as fisier:
            writer = csv.DictWriter(fisier, fieldnames=["nume", "echipament"])
            writer.writeheader()
            writer.writerows(imprumuturi)


### INCLACA PRINCIPIUL LISKOV ###
class SalvareFalsa(SalvareImprumuturi):
    def salveaza(self, imprumuturi):
        print("AM SALVAT IMPRUMUTURILE")

    
def efectueaza_salavare(salvator: SalvareImprumuturi, imprumuturi):
    salvator.salveaza(imprumuturi)


registru = RegistruImprumuturi()
registru.adauga("Ana", "Kit Arduino")
registru.adauga("Mihai", "Tastatura")
raport = RaportImprumuturi()
raport.afiseaza(registru.imprumuturi)
# salvare = SalvareTXT()
#salvare.salveaza(registru.imprumuturi)
efectueaza_salavare(SalvareTXT(), registru.imprumuturi)
