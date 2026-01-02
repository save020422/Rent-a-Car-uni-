import flet as ft
from datetime import date

class Tourist:
    def __init__(self, name, passport_number, country):
        self.name = name
        self.passport_number = passport_number  # ← pasaporte
        self.country = country                   # ← país (string)

class Car:
    def __init__(self, plate, brand, model, color, status, total_km=0):
        self.plate = plate
        self.brand = brand
        self.model = model
        self.color = color
        self.status = status  # "disponible", "alquilado", "taller"
        self.total_km = total_km

    def __str__(self):
        return f"{self.brand} {self.model}"

class RentalContract:
    def __init__(self, tourist, car, start_date, end_date, extension_days=0, with_driver=False, payment_method="efectivo"):
        self.tourist = tourist
        self.car = car
        self.start_date = start_date
        self.end_date = end_date
        self.extension_days = extension_days
        self.with_driver = with_driver
        self.payment_method = payment_method

        # Cálculo del total
        base_days = (end_date - start_date).days + 1
        base_amount = base_days * 50.0
        extension_amount = extension_days * 70.0
        self.total_amount = base_amount + extension_amount

    def print_all_attributes(self):
        print(f"\n🆕 Nuevo contrato creado:")
        print(f"   Turista: {self.tourist.name} ({self.tourist.passport_number})")
        print(f"   País: {self.tourist.country}")
        print(f"   Auto: {self.car.plate} ({self.car.brand} {self.car.model})")
        print(f"   Fechas: {self.start_date} → {self.end_date}")
        print(f"   Prórroga: {self.extension_days} días")
        print(f"   Con chofer: {'Sí' if self.with_driver else 'No'}")
        print(f"   Pago: {self.payment_method}")
        print(f"   Total: ${self.total_amount:.2f}")



class InfoManager:

    def __init__(self):
    
        self.countries = ["Argentina", "Brasil", "Chile", "Colombia", "México",
                        "Perú", "España", "Francia", "Italia", "Alemania",
                        "Japón", "Corea del Sur", "Estados Unidos", "Canadá", "Australia",
                        "India", "China", "Rusia", "Sudáfrica", "Egipto", "Portugal", "Suiza",
                        "Bélgica", "Holanda", "Noruega", "Suecia", "Dinamarca", "Polonia", "Turquía"]
        self.tourist = []
        self.contracts = []
        self.cars = [ Car("ABC123", "Toyota", "Corolla", "Rojo", "disponible"),
                        Car("XYZ789", "Honda", "Civic", "Azul", "disponible"),
                        Car("DEF456", "Ford", "Focus", "Blanco", "disponible"),
                        Car("GHI012", "Volkswagen", "Golf", "Gris", "disponible"),
                        Car("JKL345", "BMW", "Serie 3", "Negro", "disponible"),
                        Car("MNO678", "Mercedes", "C-Class", "Plateado", "disponible"),
                        Car("PQR901", "Audi", "A4", "Rojo", "disponible"),
                        Car("STU234", "Hyundai", "Elantra", "Azul", "disponible"),
                        Car("VWX567", "Nissan", "Sentra", "Blanco", "disponible"),
                        Car("YZA890", "Chevrolet", "Cruze", "Gris", "disponible"),]