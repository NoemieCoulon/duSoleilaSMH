# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import irridiation as irr
import consumption as cons

class Building:
    def __init__(self, pdl, name, coordinates, year_consumption, prod_possible):
        self.pdl = pdl
        self.name = name
        self.coordinates = coordinates
        self.year_consumption = year_consumption
        self.prod_possible = prod_possible

    def conso(self):
        file_path_mc = "/home/coulonn/Documents/Piste/duSoleilaSMH/consumption/Maison_communale 07_2023.csv"  # Change this to the correct path
        file_path_hb = "/home/coulonn/Documents/Piste/duSoleilaSMH/consumption/L_heure_ bleue_ 07_2023.csv"
        file_path_cjl = "/home/coulonn/Documents/Piste/duSoleilaSMH/consumption/Creche_Jeanne_Labourbe.csv"
        year = 2023
        month = 7
        if self.pdl == "30001931365966":
            file_path = file_path_mc
        elif self.pdl == "30001930627304":
            file_path = file_path_hb
        else:
            file_path = file_path_cjl
        consumption = cons.consumption_per_month(file_path, year, month)
        return consumption

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
        print(f"Production possible? : {self.prod_possible}")

class ProdBuilding(Building):

    def __init__(self, pdl, name, coordinates, year_consumption, roof_m2):
        super().__init__(pdl, name, coordinates, year_consumption, True)
        self.roof_m2 = roof_m2

    def __set_pv_surface__(self, pv_m2):
        self.pv_m2 = pv_m2

    def production(self):
        # Retrieve the irradiation data (assuming it's a list of values for each day)
        irradiation = irr.irridiation_year("2023")["07"]
        
        # Multiply each value in the irradiation list by self.pv_m2 and store in the production list
        production = [float(value) *0.2* float(self.pv_m2)/1000 for value in irradiation]
        
        return production
    
    def show_production(self):
        # Get consumption data
        consumption = super().conso()
        production = self.production()  # Use the base class method

        
        # Create time values (e.g., for 7 days)
        time = np.arange(1, len(production)+1)  # Array from 1 to 7 representing time (days)

        # Generate a plot
        plt.plot(time, consumption, marker='o', linestyle='-', color='r')
        plt.plot(time, production, marker='o', linestyle='-', color='b')
        plt.title('Production over Time')
        plt.xlabel('Days')
        plt.ylabel('Production (kWh)')
        plt.grid(True)

        plt.show()

    def get_info(self):
        super().get_info()
        print(f"Surface du toit: {self.roof_m2} m²")
        print(f"Surface dispo pour panneaux photovoltaïques: {self.pv_m2} m²")
