


class InfoManager :
    def __init__(self):
        self.tourist = []
        self.cars = []
        self.countrys = []


class Country:
    def __init__(self,id = None,name = None,count = None):
        self.id = int()
        self.name = str()
        self.count = int()

    def incre(self):
        self.count = self.count + 1 






class Tourist:
    _next_id = 1  # Contador automático de clase (entero)

    def __init__(self, name: str, country: str, passport_number: str, id: int | None = None):
        if id is not None:
            self.id = id
        else:
            self.id = Tourist._next_id
            Tourist._next_id += 1
        self.name = name
        self.country = country
        self.passport_number = passport_number

    
class Car:
    def __init__(self, plate: str, brand: str, model: str, color: str):
        self.plate = plate              # identificador único (como el pasaporte)
        self.brand = brand
        self.model = model
        self.color = color
        self.total_km = 0               # kilómetros recorridos (acumulado)
        self.status = "disponible"      # valores posibles: "disponible", "alquilado", "taller"


class Contrat:
    pass 
        
    