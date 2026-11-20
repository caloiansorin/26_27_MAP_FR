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
        with open("/Users/spikecsi/Desktop/SOLID/imprumuturi.txt", "w") as fisier:
            for imprumut in imprumuturi:
                fisier.write(str(imprumut) + "\n")


class SalvareJSON(SalvareImprumuturi):
    def salveaza(self, imprumuturi):
        with open("/Users/spikecsi/Desktop/SOLID/imprumuturi.json", "w") as fisier:
            json.dump(imprumuturi, fisier, indent=3)


class SalvareCSV(SalvareImprumuturi):
    def salveaza(self, imprumuturi):
        with open(
            "/Users/spikecsi/Desktop/SOLID/imprumuturi.csv", "w", newline=""
        ) as fisier:
            writer = csv.DictWriter(fisier, fieldnames=["nume", "echipament"])
            writer.writeheader()
            writer.writerows(imprumuturi)


class Notificare:
    def trimite(self, mesaj):
        raise NotImplementedError


class NotificareEmail(Notificare):
    def trimite(self, mesaj):
        print("Email trimis", mesaj)


class NotificareSMS(Notificare):
    def trimite(self, mesaj):
        print("SMS trimis", mesaj)


class ServiciuImprumuturi:
    def __init__(
        self,
        registru: RegistruImprumuturi,
        salvare: SalvareImprumuturi,
        notificare: Notificare,
    ):
        self.registru = registru
        self.salvare = salvare
        self.notificare = notificare

    def imprumuta(self, nume, echipament):
        self.registru.adauga(nume, echipament)
        self.salvare.salveaza(self.registru.imprumuturi)
        self.notificare.trimite(f"{nume} a imprumutat echipamentul {echipament}")


def efectueaza_salavare(salvator: SalvareImprumuturi, imprumuturi):
    salvator.salveaza(imprumuturi)


# registru = RegistruImprumuturi()
# registru.adauga("Ana", "Kit Arduino")
# registru.adauga("Mihai", "Tastatura")
# # AFISAM IMPRUMUTURILE:
# raport = RaportImprumuturi()
# raport.afiseaza(registru.imprumuturi)

# # Salvam imprumuturile
# salvare = SalvareJSON()
# salvare.salveaza(registru.imprumuturi)

# # Trimitem o notificare
# notificare = NotificareSMS()
# notificare.trimite("Ana a imprumutat un Kit Arduino")

# serviciu = ServiciuImprumuturi()
# serviciu.imprumuta("Ana", "Kit Arduino")
# serviciu.imprumuta("Mihai", "Tastatura")


registru = RegistruImprumuturi()
serviciu = ServiciuImprumuturi(registru, SalvareTXT(), NotificareSMS())
serviciu.imprumuta("Ana", "Kit Arduino")
serviciu.imprumuta("Maria", "Mouse")
serviciu.imprumuta("Cristian", "Monitor")
