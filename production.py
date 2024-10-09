import building_gen as build
import irridiation as irr
import matplotlib.pyplot as plt
import consumption as cons
import numpy as np

dict_buildings = build.dict_buildings

pdl_prod = "30001931365966"
maison_communale = dict_buildings[pdl_prod]
pv_m2 = 900

pdl_hb = "30001930627304"
heure_bleue = dict_buildings[pdl_hb]

pdl_cjl = "19371345857979"
creche = dict_buildings[pdl_cjl]

maison_communale.__set_pv_surface__(pv_m2)

# Get production and consumption data
production_mc = maison_communale.production()
consumption_mc = maison_communale.conso()
# consumption_hb = heure_bleue.conso()
# consumption_cjl = creche.conso()

# Calculate the total consumption by summing up consumption across all buildings for each hour
# total_consumption = [mc + hb + cjl for mc, hb, cjl in zip(consumption_mc, consumption_hb, consumption_cjl)]
hours_day = range(24)
integral_production = np.trapz(production_mc, hours_day)
total_conso_list = []

# Loop through the monthly_consumption dictionary
for day, day_data in consumption_mc.items():
    # Loop through each entry for that day
    for entry in day_data:
        # Extract the 'Total Conso' value and append it to the list
        total_conso_list.append(entry['Total Conso'])

# Now total_conso_list will contain all the 'Total Conso' values
hours_month = range(len(total_conso_list))
integral_conso_mc = np.trapz(total_conso_list, hours_month)

economise = (integral_production)*0.1
# Plotting both production and consumption
plt.figure(figsize=(10, 6))

# Plot Energy Consumption for each building
print(len(hours_month), len(total_conso_list))
plt.plot(hours_month, total_conso_list, marker='o', linestyle='-', label='Energy Consumption'+maison_communale.name+' (kW)', color='peru')
# plt.plot(hours, consumption_hb, marker='o', linestyle='-', label='Energy Consumption HB'+ heure_bleue.name+' (kW)', color='red')
# plt.plot(hours, consumption_cjl, marker='o', linestyle='-', label='Energy Consumption CJL'+creche.name+ '(kW)', color='orange')

# Plot Total Energy Consumption
# plt.plot(hours, total_consumption, marker='x', linestyle='-', label='Total Energy Consumption (kW)', color='purple', linewidth=2)

# Plot Energy Production
# plt.plot(hours_day, production_mc, marker='s', linestyle='--', label='Energy Production MC (kW)', color='green')

# Add title and labels
plt.title('Energy Production vs. Consumption for Multiple Buildings in July 2023', fontsize=16)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Energy (kW)', fontsize=12)

# Customize x-axis ticks to show hourly time in 24-hour format
plt.xticks(hours_month, [f'{hour}:00' for hour in hours_month])

# Add grid for better readability
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Add a legend to distinguish between production, individual consumption, and total consumption
plt.legend(loc='upper right', fontsize=10)

# Ensure the layout fits everything nicely
plt.tight_layout()

# Show the plot
plt.show()
