import json
import csv
#------------------------------------------------------
# Clasa Magazin
#---------------------------------------------------------
class MagazinOnline:
    def __init__(self):
        self.comenzi = []

    def adauga_comanda(self, nume,client, produs, pret, cantitate):
        comanda = {
            "nume": nume,
            "client":client,
            "produs": produs,
            "pret": pret,
            "cantitate": cantitate,
        }
        self.comenzi.append(comanda)

#-------------------------------------------------
# Afiseaza in Consola
#--------------------------------------------------
class RaportComenzi:
    def afiseaza(self, comenzi):
        for comanda in comenzi:
            print(
                f"Nume: {comanda['nume']} | "
                f"Client: {comanda['client']} | "
                f"Produs: {comanda['produs']} | "
                f"Pret: {comanda['pret']} | "
                f"Cantitate: {comanda['cantitate']}"
            )

#------------------------------------------
# Salvare in fisiere
#------------------------------------------
class SalvareComenzi:
    def salveaza(self, comenzi):
        raise NotImplementedError

class SalvareComenziCSV(SalvareComenzi):
    def salveaza(self, comenzi):
        with open(
           "D:/Cursuri_Facultate/RCSP/26_27_MAP_FR/Tema/Comenzi_Magazin_Online.csv", "w", newline="" ) as fisier:
            writer = csv.DictWriter(fisier, fieldnames=["nume", "client", "produs", "pret", "cantitate"])
            writer.writeheader()
            writer.writerows(comenzi)

class SalvareComenziJSON(SalvareComenzi):
    def salveaza(self, comenzi):
        with open("D:/Cursuri_Facultate/RCSP/26_27_MAP_FR/Tema/Comenzi_Magazin_Online.json", "w") as fisier:
            json.dump(comenzi, fisier, indent=3)

class SalvareComenziTXT(SalvareComenzi):
    def salveaza(self, comenzi):
        with open("D:/Cursuri_Facultate/RCSP/26_27_MAP_FR/Tema/Comenzi_Magazin_Online.txt", "w") as fisier:
            for comanda in comenzi:
                fisier.write(str(comanda) + "\n")
#-----------------------------------------------------------------
# Calcul total
#------------------------------------------------------------------
class CalculTotal:
    def calculeaza_total(self, comenzi):
        total = 0
        for comanda in comenzi:
            total += comanda["pret"] * comanda["cantitate"]
        return total

#--------------------------------------------------------------
# Calcul cu reducere
#   ->Student
#   ->Profesor
class Reducere(CalculTotal):
    def aplica_reducere(self, comenzi):
        raise NotImplementedError

class ReducereStudent(Reducere):
    def aplica_reducere(self, comenzi):
         total = self.calculeaza_total(comenzi)
         return total * 0.8

class ReducereProfesor(Reducere):
    def aplica_reducere(self, comenzi):
        total = self.calculeaza_total(comenzi)
        return total * 0.9

#---------------------------------------------------------------------
#  Factura
#  ->Text
#  ->json 
#--------------------------------------------------------------------
class Factura:
    def genereaza_factura(self, format):
        raise NotImplementedError

class FacturaTXT(Factura):
    def genereaza_factura(self, comenzi, total):
        with open("factura.txt", "w", encoding="utf-8") as fisier:
            fisier.write("FACTURA\n")
            for comanda in comenzi:
                fisier.write(
                    f"{comanda['client']} - {comanda['produs']} - "
                    f"{comanda['cantitate']} x {comanda['pret']} = "
                    f"{comanda['cantitate'] * comanda['pret']} lei\n"
                )
            fisier.write(f"TOTAL: {total} lei\n")

class FacturaJSON(Factura):
    def genereaza_factura(self, comenzi, total):
        date_factura = {
            "comenzi": comenzi,
            "total": total,
        }
        with open("factura.json", "w", encoding="utf-8") as fisier:
            json.dump(date_factura, fisier, indent=3, ensure_ascii=False)

#------------------------------------------------------------------------------------
# Plata
# ->PlataCash
# ->PlataCard
#---------------------------------------------------------------------------------
class Plata:
    def plata(self, suma):
        raise NotImplementedError         

class PlataCash(Plata):
    def plata(self, suma):
        print(f"Plata cash pentru suma {suma} a fost INREGISTRATA")

class PlataCard(Plata):
    def plata(self, suma):
        print(f"Plata cu cardul pentru suma {suma} a fost INREGISTRATA")

#--------------------------------------------------------------------------
def efectueaza_salvare(calculator: SalvareComenzi, comenzi):
    calculator.salveaza(comenzi)

magazin = MagazinOnline()
magazin.adauga_comanda("Ion","student", "Laptop", 3500, 1)
magazin.adauga_comanda("Maria","profesor", "Mouse", 100, 2)
magazin.adauga_comanda("Robert","muncitor", "Tastatura", 200, 5)

total_normal = CalculTotal().calculeaza_total(magazin.comenzi)
total_student = ReducereStudent().aplica_reducere(magazin.comenzi)
total_profesor = ReducereProfesor().aplica_reducere(magazin.comenzi)


print(f"Total Normal: {total_normal}")
print(f"Total student: {total_student}")
print(f"Total profesor: {total_profesor}")

raport = RaportComenzi()
raport.afiseaza(magazin.comenzi)

efectueaza_salvare(SalvareComenziTXT(), magazin.comenzi)
efectueaza_salvare(SalvareComenziJSON(), magazin.comenzi)
efectueaza_salvare(SalvareComenziCSV(), magazin.comenzi)