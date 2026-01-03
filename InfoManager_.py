from SystemOfBd import *

class InfoManager:

    def __init__(self, SysOfbd = None):

    
        self.countries = []
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
        
        self.sys_of_bd = SysOfbd
        self.load_all_data()
        
    #esta funcion carga todos los datos de la db a el ifomanager
    def load_all_data(self):
        try:
            self.countries = self.sys_of_bd.get_all_countrys()
            print("Si")

        except:
            print("no se puedo jefe")
        
        
    def incert_tourist(self,tourist):
        self.tourist.append(tourist)
        pass 

    def incert_contrats(self,contratcs):
        self.contracts.append(contratcs)
