# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

class Batiment:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates

    def conso(self):
        return [20]*7

    def show_consumption(self):
        # Get consumption data
        consumption = self.conso()  # Use the base class method
        
        # Create time values (e.g., for 7 days)
        time = np.arange(1, len(consumption)+1)  # Array from 1 to 7 representing time (days)

        # Generate a plot
        plt.plot(time, consumption, marker='o', linestyle='-', color='b')
        plt.title('Consumption over Time')
        plt.xlabel('Days')
        plt.ylabel('Consumption (kWh)')
        plt.grid(True)
        plt.show()

    def get_info(self):
        print(f"Bâtiment: {self.name}")
        print(f"Coordonnées: {self.coordinates}")

class BatimentProducteur(Batiment):

    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)

    def __set_surface__(self, roof_m2, pv_m2):
        self.roof_m2 = roof_m2
        self.pv_m2 = pv_m2

    def get_info(self):
        super().get_info()
        print(f"Surface du toit: {self.roof_m2} m²")
        print(f"Surface dispo pour panneaux photovoltaïques: {self.pv_m2} m²")
