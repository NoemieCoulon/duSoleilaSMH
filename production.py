import building_gen as build
import irridiation as irr
import matplotlib.pyplot as plt
import consumption as cons
import numpy as np
from datetime import datetime, timedelta, date  # Ensure proper imports

# Load building data
dict_buildings = build.dict_buildings

pdl_prod = "30001931365966"
maison_communale = dict_buildings[pdl_prod]
pv_m2 = 900

maison_communale.__set_pv_surface__(pv_m2)

# Get production and consumption data
production_mc = maison_communale.production()
consumption_mc = maison_communale.conso()

# Prepare to extract 'Total Conso' values and corresponding hourly timestamps
total_conso_list = []
timestamps_list = []

# Loop through the consumption_mc dictionary to extract data
for day, day_data in consumption_mc.items():
    # Ensure day is treated as a datetime object
    if isinstance(day, str):
        day = datetime.strptime(day, '%Y-%m-%d')  # Adjust format if necessary
    elif isinstance(day, date):  # This check will now work correctly
        day = datetime.combine(day, datetime.min.time())  # Convert date to datetime

    # For each day, generate 24 hourly timestamps and append 'Total Conso' values
    for hour in range(24):  # Assuming each day has 24 hourly consumption values
        timestamps_list.append(day + timedelta(hours=hour))  # Append datetime for each hour
        total_conso_list.append(day_data[hour]['Total Conso'])  # Append corresponding 'Total Conso' value

# Calculate the integral for the total consumption
hours_month = range(len(total_conso_list))
integral_conso_mc = np.trapz(total_conso_list, hours_month)

# Plotting both production and consumption
plt.figure(figsize=(10, 6))

# Plot Energy Consumption for each building with timestamps on x-axis
plt.plot(timestamps_list, total_conso_list, marker='o', linestyle='-', label=f'Energy Consumption {maison_communale.name} (kW)', color='peru')

# Add title and labels
plt.title('Energy Production vs. Consumption for Multiple Buildings in July 2023', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Energy (kW)', fontsize=12)

# Customize x-axis ticks to show only dates
unique_dates = sorted(set(ts.date() for ts in timestamps_list))  # Get unique dates
plt.xticks([datetime.combine(date, datetime.min.time()) for date in unique_dates], 
           [date.strftime('%Y-%m-%d') for date in unique_dates], rotation=45)  # Set ticks to unique dates

# Add grid for better readability
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Add a legend to distinguish between production, individual consumption, and total consumption
plt.legend(loc='upper right', fontsize=10)

# Ensure the layout fits everything nicely
plt.tight_layout()

# Show the plot
plt.show()
