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
            month = current_date[4:6]  # Extract month from the date (YYYYMMDD)
            if current_date[:4] == year:  # Ensure the year matches
                hour = int(current_date[9:11])  # Extract the hour (HH)

                # Try parsing and summing irradiation values
                gb = float(row[1])
                gd = float(row[2])
                gr = float(row[3])
                
                total_irradiation = gb + gd + gr
                irradiation_per_month[month][hour] += total_irradiation
                count_per_month[month][hour] += 1  # Count occurrences for averaging

# Calculate average irradiation per hour for each month, divided by the number of days
average_irradiation_per_month = {}
for month in irradiation_per_month:
    # Get the number of days in the current month
    days_in_month = monthrange(int(year), int(month))[1]  # Access the second element of the tuple
    # Calculate average for each hour, adjusting by the number of days
    average_irradiation_per_month[month] = [
        (irradiation / (count * days_in_month)) if count > 0 else 0
        for irradiation, count in zip(irradiation_per_month[month], count_per_month[month])
    ]

# Plot the average irradiation per hour for each month
plt.figure(figsize=(12, 8))
for month, irradiation in average_irradiation_per_month.items():
    plt.plot(range(24), irradiation, linestyle='-', label=f'Month {month}')

plt.title(f'Average Irradiation per Hour for Each Month in {year}')
plt.xlabel('Hour of the Day (HH)')
plt.ylabel('Average Irradiation (W/m² per day)')
plt.xticks(range(24), [f'{hour:02d}:00' for hour in range(24)], rotation=45)
plt.grid(True)
plt.legend(title='Months', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
