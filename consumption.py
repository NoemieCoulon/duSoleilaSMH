import csv
from collections import defaultdict
from datetime import datetime
import os

def consumption_per_month(directory, start_date, end_date):
    # Initialize a dictionary to store consumption data
    consumption_per_hour = defaultdict(lambda: defaultdict(lambda: {'Heures Creuses ete': 0, 'Heures Pleines ete': 0, 'Heures Creuses hiver': 0, 'Heures Pleines hiver': 0, 'Tarif constant': 0, 'Pointe Distributeur': 0, 'Count': 0}))
    existing_fieldnames = ['Date de Debut', 'Date de Fin', 'Heures Creuses Ete Distributeur<br><br>(kW)', 'Heures Pleines Ete Distributeur<br><br>(kW)', 'Consommation Distributeur<br><br>(kW)','Heures Creuses Hiver Distributeur<br><br>(kW)','Heures Pleines Hiver Distributeur<br><br>(kW)', 'Pointe Distributeur<br><br>(kW)' ]

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
                if not (start_date <= date_start < end_date):
                    continue  # Skip if the date is outside the range

                hour = date_start.hour  # Get the hour from the start date
                day = date_start.date()

                # Get consumption values for off-peak and peak hours
                if existing_fieldnames[2] in headers:
                    heures_creuses_ete = float(row[existing_fieldnames[2]]) if row[existing_fieldnames[2]] else 0  # Heures Creuses
                    consumption_per_hour[day][hour]['Heures Creuses ete'] += heures_creuses_ete

                if existing_fieldnames[3] in headers:
                    heures_pleines_ete = float(row[existing_fieldnames[3]]) if row[existing_fieldnames[3]] else 0
                    consumption_per_hour[day][hour]['Heures Pleines ete'] += heures_pleines_ete

                if existing_fieldnames[4] in headers:
                    tarif_constant = float(row[existing_fieldnames[4]]) if row[existing_fieldnames[4]] else 0
                    consumption_per_hour[day][hour]['Tarif constant'] += tarif_constant
                
                if existing_fieldnames[5] in headers:
                    heures_creuses_hiver = float(row[existing_fieldnames[5]]) if row[existing_fieldnames[5]] else 0
                    consumption_per_hour[day][hour]['Heures Creuses hiver'] += heures_creuses_hiver

                if existing_fieldnames[6] in headers:
                    heures_pleines_hiver = float(row[existing_fieldnames[6]]) if row[existing_fieldnames[6]] else 0
                    consumption_per_hour[day][hour]['Heures Pleines hiver'] += heures_pleines_hiver
                
                if existing_fieldnames[7] in headers:
                    pointe_distributeur = float(row[existing_fieldnames[7]]) if row[existing_fieldnames[7]] else 0
                    consumption_per_hour[day][hour]['Pointe Distributeur'] += pointe_distributeur

                # Store the consumption data in the dictionary
                consumption_per_hour[day][hour]['Count'] += 1  # Increment the counter for each hour

    # Initialize a dictionary to store hourly consumption for all specified months
    monthly_consumption = defaultdict(list)
    # Process each day and calculate averages for the month
    for day, hours in consumption_per_hour.items():
        month = day.month
        year = day.year
        

        # Initialize a dictionary to hold hourly consumption for the specific month
        hourly_consumption = defaultdict(lambda: {'Heures Creuses ete': 0, 'Heures Pleines ete': 0, 'Heures Creuses hiver': 0, 'Heures Pleines hiver': 0, 'Tarif constant': 0, 'Pointe Distributeur': 0, 'Count': 0})

        # Aggregate the data for this day into the monthly consumption
        for hour, values in hours.items():
            hourly_consumption[hour]['Heures Creuses ete'] += values['Heures Creuses ete']
            hourly_consumption[hour]['Heures Creuses hiver'] += values['Heures Creuses hiver']
            hourly_consumption[hour]['Heures Pleines ete'] += values['Heures Pleines ete']
            hourly_consumption[hour]['Heures Pleines hiver'] += values['Heures Pleines hiver']
            hourly_consumption[hour]['Tarif constant'] += values['Tarif constant']
            hourly_consumption[hour]['Pointe Distributeur'] += values['Pointe Distributeur']
            hourly_consumption[hour]['Count'] += values['Count']

        # Prepare lists for calculating the average for this day
        for hour in range(24):
            count = hourly_consumption[hour]['Count']
            if count > 0:
                avg_heures_creuses_ete = hourly_consumption[hour]['Heures Creuses ete'] / count
                avg_heures_creuses_hiver = hourly_consumption[hour]['Heures Creuses hiver'] / count
                avg_heures_pleines_ete = hourly_consumption[hour]['Heures Pleines ete'] / count
                avg_heures_pleines_hiver = hourly_consumption[hour]['Heures Pleines hiver'] / count
                avg_pointe_distributeur = hourly_consumption[hour]['Pointe Distributeur'] / count
                avg_tarif_constant = hourly_consumption[hour]['Tarif constant'] / count
            else:
                avg_heures_creuses_ete = -1
                avg_heures_creuses_hiver = -1
                avg_heures_pleines_ete = -1
                avg_heures_pleines_hiver = -1
                avg_pointe_distributeur = -1
                avg_tarif_constant = -1

            total_conso = avg_heures_creuses_ete + avg_heures_pleines_ete + avg_heures_creuses_hiver + avg_heures_pleines_hiver + avg_tarif_constant + avg_pointe_distributeur

            # Append the average values for this hour to the monthly list
            monthly_consumption[day].append({
                'Hour': hour,
                'Heures Creuses ete': avg_heures_creuses_ete,
                'Heures Creuses hiver': avg_heures_creuses_hiver,
                'Heures Pleines ete': avg_heures_pleines_ete,
                'Heures Pleines hiver': avg_heures_pleines_hiver,
                'Pointe Distributeur': avg_pointe_distributeur,
                'Tarif constant': avg_tarif_constant,
                'Total Conso': total_conso
            })
    return monthly_consumption
