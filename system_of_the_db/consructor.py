import sqlite3
import os
from Abtsration import * 


class SystemOfDb:
    def __init__(self):
        folder_path = "SrcDataBase"
        os.makedirs(folder_path, exist_ok=True)
       
        db_path = os.path.join(folder_path, "database.db")
    
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tourist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            passport_number TEXT,
            times_used_cars INTEGER,
            total_rental_value REAL
        )
        """)
        connection.commit()
        connection.close()


        def cargar_turistas(tourits_list):
            db_path = os.path.join("SrcDataBase", "database.db")
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            try:
                cursor.execute("SELECT name, passport_number, times_used_cars, total_rental_value FROM Tourist")
                for row in cursor.fetchall():
                    t = Tourist(name=row[0], passport_number=row[1])
                    t.times_used_cars = row[2]
                    t.total_rental_value = row[3]
                    tourits_list.append(t)
            
            except sqlite3.Error as e:
                print(f"Error al cargar turistas: {e}")
            finally:
                connection.close()


        def insertar_turistas_demo():
            db_path = os.path.join("SrcDataBase", "database.db")
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            turistas_demo = [
                ("Ana Pérez", "A123456", 2, 150.0),
                ("Luis Gómez", "B987654", 1, 80.0),
                ("María Torres", "C456789", 3, 220.0),
                ("Carlos Díaz", "D654321", 0, 0.0),
                ("Sofía Ramírez", "E112233", 4, 310.0),
                ("Jorge Herrera", "F998877", 2, 190.0),
                ("Valentina Cruz", "G445566", 1, 95.0),
                ("Miguel Ángel", "H778899", 5, 450.0),
                ("Isabela Núñez", "I334455", 0, 0.0),
                ("Tomás Ríos", "J667788", 3, 275.0)
            ]

            try:
                for name, passport, times_used, total_value in turistas_demo:
                    cursor.execute("""
                        INSERT OR IGNORE INTO Tourist (name, passport_number, times_used_cars, total_rental_value)
                        VALUES (?, ?, ?, ?)
                    """, (name, passport, times_used, total_value))
                connection.commit()
                print("Turistas de prueba insertados correctamente.")
            except sqlite3.Error as e:
                print(f"Error al insertar turistas demo: {e}")
            finally:
                print("Yolo")
                connection.close()
