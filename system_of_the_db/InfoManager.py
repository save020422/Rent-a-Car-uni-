from consructor import *
from datetime import date

class InfoManager:
    def __init__(self, db_ref):
        """
        Inicializa InfoManager con una REFERENCIA a SystemOfDb.
        """
        self.db = db_ref
        self.sync_with_db()

    def sync_with_db(self):
        """
        Sincroniza TODOS los datos desde la base de datos.
        """
        self.countries = self.db.get_all_countries()
        self.tourists = self.db.get_all_tourists()
        self.cars = self.db.get_all_cars()
        self.contracts = self.db.get_all_contracts()
        print(f"🔄 Sincronizado con DB: {len(self.countries)} países, {len(self.tourists)} turistas, "
              f"{len(self.cars)} autos, {len(self.contracts)} contratos.")

    # ────────────────────────────────
    # 🔹 GESTIÓN DE TURISTAS
    # ────────────────────────────────
    
    def add_tourist(self, name: str, passport: str, country: str) -> Tourist | None:
        """Añade un turista si el pasaporte es único."""
        if self.find_tourist_by_passport(passport):
            print(f"⚠️ El turista con pasaporte {passport} ya existe.")
            return None
        tourist = Tourist(name=name, passport_number=passport, country=country)
        self.db.save_tourist(tourist)
        self.tourists.append(tourist)
        return tourist

    def update_tourist(self, passport: str, new_name: str = None, new_country: str = None) -> bool:
        """Actualiza datos de un turista por pasaporte."""
        tourist = self.find_tourist_by_passport(passport)
        if not tourist:
            return False
        if new_name:
            tourist.name = new_name
        if new_country:
            tourist.country = new_country
        self.db.update_turist(tourist)
        return True

    def find_tourist_by_passport(self, passport: str) -> Tourist | None:
        return next((t for t in self.tourists if t.passport_number == passport), None)

    # ────────────────────────────────
    # 🔹 GESTIÓN DE AUTOS
    # ────────────────────────────────
    
    def add_car(self, plate: str, brand: str, model: str, color: str, status: str = "disponible") -> Car | None:
        """Añade un auto si la placa es única."""
        if self.find_car_by_plate(plate):
            print(f"⚠️ El auto con placa {plate} ya existe.")
            return None
        car = Car(plate=plate, brand=brand, model=model, color=color, status=status)
        self.db.save_car(car)
        self.cars.append(car)
        return car

    def update_car_status(self, plate: str, new_status: str) -> bool:
        """Actualiza el estado de un auto (disponible/alquilado/taller)."""
        car = self.find_car_by_plate(plate)
        if not car or new_status not in ["disponible", "alquilado", "taller"]:
            return False
        car.status = new_status
        self.db.update_car(car)
        return True

    def find_car_by_plate(self, plate: str) -> Car | None:
        return next((c for c in self.cars if c.plate == plate), None)

    def is_car_available(self, plate: str) -> bool:
        """Verifica si un auto está disponible para alquilar."""
        car = self.find_car_by_plate(plate)
        return car is not None and car.status == "disponible"

    # ────────────────────────────────
    # 🔹 GESTIÓN DE CONTRATOS
    # ────────────────────────────────
    
    def create_contract(
        self,
        passport: str,
        plate: str,
        start_date: date,
        end_date: date,
        extension_days: int = 0,
        with_driver: bool = False,
        payment_method: str = "efectivo"
    ) -> RentalContract | None:
        """
        Crea un contrato validando:
        - Turista existente
        - Auto disponible
        - Fechas válidas
        - Forma de pago válida
        """
        # Validar turista
        tourist = self.find_tourist_by_passport(passport)
        if not tourist:
            print("❌ Turista no encontrado.")
            return None

        # Validar auto
        if not self.is_car_available(plate):
            print(f"❌ Auto {plate} no está disponible.")
            return None

        # Validar fechas
        if start_date > end_date:
            print("❌ Fecha de inicio posterior a la de fin.")
            return None

        # Validar pago
        if payment_method not in {"efectivo", "cheque", "tarjeta de crédito"}:
            print("❌ Forma de pago inválida.")
            return None

        # Crear contrato
        car = self.find_car_by_plate(plate)
        try:
            contract = RentalContract(
                tourist=tourist,
                car=car,
                start_date=start_date,
                end_date=end_date,
                extension_days=extension_days,
                with_driver=with_driver,
                payment_method=payment_method
            )
            # Guardar en DB y RAM
            self.db.save_contract(contract)
            self.contracts.append(contract)
            
            # Actualizar estado del auto en RAM
            car.status = "alquilado"
            
            # Añadir turista si es nuevo (aunque ya debería existir)
            if not any(t.passport_number == tourist.passport_number for t in self.tourists):
                self.tourists.append(tourist)
                
            return contract
            
        except ValueError as e:
            print(f"❌ Error al crear contrato: {e}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return None

    def get_contracts_by_tourist(self, passport: str) -> list[RentalContract]:
        """Obtiene todos los contratos de un turista."""
        return [c for c in self.contracts if c.tourist.passport_number == passport]

    def get_contracts_by_car(self, plate: str) -> list[RentalContract]:
        """Obtiene todos los contratos de un auto."""
        return [c for c in self.contracts if c.car.plate == plate]

    # ────────────────────────────────
    # 🔹 REPORTES BÁSICOS
    # ────────────────────────────────
    
    def get_active_contracts(self) -> list[RentalContract]:
        """Contratos cuya fecha de fin es hoy o en el futuro."""
        today = date.today()
        return [c for c in self.contracts if c.end_date >= today]

    def get_violators(self) -> list[RentalContract]:
        """Turistas con prórroga > 0 (Reporte 5)."""
        return [c for c in self.contracts if c.extension_days > 0]


# === 🧪 PRUEBA DE CARGA DE DATOS DESDE LA BASE DE DATOS ===
if __name__ == "__main__":
    print("🧪 Iniciando prueba de InfoManager con base de datos...")
    
    # Crear instancia de la base de datos
    db = SystemOfDb()
    
    # Crear InfoManager con referencia a la DB
    info_mgr = InfoManager(db_ref=db)
    
    print("\n" + "="*80)
    print("🌍 PAÍSES CARGADOS")
    print("="*80)
    for i, country in enumerate(info_mgr.countries, 1):
        print(f"{i:3}. {country}")
    
    print("\n" + "="*80)
    print("👤 TURISTAS CARGADOS")
    print("="*80)
    for i, t in enumerate(info_mgr.tourists, 1):
        print(f"{i:3}. Nombre: {t.name} | Pasaporte: {t.passport_number} | País: {t.country}")
    
    print("\n" + "="*80)
    print("🚗 AUTOS CARGADOS")
    print("="*80)
    for i, c in enumerate(info_mgr.cars, 1):
        print(f"{i:3}. Placa: {c.plate} | {c.brand} {c.model} | Color: {c.color} | Estado: {c.status}")
    
    print("\n" + "="*80)
    print("📄 CONTRATOS CARGADOS")
    print("="*80)
    for i, c in enumerate(info_mgr.contracts, 1):
        print(f"{i:3}. Turista: {c.tourist.name} - Auto: {c.car.plate}")
        print(f"     Fechas: {c.start_date} → {c.end_date} | Prórroga: {c.extension_days} días")
        print(f"     Con chofer: {'Sí' if c.with_driver else 'No'} | Pago: {c.payment_method} | Total: ${c.total_amount:.2f}")
        print("-" * 70)
    
    print("\n📊 RESUMEN FINAL")
    print("="*50)
    print(f"Países:   {len(info_mgr.countries)}")
    print(f"Turistas: {len(info_mgr.tourists)}")
    print(f"Autos:    {len(info_mgr.cars)}")
    print(f"Contratos:{len(info_mgr.contracts)}")
    
    print("\n✅ Prueba completada exitosamente.")