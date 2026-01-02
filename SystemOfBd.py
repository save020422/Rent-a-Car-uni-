import os 
import sqlite3
from dataAbstration import *
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

