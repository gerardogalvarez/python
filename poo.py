"""Ejemplo de POO"""
class Vehicle:

    """Class representing a Vehicle"""
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    """Function printing vehicle info."""
    def __str__(self):
        return f"{self.modelo} is a {self.marca} model with {self.ruedas} ruedas!"

    def pita(self):
        print("moc-moc!!!")

    ruedas = 2

class Car(Vehicle):
    def pita(self):
        print("piiii!!!")

    ruedas = 4

c = Car("DS", "4 Crossbak")
c.pita()
print(c)

bici = Vehicle("Torrot", "xxx")
bici.pita()
print(bici)
