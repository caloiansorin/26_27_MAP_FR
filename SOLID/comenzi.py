import json

class Client:
    #principiul 1 (Single responsibility principle)
    def __init__(self, nume):
        self.nume = nume
        self.comenzi = []

    def adauga_comanda(self, produs, pret, cantitate):
        comanda = {
            "produs": produs,
            "pret": pret,
            "cantitate": cantitate,
        }
        self.comenzi.append(comanda)

class CalculatorTotal:
    def calculeaza_total(self, comenzi):
        total = 0
        for comanda in comenzi:
            total += comanda["pret"] * comanda["cantitate"]
        return total

class Reducere:
    def aplica(self,total):
        raise NotImplementedError

class ReducereStudent(Reducere):
    def aplica(self, total):
        return total * 0.8

class ReducereProfesor(Reducere):
    def aplica(self, total):
        return total * 0.9

class FaraReducere(Reducere):
    def aplica(self, total):
        return total

class MetodaPlata:
    def plata(self, suma):
        raise NotImplementedError

class PlataCard(MetodaPlata):
    def plata(self, suma):
        print(f"Plata cu cardul pentru suma {suma} a fost INREGISTRATA")

class PlataCash(MetodaPlata):
    def plata(self, suma):
        print(f"Plata cash pentru suma {suma} a fost INREGISTRATA")

class GenerareFactura:
    def genereaza(self, client: Client, total_final):
        raise NotImplementedError

class FacturaTXT(GenerareFactura):
    def genereaza(self, client: Client, total_final):
        nume_fisier = f"{client.nume}_factura.txt"
        with open(f"{client.nume}_factura.txt", "w") as fisier:
            fisier.write(f"Factura pentru {client.nume}\n")
            for comanda in client.comenzi:
                fisier.write(str(comanda) + "\n")
            fisier.write(f"Total final: {total_final}\n")
        print(f"Factura a fost generata in fisierul {nume_fisier}")

class FacturaJSON(GenerareFactura):
    def genereaza(self, client:Client, total_final):
        nume_fisier = f"{client.nume}_factura.json"
        with open(f"{client.nume}_factura.json", "w") as fisier:
            factura = {
                "client": client.nume,
                "comenzi": client.comenzi,
                "total_final": round(total_final,2)
            }
        with open(nume_fisier, "w") as fisier:
            json.dump(factura, fisier, indent=4)    
        print(f"Factura a fost generata in fisierul {nume_fisier}")

class ServiciuComenzi:
    def __init__(
        self,
        calculator: CalculatorTotal,
        plata: MetodaPlata,
        factura: GenerareFactura
    ):
        self.calculator = calculator
        self.plata = plata
        self.factura = factura

    def proceseaza_comanda(self, client: Client, reducere: Reducere):
        total_initial = self.calculator.calculeaza_total(client.comenzi)
        total_final = reducere.aplica(total_initial)
        print(f"\n Procesare comenzi pentru clientul {client.nume}:")
        self.plata.plata(total_final)
        self.factura.genereaza(client, total_final)   

    #def plata(self, metoda, suma):
        #if metoda == "card":
            #print(f"Plata cu cardul pentru suma {suma} a fost INREGISTRATA")
        #elif metoda == "cash":
            #print(f"Plata cash pentru suma {suma} a fost INREGISTRATA")

ion = Client("Ion")
ion.adauga_comanda("Laptop", 3000, 1)

eliza = Client("Eliza")
eliza.adauga_comanda("Telefon", 1500, 2)
eliza.adauga_comanda("Casti", 200, 1)

claudiu=Client("Claudiu")
claudiu.adauga_comanda("Televizor", 2500, 1)

calculator = CalculatorTotal()

serviciu_card_json = ServiciuComenzi(calculator, PlataCard(), FacturaJSON())
serviciu_cash_txt = ServiciuComenzi(calculator, PlataCash(), FacturaTXT())

serviciu_card_json.proceseaza_comanda(ion, ReducereStudent())
serviciu_cash_txt.proceseaza_comanda(eliza, ReducereProfesor())
serviciu_card_json.proceseaza_comanda(claudiu, FaraReducere())
 