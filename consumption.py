import csv
from collections import defaultdict
from datetime import datetime
import os

def consumption_per_month(directory, start_date, end_date):
    # Initialize a dictionary to store consumption data
    consumption_per_hour = defaultdict(lambda: defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0, 'Tarif constant': 0, 'Count': 0}))
    existing_fieldnames = ['Date de Debut', 'Date de Fin', 'Heures Creuses Ete Distributeur<br><br>(kW)', 'Heures Pleines Ete Distributeur<br><br>(kW)', 'Consommation Distributeur<br><br>(kW)']

    # List to hold the matching CSV file paths
    donnees_files = []

    # Loop through the files in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a CSV and ends with "Donnees.csv"
            if file.endswith('Donnees.csv'):
                donnees_files.append(os.path.join(root, file))

    # Process each file found
    for file_path in donnees_files:
        with open(file_path, 'r', encoding='utf-8', newline='') as file:
            file.seek(0)
            # Skip first three header lines
            file.readline()
            file.readline()
            file.readline()
            line = file.readline().replace("�", "e")
            line = line.replace("é", "e")
            line = line.replace("\n", "")
            headers = line.split(",")
            print(file_path, "headers: ", headers)
            reader = csv.DictReader(file, fieldnames=headers, delimiter=",")
            
            # Read the data
            for row in reader:
                date_start_str = row['Date de Debut']  # Start date (e.g., "01-07-23 00:00")

                try:
                    date_start = datetime.strptime(date_start_str, '%d-%m-%y %H:%M')  # Parse the date
                except ValueError:
                    print(f"Date format error in file {file_path}: {date_start_str}")
                    continue

                # Check if the date is within the specified range
                if not (start_date <= date_start <= end_date):
                    continue  # Skip if the date is outside the range

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

    # Initialize a dictionary to store hourly consumption for all specified months
    monthly_consumption = defaultdict(list)

    # Process each day and calculate averages for the month
    for day, hours in consumption_per_hour.items():
        month = day.month
        year = day.year
        if (start_date <= datetime(year, month, 1) <= end_date):
            

            # Initialize a dictionary to hold hourly consumption for the specific month
            hourly_consumption = defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0, 'Tarif constant': 0, 'Count': 0})

            # Aggregate the data for this day into the monthly consumption
            for hour, values in hours.items():
                hourly_consumption[hour]['Heures Creuses'] += values['Heures Creuses']
                hourly_consumption[hour]['Heures Pleines'] += values['Heures Pleines']
                hourly_consumption[hour]['Tarif constant'] += values['Tarif constant']
                hourly_consumption[hour]['Count'] += values['Count']

            # Prepare lists for calculating the average for this day
            for hour in range(24):
                count = hourly_consumption[hour]['Count']
                if count > 0:
                    avg_heures_creuses = hourly_consumption[hour]['Heures Creuses'] / count
                    avg_heures_pleines = hourly_consumption[hour]['Heures Pleines'] / count
                    avg_tarif_constant = hourly_consumption[hour]['Tarif constant'] / count
                else:
                    avg_heures_creuses = 0
                    avg_heures_pleines = 0
                    avg_tarif_constant = 0

                # Append the average values for this hour to the monthly list
                monthly_consumption[day].append({
                    'Hour': hour,
                    'Heures Creuses': avg_heures_creuses,
                    'Heures Pleines': avg_heures_pleines,
                    'Tarif constant': avg_tarif_constant,
                    'Total Conso': avg_heures_creuses + avg_heures_pleines + avg_tarif_constant
                })
        
    # print(monthly_consumption)
    return monthly_consumption
