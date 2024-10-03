import folium
import building_gen as buildings
import roof_gen as roof

c= folium.Map(location=[45.18, 5.76],zoom_start=15)

dict_buildings = buildings.dict_buildings
dict_roofs = roof.dict_roofs

group_pdl = folium.FeatureGroup("Compteurs").add_to(c)
group_roof = folium.FeatureGroup("Toits").add_to(c)

for pdl in dict_buildings:
    folium.Marker(dict_buildings[pdl].coordinates,icon=folium.Icon("red"),popup=dict_buildings[pdl].name+" \nConso Annuelleaaaa: "+str(dict_buildings[pdl].year_consumption)).add_to(c)
for name in dict_roofs:    
    
    if dict_roofs[name].pdl != "NA" and dict_roofs[name].pdl!="":
        # try:
        folium.Marker(dict_buildings[dict_roofs[name].pdl].coordinates,icon=folium.Icon("blue"),popup=dict_roofs[name].name+" \nToit: "+str(dict_roofs[name].roof_m2)).add_to(c)
        # except:
            # print(dict_roofs[name].name+" Not found")
            # print("")
c.save('maCarte.html')
