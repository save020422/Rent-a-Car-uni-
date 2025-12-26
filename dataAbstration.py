


from datetime import date

class InfoManager:
    def __init__(self, countries_list=None):
        # === Datos transaccionales ===
        self.tourists = []      # list[Tourist]
        self.cars = []          # list[Car]
        self.contracts = []     # list[RentalContract]
        
        # === Tabla normativa (datos maestros) ===
        self.countries = countries_list or []  # list[str]

    # ───────────────
    # Gestión de turistas
    # ───────────────
    def add_tourist(self, name: str, passport: str, country: str) -> bool:
        """
        Añade un turista si:
        - El pasaporte no existe
        - El país está en la lista normativa
        """
        pass

    def get_tourist_by_passport(self, passport: str):
        """Devuelve un turista por su número de pasaporte, o None si no existe."""
        pass

    # ───────────────
    # Gestión de autos
    # ───────────────
    def add_car(self, plate: str, brand: str, model: str, color: str, status: str = "disponible") -> bool:
        """
        Añade un auto si la placa no existe.
        """
        pass

    def get_car_by_plate(self, plate: str):
        """Devuelve un auto por su placa, o None si no existe."""
        pass

    # ───────────────
    # Disponibilidad y contratos
    # ───────────────
    def is_car_available(self, plate: str, start_date: date, end_date: date) -> bool:
        """
        Verifica que el auto no esté alquilado en NINGÚN día del rango [start_date, end_date].
        """
        pass

    def create_contract(
        self,
        passport: str,
        plate: str,
        start_date: date,
        end_date: date,
        extension_days: int = 0,
        with_driver: bool = False,
        payment_method: str = "efectivo"
    ) -> bool:
        """
        Crea un contrato si:
        - El turista existe
        - El auto existe y está disponible en las fechas
        - La forma de pago es válida
        """
        pass

    # ───────────────
    # Reportes (solo firmas, se implementan después)
    # ───────────────
    def get_tourists_report(self):
        """Reporte 1: Listado de usuarios por país."""
        pass

    def get_cars_report(self):
        """Reporte 2: Listado de autos con km."""
        pass

    def get_cars_status_report(self):
        """Reporte 3: Situación de los autos."""
        pass

    def get_contracts_report(self):
        """Reporte 4: Listado de contratos."""
        pass

    def get_violators_report(self):
        """Reporte 5: Turistas con prórroga > 0."""
        pass

    def get_summary_by_brand(self):
        """Reporte 6: Resumen por marcas y modelos."""
        pass

    def get_summary_by_country(self):
        """Reporte 7: Resumen por países."""
        pass


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


from datetime import date

from datetime import date

# Tarifas configurables (puedes moverlas a un archivo de configuración si quieres)
DAILY_RATE = 50.0        # Tarifa normal por día
EXTENSION_RATE = 70.0    # Tarifa de prórroga por día
VALID_PAYMENT_METHODS = {"efectivo", "cheque", "tarjeta de crédito"}


class RentalContract:
    def __init__(
        self,
        tourist: 'Tourist',
        car: 'Car',
        start_date: date,
        end_date: date,
        extension_days: int = 0,
        with_driver: bool = False,
        payment_method: str = "efectivo"
    ):
        # === Validaciones ===
        if not isinstance(start_date, date) or not isinstance(end_date, date):
            raise TypeError("Las fechas deben ser objetos 'datetime.date'")
        if start_date > end_date:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin.")
        if extension_days < 0:
            raise ValueError("La prórroga no puede ser negativa.")
        if payment_method not in VALID_PAYMENT_METHODS:
            raise ValueError(
                f"Forma de pago inválida. Debe ser: {', '.join(VALID_PAYMENT_METHODS)}"
            )
        if car.status != "disponible":
            raise ValueError(f"El auto {car.plate} no está disponible para alquiler.")

        # === Asignación de atributos ===
        self.tourist = tourist
        self.car = car
        self.start_date = start_date
        self.end_date = end_date
        self.extension_days = extension_days
        self.with_driver = with_driver
        self.payment_method = payment_method

        # === Cálculo del importe total ===
        self.total_amount = self._calculate_total()

        # === Actualizar estado del auto ===
        self.car.status = "alquilado"

    def _calculate_total(self) -> float:
        """Calcula el importe total: (días de contrato × tarifa normal) + (prórroga × tarifa especial)"""
        # Incluye ambos días: ejemplo: 1 al 3 → 3 días
        rental_days = (self.end_date - self.start_date).days + 1
        base_amount = rental_days * DAILY_RATE
        extension_amount = self.extension_days * EXTENSION_RATE
        total = base_amount + extension_amount
        return round(total, 2)

    def __str__(self):
        return (
            f"Contrato({self.tourist.name}, {self.car.plate}, "
            f"{self.start_date} → {self.end_date}, "
            f"prórroga={self.extension_days}d, total=${self.total_amount})"
        )

    def __repr__(self):
        return self.__str__()