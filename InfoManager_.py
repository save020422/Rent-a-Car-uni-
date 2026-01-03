from SystemOfBd import SystemOfDb, Tourist, Car, RentalContract

class InfoManager:

    def __init__(self, SysOfbd: SystemOfDb = None):
        self.countries = []
        self.tourist = []
        self.contracts = []
        self.cars = []
        self.sys_of_bd = SysOfbd
        self.load_all_data()   

   
    def sync_all(self):
        
        try:
            self.countries = self.sys_of_bd.get_all_countries()
            self.tourist = self.sys_of_bd.get_all_tourists()
            self.cars = self.sys_of_bd.get_all_cars()
            self.contracts = self.sys_of_bd.get_all_contracts()
            print("🔄 Listas sincronizadas con la BD")
        except Exception as e:
            print(f"❌ Error al sincronizar: {e}")


    def load_all_data(self):
        
        self.sync_all()

   
    def incert_tourist(self, tourist: Tourist):
       
        self.tourist.append(tourist)
        print(" intentarlo")
        try:
            self.sys_of_bd.insert_tourist(tourist)
            print(f"✅ Turista {tourist.name} insertado en BD")
            self.sync_all()  
        except Exception as e:
            print(f"❌ Error al insertar turista: {e}")

    def incert_contrats(self, contract: RentalContract):
      
        self.contracts.append(contract)
        try:
            self.sys_of_bd.insert_contract(contract)
            print(f"✅ Contrato de {contract.tourist.name} insertado en BD")
            self.sync_all()
        except Exception as e:
            print(f"❌ Error al insertar contrato: {e}")

    def incert_car(self, car: Car):
        
        self.cars.append(car)
        try:
            self.sys_of_bd.insert_car(car)
            print(f" Auto {car.plate} insertado en BD")
            self.sync_all()
        except Exception as e:
            print(f"❌ Error al insertar auto: {e}")
