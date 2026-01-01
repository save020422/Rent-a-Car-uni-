import sqlite3
import os
import random
from datetime import date, timedelta
from dataAbstration import Tourist, Car, RentalContract


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
        base_countries = [
            "Argentina", "Brasil", "Chile", "Colombia", "México",
            "Perú", "España", "Francia", "Italia", "Alemania",
            "Japón", "Corea del Sur", "Estados Unidos", "Canadá", "Australia",
            "India", "China", "Rusia", "Sudáfrica", "Egipto", "Portugal", "Suiza",
            "Bélgica", "Holanda", "Noruega", "Suecia", "Dinamarca", "Polonia", "Turquía",
            "Reino Unido", "Irlanda", "Grecia", "Finlandia", "Austria", "Hungría",
            "República Checa", "Eslovaquia", "Eslovenia", "Croacia", "Serbia",
            "Rumania", "Bulgaria", "Ucrania", "Bielorrusia", "Letonia", "Lituania", "Estonia",
            "Islandia", "Nueva Zelanda", "Singapur", "Malasia", "Tailandia", "Vietnam",
            "Filipinas", "Indonesia", "Pakistán", "Bangladés", "Nigeria", "Kenia",
            "Ghana", "Etiopía", "Marruecos", "Argelia", "Túnez", "Senegal", "Camerún",
            "Chile", "Uruguay", "Paraguay", "Bolivia", "Ecuador", "Venezuela", "Costa Rica",
            "Panamá", "República Dominicana", "Puerto Rico", "Cuba", "Honduras", "Guatemala",
            "El Salvador", "Nicaragua", "Jamaica", "Trinidad y Tobago", "Bahamas", "Barbados",
            "Qatar", "Emiratos Árabes Unidos", "Arabia Saudita", "Israel", "Líbano", "Irán",
            "Irak", "Afganistán", "Nepal", "Sri Lanka", "Mongolia", "Kazajistán", "Uzbekistán"
        ]
        while len(base_countries) < 100:
            base_countries.append(f"País {len(base_countries) + 1}")
        return list(set(base_countries))[:100]

    def _get_cars_data(self):
        brands_models = [
            ("Toyota", "Corolla"), ("Honda", "Civic"), ("Ford", "Focus"),
            ("Volkswagen", "Golf"), ("BMW", "Serie 3"), ("Mercedes", "C-Class"),
            ("Audi", "A4"), ("Hyundai", "Elantra"), ("Nissan", "Sentra"),
            ("Chevrolet", "Cruze"), ("Kia", "Forte"), ("Mazda", "3"),
            ("Subaru", "Impreza"), ("Tesla", "Model 3"), ("Peugeot", "308"),
            ("Renault", "Megane"), ("Fiat", "Tipo"), ("Suzuki", "Swift"),
            ("Lexus", "ES"), ("Volvo", "XC40")
        ]
        colors = ["Rojo", "Azul", "Blanco", "Negro", "Gris", "Plateado"]
        plates = set()
        cars = []
        for _ in range(50):
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
        first_names = ["Ana", "Carlos", "Sofía", "Luis", "María", "Javier"]
        last_names = ["González", "Rodríguez", "Fernández", "López", "Martínez"]
        return first_names, last_names

    def _ensure_sample_data(self):
        """Inserta datos de ejemplo si la base de datos está vacía."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Country")
            if cursor.fetchone()[0] > 0:
                return

            # Países
            countries = self._get_countries()
            cursor.executemany("INSERT INTO Country (name) VALUES (?)", [(c,) for c in countries])

            # Autos
            cars_data = self._get_cars_data()
            cursor.executemany(
                "INSERT INTO Car (plate, brand, model, color, status, total_km) VALUES (?, ?, ?, ?, ?, ?)",
                cars_data
            )

            # Turistas
            first_names, last_names = self._get_names()
            cursor.execute("SELECT id FROM Country")
            country_ids = [r[0] for r in cursor.fetchall()]
            tourists = []
            passports = set()
            for i in range(30):
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

            # Contratos
            cursor.execute("SELECT id FROM Tourist")
            tourist_ids = [r[0] for r in cursor.fetchall()]
            cursor.execute("SELECT id FROM Car WHERE status = 'disponible'")
            car_ids = [r[0] for r in cursor.fetchall()]
            contracts = []
            for i in range(min(15, len(tourist_ids), len(car_ids))):
                t_id = tourist_ids[i]
                c_id = car_ids[i]
                start = date.today() - timedelta(days=random.randint(5, 30))
                end = start + timedelta(days=random.randint(2, 7))
                extension = random.choice([0, 2])
                with_driver = random.choice([True, False])
                payment = random.choice(["efectivo", "tarjeta de crédito"])
                base_days = (end - start).days + 1
                total = base_days * 50.0 + extension * 70.0
                contracts.append((t_id, c_id, start.isoformat(), end.isoformat(), extension, int(with_driver), payment, total))
            cursor.executemany(
                """INSERT INTO RentalContract 
                (tourist_id, car_id, start_date, end_date, extension_days, with_driver, payment_method, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                contracts
            )

            conn.commit()
            print("✅ Base de datos inicializada con datos de ejemplo.")
        except sqlite3.Error as e:
            print(f"❌ Error al insertar datos de ejemplo: {e}")
            conn.rollback()
        finally:
            conn.close()