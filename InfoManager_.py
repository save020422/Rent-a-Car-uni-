from SystemOfBd import *

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
        
    def load_all_data():
        #esta funcion carga todos los datos de la db a el ifomanager
        pass

    def save_tourist():
        pass 