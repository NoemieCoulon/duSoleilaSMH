# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import irridiation as irr
import consumption as cons
from datetime import datetime, timedelta, date

class Building:
    def __init__(self, pdl, name, coordinates, year_consumption, prod_possible):
        self.pdl = pdl
        self.name = name
        self.coordinates = coordinates
        self.year_consumption = year_consumption
        self.prod_possible = prod_possible

    def conso(self, start_date, end_date):
        directory_csv = "/home/coulonn/Documents/Piste/duSoleilaSMH/consumption/csv/"+self.pdl+"/"
        consumption = cons.consumption_per_month(directory_csv, start_date, end_date)
        
        total_conso_list = []
        timestamps_list = []

        # Loop through the consumption_mc dictionary to extract data
        for day, day_data in consumption.items():
            # Ensure day is treated as a datetime object
            if isinstance(day, str):
                day = datetime.strptime(day, '%Y-%m-%d')  # Adjust format if necessary
            elif isinstance(day, date):  # This check will now work correctly
                day = datetime.combine(day, datetime.min.time())  # Convert date to datetime

            # For each day, generate 24 hourly timestamps and append 'Total Conso' values
            for hour in range(24):  # Assuming each day has 24 hourly consumption values
                timestamps_list.append(day + timedelta(hours=hour))  # Append datetime for each hour
                total_conso_list.append(day_data[hour]['Total Conso'])  # Append corresponding 'Total Conso' value


        return timestamps_list, total_conso_list

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

    def irridiation(self, start_date, end_date):
        directory_csv = "/home/coulonn/Documents/Piste/duSoleilaSMH/irridiation/MC_0_0.csv"
        irridiation = irr.irridiation(directory_csv, start_date, end_date)
        return irridiation
    
    def production(self, start_date, end_date):
        irridiation = self.irridiation(start_date, end_date)
        # Prepare to extract 'Total Irridiation' values and corresponding timestamps for solar production
        solar_power_list = []
        timestamps_list_solar = []

        # Loop through the production_mc dictionary to extract solar production data
        for timestamp, data in irridiation.items():
            if isinstance(timestamp, str):
                timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')  # Adjust format if necessary
            elif isinstance(timestamp, datetime):  # This check will now work correctly
                pass  # Timestamp is already a datetime object
            
            timestamps_list_solar.append(timestamp)  # Append timestamp
            solar_power_list.append(data['Total Irridiation'] *0.2* float(self.pv_m2)/1000)  # Append corresponding 'Total Irridiation' value and 0.2 is for the pv yield

        return timestamps_list_solar, solar_power_list
    
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
