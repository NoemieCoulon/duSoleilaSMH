import building_gen as build
import irridiation as irr
import matplotlib.pyplot as plt
import consumption as cons
import numpy as np
from datetime import datetime, timedelta, date  # Ensure proper imports

# Load building data
dict_buildings = build.dict_buildings
start_date = datetime(2023,6, 25)
end_date = datetime(2023,7, 5)

# start_date = datetime(2023,7, 15)
# end_date = datetime(2023,7, 30)

pdl_prod = "30001931365966"
maison_communale = dict_buildings[pdl_prod]
pv_m2 = 900

maison_communale.__set_pv_surface__(pv_m2)

# Get production and consumption data
timestamps_list, total_conso_list = maison_communale.conso(start_date, end_date)
timestamps_list_solar, solar_power_list = maison_communale.production(start_date, end_date)

print(f"Solar Power Data Points: {len(solar_power_list)}")
print(f"Consumption Data Points: {len(total_conso_list)}")

# Calculate the integral for the total consumption
hours_month = range(len(total_conso_list))
integral_conso_mc = np.trapz(total_conso_list, hours_month)

# Plotting both production and consumption
plt.figure(figsize=(10, 6))

# Plot Energy Consumption for each building with timestamps on x-axis
plt.plot(timestamps_list, total_conso_list, marker='o', linestyle='-', label=f'Energy Consumption {maison_communale.name} (kW)', color='peru')

# Plot Solar Power Production with corresponding timestamps
plt.plot(timestamps_list_solar, solar_power_list, marker='o', linestyle='-', label=f'Solar Power {maison_communale.name} (kW)', color='skyblue')

# Add title and labels
plt.title('Energy Production vs. Consumption for '+ maison_communale.name +' from '+str(start_date)+' to '+str(end_date), fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Energy (kW)', fontsize=12)

# Customize x-axis ticks to show only dates
unique_dates = sorted(set(ts.date() for ts in timestamps_list))  # Get unique dates from consumption timestamps
plt.xticks([datetime.combine(date, datetime.min.time()) for date in unique_dates], 
           [date.strftime('%Y-%m-%d') for date in unique_dates], rotation=45)  # Set ticks to unique dates

# Add grid for better readability
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Add a legend to distinguish between production and consumption
plt.legend(loc='upper right', fontsize=10)

# Ensure the layout fits everything nicely
plt.tight_layout()

# Show the plot
plt.show()
