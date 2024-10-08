import building_gen as build
import irridiation as irr
import matplotlib.pyplot as plt
import consumption as cons

dict_buildings = build.dict_buildings

pdl_prod = "30001931365966"
maison_communale = dict_buildings[pdl_prod]
pv_m2 = 900
print(maison_communale.name, maison_communale.roof_m2)

maison_communale.__set_pv_surface__(pv_m2)

print(maison_communale.name, maison_communale.roof_m2, maison_communale.pv_m2)

production_mc = maison_communale.production()
consumption_mc = cons.consumption_per_month(2023, 7)

# Plotting both production and consumption
plt.figure(figsize=(10, 6))

# Plot Energy Consumption
plt.plot(range(24), consumption_mc, marker='o', linestyle='-', label='Energy Consumption (kW)', color='green')

# Plot Energy Production
plt.plot(range(24), production_mc, marker='s', linestyle='--', label='Energy Production (kW)', color='blue')

# Add title and labels
plt.title('Energy Production vs. Consumption for Maison Communale in July 2023', fontsize=16)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Energy (kW)', fontsize=12)

# Customize x-axis ticks to show hourly time in 24-hour format
plt.xticks(range(24), [f'{hour}:00' for hour in range(24)])

# Add grid for better readability
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Add a legend to distinguish between production and consumption
plt.legend(loc='upper right', fontsize=10)

# Ensure the layout fits everything nicely
plt.tight_layout()

# Show the plot
plt.show()
