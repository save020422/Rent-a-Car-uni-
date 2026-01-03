import os
import sqlite3
from datetime import date
from dataAbstration import Tourist, Car, RentalContract


class SystemOfDb:

    def __init__(self):
        folder_path = "SrcDataBase"
        os.makedirs(folder_path, exist_ok=True)
        self.db_path = os.path.join(folder_path, "database.db")
        self._create_tables()
        self.countrys_incert()
        self.cars_incrt()

    def _create_tables(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

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
            times_used_cars INTEGER DEFAULT 0,
            total_rental_value REAL DEFAULT 0.0,
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
            FOREIGN KEY (tourist_id) REFERENCES Tourist(id) ON DELETE CASCADE,
            FOREIGN KEY (car_id) REFERENCES Car(id) ON DELETE CASCADE
        )
        """)

        connection.commit()
        connection.close()

    def insert_country(self, country_name: str):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Country (name) VALUES (?)", (country_name,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al insertar país: {e}")
            connection.rollback()
        finally:
            connection.close()

    def insert_tourist(self, tourist: Tourist):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id FROM Country WHERE name=?", (tourist.country,))
            country_row = cursor.fetchone()
            if not country_row:
                cursor.execute("INSERT INTO Country (name) VALUES (?)", (tourist.country,))
                connection.commit()
                cursor.execute("SELECT id FROM Country WHERE name=?", (tourist.country,))
                country_row = cursor.fetchone()
            country_id = country_row[0]

            cursor.execute("""
                INSERT INTO Tourist (name, passport_number, country_id, times_used_cars, total_rental_value)
                VALUES (?, ?, ?, ?, ?)
            """, (tourist.name, tourist.passport_number, country_id, 0, 0.0))
            connection.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al insertar turista: {e}")
            connection.rollback()
        finally:
            connection.close()

    def insert_car(self, car: Car):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Car (plate, brand, model, color, status, total_km)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (car.plate, car.brand, car.model, car.color, car.status, car.total_km))
            connection.commit()
        except sqlite3.Error as e:
            print(f"❌ Error al insertar auto: {e}")
            connection.rollback()
        finally:
            connection.close()

    def insert_contract(self, contract: RentalContract):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id FROM Tourist WHERE passport_number=?", (contract.tourist.passport_number,))
            tourist_row = cursor.fetchone()
            if not tourist_row:
                self.insert_tourist(contract.tourist)
                cursor.execute("SELECT id FROM Tourist WHERE passport_number=?", (contract.tourist.passport_number,))
                tourist_row = cursor.fetchone()
            tourist_id = tourist_row[0]

            cursor.execute("SELECT id, status FROM Car WHERE plate=?", (contract.car.plate,))
            car_row = cursor.fetchone()
            if not car_row:
                self.insert_car(contract.car)
                cursor.execute("SELECT id, status FROM Car WHERE plate=?", (contract.car.plate,))
                car_row = cursor.fetchone()
            car_id, car_status = car_row
            if car_status != "disponible":
                raise Exception(f"Auto '{contract.car.plate}' no está disponible (estado: {car_status})")

            cursor.execute("""
                INSERT INTO RentalContract (tourist_id, car_id, start_date, end_date, extension_days, with_driver, payment_method, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (tourist_id, car_id,
                  contract.start_date.isoformat(),
                  contract.end_date.isoformat(),
                  contract.extension_days,
                  int(contract.with_driver),
                  contract.payment_method,
                  contract.total_amount))

            cursor.execute("UPDATE Car SET status='alquilado' WHERE id=?", (car_id,))
            cursor.execute("""
                UPDATE Tourist
                SET times_used_cars = times_used_cars + 1,
                    total_rental_value = total_rental_value + ?
                WHERE id = ?
            """, (contract.total_amount, tourist_id))

            connection.commit()
            print(f"✅ Contrato insertado para {contract.tourist.name}")
        except sqlite3.Error as e:
            print(f"❌ Error al insertar contrato: {e}")
            connection.rollback()
        finally:
            connection.close()

    def get_all_countries(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM Country")
        countries = [row[0] for row in cursor.fetchall()]
        connection.close()
        return countries

    def get_all_tourists(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT t.name, t.passport_number, c.name, t.times_used_cars, t.total_rental_value
            FROM Tourist t
            JOIN Country c ON t.country_id = c.id
        """)
        tourists = []
        for row in cursor.fetchall():
            tourist = Tourist(name=row[0], passport_number=row[1], country=row[2])
            tourist.times_used_cars = row[3]
            tourist.total_rental_value = row[4]
            tourists.append(tourist)
        connection.close()
        return tourists

    def get_all_cars(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT plate, brand, model, color, status, total_km FROM Car")
        cars = []
        for row in cursor.fetchall():
            car = Car(plate=row[0], brand=row[1], model=row[2], color=row[3], status=row[4], total_km=row[5])
            cars.append(car)
        connection.close()
        return cars

    def get_all_contracts(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
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
        contracts = []
        for row in cursor.fetchall():
            tourist = Tourist(name=row[0], passport_number=row[1], country=row[2])
            car = Car(plate=row[3], brand=row[4], model=row[5], color=row[6], status=row[7], total_km=row[8])
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
        connection.close()
        return contracts

    def countrys_incert(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Country")
            if cursor.fetchone()[0] == 0:
                countries = [
                    "Argentina", "Brasil", "Chile", "Colombia", "México",
                    "Perú", "España", "Francia", "Italia", "Alemania",
                    "Japón", "Corea del Sur", "Estados Unidos", "Canadá", "Australia",
                    "India", "China", "Rusia", "Sudáfrica", "Egipto", "Portugal", "Suiza",
                    "Bélgica", "Holanda", "Noruega", "Suecia", "Dinamarca", "Polonia", "Turquía"
                ]
                cursor.executemany("INSERT INTO Country (name) VALUES (?)", [(c,) for c in countries])
                connection.commit()
        finally:
            connection.close()

    def cars_incrt(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Car")
            if cursor.fetchone()[0] == 0:
                cars = [
                    ("ABC123", "Toyota", "Corolla", "Rojo", "disponible", 0.0),
                    ("XYZ789", "Honda", "Civic", "Azul", "disponible", 0.0),
                    ("DEF456", "Ford", "Focus", "Blanco", "disponible", 0.0),
                    ("GHI012", "Volkswagen", "Golf", "Gris", "disponible", 0.0),
                    ("JKL345", "BMW", "Serie 3", "Negro", "disponible", 0.0),
                    ("MNO678", "Mercedes", "C-Class", "Plateado", "disponible", 0.0),
                    ("PQR901", "Audi", "A4", "Rojo", "disponible", 0.0),
                    ("STU234", "Hyundai", "Elantra", "Azul", "disponible", 0.0),
                    ("VWX567", "Nissan", "Sentra", "Blanco", "disponible", 0.0),
                    ("YZA890", "Chevrolet", "Cruze", "Gris", "disponible", 0.0)
                ]
                cursor.executemany("""
                    INSERT INTO Car (plate, brand, model, color, status, total_km)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, cars)
                connection.commit()
        finally:
            connection.close()
