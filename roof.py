# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

class Roof:
    def __init__(self, name, pdl, roof_m2):
        self.name = name
        self.pdl = pdl
        self.roof_m2 = roof_m2

    def get_info(self):
        print(f"Bâtiment: {self.name}")
        print(f"Pdl: {self.pdl}")

# class ProdBuilding(Building):

#     def __init__(self, name, coordinates, year_consumption):
#         super().__init__(name, coordinates, year_consumption, True)

#     def __set_surface__(self, roof_m2):
#         self.roof_m2 = roof_m2

#     def production(self):
#         return [10]*7
    
#     def show_production(self):
#         # Get consumption data
#         consumption = super().conso()
#         production = self.production()  # Use the base class method

        
#         # Create time values (e.g., for 7 days)
#         time = np.arange(1, len(production)+1)  # Array from 1 to 7 representing time (days)

#         # Generate a plot
#         plt.plot(time, consumption, marker='o', linestyle='-', color='r')
#         plt.plot(time, production, marker='o', linestyle='-', color='b')
#         plt.title('Production over Time')
#         plt.xlabel('Days')
#         plt.ylabel('Production (kWh)')
#         plt.grid(True)

#         plt.show()

#     def get_info(self):
#         super().get_info()
#         print(f"Surface du toit: {self.roof_m2} m²")
#         print(f"Surface dispo pour panneaux photovoltaïques: {self.pv_m2} m²")
