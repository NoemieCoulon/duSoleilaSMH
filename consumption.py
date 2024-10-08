import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from datetime import datetime

# Update the file path to your CSV file
file_path = "/home/coulonn/Documents/Piste/duSoleilaSMH/consumption/Maison communale 07_2023.csv"  # Change this to the correct path

# Initialize a dictionary to store consumption data
consumption_per_hour = defaultdict(lambda: defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0}))

# Open and read the CSV file using the csv library
with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)

    # Skip the first few lines until the data starts (modify if necessary)
    for _ in range(3):  # Change this based on the actual number of header lines
        next(reader)

    # Read the data
    for row in reader:
        if len(row) < 4:
            continue  # Skip rows that don't have enough data

        date_start_str = row[0]  # Start date (e.g., "01-07-23 00:00")
        date_start = datetime.strptime(date_start_str, '%d-%m-%y %H:%M')  # Parse the date
        hour = date_start.hour  # Get the hour from the start date

        # Get consumption values for off-peak and peak hours
        heures_creuses = float(row[2]) if row[2] else 0  # Heures Creuses
        heures_pleines = float(row[3]) if row[3] else 0  # Heures Pleines

        # Store the consumption data in the dictionary
        consumption_per_hour[date_start.date()][hour]['Heures Creuses'] += heures_creuses
        consumption_per_hour[date_start.date()][hour]['Heures Pleines'] += heures_pleines

def consumption_per_month(year, month):
    # Initialize a dictionary to store hourly consumption for the entire month
    hourly_consumption = defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0, 'Count': 0})

    # Filter the data for the selected month
    for day, hours in consumption_per_hour.items():
        if day.year == year and day.month == month:
            for hour, values in hours.items():
                hourly_consumption[hour]['Heures Creuses'] += values['Heures Creuses']
                hourly_consumption[hour]['Heures Pleines'] += values['Heures Pleines']
                hourly_consumption[hour]['Count'] += 1

    # Prepare data for plotting
    total_average_list = []
    heures_creuses_list = []
    heures_pleines_list = []

    for hour in range(24):
        if hourly_consumption[hour]['Count'] > 0:
            avg_heures_creuses = hourly_consumption[hour]['Heures Creuses'] / hourly_consumption[hour]['Count']
            avg_heures_pleines = hourly_consumption[hour]['Heures Pleines'] / hourly_consumption[hour]['Count']
            total_avg = avg_heures_creuses + avg_heures_pleines

            heures_creuses_list.append(avg_heures_creuses)
            heures_pleines_list.append(avg_heures_pleines)
            total_average_list.append(total_avg)
        else:
            heures_creuses_list.append(0)
            heures_pleines_list.append(0)
            total_average_list.append(0)

    return total_average_list