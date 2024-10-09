import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from datetime import datetime

# Update the file path to your CSV file
file_path = "/home/coulonn/Documents/Piste/duSoleilaSMH/consumption/Maison_communale 07_2023.csv"  # Change this to the correct path

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

# Ask the user to choose an option
option = input("Choose an option:\n1. Graph by hour for the average of each day of the week\n2. Graph by hour for a specific day of the week\n3. Graph of average consumption per hour during the selected month\nEnter 1, 2, or 3: ")

if option == '1':
    # Calculate average energy consumption per hour for each day of the week
    year = int(input("Enter the year (YYYY): "))
    month = int(input("Enter the month (1-12): "))

    # Initialize a dictionary to store hourly consumption for each day of the week
    hourly_consumption_by_day = defaultdict(lambda: defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0, 'Count': 0}))

    # Collect data for each day of the week
    for day, hours in consumption_per_hour.items():
        if day.year == year and day.month == month:
            weekday = day.weekday()  # Get the day of the week (0=Monday, 6=Sunday)
            for hour, values in hours.items():
                hourly_consumption_by_day[weekday][hour]['Heures Creuses'] += values['Heures Creuses']
                hourly_consumption_by_day[weekday][hour]['Heures Pleines'] += values['Heures Pleines']
                hourly_consumption_by_day[weekday][hour]['Count'] += 1

    # Prepare the plot for each day of the week
    plt.figure(figsize=(14, 8))
    for weekday in range(7):  # Loop over days of the week (Monday=0, Sunday=6)
        heures_creuses_list = []
        heures_pleines_list = []
        total_list = []
        for hour in range(24):
            if hourly_consumption_by_day[weekday][hour]['Count'] > 0:
                avg_heures_creuses = hourly_consumption_by_day[weekday][hour]['Heures Creuses'] / hourly_consumption_by_day[weekday][hour]['Count']
                avg_heures_pleines = hourly_consumption_by_day[weekday][hour]['Heures Pleines'] / hourly_consumption_by_day[weekday][hour]['Count']
                avg_total = (avg_heures_creuses + avg_heures_pleines)

                heures_creuses_list.append(avg_heures_creuses)
                heures_pleines_list.append(avg_heures_pleines)
                total_list.append(avg_total)
            else:
                heures_creuses_list.append(0)
                heures_pleines_list.append(0)
                total_list.append(0)

        # Plot for this day of the week
        plt.plot(range(24), total_list, marker='o', label=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][weekday])

    # Customize the plot
    plt.title(f'Average Energy Consumption per Hour for Each Day of the Week - {month}/{year}')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Consumption (kW)')
    plt.xticks(range(24), [f'{hour}:00' for hour in range(24)])
    plt.axhline(y=0, color='black', linewidth=0.5, linestyle='--')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

elif option == '2':
    # Get month, year, and day of the week input from the user
    year = int(input("Enter the year (YYYY): "))
    month = int(input("Enter the month (1-12): "))
    day_of_week_input = input("Enter the day of the week (e.g., Monday): ")

    # Initialize a dictionary to store hourly consumption for the specific day
    hourly_consumption = defaultdict(lambda: {'Heures Creuses': 0, 'Heures Pleines': 0, 'Count': 0})

    # Map input day name to the corresponding weekday number (0=Monday, 6=Sunday)
    day_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    # Filter the data for the specific month and day of the week
    for day, hours in consumption_per_hour.items():
        if day.year == year and day.month == month:
            if day.weekday() == day_map.get(day_of_week_input):  # Check if it's the selected day of the week
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

    # Plotting the total average consumption for the selected day
    plt.figure(figsize=(12, 6))
    plt.plot(range(24), total_average_list, marker='o', label='Total Average Energy Consumption (kW)', color='green')

    # Add labels and customization
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Consumption (kW)')
    plt.title(f'Average Energy Consumption by Hour on {day_of_week_input} ({month}/{year})')
    plt.xticks(range(24), [f'{hour}:00' for hour in range(24)])
    plt.axhline(y=0, color='black', linewidth=0.5, linestyle='--')
    plt.grid()
    plt.tight_layout()
    plt.show()

elif option == '3':
    # Get month and year input from the user
    year = int(input("Enter the year (YYYY): "))
    month = int(input("Enter the month (1-12): "))

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

    # Plotting the total average consumption for the selected month
    plt.figure(figsize=(12, 6))
    plt.plot(range(24), total_average_list, marker='o', label='Total Average Energy Consumption (kW)', color='blue')

    # Add labels and customization
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Consumption (kW)')
    plt.title(f'Average Energy Consumption per Hour during {month}/{year}')
    plt.xticks(range(24), [f'{hour}:00' for hour in range(24)])
    plt.axhline(y=0, color='black', linewidth=0.5, linestyle='--')
    plt.grid()
    plt.tight_layout()
    plt.show()

else:
    print("Invalid option selected.")
