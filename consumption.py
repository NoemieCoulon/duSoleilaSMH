import csv
from collections import defaultdict
from datetime import datetime

def consumption_per_month(file_path, year, month):
    # Initialize a dictionary to store consumption data
    consumption_per_hour = defaultdict(lambda: defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0, 'Count': 0}))

    # Open and read the CSV file using the csv library
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Skip the first few lines until the data starts (modify if necessary)
        for _ in range(3):  # Change this based on the actual number of header lines
            next(reader)

        # Read the data
        for row in reader:
            date_start_str = row[0]  # Start date (e.g., "01-07-23 00:00")
            date_start = datetime.strptime(date_start_str, '%d-%m-%y %H:%M')  # Parse the date
            hour = date_start.hour  # Get the hour from the start date
            day = date_start.date()

            # Get consumption values for off-peak and peak hours
            if len(row)>2:
                heures_creuses = float(row[2]) if row[2] else 0  # Heures Creuses
                consumption_per_hour[day][hour]['Heures Creuses'] += heures_creuses

            if len(row)>3:
                heures_pleines = float(row[3]) if row[3] else 0  # Heures Pleines
                consumption_per_hour[day][hour]['Heures Pleines'] += heures_pleines

            # Store the consumption data in the dictionary
            consumption_per_hour[day][hour]['Count'] += 1  # Increment the counter for each hour

    # Initialize a dictionary to store hourly consumption for the entire month
    hourly_consumption = defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0, 'Count': 0})

    # Filter the data for the selected month
    for day, hours in consumption_per_hour.items():
        if day.year == year and day.month == month:
            for hour, values in hours.items():
                hourly_consumption[hour]['Heures Creuses'] += values['Heures Creuses']
                hourly_consumption[hour]['Heures Pleines'] += values['Heures Pleines']
                hourly_consumption[hour]['Count'] += values['Count']

    # Prepare lists for plotting and calculating the average
    total_average_list = []
    heures_creuses_list = []
    heures_pleines_list = []

    # Loop over the 24 hours to calculate average consumption for each hour
    for hour in range(24):
        count = hourly_consumption[hour]['Count']
        if count > 0:
            avg_heures_creuses = hourly_consumption[hour]['Heures Creuses'] / (count)
            avg_heures_pleines = hourly_consumption[hour]['Heures Pleines'] / (count)
        else:
            avg_heures_creuses = 0
            avg_heures_pleines = 0

        heures_creuses_list.append(avg_heures_creuses)
        heures_pleines_list.append(avg_heures_pleines)
        total_average_list.append(avg_heures_creuses + avg_heures_pleines)

    return total_average_list