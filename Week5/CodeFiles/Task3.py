class vehicle:
    def __init__(self,brand ,model):
        self.brand=brand
        self.model=model

    def display(self):
        print('Vehicle')
        print(f"Brand : {self.brand}, Model : {self.model}")

class car(vehicle):
    def __init__(self,brand ,model,doors):
         super().__init__(brand,model)
         self.doors=doors
    def display(self):
        print('Car')
        super().display()
        print(f"Doors: {self.doors}")



    
class bike(vehicle):
    def __init__(self,brand ,model,engine):
         super().__init__(brand,model)
         self.engine=engine
    def display(self):
        print('Bike')
        super().display()
        print(f"Bike: {self.engine}")


v=vehicle("Honda","2019")
v.display()



c=car("BMw","2025",4)
c.display()



b=bike("BMw","2025","6787")
b.display()

