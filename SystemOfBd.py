import os 
import sqlite3
from dataAbstration import *

class SystemOfDb:

    def __init__(self):
        folder_path = "SrcDataBase"
        
        os.makedirs(folder_path, exist_ok=True)# crea una carpeta si la misma no existe 
        self.db_path = os.path.join(folder_path, "database.db")
        self._create_tables()
        #self._insert_sample_data()
        self.countrys_incert()

    def _create_tables(self):
        """Crea todas las tablas con sus relaciones."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        # Tabla de Países (maestra)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Country (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """)
        
        # Tabla de Turistas
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
        
        # Tabla de Autos
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
        
        # Tabla de Contratos (relación principal)
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

    def _insert_sample_data(self):
        """Inserta datos de ejemplo para probar el sistema."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        try:
            # Verificar si ya existen datos
            cursor.execute("SELECT COUNT(*) FROM Country")
            if cursor.fetchone()[0] > 0:
                return
            
            # Insertar países
            countries = [
                ("España",), ("México",), ("Francia",), ("Japón",), ("Estados Unidos",)
            ]
            cursor.executemany("INSERT INTO Country (name) VALUES (?)", countries)
            
            # Insertar autos
            cars = [
                ("ABC123", "Toyota", "Corolla", "Rojo", "disponible", 0.0),
                ("XYZ789", "Honda", "Civic", "Azul", "disponible", 0.0),
                ("DEF456", "Ford", "Focus", "Blanco", "disponible", 0.0)
            ]
            cursor.executemany("""
                INSERT INTO Car (plate, brand, model, color, status, total_km) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, cars)
            
            # Insertar turistas
            tourists = [
                ("Ana López", "ES123456", 1, 0, 0.0),  # España (id=1)
                ("Carlos Mendoza", "MX789012", 2, 0, 0.0),  # México (id=2)
                ("Sophie Dubois", "FR345678", 3, 0, 0.0)   # Francia (id=3)
            ]
            cursor.executemany("""
                INSERT INTO Tourist (name, passport_number, country_id, times_used_cars, total_rental_value) 
                VALUES (?, ?, ?, ?, ?)
            """, tourists)
            
            # Insertar contratos
            from datetime import date, timedelta
            today = date.today()
            contracts = [
                (1, 1, today.isoformat(), (today + timedelta(days=5)).isoformat(), 0, 0, "efectivo", 250.0),
                (2, 2, (today - timedelta(days=3)).isoformat(), today.isoformat(), 2, 1, "tarjeta de crédito", 390.0)
            ]
            cursor.executemany("""
                INSERT INTO RentalContract 
                (tourist_id, car_id, start_date, end_date, extension_days, with_driver, payment_method, total_amount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, contracts)
            
            connection.commit()
            print("✅ Datos de ejemplo insertados correctamente.")
            
        except sqlite3.Error as e:
            print(f"❌ Error al insertar datos de ejemplo: {e}")
            connection.rollback()
        finally:
            connection.close()

    # Métodos para cargar datos (opcional, pero recomendados)
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
            tourist = Tourist(
                name=row[0],
                passport_number=row[1],
                country=row[2],
                times_used_cars=row[3],
                total_rental_value=row[4]
            )
            tourists.append(tourist)
        connection.close()
        return tourists

    def get_all_cars(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT plate, brand, model, color, status, total_km FROM Car")
        cars = []
        for row in cursor.fetchall():
            car = Car(
                plate=row[0],
                brand=row[1],
                model=row[2],
                color=row[3],
                status=row[4],
                total_km=row[5]
            )
            cars.append(car)
        connection.close()
        return cars


    #this  funcion return all entided for the ram memory
    def get_all_contracts(self):
        from datetime import date
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
            tourist = Tourist(
                name=row[0],
                passport_number=row[1],
                country=row[2]
            )
            car = Car(
                plate=row[3],
                brand=row[4],
                model=row[5],
                color=row[6],
                status=row[7],
                total_km=row[8]
            )
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
    
    #@save 
        # Métodos completados
    def countrys_incert(self):
        """Inserta países adicionales si la tabla está vacía."""
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
        """Inserta autos adicionales si la tabla está vacía."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Car")
            if cursor.fetchone()[0] == 0:
                cars = [
                    ("GHI012", "Volkswagen", "Golf", "Gris", "disponible", 0.0),
                    ("JKL345", "BMW", "Serie 3", "Negro", "disponible", 0.0),
                    ("MNO678", "Mercedes", "C-Class", "Plateado", "disponible", 0.0),
                    ("PQR901", "Audi", "A4", "Rojo", "disponible", 0.0),
                    ("STU234", "Hyundai", "Elantra", "Azul", "disponible", 0.0),
                    ("VWX567", "Nissan", "Sentra", "Blanco", "disponible", 0.0),
                    ("YZA890", "Chevrolet", "Cruze", "Gris", "disponible", 0.0),
                ]
                cursor.executemany("""
                    INSERT INTO Car (plate, brand, model, color, status, total_km)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, cars)
                connection.commit()
        finally:
            connection.close()

    def get_all_countrys(self):
        """Devuelve todos los países registrados (alias del método get_all_countries)."""
        return self.get_all_countries()
