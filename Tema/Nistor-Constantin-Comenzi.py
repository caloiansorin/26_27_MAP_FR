import csv
import json
from pathlib import Path


# ------------------------------------------------------
# Comanda care va fi plasata
# ------------------------------------------------------
class Comanda:
    def __init__(self, nume, client, produs, pret, cantitate):
        self.nume = nume
        self.client = client
        self.produs = produs
        self.pret = pret
        self.cantitate = cantitate

    def calculeaza_subtotal(self):
        return self.pret * self.cantitate

    def __str__(self):
        return (
            f"Comanda(nume={self.nume!r}, client={self.client!r}, "
            f"produs={self.produs!r}, pret={self.pret!r}, cantitate={self.cantitate!r})"
        )

#--------------------------------------------
# Clasa Magazin
#--------------------------------------------
class MagazinOnline:
    def __init__(self):
        self.comenzi = []

    def adauga_comanda(self, nume, client, produs, pret, cantitate):
        comanda = Comanda(
            nume=nume,
            client=client,
            produs=produs,
            pret=pret,
            cantitate=cantitate,
        )
        self.comenzi.append(comanda)


# ------------------------------------------------------
# Calcul total și reduceri
# ------------------------------------------------------
class CalculatorTotal:
    def calculeaza_total(self, comenzi):
        total = 0.0
        for comanda in comenzi:
            total += comanda.calculeaza_subtotal()
        return total

# ------------------------------------------------------
# Reduceri
# ------------------------------------------------------
class RegulaReducere:
    def aplica(self, suma):
        raise NotImplementedError("Subclasele trebuie să implementeze metoda 'aplica'.")


class FaraReducere(RegulaReducere):
    def aplica(self, suma):
        return suma


class ReducereStudent(RegulaReducere):
    def aplica(self, suma):
        return suma * 0.8


class ReducereProfesor(RegulaReducere):
    def aplica(self, suma):
        return suma * 0.9


# ------------------------------------------------------
# Calculeaza Pretul
# ------------------------------------------------------
class ServiciuPret:
    def __init__(self, calculator, regula):
        self.calculator = calculator
        self.regula = regula

    def calculeaza_final(self, comenzi):
        total_brut = self.calculator.calculeaza_total(comenzi)
        return self.regula.aplica(total_brut)


# ------------------------------------------------------
# Afisare în consolă
# ------------------------------------------------------
class RaportComenzi:
    def afiseaza(self, comenzi):
        for comanda in comenzi:
            print(
                f"Nume: {comanda.nume} | "
                f"Client: {comanda.client} | "
                f"Produs: {comanda.produs} | "
                f"Pret: {comanda.pret} | "
                f"Cantitate: {comanda.cantitate}"
            )


# ------------------------------------------------------
# Salvare comenzi in fisiere
# ------------------------------------------------------
class SalvareComenzi:
    def __init__(self, cale_fisier):
        self.cale_fisier = Path(cale_fisier)

    def salveaza(self, comenzi):
        raise NotImplementedError("Subclasele trebuie să implementeze metoda 'salveaza'.")


class SalvareComenziCSV(SalvareComenzi):
    def salveaza(self, comenzi):
        self.cale_fisier.parent.mkdir(parents=True, exist_ok=True)
        with self.cale_fisier.open("w", newline="", encoding="utf-8") as fisier:
            writer = csv.DictWriter(
                fisier, fieldnames=["nume", "client", "produs", "pret", "cantitate"]
            )
            writer.writeheader()
            for comanda in comenzi:
                writer.writerow(
                    {
                        "nume": comanda.nume,
                        "client": comanda.client,
                        "produs": comanda.produs,
                        "pret": comanda.pret,
                        "cantitate": comanda.cantitate,
                    }
                )


class SalvareComenziJSON(SalvareComenzi):
    def salveaza(self, comenzi):
        self.cale_fisier.parent.mkdir(parents=True, exist_ok=True)
        date = []
        for comanda in comenzi:
            date.append(
                {
                    "nume": comanda.nume,
                    "client": comanda.client,
                    "produs": comanda.produs,
                    "pret": comanda.pret,
                    "cantitate": comanda.cantitate,
                }
            )
        with self.cale_fisier.open("w", encoding="utf-8") as fisier:
            json.dump(date, fisier, indent=3, ensure_ascii=False)


class SalvareComenziTXT(SalvareComenzi):
    def salveaza(self, comenzi):
        self.cale_fisier.parent.mkdir(parents=True, exist_ok=True)
        with self.cale_fisier.open("w", encoding="utf-8") as fisier:
            for comanda in comenzi:
                fisier.write(str(comanda) + "\n")


