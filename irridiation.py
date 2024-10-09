import csv
import matplotlib.pyplot as plt
import numpy as np
from calendar import monthrange

file_path = "/home/coulonn/Documents/Piste/duSoleilaSMH/irridiation/MC_0_0.csv"

# Initialize a dictionary to store data for each hour and each month
irradiation_per_month = {f"{month:02d}": [0] * 24 for month in range(1, 13)}
count_per_month = {f"{month:02d}": [0] * 24 for month in range(1, 13)}

def irridiation_year(year):
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

    # Calculate average irradiation per hour for each month
    average_irradiation_per_month = {}
    for month_key in irradiation_per_month:
        average_irradiation_per_month[month_key] = [
            (irradiation / count) if count > 0 else 0
            for irradiation, count in zip(irradiation_per_month[month_key], count_per_month[month_key])
        ]
    return average_irradiation_per_month
