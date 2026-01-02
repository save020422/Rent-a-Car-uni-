import sqlite3
import os
import random
from datetime import date, timedelta
from .dataAbstration import Tourist, Car, RentalContract


class SystemOfDb:
    def __init__(self):
        folder_path = "SrcDataBase"
        os.makedirs(folder_path, exist_ok=True)
        self.db_path = os.path.join(folder_path, "rental_system.db")
        self._create_tables()
        self._ensure_sample_data()

    def _create_tables(self):
        """Crea todas las tablas del sistema de alquiler."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Country (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tourist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            passport_number TEXT NOT NULL UNIQUE,
            country_id INTEGER NOT NULL,
            FOREIGN KEY (country_id) REFERENCES Country(id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Car (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT NOT NULL UNIQUE,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            color TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('disponible', 'alquilado', 'taller')),
            total_km REAL DEFAULT 0.0
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS RentalContract (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tourist_id INTEGER NOT NULL,
            car_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            extension_days INTEGER DEFAULT 0,
            with_driver BOOLEAN DEFAULT 0,
            payment_method TEXT NOT NULL CHECK(payment_method IN ('efectivo', 'cheque', 'tarjeta de crédito')),
            total_amount REAL NOT NULL,
            FOREIGN KEY (tourist_id) REFERENCES Tourist(id),
            FOREIGN KEY (car_id) REFERENCES Car(id)
        )
        """)
        
        conn.commit()
        conn.close()

    def get_all_countries(self):
        """Devuelve lista de nombres de países."""
        countries = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM Country ORDER BY name")
            countries = [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error al cargar países: {e}")
        finally:
            conn.close()
        return countries

    def get_all_tourists(self):
        """Devuelve lista de objetos Tourist."""
        tourists = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT t.name, t.passport_number, c.name
                FROM Tourist t
                JOIN Country c ON t.country_id = c.id
            """)
            for row in cursor.fetchall():
                tourists.append(Tourist(
                    name=row[0],
                    passport_number=row[1],
                    country=row[2]
                ))
        except sqlite3.Error as e:
            print(f"Error al cargar turistas: {e}")
        finally:
            conn.close()
        return tourists

    def get_all_cars(self):
        """Devuelve lista de objetos Car."""
        cars = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT plate, brand, model, color, status, total_km FROM Car")
            for row in cursor.fetchall():
                cars.append(Car(
                    plate=row[0],
                    brand=row[1],
                    model=row[2],
                    color=row[3],
                    status=row[4],
                    total_km=row[5] or 0.0
                ))
        except sqlite3.Error as e:
            print(f"Error al cargar autos: {e}")
        finally:
            conn.close()
        return cars

    def get_all_contracts(self):
        """Devuelve lista de objetos RentalContract."""
        contracts = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    t.name, t.passport_number, ctr.name,
                    c.plate, c.brand, c.model, c.color, c.status, c.total_km,
                    rc.start_date, rc.end_date, rc.extension_days, 
                    rc.with_driver, rc.payment_method, rc.total_amount
                FROM RentalContract rc
                JOIN Tourist t ON rc.tourist_id = t.id
                JOIN Country ctr ON t.country_id = ctr.id
                JOIN Car c ON rc.car_id = c.id
            """)
            for row in cursor.fetchall():
                tourist = Tourist(row[0], row[1], row[2])
                car = Car(row[3], row[4], row[5], row[6], row[7], row[8] or 0.0)
                contract = RentalContract(
                    tourist=tourist,
                    car=car,
                    start_date=date.fromisoformat(row[9]),
                    end_date=date.fromisoformat(row[10]),
                    extension_days=row[11],
                    with_driver=bool(row[12]),
                    payment_method=row[13]
                )
                contract.total_amount = row[14]
                contracts.append(contract)
        except sqlite3.Error as e:
            print(f"Error al cargar contratos: {e}")
        finally:
            conn.close()
        return contracts

    # ───────────────
    # MÉTODOS DE GUARDADO INDIVIDUAL
    # ───────────────
    
    def save_tourist(self, tourist: Tourist):
        """Guarda un turista en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            # Asegurar país
            cursor.execute("SELECT id FROM Country WHERE name = ?", (tourist.country,))
            country_row = cursor.fetchone()
            if not country_row:
                cursor.execute("INSERT INTO Country (name) VALUES (?)", (tourist.country,))
                country_id = cursor.lastrowid
            else:
                country_id = country_row[0]
            
            # Insertar turista
            cursor.execute(
                "INSERT INTO Tourist (name, passport_number, country_id) VALUES (?, ?, ?)",
                (tourist.name, tourist.passport_number, country_id)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al guardar turista: {e}")
            conn.rollback()
        finally:
            conn.close()

    def save_car(self, car: Car):
        """Guarda un auto en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Car (plate, brand, model, color, status, total_km) VALUES (?, ?, ?, ?, ?, ?)",
                (car.plate, car.brand, car.model, car.color, car.status, car.total_km or 0.0)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al guardar auto: {e}")
            conn.rollback()
        finally:
            conn.close()

    def update_tourist(self, tourist: Tourist):
        """Actualiza un turista existente."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Tourist SET name = ?, country_id = (SELECT id FROM Country WHERE name = ?) WHERE passport_number = ?",
                (tourist.name, tourist.country, tourist.passport_number)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al actualizar turista: {e}")
            conn.rollback()
        finally:
            conn.close()

    def update_car(self, car: Car):
        """Actualiza un auto existente."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Car SET brand = ?, model = ?, color = ?, status = ?, total_km = ? WHERE plate = ?",
                (car.brand, car.model, car.color, car.status, car.total_km or 0.0, car.plate)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al actualizar auto: {e}")
            conn.rollback()
        finally:
            conn.close()

    def save_contract(self, contract):
        """Guarda un contrato y sus entidades relacionadas."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            # País
            cursor.execute("SELECT id FROM Country WHERE name = ?", (contract.tourist.country,))
            country_row = cursor.fetchone()
            if not country_row:
                cursor.execute("INSERT INTO Country (name) VALUES (?)", (contract.tourist.country,))
                country_id = cursor.lastrowid
            else:
                country_id = country_row[0]

            # Turista
            cursor.execute("SELECT id FROM Tourist WHERE passport_number = ?", (contract.tourist.passport_number,))
            tourist_row = cursor.fetchone()
            if tourist_row:
                tourist_id = tourist_row[0]
            else:
                cursor.execute(
                    "INSERT INTO Tourist (name, passport_number, country_id) VALUES (?, ?, ?)",
                    (contract.tourist.name, contract.tourist.passport_number, country_id)
                )
                tourist_id = cursor.lastrowid

            # Auto
            cursor.execute("SELECT id FROM Car WHERE plate = ?", (contract.car.plate,))
            car_row = cursor.fetchone()
            if car_row:
                car_id = car_row[0]
                cursor.execute("UPDATE Car SET status = 'alquilado' WHERE id = ?", (car_id,))
            else:
                cursor.execute(
                    "INSERT INTO Car (plate, brand, model, color, status, total_km) VALUES (?, ?, ?, ?, 'alquilado', ?)",
                    (contract.car.plate, contract.car.brand, contract.car.model, contract.car.color, contract.car.total_km or 0.0)
                )
                car_id = cursor.lastrowid

            # Contrato
            cursor.execute(
                """INSERT INTO RentalContract 
                (tourist_id, car_id, start_date, end_date, extension_days, with_driver, payment_method, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (tourist_id, car_id, contract.start_date.isoformat(), contract.end_date.isoformat(),
                 contract.extension_days, int(contract.with_driver), contract.payment_method, contract.total_amount)
            )

            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al guardar contrato: {e}")
            conn.rollback()
        finally:
            conn.close()

    def _get_countries(self):
        # Lista base de 150 países
        base_countries = [
            "Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Antigua y Barbuda", "Arabia Saudita", 
            "Argelia", "Argentina", "Armenia", "Australia", "Austria", "Azerbaiyán", "Bahamas", "Bangladés", 
            "Barbados", "Baréin", "Bélgica", "Belice", "Benín", "Bielorrusia", "Birmania", "Bolivia", "Bosnia y Herzegovina", 
            "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burkina Faso", "Burundi", "Bután", "Cabo Verde", "Camboya", 
            "Camerún", "Canadá", "Catar", "Chad", "Chile", "China", "Chipre", "Ciudad del Vaticano", "Colombia", 
            "Comoras", "Corea del Norte", "Corea del Sur", "Costa de Marfil", "Costa Rica", "Croacia", "Cuba", 
            "Dinamarca", "Dominica", "Ecuador", "Egipto", "El Salvador", "Emiratos Árabes Unidos", "Eritrea", 
            "Eslovaquia", "Eslovenia", "España", "Estados Unidos", "Estonia", "Etiopía", "Filipinas", "Finlandia", 
            "Fiyi", "Francia", "Gabón", "Gambia", "Georgia", "Ghana", "Granada", "Grecia", "Guatemala", "Guinea", 
            "Guinea ecuatorial", "Guinea-Bisáu", "Guyana", "Haití", "Honduras", "Hungría", "India", "Indonesia", 
            "Irak", "Irán", "Irlanda", "Islandia", "Islas Marshall", "Islas Salomón", "Israel", "Italia", "Jamaica", 
            "Japón", "Jordania", "Kazajistán", "Kenia", "Kirguistán", "Kiribati", "Kuwait", "Laos", "Lesoto", 
            "Letonia", "Líbano", "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", "Madagascar", 
            "Malasia", "Malaui", "Maldivas", "Mali", "Malta", "Marruecos", "Mauricio", "Mauritania", "México", 
            "Micronesia", "Moldavia", "Mónaco", "Mongolia", "Montenegro", "Mozambique", "Namibia", "Nauru", 
            "Nepal", "Nicaragua", "Níger", "Nigeria", "Noruega", "Nueva Zelanda", "Omán", "Países Bajos", "Pakistán", 
            "Palaos", "Panamá", "Papúa Nueva Guinea", "Paraguay", "Perú", "Polonia", "Portugal", "Reino Unido", 
            "República Centroafricana", "República Checa", "República Democrática del Congo", "República del Congo", 
            "República Dominicana", "Ruanda", "Rumania", "Rusia", "Samoa", "San Cristóbal y Nieves", "San Marino", 
            "San Vicente y las Granadinas", "Santa Lucía", "Santo Tomé y Príncipe", "Senegal", "Serbia", "Seychelles", 
            "Sierra Leona", "Singapur", "Siria", "Somalia", "Sri Lanka", "Sudáfrica", "Sudán", "Sudán del Sur", 
            "Suecia", "Suiza", "Surinam", "Tailandia", "Tanzania", "Tayikistán", "Timor Oriental", "Togo", "Tonga", 
            "Trinidad y Tobago", "Túnez", "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", "Uganda", "Uruguay", 
            "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yibuti", "Zambia", "Zimbabue"
        ]
        # Asegurar 150 países
        while len(base_countries) < 150:
            base_countries.append(f"País {len(base_countries) + 1}")
        return list(set(base_countries))[:150]

    def _get_cars_data(self):
        brands_models = [
            ("Toyota", "Corolla"), ("Toyota", "Camry"), ("Toyota", "RAV4"), ("Toyota", "Hilux"),
            ("Honda", "Civic"), ("Honda", "Accord"), ("Honda", "CR-V"), ("Honda", "HR-V"),
            ("Ford", "Focus"), ("Ford", "Fiesta"), ("Ford", "Mustang"), ("Ford", "Ranger"),
            ("Volkswagen", "Golf"), ("Volkswagen", "Polo"), ("Volkswagen", "Passat"), ("Volkswagen", "Tiguan"),
            ("BMW", "Serie 3"), ("BMW", "Serie 5"), ("BMW", "X3"), ("BMW", "X5"),
            ("Mercedes", "C-Class"), ("Mercedes", "E-Class"), ("Mercedes", "GLC"), ("Mercedes", "GLE"),
            ("Audi", "A4"), ("Audi", "A6"), ("Audi", "Q5"), ("Audi", "Q7"),
            ("Hyundai", "Elantra"), ("Hyundai", "Tucson"), ("Hyundai", "Santa Fe"), ("Kia", "Forte"),
            ("Kia", "Sportage"), ("Kia", "Sorento"), ("Nissan", "Sentra"), ("Nissan", "Rogue"),
            ("Chevrolet", "Cruze"), ("Chevrolet", "Equinox"), ("Chevrolet", "Tahoe"), ("Mazda", "3"),
            ("Mazda", "CX-5"), ("Subaru", "Impreza"), ("Subaru", "Forester"), ("Tesla", "Model 3"),
            ("Tesla", "Model Y"), ("Peugeot", "308"), ("Peugeot", "3008"), ("Renault", "Megane"),
            ("Renault", "Duster"), ("Fiat", "Tipo"), ("Fiat", "500X"), ("Suzuki", "Swift"),
            ("Suzuki", "Vitara"), ("Lexus", "ES"), ("Lexus", "RX"), ("Volvo", "XC40"), ("Volvo", "XC60")
        ]
        colors = ["Rojo", "Azul", "Blanco", "Negro", "Gris", "Plateado", "Verde", "Amarillo", "Naranja", "Morado"]
        plates = set()
        cars = []
        for _ in range(100):  # ← 100 autos
            brand, model = random.choice(brands_models)
            color = random.choice(colors)
            while True:
                plate = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100,999)}"
                if plate not in plates:
                    plates.add(plate)
                    break
            status = random.choice(["disponible", "alquilado", "taller"])
            km = round(random.uniform(0, 150000), 1)
            cars.append((plate, brand, model, color, status, km))
        return cars

    def _get_names(self):
        first_names = ["Ana", "Carlos", "Sofía", "Luis", "María", "Javier", "Lucía", "Diego", "Valentina", "Miguel"]
        last_names = ["González", "Rodríguez", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Díaz", "Hernández"]
        return first_names, last_names

    def _ensure_sample_data(self):
        """Inserta datos de ejemplo si la base de datos está vacía."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Country")
            if cursor.fetchone()[0] > 0:
                return

            # 150 Países
            countries = self._get_countries()
            cursor.executemany("INSERT INTO Country (name) VALUES (?)", [(c,) for c in countries])
            print(f"✅ {len(countries)} países insertados.")

            # 100 Autos
            cars_data = self._get_cars_data()
            cursor.executemany(
                "INSERT INTO Car (plate, brand, model, color, status, total_km) VALUES (?, ?, ?, ?, ?, ?)",
                cars_data
            )
            print(f"✅ {len(cars_data)} autos insertados.")

            # 5 Turistas
            first_names, last_names = self._get_names()
            cursor.execute("SELECT id FROM Country")
            country_ids = [r[0] for r in cursor.fetchall()]
            tourists = []
            passports = set()
            for i in range(5):  # ← Solo 5 turistas
                name = f"{random.choice(first_names)} {random.choice(last_names)}"
                while True:
                    passport = f"{random.choice('ABCEFGHJKLMNOPQRSTUVWXYZ')}{random.choice('ABCEFGHJKLMNOPQRSTUVWXYZ')}{random.randint(100000, 999999)}"
                    if passport not in passports:
                        passports.add(passport)
                        break
                country_id = random.choice(country_ids)
                tourists.append((name, passport, country_id))
            cursor.executemany(
                "INSERT INTO Tourist (name, passport_number, country_id) VALUES (?, ?, ?)",
                tourists
            )
            print(f"✅ {len(tourists)} turistas insertados.")

            # Contratos (usando los 5 turistas y autos disponibles)
            cursor.execute("SELECT id FROM Tourist")
            tourist_ids = [r[0] for r in cursor.fetchall()]
            cursor.execute("SELECT id FROM Car WHERE status = 'disponible'")
            car_ids = [r[0] for r in cursor.fetchall()]
            contracts = []
            for i in range(min(10, len(tourist_ids), len(car_ids))):  # ← 10 contratos como ejemplo
                t_id = tourist_ids[i % len(tourist_ids)]
                c_id = car_ids[i]
                start = date.today() - timedelta(days=random.randint(5, 30))
                end = start + timedelta(days=random.randint(2, 7))
                extension = random.choice([0, 0, 0, 2, 5])
                with_driver = random.choice([True, False])
                payment = random.choice(["efectivo", "tarjeta de crédito", "cheque"])
                base_days = (end - start).days + 1
                total = base_days * 50.0 + extension * 70.0
                contracts.append((t_id, c_id, start.isoformat(), end.isoformat(), extension, int(with_driver), payment, total))
            cursor.executemany(
                """INSERT INTO RentalContract 
                (tourist_id, car_id, start_date, end_date, extension_days, with_driver, payment_method, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                contracts
            )
            print(f"✅ {len(contracts)} contratos insertados.")

            conn.commit()
            print("🎉 Base de datos inicializada con datos personalizados.")
        except sqlite3.Error as e:
            print(f"❌ Error al insertar datos de ejemplo: {e}")
            conn.rollback()
        finally:
            conn.close()


# =====================================================================
# InfoManager - con función de actualización mejorada
# =====================================================================

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

    # ... (el resto de tus métodos de InfoManager se mantienen igual) ...

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
        self.db.update_tourist(tourist)
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
            
            # Añadir turista si es nuevo
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
# === 🧪 PRUEBA COMPLETA: IMPRIMIR + INSERTAR + VOLVER A IMPRIMIR ===
if __name__ == "__main__":
    print("🧪 Iniciando prueba COMPLETA de InfoManager con base de datos...")
    
    # Crear instancia de la base de datos
    db = SystemOfDb()
    
    # Crear InfoManager con referencia a la DB
    info_mgr = InfoManager(db_ref=db)
    
    # ────────────────────────────────────────
    # IMPRIMIR DATOS INICIALES
    # ────────────────────────────────────────
    print("\n" + "="*80)
    print("🌍 LISTADO INICIAL DE PAÍSES")
    print("="*80)
    for i, country in enumerate(info_mgr.countries[:10], 1):  # Mostrar solo 10 de 150
        print(f"{i:3}. {country}")
    if len(info_mgr.countries) > 10:
        print(f"    ... y {len(info_mgr.countries) - 10} más")

    print("\n" + "="*80)
    print("👤 LISTADO INICIAL DE TURISTAS")
    print("="*80)
    for i, t in enumerate(info_mgr.tourists, 1):
        print(f"{i:3}. Nombre: {t.name} | Pasaporte: {t.passport_number} | País: {t.country}")

    print("\n" + "="*80)
    print("🚗 LISTADO INICIAL DE AUTOS")
    print("="*80)
    for i, c in enumerate(info_mgr.cars[:10], 1):  # Mostrar solo 10 de 100
        print(f"{i:3}. Placa: {c.plate} | {c.brand} {c.model} | Color: {c.color} | Estado: {c.status}")
    if len(info_mgr.cars) > 10:
        print(f"    ... y {len(info_mgr.cars) - 10} más")

    print("\n" + "="*80)
    print("📄 LISTADO INICIAL DE CONTRATOS")
    print("="*80)
    for i, c in enumerate(info_mgr.contracts, 1):
        chofer = "Sí" if c.with_driver else "No"
        print(f"{i:3}. Turista: {c.tourist.name} - Auto: {c.car.plate}")
        print(f"     Fechas: {c.start_date} → {c.end_date} | Prórroga: {c.extension_days} días")
        print(f"     Chofer: {chofer} | Pago: {c.payment_method} | Total: ${c.total_amount:.2f}")
        print("-" * 70)

    # ────────────────────────────────────────
    # AÑADIR NUEVAS ENTIDADES
    # ────────────────────────────────────────
    print("\n" + "="*80)
    print("➕ AÑADIENDO NUEVAS ENTIDADES")
    print("="*80)
    
    # Añadir 2 turistas
    new_tourist1 = info_mgr.add_tourist("NUEVO Turista 1", "NT001", "España")
    new_tourist2 = info_mgr.add_tourist("NUEVO Turista 2", "NT002", "México")
    
    # Añadir 3 autos
    new_car1 = info_mgr.add_car("NEW001", "Toyota", "Hilux", "Gris", "disponible")
    new_car2 = info_mgr.add_car("NEW002", "Ford", "Ranger", "Blanco", "disponible")
    new_car3 = info_mgr.add_car("NEW003", "Volkswagen", "Tiguan", "Azul", "disponible")
    
    # Añadir 2 contratos
    from datetime import date, timedelta
    today = date.today()
    
    contract1 = info_mgr.create_contract(
        passport="NT001",
        plate="NEW001",
        start_date=today,
        end_date=today + timedelta(days=5),
        extension_days=0,
        with_driver=True,
        payment_method="tarjeta de crédito"
    )
    
    contract2 = info_mgr.create_contract(
        passport="NT002",
        plate="NEW002",
        start_date=today - timedelta(days=2),
        end_date=today + timedelta(days=3),
        extension_days=2,
        with_driver=False,
        payment_method="efectivo"
    )
    
    print("✅ Entidades nuevas añadidas exitosamente.")
    
    # ────────────────────────────────────────
    # IMPRIMIR DATOS ACTUALIZADOS
    # ────────────────────────────────────────
    print("\n" + "="*80)
    print("🔄 DATOS ACTUALIZADOS DESPUÉS DE LAS INSERCIONES")
    print("="*80)
    print(f"Países:   {len(info_mgr.countries)}")
    print(f"Turistas: {len(info_mgr.tourists)}")
    print(f"Autos:    {len(info_mgr.cars)}")
    print(f"Contratos:{len(info_mgr.contracts)}")
    
    # Mostrar los nuevos turistas
    print("\n👤 NUEVOS TURISTAS AÑADIDOS:")
    for t in [new_tourist1, new_tourist2]:
        if t:
            print(f"   - {t.name} ({t.passport_number}) de {t.country}")
    
    # Mostrar los nuevos autos
    print("\n🚗 NUEVOS AUTOS AÑADIDOS:")
    for c in [new_car1, new_car2, new_car3]:
        if c:
            print(f"   - {c.plate}: {c.brand} {c.model} ({c.color}) - {c.status}")
    
    # Mostrar los nuevos contratos
    print("\n📄 NUEVOS CONTRATOS AÑADIDOS:")
    for i, c in enumerate([contract1, contract2], 1):
        if c:
            print(f"   #{i}: {c.tourist.name} alquiló {c.car.plate} del {c.start_date} al {c.end_date}")
    
    print("\n✅ Prueba COMPLETA finalizada con éxito.")