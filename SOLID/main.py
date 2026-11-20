# Registru Echipament Laborator - Principiile SOLID
from dataclasses import asdict

class RegistruImprumuturi:
    def __init__(self):     # ne pregatim o lista goala
        self.imprumuturi = []
    def adauga(self, nume, echipament):
        imprumut = {
            "nume": nume,
            "echipament": echipament,
        }
        self.imprumuturi.append(imprumut)
    
class RaportImprumuturi:    
    def afiseaza(self, imprumuturi):
        for imprumut in imprumuturi :
            print(imprumut)

class SalvareTXT:
    def salveaza(self, imprumuturi):
        with open(file="/home/nistor/Workspace/1_inbox/academic/ub/anul2/RCSP/26_27_MAP_FR/SOLID/imprumuturi.txt",mode="w") as fisier:
            for imprumut in imprumuturi:
                fisier.write(str(imprumut)+"\n")

registru = RegistruImprumuturi()
registru.adauga("Ana", "Kit Arduino")
registru.adauga("Marcel", "Kit Raspberry")
registru.adauga("Ionel", "Laptop Thinkpad x230")

raport = RaportImprumuturi()
raport.afiseaza(registru.imprumuturi)

salvare = SalvareTXT()
salvare.salveaza(registru.imprumuturi)