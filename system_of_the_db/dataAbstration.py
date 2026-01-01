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
