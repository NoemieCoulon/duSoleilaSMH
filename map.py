import folium
import building_gen as buildings

c= folium.Map(location=[45.18, 5.76],zoom_start=15)

dict_buildings = buildings.dict_buildings

for name in dict_buildings:
    folium.Marker(dict_buildings[name].coordinates,popup=dict_buildings[name].name+" \nConso Annuelle: "+str(dict_buildings[name].year_consumption)).add_to(c)
c.save('maCarte.html')