# ------------------------------------------------------
# Facturare 
# ------------------------------------------------------
class Factura:
    def __init__(self, cale_fisier):
        self.cale_fisier = Path(cale_fisier)

    def genereaza_factura(self, comenzi, total):
        raise NotImplementedError(
            "Subclasele trebuie să implementeze metoda 'genereaza_factura'."
        )


class FacturaTXT(Factura):
    def genereaza_factura(self, comenzi, total):
        with self.cale_fisier.open("w", encoding="utf-8") as fisier:
            fisier.write("FACTURA\n")
            for comanda in comenzi:
                subtotal = comanda.calculeaza_subtotal()
                fisier.write(
                    f"{comanda.client} - {comanda.produs} - "
                    f"{comanda.cantitate} x {comanda.pret} = "
                    f"{subtotal} lei\n"
                )
            fisier.write(f"TOTAL: {total} lei\n")


class FacturaJSON(Factura):
    def genereaza_factura(self, comenzi, total):
        comenzi_facturate = []
        for comanda in comenzi:
            comenzi_facturate.append(
                {
                    "client": comanda.client,
                    "produs": comanda.produs,
                    "cantitate": comanda.cantitate,
                    "pret": comanda.pret,
                    "subtotal": comanda.calculeaza_subtotal(),
                }
            )
        date_factura = {
            "comenzi": comenzi_facturate,
            "total": total,
        }
        with self.cale_fisier.open("w", encoding="utf-8") as fisier:
            json.dump(date_factura, fisier, indent=3, ensure_ascii=False)


# ------------------------------------------------------
# Plată
# ------------------------------------------------------
class Plata:
    def proceseaza_plata(self, suma):
        raise NotImplementedError(
            "Subclasele trebuie să implementeze metoda 'proceseaza_plata'."
        )


class PlataCash(Plata):
    def proceseaza_plata(self, suma):
        print(f"Plata cash pentru suma {suma} a fost INREGISTRATA")


class PlataCard(Plata):
    def proceseaza_plata(self, suma):
        print(f"Plata cu cardul pentru suma {suma} a fost INREGISTRATA")


# ------------------------------------------------------
# functii utile
# ------------------------------------------------------
def efectueaza_salvare(salvator, comenzi):
    salvator.salveaza(comenzi)


def proceseaza_factura(generator_factura, comenzi, total):
    generator_factura.genereaza_factura(comenzi, total)


def efectueaza_plata(metoda_plata, suma):
    metoda_plata.proceseaza_plata(suma)


def main():
    magazin = MagazinOnline()
    magazin.adauga_comanda("Ion", "student", "Laptop", 3500, 1)
    magazin.adauga_comanda("Maria", "profesor", "Mouse", 100, 2)
    magazin.adauga_comanda("Robert", "muncitor", "Tastatura", 200, 5)

    calculator = CalculatorTotal()
    total_normal = ServiciuPret(calculator, FaraReducere()).calculeaza_final(
        magazin.comenzi
    )
    total_student = ServiciuPret(calculator, ReducereStudent()).calculeaza_final(
        magazin.comenzi
    )
    total_profesor = ServiciuPret(calculator, ReducereProfesor()).calculeaza_final(
        magazin.comenzi
    )

    print(f"Total Normal: {total_normal}")
    print(f"Total student: {total_student}")
    print(f"Total profesor: {total_profesor}")

    raport = RaportComenzi()
    raport.afiseaza(magazin.comenzi)

    baza_path = Path("D:/Cursuri_Facultate/RCSP/26_27_MAP_FR/Tema")
    efectueaza_salvare(
        SalvareComenziTXT(baza_path / "Comenzi_Magazin_Online.txt"), magazin.comenzi
    )
    efectueaza_salvare(
        SalvareComenziJSON(baza_path / "Comenzi_Magazin_Online.json"), magazin.comenzi
    )
    efectueaza_salvare(
        SalvareComenziCSV(baza_path / "Comenzi_Magazin_Online.csv"), magazin.comenzi
    )

    proceseaza_factura(FacturaTXT("factura.txt"), magazin.comenzi, total_normal)
    proceseaza_factura(FacturaJSON("factura.json"), magazin.comenzi, total_normal)

    efectueaza_plata(PlataCash(), total_normal)
    efectueaza_plata(PlataCard(), total_student)


if __name__ == "__main__":
    main()