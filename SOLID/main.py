# Registru Echipament Laborator - Principiile SOLID
from dataclasses import asdict
import json
import os
import csv


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
    def salveaza(self,imprumuturi):
        with open("/home/nistor/Workspace/1_inbox/academic/ub/anul2/RCSP/26_27_MAP_FR/SOLID/imprumuturi.txt", "w") as fisier:
            for imprumut in imprumuturi:
                    fisier.write(str(imprumut) + "\n")

class SalvareJSON(SalvareImprumuturi):
    def salveaza(self, imprumuturi):
        with open("/home/nistor/Workspace/1_inbox/academic/ub/anul2/RCSP/26_27_MAP_FR/SOLID/imprumuturi.json", "w") as fisier:
            json.dump(imprumuturi, fisier, indent = 3)

class SalvareCSV(SalvareImprumuturi):
    def salveaza(self, imprumuturi):
        with open("/home/nistor/Workspace/1_inbox/academic/ub/anul2/RCSP/26_27_MAP_FR/SOLID/imprumuturi.csv", "w", newline="") as fisier:
            writer = csv.DictWriter(fisier, fieldnames=["nume", "echipament"])
            writer.writeheader()
            writer.writerow(rowdict=imprumuturi)

def efectueaza_salvare(salvator:SalvareImprumuturi, imprumuturi):
    salvator.salveaza(imprumuturi)

#Incalcarea Principiului Liskov
class SalvareFalsa(SalvareImprumuturi):
    def salveaza(self, imprumuturi):
        print("AM SALVAT IMPRUMUTURILE")
 
registru = RegistruImprumuturi()
registru.adauga("Ana", "Kit Arduino")
registru.adauga("Marcel", "Kit Raspberry")
registru.adauga("Ionel", "Laptop Thinkpad x230")

raport = RaportImprumuturi()
raport.afiseaza(registru.imprumuturi)

#salvare = SalvareCSV()
#salvare.salveaza(registru.imprumuturi)

#efectueaza_salvare(SalvareJSON(), registru.imprumuturi)
#efectueaza_salvare(SalvareCSV(), registru.imprumuturi)

efectueaza_salvare(SalvareFalsa(), registru.imprumuturi)