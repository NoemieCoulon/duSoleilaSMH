import csv
import matplotlib.pyplot as plt
import numpy as np
from calendar import monthrange

file_path = "/home/coulonn/Documents/Piste/duSoleilaSMH/irridiation/MC_0_0.csv"

# Initialize a dictionary to store data for each hour and each month
irradiation_per_month = {f"{month:02d}": [0] * 24 for month in range(1, 13)}
count_per_month = {f"{month:02d}": [0] * 24 for month in range(1, 13)}

# Ask the user to input the year in the format YYYY
year = input("Enter the year in the format YYYY (e.g., 2023): ")

# Ask the user whether to display all months or a specific month
choice = input("Do you want to see the average irradiation for all months (A) or a specific month (S)? Enter A or S: ").strip().upper()

if choice == 'S':
    month = input("Enter the month in the format MM (e.g., 01 for January): ").strip().zfill(2)
else:
    month = None  # Set to None if we want to show all months

# Open and read the CSV file using the csv library
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    
    # Skip the metadata lines
    for _ in range(9):
        next(reader)

    # Check if month filtering works properly
    for row in reader:
        if len(row) == 8:
            current_date = row[0]
            current_month = current_date[4:6]  # Extract month from the date (YYYYMMDD)
            if current_date[:4] == year:  # Ensure the year matches
                hour = int(current_date[9:11])  # Extract the hour (HH)

                # Try parsing and summing irradiation values
                gb = float(row[1])
                gd = float(row[2])
                gr = float(row[3])
                
                total_irradiation = gb + gd + gr
                irradiation_per_month[current_month][hour] += total_irradiation
                count_per_month[current_month][hour] += 1  # Count occurrences for averaging

# Calculate average irradiation per hour for each month, divided by the number of days
average_irradiation_per_month = {}
for month_key in irradiation_per_month:
    # Get the number of days in the current month
    days_in_month = monthrange(int(year), int(month_key))[1]  # Access the second element of the tuple
    # Calculate average for each hour, adjusting by the number of days
    average_irradiation_per_month[month_key] = [
        (irradiation / (count * days_in_month)) if count > 0 else 0
        for irradiation, count in zip(irradiation_per_month[month_key], count_per_month[month_key])
    ]

# Plotting based on user choice
plt.figure(figsize=(12, 8))

if choice == 'S':
    # Display only the specific month chosen by the user
    plt.plot(range(24), average_irradiation_per_month[month], linestyle='-', label=f'Month {month}')
    plt.title(f'Average Irradiation per Hour for {month} {year} (divided by number of days)')
else:
    # Display all months
    for month_key, irradiation in average_irradiation_per_month.items():
        plt.plot(range(24), irradiation, linestyle='-', label=f'Month {month_key}')

    plt.title(f'Average Irradiation per Hour for Each Month in {year} (divided by number of days)')

plt.xlabel('Hour of the Day (HH)')
plt.ylabel('Average Irradiation (W/m² per day)')
plt.xticks(range(24), [f'{hour:02d}00' for hour in range(24)], rotation=45)
plt.grid(True)
plt.legend(title='Months', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
