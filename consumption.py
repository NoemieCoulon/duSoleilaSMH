import csv
from collections import defaultdict
from datetime import datetime

def consumption_per_month(file_path, year, month):
    # Initialize a dictionary to store consumption data
    consumption_per_hour = defaultdict(lambda: defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0, 'Tarif constant': 0, 'Count': 0}))
    existing_fieldnames = ['Date de Debut', 'Date de Fin', 'Heures Creuses Ete Distributeur<br><br>(kW)', 'Heures Pleines Ete Distributeur<br><br>(kW)','Consommation Distributeur<br><br>(kW)']
    # Open and read the CSV file using the csv library
    with open(file_path, 'r', encoding='utf-8', newline='') as file:
        file.readline()
        file.readline()
        file.readline()
        line = file.readline().replace("�","e")
        line = line.replace("\n","")
        headers = line.split(",")
        print(file_path, headers)
        reader = csv.DictReader(file, fieldnames = headers,  delimiter=",")
        # Read the data
        for row in reader:
            date_start_str = row['Date de Debut']  # Start date (e.g., "01-07-23 00:00")
            # try:
            date_start = datetime.strptime(date_start_str, '%d-%m-%y %H:%M')  # Parse the date
            hour = date_start.hour  # Get the hour from the start date
            day = date_start.date()
            # Get consumption values for off-peak and peak hours
            
            if existing_fieldnames[2] in headers:
                heures_creuses = float(row[existing_fieldnames[2]]) if row[existing_fieldnames[2]] else 0  # Heures Creuses
                consumption_per_hour[day][hour]['Heures Creuses'] += heures_creuses

            if existing_fieldnames[3] in headers:
                heures_pleines = float(row[existing_fieldnames[3]]) if row[existing_fieldnames[3]] else 0
                consumption_per_hour[day][hour]['Heures Pleines'] += heures_pleines

            if existing_fieldnames[4] in headers:
                tarif_plein = float(row[existing_fieldnames[4]]) if row[existing_fieldnames[4]] else 0
                consumption_per_hour[day][hour]['Tarif constant'] += tarif_plein

            # Store the consumption data in the dictionary
            consumption_per_hour[day][hour]['Count'] += 1  # Increment the counter for each hour

    # Initialize a dictionary to store hourly consumption for the entire month
    hourly_consumption = defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0, 'Tarif constant' :0, 'Count': 0})

    # Filter the data for the selected month
    for day, hours in consumption_per_hour.items():
        if day.year == year and day.month == month:
            for hour, values in hours.items():
                hourly_consumption[hour]['Heures Creuses'] += values['Heures Creuses']
                hourly_consumption[hour]['Heures Pleines'] += values['Heures Pleines']
                hourly_consumption[hour]['Tarif constant'] += values['Tarif constant']
                hourly_consumption[hour]['Count'] += values['Count']

    # Prepare lists for plotting and calculating the average
    total_average_list = []
    heures_creuses_list = []
    heures_pleines_list = []
    tarif_constant_list = []

    # Loop over the 24 hours to calculate average consumption for each hour
    for hour in range(24):
        count = hourly_consumption[hour]['Count']
        if count > 0:
            avg_heures_creuses = hourly_consumption[hour]['Heures Creuses'] / (count)
            avg_heures_pleines = hourly_consumption[hour]['Heures Pleines'] / (count)
            avg_tarif_constant = hourly_consumption[hour]['Tarif constant'] / (count)
        else:
            avg_heures_creuses = 0
            avg_heures_pleines = 0
            avg_tarif_constant = 0

        heures_creuses_list.append(avg_heures_creuses)
        heures_pleines_list.append(avg_heures_pleines)
        tarif_constant_list.append(avg_tarif_constant)
        total_average_list.append(avg_heures_creuses + avg_heures_pleines+avg_tarif_constant)
    return total_average_list